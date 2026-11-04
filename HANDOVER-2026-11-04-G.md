# HANDOVER — 2026-11-04 (G): 41 golds; the tantrasara-ahnika drill is cracked

*Read after HANDOVER-F. Together: E = beauty-pass method, F = a12 drill, G = scale-out.*

## State (verified: full-sweep 42/42 check.py CANONICAL, 2026-11-04)

- **REGISTRY: 101 works / 41 gold / 60 pending** (todoregistry synced).
- **GOLD #38–#41 this session**: tantrasara-a15 (7u), a21 (13u, incl. 2 Prakrit
  seal verses), a10 (18u kalādhvā), a16 (24u parokṣa-dīkṣā) — each: hand-crafted
  L0 (cm/l0cm-v1-N.json) → T1 md+jsonl+report → argmaps (fill_argmap) → L2 →
  C1 (essence=1 per unit) → L3 (reword to clear zero-shared) → L4 DRAFTs
  (craft+rejected+read-aloud) → data emit → gates → site ABSTENTION → STATUS →
  registry. All validate 0 / proof PASS / qa NEEDS_WITNESS / check CANONICAL.
- **gitarthasangraha slice 1/19 (gita-a00)**: 58 tok L0 with **5 LIVE forks**
  (mādhānyataḥ prime — neutral surface, 3 emend candidates recorded; Ingalls
  print-corruption grounds; Gita Supersite + Sharma 1983 = future collation/
  witness). Paratext excluded per paratext rule; ALIGN disposition in
  `tools/proof-disp.json`. Site ABSTENTION written.
- Site ABSTENTION skeletons now exist for a10/a12/a15/a16/gita-a00
  (**owner commits ipvv**).
- Site skeletons + proof dispositions follow the house patterns; prove PASS
  everywhere.

## The scale-out recipe (per remaining tantrasara ahnika: a11(25) a07(28)
## a14(29) a03(34) a05(43) a04(46) a09/a22(53) a20(65) a06(82) a08(93) a13(101))

1. Register in workcfg (kind=abhts, ahnika=N, songs tsa-aNN (1,units)).
   Count units via `parse_abhts` FIRST — batch-era STATUS "verses" counts lie.
2. Dump spans; hand-write `cm/l0cm-v1-N.json` = [lemma, morph, gloss] per SPAN
   token (ONE entry per whitespace token; fused-span rule: whatever the source
   joined, you join — verify with the length check loop; save only when ALL OK).
3. working-t1 (tokens from spans+cm; quick_english hand-written from source
   reading) → build_l0 → schemas validate → drift 0.
4. T1-<song>.md + .l0.jsonl + .report (PARSED/AMBIGUOUS/FAILED + tokens lines).
5. argmaps (content hand-written) → fill_argmap (fills l0_ids + sha, gates).
6. L2 (quick_english + pipe-exact cite + l0_ids + supplied[]) + C1 (essence
   one line per unit + 7 sections + rasa; 0 quotes, 0 shared sentences).
7. L3 handcrafted lines — REWORD vs L2 (joined L3 must not equal any L2
   sentence; short units are the trap — a16 had 7 collisions caught by gate).
8. L4 DRAFT per unit: craft_notes (sthāyin + rows + rejected + read-aloud) +
   reads_against + status machine-proposed; data/l4 == DRAFT['l4'].
9. data emit (t1+l0+argmap+l2+c1 unwrapped-dict+l3+l4) + c1/C1-<song>.md +
   site ABSTENTION skeleton (ipvv) + STATUS + REGISTRY gold-mark + todoregistry
   arithmetic + validate/proof/qa/check → commit (push only when asked).
10. Diacritic gate: ASCII 'Siva' in L4 = error → use Śiva everywhere (caught a21).

## Pitfalls logged this session (read before scaling)

- `git rm <prefix>*` aborts when new files share the prefix — exact names only.
- Byte-offsets ≠ char offsets in decoded strings (IAST) — slice BYTES, not str.
- `t1-qe.json` staged file got clobbered with CM data (file-drop instability
  from handover-E) — regenerate quick_english from lore, never trust a
  `cm/t1-qe` blindly; check its shape.
- argmap option_choices needs {l0_id, chosen_index, rejected[], reason} and
  option source ∈ controlled vocab (grammar, not manual).
- Cites must include '|' pāda separators as printed (proof real_fails strip
  only spaces).
- Gloss strings in working-t1 must NOT contain parens (breaks [and]-MD parse).
- proof-disp lives in `tools/proof-disp.json` keyed by song (check.py reads it).

## Open owner items (unchanged + new)

- First-verse L4 voice verdicts: a12, a15, a21, a10, a16, gita-a00 (all this
  session) + every prior gold's first verse still outstanding.
- Human review of every machine-proposed stack; stava/sivastotravali register
  (archaic vs contemporary) before any line-level re-craft there.
- paramarthasara normalization + sivastotravali conversion (assessed, need nod).
- Gita: continue a01→a18 (48-unit adhyāya 1 next); Sharma-1983 + Supersite
  collation for the 5 LIVE forks when vendored/available.
- Mystics: specs only (IMPORT.md), no pipeline until Kashmiri-gloss stage designed.
- C2 waived per owner (existing C2 stays).
