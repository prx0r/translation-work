# TARGETS — crystal queue (one at a time)

*Reordered 2026-11-01: audio-first (anuttarashtika, bhairavastava — both gold), then shortest-to-longest among pending. "Gold" = transformed to crystal standard (11 works). "Partial" = in progress. "Pending" = awaiting transformation.*

## Gold (done — 11 works)

| # | Work | Verses | Audio |
|---|------|--------|-------|
| 1 | pancashloki | 5 | — |
| 2 | bhairavastava | 10 | ✓ |
| 3 | anuttarastika | 8 | ✓ |
| 4 | parapravesika | prose (9 pass.) | — |
| 5 | bodhapancadasika | 15 | — |
| 6 | bodhavilasa | 42 | — |
| 7 | bhairavanukarana | 48 | — |
| 8 | ajadapramatrsiddhi | 27 | — |
| 9 | paryantapancasika | 52 | — |
| 10 | pratyabhijnahrdaya (phrdaya) | 20 | — |
| 11 | ghatakarpara | 21 | — |
| 12 | spandasandoha | 2 | — |

## Partial (in progress)

| # | Work | Verses | State |
|---|------|--------|-------|
| 13 | sivastotravali | 25 songs | s01–s05 canonical, s06–s20 legacy (per-song) |

## Queue (ordered: audio-first, then shortest-to-longest)

### Tier 1 — very short (≤ 8 verses), no repo dir (need source + full build)

| # | Work | Verses | Audio | State |
|---|------|--------|-------|-------|
| 14 | anubhavanivedana | 4 | — | no repo dir, needs source + full build |
| 15 | paramarthacarca | 8 | — | no repo dir, needs source + full build |
| 16 | paramadvayadvadashika | 13 | — | no repo dir, needs source + full build |
| 17 | dehastha | 16 | — | no repo dir, needs source + full build |
| 18 | rahasyapanchadashika | 16 | — | no repo dir, needs source + full build |
| 19 | mahopadeshavimshatika | 20 | — | no repo dir, needs source + full build |

### Tier 2 — short (≤ 30 verses), repo present

| # | Work | Verses | Audio | State |
|---|------|--------|-------|-------|
| 20 | sambandhasiddhi | 21 | — | tier-1, verify only (T1 is raw Sanskrit) |
| 21 | kramastotra | 30 | — | tier-3, needs rebuild |

### Tier 3 — medium (35–56 verses), repo present

| # | Work | Verses | Audio | State |
|---|------|--------|-------|-------|
| 22 | ptvmadhyama | 35 | — | T1 corrupt, needs T1 rebuild |
| 23 | isvarasiddhi | 56 | — | T1 corrupt, needs T1 rebuild |

### Tier 4 — sivastotravali (per-song, 20 remaining)

| # | Song | Verses | Audio | State |
|---|------|--------|-------|-------|
| 24 | s06 | 11 | — | legacy |
| 25 | s07 | 9 | — | legacy |
| 26 | s08 | 13 | — | legacy |
| 27 | s09 | 20 | — | legacy |
| 28 | s10 | 26 | — | legacy |
| 29 | s11 | 15 | — | legacy |
| 30 | s12 | 29 | — | legacy |
| 31 | s13 | 20 | — | legacy |
| 32 | s14 | 24 | — | legacy |
| 33 | s15 | 19 | — | legacy |
| 34 | s16 | 30 | — | legacy |
| 35 | s17 | 48 | — | legacy |
| 36 | s18 | 21 | — | legacy |
| 37 | s19 | 17 | — | legacy |
| 38 | s20 | 21 | — | legacy |

### Tier 5 — long (100+ verses), repo present

| # | Work | Verses | Audio | State |
|---|------|--------|-------|-------|
| 39 | stavacintamani | 120 | — | tier-3, L2.v2 corruption, needs rebuild |
| 40 | paramarthasara | 104 | — | tier-1, verify only |
| 41 | tattvasandoha | ? | — | needs source + full build |

## Rules (from mistakes.md + crystal.md + FINAL-PROCESS.md)

One work at a time. T1/L0 → argmaps → L2 → C1 → mechanical checks → human review.
Nothing marked complete by the machine; COMPLETE always means "machine-proposed, needs human review."
Each transformation: lore search (one) + rasa file + peer review + process.md + commit.
check.py must pass before any commit.

## Audit findings (from ipvv deepdive, 2026-11-01)

1. Generic glossary (T7): replace 12-term list with per-work ledgers before term-consistency gates.
2. Unlocatable L200/C1 (F3): commit or publish location. Blocks qa_vs_witness.
3. "DONE" vs 0 PASS (F1): rename STAGED. Labels are public claims.
4. T1 raw-Sanskrit records (F2): either gloss or rename the stage.
5. Recension notes (F4): one line each. Counts are claims.
6. GATE status in Notes (F5): so drafts are never cited as results.
7. `needs` field (F6): done on our side; ipvv batch records don't have it.
8. Namespace collision (F7): works/ipvv vs works/spanda-sutra etc. — decide together.

## Concept database

32 concept files (21 from works + 11 from glossary enrichment).
325-term glossary index (sanskrit-trikashaivism.com, scraped).
build_concepts.py reports coverage. Gold works must have 100%. Legacy works get a warning.
Concept database is post-translation (derivative of C1 KEY TERMS, not prerequisite).

## Registry

REGISTRY.json tracks all 94 works: 11 gold, 1 partial, 82 pending.
FINAL-PROCESS.md is the canonical process. check.py is the gate (CANONICAL: 0 failures).
