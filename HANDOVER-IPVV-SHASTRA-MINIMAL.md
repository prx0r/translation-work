# HANDOVER — IPVV SHASTRA-MINIMAL (2026-11-06)

**Read after:** `SHASTRA-MINIMAL.md`, `AGENTS.md`, `tools/shastra_merge.py --help`,
`tools/proof_record.py --help` (note `--shastra`).

## State (verified 2026-11-06, check.py CANONICAL 0 failures)

- **Schemas:** 1.4.0 (`c1.essence_only`); structural release 2.1.0; `stack.json`/`DATATYPES.json` in sync.
- **IPVV intake:** `ipvv/source/{edition.txt, segments.json, manifest.json}` — 49 chunks,
  177,954 tokens, byte-verbatim vs M00020/21/22, workcfg resolves.
- **Canonical data:** 49/49 chunks have `data/<song>.t1.json` + `.l0.json` (scaffolded,
  60,846 tokens total). 3/49 have full 5-layer + proof PASS:
  - `chunk-j-k1-11-kartapi-kalpita` (772 tok, align 0.96, cites 5/5)
  - `chunk-v2-s-astamo-close-jnanadhikara` (918 tok, align 0.938, cites 4/4)
  - `chunk-v3-p-tattva-caturtho-close-k1-3` (881 tok, align 0.957, cites 5/5)
- **Partial:** `chunk-b-eligibility-gita` (596/1633 tok, 5 AMBIG, proof BLOCKED on ALIGN).
- **Remaining:** 45 chunks, 117,108 tokens (see queue below).
- **Tools landed:** `tools/shastra_merge.py`, `tools/proof_record.py --shastra`,
  `schemas/c1.py` essence_only. `tools/shastra_gaps.py` lives in `/tmp/opencode/` —
  **copy to `tools/shastra_gaps.py` before next session** (it is the gap reporter).
- **G-tables:** `ipvv/cm/<chunk>_G*.py` (hand-authored gloss batches). Keep them;
  they are the authoring record. Sidecars: `*-covered.json`, `*-status.json`.

## The loop (one chunk, end to end, no batches)

Pick the shortest-gap chunk first (queue below). For each chunk:

1. **Gap report.** `python3 tools/shastra_gaps.py <song> <verse> <v1-jsonl>` writes
   `/tmp/opencode/<song>-gap.json`. Read it. Paratext (daṇḍas, page/verse numbers,
   editorial marks) is EXCLUDED with note, never glossed (parapravesika precedent).
2. **Hand-gloss gaps.** Author `ipvv/cm/<chunk>_G<N>.py` with `G<N> = [(src_idx, gloss, grounds)]`
   and optional `<MOD>_STATUS = {src_idx: "AMBIGUOUS"}`. Rules:
   - gloss = hyphenated, compound-ordered, paren-free (schema bars parens).
   - fused compounds stay ONE row (tantrasara fused-span rule).
   - grounds cite T1-doc line (`T1D L#`) or `GRM`/`TOR`/`ARG`; if the cited line
     lacks the exact surface, mark the ground `context` honestly — never fabricate.
   - AMBIGUOUS only for real lacunae/dash-runs/print damage; never smooth.
3. **Merge.** `PYTHONPATH=ipvv/cm python3 tools/shastra_merge.py --song <s> --verse <N>
   --v1 <v1-jsonl> --gtables <G1,G2,...>`. It rebuilds T1+L0 in source order,
   reindexes L0 ids, persists `*-covered.json` + `*-status.json`.
4. **Argmap.** Convert `ipvv/pilot/pilot_V<N>_ARGUMENT_MAP.md` → `ipvv/data/<song>.argmap.json`
   (`scope: "passage"`, `structured: true`, `traces.t1_verse`, `traces.l0_ids` (hinge ids),
   `sanskrit_sha` = sha of full chunk span). Adjudicate any forks in `option_choices`.
   Validate: `python3 tools/validate_song.py --song <s> --work ipvv`.
5. **L2.** Convert `ipvv/pilot/pilot_V<N>_L2_read.md` → `ipvv/data/<song>.l2.json`:
   rename `song`/`verse_id` to the canonical song id, retrace `l0_ids` (hinge ids),
   `sanskrit_cite` = 3–5 chunk-slice substrings byte-exact in the span (split on `|`).
   Move the old transcription to `ipvv/cm/legacy-transcription-<chunk>.l2.json`.
6. **C1-essence.** Write `ipvv/data/<song>.c1.json` with `essence_only: true`,
   `renders: {}`, 3–6 lines. Bars: 0 quotes, 0 metacommentary (broad scan), 0 shared
   sentences (≥8 words) vs L2.
7. **Gates.** `python3 tools/validate_song.py --song <s> --work ipvv` → 0 errors.
   `python3 tools/proof_record.py --song <s> --work ipvv --shastra` → gate PASS.
   `python3 check.py` → CANONICAL 0 failures.
8. **STATUS.** Append song to `counts.shastra_pass` in `ipvv/STATUS.json`; update `next`.

## Queue (shortest gap first — do these before the long ones)

| # | song | verse | src tok | gap | pilot argmap |
|---|------|-------|---------|-----|--------------|
| 1 | chunk-v2-n-sastho-k8-11 | 28 | 1842 | 1144 | V2N |
| 2 | chunk-v2-q-saptamo-k11-close | 31 | 2228 | 1302 | V2Q |
| 3 | chunk-v3-i-kriya-caturtho-close-k20-21 | 42 | 2419 | 1583 | V3I |
| 4 | chunk-v3-f-kriya-trtiyo-close | 39 | 2555 | 1605 | V3F |
| 5 | chunk-i-k1-9-1-10-kriya-karyakarana | 9 | 2988 | 1943 | V1I |
| 6 | chunk-k-purvapaksa-siddhanta | 11 | 3235 | 2133 | V1K |
| 7 | chunk-a-svatyandya | 1 | 2138 | 2136 | V1A |
| 8 | chunk-v3-o-tattva-trtiyo-k9-15 | 48 | 3299 | 2172 | V3O |
| 9 | chunk-v2-a-caturtho-vimarsa-aham | 15 | 3349 | 2177 | V2A |
| 10 | chunk-f-upoddhata-k1-7 | 6 | 3203 | 2241 | V1F |
| … | (remaining 35 by ascending gap) | | | | |

Full sorted list: `python3 -c "import json,sys,os; sys.path.insert(0,'tools'); os.chdir('/root/translation-work'); from workcfg import source_spans; mp=json.load(open('ipvv/chunk-song-map.json')); r=[]; \nfor o,s in mp.items():\n t=json.load(open('ipvv/data/'+s+'.t1.json')); v=t[0]['verse']; r.append((s,v,len(source_spans('ipvv')[v]),sum(len(x.get('tokens',[])) for x in t),s))\nr.sort(key=lambda x:x[3]-x[2] if x[2] else 99999)\n[print(f\"{a:46s} v{b:3} gap={c-d}\") for a,b,c,d,_ in r]"`

## Known issues / do not touch

- `chunk-b-eligibility-gita` is a marathon (1037 gaps). Do not block on it; interleave.
- V1 T1 docs are prose, not gloss lists — do not run `t1_extract` on them expecting
  100% PARSED; the shastra loop uses chunk spans, not GRETIL markers.
- R2 keys rotate; repo is truth. Do not re-pull.
- `proof_record.py --shastra` B3 uses concat-align ratio; sub-0.90 chunks need
  recorded dispositions (`--disp`), otherwise BLOCKED.
- C2 is waived per owner (existing C2 stays; no new eli5/genz).

## Repo hygiene

- All work uncommitted (owner pushes). Run `python3 check.py` → CANONICAL 0 failures
  before every commit. Do not push.
- No secrets in tree (verified 2026-11-06).
- `ipvv/cm/` holds G-tables + sidecars + legacy L2 transcriptions — do not delete.

## Next agent: start with chunk-v2-n-sastho-k8-11 (gap 1144). It has a pilot argmap
(`pilot_V2N_ARGUMENT_MAP.md`) and L2 read. Expected: 2–3 sessions to PASS.
