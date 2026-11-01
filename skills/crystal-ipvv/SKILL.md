# SKILL: crystal-ipvv — THE canonical translation process

*This is the ONLY process for Sanskrit translation in `/root/translation-work`.
No other drill, checklist, or pipeline doc authorizes work here. If another document
describes the layers differently, this skill plus `LAYERS.md` win (after the verbatim
User Directive 2026-11-01 in `AGENTS.md`). Per-datatype prompts with good/bad exhibits:
`EXAMPLES.md` (same folder — read it with this file). Standard: `crystal.md`; failure
log: `mistakes.md`.*

*This is the ONLY process for Sanskrit translation in `/root/translation-work`.
No other drill, checklist, or pipeline doc authorizes work here. If another document
describes the layers differently, this skill plus `LAYERS.md` win (after the verbatim
User Directive 2026-11-01 in `AGENTS.md`). Standard: `crystal.md`. Failure log:
`mistakes.md`. Contracts: `LAYERS.md`. Read all four before touching a work.*

*Why the order is the order: each layer looks at the previous layers for support.
T1 is covered first so coverage is settled; L0 audits every token so forks live in
exactly one place; argmap reads the whole verse against Sanskrit+T1+L0+scholarship
so adjudication is on the record; L2 renders the plain meaning so every clause
traces down; C1 names the essence so renders have something to point at; C2 is
prompts all the way down. Skip a layer and every layer above it is ungrounded.*

## The drill (one work, end to end, no batches)

1. **Pick ONE target** from `targets.md` queue. Never parallelize across works.
2. **Source first.** Locate the Sanskrit text (ipvv data, GRETIL, Muktabodha,
   SanskritDocuments). Read and master it before writing anything.
3. **Lore: ONE focused web search** on the specific work (editions, translations,
   scholarship) **plus the rasa file** (`lore/rasa/abhinavagupta-rasa-grounding-*.md`)
   whenever the work's C1 will need a `rasa{}` note. Verse-specific notes only.
   Rate limits are real — one search, then work.
4. **T1 (fast translation, lore-primed).** Seed context first (traditions lore, other
   good translations — step 3 feeds this), then quick verse drafts + pada-split
   `[and]-gloss (iast)` tokens over the whole text. Speed over precision; coverage is
   the point. Genuine forks are marked for L0 `options[]` with grounds — never smoothed.
   Then `python3 /root/ipvv/tools/t1_extract.py T1.md --out T1` (needs
   `translations/_stack/ipvv/l0/`). L0 must be 100% PARSED — necessary, never sufficient.
5. **Argmaps (one file per passage; verses as structured data).** Read the verse as a
   whole against Sanskrit + T1 + L0 + scholarship (lore search, papers, witnesses).
   Terse logical statements: what is at issue → step-by-step with the Sanskrit verse
   cited → adjudicate L0 forks on the record (`option_choices`: which gloss fits better
   + why + what was rejected) → unresolved (honest gaps only) → decision for L2. Lore
   line must be verse-specific; never copy-paste a block across passages.
6. **L2 (read prose) then L2.v2 (+ Sanskrit).** Our translation proper: readable
   line-by-line plain English, the exact meaning we think, every clause tracing to L0,
   cite byte-exact. No interpretive essays smuggled into L2; nothing that belongs in C1.
   Log bracketed supplies in `supplied[]` (ipvv L2 compat).
7. **C1 then C1.v2 (the essence, nothing else).** SUMMARY = the claim in sharp prose.
   EXPLANATION = the reasoning, stated directly. The essay must carry rasadhvani, not
   just paraphrase: name what the verse DOES (relish it aims at), using
   `lore/rasa/` — and where a dominant rasa can be honestly named, record it in the
   C1 object's `rasa{}` block (dominant, sthāyibhava, justification). Forbidden in C1,
   always: quoted English gloss-words; sentences *about* the text (full banned list
   under gate 8); any sentence shared with L2.
8. **C2 (prompt renders).** A new reading is just a prompt: `tools/render_c2.py --song
   sXX --style <name> --prompt "..."` (starters: `eli5`, `genz`). Model output must
   carry `[E#]` essence tags per paragraph; untagged output is rejected to `.draft`,
   never merged. Validate, then merge into `data/<song>.c2.json`. Withhold from site
   until essence is human-reviewed (T4).
9. **Run the gates, fix what fails, triage the living queue:**
   - L0: 100% parsed AND T1 covers the full source (verse count vs edition — parse rate cannot certify this).
   - Zero long sentences shared between C1 and L2.
   - Zero long sentences shared across the work's argmaps.
   - Zero `"` characters in any C1 file.
   - No metacommentary phrases (grep: `the (verse|hymn|stotra) (has|is|quotes|describes|opens|closes)`, `imagery does`, `grammar carries`, `closes the arc`, `quotes itself`).
   - Triage open suggestions: `tools/propose.py --song sXX --list --status open` — support, accept (writes history), or reject with reason. Never merge without grounds.
   - `python3 check.py` → CANONICAL, 0 failures (schemas, proofs, round-trips, site data, contract).
10. **Registry + STATUS.** Mark COMPLETE only as `machine-proposed, needs human review`. Never mark final. Never claim human review happened.

## Non-negotiables

- A C1 sentence that could sit unchanged in L2 is a failed C1 sentence. Rewrite it.
- A verse half missing from T1 invalidates everything downstream — re-derive from the fixed T1.
- Uncertainty is marked in place (obscure compounds, open antecedents, undecodable chronograms), never smoothed over and never invented around.
- A fork with no grounds is an invention. A render with no maps_to is drift. An answer with no trace is not an answer.
- Small, sharp, finished beats big, batchy, and approximate. If in doubt, shrink the scope, never the standard.
