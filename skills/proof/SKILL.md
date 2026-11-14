# SKILL: proof — what a translation proof is, how it's computed, why to trust it

*Read this before citing any `proof-*.json` gate, or before asking ChatGPT
(or anyone) to trust one. The code is `tools/proof_record.py`
(`TOOL_VERSION = "proof_record v1 2026-11-01"`, stdlib only, no models);
schemas in `schemas/`; cross-layer checks in `tools/validate_song.py`.
Companion: `PROVE-EXPOSE.md` (the publish pipeline this gate guards).*

## 1. What a proof IS (one paragraph)

A `proof-<song>.json` file is a **machine-checkable verdict that one song's
translation layers are internally consistent, complete against the source,
and honestly labeled**. Its core field is `deterministic_gate`:

- `PASS` — `blocking` is empty. Every check below held.
- `BLOCKED` — `blocking` lists named failures (`ALIGN_NODISP v967
  ratio=0.848`, `L2_CITE_FAIL 2`, …). A BLOCKED song must not be served
  as verified; `needs[]` names the repair for each failure.

**PASS does not mean "the Sanskrit scholarship is correct."** It means the
mechanical contract holds. Meaning is judged separately: beam drafts prose,
deterministic scripts assemble, validators judge *shape*, the assessor judges
*meaning*, a human disposes. No single writer can mint PASS — that
separation is the whole trust model (see §5).

## 2. How it is computed (the checks, in order)

Input: the song's canonical JSON (`data/<song>.t1|l0|argmap|l2|c1.json`),
the byte-pinned source spans, and optionally `tools/proof-disp.json`
(recorded per-verse dispositions — §3).

1. **Verse census.** T1 verse set must equal the source span set, exactly.
   Missing or extra verses block (`VERSE_COUNT`, `MISSING_VERSES`). A
   translation that skips verses can never pass.
2. **B1 — L0 parse.** Every term token must be `PARSED` (`FAILED` count must
   be 0). Unparsed morphology blocks.
3. **B3 — concat-align, per verse.** T1 surfaces are concatenated and compared
   (difflib ratio) against the source span tokens, after cleaning: dandas
   stripped, parens removed, pure-apparatus tokens dropped (page marks,
   sigla, refs — never glossed, never counted). Ratio must be ≥ 0.90 per
   verse, else `ALIGN_NODISP vNN ratio=0.xxx` blocks — unless a disposition
   is recorded for that verse (see §3).
4. **B4/B5/B6 + quotes + metacommentary.** C1 essence vs L2 read-prose must
   share **zero** sentences ≥ 8 words (`C1_L2_SHARED`); C1 must contain zero
   `"` characters (`C1_QUOTES` — gloss-words are hedging, not claims); C1
   must match none of the document-talk patterns (`C1_METACOMMENTARY`:
   "the verse describes…", "the grammar does…", etc. — C1 states the
   matter, never the document). C1 over 700 words is a warning.
5. **B7 — L2 cites are byte-exact.** Every Sanskrit citation in L2 must occur
   verbatim in the source span (after the same apparatus cleaning).
   Failures are listed verbatim (`L2_CITE_FAIL n`). A translation that cites
   words the source does not contain can never pass.
6. **B8 — canonical data objects validate.** `validate_song.py` enforces the
   schemas plus cross-layer invariants, including: `L0.chosen ==
   T1.quick_gloss` (unless revised with reason); T1+L0+argmap+L2 span
   *exactly* the source verse set; every argmap trace resolves
   (`t1_verse` exists, every `l0_id` exists); every L2 verse cites ≥1
   existing `l0_id`; C1 essence non-empty; every C2 paragraph maps to an
   essence index; L4 traces must be a subset of its L3's (music never adds
   doctrine). Any violation blocks (`DATA_OBJECTS n …`).
7. **`needs[]`, `layer_sha256`, `lineage`.** Every block maps to a named
   repair (`fix: word-order/gloss vs source for v967`); a PASS record needs
   only `["human-review"]`. Each layer's canonical hash is recorded, so any
   later edit is detectable. `lineage` pins the tool version, the source
   sha256, and the exact files. On PASS the tool writes its decision-trail
   row — and **refuses to exit 0 if that write fails** (a proof without its
   receipt is incomplete state). Exit codes: 0 = PASS, 1 = BLOCKED,
   2 = infrastructure failure (never a judgment).

## 3. Dispositions: the honest-exception mechanism

Some sub-0.90 alignments are genuine sandhi (T1 writes citation forms,
the witness joins them: `-aḥ`→`-o`, `iti`+`eṣa`→`ityeṣa`, visarga→ś before
palatals). Those are recorded per verse in `tools/proof-disp.json` with the
*grounds named* (`"sandhi-only: devaḥ+ca→devaśca (visarga→ś …);
assessor-verified <date>"`). Rules, enforced by tooling and process:

- A disposition excuses exactly one verse's number, never a pattern.
- Since 2026-11-14, keys are work-qualified (`"mukta-m00013:mukta-m0-p02"`);
  bare song names are legacy fallback only — because names like
  `mukta-m0-p01` exist in several works, and a bare key could otherwise
  suppress a genuinely different verse in another work. A migration script
  re-verified every entry in its owning work before re-keying it.
- A disposition is an assessor act with stated grounds, or it does not exist.
  Forks without grounds are inventions; agreement is not evidence (§5).

## 4. How to verify one yourself (no trust required)

Everything needed ships with the repo: `python3 tools/proof_record.py
--song S --work W --shastra [--disp tools/proof-disp.json]` recomputes the
verdict from current bytes — same inputs, same verdict, no models, no
network. For published works, `svread/data/verify/<work>-<target>/`
packs carry the exact hashed bytes: `curl -s <url> | sha256sum` must equal
the recorded hash, or the pack is rejected (emitters abort the whole publish
rather than ship one bad pack). Spot-check any verse by hand: concatenate
the T1 surfaces, strip apparatus, and compare against the source span.

## 5. Why ChatGPT should trust it — and exactly how far

Trustworthy parts (mechanical, re-runnable by anyone):

- **Deterministic.** No LLMs, no network, stdlib only. Re-running gives the
  identical verdict or exposes drift.
- **Fail-closed.** Anything unchecked blocks. Unknown states get names
  (`needs[]`, `warnings`, `stale-pass`), never silent passes. Exit code 2
  on infrastructure failure is distinct from gate failure.
- **Separation of powers.** The drafter (beam, free model) cannot write
  canonical files; the assembler (scripts) cannot author; the validators
  cannot judge meaning; the assessor cannot mint PASS without the gates;
  nothing ships red. No single component can launder an error end to end.
- **Battle-tested against real laundering.** The gates exist because each
  was once bypassed: dropped repetitions (Kularnava kul-p39, caught at
  0.848, repaired, re-proofed to 1.0); reversed word order; vote-counted
  promotions (3,044 rows reverted — agreement is not evidence); lax
  auto-promotion; gloss-words smuggled in quotes (banned outright).

Limits, stated plainly (do not over-claim):

- PASS certifies the *contract*, not scholarly correctness. A fluent, fully
  traced, perfectly aligned translation can still misread the philosophy —
  that judgment lives with the assessor and the human reviewer, never in
  this file.
- Sandhi-variant spellings need human-judged dispositions (§3). The audit
  tooling proposes; the assessor disposes. A disposition is a signed claim
  with grounds, auditable in git history.
- Witnesses are UNPINNED corpus-wide (no collation claims are made).
- Everything is machine-proposed until a human signs. `needs:
  ["human-review"]` on a PASS record is not decoration — it is the
  remaining step.

Operational meaning of trust: cite the proof file (gate + layer hashes +
source sha), never the prose alone; re-verify on read (it is cheap);
treat BLOCKED as do-not-serve and `needs[]` as the repair queue.

## 6. Worked example (60 seconds)

Kularnavatantra kul-p39 v967: T1 read "yatra mano yāti tatra samādhayaḥ"
(5 tokens); the source reads "yatra yatra mano yāti tatra tatra
samādhayaḥ" (7 — emphatic doubling). Proof: `ALIGN_NODISP v967
ratio=0.848`, BLOCKED. Repair (assessor): restore the two dropped tokens to
T1+L0 with history notes, renumber positions, re-run proof → `PASS`,
ratio 1.0. Nothing was smoothed, nothing renamed; the diff is in git.

## 7. Pointers

Code: `tools/proof_record.py`, `tools/validate_song.py`, `schemas/`,
`tools/audit_align.py` (batch ALIGN_NODISP triage), `tools/repair_disp_keys.py`
(key hygiene), `tools/proof-disp.json` (recorded dispositions, work-qualified).
Process: `PROVE-EXPOSE.md` (the publish pipeline this gate guards),
`BEAM-FLOW.md` / `skills/largetext/SKILL.md` (who does what),
`skills/crystal-ipvv/SKILL.md` (the translation law).
