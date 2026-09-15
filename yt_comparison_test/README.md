# yt cross-check (compare the Kaitai parse against yt)

Load the same RAMSES AMR dataset with **yt** and compare it against the
Kaitai parse produced by the main test in `../python_backend_test/`. This is
the independent check that addresses the open question: is the `.ksy` reading
the AMR structure correctly?

## Files

| File | Role |
|------|------|
| `compare_with_yt.py` | Loads the dataset with yt, parses one AMR file with the Kaitai parser, and emits a Markdown report. |
| `yt_comparison_report.md` | The generated cross-check report. |

## Setup

`yt` is installed in the project venv (alongside `kaitaistruct`):

```bash
uv venv .venv --python 3.11
VIRTUAL_ENV=.venv uv pip install -r ../requirements.txt yt
```

The dataset is the same `ramses_rt_00088.tar.gz` from `https://yt-project.org/data/`.
yt needs the `amr_*.out*` and `info_*.txt` files (the grid hierarchy comes from
the AMR files; hydro/part files are only needed for fields):

```bash
tar -xzf ramses_rt_00088.tar.gz -C <dir> \
  'ramses_rt_00088/output_00088/amr_00088.out000*' \
  'ramses_rt_00088/output_00088/info_00088.txt' \
  'ramses_rt_00088/output_00088/info_rt_00088.txt' \
  'ramses_rt_00088/output_00088/header_00088.txt'
```

## Run

```bash
export YT_DATA_DIR=/tmp/yt_dataset/ramses_rt_00088/output_00088
export RAMSES_AMR=/tmp/ex/ramses_rt_00088/output_00088/amr_00088.out00001
python compare_with_yt.py > yt_comparison_report.md
```

## What it checks and the finding

- **Global parameters** (`ncpu`, `nlevelmax`, `boxlen`, `ordering`, `ngridmax`,
  `current_time`) — these match between yt and Kaitai, independently validating
  the **header** portion of the `.ksy`.
- **Grid counts** — reading each CPU's own `amr_*.outNNN` file and computing
  `numbl[min_level:, cpu].sum()` reproduces yt's per-domain `local_oct_count`
  **exactly for all 16 CPUs**.

**Conclusion: the open question is resolved.** `numbl` is read identically by
Kaitai and yt; the AMR data is genuinely **per-CPU** (each `amr_*.outNNN` file
holds that CPU's own `numbl`), and `yt`'s per-domain oct count is simply
`numbl[min_level:, cpu].sum()`. To recover the full structure you parse one
file per CPU. The full result is in `yt_comparison_report.md`.
