# L4 SONG PROCESS — word for word, as directed

*2026-11-03 · The owner's directives, saved verbatim, then operationalized.
Where this file and a validator disagree, the owner decides verse by verse.*

## Verbatim directives

1. *"for paramarthasara the point is u reread all former layers from t1 l0 c1
argmap all the way to l3 and then using all that context write the l4 song
transmission which basically takes l3 and applies these rules subjectively by
u using all information to create beauty"*
2. *"you can also break rules in the name of beauty"*
3. *"u should also have l4 justification save with it verse by verse exactly
like this"* [i.e. the DRAFT-file form: lines + craft_notes + reads_against]
4. *"ensuring you are reading all prior levels the point is l4 is the complete
exposition using sanskrit abhinavagupta theory and all our analysis"*
5. *"also ensure you are rereading the sanskrit again thats your ultimate
authority the rest is ideas"*

## Operationalized (what the agent actually does, verse by verse)

1. **Sanskrit first, as ultimate authority.** Re-read the verse's
   `sanskrit_cite` fresh — parse it yourself (cases, compounds, verb tense,
   word order), not via anyone's gloss. T1/L0/argmap/L2/C1/L3 are ideas about
   the verse; the Sanskrit is the verse. If the layers disagree with the
   Sanskrit, the Sanskrit wins — record the correction.
2. **Read all prior levels.** T1 (quick glosses) → L0 (tokens, morph, forks)
   → argmap (premises, inference, uncertainties) → L2 (voice) → C1
   (essence indices, rasa block) → L3 (the frozen lines). Note essence_maps
   and the rasa/sthāyin.
3. **Name the sthāyin** (one phrase) and the verse's color inside the song's
   rasa. Name which transmission-table rows fire
   (`lore/rasa/english-transmission-2026-11-03.md` §2).
4. **Draft the song** from L3: small edits, reordering, rhythm, rhyme,
   refrain. Consult `lore/bank/songcraft-bank.json` for the device, not the
   style.
5. **Justify verse by verse**, saved with the verse (craft_notes +
   reads_against, DRAFT-file form): every edit with its reason, the
   Abhinavagupta frame it serves, the read-aloud audit — **plus the
   rejected options**: each genuine alternative considered (diction swap,
   line-break, kept/dropped particle, refrain placement, close-shape)
   with the exact reason it lost (which layer, transmission-table row,
   or read-aloud fact killed it). A choice with no named rival is a
   preference, not a decision.
6. **Validate, then confess.** Run the l4 schema + subset checks. Anything
   that fails is flagged to the owner with the beauty-reason, never silently.
   Beauty may break rules; it may not hide the breakage.
7. **One verse, owner verdict, then continue.** DRAFT files live outside
   `data/` until verdicts accumulate; merge into `data/<song>.l4.json` only
   on approval. First verse of a work sets the voice — it gets extra scrutiny.

## Non-overridable (even for beauty)

- Sanskrit authority (§5 of directives): a beautiful line the Sanskrit cannot
  bear is invention, not song. The subset rule is this principle in
  machine form — break it only with owner eyes on the exact break.
- One at a time (rules 15/17): batch songwriting is batch production,
  however musical the lines.
- Git honesty: DRAFT outside `data/`; canonical only on verdict.
