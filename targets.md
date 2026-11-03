# TARGETS — crystal queue (one at a time)

*Updated 2026-11-02 (Tier 1 complete, 18 gold). Rewritten earlier 2026-11-02: prior edition (2026-11-01) was stale — it listed old-format works as gold, showed anubhavanivedana/paramarthacarca as "no repo dir", and sivastotravali as partial. "Gold" below = canonical data pipeline (T1/L0/argmap/L2/C1/L3 JSON + validate + proof PASS), matching REGISTRY.json. Old-format works with full legacy pipelines are ranked as transform candidates, shortest first.*

## Gold (done — 18 works, canonical pipeline)

| # | Work | Verses | Audio |
|---|---|------|--------|
| 1 | spandasandoha | 2 | — |
| 2 | anubhavanivedana | 4 | — |
| 3 | pancashloki | 5 | — |
| 4 | anuttarastika | 8 | ✓ |
| 5 | paramarthacarca | 8 | — |
| 6 | bhairavastava | 10 | ✓ |
| 7 | bodhapancadasika | 15 | — |
| 8 | phrdaya | 20 (5 songs) | — |
| 9 | ghatakarpara | 21 | — |
| 10 | sambandhasiddhi | 23 | — |
| 11 | ajadapramatrsiddhi | 27 | — |
| 12 | kramastotra | 30 | — |
| 13 | bodhavilasa | 41 (5 songs; print jumps 13→15) | — |
| 14 | bhairavanukarana | 48 | — |
| 15 | paryantapancasika | 52 | — |
| 16 | isvarasiddhi | 56 | — |
| 17 | parapravesika | prose, 9 passages | — |
| 18 | sivastotravali | 450 (20 songs) | — |

## Queue — Tier 1: TRANSFORM COMPLETE 2026-11-02

All seven Tier-1 works transformed to gold this session (parapravesika, bodhapancadasika, phrdaya, kramastotra, bodhavilasa, bhairavanukarana, paryantapancasika). Notable cruxes logged in data NOTEs: v24 hemistich recovered (krama), kalayantī emendation + live fork (krama v26), print jumps (bodhavilasa 13→15), double-marked v12 (bodhavilasa), missing 43-marker (paryanta), siddhi-triple revision (phrdaya).

## Queue — Tier 2: verify / rebuild — **NEXT**

paramarthasara DONE 2026-11-03 — gold #19 (105 verses, full transform; v1 recovered). Next: stavacintamani (120 verses, rebuild) or ptvmadhyama (T1 rebuild first).

## Queue — Tier 2 detail: verify / rebuild

| # | Work | Size | State |
|---|------|------|-------|
| 19 | paramarthasara | 104 verses, 12 passages | tier-1, verify only |
| 20 | stavacintamani | 120 verses, 12 passages | tier-3, needs rebuild |
| 21 | ptvmadhyama | 35 verses, 4 passages | T1 corrupt, needs T1 rebuild first |

## Queue — Tier 3: source acquisition (no repo data yet)

| # | Work | Verses |
|---|------|--------|
| 22 | paramadvayadvadashika | 13 |
| 23 | dehastha | 16 |
| 24 | rahasyapanchadashika | 16 |
| 25 | mahopadeshavimshatika | 20 |
| 26 | tattvasandoha | ? |

## Queue — Tier 4: campaigns (37 + 22 legacy works)

| # | Work | Size |
|---|------|------|
| 27 | tantrasara-a01…a22 | 22 works, legacy |
| 28 | tantraloka-a01…a37 | 37 works, legacy |

## Rules (from mistakes.md + crystal.md + FINAL-PROCESS.md)

One work at a time. T1/L0 → argmaps → L2 → C1 → L3 (handcrafted, never copied from L2) → mechanical checks → human review.
Nothing marked complete by the machine; COMPLETE always means "machine-proposed, needs human review."
Each transformation: lore search (one) + rasa file + peer review + process note + commit.
check.py must pass before any commit. Tools resolve (work, song) via tools/workcfg.py — register new works there instead of hardcoding.

## Audit findings (from ipvv deepdive, 2026-11-01) — disposition 2026-11-02

1. Generic glossary (T7): DONE — per-work ledgers in T1 headers.
2. Unlocatable L200/C1 (F3): DONE — canonical data paths + site emission.
3. "DONE" vs 0 PASS (F1): DONE — STAGED vocabulary; machine-proposed everywhere.
4. T1 raw-Sanskrit records (F2): DONE — pada-split gloss bars enforced.
5. Recension notes (F4): DONE — variants in argmap uncertainties + NOTEs.
6. GATE status in Notes (F5): DONE — proof records carry gate + lineage.
7. `needs` field (F6): DONE on our side.
8. Namespace collision (F7): OPEN — works/ipvv vs works/spanda-sutra naming, decide with owner.

## Concept database

lore/concepts/ — derivative of C1 KEY TERMS, post-translation (not prerequisite).
build_concepts.py reports coverage. check.py enforces 100% only for works listed in its is_gold tuple (currently ghatakarpara, spandasandoha — extend as concept files are built).

## Registry

REGISTRY.json tracks all 92 works: 11 gold, 0 partial, 81 pending.
FINAL-PROCESS.md is the canonical process. check.py is the gate (CANONICAL: 0 failures).
