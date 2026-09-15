# RAMSES AMR parser test (standard Kaitai Python backend)

Read a real RAMSES AMR output file with the **standard Kaitai Struct Python
backend** and print/verify its structure. This is the first test for the
`kaitai_awkward_parameter_types` work — deliberately **no Awkward**, just the
plain Kaitai runtime.

## Goal

Compile the existing `ramses_amr.ksy` spec (at the repo root) to Python and
parse the sample file from the yt test dataset, printing the parsed header and
AMR structure and checking it against the values recorded in the simulation's
`info_00088.txt`.

## What's here

| File | Role |
|------|------|
| `parse_amr.py` | CLI: parse a file and print the structure. |
| `test_ramses_amr.py` | pytest: asserts the parser consumes the whole file and the header matches `info_00088.txt`. |
| `verified_output.txt` | The captured verified output shown below. |

The `.ksy` spec and generated parser live at the **repo root** (see the root
`README.md` for setup and data download).

## Run

Run from the repo root (the test files add the root to `sys.path`, so the
generated parser is always found):

```bash
# Print the structure
python python_backend_test/parse_amr.py ramses_rt_00088/output_00088/amr_00088.out00001

# Assertion test (sample path can be overridden via RAMSES_AMR_SAMPLE)
python -m pytest python_backend_test/test_ramses_amr.py -v
```

## Verified output (`amr_00088.out00001`)

See the full text in [`verified_output.txt`](verified_output.txt). Summary from
the run:

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
t           = 0.023160390903961547
nstep       = [2610, 2610]
ordering    = hilbert
free_mem    = [27741, 1000000, 972260, 27740, 28849]
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
