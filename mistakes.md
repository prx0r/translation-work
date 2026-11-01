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
