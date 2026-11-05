# TANTRALOKA RECON — all 37 āhnikas (2026-11-06)

*Recon = spans verified + counted + registered + assessed. No translation yet.
Parser: `tools/workcfg.py::parse_taloka` (`[AbhT_A.V]` markers; `::CN` headers,
C6/C7 split across two lines handled). Source: GRETIL KSTS tantraloka.txt
(17,642 lines, 5860 verses). Legacy: frozen batch-era T1.md per ahnika
(2026-10-31, 10-verse passages, BLOCKED gates) — frozen, never edit.*

## Master table (parsed vs legacy; all match except noted)

| Ahnika | Verses | Tokens | Avg | Legacy T1 | Passages | Flags |
|---|---|---|---|---|---|---|
| a01 | 333 | 2461 | 7.4 | 334 claimed | 34 | OFF-BY-ONE: legacy header says 334 |
| a02 | 50 | 413 | 8.3 | 50 | 5 | clean |
| a03 | 295 | 2315 | 7.8 | 295 | 30 | verse 0b present (intro half-verse); spans keyed 0–294 |
| a04 | 279 | 2235 | 8.0 | 279 | 28 | clean |
| a05 | 159 | 1154 | 7.3 | 159 | 16 | clean |
| a06 | 252 | 2001 | 7.9 | 252 | 26 | clean |
| a07 | 71 | 576 | 8.1 | 71 | 8 | clean |
| a08 | 452 | 3563 | 7.9 | 452 | 46 | clean |
| a09 | 314 | 2614 | 8.3 | 314 | 32 | clean |
| a10 | 310 | 2561 | 8.3 | 310 | 31 | clean |
| a11 | 118 | 944 | 8.0 | 118 | 12 | clean |
| a12 | 26 | 208 | 8.0 | 26 | 3 | clean |
| a13 | 362 | 2895 | 8.0 | 362 | 37 | clean |
| a14 | 47 | 366 | 7.8 | 47 | 5 | clean |
| a15 | 613 | 4776 | 7.8 | 613 | 62 | LARGEST |
| a16 | 311 | 2319 | 7.5 | 311 | 32 | clean |
| a17 | 122 | 934 | 7.7 | 122 | 13 | clean |
| a18 | 11 | 108 | 9.8 | 11 | 2 | longer verses (mixed meter?) |
| a19 | 56 | 457 | 8.2 | 56 | 6 | clean |
| a20 | 16 | 122 | 7.6 | 16 | 2 | clean |
| a21 | 61 | 464 | 7.6 | 61 | 7 | clean |
| a22 | 48 | 374 | 7.8 | 48 | 5 | clean |
| a23 | 103 | 814 | 7.9 | 103 | 11 | clean |
| a24 | 24 | 176 | 7.3 | 24 | 3 | clean |
| a25 | 29 | 241 | 8.3 | 29 | 3 | clean |
| a26 | 76 | 605 | 8.0 | 76 | 8 | clean |
| a27 | 59 | 465 | 7.9 | 59 | 6 | clean |
| a28 | 435 | 3469 | 8.0 | 435 | 44 | clean |
| a29 | 292 | 2294 | 7.9 | 292 | 30 | Kaula rite (hard content) |
| a30 | 123 | 950 | 7.7 | 123 | 13 | clean |
| a31 | 164 | 1338 | 8.2 | 164 | 17 | clean |
| a32 | 68 | 566 | 8.3 | 68 | 7 | clean |
| a33 | 32 | 235 | 7.3 | 32 | 4 | clean |
| a34 | 4 | 28 | 7.0 | 4 | 1 | SMALLEST — pilot candidate |
| a35 | 44 | 345 | 7.8 | 44 | 5 | clean |
| a36 | 16 | 135 | 8.4 | 16 | 2 | clean |
| a37 | 85 | 772 | 9.1 | 85 | 9 | longer verses (mixed meter?) |
| Total | 5860 | — | — | — | — | — |

Uniform anuṣṭubh śloka profile (median 7–8 tokens/verse). No verse-number gaps
anywhere. No duplicate numbers (a03's 295 = keys 0–294, verse 0b = intro
half-verse `atha paraupayikaṃ praṇigadyate…`, keep as v00, do not renumber).

## Meter notes (from token-length distribution)

Nearly all śloka anuṣṭubh (pāda ≈ 8 syllables ≈ 4–5 tokens/pāda → ~8
tokens/verse at whitespace tokenization… observed medians 7–8 fit fused
compounds). Outliers: a18 (avg 9.8) and a37 (avg 9.1) likely carry
triṣṭubh/upajāti stretches — verify at transform time by scansion, do not
assume.

## Difficulty tiers (size-led; content flags noted)

- XS (≤30v): a34(4), a18(11), a20(16), a36(16), a24(24), a12(26), a25(29).
  Pilot tier. a34 is 4 verses — first transform candidate.
- S (30–70): a33(32), a35(44), a14(47), a22(48), a02(50), a19(56), a27(59),
  a21(61), a32(68).
- M (70–150): a07(71), a26(76), a37(85), a23(103), a11(118), a17(122),
  a30(123).
- L (150–320): a05(159), a31(164), a06(252), a04(279), a29(292 + Kaula-rite
  content-hard), a03(295 + verse-0), a10(310), a16(311), a09(314).
- XL (330+): a01(333 + off-by-one), a13(362), a28(435), a08(452),
  a15(613, the campaign's Everest).

Content-hard flags (from tradition, to confirm with lore at transform time):
a29 (kula-yāga rite), a15 (largest + phonematic doctrine), a28 (cosmic body),
a01 (opening stakes: jñāna/ajñāna, pratyabhijñā seed), a37 (closing).

## Witness status

No Tantraloka witness vendored in lore/witnesses/ (only sivastotravali
Lakshmanjoo + legacy L2s for small works). External parallels (comparison
only, never copied): Dyczkowski's 11-volume Tantrāloka translation with
Jayaratha commentary; Chakravarty/Bertagni English; OccultGuide chapter
summaries; vishvasa Hindi-English rendering. Expect qa NEEDS_WITNESS for all
transforms until/unless a witness is vendored (owner decision).

## Transform order (owner goal: shortest-first, a34 → … → a15)

a34(4) → a18(11) → a20(16) → a36(16) → a24(24) → a12(26) → a25(29) →
a33(32) → a35(44) → a14(47) → a22(48) → a02(50) → a19(56) → a27(59) →
a21(61) → a32(68) → a07(71) → a26(76) → a37(85) → a23(103) → a11(118) →
a17(122) → a30(123) → a05(159) → a31(164) → a06(252) → a04(279) →
a29(292) → a03(295) → a10(310) → a16(311) → a09(314) → a01(333) →
a13(362) → a28(435) → a08(452) → a15(613).

## Registration (workcfg, kind=taloka, songs tsa-aNN)

Batches: A (a01–12), B (a13–25), C (a26–37). Song id form `tsa-aNN`
(one song per ahnika, verse-addressed data objects like tantrasara golds).
Do NOT touch legacy files.

## Open items for owner (do not self-resolve)

1. Transform order approval (list above) + pilot nod for a34.
2. Witness decision: vendored witness for Tantraloka (Dyczkowski text cannot
   be hosted — rights; Lakshmanjoo-style notes don't exist for TAL)? If none,
   all proofs carry NEEDS_WITNESS honestly.
3. a18/a37 mixed-meter question can wait until transform (scansion then).
4. a01 334-vs-333: legacy header counts 334, GRETIL numbers 333 — record as
   boundary, do not "fix" either side.
