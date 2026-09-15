#!/usr/bin/env python3
"""
Generate an annotated dump of a RAMSES AMR file parsed with the standard
Kaitai Python backend (generated with `ksc --read-pos`).

For every field it prints: byte offset, byte size, the parsed value (or a
compact summary), and a human annotation. It also includes a legend of every
Kaitai type used in `ramses_amr.ksy` and how each maps to the binary layout.

Usage:
    python annotate_structure.py <amr_file> > annotated_structure.txt
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaitaistruct import KaitaiStream, BytesIO
import ramses_amr


# ---- reference: all types defined in ramses_amr.ksy ----
TYPES_LEGEND = {
    "ramses_amr": "TOP-LEVEL: reads `header` (ramses_header) then `amr_info` (ramses_amr_info).",
    "ramses_header": "Holds the scalar simulation metadata (Fortran sequential records, see header table below).",
    "ramses_amr_info": "One `ramses_amr_level_info` per AMR level (nlevelmax of them).",
    "ramses_amr_level_info(level)": (
        "For each CPU index `i` in [0, ncpu+nboundary): if numbl[level][i] != 0 it "
        "reads a `ramses_level_cpu_info` (that CPU has grids at this level), else an "
        "`empty_type`."
    ),
    "ramses_level_cpu_info": (
        "One AMR grid's linked-list record: `grid_index`, `grid_next`, `grid_prev` "
        "(each a fortran_skip), `pos_x/y/z` (fortran_vector of f8), and 31 `fields` "
        "(each a fortran_skip)."
    ),
    "fortran_record(num_records, type)": (
        "[u4 rec_size1] [num_records x <type>] [u4 rec_size2]. This is a Fortran "
        "sequential unformatted record: the leading/trailing u4s are the byte count."
    ),
    "fortran_vector(type)": (
        "[u4 rec_size1] [rec_size1 bytes = values] [u4 rec_size2]. Values are read "
        "until the substream (rec_size1 bytes) is exhausted."
    ),
    "fortran_2d_vector(type, nrows)": (
        "[u4 rec_size1] [nrows sub-vectors, each rec_size1/nrows bytes] [u4 rec_size2]."
        " Used for the 2D numbl array (rows = levels, columns = CPUs)."
    ),
    "vector_values(type)": "Inner array of values; reads until end of its substream.",
    "fortran_skip": "[u4 rec_size1] [rec_size1 bytes, skipped] [u4 rec_size2].",
    "charstring": "[u4 rec_size1] [ascii string] [u4 rec_size2].",
    "empty_type": "Reads nothing (placeholder for a CPU with zero grids at a level).",
}

HEADER_NOTES = {
    "ncpu": "number of CPUs / MPI processes",
    "ndim": "number of dimensions",
    "nx": "cells per coarse grid per direction (3 values)",
    "nlevelmax": "max refinement level (levelmax; 8 here)",
    "ngridmax": "max number of AMR grids allowed",
    "nboundary": "number of boundary (dummy) domains (0 = none)",
    "ngrid_current": "active grids in this file / CPU",
    "boxlen": "box size in code units",
    "nout": "output counters (3 values)",
    "tout": "output times (first nout[0] of them)",
    "aout": "scale factor a at those output times",
    "t": "current simulation time",
    "dtold": "previous timestep per level",
    "dtnew": "new timestep per level",
    "nstep": "coarse + fine timestep counters (2 values)",
    "stat": "statistics counters (3 values)",
    "cosm": "cosmology parameters (7 values)",
    "timing": "timing records (5 values)",
    "mass_sph": "mass of sink particles (0 if none)",
    "headl": "linked-list head: first grid index per level group",
    "taill": "linked-list tail: last grid index per level group",
    "numbl": "grids per level per CPU (nlevelmax x ncpu matrix)",
    "unk1": "unused record (skipped)",
    "ngridbound": "boundary grids per level (only if nboundary > 0)",
    "free_mem": "free-memory counters (5 values)",
    "ordering": "AMR grid ordering (e.g. hilbert)",
    "unk2": "4 trailing unused records (skipped)",
}


def _fmt(val, limit=6):
    # compact value summary for long lists
    if isinstance(val, list):
        head = ", ".join(str(v) for v in val[:limit])
        n = len(val)
        extra = ", ..." if n > limit else ""
        return "[%s%s] (n=%d)" % (head, extra, n)
    return str(val)


def line(offset, size, name, value, note):
    print("  %08x  %8d  %-14s = %-42s  # %s" % (offset, size, name, value, note))


def size_of(d, name):
    try:
        return d[name]["end"] - d[name]["start"]
    except KeyError:
        return 0


def offset_of(d, name):
    try:
        return d[name]["start"]
    except KeyError:
        return 0


def dump_header(h, out):
    print("### Header (ramses_header)   offset / byte-size / value / note")
    d = h._debug
    for name in h.SEQ_FIELDS:
        if not hasattr(h, name):
            continue  # e.g. ngridbound absent when nboundary == 0
        obj = getattr(h, name)
        off = offset_of(d, name)
        size = size_of(d, name)
        cls = type(obj).__name__
        note = HEADER_NOTES.get(name, "")
        if isinstance(obj, ramses_amr.RamsesAmr.FortranRecord):
            val = _fmt(obj.value)
            print("  %08x  %8d  %-14s = %-42s  # %s [%s %s]" % (
                off, size, name, val, note, cls, obj.record_type))
        elif isinstance(obj, ramses_amr.RamsesAmr.FortranVector):
            vals = obj.vector.values
            print("  %08x  %8d  %-14s = %-42s  # %s [%s %s, rec=%d bytes]" % (
                off, size, name, _fmt(vals), note, cls, obj.record_type,
                obj.rec_size1))
        elif isinstance(obj, ramses_amr.RamsesAmr.Fortran2dVector):
            print("  %08x  %8d  %-14s = %-42s  # %s [%s rows x cols, rec=%d]" % (
                off, size, name, "%dx%d u4 matrix" % (obj.nrows, obj.rec_size1 // obj.nrows),
                note, cls, obj.rec_size1))
        elif isinstance(obj, ramses_amr.RamsesAmr.Charstring):
            print("  %08x  %8d  %-14s = %-42s  # %s [%s '%s']" % (
                off, size, name, repr(obj.contents.strip()), note, cls,
                obj.contents.strip()))
        elif isinstance(obj, ramses_amr.RamsesAmr.FortranSkip):
            print("  %08x  %8d  %-14s = %-42s  # %s [%s rec=%d bytes]" % (
                off, size, name, "<skip %d bytes>" % obj.rec_size1, note, cls,
                obj.rec_size1))
        else:
            if isinstance(obj, list):
                val = "%d items" % len(obj)
            else:
                val = ""
            print("  %08x  %8d  %-14s = %-42s  # %s [%s]" % (off, size, name, val, note, cls))


def dump_numbl(h, out):
    nb = h.numbl
    print("### numbl (grids per level per CPU)  [nlevelmax x ncpu]")
    print("  total record bytes = %d (rec_size1=%d)" % (
        nb._debug["vector"]["end"] - nb._debug["vector"]["start"], nb.rec_size1))
    for lvl, row in enumerate(nb.vector):
        vals = row.values
        nz = sum(1 for v in vals if v != 0)
        print("    level %d: n_cpu=%d nonzero=%d  head=%s" % (
            lvl, len(vals), nz, vals[:8]))


def dump_amr_info(r, out):
    ai = r.amr_info
    print("### amr_info (one ramses_amr_level_info per level)")
    for li in ai.level_infos:
        d = li._debug
        off = offset_of(d, "cpu_info")
        size = size_of(d, "cpu_info")
        nonempty = [i for i, c in enumerate(li.cpu_info)
                    if not isinstance(c, ramses_amr.RamsesAmr.EmptyType)]
        print("  level %d  offset=%08x bytes=%d  cpu_entries=%d  nonempty=%d  cpus=%s" % (
            li.level, off, size, len(li.cpu_info), len(nonempty), nonempty[:10]))
        if nonempty:
            ci = li.cpu_info[nonempty[0]]
            dump_grid_record(ci, "        ")


def dump_grid_record(g, ind):
    print(ind + "first nonempty cpu grid record:")
    d = g._debug
    print(ind + "  -- grid_index (fortran_skip) size=%d" % size_of(d, "grid_index"))
    print(ind + "  -- grid_next   (fortran_skip) size=%d" % size_of(d, "grid_next"))
    print(ind + "  -- grid_prev   (fortran_skip) size=%d" % size_of(d, "grid_prev"))
    for axis in ("pos_x", "pos_y", "pos_z"):
        vec = getattr(g, axis)
        size = size_of(d, axis)
        print(ind + "  -- %-6s (fortran_vector f8) size=%d  n=%d  head=%s" % (
            axis, size, len(vec.vector.values), _fmt(vec.vector.values, 3)))
    fsize = size_of(d, "fields")
    print(ind + "  -- fields: 31 x fortran_skip, total=%d bytes" % fsize)


def main(path):
    data = open(path, "rb").read()
    r = ramses_amr.RamsesAmr(KaitaiStream(BytesIO(data)))
    out = sys.stdout

    print("# RAMSES AMR annotated structure")
    print("# file : %s" % path)
    print("# bytes: %d" % len(data))
    print("# method: standard Kaitai Python backend, parser compiled with ksc --read-pos")
    print("# generated by annotate_structure.py")
    print("")

    print("## Types in ramses_amr.ksy")
    for name, desc in TYPES_LEGEND.items():
        print("- %-28s: %s" % (name, desc))
    print("")

    print("## Header")
    dump_header(r.header, out)
    print("")
    dump_numbl(r.header, out)
    print("")
    dump_amr_info(r, out)
    print("")
    print("## Total: parsed %d bytes; header+amr_info account for the whole file." % len(data))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
