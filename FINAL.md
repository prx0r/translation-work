# FINAL — the best approach, as it now stands

*2026-11-01 · schemas v1.1.0 · `check.py`: CANONICAL, 0 failures · 4 commits · tree clean.
Read this first, then `AGENTS.md` (verbatim directive), `LAYERS.md`, `SKILL.md` + `EXAMPLES.md`.*

## The thesis

Small, sharp, finished beats big, batchy, approximate. One work, end to end, manually.
Machine proposes; humans dispose. Every claim in a higher layer must point at the
lower-layer objects it stands on. No layer floats.

## The stack (why the order is the order)

Each layer looks at the previous layers for support. Nothing is invented at a higher
layer that isn't grounded below.

```
SOURCE (sha-pinned GRETIL slice)
  → T1  fast translation, lore-primed: verse draft + pada-split glosses over the
        whole text. Coverage before sharpness. History[] on every change.
  → L0  scholarly audit, term-by-term: morphology + ranked OPTIONS (grounds +
        source: grammar / lakshmanjoo / dyczkowski / ksemaraja-vivrti / witness-*
        / t1-draft). Forks live here and nowhere else (fork: none|live|resolved).
        AMBIGUOUS stays parse-quality (ipvv meaning). Forked tokens require
        analyzed morph — no unknowns on forks.
  → ARGMAP  reads the verse as a whole against Sanskrit+T1+L0+scholarship;
        terse logical statements; adjudicates forks on the record (option_choices:
        chosen, rejected, reason). scope: verse | passage (dialectic lives at
        passage grain). next_pressure: what the next chunk must handle.
  → L2  our translation proper: readable line-by-line plain English, every clause
        tracing to L0 ids, cite byte-exact. supplied[] logs bracketed insertions.
  → C1  the subtle essence over all lower levels, framed by Abhinavagupta's rasa
        theory: names what the verse DOES (relish/camatkāra), not just what it says.
        Optional rasa{} block. Standard 7-part essay preserved verbatim.
  → C2  prompt renders (eli5, genz, poetic, formal, …): style + reproducing
        prompt + model/date + paragraphs mapped to essence indices. A new reading is
        just a prompt.
  → Proof  B1–B8, all machine-checkable, per-song JSON (PASS/BLOCKED + needs + lineage)
  → Site  chunks (PASS only carries English), variants (per-word alternatives),
        argmaps, corpus, receipts — all built, never hand-written.
```

## The only process

`skills/crystal-ipvv/SKILL.md` is the sole authorized workflow. Per-datatype
PROMPT + GOOD (verbatim) + BAD (verbatim fixes) + WHY: `EXAMPLES.md`. Standard:
`crystal.md`. Failure log: `mistakes.md` (7 rules, all mapped to BAD entries).
Queue: `targets.md`.

## Living translation (how others join)

Anyone proposes (`tools/propose.py`, grounds required — votes are not scholarship).
Others support (signed attestations). Maintainer merges (writes history, never
silently) or rejects with reasons. Agreement: `signoff`. Git holds every step.
External channels (GRETIL, Ambuda, SARIT, sohamhamso) in `lore/links.json`
(verified URLs only). Witness text is never hosted.

## What we stole and what we didn't

From ipvv: the DAG shape, the five-dimension proof, the four-section argmap template,
the honest-gap convention, the peer-review bar (DONE = gate-pass + human-accepted),
the `needs` field, witness QA. From sanskritbenchy: the proof envelope, the Kendall
protocol (queued, Trika slice only), candidate-disagreement as fork detector,
MQM pair format, gold records as the discipline template. We did NOT take: ipvv's
frozen-T1 discipline (we use living JSON + history), their generic 12-term glossary
(replaced by per-work ledgers), their L200 8-section audit (deferred, D1), COMET
(no torch), triangulation (silent for all Śaiva texts — verified), the confidence
vector (7/11 unavailable), finetuning (no GPUs).

## What we added that neither has

- L0 `options[]` with grounds + sources (ipvv has single gloss)
- `fork` axis separate from parse quality (T5)
- argmap traces (t1_verse, l0_ids, sanskrit_sha) + `option_choices` with reasons
- C1 essence + C2 prompt renders with `maps_to` enforcement
- rasa notes (optional, unfilled) grounded in Abhinavagupta
- signoff, suggestion, variants, proof B8, `check.py` canonical gate
- per-verse GRETIL line anchors for chat citations
- living-translation loop (propose/support/accept, git-diffed, qa_vs_witness)

## Known gaps (honest)

- T2: per-clause L2→L0 derivation (verse-grain only today)
- T3: history[] on T1 (schema + validator ready; first fill pending)
- T6: witness-hierarchy rule (grammar vs witness precedence) — queued
- T1/T8: passage-scope argmaps for śāstra texts — queued
- Essence: mechanical-from-SUMMARY, needs human review (T4)
- Signoffs: zero signed — everything displays as machine-proposed
- Chat worker contract: specified, not wired (owner-side TODO)
- Generic ledger: T1 headers are the ledger; machine-readable ledger file queued

## The gate

`python3 check.py` → CANONICAL, 0 failures. Run before any commit, after any change.
