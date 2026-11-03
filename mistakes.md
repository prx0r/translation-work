# MISTAKES LOG — binding rules, learned the hard way

*Every entry below is a real defect found in review. Check every work against this list before marking anything complete.*

## 1. No quoted English gloss-words in C1 — EVER
Wrapping English words in quotation marks ("therefore", "I am", "victory to Maheśa") reads as hedging/scare-quotes and as metacommentary. It came from carrying the T1 gloss habit (`[and]-gloss (sanskrit)`) into the wrong layer. In C1 the Sanskrit-in-parens already anchors every claim; quotes add nothing but noise. State the word directly, Sanskrit beside it, no quotes. Applies to both C1.md and C1.v2.md, all works, no exceptions.

## 2. No metacommentary in C1 — EVER
C1 never talks *about the text*. Banned patterns: "the verse/hymn/stotra has/describes/quotes/opens/closes ...", "the grammar/imagery does ...", "this closes the arc", "the move from X to Y", "means and fruit are one event" is fine (states the argument); "the stotra describes its own arising" is not (talks about the text). C1 states the matters — Lord, self, bliss, mind — never the document.

## 3. L2 vs C1 must be different layers — verify with zero shared sentences
L2 = read prose (translation carrying the devotional/philosophical voice). C1 = argument condensation (the claims, the moves, the arc). After writing both, mechanically check: zero long sentences shared. If they overlap, C1 has failed and must be rewritten, not patched.

## 4. T1 must cover the FULL source — parse rate alone proves nothing
L0 59/59 or 114/114 means every token parsed, not that every word was tokenised. Bhairavastava passed L0 at 59/59 while missing the first half of all 10 verses. Always verify T1 against the source: every pāda glossed, verse count matches. Coverage is judged against the source text, never against the tool's report.

## 5. No copy-paste lore across passages — EVER
Each passage's lore note must be verse-specific and distinct. A shared boilerplate paragraph across argmaps is a batch-smear signature. Check mechanically: zero long sentences shared across a work's argmaps.

## 6. Mark uncertainty, never invent
Obscure forms (e.g. prāsuvatkāyaḥ), open antecedents (yena), undecoded chronograms (vasurasapauṣe) get flagged in place, not smoothed over. A guess presented as fact is worse than a gap.

## 7. One work at a time, manually
Batch production caused every defect above. Single target end-to-end: T1+L0 → argmaps → L2 → C1 → verify → human review. No work is marked complete by the machine; COMPLETE always means "machine-proposed, needs human review" until a human signs off.

## 8. C1 must state the MATTERS, never the document — the gate is a proxy, not the rule
C1 that "talks about the poem" is metacommentary even when it passes the regex. The banned patterns list in rule 2 is a floor, not a ceiling. The actual rule: C1 states the matters — Lord, self, bliss, mind, Kāma, separation, cloud, rasa — never the document (poem, passage, text, song, lament, beauty, close, reader, first/middle/final). "The poem's argument is that X" is metacommentary; "X is the case" is not. "The passage performs śṛṅgāra through four movements" is metacommentary; "Kāma arises in the heart; the cloud becomes the messenger" is not. The ghatakarpara C1 passed the regex gate three times while being saturated with document-reference ("The poem's argument is...", "The passage performs...", "The close is aesthetic...", "First of three passages", "reader knows"). Only a broad scan for "the poem/passage/text/song/work", "the lament/beauty/close", "first/middle/final passage", "reader knows" caught it. The fix: read the C1 against the rule, not the regex. The gate is a proxy; the rule is the law. If the gate passes but the output talks about the document, the gate is wrong, not the output.

## 9. The gate is a proxy — never trust a PASS that contradicts the rule
A validator that checks patterns cannot check meaning. "0 metacommentary hits" means 0 regex matches, not 0 metacommentary. The ghatakarpara case: 3 passes, each with 0 regex hits, but 21/13/0 broad hits. The broad scan found them. The rule found them. The narrow gate did not. Lesson: every gate is a proxy for a rule. When the proxy and the rule disagree, the rule wins. Always read the output against the rule, not just the gate.


## 10. No scripts, no bulk — hand-craft every work, one at a time
Scripts that scaffold T1/L0/argmap/L2/C1 from existing MD produce schema-valid but shallow work: generic rasa, copy-paste argmap inference, placeholder sections, no scholarly depth. Every work must be hand-crafted end to end by reading the source, doing one focused web search, and writing each layer by hand. Bulk transforms of multiple works in one session are forbidden — they caused every defect above. The machine proposes data objects; it does not write them. Scripts are proxies, never authors.


## 11. Depth over speed — every layer must be hand-crafted, never scaffolded
Scripts that generate T1/L0/argmap/L2/C1 from existing MD produce schema-valid but shallow work. The mechanical gate (0 meta, 0 shared, 0 quotes) is a proxy, not the rule. The rule: each layer must be read against the verse, not the regex. T1 glosses must be pada-split, not surface-as-gloss. L0 must have analyzed morph, not morph_unknown=true. Argmap premises must be terse logical statements, not copy-pasted L2 sentences. L2 must carry rasa in word choice, not just convey meaning. C1 must state the matters with evocative rasa, not generic placeholders. Concepts must be enriched with sources, rasa, works, related — not skeletons. Peer review must compare against scholarship. One work at a time, by hand, with depth. Bulk transforms of multiple works in one session are forbidden. The machine proposes data objects; it does not write them. Scripts are proxies, never authors. Quality beats speed. Depth beats coverage.

## Rule 12: C1 is pristine translation only
C1 holds the rasa-evocative translation (essence + rasa block). Every note, explanation, boundary, key term, local context, and related reference that is not the translation itself moves to C1 NOTE (data/<song>.c1.json.NOTE.md or c1/C1-<song>.NOTE.md). The site feeds C1 directly; notes in C1 pollute the reader. When in doubt, move it out.

## Why this keeps going wrong
The gate validates schema and round-trips, not prose quality or placement. It cannot tell a precise rasa-evocative translation from a meta sentence. The narrow regex gate is a proxy; the broad scan (move anything that is not the translation) is the rule. When proxy and rule disagree, the rule wins.

## Rule 13: Display-only data types
Anything not meant to be displayed to the reader does not belong in a display data type (T1, L0, argmap, L2, C1, C2). It belongs in a NOTE file (C1 NOTE, L2 NOTE, etc.). Display data types carry only what the site renders.

## Rule 14: L3 reads aloud clean — no dashes, no slashes
L3 is the transmission a reader reads straight through. No `-`/`—` and no `/`
anywhere in L3 lines: plain words, commas and colons only. Hyphenated compounds
(`cave-entered`, `mind-mirror`) and em-dash pauses are T1/L2 habits leaking into
the reading layer — rewrite the line instead ("lodged in many caves",
"shines in mind's mirror"). If a line needs a dash to scan, the line is unfinished.
Everything in L3 is read aloud by TTS: plain ASCII only, no diacritics
(`Siva` not `Śiva`, `Maya` not `Māyā`) — a character the voice cannot pronounce
is a defect in the line.
