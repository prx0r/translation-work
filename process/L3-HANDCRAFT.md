# L3 HANDCRAFT — how the final translation gets made

*2026-11-02. The method used on Bhairavastava (10/10), then applied work by work.
L3 is the single translation to look at: line-by-line, evocative, final. It
incorporates everything below it and invents nothing above it.*

## What L3 is (and is not)

- L3 renders the verse — never talks about it. No metacommentary ("the verse
  says/closes"), no essay headers, no rasa labels, no trailers. (Bars 2, 8.)
- L3 is NOT L2 polished. L2 is plain exact prose; L3 is the beautiful
  transmission: same claims, carried in rhythm and diction. Zero shared
  obligation to L2's sentences — but zero new doctrine either.
- L3 is NOT C1 condensed. C1 states what the verse does; L3 does it.
- Every line traces to L0 ids + C1 essence indices (schema-enforced). A line
  that floats is rejected, however beautiful.

## The pass order (one work, end to end, manually)

1. **Read everything for the verse**: SA aloud (pada breaks) → T1 glosses →
   L0 chosen (note revised/forked tokens) → argmap premises + uncertainties →
   L2 → C1 SUMMARY + rasa + NOTE (KEY TERMS, EXPLANATION, BOUNDARY).
2. **Fix the line shape first**: hemistich couplets (2 lines). Line 1 opens,
   line 2 lands. Em-dash joins related clauses; colons before catalogues.
3. **Give every line a spine**: each line needs a finite verb or a justified
   fragment. Dangling participles ("and made of You, all is mine") get
   re-anchored ("made of You, all is mine" as absolute — or rewritten).
   Stacked appositions ("consciousness itself, one, without end") get an
   explicit predicate ("consciousness itself *is* one — without end or
   beginning").
4. **Kill the small defects**: possessive typos (awareness' → awareness's);
   repeated words across the couplet (won/win → won/obtain); split
   superlatives ("most wrathful, terrible" → "most wrathful and terrible");
   cognate echoes (streams/stream → pours/stream); leading conjunctions
   after semicolons ("; and never" → ": never").
5. **Check coverage against L0**: every L0 token's content must surface
   somewhere in the couplet. Dropped stems (śaraṇya, tena, maru, pūrṇa)
   are restored; untranslatable residues (colophon dates, vocatives kept
   as names) are kept honestly, not smoothed.
6. **Honor BOUNDARY items**: where the NOTE marks unresolved (svātmamaya
   constitutive-vs-identity, samayajña vocative-vs-qualifier, eka 'one' vs
   'alone'), pick the reading the couplet needs and record the fork in the
   L3 `notes` field. Never present a guess as fact (Bar 6).
7. **Variants**: where the printed SA disagrees with L0/NOTE consensus
   (bhavati vs bhavamaru), translate the coherent reading, mark
   `fidelity: not-resolved`, record the variant. SA itself is never
   silently emended — that decision belongs to the owner + Sanskritist.
8. **Validate mechanically**: schemas/l3.py (lines non-empty, l0_ids exist,
   essence indices in range) + svread checker S13 (no headers/trailers,
   no BLOCKED, no commentary smell, couplet convention). Then read the
   finished couplets aloud — the ear catches what the gates miss.

## What stays out (translation, not commentary)

- Added sentences with no SA/L0 counterpart (the p03/p08 L2 failure mode).
- Ungrounded possessives ("my darkness" with no mama-genitive).
- Interpretive closures of open questions (samaya = "covenant" is allowed
  in L0-gloss position only where the lane already commits; L3 states the
  chosen reading + notes the fork).
- Rasa theory ABOUT the verse. Rasa must be IN the diction (Bar 9):
  "trickles" vs "pours" vs "streams" is a rasa decision with a reason
  tied to the sthāyibhāva — record the reason in notes when non-obvious.

## Provenance

- L3 drafts are machine-proposed, needs human-review — same as every layer.
- Site-lane hand fixes are preserved by the emitter guard; T1/L0 fixes
  that need re-tokenization belong to the crystal pipeline (documented
  per-verse in L3 notes + audit flags, never hand-forced).
