# TARGETS — crystal queue (one at a time)

*User-supplied list, 2026-10-31. Order below is the build order. Status: done items stay in REGISTRY completed; everything else is queued here. "Repo" = whether /root/translation-work already has a directory (many listed counts refer to outside pipelines, not this repo).*

| # | Work | Verses | Repo dir | State |
|---|------|--------|----------|-------|
| 1 | pancashloki | 5 | yes | DONE (crystal template, 2026-10-31) |
| 2 | bhairavastava | 10 | yes | DONE (repaired + sharpened, 2026-10-31) |
| 3 | anuttarastika | 8 | yes | DONE (crystal 2026-11-01: T1 197/197, per-verse argmaps, C1 distinct, gates pass) |
| 4 | anubhavanivedana | 4 | NO | needs source + full build |
| 5 | paramarthacarca | 8 | NO | needs source + full build |
| 6 | parapravesika | prose (9 pass.) | yes | DONE (built end-to-end 2026-11-01: T1 1116/1116, readable C1, all gates pass) |
| 7 | sivastotravali | 25 | yes | tier-2, needs C1 separation + lore check |
| 8 | bodhapancadasika | 15 | yes | DONE (crystal rebuild 2026-11-01: real argmaps, lucid C1, all gates pass) |
| 9 | kramastotra | 30 | yes | tier-3 mechanical, needs rebuild |
| 10 | stavacintamani | 120 | yes | tier-3 mechanical + L2.v2 corruption, needs rebuild |
| 11 | sambandhasiddhi | 9 | yes | tier-1, verify only |
| 12 | paramarthasara | 105 | yes | tier-1, verify only |
| 13 | dehastha | 16 | NO | needs source + full build |
| 14 | rahasyapanchadashika | 16 | NO | needs source + full build |
| 15 | paramadvayadvadashika | 13 | NO | needs source + full build |
| 16 | mahopadeshavimshatika | 20 | NO | needs source + full build |
| 17 | bodhavilasa | 42 | yes | DONE (crystal verify 2026-11-01: T1 genuine 385/385, C1 rebuilt lucid, all gates pass) |
| 18 | bhairavanukarana | 48 | yes | DONE (crystal rebuild 2026-11-01: T1 per-word 515/515, 48v vs GRETIL, C1 rebuilt lucid, all gates pass) |
| 19 | ajadapramatrsiddhi | 27 | yes | DONE (crystal rebuild 2026-11-01: T1 per-word 285/285, C1 rebuilt lucid, all gates pass) |
| 20 | paryantapancasika | 52 | yes | DONE (crystal verify 2026-11-01: T1 genuine 625/625, C1 rebuilt lucid, all gates pass) |
| 21 | pratyabhijnahrdaya | 20 | yes (phrdaya) | DONE (crystal verify 2026-11-01: T1 genuine, C1 rebuilt lucid, all gates pass) |
| 22 | isvarasiddhi | 17 | yes | T1 corrupt (single-token passages), needs T1 rebuild |
| 23 | ptvmadhyama | 12 | yes | T1 corrupt (single-token passages), needs T1 rebuild |
| 24 | tattvasandoha | ? | NO | needs source + full build |

## Rules (from mistakes.md + crystal.md)

One work at a time. T1/L0 → argmaps → L2 → C1 → mechanical checks → human review. Nothing marked complete by the machine.
