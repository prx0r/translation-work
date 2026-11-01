# CRYSTAL — what a finished work looks like

*Standard, with exhibits. A work is crystal when every check below passes. Pancashloki and Bhairavastava (as of 2026-10-31) are the reference specimens — machine-proposed, pending human review, but structurally crystal.*

## The checks

1. **T1 covers the full source.** Every pāda glossed, verses counted against the edition — not against the tool report. L0 at 114/114 or 137/137 is necessary, never sufficient: Bhairavastava once passed at 59/59 while missing the first half of all 10 verses.
2. **C1 shares zero long sentences with L2** (checked mechanically). L2 translates; C1 condenses. Any overlap means C1 was copied, not written.
3. **No sentence is shared across the work's argmaps** (checked mechanically). Each passage gets its own lore and its own reconstruction.
4. **No quoted English gloss-words, no metacommentary.** No "the verse/hymn/stotra does X", no "imagery/grammar does Y", no scare quotes. Sanskrit in parens does all anchoring.
5. **Uncertainties marked, never smoothed** (prāsuvatkāyaḥ, tanutāpavidhātrī, vasurasapauṣe, yena's antecedent).
6. **Lucidity test:** read C1.v2 alone — a stranger gets the whole argument in one pass.

## Crystal exhibits (from the two specimens)

- Whole-arc paragraph, Bhairavastava: *"The all-pervading, consciousness-made, one, endless, beginningless real — Bhairava, refuge of the helpless — met by a mind become His, venerating in the heart... Veneration → grace-disclosure → identity → no-fear-talk → averted gaze → power-filled → darkness dispelled → fearlessness → awakening → entry → affliction-occasion → nondifference → rites relativized → contemplation → rejoicing → vision → pacification."*
- Verse-level condensation, Pañcaślokī v. 3: *"Five denials of divine response (speak, see, hear, come, support) gathered into one śruti-verdict: devoid of the organs of response."*
- Verse-level condensation, Bhairavastava v. 6: *"Bliss is the destination of entering, not a feeling felt: emi takes nirvṛtim as its goal — to enter the being-full, nectar-laden, complete Lord."*
- Marked uncertainty, Pañcaślokī v. 5: *"whose body has attained it (prāsuvatkāyaḥ)"* — flagged obscure in argmap §3 rather than glossed over.

## Non-crystal exhibits (found in-repo, queued for one-by-one rebuild)

- **Gloss dumped as C1** (stavacintamani C1.md): *"EXPLANATION. The passage moves in three steps. (1) Power: whose desire alone has fruit (three-world); Lord, who knows extent of works; Brahmā etc. run up karma-ladder..."* — T1 gloss pasted under a C1 heading. No argument stated.
- **Talking about the text** (kramastotra C1.v2, before fix): *"The stotra is about the 'sequence' (krama)"* — metacommentary plus scare quotes; the passage's claim never appears.
- **Quoted translations standing in for condensation** (anuttarastika, sivastotravali, paryantapancasika C1s): whole rendered lines in quotes where the argument should be. Quotes stripped 2026-10-31; deep rewrite queued.
- **Coverage fraud by parse rate** (bhairavastava, before fix): L0 59/59 PARSED while T1 carried only second halves. Fixed by restoring full verses → 114/114.
- **Copy-paste lore** (bhairavastava argmaps, before fix): identical 60-word lore paragraph in all 10 files. Fixed with verse-specific notes; verified zero shared sentences.

## Rule of the house

One work at a time. T1/L0 → argmaps → L2 → C1 → mechanical checks (parse rate, zero-overlap C1/L2, zero-overlap argmaps, no quotes, no metacommentary phrases) → human review. Nothing is marked complete by the machine.
