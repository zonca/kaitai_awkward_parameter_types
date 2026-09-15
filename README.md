# RAMSES file-format test (standard Kaitai Python backend)

Read a real RAMSES AMR output file with the **standard Kaitai Struct Python
backend** and print/verify its structure. This is the first test for the
`kaitai_awkward_parameter_types` work — deliberately **no Awkward**, just the
plain Kaitai runtime.

## Goal

Compile the existing `ramses_amr.ksy` spec to Python and parse the sample file
from the yt test dataset, printing the parsed header and AMR structure and
checking it against the values recorded in the simulation's `info_00088.txt`.

## What's here

The repo root keeps the **reusable** Kaitai spec and generated parser; the test
harness lives in `python_backend_test/`.

| File | Role |
|------|------|
| `ramses_amr.ksy` | Kaitai Struct spec (source: `data-exp-lab/astro-data-formats` `ramses_amr.ksy`). Reused by the tests. |
| `ramses_amr.py` | **Generated** parser (compiled with `ksc`, the official Kaitai Struct Compiler v0.11). Reused by the tests. |
| `requirements.txt` | Runtime deps (`kaitaistruct>=0.11`, `pytest`). |
| `python_backend_test/parse_amr.py` | CLI: parse a file and print the structure. |
| `python_backend_test/test_ramses_amr.py` | pytest: asserts the parser consumes the whole file and the header matches `info_00088.txt`. |
| `python_backend_test/verified_output.txt` | The captured verified output shown below. |

## Environment

The generated parser requires `kaitaistruct >= 0.11` (a system install of 0.10
is too old). A `uv` venv provides the runtime:

```bash
uv venv .venv --python 3.11
VIRTUAL_ENV=.venv uv pip install -r requirements.txt
```

The parser was generated from the `.ksy` with `ksc` (the official Kaitai
Struct Compiler, v0.11.0). On Debian/PureOS the compiler and its Java runtime
are installed with:

```bash
sudo apt-get install -y default-jre              # provides java
curl -sL -o ksc.deb \
  "https://github.com/kaitai-io/kaitai_struct_compiler/releases/download/0.11/kaitai-struct-compiler_0.11_all.deb"
sudo apt-get install -y ./ksc.deb

# regenerate the parser from the .ksy spec
ksc -t python --outdir . ramses_amr.ksy
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

## Run

```bash
# Print the structure
python python_backend_test/parse_amr.py ramses_rt_00088/output_00088/amr_00088.out00001

# Assertion test (sample path can be overridden via RAMSES_AMR_SAMPLE)
python -m pytest python_backend_test/test_ramses_amr.py -v
```

## Verified output (`amr_00088.out00001`)

```
=== RAMSES AMR header ===
ncpu        = 16
ndim        = 3
nx          = [1, 1, 1]
nlevelmax   = 8
ngridmax    = 1000000
nboundary   = 0
ngrid_current = 27740
boxlen      = 6.0
nout        = [1, 1, 89]
tout        = [80.0]
aout        = [1.100000023841858]
t           = 0.023160390903961547
dtold       = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.74568965605992e-06, 7.74568965605992e-06]
dtnew       = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.746136848584593e-06, 7.746136848584593e-06]
nstep       = [2610, 2610]
stat        = [0.8147596519947791, 19.816301706784884, 0.0]
cosm        = [1.0, 0.0, 0.0, 0.0, 1.0, 10.0, 0.0]
timing      = [1.0, 0.0, 1.0, 0.0, 0.0]
mass_sph    = [2e-08]
headl       = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 7, 0, 0, 8, 9, 0, 10, 14, 18, 22, 26, 29, 34, 38, 42, 46, 50, 54, 55, 59, 63, 67, 71, 106, 128, 138, 144, 148, 152, 166, 180, 186, 192, 194, 196, 199, 204, 213, 231, 514, 604, 644, 668, 676, 684, 729, 775, 787, 797, 799, 801, 807, 817, 836, 908, 3175, 3531, 3691, 3787, 3803, 3819, 3972, 4144, 4166, 4184, 4186, 4188, 4200, 4220, 4257, 4545, 22681, 24059, 24699, 25083, 25115, 25147, 25708, 26372, 26414, 26448, 26450, 26452, 26476, 26516, 26589, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
taill       = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 7, 0, 0, 8, 9, 0, 13, 17, 21, 25, 28, 33, 37, 41, 45, 49, 53, 54, 58, 62, 66, 70, 105, 127, 137, 143, 147, 151, 165, 179, 185, 191, 193, 195, 198, 203, 212, 230, 513, 603, 643, 667, 675, 683, 728, 774, 786, 796, 798, 800, 806, 816, 835, 907, 3174, 3530, 3690, 3786, 3802, 3818, 3971, 4143, 4165, 4183, 4185, 4187, 4199, 4219, 4256, 4544, 22680, 24058, 24698, 25082, 25114, 25146, 25707, 26371, 26413, 26447, 26449, 26451, 26475, 26515, 26588, 27740, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
numbl rows  = 8
  numbl[0]: n=16, head=[0, 0, 0, 0, 0, 0, 0, 0]
  numbl[1]: n=16, head=[0, 1, 0, 1, 0, 1, 0, 1]
  numbl[2]: n=16, head=[4, 4, 4, 4, 3, 5, 4, 4]
  numbl[3]: n=16, head=[35, 22, 10, 6, 4, 4, 14, 14]
  numbl[4]: n=16, head=[283, 90, 40, 24, 8, 8, 45, 46]
  numbl[5]: n=16, head=[2267, 356, 160, 96, 16, 16, 153, 172]
  numbl[6]: n=16, head=[18136, 1378, 640, 384, 32, 32, 561, 664]
  numbl[7]: n=16, head=[0, 0, 0, 0, 0, 0, 0, 0]
free_mem    = [27741, 1000000, 972260, 27740, 28849]
ordering    = hilbert                                                                                                                         
=== amr_info ===
num levels  = 8
  level 0: cpu_entries=16, non_empty=1
  level 1: cpu_entries=16, non_empty=8
  level 2: cpu_entries=16, non_empty=16
  level 3: cpu_entries=16, non_empty=16
  level 4: cpu_entries=16, non_empty=16
  level 5: cpu_entries=16, non_empty=16
  level 6: cpu_entries=16, non_empty=16
  level 7: cpu_entries=16, non_empty=0
=== OK: parsed 4467472 bytes with standard Kaitai Python backend ===
```

The parser consumed the **entire** file (`is_eof == True`, 0 bytes remaining),
and every header value matches `info_00088.txt`. `pytest`: **3 passed**
(`test_parse_consumes_entire_file`, `test_header_global_parameters_match_simulation`,
`test_amr_info_levels_present`).

## Observations / open questions

- Each `amr_00088.out000NN` file yields a different `ngrid_current` and
  different per-level `non_empty` counts, i.e. each file holds **per-CPU** AMR
  data. The `.ksy` reads the header plus a `cpu_info` record for every
  `(level, cpu)` whose `numbl` is nonzero, so per-file results are valid but
  the interpretation of "one record per nonzero numbl entry" may not yet
  capture all grids per CPU. Worth confirming with Matt/Amy.
- The `.ksy` uses `ks-opaque-types: true` and `.as<u4>` type casts; both are
  supported by the Kaitai compiler used (v0.11.0).
