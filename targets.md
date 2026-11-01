# TARGETS — crystal queue (one at a time)

*Reordered 2026-11-01 after the ipvv deepdive audit (lore/ipvv-deepdive-2026-11-01.md)
and the canonical process finalization (FINAL-PROCESS.md). Order: short first, verify-before-rebuild,
corrupt-T1 last, no-repo-dir works need source. "Gold" = transformed to crystal standard.*

## Gold (done — 11 works + 1 partial)

| # | Work | Verses | Notes |
|---|------|--------|-------|
| 1 | pancashloki | 5 | crystal template |
| 2 | bhairavastava | 10 | repaired + sharpened |
| 3 | anuttarastika | 8 | crystal 2026-11-01 |
| 4 | parapravesika | prose (9 pass.) | built end-to-end |
| 5 | bodhapancadasika | 15 | crystal rebuild |
| 6 | bodhavilasa | 42 | crystal verify |
| 7 | bhairavanukarana | 48 | crystal rebuild |
| 8 | ajadapramatrsiddhi | 27 | crystal rebuild |
| 9 | paryantapancasika | 52 | crystal verify |
| 10 | pratyabhijnahrdaya (phrdaya) | 20 | crystal verify |
| 11 | ghatakarpara | 21 | crystal 2026-11-01 (full process, 7 passes) |
| 12 | spandasandoha | 2 | crystal 2026-11-01 (full process, peer review, concept db) |
| — | sivastotravali | 25 songs | partial: s01–s05 canonical, s06–s20 legacy |

## Queue (ordered by: short → verify → rebuild → corrupt → no-source)

### Tier A — short, repo present, needs transformation

| # | Work | Verses | State | Why this order |
|---|------|--------|-------|----------------|
| 13 | sambandhasiddhi | 9 (3 pass.) | tier-1, verify only | shortest remaining; T1 is raw Sanskrit but passages are dense; verify only |
| 14 | kramastotra | 30 (30 pass.) | tier-3, needs rebuild | short, mechanical, needs rebuild |
| 15 | isvarasiddhi | 56 (7 pass.) | T1 corrupt | needs T1 rebuild; dense philosophy |
| 16 | ptvmadhyama | 35 (4 pass.) | T1 corrupt | needs T1 rebuild; Madhyamaka |
| 17 | stavacintamani | 120 | tier-3, L2.v2 corruption | big; needs full rebuild; do after short works |

### Tier B — sivastotravali (per-song, 20 remaining)

| # | Song | Verses | State |
|---|------|--------|-------|
| 18 | s06 | 11 | legacy (argmap+L2+C1 exist, T1 raw) |
| 19 | s07 | 9 | legacy |
| 20 | s08 | 13 | legacy |
| 21 | s09 | 20 | legacy |
| 22 | s10 | 26 | legacy |
| 23 | s11 | 15 | legacy |
| 24 | s12 | 29 | legacy |
| 25 | s13 | 20 | legacy (argmap+L2+C1 exist) |
| 26 | s14 | 24 | legacy |
| 27 | s15 | 19 | legacy |
| 28 | s16 | 30 | legacy |
| 29 | s17 | 48 | legacy |
| 30 | s18 | 21 | legacy |
| 31 | s19 | 17 | legacy |
| 32 | s20 | 21 | legacy |

### Tier C — no repo dir (need source + full build)

| # | Work | Verses | State |
|---|------|--------|-------|
| 33 | anubhavanivedana | 4 | needs source + full build |
| 34 | paramarthacarca | 8 | needs source + full build |
| 35 | paramadvayadvadashika | 13 | needs source + full build |
| 36 | dehastha | 16 | needs source + full build |
| 37 | rahasyapanchadashika | 16 | needs source + full build |
| 38 | mahopadeshavimshatika | 20 | needs source + full build |
| 39 | tattvasandoha | ? | needs source + full build |

### Tier D — big works (do last)

| # | Work | Verses | State |
|---|------|--------|-------|
| 40 | paramarthasara | 105 | tier-1, verify only |
| 41 | stavacintamani | 120 | tier-3, L2.v2 corruption |

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

21 concept files (10 from sivastotravali-era + 11 from ghatakarpara/spandasandoha).
325-term glossary index (sanskrit-trikashaivism.com, scraped).
build_concepts.py reports coverage. Gold works must have 100%. Legacy works get a warning.
Concept database is post-translation (derivative of C1 KEY TERMS, not prerequisite).

## Registry

REGISTRY.json tracks all 94 works: 11 gold, 1 partial, 82 pending.
FINAL-PROCESS.md is the canonical process. check.py is the gate (CANONICAL: 0 failures).
