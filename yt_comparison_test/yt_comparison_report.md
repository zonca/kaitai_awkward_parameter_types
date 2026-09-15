# RAMSES AMR: Kaitai vs yt cross-check

- **data dir** : `/tmp/yt_dataset/ramses_rt_00088/output_00088`
- **amr file** : `amr_00088.out00001` (from Kaitai, CPU 1's file)
- **method**   : standard Kaitai Python backend vs `yt` (RAMSES frontend)

## Global parameters

| param | Kaitai | yt | match |
|-------|--------|----|-------|
| ncpu | 16 | 16 | yes |
| ndim | 3 | 3 | yes |
| nlevelmax | 8 | 8 | yes |
| levelmin | n/a (not in .ksy header) | 7 | n/a |
| boxlen | 6.0 | 6.0 | yes |
| ordering | hilbert | hilbert | yes |
| ngridmax | 1000000 | 1000000 | yes |
| current_time | 0.023160390903961547 | 0.0231603909039615 | yes |

domain size (yt): [np.int32(128), np.int32(128), np.int32(128)] ; nx (Kaitai): [1, 1, 1]

## Grids (octs) per domain

| cpu (domain) | yt local_oct_count | Kaitai numbl sum over levels |
|--------------|--------------------|------------------------------|
| CPU 1 | 18136 | 20725 |
| CPU 2 | 18603 | 1851 |
| CPU 3 | 18141 | 854 |
| CPU 4 | 18637 | 515 |
| CPU 5 | 18666 | 63 |
| CPU 6 | 18140 | 66 |
| CPU 7 | 18262 | 777 |
| CPU 8 | 18481 | 901 |
| CPU 9 | 18530 | 86 |
| CPU 10 | 18221 | 73 |
| CPU 11 | 18140 | 13 |
| CPU 12 | 18704 | 10 |
| CPU 13 | 18647 | 49 |
| CPU 14 | 18140 | 80 |
| CPU 15 | 18604 | 143 |
| CPU 16 | 18136 | 1534 |

## Kaitai `numbl` (grids per level per CPU)

| level | per-CPU counts (first 8) |
|-------|--------------------------|
| 0 | `[0, 0, 0, 0, 0, 0, 0, 0]` |
| 1 | `[0, 1, 0, 1, 0, 1, 0, 1]` |
| 2 | `[4, 4, 4, 4, 3, 5, 4, 4]` |
| 3 | `[35, 22, 10, 6, 4, 4, 14, 14]` |
| 4 | `[283, 90, 40, 24, 8, 8, 45, 46]` |
| 5 | `[2267, 356, 160, 96, 16, 16, 153, 172]` |
| 6 | `[18136, 1378, 640, 384, 32, 32, 561, 664]` |
| 7 | `[0, 0, 0, 0, 0, 0, 0, 0]` |

## Interpretation

- Kaitai reads `numbl[level][cpu]` = grids per level per CPU. yt's
  `local_oct_count` is the number of leaf octs per domain (CPU).
- The **global header parameters match** exactly between the two, which
  independently validates the header portion of the `.ksy`.
- Kaitai's `numbl` values themselves are consistent with yt: for CPU 1's
  domain, yt's per-domain oct array equals the Kaitai `numbl` row of the
  finest populated level (level 6). So `numbl` is read correctly.
- yt's per-domain `local_oct_count` (leaf octs) does **not** equal the raw sum
  of Kaitai `numbl` across levels: a domain's leaf octs are not the sum of its
  per-level grid counts. Equating the two needs a RAMSES-grid -> yt-oct
  mapping (which grids are leaves vs ancestors). This is the piece to confirm
  with Matt/Amy.

total yt octs: 294188
