# AGENTS.md — Translation-Work Control Plane (IPVV)

*Working Sanskrit translations in /root/translation-work. When in doubt, check here first.*
*Independent of /root/AGENTS.md (Drop project) — do not mix the two tracks.*

## Identity

I am a Sanskrit translation agent working one text at a time toward crystal quality.
I do not batch. I do not mark work complete — the human reviews; I only propose.
My job: take the next target from the queue and return it stunning, or return it
honestly incomplete.

The standard is crystal.md. The failure log is mistakes.md. The process is
FINAL-PROCESS.md (THE canonical process, no deviations). The skill is
skills/crystal-ipvv/SKILL.md (the ONLY authorized workflow). The examples are
skills/crystal-ipvv/EXAMPLES.md (per-datatype prompts + good/bad exhibits).
The gate is check.py (exit 0 = canonical, else fix what it names).
The registry is REGISTRY.json (11 gold, 1 partial, 82 pending).

## The Skill (the law)

Next-agent focus, no exceptions: skills/crystal-ipvv/SKILL.md

One work at a time: source -> lore (one focused search) -> T1 (full-verse) ->
L0 (100% parsed, coverage verified vs source) -> per-passage argmaps (real
reconstruction, distinct lore) -> L2 read prose -> C1 argument condensation ->
mechanical gates -> registry as machine-proposed, never final.

## The Stack (why the order is the order)

Each layer looks at the previous layers for support. Nothing floats.

SOURCE (sha-pinned, verse count verified vs edition)
  -> T1  fast translation, lore-primed: verse draft + pada-split glosses over whole text.
         Coverage before sharpness. History[] on every change.
  -> L0  scholarly audit, term-by-term: morphology + ranked OPTIONS (grounds + source).
         Forks live here and nowhere else (fork: none|live|resolved).
         AMBIGUOUS stays parse-quality (ipvv meaning). Forked tokens require analyzed morph.
  -> ARGMAP  reads verse as whole against Sanskrit+T1+L0+scholarship. Terse logical
         statements. Adjudicates forks on the record (option_choices: chosen, rejected,
         reason). Scholarly refs as support, not claims. No certainty/uncertainty labels.
  -> L2  our translation proper: readable line-by-line plain English, every clause
         tracing to L0 ids, cite byte-exact. Rasa carried in word choice and rhythm.
         supplied[] logs bracketed insertions.
  -> C1  subtle essence over all lower levels, rasa theory: names what verse DOES,
         not just what it says. Optional rasa{} block. Standard 7-part essay preserved.
         No document-reference. No quotes. No shared sentences with L2.
  -> C2  prompt renders (eli5, genz, poetic, formal, ...): style + reproducing prompt +
         model/date + paragraphs mapped to essence indices. A new reading is just a prompt.
  -> Proof  B1-B8, all machine-checkable, per-song JSON (PASS/BLOCKED + needs + lineage)
  -> Site  chunks (PASS only carries English), variants, argmaps, corpus, receipts.

## Absolute Bars (from mistakes.md, learned the hard way)

1. No quoted English gloss-words in C1 — EVER. Sanskrit-in-parens anchors; quotes add noise.
2. No metacommentary in C1 — EVER. C1 never talks about the text. Banned: "the verse has/describes/quotes/opens/closes", "the grammar/imagery does", "this closes the arc", "the move from X to Y". C1 states the matters (Lord, self, bliss, mind, Kama, separation, cloud, rasa) — never the document. The narrow grep is a floor, not a ceiling. Also run the BROAD scan: "the poem/passage/text/song/work", "this passage/poem/text/song", "the lament/beauty/close", "first/middle/final passage", "reader knows/has nothing". Any hit = metacommentary, even if the narrow gate passes. The gate is a proxy; the rule is the law.
3. L2 vs C1 must be different layers — verify with zero shared sentences. L2 = read prose (translation carrying devotional/philosophical voice). C1 = argument condensation (claims, moves, arc). If they overlap, C1 failed and must be rewritten, not patched.
4. T1 must cover the FULL source — parse rate alone proves nothing. L0 59/59 or 114/114 means every token parsed, not that every word was tokenised. Bhairavastava passed L0 at 59/59 while missing the first half of all 10 verses. Always verify T1 against source: every pada glossed, verse count matches. Coverage judged against source text, never tool report.
5. No copy-paste lore across passages — EVER. Each passage's lore note must be verse-specific and distinct. Shared boilerplate is a batch-smear signature. Check mechanically: zero long sentences shared across a work's argmaps.
6. Mark uncertainty, never invent. Obscure forms, open antecedents, undecoded chronograms get flagged in place, not smoothed over. A guess presented as fact is worse than a gap.
7. One work at a time, manually. Batch production caused every defect above. Single target end-to-end: T1+L0 -> argmaps -> L2 -> C1 -> verify -> human review. No work marked complete by machine; COMPLETE always means "machine-proposed, needs human review" until human signs off.
8. C1 states the MATTERS, never the document. The gate is a proxy, not the rule. When the proxy and the rule disagree, the rule wins. Always read the output against the rule, not just the gate.
9. Rasa in L2 is not decoration. Each word choice must be justified by the verse's rasa. "Sounds better" is not a reason. "Evoke the rasa because [specific reason tied to the sthAyibhAva]" is a reason.
10. A fork with no grounds is an invention. A render with no maps_to is drift. An answer with no trace is not an answer.

## Absolute Bars (from mistakes.md)

Every entry in mistakes.md is a real defect found in review. Check every work against this list before marking anything complete. The 7 original rules plus 2 added (metacommentary gate weakness, gate-as-proxy).

## The 10 Binding Rules (from /root/AGENTS.md, Drop project — for reference)

Rule 0: Test against real infrastructure. Rule 1: Never push directly. Rule 2: Schemas are truth.
Rule 3: Pipelines are pure functions. Rule 4: One canonical code path. Rule 5: Observations immutable.
Rule 6: Every decision logged. Rule 7: Features freeze at decision time. Rule 8: CM2 is primary reward.
Rule 9: Calibrate, don't force. Rule 10: Preserve every rejected candidate.

## File Reference

Schemas (validators): schemas/base.py, t1.py, l0.py, argmap.py, l2.py, c1.py, c2.py, signoff.py, suggestion.py
Tools: tools/emit_data.py, validate_song.py, render_md.py, proof_record.py (+disp), emit_site.py, validate_site.py, render_c2.py, propose.py, qa_vs_witness.py, build_concepts.py, lookup_concept.py
Canonical docs: FINAL.md, FINAL-PROCESS.md, LAYERS.md, ALIGNMENT.md, CANONICAL.md, TENSIONS.json, DATATYPES.json, stack.json, README.md, CHAT.md, mistakes.md, crystal.md, targets.md, THEMES.md, INDEX.json, REGISTRY.json
Lore: lore/rasa/ (Abhinavagupta grounding), lore/witnesses/ (vendored, comparison only), lore/links.json (verified URLs), lore/concepts/ (21 concept files), lore/ipvv-deepdive-2026-11-01.md
Skills: skills/crystal-ipvv/SKILL.md (THE process), EXAMPLES.md (prompts + good/bad)
Gate: check.py (exit 0 = canonical)

## Layer Contracts (from LAYERS.md)

T1 — fast translation, lore-primed. Verse draft + pada-split glosses over whole text. Coverage before sharpness. History[] on every change.
L0 — scholarly audit, term-by-term. Morphology + ranked OPTIONS (grounds + source). Forks live here only (fork: none|live|resolved). AMBIGUOUS stays parse-quality. Forked tokens require analyzed morph.
ARGMAP — reads verse as whole against Sanskrit+T1+L0+scholarship. Terse logical statements. Adjudicates forks on the record (option_choices). Scholarly refs as support, not claims. No certainty/uncertainty labels.
L2 — our translation proper. Readable line-by-line plain English, every clause tracing to L0 ids, cite byte-exact. Rasa carried in word choice and rhythm. supplied[] logs bracketed insertions.
C1 — subtle essence over all lower levels, rasa theory. Names what verse DOES. Optional rasa{} block. Standard 7-part essay preserved. No document-reference. No quotes. No shared sentences with L2.
C2 — prompt renders (eli5, genz, poetic, formal, ...). Style + reproducing prompt + model/date + paragraphs mapped to essence indices. A new reading is just a prompt.

## Invariants (validator-enforced)

1. L0.chosen == T1.quick_gloss unless L0.revised with reason.
2. fork live|resolved ⟺ ≥2 options; resolved ⟺ argmap option_choices entry with matching index. AMBIGUOUS is parse quality, not fork state.
3. Argmap traces resolve: t1_verse exists, every l0_id exists, sanskrit_sha matches source.
4. L2 lists ≥1 existing l0_id per verse.
5. C1 essence non-empty; standard render preserved with all 7 sections.
6. C2 renders: prompt non-empty; every paragraph maps to essence.
7. Verse/song coverage: T1+L0+argmap+L2 span exactly the source verse set.

## Living Translation (how others join)

Anyone proposes (tools/propose.py, grounds required — votes are not scholarship). Others support (signed attestations). Maintainer merges (history written, never silent) or rejects with reasons. Agreement: signoff. Git holds every step. External channels (GRETIL, Ambuda, SARIT, sohamhamso) in lore/links.json (verified URLs only). Witness text never hosted.

## Concept Database

lore/concepts/ — one JSON per concept (definition, tradition, rasa, sources, works, related, translations). 21 concepts from 2 gold works. build_concepts.py reports coverage. Gold works must have 100%. Legacy works get a warning. Concept database is post-translation (derivative of C1 KEY TERMS, not prerequisite). lore/trika_glossary_index.json — 325 terms from sanskrit-trikashaivism.com (scraped gold reference). lookup_concept.py — look up, search, create skeleton.

## How to Transform a Legacy Work to Gold Standard

1. Read the work's existing files (T1, L2, C1, argmaps, STATUS).
2. Do a lore search (one focused web search + rasa file if needed).
3. Rebuild T1 with per-pada glosses (pada-split, not whitespace-token).
4. Run t1_extract -> L0. Verify 100% PARSED + verse count vs source.
5. Rewrite argmaps (terse logical, scholarly refs as support, no certainty labels).
6. Rewrite L2 (rasa-carried: words that evoke, not just convey).
7. Rewrite C1 (states matters, never document; rasa{} filled; 0 quotes; 0 meta).
8. Run mechanical gates (0 shared sentences, 0 quotes, 0 meta, L0 100%).
9. Create data JSON (emit_data or manual), validate against schemas.
10. Run proof_record (PASS/BLOCKED + needs + lineage).
11. Run qa_vs_witness if a witness is available.
12. Update STATUS.json (machine-proposed, needs human review).
13. Concept pass: build_concepts.py. Create skeletons, enrich with sources/rasa/works/related.
14. Commit. Run check.py. Must pass.

## Prior Translations

All prior translations (40+ works in this repo + 26 ipvv site translations) are NOT lost. They are STAGED — awaiting transformation to gold standard, one by one, with peer review and web searches. Each transformation follows the steps above. The registry tracks which are done and which are pending. 11 gold, 1 partial (sivastotravali 5/20), 82 pending.

## The Gate

python3 check.py -> CANONICAL, 0 failures. Run before any commit, after any change.
