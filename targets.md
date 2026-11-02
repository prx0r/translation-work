# TARGETS — crystal queue (one at a time)

*Rewritten 2026-11-02: prior edition (2026-11-01) was stale — it listed old-format works as gold, showed anubhavanivedana/paramarthacarca as "no repo dir", and sivastotravali as partial. "Gold" below = canonical data pipeline (T1/L0/argmap/L2/C1/L3 JSON + validate + proof PASS), matching REGISTRY.json. Old-format works with full legacy pipelines are ranked as transform candidates, shortest first.*

## Gold (done — 11 works, canonical pipeline)

| # | Work | Verses | Audio |
|---|------|--------|-------|
| 1 | spandasandoha | 2 | — |
| 2 | anubhavanivedana | 4 | — |
| 3 | pancashloki | 5 | — |
| 4 | anuttarastika | 8 | ✓ |
| 5 | paramarthacarca | 8 | — |
| 6 | bhairavastava | 10 | ✓ |
| 7 | ghatakarpara | 21 | — |
| 8 | sambandhasiddhi | 23 | — |
| 9 | ajadapramatrsiddhi | 27 | — |
| 10 | isvarasiddhi | 56 | — |
| 11 | sivastotravali | 450 (20 songs) | — |

## Queue — Tier 1: transform (legacy pipeline present, shortest first)

Old-format T1/L2/argmaps/c1/passages exist; job = canonical data objects per song + validate + proof + handcrafted L3, per AGENTS.md "How to Transform a Legacy Work".

| # | Work | Size | State |
|---|------|------|-------|
| 12 | parapravesika | prose, 9 passages | built end-to-end 2026-11-01, needs human-review + transform — **NEXT** |
| 13 | bodhapancadasika | 15 | legacy old-format |
| 14 | phrdaya | 20 verses, 5 passages | raw verified 2026-10-31 |
| 15 | kramastotra | 30 verses, 30 passages | tier-3, needs rebuild |
| 16 | bodhavilasa | 42 | legacy old-format |
| 17 | bhairavanukarana | 47 verses, 5 passages | needs human-review |
| 18 | paryantapancasika | 52 | legacy old-format |

## Queue — Tier 2: verify / rebuild

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
