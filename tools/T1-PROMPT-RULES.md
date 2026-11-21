# T1 prompt rules (ported from patalacheckpoints t1_worker + burn lessons)

*Rules every T1 drafting call must carry. Violations found in review are
traced to the missing rule.*

1. **Term-context packet, never flat dictionary.** Technical senses
   (krama, śakti, vimarśa, prakāśa, spanda, kula…) come from the work's
   lore brief + ledger, never a generic gloss.
2. **Unanalyzable → empty, never fabricated.** If a token can't be
   analyzed, gloss "" and flag; a guess presented as fact is worse
   than a gap. (Fixes EF-T1-2026-0003-class tatpuruṣa mis-glosses.)
3. **Preserve negation / polarity / case** exactly in the gloss.
4. **Echo surfaces byte-exact.** Sandhi splits marked with `+`;
   never invent or swap tokens.
5. **Pada-split compounds, not whitespace tokens.** `dvaita+advaita+
   vivarjitam`, never one lump. (Burn lesson: reviewers bounce
   unsplit rows as "bad row".)
6. **Labeled verses, never renumber.** Pass verses pre-split with
   fixed numbers; the model glosses each block under its given number.
   (Burn lesson: continuous text causes numbering slide.)
7. **Batch size ≤25 verses per call; seed triples ≤12 verses.**
   (Burn evidence: 25v triples bounce "premise too short", 12v pass.)
8. **Coverage-gate everything.** Concatenated surfaces must cover the
   source verse at difflib ≥0.85 (sandhi joints explain the rest).
