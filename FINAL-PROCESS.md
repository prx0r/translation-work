# FINAL PROCESS — the canonical gold standard (set in stone)

*2026-11-01. This is THE process. No deviations. No alternatives. No "we'll do it differently this time."
Every work, every verse, every layer follows this. If another document describes the layers
differently, this file wins (after the verbatim User Directive 2026-11-01 in AGENTS.md).*

## The thesis

Small, sharp, finished beats big, batchy, approximate. One work, end to end, manually.
Machine proposes; humans dispose. Every claim in a higher layer must point at the
lower-layer objects it stands on. No layer floats.

## The stack (why the order is the order)

Each layer looks at the previous layers for support. Nothing is invented at a higher
layer that isn't grounded below.

```
SOURCE (sha-pinned, verse count verified against edition)
  → T1  fast translation, lore-primed: verse draft + pada-split glosses over the
        whole text. Coverage before sharpness. History[] on every change.
  → L0  scholarly audit, term-by-term: morphology + ranked OPTIONS (grounds +
        source: grammar / lakshmanjoo / dyczkowski / ksemaraja-vivrti / witness-*
        / t1-draft). Forks live here and nowhere else (fork: none|live|resolved).
        AMBIGUOUS stays parse-quality (ipvv meaning). Forked tokens require
        analyzed morph — no unknowns on forks.
  → ARGMAP  reads the verse as a whole against Sanskrit+T1+L0+scholarship;
        terse logical statements; adjudicates forks on the record (option_choices:
        chosen, rejected, reason). scope: verse | passage. next_pressure.
        Scholarly references woven in as support, not as claims. No certainty/
        uncertainty labels — the verse either resolves or it doesn't.
  → L2  our translation proper: readable line-by-line plain English, every clause
        tracing to L0 ids, cite byte-exact. Rasa carried in word choice and rhythm
        (not decorated with punctuation — evoked through configuration). supplied[]
        logs bracketed insertions.
  → C1  the subtle essence over all lower levels, framed by Abhinavagupta's rasa
        theory: names what the verse DOES (relish/camatkāra), not just what it says.
        Optional rasa{} block (dominant, sthāyibhāva, justification). Standard 7-part
        essay preserved verbatim. No document-reference (metacommentary). No quotes.
  → C2  prompt renders (eli5, genz, poetic, formal, …): style + reproducing prompt +
        model/date + paragraphs mapped to essence indices. A new reading is just a
        prompt. Withheld from site until essence is human-reviewed.
  → Proof  B1–B8, all machine-checkable, per-song JSON (PASS/BLOCKED + needs + lineage)
  → Site  chunks (PASS only carries English), variants (per-word alternatives),
        argmaps, corpus, receipts — all built, never hand-written.
```

## The only process (SKILL.md)

`skills/crystal-ipvv/SKILL.md` is the sole authorized workflow. Read it with
`crystal.md` (standard), `mistakes.md` (failure log), `EXAMPLES.md` (prompts +
good/bad exhibits per datatype), `targets.md` (queue).

## The drill (one work, end to end, no batches)

1. Pick ONE target from `targets.md`. Never parallelize across works.
2. Source first. Read and master it before writing anything.
3. Lore: ONE focused web search (editions, translations, scholarship) + rasa file.
   Verse-specific notes only. Rate limits are real — one search, then work.
4. T1: lore-primed fast pass. Verse draft + pada-split glosses over the whole text.
   Genuine forks marked for L0 options[] with grounds — never smoothed.
   Then `t1_extract.py`. L0 must be 100% PARSED — necessary, never sufficient.
5. Argmaps: one file per passage. Terse logical statements from Sanskrit+T1+L0+
   scholarship. Scholarly references woven in as support, not as claims. No certainty/
   uncertainty labels — the verse either resolves or it doesn't; state what it does
   not resolve. Adjudicate L0 forks on the record (option_choices). Verse-specific
   lore only.
6. L2: plain English, every clause tracing to L0, cite byte-exact. Rasa carried in
   word choice and rhythm (not decorated with punctuation — evoked through
   configuration). Log bracketed supplies in supplied[].
7. C1: essence (atomic propositions) + standard 7-part essay. Name what the verse
   DOES (rasa). Optional rasa{} block. No document-reference. No quotes. No shared
   sentences with L2.
8. C2: prompt renders. `render_c2.py --print-prompt`, run it, ingest with
   `--text-file`. Untagged output rejected to .draft, never merged.
9. Gates: L0 100% + full source coverage; 0 shared C1/L2; 0 shared argmap; 0 quotes;
   0 metacommentary (broad scan: "the poem/passage/text/song/work", "the lament/
   beauty/close", "first/middle/final passage", "reader knows"); check.py → CANONICAL.
10. Registry + STATUS. Mark COMPLETE only as "machine-proposed, needs human review."
    Never mark final.

## Non-negotiables

- A C1 sentence that could sit unchanged in L2 is a failed C1 sentence. Rewrite it.
- A verse half missing from T1 invalidates everything downstream.
- Uncertainty is marked in place, never smoothed over, never invented around.
- A fork with no grounds is an invention. A render with no maps_to is drift.
- An answer with no trace is not an answer.
- The gate is a proxy; the rule is the law. When they disagree, the rule wins.
- Rasa in L2: each word choice justified by the verse's rasa. "Sounds better" is
  not a reason. "Evoke the rasa because [specific reason]" is.
- Small, sharp, finished beats big, batchy, approximate.

## Living translation (how others join)

Anyone proposes (`tools/propose.py`, grounds required). Others support (signed
attestations). Maintainer merges (history written, never silent) or rejects with
reasons. Agreement: `signoff`. Git holds every step. External channels (GRETIL,
Ambuda, SARIT, sohamhamso) in `lore/links.json` (verified URLs only). Witness
text never hosted.

## The gate

`python3 check.py` → CANONICAL, 0 failures. Run before any commit, after any change.

## How to transform a legacy work to gold standard

1. Read the work's existing files (T1, L2, C1, argmaps, STATUS).
2. Do a lore search (one focused web search + rasa file if needed).
3. Rebuild T1 with per-pada glosses (pada-split, not whitespace-token).
4. Run t1_extract → L0. Verify 100% PARSED + verse count vs source.
5. Rewrite argmaps (terse logical, scholarly refs as support, no certainty labels).
6. Rewrite L2 (rasa-carried: words that evoke, not just convey).
7. Rewrite C1 (states matters, never document; rasa{} filled; 0 quotes; 0 meta).
8. Run mechanical gates (0 shared sentences, 0 quotes, 0 meta, L0 100%).
9. Create data JSON (emit_data or manual), validate against schemas.
10. Run proof_record (PASS/BLOCKED + needs + lineage).
11. Run qa_vs_witness if a witness is available.
12. Update STATUS.json (machine-proposed, needs human review).
13. Commit. Run check.py. Must pass.

## Prior translations

All prior translations (40+ works in this repo + 26 ipvv site translations) are NOT
lost. They are STAGED — awaiting transformation to gold standard, one by one, with
peer review and web searches. Each transformation follows the steps above. The
registry tracks which are done and which are pending.
