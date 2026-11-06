# REVIEW — IPVV śāstra-minimal build, 2026-11-06

*Full audit of this session's work against SHASTRA-MINIMAL.md + the repo's
absolute bars (mistakes.md). Machine-proposed review; no work re-run, no
files rewritten besides this one.*

## 1. Scoreboard (verified by direct file reads)

| Metric | Value |
|---|---|
| Source (workcfg, sha-intake) | 49 chunks / 177,954 tokens |
| T1 tokens in `ipvv/data/` | 60,846 (34%) |
| Chunks with all 5 layers | 4 (chunkJ, V2-N, V2-S, V3-P) |
| **Proof PASS** | **3 — chunkJ, V2-S, V3-P** |
| Proof BLOCKED | 2 (chunkB: ALIGN 0.459 + C1/L2 missing; V2-N: ALIGN 0.303) |
| Proof files written | 5 (others have inventory receipts only) |
| Scaffolded T1+L0 only | 44 chunks |
| `check.py` | CANONICAL 0 failures (re-run twice) |
| Registry header | stale: gold 71 vs actual 72 (pre-existing drift) |

Per-chunk PASS details: chunkJ 772 tok, align 0.960, cites 5/5 ·
V2-S 918 tok, align 0.938, cites 4/4 · V3-P 881 tok, align 0.957, cites 5/5.
All three: validate_song 0 errors, C1 0 quotes/0 meta/0 shared≥8w, argmap
traces resolve, machine-proposed (needs=human-review).

## 2. What landed (keep — do not rebuild)

- `SHASTRA-MINIMAL.md` — layer contract: SOURCE → T1 → L0 → ARGMAP → L2 →
  C1-essence (+Proof-SHASTRA). L3/L4/C2 waived for śāstra; verdict-able spec.
- **Schemas 1.4.0**: `schemas/c1.py` `essence_only` (renders {} allowed);
  `SCHEMA_VERSION`, `stack.json` (1.3.0), `DATATYPES.json` (1.4.0),
  `check.py` pins updated; structural release `schemas/releases/2.1.0.json`.
  Classic path regression-tested (sivastotravali s01 proof PASS with --disp).
- **IPVV intake (verified)**: `ipvv/source/{edition.txt 2,041,720 B,
  segments.json 49, manifest.json sha=db44b7ce}`; all 49 bundle slices
  byte-verbatim vs M00020/21/22 (49/49 exact-sha vs `source/volumes/*.json`);
  `workcfg` kind=segments resolves; song ids normalized
  (`chunk-song-map.json`, `chunk-table.json`).
- **Tools** (in-repo, all used this session):
  - `tools/shastra_merge.py` — T1+L0 rebuild from G-tables, source-ordered,
    L0-id reindex, `*-covered.json` + `*-status.json` sidecars, idempotent.
  - `tools/proof_record.py --shastra` — chunk-span source, contract data JSON,
    chunk-slice cites, C1-essence; B1-B8 otherwise unchanged.
  - `tools/shastra_autogloss.py` — lifts hand glosses from frozen T1 docs +
    v1 rows (assembly only, never authors).
  - `tools/shastra_convert_chunk.py` — pilot→argmap/L2/C1 converter
    (pilot_label fixed: `chunk_id[5].upper()` for vol1; **never run end-to-end**
    on a vol1 chunk — its only run was V2-N via the earlier path).
  - `ipvv/cm/measure-all.py` — gap reporter.
- **Hand-gloss authoring records**: 23 G-tables in `ipvv/cm/`
  (chunkJ G1-G5, v2s G1-G4, v3p G1-G4, chunkB G1-G6, v2n Gauto) — these are
  the authored-content ledger for what's glossed; keep, don't regenerate.
- `HANDOVER-IPVV-SHASTRA-MINIMAL.md` — next-steps handover (queue + loop).
- `ipvv/proof/inventory-*.json` × 49 — presence receipts (gate=INVENTORY,
  explicitly NOT gold PASS).
- `ipvv/STATUS.json` — shastra_pass list + notes current.

## 3. Defects found (fix before any new PASS claim)

**D1 — paratext glossed in 2 of 3 PASS chunks (9 rows). Real, gate-invisible.**
- V2-S: 8 paratext rows carry English glosses — 4 daṇḍas
  (`|` → in-non-becoming / thus / that-very-and / purity-impurity), 2 `|]`
  (→ close-bracket), 2 verse numbers (`9`→the-9, `10`→the-10).
- V3-P: 1 daṇda (`|` → thus).
- chunkJ: clean (0).
- Root cause: `shastra_merge.py` checks `i in sc_by_idx` → `i in G` **before**
  `is_paratext(tok)`, so G-table entries keyed at paratext positions (authored
  off-by-one against filtered gap lists — see D2) gloss the daṇda instead of
  being skipped. No real source token is missing (verified: real-missing=0 on
  all 3 PASS chunks) — the intended glosses landed via other rows/v1.
- Violates: parapravesika paratext-exclusion precedent (excluded with note,
  never glossed).
- Fix recipe (1 pass, no re-glossing): (a) reorder `is_paratext` first in
  `shastra_merge.py`; (b) delete the 9 paratext rows from the 2 T1+L0 files +
  their `*-covered.json` entries; (c) re-run `validate_song` +
  `proof_record --shastra` per chunk (layer_sha256 changes, proofs refresh);
  (d) re-run `check.py`.

**D2 — G-table index integrity: 7 paratext-keyed entries.**
- `v2s_G3` 509, 519; `v2s_G4` 736, 739, 779, 791; `v3p_G2` 414.
- chunkB/chunkJ/v2n G-tables: clean (0).
- These are entries whose key hit a `|`/`|]`; because no real token went
  missing, they are *extra* rows, not shifted-pair rows — but the shift theory
  (authored from filtered lists, not raw indices) was **not** disproven for
  semantic mismatch. Before signoff: re-anchor every v2s_G4 entry in the
  730-800 band against `source_spans('ipvv')[33]` and confirm gloss content
  matches the surface (one spot-check already found index-792 suspicion).
- Automated check to re-run: paratext/out-of-range key scan (the script used
  in this review, ~20 lines) — 7 hits as listed.

**D3 — V2-N is drafted, NOT done.**
- Has argmap/l2/c1 written by `shastra_convert_chunk.py`, but T1 only
  698/1842 (38%) → proof BLOCKED ALIGN 0.303.
- Proven remedy not yet applied: v1-row **char-offset** mapping covers
  1666/1842 (measured); current autogloss used difflib exact-match (697).
  Do not count V2-N as 5-layer done.
- Its argmap was machine-parsed from the pilot (premises = prose paragraphs);
  unreviewed.

**D4 — gloss provenance completeness (audit B, partial).**
- 1,827 G-entries checked; 1,718 cite T1D; 31 citation flags reviewed → all
  fused-component/context cases (honest), 0 fabrication found in samples.
- 109 GRM-only grounds (grammar-derived, no doc line) — unverified; acceptable
  as machine-proposed but should be sampled in human review.
- 6 chunks' G-tables have auto-derived entries (v1-row/doc substring) where
  surface↔gloss fit was not semantically verified (e.g. earlier 'tu'→
  'unreal-pride' mismatches were dropped; verify none remain — grep G-tables
  for glosses whose content words don't occur near the token's T1-doc line).

**D5 — C1 essence quality.** All 4 essences are derived from pilot
question/inference first-sentences — mechanically clean (0 quotes/meta/shared)
but formulaic; read-aloud pass + human review outstanding (needs=human-review
everywhere, correctly).

**D6 — scratch policy drift.** Gap reports, G-draft candidates, R2 tarballs
(145 MB), and audit scripts (audit_b*.py) lived in `/tmp/opencode/` — outside
repo policy ("ALL intermediates live in this repo"). Status.json still points
staging at `/root/ipvv-r2-staging` (empty). Before commit: move the audit
scripts + gap jsons needed for reproducibility into `ipvv/cm/`; drop the rest.

## 4. Token/process critique (why the tail of this session was wasteful)

- 6 failed bash heredocs / unterminated JSON payloads (~300 KB of tool output
  lost to truncation), an 80 KB particle dict written repeatedly, two rewrite
  loops on the same script. Net result after the last PASS: zero.
- 4 audit scripts (`audit_b*.py`) rebuilt the same check 4× before it was
  correct; the final one (~30 lines) should have been written once.
- Lesson recorded: one verification script per invariant, written to
  `ipvv/cm/`, re-run — not re-derived in-session. Commands must be ≤200 lines;
  longer heredocs fail JSON parse at this client.

## 5. What remains to 49/49 (ordered, cheapest first)

1. **Fix D1** (paratext rows + merge ordering + refresh proofs) — ~1 pass.
2. **Re-anchor D2** spot-check (v2s_G4 730-800 band) — one script run.
3. **Char-offset T1/L0 converter** for all 44 scaffolded chunks + chunkB +
   V2-N: v1-row `char_start/char_end` → source-token overlap → gloss
   (proven: 1666/1842 on V2-N; expect ~90-95% coverage per chunk) + particle
   dict + T1-doc exact fill. This is THE lever: lifts every chunk toward the
   0.90 align bar in one mechanical pass. Remaining gaps stay AMBIGUOUS, never
   faked.
4. **Batch argmap/L2/C1** via `shastra_convert_chunk.py` (validate pilot_label
   on ONE vol1 chunk first — it has never run end-to-end).
5. **Proof sweep** `--shastra` per chunk; triage BLOCKEDs (ALIGN_NODISP needs
   `--disp` records or more gloss coverage).
6. **Gloss spot-audit D4/D5** before any "49/49 done" claim; human review
   remains owner-gated (machine-proposed everywhere, no exceptions).
7. Closeout: inventory/proof consistency, `check.py`, REGISTRY header drift
   (71→72), STATUS update, owner push decision (nothing pushed this session).

## 6. Things NOT to do

- Do not regenerate G-tables or re-gloss covered tokens — the authoring ledger
  is `ipvv/cm/*.py` + sidecars.
- Do not hand-write PASS records (inventory gate=INVENTORY ≠ PASS).
- Do not claim V2-N or chunkB as PASS without re-running proof after fixes.
- Do not push; 223 uncommitted paths include this session's entire output.
- No L3/L4/C2 for IPVV (owner-shastra-minimal: prose exegesis, no song).
