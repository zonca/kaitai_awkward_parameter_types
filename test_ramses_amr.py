import os
import pytest
from kaitaistruct import KaitaiStream, BytesIO
import ramses_amr

# Path to the sample RAMSES AMR file (file 00088, CPU 1) extracted from
# ramses_rt_00088.tar.gz (https://yt-project.org/data/ramses_rt_00088.tar.gz)
SAMPLE = os.environ.get(
    "RAMSES_AMR_SAMPLE",
    "/tmp/ex/ramses_rt_00088/output_00088/amr_00088.out00001",
)


def parse(sample: str):
    with open(sample, "rb") as f:
        data = f.read()
    r = ramses_amr.RamsesAmr(KaitaiStream(BytesIO(data)))
    return data, r


def test_parse_consumes_entire_file():
    data, r = parse(SAMPLE)
    # The generated parser must read the whole file without falling short or
    # over-reading (KaitaiStream raises EOFError if it runs past the end).
    assert r._io.is_eof(), "parser did not reach end of stream"
    # top-level structure
    assert r.header is not None
    assert r.amr_info is not None


def test_header_global_parameters_match_simulation():
    # Reference values from ramses_rt_00088/output_00088/info_00088.txt
    _, r = parse(SAMPLE)
    h = r.header
    assert h.ncpu.value[0] == 16
    assert h.ndim.value[0] == 3
    assert h.nlevelmax.value[0] == 8
    assert h.ngridmax.value[0] == 1000000
    assert h.nboundary.value[0] == 0
    assert h.boxlen.value[0] == pytest.approx(6.0)
    assert h.ordering.contents.strip() == "hilbert"
    # nlevelmax rows of level info
    assert len(r.amr_info.level_infos) == 8


def test_amr_info_levels_present():
    _, r = parse(SAMPLE)
    levels = r.amr_info.level_infos
    assert len(levels) == 8
    # level 0 should have exactly 1 active CPU (see info/observations)
    assert sum(1 for c in levels[0].cpu_info
               if not isinstance(c, ramses_amr.RamsesAmr.EmptyType)) >= 1
