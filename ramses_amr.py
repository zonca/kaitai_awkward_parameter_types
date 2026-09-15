# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class RamsesAmr(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(RamsesAmr, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.header = RamsesAmr.RamsesHeader(self._io, self, self._root)
        self.amr_info = RamsesAmr.RamsesAmrInfo(self._io, self, self._root)


    def _fetch_instances(self):
        pass
        self.header._fetch_instances()
        self.amr_info._fetch_instances()

    class Charstring(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(RamsesAmr.Charstring, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.rec_size1 = self._io.read_u4le()
            self.contents = (self._io.read_bytes(self.rec_size1)).decode(u"ASCII")
            self.rec_size2 = self._io.read_u4le()


        def _fetch_instances(self):
            pass


    class EmptyType(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(RamsesAmr.EmptyType, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            pass


        def _fetch_instances(self):
            pass


    class Fortran2dVector(KaitaiStruct):
        def __init__(self, record_type, nrows, _io, _parent=None, _root=None):
            super(RamsesAmr.Fortran2dVector, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.record_type = record_type
            self.nrows = nrows
            self._read()

        def _read(self):
            self.rec_size1 = self._io.read_u4le()
            self._raw_vector = []
            self.vector = []
            for i in range(self.nrows):
                self._raw_vector.append(self._io.read_bytes(self.rec_size1 // self.nrows))
                _io__raw_vector = KaitaiStream(BytesIO(self._raw_vector[i]))
                self.vector.append(RamsesAmr.VectorValues(self.record_type, _io__raw_vector, self, self._root))

            self.rec_size2 = self._io.read_u4le()


        def _fetch_instances(self):
            pass
            for i in range(len(self.vector)):
                pass
                self.vector[i]._fetch_instances()



    class FortranRecord(KaitaiStruct):
        def __init__(self, num_records, record_type, _io, _parent=None, _root=None):
            super(RamsesAmr.FortranRecord, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.num_records = num_records
            self.record_type = record_type
            self._read()

        def _read(self):
            self.rec_size1 = self._io.read_u4le()
            self.value = []
            for i in range(self.num_records):
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

            self.rec_size2 = self._io.read_u4le()


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
        def __init__(self, _io, _parent=None, _root=None):
            super(RamsesAmr.FortranSkip, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.rec_size1 = self._io.read_u4le()
            self.contents = self._io.read_bytes(self.rec_size1)
            self.rec_size2 = self._io.read_u4le()


        def _fetch_instances(self):
            pass


    class FortranVector(KaitaiStruct):
        def __init__(self, record_type, _io, _parent=None, _root=None):
            super(RamsesAmr.FortranVector, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.record_type = record_type
            self._read()

        def _read(self):
            self.rec_size1 = self._io.read_u4le()
            self._raw_vector = self._io.read_bytes(self.rec_size1)
            _io__raw_vector = KaitaiStream(BytesIO(self._raw_vector))
            self.vector = RamsesAmr.VectorValues(self.record_type, _io__raw_vector, self, self._root)
            self.rec_size2 = self._io.read_u4le()


        def _fetch_instances(self):
            pass
            self.vector._fetch_instances()


    class RamsesAmrInfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(RamsesAmr.RamsesAmrInfo, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.level_infos = []
            for i in range(self._root.header.nlevelmax.value[0]):
                self.level_infos.append(RamsesAmr.RamsesAmrLevelInfo(i, self._io, self, self._root))



        def _fetch_instances(self):
            pass
            for i in range(len(self.level_infos)):
                pass
                self.level_infos[i]._fetch_instances()



    class RamsesAmrLevelInfo(KaitaiStruct):
        def __init__(self, level, _io, _parent=None, _root=None):
            super(RamsesAmr.RamsesAmrLevelInfo, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.level = level
            self._read()

        def _read(self):
            self.cpu_info = []
            for i in range(self._root.header.ncpu.value[0] + self._root.header.nboundary.value[0]):
                _on = self._root.header.numbl.vector[self.level].values[i]
                if _on == 0:
                    pass
                    self.cpu_info.append(RamsesAmr.EmptyType(self._io, self, self._root))
                else:
                    pass
                    self.cpu_info.append(RamsesAmr.RamsesLevelCpuInfo(self._io, self, self._root))



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
        def __init__(self, _io, _parent=None, _root=None):
            super(RamsesAmr.RamsesHeader, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.ncpu = RamsesAmr.FortranRecord(1, u"u4", self._io, self, self._root)
            self.ndim = RamsesAmr.FortranRecord(1, u"u4", self._io, self, self._root)
            self.nx = RamsesAmr.FortranRecord(3, u"u4", self._io, self, self._root)
            self.nlevelmax = RamsesAmr.FortranRecord(1, u"u4", self._io, self, self._root)
            self.ngridmax = RamsesAmr.FortranRecord(1, u"u4", self._io, self, self._root)
            self.nboundary = RamsesAmr.FortranRecord(1, u"u4", self._io, self, self._root)
            self.ngrid_current = RamsesAmr.FortranRecord(1, u"u4", self._io, self, self._root)
            self.boxlen = RamsesAmr.FortranRecord(1, u"f8", self._io, self, self._root)
            self.nout = RamsesAmr.FortranRecord(3, u"u4", self._io, self, self._root)
            self.tout = RamsesAmr.FortranRecord(self.nout.value[0], u"f8", self._io, self, self._root)
            self.aout = RamsesAmr.FortranRecord(self.nout.value[0], u"f8", self._io, self, self._root)
            self.t = RamsesAmr.FortranRecord(1, u"f8", self._io, self, self._root)
            self.dtold = RamsesAmr.FortranRecord(self.nlevelmax.value[0], u"f8", self._io, self, self._root)
            self.dtnew = RamsesAmr.FortranRecord(self.nlevelmax.value[0], u"f8", self._io, self, self._root)
            self.nstep = RamsesAmr.FortranRecord(2, u"u4", self._io, self, self._root)
            self.stat = RamsesAmr.FortranRecord(3, u"f8", self._io, self, self._root)
            self.cosm = RamsesAmr.FortranRecord(7, u"f8", self._io, self, self._root)
            self.timing = RamsesAmr.FortranRecord(5, u"f8", self._io, self, self._root)
            self.mass_sph = RamsesAmr.FortranRecord(1, u"f8", self._io, self, self._root)
            self.headl = RamsesAmr.FortranVector(u"u4", self._io, self, self._root)
            self.taill = RamsesAmr.FortranVector(u"u4", self._io, self, self._root)
            self.numbl = RamsesAmr.Fortran2dVector(u"u4", self.nlevelmax.value[0], self._io, self, self._root)
            self.unk1 = RamsesAmr.FortranSkip(self._io, self, self._root)
            if self.nboundary.value[0] > 0:
                pass
                self.ngridbound = RamsesAmr.FortranVector(u"u4", self._io, self, self._root)

            self.free_mem = RamsesAmr.FortranRecord(5, u"u4", self._io, self, self._root)
            self.ordering = RamsesAmr.Charstring(self._io, self, self._root)
            self.unk2 = []
            for i in range(4):
                self.unk2.append(RamsesAmr.FortranSkip(self._io, self, self._root))



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
        def __init__(self, _io, _parent=None, _root=None):
            super(RamsesAmr.RamsesLevelCpuInfo, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.grid_index = RamsesAmr.FortranSkip(self._io, self, self._root)
            self.grid_next = RamsesAmr.FortranSkip(self._io, self, self._root)
            self.grid_prev = RamsesAmr.FortranSkip(self._io, self, self._root)
            self.pos_x = RamsesAmr.FortranVector(u"f8", self._io, self, self._root)
            self.pos_y = RamsesAmr.FortranVector(u"f8", self._io, self, self._root)
            self.pos_z = RamsesAmr.FortranVector(u"f8", self._io, self, self._root)
            self.fields = []
            for i in range(31):
                self.fields.append(RamsesAmr.FortranSkip(self._io, self, self._root))



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
        def __init__(self, record_type, _io, _parent=None, _root=None):
            super(RamsesAmr.VectorValues, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self.record_type = record_type
            self._read()

        def _read(self):
            self.values = []
            i = 0
            while not self._io.is_eof():
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
                i += 1



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




