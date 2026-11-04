# works/ipvv — crown build + full R2 import (2026-11-05)

> IMPORT NOTE (svread/endgame lane): all available IPVV material pulled from R2
> (`sanskritree/ipvv-translations/`, `patala/public/published/ipvv/`, `uploads` t1-batches)
> into this directory + staged at `/root/ipvv-r2-staging/`. Read `../IPVV-IMPORT.md`
> first — it lists every source, every hash, what is NOT done (proofs, t1/l0 contract
> conversion) and the exact recipes. Proofs have NOT been run; GATE.json is explicitly
> BLOCKED/PROOF_NOT_RUN for all 49 chunks.

# works/ipvv — crown build

Status: T1 frozen (63), L0 102k real, pilot 109 real, L200 63, C1 63, published 49, SYN/ESS/EDU 0.

## Sources

- Sanskrit: Muktabodha M00020/21/22 (Vols 1–3) + Torella IPK (base). See `manifests/IPVV_MANIFEST.md`.
- R2: `sanskritree/ipvv-translations/` full list `manifests/R2-IPVV-ALL.txt`.
- Published: `patala/public/published/` list `manifests/PUBLISHED-ALL.txt`.

## What exists here (this repo)

- `process/` + `specs/` + `skills/` = pure pipe.
- `samples/` = T1/L1/L2/ARGMAP heads.
- `logs/` = calibration, lessons, stalls, FAILS.

## Next

Fix `pt:passage` vs `tantra:text` ID mismatch → READ site → backfill 3 legacy → extend Vol-3 L1.
