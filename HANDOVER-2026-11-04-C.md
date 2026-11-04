# HANDOVER — 2026-11-04 (C): vbt GOLD #29 + the overlap-audit lesson

*For the next agent. Read AGENTS.md → todoregistry.md → REGISTRY.json → HANDOVER-2026-11-04-B.md → this file.*
*Nothing below is invented: every count came from a gate run this session.*

## 0. Where we stand (verified, all committed)

- **REGISTRY**: 92 works / **29 gold** / 63 pending.
- **Gold #29 vbt** (162v full tantra, 17 songs): T1 span-exact / L0 1717 tok 100% PARSED 0 drift / argmaps 162/162 / L2 rasa-carried byte-exact / C1 essence+7-part+rasa 0 quotes/meta/shared / data t1/l0/argmap/l2/c1/l3/l4 x17 / L3 162 couplets 0 shared w/ L2 / L4 162 DRAFTs song-set w/ craft_notes+rejected-killers+reads_against / C2 eli5+genz full essence coverage (translator-hand) / c1.NOTE x17 (voice maps, key terms, cruxes). validate 0 x17 · proof PASS x17 · roundtrip 0 x17 · `check.py --work vbt` **CANONICAL: 0 failures** · qa NEEDS_WITNESS (no witness vendored — honest, same as all golds).
- **63 pending** = 5 no-repo intakes (dehastha, mahopadeshavimshatika, paramadvayadvadashika, rahasyapanchadashika, tattvasandoha) + paramarthadvadasika anomaly + tantrasara-a03-a22 (20) + tantraloka-a01-a37 (37).

## 1. Two discipline events this session (both caught, both fixed, both committed)

1. **L3 data never emitted.** L4 validation failed x14 songs with 'l4 present without L3' (28 gate failures) because `data/*.l3.json` was never written — working L3 existed but the data lane stopped at c1. Fix: verbatim emit working→data (gold pattern, cf. paratrimshika), validate 0 x17. Lesson: the data lane is part of the layer — a layer not emitted does not exist to the gate.
2. **p13-p14 L4 composed from memory, 0% true.** 20 verses (v121-140) were sung from remembered themes while the actual verses teach devotion-excess, equal-pairs, net-questions, sovereign speech. Schema validation passed (traces copied from real L3) — the English sang a different tantra than the traces proved. Caught by a content-word overlap audit (L4 lines vs own L3: bad 20 at 0.00-0.25, good 142 at ≥0.83, median 1.0). RE-SUNG from extracted L3+argmap+essence; re-audited 162/162 aligned. Codified as **mistakes.md #19**: extract first, sing second; overlap-audit every L4 batch; the validator checks traces, only the audit checks the song is about the verse.

## 2. Standing owner items (unchanged, still binding)

- First-verse L4 voice verdict per recent gold (vbt v01 outstanding) + human review of every machine-proposed stack. Nothing marked final.
- paratrimshika↔ptvmadhyama cross-link; legacy-L2 witness conversion + qa re-run; ptvmadhyama re-aim decision; paramarthadvadasika anomaly.
- tantrasara/tantraloka scope confirmed deferred until after no-repo intakes (prior handover §5).

## 3. Next (ordered)

1. No-repo intakes ×5 (+anomaly) via `tools/intake.py` — one work at a time, full 14-step pipeline each.
2. tantrasara-a03–a22 (20), same pattern as a01/a02.
3. tantraloka-a01–a37 (37) — owner confirms scope before starting.
