#!/usr/bin/env python3
"""
Generate an annotated dump of a RAMSES AMR file parsed with the standard
Kaitai Python backend (generated with `ksc --read-pos`), as Markdown so it
renders nicely on GitHub (tables + headings).

For every field it prints: byte offset, byte size (human readable), the parsed
value (or a compact summary), and a human annotation. It also includes a legend
of every Kaitai type used in `ramses_amr.ksy` and how each maps to the binary
layout.

Usage:
    python annotate_structure.py <amr_file> > annotated_structure.md
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


def hsize(n):
    """Human-readable byte size: 12 B, 520 B, 2.3 KB, 3.5 MB, ..."""
    n = float(n)
    if n < 1024:
        return "%d B" % n
    for unit in ("KB", "MB", "GB", "TB"):
        n /= 1024.0
        if n < 1024:
            return "%.1f %s" % (n, unit)
    return "%.1f PB" % (n / 1024.0)


def _fmt(val, limit=6):
    if isinstance(val, list):
        head = ", ".join(str(v) for v in val[:limit])
        n = len(val)
        extra = ", ..." if n > limit else ""
        return "[%s%s] (n=%d)" % (head, extra, n)
    return str(val)


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


def dump_header(h):
    d = h._debug
    print("| offset | size | field | value | note |")
    print("|--------|------|-------|-------|------|")
    for name in h.SEQ_FIELDS:
        if not hasattr(h, name):
            continue
        obj = getattr(h, name)
        off = offset_of(d, name)
        size = size_of(d, name)
        cls = type(obj).__name__
        note = HEADER_NOTES.get(name, "")
        if isinstance(obj, ramses_amr.RamsesAmr.FortranRecord):
            val = "`%s`" % _fmt(obj.value)
            note = "%s [%s %s]" % (note, cls, obj.record_type)
        elif isinstance(obj, ramses_amr.RamsesAmr.FortranVector):
            val = "`%s`" % _fmt(obj.vector.values)
            note = "%s [%s %s, rec=%s]" % (note, cls, obj.record_type, hsize(obj.rec_size1))
        elif isinstance(obj, ramses_amr.RamsesAmr.Fortran2dVector):
            val = "`%dx%d u4`" % (obj.nrows, obj.rec_size1 // obj.nrows)
            note = "%s [%s, rec=%s]" % (note, cls, hsize(obj.rec_size1))
        elif isinstance(obj, ramses_amr.RamsesAmr.Charstring):
            val = "`%s`" % obj.contents.strip()
            note = "%s [%s]" % (note, cls)
        elif isinstance(obj, ramses_amr.RamsesAmr.FortranSkip):
            val = "`<skip %s>`" % hsize(obj.rec_size1)
            note = "%s [%s]" % (note, cls)
        else:
            if isinstance(obj, list):
                val = "`%d items`" % len(obj)
            else:
                val = ""
            note = "%s [%s]" % (note, cls)
        print("| `%08x` | %s | `%s` | %s | %s |" % (off, hsize(size), name, val, note))


def dump_numbl(h):
    nb = h.numbl
    total = nb._debug["vector"]["end"] - nb._debug["vector"]["start"]
    print("**total record:** %s (%d bytes, rec_size1=%s)\n" % (hsize(total), total, hsize(nb.rec_size1)))
    print("| level | n_cpu | nonzero | head (first 8) |")
    print("|-------|-------|---------|----------------|")
    for lvl, r in enumerate(nb.vector):
        vals = r.values
        nz = sum(1 for v in vals if v != 0)
        print("| %d | %d | %d | `%s` |" % (lvl, len(vals), nz, vals[:8]))


def dump_amr_info(r):
    ai = r.amr_info
    print("| level | offset | size | cpu_entries | nonempty | cpus (first 10) |")
    print("|-------|--------|------|-------------|----------|-----------------|")
    for li in ai.level_infos:
        d = li._debug
        off = offset_of(d, "cpu_info")
        size = size_of(d, "cpu_info")
        nonempty = [i for i, c in enumerate(li.cpu_info)
                    if not isinstance(c, ramses_amr.RamsesAmr.EmptyType)]
        print("| %d | `%08x` | %s | %d | %d | `%s` |" % (
            li.level, off, hsize(size), len(li.cpu_info), len(nonempty), nonempty[:10]))
    print()
    for li in ai.level_infos:
        nonempty = [i for i, c in enumerate(li.cpu_info)
                    if not isinstance(c, ramses_amr.RamsesAmr.EmptyType)]
        if not nonempty:
            continue
        g = li.cpu_info[nonempty[0]]
        d = g._debug
        print("### level %d - first nonempty CPU grid record" % li.level)
        print("| component | size | n | head (first 3) |")
        print("|-----------|------|---|----------------|")
        for f in ("grid_index", "grid_next", "grid_prev"):
            print("| `%s` (fortran_skip) | %s | - | - |" % (f, hsize(size_of(d, f))))
        for axis in ("pos_x", "pos_y", "pos_z"):
            vec = getattr(g, axis)
            print("| `%s` (fortran_vector f8) | %s | %d | `%s` |" % (
                axis, hsize(size_of(d, axis)), len(vec.vector.values), vec.vector.values[:3]))
        print("| `fields` (31 x fortran_skip) | %s | 31 | - |" % hsize(size_of(d, "fields")))
        print()


def main(path):
    data = open(path, "rb").read()
    r = ramses_amr.RamsesAmr(KaitaiStream(BytesIO(data)))

    print("# RAMSES AMR annotated structure")
    print("")
    print("- **file:** `%s`" % os.path.basename(path))
    print("- **size:** %s (%d bytes)" % (hsize(len(data)), len(data)))
    print("- **method:** standard Kaitai Python backend, parser compiled with `ksc --read-pos`")
    print("- **generated by:** `annotate_structure.py`")
    print("")
    print("## Types in `ramses_amr.ksy`")
    print("")
    print("| Type | Meaning |")
    print("|------|---------|")
    for name, desc in TYPES_LEGEND.items():
        print("| `%s` | %s |" % (name, desc))
    print("")
    print("## Header (`ramses_header`)")
    print("")
    dump_header(r.header)
    print("")
    print("## `numbl` (grids per level per CPU)")
    print("")
    dump_numbl(r.header)
    print("")
    print("## `amr_info` (one `ramses_amr_level_info` per level)")
    print("")
    dump_amr_info(r)
    print("## Total: %s (%d bytes); header + amr_info account for the whole file." % (
        hsize(len(data)), len(data)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
