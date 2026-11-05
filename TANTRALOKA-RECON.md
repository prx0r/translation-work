# TANTRALOKA RECON — all 37 āhnikas (2026-11-06, parser fixed 2026-11-07)

*Recon = spans verified + counted + registered + assessed. No translation yet.
Parser: `tools/workcfg.py::parse_taloka` (`[AbhT_A.V]` markers; `:CN`
single-colon headers skipped — they leaked into v1 buffers before the fix;
unmarked `/ 0b` topic lines carved as verse 0). Source: GRETIL KSTS
tantraloka.txt (17,642 lines, 5864 units = 5860 numbered verses + 4 carved
v00s; a03 v00 marked in source). Legacy: frozen batch-era T1.md per ahnika
(2026-10-31, 10-verse passages, BLOCKED gates) — frozen, never edit.*

## Master table (parsed vs legacy; all match except noted)

| Ahnika | Units | Tokens | Avg | Legacy T1 | Passages | Flags |
|---|---|---|---|---|---|---|
| a01 | 333 | 2455 | 7.4 | 334 claimed | 34 | RESOLVED: parser 333 = GRETIL numbering; legacy header 334 (1 extra) frozen, not fixed |
| a02 | 50 | 406 | 8.1 | 50 | 5 | clean |
| a03 | 295 | 2312 | 7.8 | 295 | 30 | verse 0b present (marked [AbhT_3.0]) — spans keyed 0–294, v00 translated with work |
| a04 | 279 | 2231 | 8.0 | 279 | 28 | clean |
| a05 | 159 | 1150 | 7.2 | 159 | 16 | clean |
| a06 | 252 | 1998 | 7.9 | 252 | 26 | clean |
| a07 | 71 | 573 | 8.1 | 71 | 8 | clean |
| a08 | 452 | 3559 | 7.9 | 452 | 46 | clean |
| a09 | 314 | 2611 | 8.3 | 314 | 32 | clean |
| a10 | 310 | 2557 | 8.2 | 310 | 31 | clean |
| a11 | 118 | 940 | 8.0 | 118 | 12 | clean |
| a12 | 26 | 204 | 7.8 | 26 | 3 | clean |
| a13 | 362 | 2891 | 8.0 | 362 | 37 | clean |
| a14 | 47 | 362 | 7.7 | 47 | 5 | clean |
| a15 | 613 | 4772 | 7.8 | 613 | 62 | LARGEST |
| a16 | 311 | 2315 | 7.4 | 311 | 32 | clean |
| a17 | 122 | 930 | 7.6 | 122 | 13 | clean |
| a18 | 11 | 104 | 9.5 | 11 | 2 | longer verses (mixed meter?) |
| a19 | 56 | 453 | 8.1 | 56 | 6 | clean |
| a20 | 16 | 118 | 7.4 | 16 | 2 | clean |
| a21 | 61 | 460 | 7.5 | 61 | 7 | clean |
| a22 | 48 | 370 | 7.7 | 48 | 5 | clean |
| a23 | 103 | 810 | 7.9 | 103 | 11 | clean |
| a24 | 24 | 172 | 7.2 | 24 | 3 | clean |
| a25 | 29 | 237 | 8.2 | 29 | 3 | clean |
| a26 | 76 | 601 | 7.9 | 76 | 8 | clean |
| a27 | 59 | 461 | 7.8 | 59 | 6 | clean |
| a28 | 435 | 3465 | 8.0 | 435 | 44 | clean |
| a29 | 292 | 2290 | 7.8 | 292 | 30 | Kaula rite (hard content) |
| a30 | 123 | 946 | 7.7 | 123 | 13 | clean |
| a31 | 164 | 1334 | 8.1 | 164 | 17 | clean |
| a32 | 69 | 561 | 8.1 | 68 | 7 | v00 topic line carved (atha kathaye mudrāṇāṃ…) — spans keyed 0–68 |
| a33 | 33 | 230 | 7.0 | 32 | 4 | v00 topic line carved (athāvasarasaṃprāpta ekīkāro…) — spans keyed 0–32 |
| a34 | 5 | 23 | 4.6 | 4 | 1 | SMALLEST — pilot candidate; v00 topic line carved (ucyate…svasvarūpapraveśaḥ…) — spans 0–4 |
| a35 | 44 | 341 | 7.8 | 44 | 5 | clean |
| a36 | 17 | 130 | 7.6 | 16 | 2 | v00 topic line carved (āyātiratha śāstrasya…) — spans keyed 0–16 |
| a37 | 85 | 768 | 9.0 | 85 | 9 | longer verses (mixed meter?) |
| Total | 5864 | — | — | — | — | — |

Units = numbered verses + carved v00 topic lines (a03 marked in source;
a32/a33/a34/a36 carved by parser, songs lists start at 0). Uniform anuṣṭubh
śloka profile (median 7–8 tokens/verse). No verse-number gaps. a01: parser
333 = GRETIL numbering — the old 334-vs-333 discrepancy was header leakage
into v1, resolved by the fix.

## Meter notes (from token-length distribution)

Nearly all śloka anuṣṭubh (pāda ≈ 8 syllables ≈ 4–5 tokens/pāda → ~8
tokens/verse at whitespace tokenization… observed medians 7–8 fit fused
compounds). Outliers: a18 (avg 9.8) and a37 (avg 9.1) likely carry
triṣṭubh/upajāti stretches — verify at transform time by scansion, do not
assume.

## Difficulty tiers (size-led; content flags noted)

- XS (≤30u): a34(5u: v00+4), a18(11), a20(16), a36(17u: v00+16), a24(24), a12(26), a25(29).
  Pilot tier. a34 is 4 verses + topic line — first transform candidate.
- S (30–70): a33(33u: v00+32), a35(44), a14(47), a22(48), a02(50), a19(56), a27(59),
  a21(61), a32(69u: v00+68).
- M (70–150): a07(71), a26(76), a37(85), a23(103), a11(118), a17(122),
  a30(123).
- L (150–320): a05(159), a31(164), a06(252), a04(279), a29(292 + Kaula-rite
  content-hard), a03(295 + verse-0), a10(310), a16(311), a09(314).
- XL (330+): a01(333, off-by-one resolved by parser fix), a13(362), a28(435), a08(452),
  a15(613, the campaign's Everest).

Content-hard flags (from tradition, to confirm with lore at transform time):
a29 (kula-yāga rite), a15 (largest + phonematic doctrine), a28 (cosmic body),
a01 (opening stakes: jñāna/ajñāna, pratyabhijñā seed), a37 (closing).

## Witness status (vendored vs needed per ahnika)

No Tantraloka witness vendored in lore/witnesses/ (only sivastotravali
Lakshmanjoo + legacy L2s for small works). Expect qa NEEDS_WITNESS for
all transforms unless the owner decides otherwise. External parallels
(comparison only, never hosted/copied): Dyczkowski 11-volume translation +
Jayaratha commentary (Vol 1=ch1, Vol 2=ch2–3, Vol 3=ch4, Vol 4=ch5–6,
Vol 5=ch7–8, Vol 6=ch9–10, Vol 7=ch11–14, Vol 8=ch15, Vol 9=ch16–27,
Vol 10=ch28–29, Vol 11=ch30–37); Lakshmanjoo revelation + lectures;
Hareesh.org ch1 + ch29 partial translations; OccultGuide chapter summaries
(incl. ch15 full); Muktabodha IAST (M00093, ch15–38); HuggingFace
tantraloka-dyczkowski-raw dataset (glossary/entities index — lookup aid,
never source text).
Chapter-specific: Vol 5 TOC maps ch7 (cakrodaya, 71v) + ch8 (deśādhvan,
224 worlds, 452v); Vol 10 summary maps ch28 (parvan/Aadiyāga/pavitraka/
vyākhyā/gurupūjā) + ch29 (kula-yāga, 292 deliberately obscure verses,
dūtī, six vedhas); Vol 8 = ch15 (samaya initiation, Trika trident,
36+1 levels); Vol 1 TOC maps ch1 (vijñāna types vv2–105, means vv140–247,
topics enunciation vv279–333).

## Lore for the top-5 hardest (one focused search each, 2026-11-06)

- a15 (613, Everest): Dyczkowski Vol 8 (samaya initiation, Trika trident,
  Parā/Parāparā/Aparā on Bhairavas, 36+1 levels) + OccultGuide ch15 full
  translation + Muktabodha M00093 IAST. Entry point for transform: Vol 8
  structure + OccultGuide paragraph map.
- a29 (292, Kaula rite): Hareesh 12-parter in progress (abstruse by design,
  bracketed insertions, 6 ways of kula-yāga, dūtī, six vedhas); Dupuche
  551pp monograph; Silburn union-and-unity study; Dyczkowski Vol 10 summary
  (tantra→kula modality break at ch29, Jayadrathayāmala Mādhavakula source).
  NOTE: esoteric content — translate faithfully, no bowdlerizing, no
  sensationalizing; witness with brackets as Hareesh does.
- a08 (452, deśādhvan): Dyczkowski Vol 5 (Svacchanda-based, 224 worlds in
  36 tattvas) + first-100-verses PDF (Devanāgarī+IAST+translation) +
  Lakshmanjoo revelation (authority, not text).
- a28 (435, parvan/Aadiyaga): Dyczkowski Vol 10 summary (nitya vs
  nimittika rites, Aadiyāga foremost sacrifice, pavitraka, vyākhyāvidhi,
  expiation, gurupūjā) — pairs with our a20 gold (same rite complex).
- a01 (333, foundation): Dyczkowski Vol 1 TOC (vijñāna types, means,
  topics enunciation) + Hareesh ch1 partial + ch1 PDF (Devanāgarī+IAST).
- a13 (362, next): no dedicated search yet; Vol 7 covers ch11–14 only —
  queue a dedicated search at transform time.

## Transform order (owner goal: shortest-first, a34 → … → a15)

a34(5) → a18(11) → a20(16) → a36(17) → a24(24) → a12(26) → a25(29) →
a33(33) → a35(44) → a14(47) → a22(48) → a02(50) → a19(56) → a27(59) →
a21(61) → a32(69) → a07(71) → a26(76) → a37(85) → a23(103) → a11(118) →
a17(122) → a30(123) → a05(159) → a31(164) → a06(252) → a04(279) →
a29(292) → a03(295) → a10(310) → a16(311) → a09(314) → a01(333) →
a13(362) → a28(435) → a08(452) → a15(613).

## Registration (workcfg, kind=taloka, songs tsa-aNN)

Batches: A (a01–12), B (a13–25), C (a26–37). Song id form `tal-aNN`
(one song per ahnika, verse-addressed data objects like tantrasara golds).
Do NOT touch legacy files.

## Open items for owner (do not self-resolve)

1. Transform order approval (list above) + pilot nod for a34.
2. Witness decision: vendored witness for Tantraloka (Dyczkowski text cannot
   be hosted — rights; Lakshmanjoo-style notes don't exist for TAL)? If none,
   all proofs carry NEEDS_WITNESS honestly.
3. a18/a37 mixed-meter question can wait until transform (scansion then).
4. a01 334-vs-333 RESOLVED 2026-11-07: the phantom 334th was `:C`/`:E`
   header leakage into v1 (parser bug, fixed). Parser 333 = GRETIL numbering.
   Legacy T1.md header still claims 334 — frozen, not fixed.
