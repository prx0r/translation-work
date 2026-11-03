# SKILL: l4-song — the song transmission

*Companion to `skills/crystal-ipvv/SKILL.md` (the canonical translation
process). This skill governs ONLY the L4 pass: L3 set to music. Read it with
`process/L4-SONG-PROCESS-2026-11-03.md` (verbatim owner directives),
`lore/rasa/english-transmission-2026-11-03.md` (transmission table), and
`lore/bank/songcraft-bank.json` (21 exhibits). Standard: `crystal.md`.
Failure log: `mistakes.md` #17. Validator: `schemas/l4.py`.*

## The drill (one verse at a time, no batches)

1. **Sanskrit first — ultimate authority.** Re-read the verse's
   `sanskrit_cite` and parse it fresh yourself: cases, compounds, verb tense
   and aspect, word order, where the sentence lands. Everything else — T1, L0,
   argmap, L2, C1, L3 — is ideas about the verse. If the layers disagree with
   your parse, the Sanskrit wins; record the correction in craft_notes.
2. **Read all prior levels.** T1 glosses → L0 tokens/morph/forks → argmap
   premises/inference/uncertainties → L2 voice → C1 essence indices + rasa
   block → L3 frozen lines. Copy `l0_ids`, `essence_maps`, `sanskrit_cite`
   from the verse's L3 (subset = equality is safest).
3. **Name the sthāyin** (one phrase) + the verse's color inside the song's
   rasa. Name which transmission-table rows fire (compounds→enjambment,
   verb-final→end-weight, yamaka→assonance, gait→gait, refrain→repeat,
   vocative→kept, vowel arc, rupture-point, close-shape).
4. **Draft the song** from L3 with small edits: rhythm, order, sound, rhyme,
   refrain. Steal devices from the bank, never style. Candidate defaults:
   couplet; octosyllabic for dance-passages; end-weight doctrine words
   line-final; refrains verbatim-repeated; `form` recorded.
5. **Justify verse by verse**, saved WITH the verse (DRAFT-file form):
   `craft_notes` (every edit + reason + Abhinavagupta frame + read-aloud
   audit + corrections like stay→ground) and `reads_against` (the exact
   layer readings used). A justification written after the fact is decoration;
   write it as you compose. **Name the rejected options**: every real
   alternative you considered (a diction swap, a different line-break, a
   kept-vs-dropped particle, a refrain placement) with the reason it lost —
   which layer, row, or read-aloud fact killed it. A choice with no named
   rival is a preference, not a decision.
6. **Validate, then confess.** Schema (no `/`, exact diacritics Śiva/Māyā/
   Śambhu, traces exist, essence in range) + subset vs L3 + coverage when the
   song completes. Any failure is flagged to the owner WITH the beauty-reason
   — beauty may break rules, it may not hide the breakage.
7. **Verdict before continuing.** DRAFT file outside `data/`
   (`<work>/L4-<song>-vNN.DRAFT.json`). Merge into `data/<song>.l4.json`
   only on owner approval. First verse of a work sets the voice: extra
   scrutiny, no onward movement until it lands.

## Loop per verse (say it while composing)

> Sanskrit → sthāyin → firing rows → draft → justify → validate → confess →
> verdict.

## Non-negotiables

- A line the Sanskrit cannot bear is invention, not song — however beautiful.
- A rhyme that needs a new slant is new doctrine: re-ground it or drop it.
- "O" and refrains carry no doctrine and must smuggle none.
- The ear is the last gate: read aloud; if it won't scan, it won't parse.
- One verse at a time. Batch songwriting is batch production (mistakes.md
  #10/11/15), however the lines were composed.
