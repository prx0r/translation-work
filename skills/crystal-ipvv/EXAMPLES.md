# SKILL EXAMPLES — prompts + good/bad per datatype, all from our own work

*Companion to `SKILL.md`. Every GOOD is verbatim from this repo (file + date given).
Every BAD is either verbatim from a defect we actually fixed (with the fix shown) or
marked [constructed] where no real instance exists. The point: show the model exactly
what passing looks like and exactly what failing looks like, in our own hand.*

*Loop for every layer: PROMPT the model → produce → VALIDATE with the schema tool →
fix what fails. A validator error is not an insult; it is the spec talking to you.*

---

## T1 — fast translation, lore-primed

**Prompt the model with:**
> Translate this verse quickly, then gloss every pada: one `[and]-gloss (iast)` token
> per pada (split compounds; stems split, inflection on the final stem). Speed over
> precision; face every pada. Mark genuine forks for L0 with a TODO, do not resolve
> them here. Convention: `LAYERS.md`. Never one-token-per-whitespace-token.

**GOOD** (`sivastotravali/T1-s01.md`, v6, post-fix):
```
[and]-of-endless-bliss (anantānanda) [and]-of-the-ocean (sindhoḥ)
[and]-in-dense (sāndra) [and]-bhakti-bliss-nectar (bhaktyānandarasā) [and]-drenched (āplutāḥ)
```
*Why good: token order follows the Sanskrit compound order (`anantānandasindhos`,
`sāndrabhaktyānandarasāplutāḥ`); citation forms; every pada faced.*

**BAD** (same verse, pre-fix — real defect caught by the concat-aligner):
```
[and]-of-the-ocean (sindhoḥ) [and]-of-endless-bliss (anantānanda)
[and]-drenched (āplutāḥ) [and]-in-dense (sāndra) [and]-bhakti-bliss-nectar (bhaktyānandarasā)
```
*Why bad: follows the English gloss order, not the Sanskrit order. Reversed compounds
read backwards. The aligner flagged ratio 0.827; hunk inspection showed pure order
inversion, no sandhi excuse. Fix: reorder to source order, never reorder to English.*

**BAD** (real m/ṃ typos, s03/s04 fixes): `(vedyam)` for source `vedyaṃ`;
`(subhagam)` for `subhagaṃ`; `(tava)` for source `te`.
*Why bad: anusvāra and enclitic errors change the morphology the whole stack stands on.
T1 is the floor — a wrong token here poisons L0, argmap, L2 silently.*

---

## L0 — scholarly audit, forks live here

**Prompt the model with:**
> For each token: surface, citation lemma, morphology (`m.nom.sg`,
> `3sg.pres.mid √gam`, `indecl.`). List EVERY genuine meaning-fork as an option with
> grammatical grounds and a source (`grammar` / `lakshmanjoo` / `dyczkowski` /
> `ksemaraja-vivrti` / `witness-*` / `t1-draft`), ranked. Max 5. Forked tokens must
> have analyzed morph — unknown morphology on a fork is rejected. Mark `fork: live`
> (undecided) or `resolved` (argmap will adjudicate). No sourceless options: a gloss
> without grounds is an invention, not a reading.

**GOOD** (`sivastotravali/data/s01.l0.json`, `s01-v21-p011`, the anāma crux):
`s01-v21-p011`, `surface: anāma`, `morph: indect. (a-naman, privative bahuvrihi)`,
`status: PARSED`, `fork: resolved`, two options — `nameless` (t1-draft, rank 1, with
grounds) and `of-no-account, infamous` (grammar, rank 2, with grounds citing the
`ko … gaṇyate` counting context), `chosen_index: 0`, plus `history[]`.
*Why good: the fork is explicit, both readings are grounded, morphology is stated,
the working choice is recorded with history, and the argmap adjudicates it
(`option_choices` with reason + rejected alternative). A future scholar sees the
whole decision, not just the winner.*

**BAD** (real validator rejection, s01-sug001 accept flow):
```
"fork:live|resolved requires analyzed morph (case/number/gender or tense/mood/voice+root)
— no unknown morphology on a fork"
```
*Why bad: the proposal added a live fork while `morph_unknown` was still true. The
system refused to let an unanalyzed token carry two readings. Fix was scholarship
(`pres.part.m.gen.sg √dhyai`), not paperwork.*

**BAD** (real validator rejection, groundless suggestion):
```
"suggestion: empty grounds (grammar/witness/reason — proposals without grounds are votes, not scholarship)"
```
*Why bad: `{"gloss":"whatever","source":"grammar"}` with no grounds. A source tag is
not grounds; grounds are the grammatical or witness reasoning a reviewer can check.*

---

## ARGMAP — terse logic + adjudication

**Prompt the model with:**
> Read the verse as a whole against Sanskrit + T1 + L0 + scholarship. Write terse
> logical statements: what is at issue, step-by-step with the Sanskrit verse cited,
> then inference. Where L0 offers a fork, adjudicate it on the record
> (`option_choices`: which gloss fits better + why + what was rejected). List open
> uncertainties honestly. End with the decision for L2. Verse-specific lore only.

**GOOD** (`sivastotravali/data/s01.argmap.json`, s01-v21: reconstruction + uncertainty
+ adjudication together):
reconstruction states the diving-the-ocean reading; `uncertainties` carries
"anāma crux: nameless (mystic) vs of-no-account (social)..."; `option_choices`
records `l0_id s01-v21-p011, chosen_index 0, rejected ["of-no-account, infamous"]`
with reason ("L2 keeps the mystic register ... crux left open per C1 boundary").
*Why good: sharp translation, honest fork, decision with reason — the three jobs of
an argmap in one object.*

**BAD** (mistakes.md #5 — boilerplate lore across passages):
*Why bad: a shared lore paragraph pasted across argmaps is a batch-smear signature;
it proves no verse was read. Checked mechanically (zero shared long sentences).
Each passage's lore must be verse-specific and distinct.*

**BAD** (argmap with no traces — validator):
*An argmap whose `t1_verse` does not exist or whose `l0_ids` point nowhere is
rejected. An argument that cannot point at its tokens is commentary, not reconstruction.*

---

## L2 — our translation proper

**Prompt the model with:**
> Render the verse in plain, readable English — the exact meaning we think, line by
> line. Every clause must trace to ≥1 L0 id (list them). Cite the Sanskrit byte-exact.
> No interpretive essays; nothing that belongs in C1. Log bracketed supplies in
> `supplied[]`.

**GOOD** (`sivastotravali/L2-s01.md`, v1):
> Of one who neither meditates nor chants, manifestation may come without any
> preparatory rule. Just so — O light of Śiva — we bow to him who possesses devotion.
*Why good: natural English, no gloss-words leaking through (`bhakti-possessing` would
be T1 leaking into L2), devotional voice carried, cite exact.*

**BAD** [constructed — no real instance; our L2s pass]: *"We bow to him, the
bhakti-possessing (bhaktiśālinam), without preparatory rule (avidhipūrvakam)."*
*Why bad: hyphen-glosses smuggled from T1; reads as a gloss string, not a line.
L2 dissolves gloss-talk into prose or it has failed.*

**BAD** (mistakes.md #3 — L2/C1 sharing sentences):
*Why bad: a sentence that could sit unchanged in either layer means the layers have
collapsed. C1 must be rewritten, not patched. Checked mechanically (zero shared
long sentences).*

---

## C1 — essence + standard essay

**Prompt the model with:**
> State the song's essence as atomic propositions. Then the 7-part essay (SUMMARY,
> FUNCTION, KEY TERMS, LOCAL CONTEXT, EXPLANATION, BOUNDARY, RELATED): the claim in
> sharp prose, the reasoning stated directly. Name what the verse DOES (rasa):
> consult `lore/rasa/`. Never quote English gloss-words. Never write about the text
> (no "the verse describes…", "this closes the arc"). Zero sentences shared with L2.

**GOOD** (`sivastotravali/c1/C1-s01.md`, SUMMARY — verbatim):
> The song establishes devotion without preparatory rule as valid, then proves it:
> since all beings desire the self and the self alone is consciousness, love directed
> at it stands on its own nature and needs no external ground. […]

**BAD** (real pre-fix lines, all four caught by the metacommentary gate):
- *"The song does not explain HOW opposites coincide…"* → fixed to *"HOW opposites
  coincide is unexplained — their coincidence is performed, not derived…"*
- *"The song does not explain WHY the placed behave like men…"* → *"WHY the placed
  behave like men … are held open as lived facts."*
- *"The song does not rank its 26 assignments…"* → *"The 26 assignments are
  unranked…"*
*Why bad: every one talks about the document instead of stating the matter. The fix
is always the same move: delete the song, keep the claim.*
*Also bad (mistakes.md #1):* `"therefore"`, `"I am"`, `"victory to Maheśa"` — quoted
gloss-words read as hedging. State the word directly, Sanskrit beside it, no quotes.

---

## C2 — prompt renders

**Prompt the model with** (`tools/render_c2.py --print-prompt` builds this; never hand-roll):
> [STYLE paragraph]. Use ONLY the ESSENCE list below; end EACH paragraph with essence
> tags like `[E0]` (every paragraph needs at least one tag, tags only from the list).
> [essence + L2 grounding + C1 SUMMARY follow]

**GOOD** (`s01.c2.json`, genz render — accepted, `maps_to` verified):
> …your tired, dusty mind? Water it with this and it fruits. `[E2]`
*Why good: voice changed, doctrine intact, every paragraph points at essence.*

**BAD** (real rejected ingest, style `negtest` — validator output verbatim):
```
"untagged paragraph (rejected): A paragraph with no tags at all.",
"out-of-range tags [99] in: Another one with a bogus tag."
```
*Why bad: untagged prose cannot prove what it renders; out-of-range tags point at
nothing. Output saved to `.draft`, never merged. Fail-closed.*

---

## Proof record + suggestion flow

**GOOD** (proof PASS): `deterministic_gate: PASS`, `blocking: []`, `needs:
["human-review"]`, cites 26/26 byte-exact, zero shared C1/L2 sentences.
**BAD-shaped (review, not failure)**: `qa_vs_witness` SHIP_WITH_NOTES — e.g.
`svabhāvasiddhā`, `samāveśa`, `vyutthāna` unattested in Lakshmanjoo. *Why listed:
unattested ≠ wrong (a witness may paraphrase), but it IS the review queue —
exactly the terms a human must check.*
**BAD-shaped (the classic)**: mistakes.md #4 — Bhairavastava L0 59/59 PARSED while
missing the first half of all 10 verses. *Why bad: parse rate certifies the tool,
never the coverage. Coverage is judged against the source (verse count + concat
alignment), i.e. proof gates B1–B3.*

**Suggestion flow GOOD** (`s01-sug001`, real history): proposed with grounds →
supported with a note → accepted with maintainer reason → L0 gained an option,
history written, argmap untouched (live fork, undecided).
**Suggestion flow BAD**: groundless proposal (rejected by validator, above);
merging without history (tool refuses — accept path writes it or fails).

---

## ipvv gold standard — why it's good (and its honest limit)

The `pipeline/gold_records/` objects (e.g. `tantra_text_kramasadbhava_1_8.json`)
are shaped right: **stages** (T1 with `close_translation` + `reader_draft` separated),
**flags** (`["X"]` marks the crux instead of smoothing it), **`lexical_decisions`**
and **`grammatical_notes`** slots (the decision has a home even when empty),
**`parallels`**, **`lineage`** (created_by, derived_from, supersedes), **`policy`**
(schema/contract versions), **`review_status`**. That shape is what our L0 options
+ grounds + history + signoff systematize at scale.
*Honest limit: the exemplar itself is thin — empty `lexical_decisions`, empty
`notes`, T1-stage only. The gold is in the schema discipline, not the content.
Our anāma record (2 grounded options + adjudication + history + signoff-pending)
is what a filled gold record looks like.*

## The 5,601 benchy exemplars — what they are, what they're good for

**What they are:** 5,552 mitrasamgraha (Gītā-based, Vedic/General tradition) +
373 Pratyabhijñā/Trika + 278 Śaiva Siddhānta + 123 Krama. Flat `{id, work, source,
gold, tradition}` — one gold per verse, no options, no grounds, no forks.
**Useful for:** (1) the Kendall protocol on the **Trika slice** — ranking metrics
against a judge on our own tradition's verses; (2) Gītā bulk as a negative control
and metric sanity check; (3) term-frequency background for glossary work.
**NOT useful for:** adjudicating a fork (whole-verse tau says nothing about which
gloss of one word is right); training our task (Gītā register ≠ stotra register,
single-gold format has nowhere to put a fork); any claim about Trika doctrine
(Gītā golds carry Vedāntic renderings — running term checks against them would
flag correct Trika readings). Use the slice, never the bulk, for anything load-bearing.
