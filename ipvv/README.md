# ipvv — Īśvarapratyabhijñāvivṛtivimarśinī (IPVV)

*Status: **translation machine-proposed, needs human review** — 49/49 chunks translated, word-level 95.4% (147,287/154,450 tokens), schema 98/98 PASS, source byte-verified. Proof gate (argmap/L2/C1): deferred by owner.*

## Layout (tantrasara-style: one dir per chunk)

```
ipvv/
  <chunk_id>/              # e.g. chunkA-svatyandya, chunkV2-Q-saptamo-k11-close
    SOURCE.txt             # chunk source text (from published bundle)
    SOURCE.sha             # sha256 of SOURCE.txt
    T1.md                  # the translation (edit here)
    T1.l0.jsonl            # raw L0 rows (gloss intake, in-repo)
    T1.l0.report.txt       # PARSED/AMBIGUOUS/FAILED breakdown
    STATUS.json            # per-chunk counts + proof status
    data/<song>.t1.json    # machine word-gloss layer (canonical)
    data/<song>.l0.json
    data/<song>.<layer>.json  # argmap/l2/c1 where produced
  source/                  # intake: edition.txt + segments.json + manifest (byte-verbatim)
  published/               # pt-passage bundles (source slices)
  cm/                      # gloss tables, charfill stats, residuals, reports
  proof/                   # proof records (shastra gate)
  pilot/                   # L2 prose reads + argument maps
  data/                    # COMPAT SYMLINKS -> <chunk_id>/data/ (for generic repo tools)
  STATUS.json, README.md, chunk-table.json, chunk-song-map.json
```

## Read the translation
- Per chunk: `ipvv/<chunk_id>/T1.md` (49 files — this is the translation)
- Machine gloss: `ipvv/<chunk_id>/data/<song>.t1.json`

## Regenerate / verify
```bash
# fold row glosses (idempotent; reads in-repo T1.l0.jsonl):
python3 tools/shastra_batch_fill.py
# schema check one chunk: python3 tools/validate_song.py --song <song> --work ipvv
# proof gate one chunk:    python3 tools/proof_record.py --song <song> --work ipvv --shastra
# repo gate:               python3 check.py
```

## Per-chunk coverage

| # | chunk | vol | real | glossed | missing | % | proof |
|---|-------|-----|------|---------|---------|---|-------|
| 1 | chunk-a-svatyandya | M00020 | 1921 | 378 | 1543 | 19.7 | — |
| 2 | chunk-b-eligibility-gita | M00020 | 1431 | 855 | 576 | 59.7 | — |
| 3 | chunk-c-svatma-maya-upanishad | M00020 | 3214 | 2057 | 1157 | 64.0 | — |
| 4 | chunk-d-memory-pramana | M00020 | 3146 | 2650 | 496 | 84.2 | — |
| 5 | chunk-e-cit-acid-dvairasya | M00020 | 3504 | 2977 | 527 | 85.0 | — |
| 6 | chunk-f-upoddhata-k1-7 | M00020 | 2793 | 2589 | 204 | 92.7 | — |
| 7 | chunk-g-k1-2-7-1-8-citsvarupam | M00020 | 3269 | 3135 | 134 | 95.9 ✓ | — |
| 8 | chunk-h-k1-8-caitanyamajada-pratibimba | M00020 | 3931 | 3787 | 144 | 96.3 ✓ | — |
| 9 | chunk-i-k1-9-1-10-kriya-karyakarana | M00020 | 2623 | 2487 | 136 | 94.8 | — |
| 10 | chunk-j-k1-11-kartapi-kalpita | M00020 | 770 | 770 | 0 | 100.0 ✓ | PASS |
| 11 | chunk-k-purvapaksa-siddhanta | M00020 | 2823 | 2724 | 99 | 96.5 ✓ | — |
| 12 | chunk-l-memory-error-sankaranandana | M00020 | 3205 | 3074 | 131 | 95.9 ✓ | — |
| 13 | chunk-m-jnanadhikara-reflexion-core | M00020 | 3914 | 3754 | 160 | 95.9 ✓ | — |
| 14 | chunk-n-close-mahesvara-saktis | M00020 | 3348 | 3242 | 106 | 96.8 ✓ | — |
| 15 | chunk-v2-a-caturtho-vimarsa-aham | M00021 | 2949 | 2851 | 98 | 96.7 ✓ | — |
| 16 | chunk-v2-b-sahajavimarsa-prakasavimarsa | M00021 | 3090 | 2976 | 114 | 96.3 ✓ | — |
| 17 | chunk-v2-c-vistanti-ajadapramatrsiddhi | M00021 | 2882 | 2790 | 92 | 96.8 ✓ | — |
| 18 | chunk-v2-d-pancamo-vimarsa-jnanasakti | M00021 | 3324 | 3196 | 128 | 96.1 ✓ | — |
| 19 | chunk-v2-e-pancamo-jnanasakti-k5 | M00021 | 3507 | 3425 | 82 | 97.7 ✓ | — |
| 20 | chunk-v2-f-pancamo-vimarsa-k6 | M00021 | 3550 | 3499 | 51 | 98.6 ✓ | — |
| 21 | chunk-v2-g-pancamo-vimarsa-k7-10 | M00021 | 3572 | 3532 | 40 | 98.9 ✓ | — |
| 22 | chunk-v2-h-pancamo-vimarsa-k11-13 | M00021 | 3544 | 3497 | 47 | 98.7 ✓ | — |
| 23 | chunk-v2-i-pancamo-vimarsa-k14-19 | M00021 | 3264 | 3218 | 46 | 98.6 ✓ | — |
| 24 | chunk-v2-j-pancamo-vimarsa-k19-20 | M00021 | 3570 | 3525 | 45 | 98.7 ✓ | — |
| 25 | chunk-v2-k-pancamo-vimarsa-k20-21 | M00021 | 3531 | 3478 | 53 | 98.5 ✓ | — |
| 26 | chunk-v2-l-sastho-vimarsa-smrti-apohana | M00021 | 3799 | 3746 | 53 | 98.6 ✓ | — |
| 27 | chunk-v2-m-sastho-vimarsa-k6-7 | M00021 | 3224 | 3162 | 62 | 98.1 ✓ | — |
| 28 | chunk-v2-n-sastho-k8-11 | M00021 | 1595 | 1561 | 34 | 97.9 ✓ | — |
| 29 | chunk-v2-o-saptamo-vimarsa | M00021 | 3587 | 3556 | 31 | 99.1 ✓ | — |
| 30 | chunk-v2-p-saptamo-k5-10 | M00021 | 3871 | 3841 | 30 | 99.2 ✓ | — |
| 31 | chunk-v2-q-saptamo-k11-close | M00021 | 1961 | 1940 | 21 | 98.9 ✓ | PASS |
| 32 | chunk-v2-r-astamo-vimarsa | M00021 | 3553 | 3520 | 33 | 99.1 ✓ | — |
| 33 | chunk-v2-s-astamo-close-jnanadhikara | M00021 | 910 | 910 | 0 | 100.0 ✓ | PASS |
| 34 | chunk-v3-a-kriya-prathamo-k1-2 | M00022 | 3487 | 3437 | 50 | 98.6 ✓ | — |
| 35 | chunk-v3-b-kriya-dvitiyo-k1-7 | M00022 | 5862 | 5838 | 24 | 99.6 ✓ | — |
| 36 | chunk-v3-c-kriya-trtiyo-k1-2 | M00022 | 4328 | 4298 | 30 | 99.3 ✓ | — |
| 37 | chunk-v3-d-kriya-trtiyo-k3-8 | M00022 | 4631 | 4600 | 31 | 99.3 ✓ | — |
| 38 | chunk-v3-e-kriya-trtiyo-k9-17 | M00022 | 4567 | 4490 | 77 | 98.3 ✓ | — |
| 39 | chunk-v3-f-kriya-trtiyo-close | M00022 | 2232 | 2201 | 31 | 98.6 ✓ | — |
| 40 | chunk-v3-g-kriya-caturtho-k1-11 | M00022 | 3448 | 3392 | 56 | 98.4 ✓ | — |
| 41 | chunk-v3-h-kriya-caturtho-k12-19 | M00022 | 4564 | 4512 | 52 | 98.9 ✓ | — |
| 42 | chunk-v3-i-kriya-caturtho-close-k20-21 | M00022 | 2109 | 2075 | 34 | 98.4 ✓ | — |
| 43 | chunk-v3-j-agama-prathamo-k1-7 | M00022 | 3093 | 3042 | 51 | 98.4 ✓ | — |
| 44 | chunk-v3-k-agama-prathamo-k8-11-close | M00022 | 3362 | 3324 | 38 | 98.9 ✓ | — |
| 45 | chunk-v3-l-agama-dvitiyo-k1-11 | M00022 | 2985 | 2919 | 66 | 97.8 ✓ | — |
| 46 | chunk-v3-m-agama-dvitiyo-close-k12-20 | M00022 | 3596 | 3556 | 40 | 98.9 ✓ | — |
| 47 | chunk-v3-n-tattva-prathamo-k1-8 | M00022 | 3321 | 3254 | 67 | 98.0 ✓ | — |
| 48 | chunk-v3-o-tattva-trtiyo-k9-15 | M00022 | 2814 | 2771 | 43 | 98.5 ✓ | — |
| 49 | chunk-v3-p-tattva-caturtho-close-k1-3 | M00022 | 876 | 876 | 0 | 100.0 ✓ | PASS |

Totals: **147,287/154,450 = 95.4%** glossed. Missing 7,163 tokens concentrated in vol1 A–E (thin row intake — prose T1 docs cover them).

Proof PASS (4): chunk-j-k1-11-kartapi-kalpita, chunk-v2-s-astamo-close-jnanadhikara, chunk-v3-p-tattva-caturtho-close-k1-3, chunk-v2-q-saptamo-k11-close

*Machine-proposed throughout — human review required before any COMPLETE marking.*
