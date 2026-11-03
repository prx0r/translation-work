# translation-work — canonical Sanskrit translation stack

*The clear version. If this file conflicts with anything else here, this file wins —
after the verbatim User Directive 2026-11-01 in `AGENTS.md`, which wins over everything.*

## What this is

Machine-proposed, human-reviewed translations of Sanskrit works, built as **data objects,
not documents**. Every layer is JSON, validated by schemas, gated by `check.py`, with
Markdown kept only as rendered views for human review.

## The stack (why the order is the order)

Each layer looks at the previous layers for support. Nothing floats:

| # | Layer | Reads | Produces | Validator |
|---|---|---|---|---|
| 0 | SOURCE | GRETIL / editions (sha-pinned) | verse text | byte match |
| 1 | T1 | SOURCE + lore (traditions, good translations) | fast full-verse draft + per-token quick gloss | `schemas/t1.py` |
| 2 | L0 | SOURCE + T1 | per-token OPTIONS (ranked, sourced, grounded); forks live here only | `schemas/l0.py` |
| 3 | ARGMAP | SOURCE + T1 + L0 + scholarship | terse argument; adjudicates forks on the record | `schemas/argmap.py` |
| 4 | L2 | all above | plain-English verse, cites byte-exact | `schemas/l2.py` + proof B7 |
| 5 | C1 | all above + rasa lore | essence + standard essay (sharpest poetic reading) | `schemas/c1.py` |
| 6 | L3 | SOURCE + T1 + L0 + ARGMAP + L2 + C1 | final exact transmission, line-by-line verse (frozen once loved) | `schemas/l3.py` |
| 7 | L4 | L3 + C1 essence/rasa | the song: L3 set to music (prosody, rhythm, rhyme); traces subset of L3 | `schemas/l4.py` |
| 8 | C2 | essence + L3 (+ L4) + a prompt | style renders (eli5, genz, …), maps_to enforced | `schemas/c2.py` |
| 9 | Proof | everything | PASS/BLOCKED + needs + lineage | `tools/proof_record.py` |
| 10 | Site | proof-PASS data only | reader chunks, variants, argmaps | `tools/validate_site.py` |

Full contract: `LAYERS.md`. Relation to ipvv + benchy: `ALIGNMENT.md`. Known tensions: `TENSIONS.json`.
Machine-readable registry of every datatype: `DATATYPES.json`. Version manifest: `stack.json`.

## The only process

`skills/crystal-ipvv/SKILL.md` is the **sole** authorized workflow (one work end to end,
no batches). Standard: `crystal.md`. Failure log: `mistakes.md`. Queue: `targets.md`.

## Living translation (how to contribute)

Anyone can propose an alternative: `tools/propose.py` (grounds required — votes without
grounds are rejected). Others add supports; a maintainer accepts (history is written,
never silent) or rejects with reasons. Agreement is recorded in `data/<song>.signoff.json`.
Git holds every step. External contributions welcome via GRETIL / Ambuda / SARIT —
see `lore/links.json` (verified links only).

## File map

```
translation-work/
  AGENTS.md            operating system + verbatim user directive (highest precedence)
  CANONICAL.md         what counts as canonical + change protocol
  LAYERS.md            layer contracts + invariants + living-translation rules
  ALIGNMENT.md         vs ipvv schemas, vs sanskritbenchy, stale-doctrine log
  TENSIONS.json        known frictions + status (fixed/accepted/queued)
  DATATYPES.json       every datatype + worker contracts + global rules
  stack.json           version manifest (schemas v1.1.0)
  check.py             THE gate — CANONICAL or not (exit 0/1)
  schemas/             validators (t1/l0/argmap/l2/c1/c2/signoff/suggestion + base)
  tools/               emit_data, validate_song, render_md, proof_record (+disp),
                       emit_site, validate_site, render_c2, propose, qa_vs_witness
  lore/                rasa grounding · witnesses (vendored, comparison only) ·
                       links (verified) · song notes (e.g. mealtime yajna memo)
  logs/qa/             witness-QA reports (SHIP_AS_IS / WITH_NOTES / HOLD)
  <work>/              per-work directory (see sivastotravali/ below)
  sivastotravali/
    data/              CANONICAL per-song JSON (t1/l0/argmap/l2/c1/c2/suggest/signoff)
    proof/             proof records (PASS/BLOCKED + needs + lineage)
    scholar/           append-only versions/reviews/promotions (fork chains + signoffs)
    T1-sXX.md          frozen token gloss (rendered view of data)
    argmaps/sivst-sXX.md   verse argmaps (rendered view)
    argmaps/sivst-p01..p05.md + argmap.json   passage-scope argmaps (multi-verse dialectic)
    L2-sXX.md          read prose (rendered view) — all 20 songs
    c1/C1-sXX.md       standard essays (rendered view) — all 20 songs
    T1.md              coarse 2026-10-30 original (cited provenance, read-only)
    L200.md, L200-s01.md   legacy audits (human-readable, kept per D1)
    T1-SKEL-s06..s20.md    live work queue (skeletons; s01-s05 removed as done)
    STATUS.json        work state (this file is the ledger, keep it true)
```

## Entry points

- **New agent?** Read `AGENTS.md` → this file → `LAYERS.md` → `skills/crystal-ipvv/SKILL.md` → pick from `targets.md`.
- **New song?** `tools/emit_data.py` → fill T1 glosses → `t1_extract` → align-fix → `validate_song.py` → `proof_record.py` → `check.py`.
- **New render?** `tools/render_c2.py --print-prompt`, run it, ingest with `--text-file`.
- **Disagree with a gloss?** `tools/propose.py` (grounds required) → gather supports → maintainer merges.
- **Is it canonical?** `python3 check.py` — exit 0 or fix what it names.

## What was removed (2026-11-01 audit)

Superseded batch-era files deleted (git history preserves them): root `ARGMAP.md`,
`GATE.json`, `L1.md`, `L2.md`, `L2.v2.md`, `T1-SKEL-s01..s05`. Kept deliberately:
`T1.md` (cited provenance), `L200.md`/`L200-s01.md` (legacy audits),
`argmaps/sivst-p01..p05.md` + `argmap.json` (passage-scope layer), `T1-SKEL-s06..s20`
(live queue). `check.py` fails if any banned path reappears.
