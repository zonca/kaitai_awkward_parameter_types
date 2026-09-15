# RAMSES Kaitai spec and generated Python parser

Kaitai Struct spec (`ramses_amr.ksy`) and its generated Python parser
(`ramses_amr.py`) for RAMSES AMR output files. The actual parser test lives in
[`python_backend_test/`](python_backend_test/README.md).

## What's here

| File | Role |
|------|------|
| `ramses_amr.ksy` | Kaitai Struct spec (source: `data-exp-lab/astro-data-formats` `ramses_amr.ksy`). |
| `ramses_amr.py` | **Generated** parser (compiled with `ksc`, the official Kaitai Struct Compiler v0.11). |
| `requirements.txt` | Runtime deps (`kaitaistruct>=0.11`, `pytest`). |
| `python_backend_test/` | The test harness (see its README). |
| `yt_comparison_test/` | Cross-checks the Kaitai parse against `yt` (see its README). |

## Environment

The generated parser requires `kaitaistruct >= 0.11` (a system install of 0.10
is too old). A `uv` venv provides the runtime:

```bash
uv venv .venv --python 3.11
VIRTUAL_ENV=.venv uv pip install -r requirements.txt
```

## Generate the parser with `ksc`

Install the compiler and its Java runtime on Debian/PureOS:

```bash
sudo apt-get install -y default-jre              # provides java
curl -sL -o ksc.deb \
  "https://github.com/kaitai-io/kaitai_struct_compiler/releases/download/0.11/kaitai-struct-compiler_0.11_all.deb"
sudo apt-get install -y ./ksc.deb

# regenerate the parser from the .ksy spec (--read-pos records byte offsets,
# used by the annotated-structure tool in python_backend_test/)
ksc -t python --read-pos --outdir . ramses_amr.ksy
```

(`ksc` emits a few style warnings for this spec — `num_vector` vs `nrows`,
canonical `ASCII`, etc. — that are harmless.)

## Data

Dataset: `ramses_rt_00088.tar.gz` from `https://yt-project.org/data/`
(~646 MB). The AMR structure is split per-CPU into files
`amr_00088.out00001`..`.out00016`. **Do not commit the data** (ignore
`*.tar.gz`, `*.out`).

```bash
curl -sL -o ramses_rt_00088.tar.gz \
  "https://yt-project.org/data/ramses_rt_00088.tar.gz"
tar -xzf ramses_rt_00088.tar.gz \
  'ramses_rt_00088/output_00088/amr_00088.out00001' \
  'ramses_rt_00088/output_00088/info_00088.txt'
```

Reference global values (from `info_00088.txt`): ncpu=16, ndim=3,
nlevelmax=8, ngridmax=1000000, boxlen=6.0, ordering="hilbert", nboundary=0.

## Notes / gotchas

- **`ksc -d` short form fails on Unix** ("Is a directory") — use the long form
  `--outdir` (the ones in this README do).
- **The AMR data is per-CPU**: `ramses_rt_00088/output_00088/amr_00088.out00001`
  .. `.out00016` each hold one CPU's data (its own `numbl`). yt reads each file
  separately; its per-domain oct count is `numbl[min_level:, cpu].sum()`. To
  reconstruct the whole AMR tree, parse one file per CPU. See
  [`yt_comparison_test/`](yt_comparison_test/README.md).
- **`nx` in the header (`[1,1,1]`) is not the domain size** — it is the number of
  root coarse cells per direction; yt's `domain_dimensions` (`[128,128,128]`) is
  the base grid resolution (`2**levelmin`). They measure different things.
- `ksc` prints harmless style warnings for this spec (`num_vector` vs `nrows`,
  canonical `ASCII`, etc.).

## Test

See [`python_backend_test/README.md`](python_backend_test/README.md) for how to
run the parser test and its verified output.
