# proofs — NOT RUN (2026-11-05)

No `proof-<chunk>.json` exists for ipvv yet. emit_scholar therefore withholds
every chunk (they will all appear in `withheld_songs` until proofs PASS) — that
is correct behavior, not a failure. Do NOT hand-write PASS records.

Recipe (the gold-lane pattern, HANDOVER-G):
1. Source spans: `ipvv/site/data/sanskrit/ipvv-vol{1,2,3}.txt` (M00020/21/22) on
   disk; per-chunk byte spans live in `published/pt-passage-*.json` (`source.start/end/text`)
   → build `source/manifest.json` via `tools/intake.py` + a `workcfg` entry
   (`source`, `song_verses`, `source_spans`) for song == chunk id.
2. L0 contract conversion: R2 `l0` tarballs (see STATUS r2_key/sha) are line-level
   crown-build rows; proof B1 needs contract-shaped `T1-<chunk>.l0.jsonl` token rows
   + a report with PARSED/AMBIGUOUS/FAILED matching `parse` expectations.
3. Then per chunk: `python3 tools/proof_record.py --song <chunk> --work ipvv`
   (verify it picks up workcfg spans) → PASS record → `emit_scholar --work ipvv`.
4. Only after proofs: source_verses needs workcfg/display wiring (IPVV-IMPORT.md §G).
