# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
import collections


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class RamsesAmr(KaitaiStruct):
    SEQ_FIELDS = ["header", "amr_info"]
    def __init__(self, _io, _parent=None, _root=None):
        super(RamsesAmr, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._debug = collections.defaultdict(dict)
        self._read()

    def _read(self):
        self._debug['header']['start'] = self._io.pos()
        self.header = RamsesAmr.RamsesHeader(self._io, self, self._root)
        self._debug['header']['end'] = self._io.pos()
        self._debug['amr_info']['start'] = self._io.pos()
        self.amr_info = RamsesAmr.RamsesAmrInfo(self._io, self, self._root)
        self._debug['amr_info']['end'] = self._io.pos()


    def _fetch_instances(self):
        pass
        self.header._fetch_instances()
        self.amr_info._fetch_instances()

    class Charstring(KaitaiStruct):
        SEQ_FIELDS = ["rec_size1", "contents", "rec_size2"]
        def __init__(self, _io, _parent=None, _root=None):
            super(RamsesAmr.Charstring, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._debug = collections.defaultdict(dict)
            self._read()

        def _read(self):
            self._debug['rec_size1']['start'] = self._io.pos()
            self.rec_size1 = self._io.read_u4le()
            self._debug['rec_size1']['end'] = self._io.pos()
            self._debug['contents']['start'] = self._io.pos()
            self.contents = (self._io.read_bytes(self.rec_size1)).decode(u"ASCII")
            self._debug['contents']['end'] = self._io.pos()
            self._debug['rec_size2']['start'] = self._io.pos()
            self.rec_size2 = self._io.read_u4le()
            self._debug['rec_size2']['end'] = self._io.pos()


        def _fetch_instances(self):
            pass


    class EmptyType(KaitaiStruct):
        SEQ_FIELDS = []
        def __init__(self, _io, _parent=None, _root=None):
            super(RamsesAmr.EmptyType, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._debug = collections.defaultdict(dict)
            self._read()

        def _read(self):
            pass


        def _fetch_instances(self):
            pass


    class Fortran2dVector(KaitaiStruct):
        SEQ_FIELDS = ["rec_size1", "vector", "rec_size2"]
        def __init__(self, record_type, nrows, _io, _parent=None, _root=None):
            super(RamsesAmr.Fortran2dVector, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.record_type = record_type
            self.nrows = nrows
            self._debug = collections.defaultdict(dict)
            self._read()

        def _read(self):
            self._debug['rec_size1']['start'] = self._io.pos()
            self.rec_size1 = self._io.read_u4le()
            self._debug['rec_size1']['end'] = self._io.pos()
            self._debug['vector']['start'] = self._io.pos()
            self._debug['vector']['arr'] = []
            self._raw_vector = []
            self.vector = []
            for i in range(self.nrows):
                self._debug['vector']['arr'].append({'start': self._io.pos()})
                self._raw_vector.append(self._io.read_bytes(self.rec_size1 // self.nrows))
                _io__raw_vector = KaitaiStream(BytesIO(self._raw_vector[i]))
                self.vector.append(RamsesAmr.VectorValues(self.record_type, _io__raw_vector, self, self._root))
                self._debug['vector']['arr'][i]['end'] = self._io.pos()

            self._debug['vector']['end'] = self._io.pos()
            self._debug['rec_size2']['start'] = self._io.pos()
            self.rec_size2 = self._io.read_u4le()
            self._debug['rec_size2']['end'] = self._io.pos()


        def _fetch_instances(self):
            pass
            for i in range(len(self.vector)):
                pass
                self.vector[i]._fetch_instances()



    class FortranRecord(KaitaiStruct):
        SEQ_FIELDS = ["rec_size1", "value", "rec_size2"]
        def __init__(self, num_records, record_type, _io, _parent=None, _root=None):
            super(RamsesAmr.FortranRecord, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.num_records = num_records
            self.record_type = record_type
            self._debug = collections.defaultdict(dict)
            self._read()

        def _read(self):
            self._debug['rec_size1']['start'] = self._io.pos()
            self.rec_size1 = self._io.read_u4le()
            self._debug['rec_size1']['end'] = self._io.pos()
            self._debug['value']['start'] = self._io.pos()
            self._debug['value']['arr'] = []
            self.value = []
            for i in range(self.num_records):
                self._debug['value']['arr'].append({'start': self._io.pos()})
                _on = self.record_type
                if _on == u"f4":
                    pass
                    self.value.append(self._io.read_f4le())
                elif _on == u"f8":
                    pass
                    self.value.append(self._io.read_f8le())
                elif _on == u"u4":
                    pass
                    self.value.append(self._io.read_u4le())
                elif _on == u"u8":
                    pass
                    self.value.append(self._io.read_u8le())
                self._debug['value']['arr'][i]['end'] = self._io.pos()

            self._debug['value']['end'] = self._io.pos()
            self._debug['rec_size2']['start'] = self._io.pos()
            self.rec_size2 = self._io.read_u4le()
            self._debug['rec_size2']['end'] = self._io.pos()


        def _fetch_instances(self):
            pass
            for i in range(len(self.value)):
                pass
                _on = self.record_type
                if _on == u"f4":
                    pass
                elif _on == u"f8":
                    pass
                elif _on == u"u4":
                    pass
                elif _on == u"u8":
                    pass



    class FortranSkip(KaitaiStruct):
        SEQ_FIELDS = ["rec_size1", "contents", "rec_size2"]
        def __init__(self, _io, _parent=None, _root=None):
            super(RamsesAmr.FortranSkip, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._debug = collections.defaultdict(dict)
            self._read()

        def _read(self):
            self._debug['rec_size1']['start'] = self._io.pos()
            self.rec_size1 = self._io.read_u4le()
            self._debug['rec_size1']['end'] = self._io.pos()
            self._debug['contents']['start'] = self._io.pos()
            self.contents = self._io.read_bytes(self.rec_size1)
            self._debug['contents']['end'] = self._io.pos()
            self._debug['rec_size2']['start'] = self._io.pos()
            self.rec_size2 = self._io.read_u4le()
            self._debug['rec_size2']['end'] = self._io.pos()


        def _fetch_instances(self):
            pass


    class FortranVector(KaitaiStruct):
        SEQ_FIELDS = ["rec_size1", "vector", "rec_size2"]
        def __init__(self, record_type, _io, _parent=None, _root=None):
            super(RamsesAmr.FortranVector, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.record_type = record_type
            self._debug = collections.defaultdict(dict)
            self._read()

        def _read(self):
            self._debug['rec_size1']['start'] = self._io.pos()
            self.rec_size1 = self._io.read_u4le()
            self._debug['rec_size1']['end'] = self._io.pos()
            self._debug['vector']['start'] = self._io.pos()
            self._raw_vector = self._io.read_bytes(self.rec_size1)
            _io__raw_vector = KaitaiStream(BytesIO(self._raw_vector))
            self.vector = RamsesAmr.VectorValues(self.record_type, _io__raw_vector, self, self._root)
            self._debug['vector']['end'] = self._io.pos()
            self._debug['rec_size2']['start'] = self._io.pos()
            self.rec_size2 = self._io.read_u4le()
            self._debug['rec_size2']['end'] = self._io.pos()


        def _fetch_instances(self):
            pass
            self.vector._fetch_instances()


    class RamsesAmrInfo(KaitaiStruct):
        SEQ_FIELDS = ["level_infos"]
        def __init__(self, _io, _parent=None, _root=None):
            super(RamsesAmr.RamsesAmrInfo, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._debug = collections.defaultdict(dict)
            self._read()

        def _read(self):
            self._debug['level_infos']['start'] = self._io.pos()
            self._debug['level_infos']['arr'] = []
            self.level_infos = []
            for i in range(self._root.header.nlevelmax.value[0]):
                self._debug['level_infos']['arr'].append({'start': self._io.pos()})
                self.level_infos.append(RamsesAmr.RamsesAmrLevelInfo(i, self._io, self, self._root))
                self._debug['level_infos']['arr'][i]['end'] = self._io.pos()

            self._debug['level_infos']['end'] = self._io.pos()


        def _fetch_instances(self):
            pass
            for i in range(len(self.level_infos)):
                pass
                self.level_infos[i]._fetch_instances()



    class RamsesAmrLevelInfo(KaitaiStruct):
        SEQ_FIELDS = ["cpu_info"]
        def __init__(self, level, _io, _parent=None, _root=None):
            super(RamsesAmr.RamsesAmrLevelInfo, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.level = level
            self._debug = collections.defaultdict(dict)
            self._read()

        def _read(self):
            self._debug['cpu_info']['start'] = self._io.pos()
            self._debug['cpu_info']['arr'] = []
            self.cpu_info = []
            for i in range(self._root.header.ncpu.value[0] + self._root.header.nboundary.value[0]):
                self._debug['cpu_info']['arr'].append({'start': self._io.pos()})
                _on = self._root.header.numbl.vector[self.level].values[i]
                if _on == 0:
                    pass
                    self.cpu_info.append(RamsesAmr.EmptyType(self._io, self, self._root))
                else:
                    pass
                    self.cpu_info.append(RamsesAmr.RamsesLevelCpuInfo(self._io, self, self._root))
                self._debug['cpu_info']['arr'][i]['end'] = self._io.pos()

            self._debug['cpu_info']['end'] = self._io.pos()


        def _fetch_instances(self):
            pass
            for i in range(len(self.cpu_info)):
                pass
                _on = self._root.header.numbl.vector[self.level].values[i]
                if _on == 0:
                    pass
                    self.cpu_info[i]._fetch_instances()
                else:
                    pass
                    self.cpu_info[i]._fetch_instances()



    class RamsesHeader(KaitaiStruct):
        SEQ_FIELDS = ["ncpu", "ndim", "nx", "nlevelmax", "ngridmax", "nboundary", "ngrid_current", "boxlen", "nout", "tout", "aout", "t", "dtold", "dtnew", "nstep", "stat", "cosm", "timing", "mass_sph", "headl", "taill", "numbl", "unk1", "ngridbound", "free_mem", "ordering", "unk2"]
        def __init__(self, _io, _parent=None, _root=None):
            super(RamsesAmr.RamsesHeader, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._debug = collections.defaultdict(dict)
            self._read()

        def _read(self):
            self._debug['ncpu']['start'] = self._io.pos()
            self.ncpu = RamsesAmr.FortranRecord(1, u"u4", self._io, self, self._root)
            self._debug['ncpu']['end'] = self._io.pos()
            self._debug['ndim']['start'] = self._io.pos()
            self.ndim = RamsesAmr.FortranRecord(1, u"u4", self._io, self, self._root)
            self._debug['ndim']['end'] = self._io.pos()
            self._debug['nx']['start'] = self._io.pos()
            self.nx = RamsesAmr.FortranRecord(3, u"u4", self._io, self, self._root)
            self._debug['nx']['end'] = self._io.pos()
            self._debug['nlevelmax']['start'] = self._io.pos()
            self.nlevelmax = RamsesAmr.FortranRecord(1, u"u4", self._io, self, self._root)
            self._debug['nlevelmax']['end'] = self._io.pos()
            self._debug['ngridmax']['start'] = self._io.pos()
            self.ngridmax = RamsesAmr.FortranRecord(1, u"u4", self._io, self, self._root)
            self._debug['ngridmax']['end'] = self._io.pos()
            self._debug['nboundary']['start'] = self._io.pos()
            self.nboundary = RamsesAmr.FortranRecord(1, u"u4", self._io, self, self._root)
            self._debug['nboundary']['end'] = self._io.pos()
            self._debug['ngrid_current']['start'] = self._io.pos()
            self.ngrid_current = RamsesAmr.FortranRecord(1, u"u4", self._io, self, self._root)
            self._debug['ngrid_current']['end'] = self._io.pos()
            self._debug['boxlen']['start'] = self._io.pos()
            self.boxlen = RamsesAmr.FortranRecord(1, u"f8", self._io, self, self._root)
            self._debug['boxlen']['end'] = self._io.pos()
            self._debug['nout']['start'] = self._io.pos()
            self.nout = RamsesAmr.FortranRecord(3, u"u4", self._io, self, self._root)
            self._debug['nout']['end'] = self._io.pos()
            self._debug['tout']['start'] = self._io.pos()
            self.tout = RamsesAmr.FortranRecord(self.nout.value[0], u"f8", self._io, self, self._root)
            self._debug['tout']['end'] = self._io.pos()
            self._debug['aout']['start'] = self._io.pos()
            self.aout = RamsesAmr.FortranRecord(self.nout.value[0], u"f8", self._io, self, self._root)
            self._debug['aout']['end'] = self._io.pos()
            self._debug['t']['start'] = self._io.pos()
            self.t = RamsesAmr.FortranRecord(1, u"f8", self._io, self, self._root)
            self._debug['t']['end'] = self._io.pos()
            self._debug['dtold']['start'] = self._io.pos()
            self.dtold = RamsesAmr.FortranRecord(self.nlevelmax.value[0], u"f8", self._io, self, self._root)
            self._debug['dtold']['end'] = self._io.pos()
            self._debug['dtnew']['start'] = self._io.pos()
            self.dtnew = RamsesAmr.FortranRecord(self.nlevelmax.value[0], u"f8", self._io, self, self._root)
            self._debug['dtnew']['end'] = self._io.pos()
            self._debug['nstep']['start'] = self._io.pos()
            self.nstep = RamsesAmr.FortranRecord(2, u"u4", self._io, self, self._root)
            self._debug['nstep']['end'] = self._io.pos()
            self._debug['stat']['start'] = self._io.pos()
            self.stat = RamsesAmr.FortranRecord(3, u"f8", self._io, self, self._root)
            self._debug['stat']['end'] = self._io.pos()
            self._debug['cosm']['start'] = self._io.pos()
            self.cosm = RamsesAmr.FortranRecord(7, u"f8", self._io, self, self._root)
            self._debug['cosm']['end'] = self._io.pos()
            self._debug['timing']['start'] = self._io.pos()
            self.timing = RamsesAmr.FortranRecord(5, u"f8", self._io, self, self._root)
            self._debug['timing']['end'] = self._io.pos()
            self._debug['mass_sph']['start'] = self._io.pos()
            self.mass_sph = RamsesAmr.FortranRecord(1, u"f8", self._io, self, self._root)
            self._debug['mass_sph']['end'] = self._io.pos()
            self._debug['headl']['start'] = self._io.pos()
            self.headl = RamsesAmr.FortranVector(u"u4", self._io, self, self._root)
            self._debug['headl']['end'] = self._io.pos()
            self._debug['taill']['start'] = self._io.pos()
            self.taill = RamsesAmr.FortranVector(u"u4", self._io, self, self._root)
            self._debug['taill']['end'] = self._io.pos()
            self._debug['numbl']['start'] = self._io.pos()
            self.numbl = RamsesAmr.Fortran2dVector(u"u4", self.nlevelmax.value[0], self._io, self, self._root)
            self._debug['numbl']['end'] = self._io.pos()
            self._debug['unk1']['start'] = self._io.pos()
            self.unk1 = RamsesAmr.FortranSkip(self._io, self, self._root)
            self._debug['unk1']['end'] = self._io.pos()
            if self.nboundary.value[0] > 0:
                pass
                self._debug['ngridbound']['start'] = self._io.pos()
                self.ngridbound = RamsesAmr.FortranVector(u"u4", self._io, self, self._root)
                self._debug['ngridbound']['end'] = self._io.pos()

            self._debug['free_mem']['start'] = self._io.pos()
            self.free_mem = RamsesAmr.FortranRecord(5, u"u4", self._io, self, self._root)
            self._debug['free_mem']['end'] = self._io.pos()
            self._debug['ordering']['start'] = self._io.pos()
            self.ordering = RamsesAmr.Charstring(self._io, self, self._root)
            self._debug['ordering']['end'] = self._io.pos()
            self._debug['unk2']['start'] = self._io.pos()
            self._debug['unk2']['arr'] = []
            self.unk2 = []
            for i in range(4):
                self._debug['unk2']['arr'].append({'start': self._io.pos()})
                self.unk2.append(RamsesAmr.FortranSkip(self._io, self, self._root))
                self._debug['unk2']['arr'][i]['end'] = self._io.pos()

            self._debug['unk2']['end'] = self._io.pos()


        def _fetch_instances(self):
            pass
            self.ncpu._fetch_instances()
            self.ndim._fetch_instances()
            self.nx._fetch_instances()
            self.nlevelmax._fetch_instances()
            self.ngridmax._fetch_instances()
            self.nboundary._fetch_instances()
            self.ngrid_current._fetch_instances()
            self.boxlen._fetch_instances()
            self.nout._fetch_instances()
            self.tout._fetch_instances()
            self.aout._fetch_instances()
            self.t._fetch_instances()
            self.dtold._fetch_instances()
            self.dtnew._fetch_instances()
            self.nstep._fetch_instances()
            self.stat._fetch_instances()
            self.cosm._fetch_instances()
            self.timing._fetch_instances()
            self.mass_sph._fetch_instances()
            self.headl._fetch_instances()
            self.taill._fetch_instances()
            self.numbl._fetch_instances()
            self.unk1._fetch_instances()
            if self.nboundary.value[0] > 0:
                pass
                self.ngridbound._fetch_instances()

            self.free_mem._fetch_instances()
            self.ordering._fetch_instances()
            for i in range(len(self.unk2)):
                pass
                self.unk2[i]._fetch_instances()



    class RamsesLevelCpuInfo(KaitaiStruct):
        SEQ_FIELDS = ["grid_index", "grid_next", "grid_prev", "pos_x", "pos_y", "pos_z", "fields"]
        def __init__(self, _io, _parent=None, _root=None):
            super(RamsesAmr.RamsesLevelCpuInfo, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._debug = collections.defaultdict(dict)
            self._read()

        def _read(self):
            self._debug['grid_index']['start'] = self._io.pos()
            self.grid_index = RamsesAmr.FortranSkip(self._io, self, self._root)
            self._debug['grid_index']['end'] = self._io.pos()
            self._debug['grid_next']['start'] = self._io.pos()
            self.grid_next = RamsesAmr.FortranSkip(self._io, self, self._root)
            self._debug['grid_next']['end'] = self._io.pos()
            self._debug['grid_prev']['start'] = self._io.pos()
            self.grid_prev = RamsesAmr.FortranSkip(self._io, self, self._root)
            self._debug['grid_prev']['end'] = self._io.pos()
            self._debug['pos_x']['start'] = self._io.pos()
            self.pos_x = RamsesAmr.FortranVector(u"f8", self._io, self, self._root)
            self._debug['pos_x']['end'] = self._io.pos()
            self._debug['pos_y']['start'] = self._io.pos()
            self.pos_y = RamsesAmr.FortranVector(u"f8", self._io, self, self._root)
            self._debug['pos_y']['end'] = self._io.pos()
            self._debug['pos_z']['start'] = self._io.pos()
            self.pos_z = RamsesAmr.FortranVector(u"f8", self._io, self, self._root)
            self._debug['pos_z']['end'] = self._io.pos()
            self._debug['fields']['start'] = self._io.pos()
            self._debug['fields']['arr'] = []
            self.fields = []
            for i in range(31):
                self._debug['fields']['arr'].append({'start': self._io.pos()})
                self.fields.append(RamsesAmr.FortranSkip(self._io, self, self._root))
                self._debug['fields']['arr'][i]['end'] = self._io.pos()

            self._debug['fields']['end'] = self._io.pos()


        def _fetch_instances(self):
            pass
            self.grid_index._fetch_instances()
            self.grid_next._fetch_instances()
            self.grid_prev._fetch_instances()
            self.pos_x._fetch_instances()
            self.pos_y._fetch_instances()
            self.pos_z._fetch_instances()
            for i in range(len(self.fields)):
                pass
                self.fields[i]._fetch_instances()



    class VectorValues(KaitaiStruct):
        SEQ_FIELDS = ["values"]
        def __init__(self, record_type, _io, _parent=None, _root=None):
            super(RamsesAmr.VectorValues, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.record_type = record_type
            self._debug = collections.defaultdict(dict)
            self._read()

        def _read(self):
            self._debug['values']['start'] = self._io.pos()
            self._debug['values']['arr'] = []
            self.values = []
            i = 0
            while not self._io.is_eof():
                self._debug['values']['arr'].append({'start': self._io.pos()})
                _on = self.record_type
                if _on == u"f4":
                    pass
                    self.values.append(self._io.read_f4le())
                elif _on == u"f8":
                    pass
                    self.values.append(self._io.read_f8le())
                elif _on == u"u4":
                    pass
                    self.values.append(self._io.read_u4le())
                elif _on == u"u8":
                    pass
                    self.values.append(self._io.read_u8le())
                self._debug['values']['arr'][len(self.values) - 1]['end'] = self._io.pos()
                i += 1

            self._debug['values']['end'] = self._io.pos()


        def _fetch_instances(self):
            pass
            for i in range(len(self.values)):
                pass
                _on = self.record_type
                if _on == u"f4":
                    pass
                elif _on == u"f8":
                    pass
                elif _on == u"u4":
                    pass
                elif _on == u"u8":
                    pass




