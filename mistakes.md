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

## Rule 14: L3 reads aloud clean — no slashes
L3 is the transmission a reader reads straight through. No `/` anywhere in L3
lines: slashes never survive the voice. Hyphens stay — beloved compounds
(`bliss-essence`, `praise-bonds`, `churn-named`) read fine aloud and carry the
poetry; em-dash pauses read as pauses. Plain words, commas and colons otherwise.
Proper names and terms keep their exact Sanskrit diacritics (Śiva, Māyā, Śambhu):
readability never costs exactness.

## Rule 16: L3 is rhythm — cadence is what makes a verse make sense
Take the exact L3 and make it poetic through rhythm. A verse that will not scan
will not parse: the ear gives up before the mind begins. So the final pass over
every couplet is musical, not grammatical — stress, pause, return — and every
inserted word ("is", "are", "be") must earn its place in the beat as well as the
sense. This is the whole point of the grammar and translation underneath: exact
words set to a rhythm the ear can follow. A couplet that is exact but unrhythmic
is unfinished; a couplet that sings but adds claims is unfaithful. Both bars hold.

## 15. Read the whole stack before touching a layer — never rewrite a living voice unaskedThe Kramastotra L3 rewrite (2026-11-03): 30 loved couplets were replaced in one
batch to satisfy a style rule, without re-reading C1, argmaps, or history — the
very layers L3 must look at (LAYERS.md: L3 looks at ALL lower levels). Delivery
through a script envelope made hand-composed lines feel machine-made, and the
result flattened poetic compounds the owner loved ("praise-bonds", "churn-named",
"taste spilling joy", "power-juiced") into plainer ones nobody asked for.
Reverted in full. Binding lessons:
- L3 work starts by re-reading C1 + argmaps + L0 + history + repo material (as the
  Paramarthasara p01 pass did), never from L2 alone.
- A script that writes files is still a script: batch-rewriting 30 verses in one
  go is batch production (rules 10/11), however the lines were composed.
- Style rules (rule 14) govern NEW lines. Existing lines readers love are not
  defects because a new rule exists. Fix defects, never taste.
- Unasked rewrites of a living layer are forbidden. Propose one verse, get a
  verdict, then continue — one at a time.

## 17. L4 sings, L3 means — never the reverse
L3 is the exact transmission; once handcrafted and loved it is FROZEN. All
musical work — prosody, rhythm, rhyme, refrain, rearrangement — lives in L4,
never in L3 edits. The subset rule is the enforcement: every L4's l0_ids and
essence_maps must already be present in its L3. A rhyme word that needs a new
slant is not music, it is new doctrine — re-ground it in L3 first (with
history and reasons, through the living loop), or drop the rhyme. Rhyme never
twists meaning; rhythm never adds claims. Refrains and vocables (aho, he,
repetition for chant) are music, allowed without L0 trace, but they carry no
doctrine and must not smuggle any. First L4 verse of a work needs owner
verdict before the rest — one at a time (rule 15). The validator checks
traces, slashes, and diacritics; the ear checks the rest. A couplet that is
exact but unrhythmic is unfinished L4, not failed L3 — finish the song, do
not touch the transmission.

## 18. Producers own their files — a re-emit is not a refresh

The blanket re-emit (2026-11-03): to add one field everywhere I ran
`emit_site_general --work <all19>`. Four of those works (ajadapramatrsiddhi,
isvarasiddhi, sambandhasiddhi, tantrasara-a01) are owned by ipvv's
`ingest_batch.py` — song-grained chunks with en_variants/checks/styles that this
emitter neither reads nor reproduces. Their prior files were silently reshaped:
fields destroyed, granularity changed, provenance dropped. Three were restored
from git; tantrasara-a01's original was untracked and unrecoverable — it was
re-emitted through the legitimate path (emitter + passages fallback + trace) so
the data is now coherent, but the old record is gone. Same day, earlier: a
sivastotravali re-emit overwrote 130 hand-written argmap views (restored; both
emitters now preserve existing argmap files unless --force).

The rule, mechanised: **emit_site_general REFUSES to write over an ingest-shaped
file (exit 2, "REFUSING … produced by ipvv tools/ingest_batch.py").** Before any
bulk write, ask which tool produced the file you are about to replace, and read
the ownership table in AGENT-MAP.md. Preserve-by-default beats restore-from-git;
git restore only works for committed sins.

## 19. L4 lines must be sung from the verse's own L3 — verify overlap, never trust memory

The VBT L4 grind (2026-11-04): songs p01-p12 and p15-p17 were sung with the L3
in front of them and every line shares nearly all its content words with its L3
(median overlap 1.0). Songs p13-p14 (20 verses) were composed from memory of what
the verses "should" contain — void-spheres, anusvaras, māyā-counting — while the
actual v121-140 teach devotion-excess, equal-pairs, net-questions, and sovereign
speech. Overlap with the true L3: 0.00-0.25. The schema validator passed them
(0 errors) because traces were copied from the real L3 — the English sang a
different tantra than the traces proved. The craft_notes even justified the wrong
lines beautifully, which is worse than no notes: a justification with no named
rival is decoration, and here the rival (the actual verse) was never read.

The rule, mechanised: **after every L4 batch, run the content-word overlap audit
(L4 lines vs the verse's own L3 lines); anything below 0.30 is re-sung from the
extracted L3, argmap, and essence — never defended.** Extract first (L3 lines +
argmap Q→I + essence + song rasa), then sing. The validator checks traces; only
the audit checks that the song is about the verse.

## 20. Never promote uncertainty by vote-counting (largetext deambig incident, 2026-11-06)
A "prose-overlap + cross-chunk agreement" audit promoted 3,044 AMBIGUOUS L0 rows to PARSED. Spot-read caught laundered errors: `omiti`→'the-manifestation', `apekṣāyā`→'not-verily', `śiṃśapātvaṃ`→'the-Sāṃkhyas-and-the-rest' — wrong glosses with repeated votes. Agreement can be shared error. Reverted all 3,044. Survivor rule: unanimous exact-surface agreement across ≥3 distinct songs with ZERO dissent, or closed-class canonical sense — 22 kept. When the rule and the count disagree, the rule wins.

## 21. Unbriefed beam output degenerates to uniform shape (largetext TAL batch, 2026-11-06)
18 TAL briefs without transmission context came back as uniform 8-verse blocks (31/32 spans length exactly 8) or content-free ("summary unavailable" × 37). Beam without scholarship does geometry, not reading. Fix: assessor web-searches first, writes a 1-page transmission brief (what the text is / moves / traps / approach), packet injects it; window tasks ≤60 verses; variety gate rejects >80% same-length spans. Briefs live in `process/beam/lore/`.

## 22. Small reasoning budgets return null content, not short content (beam-free, 2026-11-06)
beam-free burns the token budget on hidden reasoning; `max_tokens: 20`–4000 calls returned `finish=length` with null content deterministically. Not intermittent — do not retry-loop it. Fix: `reasoning_effort: low` + generous `max_tokens` (8000) in `tools/beam_client.py`. Health-check with a ping before queueing a batch.

## 23. Proof ALIGN must exclude paratext from the source side (IPVV converter sweep, 2026-11-06)
B3 concat-align compared T1 surfaces against the RAW source span including paratext (daṇḍas, page marks, editorial refs) that the contract excludes from T1. Result: 7 chunks with byte-perfect T1 (verified 1.0 vs source-minus-paratext) BLOCKED at 0.076–0.796. The data was right; the proxy was wrong (rule 9). Fix in `tools/proof_record.py`: filter `is_paratext` from the source side before comparing. All 7 flipped to PASS. Lesson: when a gate fails on clean data, check whether the gate measures the contract or the raw ink.

## 24. Auto-approval without sampling is blind approval (largetext, 2026-11-06)
`auto-review` approved 36 window briefs on gates alone (tiling + variety + schema) with zero content reads. Gates check shape, never meaning — the same hole as #9, one level up: a plausible-but-wrong brief tiles perfectly (uniform blocks even pass tiling when they happen to cover). Rule now: deterministic 1-in-5 HOLD for assessor spot-read (`sha256(task_id) % 5 == 4`), all full-ahnika briefs held, pilot prose never auto-approved. Sampling is the only content check in the autonomous path; without it the loop certifies its own homework.

## 25. TAL campaign: stage-order and gate lessons (2026-11-06, a23/a11/a17 built autonomously)
- **Dependent stages need a source of truth, not an order.** CM and argmap read glosses from `working-t1`, which is only merged at the assemble stage — so CM/argmap seeded after gloss all failed with "glosses missing". Fix: runners fall back to `process/beam/runs/<song>-gloss-vNN/gloss.json`. Rule: a stage runner must be able to read the PREVIOUS stage's output wherever it lives, never assume the merge happened.
- **Assemble before a dependent stage needs L0 → read CM rows.** argmap needs morphology; `working-l0` doesn't exist until assemble. Fix: read `runs/<song>-cm-vNN/cm.json` when L0 is absent.
- **Gates must be right before they are strict.** The gloss gate rejected the pronoun "I" (capital) — fixed to allow only standalone `I`; then correctly rejected grammar leakage (`vocative-word`, `by-dual-self`, `by-vocative-case-only`). Fix for the leaks: hand-gloss with plain English ("address-word", "twofold-natured") rather than weakening the gate. A strict gate plus an honest hand-fix beats a lenient gate plus silent garbage.
- **Sandhi tokenisation is the source of truth.** A hand gloss split `syāt` + `prakāśasya` where the source token is `syātprakāśasya`; the row-count check caught it. Rule: hand-written glosses must be built by copying the token list, never by re-tokenising from memory.
- **Long campaigns need worker supervision.** Workers exit when the queue drains and die with their shells; a driver waiting on tasks must restart them or it waits forever. `tal_run_all.sh` + `ralph.sh` restart workers each pass.
