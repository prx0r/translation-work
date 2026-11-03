# LAYERS — the translation stack (data objects, not MD files)

*2026-11-01, schemas v1.1.0. Supersedes the MD-only pipeline. MD remains as RENDERED VIEWS
for human review (`render_md.py` regenerates them; never hand-edit a rendered MD —
edit the JSON, re-render). Canonical manifest: `stack.json`. Executable gate: `check.py`.*

## Why the order is the order

Each layer looks at the previous layers for support. Nothing floats: every claim in a
higher layer must point at the lower-layer objects it stands on. The order is the
dependency chain, and the validators enforce it.

```
GRETIL source verse (sha-pinned)
  │  T1 looks at: SOURCE + seeded context (traditions lore, other good translations)
  ▼
  T1 — the fast translation: verse draft + per-token quick gloss over the whole text.
       Speed over precision; coverage is the point — every pāda faced before anything
       sharp is attempted. May be revised only by L0, with a flag.
  │  L0 looks at: SOURCE + T1 (chosen must equal T1 gloss unless revised+reason)
  ▼
  L0 — the scholarly audit: term-by-term literal gloss with every genuine meaning-fork
       as a ranked OPTION (options[]), each with grammatical grounds and a source
       (grammar / lakshmanjoo / dyczkowski / ksemaraja-vivrti / witness-* / t1-draft).
       Forks live HERE and nowhere else: fork none|live|resolved; AMBIGUOUS stays
       parse-quality (ipvv meaning). Morphology is stated on every forked token
       (m.nom.sg · 3sg.pres.mid √gam · indecl.; no morph_unknown on forks).
       Every change ever is appended to history[] ({gloss, reason, date}): the base
       is living, its past is immutable. Consensus: machine proposes, humans dispose
       (data/<song>.signoff.json); git holds every choice as a JSON diff.
  │  ARGMAP looks at: SOURCE + T1 + L0 + scholarship (lore search, papers, witnesses)
  ▼
  ARGMAP — what the verse says, as a whole: speaker, question, premises (terse logical
       statements), inference, payoff, uncertainties. Adjudicates L0 forks on the record
       (option_choices: which gloss fits better + why + what was rejected).
  │  L2 looks at: SOURCE + T1 + L0 + ARGMAP (traces required to all of them)
  ▼
  L2 — our translation proper: readable line-by-line plain English, the exact meaning
       we think, every clause tracing to L0 ids, Sanskrit cite byte-exact.
  │  C1 looks at: ALL lower levels (SOURCE + T1 + L0 + ARGMAP + L2)
  ▼
  C1 — the subtle essence: the sharpest poetic reading, evoking what the verse DOES
       (Abhinavagupta's rasa theory: the text aims at relish/camatkāra, so the essence
       names the relish, not just the doctrine). Song-level essence[] + the standard
       7-part essay, preserved. Renders of it live in C2.
  │  L3 looks at: SOURCE + T1 + L0 + ARGMAP + L2 + C1 (essence, rasa, notes, boundaries)
  ▼
  L3 — the final canonical translation: one translation to look at. Line-by-line evocative
       verse, every line traces to L0 + essence indices. No new doctrine, boundary items
       stay open with notes. Distills C1's essence into the single reading — the sharpest
       poetic reading as prose, then as verse. Machine-proposed until signed.
  │  C2 looks at: C1 essence + L3 (final text) + a PROMPT (+ frozen layers)
  ▼
  C2 — further renders (genz, eli5, poetic, formal, …): style + reproducing prompt +
       model/date + paragraphs mapped to essence. A new reading is just a prompt away;
       unmapped paragraphs are rejected. Infinite renderings, all grounded in L3+C1.
```

## Layer contracts (one line each, validators enforce the rest)

- **T1**: lore-primed fast pass; verse draft + quick gloss per token. Coverage guarantee.
- **L0**: auditable options with grounds + sources; `chosen == T1.quick_gloss` unless revised.
- **ARGMAP**: whole-verse argument as terse logical statements; fork adjudication with reasons.
- **L2**: plain-English exact meaning; clause→L0 traces; byte-exact cite.
- **C1**: essence (+ optional rasa note) + standard essay; refers to all lower levels.
- **L3**: final canonical translation; line-by-line evocative verse, every line
  traces to L0 + essence; no new claims, boundary items stay open with notes.
  Readability is the contract: plain words, commas and colons only — no dashes
  (`-`, `—`) and no slashes (`/`) anywhere in L3 lines. A transmission must read
  aloud cleanly; hyphenated compounds and slash-alternatives are T1 habits, not
  reading English. Rewrite, don't punctuate around. Everything in L3 is read
  aloud by TTS: plain ASCII only, no diacritics.
- **C2**: prompt + style + maps_to; reproducibility is the contract.

## Directory shape (per song, beside the legacy MD)

```
sivastotravali/
  data/s01.t1.json       # T1 objects (array, one per verse)
  data/s01.l0.json       # L0 objects (array, one per token)
  data/s01.argmap.json   # argmap objects (one per verse; scope verse|passage)
  data/s01.l2.json       # L2 objects (one per verse)
  data/s01.c1.json       # C1 object (essence + standard render)
  data/s01.l3.json       # L3 objects (one per verse; the single translation to read)
  data/s01.c2.json       # C2 renders (style + prompt + maps_to) — optional
  proof/proof-s01.json   # proof record (validates data objects when present)
```

## Living translation (how others join in)

The stack is append-mostly and every change is a JSON diff away:

- **Propose**: anyone runs `tools/propose.py` (new-option / choose-option / gloss-edit /
  l2-edit / essence-note / witness / morph-fix) with **grounds** — grammar, witness, or
  reason. Groundless proposals are rejected by the validator: votes are not scholarship.
- **Support**: readers add signed attestations (`--support ID --by NAME [--note]`).
  Weight follows reviewer trust; there is no auth infra, honesty over machinery.
- **Accept**: the maintainer merges (`--accept`), which writes `history[]` on the
  touched objects and, for gloss choices, the argmap `option_choices` record.
  Nothing enters canonical data except through accept. Rejects require reasons
  (closed PRs explain why); superseded suggestions stay on file.
- **Agree**: `data/<song>.signoff.json` (who, when, scope) marks human acceptance;
  the site carries by/date/scope. Git holds every step: proposal, supports,
  merge, signoff.
- **Upstream**: typos in GRETIL etc. go upstream (GRETIL contact, Ambuda proofing,
  SARIT fork/PR) — we record edition + line and never silently emend.
  Verified channels live in `lore/links.json`; witness text is never hosted.

## Invariants (validator-enforced)

1. L0.chosen == T1.quick_gloss for the token, unless L0.revised with reason.
2. fork live|resolved ⟺ ≥2 options; resolved ⟺ argmap option_choices entry with matching index.
   (AMBIGUOUS is parse quality, not fork state.)
3. Argmap traces resolve: t1_verse exists, every l0_id exists, sanskrit_sha matches source.
4. L2 lists ≥1 existing l0_id per verse.
5. C1 essence non-empty; standard render preserved with all 7 sections.
6. C2 renders: prompt non-empty; every paragraph maps to essence.
7. Verse/song coverage: T1+L0+argmap+L2 span exactly the GRETIL verse set, no more, no less.
8. L3 lines non-empty; every L3 lists ≥1 existing l0_id and ≥1 essence index.
