# PARABLEREGISTRY — parable render queue (shortest first)

Status: LIVING FILE. Order = shortest work first. Paramarthasara is
IN_PROGRESS (literal done all 105; parable songs done: p01, p02, p03,
p12; roadman v1 done all 105). Everything else QUEUED.
Method: `ipvv/skills/allegory` (parable mode). Feedstock per song:
finished literal + L4 + C1 essence + argmap. Output per song: parable
+ hinge map + limit + rasa + voices (GRANNY/KID) + ONE image prompt.
Rule: ordinary words inside, doctrine in the map, no moral inside.

## Queue (gold first, then intake)

| # | Work | Verses | Songs | Literal | Parable | Note |
|---|------|--------|-------|---------|---------|------|
| 1 | spandasandoha | 2 | 1 | — | — | shortest; start here after paramarthasara |
| 2 | anubhavanivedana | 4 | 4 | — | — | |
| 3 | tantrasara-a02 | 4 | 1 | — | — | |
| 4 | pancashloki | 5 | 5 | — | — | |
| 5 | tantrasara-a01 | 5 | 1 | — | — | |
| 6 | anuttarastika | 8 | 8 | — | — | |
| 7 | paramarthacarca | 8 | 8 | — | — | |
| 8 | bhairavastava | 10 | 10 | — | — | has v2 roadman + killers to learn from |
| 9 | bodhapancadasika | 15 | 15 | — | — | |
| 10 | phrdaya | 20 | 5 | — | — | |
| 11 | ghatakarpara | 21 | 3 | — | — | needs recording, not wiring (no chant) |
| 12 | sambandhasiddhi | 23 | 3 | — | — | |
| 13 | ajadapramatrsiddhi | 27 | 3 | — | — | |
| 14 | kramastotra | 30 | 30 | — | — | |
| 15 | bodhavilasa | 41 | 5 | — | — | |
| 16 | bhairavanukarana | 48 | 5 | — | — | |
| 17 | paryantapancasika | 52 | 8 | — | — | |
| 18 | isvarasiddhi | 56 | 7 | — | — | |
| 19 | parapravesika | 9 passages (prose) | 9 | — | — | prose, not verse — parable mode TBD |
| 20 | paramarthasara | 105 | 12 | DONE (LITERAL-DRAFT) | 4/12 (p01,p02,p03,p12) | IN_PROGRESS |
| 21 | sivastotravali | 450 | 20 | — | — | the mountain; last |
| 22 | stavacintamani | TBD (~119) | — | T1 p01-p03 | — | intake: T1 in progress |
| 23 | sivasutra | TBD | — | — | — | intake |
| 24 | spanda | TBD | — | — | — | intake |
| 25 | vbt | TBD | — | L0 partial | — | intake |
| 26 | saktavijnana | TBD | — | — | — | intake |
| 27 | svabodhasiddhi | TBD | — | — | — | intake |
| 28 | tantrasara (full) | TBD | — | — | — | intake; ahnikas split first |
| 29 | ptvmadhyama | TBD | — | — | — | intake |
| 30 | dehastha | TBD | — | chanted | — | intake |

Counts for pending works get filled at intake (verse map first, per
crystal pipeline). Parapravesika is prose — parable treatment undecided.

## Process (per song)

1. Literal exists? If no, run `literal` skill full pass first (Sanskrit
   first, whole stack, no-metaphor rule). Never parable without literal.
2. Read feedstock: literal + L4 couplets (music) + C1 essence + rasa +
   argmap Q/premises (clearest explanation).
3. Collect the song's image-set (its furniture). Reach outside only for
   the frame, never the doctrine.
4. Write the parable: ordinary words only, human scale, one turn, end on
   the turn. No doctrine terms, no moral speech inside.
5. Ship map (hinge only) + limit + rasa + voice map (GRANNY reads;
   KID only where the story has a child — usually silent) + ONE image
   prompt (the song's world as one landscape, black ink on white paper,
   preset `sleepdraw/lora2-inv.yaml`).
6. Rasa set, delivery tagged: rasa → direction; inline tags per damn
   house guide (max 3, one emotion/sentence, pauses do the work).
   Paper-validate: `damn/fish/validate.py` ($0). Drama-3 for shorts
   (owner call). Voice chairs open until owner ear-checks. No renders
   without explicit owner yes per call.
7. ONE image per parable, only after confirmation. Tool: `bl image
   generate --size 1080*1920` (free tier). No generation before the
   parable is confirmed.
8. Assemble the short: image + audio + subtitles, vertical 9:16.
   Phase 1 = still + slow zoom over the listening time. Phase 2 =
   inverted etch reveal (techdou inversion — not yet built).
9. Batch order for the whole queue: ALL scripts first → confirm →
   images + audio → assembly. Never media before confirmation.
10. Run embodiment test (remove doctrine — does it collapse?) and the
   Jesus test (a stranger follows every line?). Fix or drop.
11. Save per-work file: `<work>/PARABLE-v1.DRAFT.json`
   (items per song: song, verses, c2-parable, map, limit, rasa,
   voices, image-prompt). MACHINE_DRAFT until human promotes.

## Seeds (the bar — approved)

- **Paramarthasara song 1** (refuge/question/egg/crystal/mirror):
  worked example in `ipvv/skills/allegory/SKILL.md`. The reference
  parable: ferryman with a life, hinge map, stated limit.
- **Paramarthasara song 12** (fallen/honored/striving/colophon):
  five-paragraph farewell; deposed king; limit = exile ends, this
  road doesn't. Rasa maṅgala-śānta.
- **Paramarthasara song 3** (organs/coverings/rope-snake): teacher +
  student at dawn; ends on the unmeasured fright. First voiced +
  painted exemplar (GRANNY/KID + lora2 prompts).
- Song 2 was re-cut under the ordinary-words law (no Māyā inside);
  current version is the standard for diction.

## STATUS snapshot (2026-11-04)
PARAMARTHASARA songs DONE (drafted): 1, 2, 3, 4 (keeper: spider
parable + P1 seal family), 12 → REMAINING: 5, 6, 7, 8, 9, 10, 11.
All other works: literal first (P0), then songs. Song-4 full media
chain exists (audio/etch/print/seal) as the template.

## PARABLE RATINGS (owner's kid-story bar; spider-song4 = 9.5 benchmark)
ghatakarpara 9.4 · bhairavastava 8.8 · spandasandoha 8.5 ·
parapravesika 8.6 · kramastotra 8.2 · anubhavanivedana 8.0 ·
sambandhasiddhi 8.0 · phrdaya 7.8 · bodhavilasa 7.8 ·
bhairavanukarana 7.6 · pancashloki 7.5 · anuttarastika 7.5 ·
paramarthacarca 7.5 · param-s06/s07/s11 7.5-8.0 ·
bodhapancadasika 7.0 · param-s05/s08/s09/s10 7.0-7.5 ·
sivastotravali 6.8 · ajadapramatrsiddhi 6.8 · isvarasiddhi 6.5 ·
paryantapancasika 5.8 (REDO, new angle: the never-heated pond).
Rationale each: see review notes in PARABLEVIDEO journey log.

## TIER 2 — new golds from pipeline lane (pulled 2026-11-04+)
Shortest→longest. (tantrasara-a17/a18 placed last of tier by owner-
exclusion note: "forget tantrasara" was said for the original queue;
latest order = "all available" — flag kept, both included at end.)

| # | Work | Verses | Songs | Feed |
|---|------|--------|-------|------|
| T2-1 | paramarthadvadasika | 13 | 2 | c1/l2/argmap ✓ |
| T2-2 | dehastha | 16 | 2 | ✓ |
| T2-3 | rahasyapanchadashika | 16 | 2 | ✓ |
| T2-4 | mahopadeshavimshatika | 20 | 2 | ✓ |
| T2-5 | spanda | 25 | 4 | ✓ |
| T2-6 | saktavijnana | 30 | 3 | ✓ |
| T2-7 | svabodhasiddhi | 33 | 4 | ✓ |
| T2-8 | ptvmadhyama | 35 | 4 | ✓ |
| T2-9 | paratrimshika | 36 | 4 | ✓ |
| T2-10 | sivasutra | 75 | 8 | ✓ |
| T2-11 | stavacintamani | 120 | 13 | ✓ |
| T2-12 | vbt | 162 | 17 | ✓ (+ new working-t1) |
| T2-13 | tantrasara-a18 | 2 | 1 | ✓ (owner-exclusion flag) |
| T2-14 | tantrasara-a17 | 6 | 1 | ✓ (owner-exclusion flag) |
| T2-15 | tantrasara-a19 | 7 | 1 | ✓ (owner-exclusion flag; NEW gold) |

NOT parable-ready (no feedstock — pipeline must run first):
tantraloka-a01..a37, tantrasara-a03..a16/a19..a22, tattvasandoha.
