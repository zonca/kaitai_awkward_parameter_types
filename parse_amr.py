import sys, io
from kaitaistruct import KaitaiStream, BytesIO
import ramses_amr

def main(path):
    with open(path, 'rb') as f:
        data = f.read()
    r = ramses_amr.RamsesAmr(KaitaiStream(BytesIO(data)))
    h = r.header
    print("=== RAMSES AMR header ===")
    print("ncpu        =", h.ncpu.value[0])
    print("ndim        =", h.ndim.value[0])
    print("nx          =", h.nx.value)
    print("nlevelmax   =", h.nlevelmax.value[0])
    print("ngridmax    =", h.ngridmax.value[0])
    print("nboundary   =", h.nboundary.value[0])
    print("ngrid_current =", h.ngrid_current.value[0])
    print("boxlen      =", h.boxlen.value[0])
    print("nout        =", h.nout.value)
    print("tout        =", h.tout.value)
    print("aout        =", h.aout.value)
    print("t           =", h.t.value[0])
    print("dtold       =", h.dtold.value)
    print("dtnew       =", h.dtnew.value)
    print("nstep       =", h.nstep.value)
    print("stat        =", h.stat.value)
    print("cosm        =", h.cosm.value)
    print("timing      =", h.timing.value)
    print("mass_sph    =", h.mass_sph.value)
    print("headl       =", h.headl.vector.values)
    print("taill       =", h.taill.vector.values)
    print("numbl rows  =", len(h.numbl.vector))
    for lvl in range(len(h.numbl.vector)):
        vals = h.numbl.vector[lvl].values
        print("  numbl[%d]: n=%d, head=%s" % (lvl, len(vals), vals[:8]))
    if hasattr(h, 'ngridbound'):
        print("ngridbound  =", h.ngridbound.vector.values)
    print("free_mem    =", h.free_mem.value)
    print("ordering    =", h.ordering.contents)
    print("=== amr_info ===")
    print("num levels  =", len(r.amr_info.level_infos))
    for li in r.amr_info.level_infos:
        nonempty = sum(1 for c in li.cpu_info if not isinstance(c, ramses_amr.RamsesAmr.EmptyType))
        print("  level %d: cpu_entries=%d, non_empty=%d" % (li.level, len(li.cpu_info), nonempty))
    print("=== OK: parsed %d bytes with standard Kaitai Python backend ===" % len(data))

if __name__ == '__main__':
    main(sys.argv[1])
