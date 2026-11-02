# TEN — what 10/10 means (frozen 2026-11-02)

*One point per criterion. A song is 10/10 when all ten hold.
Machine-checkable where possible; human-judged where not.
COMPLETE still means machine-proposed until a human signs off.*

1. **T1 covers the FULL source, pada-split.** Every compound analyzed to stems;
   zero whitespace-compounds standing as tokens. Verse count matches the edition.
2. **T1 glosses accurate.** No category errors: honorific bhavat- vs √bhū
   participle, enclitic te/me vs demonstratives, participles vs finite verbs —
   verified per verse, not per pattern.
3. **L0 100% PARSED, morph analyzed everywhere.** Zero morph_unknown.
   Every token carries real morphology, not comp() vagueness where analysis is possible.
4. **Genuine forks minted.** ≥1 per ~5 verses, each with grounds + source
   (grammar / lakshmanjoo / bailly / ksemaraja-vivrti / witness-*). No invention forks.
5. **Forks adjudicated on the record.** resolved ⟺ argmap option_choices entry;
   live ⟺ honestly undecided with the decision deferred, never smoothed.
6. **Argmaps structured.** Terse premises (never chopped L2), real inference
   (never restated question), uncertainties in place (never "see C1", never empty
   where a crux exists). Correct poet in speaker (Utpaladeva here).
7. **L2 complete and faithful.** Every pada rendered (zero drops, zero truncations);
   no inventions (husband, hx), no inversions (active/passive, inside/outside),
   no garble. Cites byte-exact including editorial marks, doubt logged not scrubbed.
8. **L2 rasa-carried.** Word choices justified by the verse's sthāyibhāva;
   one voice per song. "Sounds better" is not a reason.
9. **C1 capstone.** Sharp SUMMARY + filled rasa{} + full NOTE (commentary complete).
   Poetic realization follows the frozen register split (L2 plain / C1 poetic).
10. **Provenance.** Proof PASS, witness-QA triaged (SHIP notes become todos, not dust),
    history[] on every changed object, signoff scope stated.

## Current map (2026-11-02 audit)

- 8s (s01/s04/s05): missing 4 (fork density), 8 (rasa pass), 9 (poetic).
- 7.5s (s02/s06/s07/s08): missing 4, 8, 9 + tier-specific residue.
- 7s (s03/s10/s11/s12/s13/s17): missing 1 (s14 only), 3 (s09+), 4, 5 (s01-05 shape), 6 (s17 done, s09+ residue), 8, 9.
- 6.5s (s09/s15/s16/s18/s19/s20): missing 4, 8, 9 + residue noted per song.
- 5.5 (s14): missing 1 (v02-v24), then 4, 8, 9.

## Order of work

Structure first (criterion 1: s14 splits), then decisions (4+5: forks),
then voice (8), then capstone (9). Criteria 2/3/6/7/10 are enforced per-verse
as we go; check.py guards 7/10 mechanically after every change.
