# MANUAL REVIEW — Śivastotrāvalī (sivastotravali), 20 songs / 450 verses

*Date 2026-11-01. Scope: whole work, all 20 songs. Reviewed by hand against FINAL-PROCESS.md, mistakes.md (11 rules), SKILL.md, NOTES 30 TODOs. Gate: check.py CANONICAL 0 failures (mechanical only).*

## 1. Verdict

**Machine-proposed, mechanically clean, not crystal quality.** All 20 songs PASS the proof gate (0 blocking). Concept coverage 56/56. Peer reviews 20/20. But depth is uneven and several TODOs are overstated as done: T1 glosses for s09–s20 are identity (Sanskrit echoed), L0 morphology is unknown for every song except s08, scholarly alternatives are absent, argmaps for s01–s05 are legacy/backfilled, L2 is plain (not rasa-carried), and C1 carries minor metacommentary in 3 songs. Do not treat registry "gold" as human-approved; signoffs = 0.

## 2. State of the work

| Item | Value |
|---|---|
| Songs | 20 (s01–s20) |
| Verses | 450 |
| L0 tokens | 5,364 |
| Proof | 20/20 PASS, 0 blocking, warnings: s01, s03, s04, s06 (1 each) |
| Concept coverage | 56/56 |
| Peer reviews | 20 files |
| Signoffs | 0 (machine-proposed) |
| C2 renders | s01 only (eli5, genz, testrun) |

## 3. Per-song metrics

| Song | Verses | Tokens | T1 identity gloss | morph unknown | Forks | Argmap | C1 words | L2 lines | Proof warn |
|---|---|---|---|---|---|---|---|---|---|
| s01 | 26 | 342 | 2/342 | 340/342 | 2 | legacy (backfilled) | 692 | 109 | 1 |
| s02 | 29 | 265 | 0/265 | 265/265 | 0 | legacy (backfilled) | 550 | 121 | 0 |
| s03 | 21 | 324 | 0/324 | 324/324 | 0 | legacy (backfilled) | 541 | 89 | 1 |
| s04 | 25 | 521 | 2/521 | 521/521 | 0 | legacy (backfilled) | 544 | 105 | 1 |
| s05 | 26 | 423 | 3/423 | 423/423 | 0 | legacy (backfilled) | 406 | 109 | 0 |
| s06 | 11 | 119 | 0/119 | 119/119 | 0 | structured | 357 | 49 | 1 |
| s07 | 9 | 82 | 0/82 | 82/82 | 0 | structured | 363 | 41 | 0 |
| s08 | 13 | 167 | 0/167 | 0/167 | 0 | structured | 435 | 57 | 0 |
| s09 | 20 | 175 | 175/175 | 175/175 | 0 | structured | 435 | 85 | 0 |
| s10 | 26 | 290 | 290/290 | 290/290 | 0 | structured | 441 | 109 | 0 |
| s11 | 15 | 270 | 270/270 | 270/270 | 0 | structured | 405 | 66 | 0 |
| s12 | 29 | 418 | 418/418 | 418/418 | 0 | structured | 426 | 121 | 0 |
| s13 | 20 | 265 | 265/265 | 265/265 | 0 | structured | 605 | 85 | 0 |
| s14 | 24 | 107 | 107/107 | 107/107 | 0 | structured | 564 | 101 | 0 |
| s15 | 19 | 231 | 231/231 | 231/231 | 0 | structured | 531 | 81 | 0 |
| s16 | 30 | 355 | 355/355 | 355/355 | 0 | structured | 567 | 125 | 0 |
| s17 | 48 | 467 | 467/467 | 467/467 | 0 | structured | 583 | 197 | 0 |
| s18 | 21 | 287 | 287/287 | 287/287 | 0 | structured | 534 | 89 | 0 |
| s19 | 17 | 204 | 204/204 | 204/204 | 0 | structured | 411 | 73 | 0 |
| s20 | 21 | 229 | 229/229 | 229/229 | 0 | structured | 458 | 89 | 0 |

## 4. Assessment against the 11 rules (mistakes.md)

1. **No quoted English gloss-words in C1** — PASS (proof: 0 quotes all 20).
2. **No metacommentary in C1** — MECHANICAL PASS, MANUAL FAIL in 3 songs: `C1-s01.md` ("reader has nothing presupposed", "sets the collection's stance"), `C1-s03.md` ("Love-song as metaphysics..."), `C1-s11.md` ("Verse 12's cornered metaphysics is complaint... not the text"). Also aggregate `C1.md` uses "The passage moves in two steps" repeatedly — document-reference at aggregate level. Strip these.
3. **L2 vs C1 zero shared sentences** — PASS (proof: 0 shared all 20).
4. **T1 full source coverage** — VERSE COUNTS PASS (all 26/29/... match source), but TOKEN QUALITY FAILS for s09–s20: every T1 quick_gloss equals the surface Sanskrit (identity gloss), i.e. the pada-split was not actually translated. s01–s08 are translated. This is the single biggest defect.
5. **No copy-paste lore across passages** — NOT VERIFIED by hand; argmaps s06–s20 share the vague uncertainty "See C1 BOUNDARY for open questions", which is boilerplate. Flag for cleanup.
6. **Mark uncertainty, never invent** — PARTIAL. Argmaps carry uncertainties (good), but several are vague placeholders. s01 has 2 real forks (na / dhyāyataḥ, anāma) with grounds — good. All other songs have 0 forks and 0 alternatives: L0 is a single-option backfill, not a scholarly audit.
7. **One work at a time, manually** — PASS in spirit (single work).
8. **C1 states the MATTERS** — PASS mechanically, MANUAL FAIL in the 3 songs above.
9. **Rasa in L2 is not decoration** — FAIL: L2 is plain translation throughout (per STATUS: "L2 plain, not rasa-carried"). Rasa lives only in C1. Only s01–s05 have rasa blocks filled; s06–s20 have rasa blocks but L2 word choice is not rasa-justified. Needs rasa-carrying pass.
10. **Fork with grounds / render with maps_to / answer with trace** — Forks: only 2, both with grounds (good). Traces: all argmaps have t1_verse + l0_ids (good). C2 maps_to: only s01 has C2 renders.
11. **Depth over speed** — FAIL: s09–s20 were clearly produced by bulk scaffolding (identity glosses, morph unknown, single options). This is the batch-smear signature the rules forbid.

## 5. 30-TODO status (sivastotravali-relevant subset)

Project TODOs 1–17 concern other works (ghatakarpara, spandasandoha, pancashloki, anubhavanivedana, paramarthacarca, bhairavastava, anuttarastika) — not this work. Sivastotravali-relevant:

| TODO | Claimed | Actual |
|---|---|---|
| 18 s06 T1 pada-split + L0 morph | DONE | T1 done (English glosses); L0 morph NOT done (119/119 unknown) |
| 19 s07 T1 + L0 morph | DONE | T1 done; L0 morph NOT done (82/82 unknown) |
| 20 s08 T1 + L0 morph | DONE | DONE (0 unknown) — best song |
| 21 s09 T1 + L0 morph | DONE | NOT done (identity glosses, 175/175 unknown) |
| 22 s10 | DONE | NOT done |
| 23 s11 | DONE | NOT done |
| 24 s12 | DONE | NOT done |
| 25 s13–s20 | DONE | NOT done (all identity glosses) |
| 26 s08–s20 argmaps | DONE (partial) | Structured JSON exists, but s01–s05 still legacy; premises for s06–s20 are short phrases, uncertainties vague |
| 27 s08–s20 L2 rasa-carried | DONE (verification) | NOT done — L2 plain throughout |
| 28 s08–s20 peer reviews | DONE (all 15) | DONE (20 files incl. s01–s05) |
| 29 concept enrichment | DONE (3 enriched, 100+ skeletons) | Coverage 56/56; enrichment depth not verified |
| 30 final verification | DONE | Mechanical only; depth review pending (this report) |

**Conclusion: TODOs 21–25 are overstated.** The data shows s09–s20 T1 was scaffolded, not hand-crafted.

## 6. Strengths

- Complete mechanical skeleton: 20 songs, 450 verses, all data objects (T1/L0/argmap/L2/C1), all proof PASS.
- Source coverage verified: every song's t1_verses == source_verses.
- L2 cites byte-exact Sanskrit for every verse (0 failures).
- L2 vs C1 zero shared sentences (0 all songs).
- C1 quotes 0 all songs.
- Concept coverage 56/56.
- Peer reviews 20/20, honest about gaps.
- s08 is the model song: T1 translated, L0 morph fully analyzed (167/167, 0 unknown), structured argmap, peer review done.
- s01 has 2 genuine forks with morphology and grounds (living-translation proof-of-concept).

## 7. Defects (prioritized)

**P0 (blocks "gold" honesty)**
- s09–s20 T1 is identity glosses (100%). These 11 songs need real pada-split glosses before anything else. ~2,800 tokens.
- L0 morphology unknown for 19/20 songs (~5,197 tokens). Only s08 done.

**P1 (depth)**
- L0 has 1 option per token for 19/20 songs — no scholarly alternatives (grammar / Lakshmanjoo / Dyczkowski / Ksemaraja-vivrti). Only s01 has 2 forks.
- Argmaps s01–s05 are legacy format (structured=false, traces_backfilled=true, reconstruction-as-prose). Convert to structured terse logical format.
- Argmap uncertainties for s06–s20 are vague ("See C1 BOUNDARY"). Replace with real open questions.
- L2 is plain, not rasa-carried, for all 20 songs.

**P2 (polish)**
- C1 metacommentary in s01, s03, s11 (and aggregate C1.md). Strip document-reference.
- C2 renders only s01; decide whether to generate for others (currently withheld for human review).
- Aggregate C1.md uses "The passage moves in two steps" — rewrite as matters, not document.
- Warnings: s01 (ledger gloss missing bhaktiśālin), s03, s04, s06 (1 each) — inspect.

**P3 (process)**
- Signoffs: 0. Everything displays as machine-proposed. Human must sign off.
- Registry marks sivastotravali "gold" despite partial depth. Consider downgrading to "partial" until s09–s20 T1/L0 done.

## 8. Recommended hand-refinement order (one song at a time)

1. s09 (20v, 175 tokens) — first identity-gloss song; convert to real T1 + L0 morph, model on s08.
2. s10, s11, s12 (larger) — same treatment.
3. s13–s20 — bulk of remaining identity glosses.
4. Backfill L0 morphology for s01–s07 (and s09–s20 after T1).
5. Add scholarly alternatives (options[]) for high-value forks.
6. Convert s01–s05 argmaps to structured format; sharpen s06–s20 uncertainties.
7. Rasa-carrying L2 pass across all 20 songs.
8. C1 meta cleanup (s01, s03, s11, aggregate).
9. Human signoff per song.

## 9. Honest bottom line

The Śivastotrāvalī is a **complete mechanical skeleton with real source coverage and honest peer reviews**, but **not crystal quality**. The biggest single problem is that s09–s20 were scaffolded with identity glosses and never hand-translated, which contradicts both Rule 4 and Rule 11. The NOTES claim these TODOs are "DONE"; the data shows they are not. Treat the registry "gold" status as provisional until the P0 items are cleared. s08 is the only song that currently meets the bar; use it as the template.
