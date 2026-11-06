# HANDOVER — IPVV NEXT AGENT: full plan (2026-11-06)

*Read order: this file → `SHASTRA-MINIMAL.md` (the contract) →
`REVIEW-IPVV-2026-11-06.md` (audit, defects D1–D6, measured numbers) →
`HANDOVER-IPVV-SHASTRA-MINIMAL.md` (chunk queue, loop commands) →
`AGENTS.md` + `skills/crystal-ipvv/SKILL.md`. Nothing in those four is
rewritten here; this file says WHAT to do and WHY, in order.*

**Two rules that outrank everything below:**
1. **Never regenerate work that already passes.** The 3 PASS chunks (chunkJ,
   V2-S, V3-P), their G-tables, the intake, schemas 1.4.0, and the tools are
   finished artifacts — fix them only where a named defect (D1/D2) requires
   it, and only with the given recipe. No re-glossing, no re-authored
   argmaps, no re-derived essences for passing chunks.
2. **Quality bar unchanged.** Machine-proposed, never final. Paratext never
   glossed. Uncertainty marked, never smoothed. Scripts assemble/verify —
   they do not author glosses. `check.py` → CANONICAL before any commit.

---

## A. Where we are (measured 2026-11-06, see REVIEW §1)

- 3/49 chunks full minimal stack **PASS** (align 0.938–0.960, cites clean).
- 1 drafted-not-done: V2-N (all 5 layers written, T1 only 698/1842 → BLOCKED).
- 1 in progress: chunkB (596/1633 hand-glossed, G1–G6 tables on file).
- 44 scaffolded T1+L0 only. Total T1 coverage 60,846/177,954 (34%).
- Tooling proven: intake (49/49 byte-verbatim), `shastra_merge.py`,
  `proof_record --shastra`, `shastra_autogloss.py`, converter (needs 1
  vol1 validation run). Char-offset v1→T1 mapping **measured 89% of real
  tokens** repo-wide (V2/V3 85–95%, vol1 A–F weak: 1–80%).

## B. Why this order (the reasoning, so you can deviate intelligently)

The bottleneck is T1 gloss coverage vs the proof ALIGN bar (0.90, or
`--disp` dispositions below it). Everything else (argmap, L2, C1-essence)
converts from pilots mechanically. So: **coverage first, layers second,
proofs third, hand-work only on what automation provably cannot reach.**
Hand-glossing 99k tokens is not the plan; the plan is to measure what
automation reaches, then hand-fill only the residue. If a phase's measured
coverage lands short, stop and report — do not fake glosses to pass a gate.

## C. Work plan

### Phase 1 — defects (do first; they contaminate new work)
1. **D1 paratext rows** (V2-S: 8, V3-P: 1): reorder `is_paratext(tok)` first
   in `tools/shastra_merge.py` (before the `i in G` branch), delete the 9
   paratext rows from those 2 T1+L0 JSONs + their `*-covered.json` entries,
   re-run `validate_song` + `proof_record --shastra` (hashes refresh), then
   `check.py`. *Why first:* the merge bug will silently re-inject daṇḍa
   glosses into every future merge.
2. **D2 G-table keys**: run the paratext-key scan from REVIEW §3 (7 hits);
   re-anchor the v2s_G4 730–800 band against `source_spans('ipvv')[33]`
   (one spot-check already suspected idx 792). Fix table keys only — do not
   touch surrounding entries.

### Phase 2 — char-offset coverage fill (the lever)
3. Write `tools/shastra_charfill.py`: for each of the 44 scaffolded chunks
   + chunkB + V2-N, map v1-row `char_start/char_end` (tarballs staged in
   `/tmp/opencode/r2/`, re-pull from R2 if gone: `sanskritree/ipvv-translations/l0/`)
   → source-token spans (bundle `published/pt-passage-ipvv-<chunk>-md.json`)
   → fill T1 quick_gloss + L0 options[0] for uncovered REAL tokens only.
   Order: char-offset (89% measured) → T1-doc paren-gloss exact match
   (measured 553/991 of chunkB's residue) → compact particle dict → else
   leave the token uncovered and report it. Reuse `shastra_merge.py`'s
   sidecar/idempotency pattern; G-table glosses are authoritative — fill
   never overwrites an existing token.
   *Acceptance:* per-chunk real-token coverage ≥90% OR a residual list
   written to `ipvv/cm/<song>-residual.json`. Never guess a gloss.
   Note: vol1 chunks A–F will fail this bar (1–80%); they go to Phase 4.
   Fix the bundle-glob miss for chunk ids containing dots (G/H/I) here too.

### Phase 3 — layers + proofs (batch)
4. Validate `shastra_convert_chunk.py` on **one** vol1 chunk end-to-end
   first (pilot_label fix `chunk_id[5]` has never run on vol1) — check
   argmap premises parse, L2 cites byte-exact, C1 0-quotes/0-meta/0-shared.
   Then batch across chunks that have ≥90% T1: argmap (pilot V-label),
   L2 (rename + retrace + chunk-slice cites), C1-essence (pilot-derived,
   filter shared sentences), `validate_song` → `proof_record --shastra`.
5. Triage BLOCKEDs: ALIGN <0.90 → either Phase 2 residual fill or record a
   disposition via `--disp` (legitimate; say what is missing, never waive
   silently). Layer errors → fix data, never widen a validator.

### Phase 4 — vol1 tail (the genuine hand work)
6. chunkA (1,926 real tokens, 13 rows), chunkB (1,435, 210), chunkC–F
   (residues 300–1,700): use T1-doc `(surface)` extraction as candidate
   glosses (assemble + verify — they are already hand-written in the frozen
   docs), then G-tables only for what extraction misses. Report session-by-
   session coverage; do not batch-forge.

### Phase 5 — audit + closeout (before any "done" claim)
7. Re-run REVIEW's three scans (paratext-key, surface↔gloss fit, citation
   grounds) as ONE script saved in `ipvv/cm/audit_shastra.py`; sample the
   109 GRM-only grounds (D4); read-aloud the 4 essences (D5).
8. Update `ipvv/STATUS.json` (shastra_pass list), `HANDOVER-IPVV-SHASTRA-MINIMAL.md`
   queue, and REVIEW (append deltas — don't rewrite). Move stray /tmp
   intermediates into `ipvv/cm/` (D6 scratch policy). `check.py` → CANONICAL.
9. Final state: all 49 either PASS or PASS-with-recorded-disposition,
   every chunk `needs: human-review`, owner signoff requested — that is
   "done" for the agent; the human review is NOT ours to run.

## D. Session economics (from REVIEW §4 — why the last tail wasted tokens)
- One verification script per invariant, written once to `ipvv/cm/`, re-run.
- Commands ≤200 lines; bigger heredocs fail JSON parse at this client.
- No re-derivation of audited facts — cite the REVIEW, re-measure only the
  one number that changed (coverage).
- After each phase: one `check.py` + one summary line; no status essays.

## E. Definition of done
`validate_song` 0 errors on 49 · proof PASS (or disposition file) on 49 ·
`check.py` CANONICAL · audit scans clean · STATUS/queue updated ·
nothing pushed (owner pushes) · everything labelled machine-proposed.
