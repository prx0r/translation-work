# ipvv — Īśvarapratyabhijñāvivṛtivimarśinī (IPVV)

*Status: **translation machine-proposed, needs human review** — 49/49 chunks hand-closed, T1+L0 0 gaps (149,683 PARSED + 4,773 AMBIGUOUS with real glosses of 154,456 rows), schema 0 errors repo-wide, source byte-verified. Proof gate (argmap/L2/C1): 4 PASS, rest deferred by owner.*

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
| 1 | chunk-a-svatyandya | M00020 | 1921 | 1921 | 0 | 100.0 | — |
| 2 | chunk-b-eligibility-gita | M00020 | 1431 | 1431 | 0 | 100.0 | — |
| 3 | chunk-c-svatma-maya-upanishad | M00020 | 3214 | 3214 | 0 | 100.0 | — |
| 4 | chunk-d-memory-pramana | M00020 | 3146 | 3146 | 0 | 100.0 | — |
| 5 | chunk-e-cit-acid-dvairasya | M00020 | 3504 | 3504 | 0 | 100.0 | — |
| 6 | chunk-f-upoddhata-k1-7 | M00020 | 2793 | 2793 | 0 | 100.0 | — |
| 7 | chunk-g-k1-2-7-1-8-citsvarupam | M00020 | 3269 | 3269 | 0 | 100.0 | — |
| 8 | chunk-h-k1-8-caitanyamajada-pratibimba | M00020 | 3931 | 3931 | 0 | 100.0 | — |
| 9 | chunk-i-k1-9-1-10-kriya-karyakarana | M00020 | 2623 | 2623 | 0 | 100.0 | — |
| 10 | chunk-j-k1-11-kartapi-kalpita | M00020 | 770 | 772 | 0 | 100.3 | PASS |
| 11 | chunk-k-purvapaksa-siddhanta | M00020 | 2823 | 2823 | 0 | 100.0 | — |
| 12 | chunk-l-memory-error-sankaranandana | M00020 | 3205 | 3205 | 0 | 100.0 | — |
| 13 | chunk-m-jnanadhikara-reflexion-core | M00020 | 3914 | 3914 | 0 | 100.0 | — |
| 14 | chunk-n-close-mahesvara-saktis | M00020 | 3348 | 3348 | 0 | 100.0 | — |
| 15 | chunk-v2-a-caturtho-vimarsa-aham | M00021 | 2949 | 2949 | 0 | 100.0 | — |
| 16 | chunk-v2-b-sahajavimarsa-prakasavimarsa | M00021 | 3090 | 3090 | 0 | 100.0 | — |
| 17 | chunk-v2-c-vistanti-ajadapramatrsiddhi | M00021 | 2882 | 2882 | 0 | 100.0 | — |
| 18 | chunk-v2-d-pancamo-vimarsa-jnanasakti | M00021 | 3324 | 3324 | 0 | 100.0 | — |
| 19 | chunk-v2-e-pancamo-jnanasakti-k5 | M00021 | 3507 | 3507 | 0 | 100.0 | — |
| 20 | chunk-v2-f-pancamo-vimarsa-k6 | M00021 | 3550 | 3550 | 0 | 100.0 | — |
| 21 | chunk-v2-g-pancamo-vimarsa-k7-10 | M00021 | 3572 | 3572 | 0 | 100.0 | — |
| 22 | chunk-v2-h-pancamo-vimarsa-k11-13 | M00021 | 3544 | 3544 | 0 | 100.0 | — |
| 23 | chunk-v2-i-pancamo-vimarsa-k14-19 | M00021 | 3264 | 3264 | 0 | 100.0 | — |
| 24 | chunk-v2-j-pancamo-vimarsa-k19-20 | M00021 | 3570 | 3570 | 0 | 100.0 | — |
| 25 | chunk-v2-k-pancamo-vimarsa-k20-21 | M00021 | 3531 | 3531 | 0 | 100.0 | — |
| 26 | chunk-v2-l-sastho-vimarsa-smrti-apohana | M00021 | 3799 | 3799 | 0 | 100.0 | — |
| 27 | chunk-v2-m-sastho-vimarsa-k6-7 | M00021 | 3224 | 3224 | 0 | 100.0 | — |
| 28 | chunk-v2-n-sastho-k8-11 | M00021 | 1595 | 1595 | 0 | 100.0 | — |
| 29 | chunk-v2-o-saptamo-vimarsa | M00021 | 3587 | 3587 | 0 | 100.0 | — |
| 30 | chunk-v2-p-saptamo-k5-10 | M00021 | 3871 | 3871 | 0 | 100.0 | — |
| 31 | chunk-v2-q-saptamo-k11-close | M00021 | 1961 | 1961 | 0 | 100.0 | PASS |
| 32 | chunk-v2-r-astamo-vimarsa | M00021 | 3553 | 3553 | 0 | 100.0 | — |
| 33 | chunk-v2-s-astamo-close-jnanadhikara | M00021 | 910 | 910 | 0 | 100.0 | PASS |
| 34 | chunk-v3-a-kriya-prathamo-k1-2 | M00022 | 3487 | 3487 | 0 | 100.0 | — |
| 35 | chunk-v3-b-kriya-dvitiyo-k1-7 | M00022 | 5862 | 5862 | 0 | 100.0 | — |
| 36 | chunk-v3-c-kriya-trtiyo-k1-2 | M00022 | 4328 | 4328 | 0 | 100.0 | — |
| 37 | chunk-v3-d-kriya-trtiyo-k3-8 | M00022 | 4631 | 4631 | 0 | 100.0 | — |
| 38 | chunk-v3-e-kriya-trtiyo-k9-17 | M00022 | 4567 | 4567 | 0 | 100.0 | — |
| 39 | chunk-v3-f-kriya-trtiyo-close | M00022 | 2232 | 2232 | 0 | 100.0 | — |
| 40 | chunk-v3-g-kriya-caturtho-k1-11 | M00022 | 3448 | 3448 | 0 | 100.0 | — |
| 41 | chunk-v3-h-kriya-caturtho-k12-19 | M00022 | 4564 | 4564 | 0 | 100.0 | — |
| 42 | chunk-v3-i-kriya-caturtho-close-k20-21 | M00022 | 2109 | 2109 | 0 | 100.0 | — |
| 43 | chunk-v3-j-agama-prathamo-k1-7 | M00022 | 3093 | 3093 | 0 | 100.0 | — |
| 44 | chunk-v3-k-agama-prathamo-k8-11-close | M00022 | 3362 | 3362 | 0 | 100.0 | — |
| 45 | chunk-v3-l-agama-dvitiyo-k1-11 | M00022 | 2985 | 2985 | 0 | 100.0 | — |
| 46 | chunk-v3-m-agama-dvitiyo-close-k12-20 | M00022 | 3596 | 3596 | 0 | 100.0 | — |
| 47 | chunk-v3-n-tattva-prathamo-k1-8 | M00022 | 3321 | 3321 | 0 | 100.0 | — |
| 48 | chunk-v3-o-tattva-trtiyo-k9-15 | M00022 | 2814 | 2814 | 0 | 100.0 | — |
| 49 | chunk-v3-p-tattva-caturtho-close-k1-3 | M00022 | 876 | 880 | 0 | 100.5 | PASS |

Totals: **154,456 rows for 154,450 real tokens = 0 gaps** (149,683 PARSED; 4,773 AMBIGUOUS all carrying real best-effort glosses (strict audit reverted 3,044 lax promotions; unanimous-only rule kept 22) — every row machine-proposed, human review required).

Proof PASS (4): chunk-j-k1-11-kartapi-kalpita, chunk-v2-s-astamo-close-jnanadhikara, chunk-v3-p-tattva-caturtho-close-k1-3, chunk-v2-q-saptamo-k11-close

*Machine-proposed throughout — human review required before any COMPLETE marking.*
