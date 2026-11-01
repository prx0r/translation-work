# ALIGNMENT — our data-object stack vs the original ipvv schemas vs sanskritbenchy

*2026-11-01. Answers: does ours align with `ipvv/specs/`? How does it differ? How does
sanskritbenchy support it? Read with `LAYERS.md` (the contract) and `AGENTS.md/User Directive 2026-11-01`.*

## 1. ipvv DAG vs our DAG

ipvv `specs/CANONICAL-DAG.yaml`: `SOURCE → T1 → L0 → ARGMAP(lateral) → L2 → L200 → C1 → THEME → …`

Ours (`LAYERS.md`): `SOURCE → T1 → L0 → ARGMAP → L2 → C1(essence+renders)`.

| Layer | ipvv spec | Ours | Verdict |
|---|---|---|---|
| SOURCE | `passage.json`: immutable cut, edition locator, verbatim Sanskrit | GRETIL slice, `source_sha` per song/verse | Aligns. Ours is addressable by (song, verse); ipvv by (work, chunk). Mapping: chunk ≈ song. |
| T1 | `t1.json`: MD **text** chunk, immutable, inline `[and]-gloss (iast)` grammar, frozen_hash | Data objects: verse draft + per-token quick gloss; MD is a rendered view | **Compatible extension.** Our objects render byte-identically to ipvv T1 text (`render_md.py` round-trip proves it). Immutability preserved (frozen MD untouched; JSON carries `source_sha`). |
| L0 | `l0_schema.json`: coordinates + `raw_fragment`/`lemma_iast`/`literal_gloss` (SINGLE gloss) + `status` | Same core + `options[]` (ranked, sourced, grounded), `chosen_index`, `morph`, `legacy_raw` | **Strict superset.** Every ipvv L0 record validates as our L0 with one option. The single-gloss field could not express forks — ours can. |
| ARGMAP | `argmap.json`: speaker/question/premises/inference (+conclusion, unresolved_terms) | Same + `traces{t1_verse, l0_ids}` + `structured` tier + `option_choices[]` | **Strict superset.** ipvv has no trace links and nowhere to record "the other gloss fits better" — `option_choices` is that place (decision + reason + rejected alternatives, consistency-checked against L0). |
| L2 | `l2.json`: text + `argmap_id` + `derived_from_l0` (id range) + `supplied[]` + `fidelity` | text + cite + `l0_ids` (exact ids, stronger than a range) + byte-exact cite check; `supplied`/`fidelity` optional | **Aligns with one backfill gap.** `supplied`/`fidelity` accepted but not yet populated (backfill TODO). The cite check is stricter than ipvv's. |
| L200 | `l200.json`: MT-vs-IA audit, `derivation_map` (L2 para → argmap → L0 → source), MT decision types | **Missing as a layer.** Partially covered: MT/GRAMMATICAL notes live in L0 `grounds`; IA assertions live in argmap uncertainties + C1 BOUNDARY; `derivation` accepted optionally in c1 objects | **Named deviation D1.** Consciously deferred: at verse granularity the argmap traces already are the derivation map. Revisit if C1 essence stops tracing cleanly to argmaps. `L200-sXX.md` legacy files remain the human-readable audit where present. |
| C1 | `c1.json`: single body 100–450w + fixed sections, requires `l200_id` | `essence[]` + `renders{standard + eli5/genz/poetic/formal…}`, standard == legacy 7-part essay preserved; `maps_to` enforcement on non-standard renders | **Extension on top of ipvv shape.** `renders.standard.sections` IS the ipvv C1 body. Deviation D2: no `l200_id` required (follows from D1); essence is currently mechanical-from-SUMMARY pending human review. |

## 2. sanskritbenchy in support (what we take, mapped to layers)

- **Gold-record pattern** (`lexical_decisions`, `grammatical_notes`, `flags`, `parallels` per T1 in
  `pipeline/gold_records/`) → adopted as L0 **option `grounds` + `source`** vocabulary. A fork with
  `source: lakshmanjoo/dyczkowski/ksemaraja-vivrti/grammar` and a grounds note is the benchy
  lexical-decision, per token instead of per passage. Exemplar: `s01-v21-p011` (anāma crux).
- **Renderer N-candidates + `candidate_disagreement`** → the fork *generator*: where renders diverge,
  mint L0 options. Cheap deterministic stand-in until model calls are wired.
- **MQM `candidate_a/candidate_b` pairwise format** → the shape of `option_choices`: adjudication
  between live alternatives with a recorded reason, exactly "oh the other literal gloss fits better."
- **Kendall tau protocol** → decides *which ranking signal* orders options (chrF-real vs semantic-judge
  vs proof-gate on the Trika slice). Runs after s06–s20; does not block translation.
- **Proof envelope** (`source_sha`, deterministic gate, lineage) → already inside `proof/proof-sXX.json`
  (B8 validates the data objects themselves).
- **Triangulation**: silent for all Śaiva texts (verified: MITRA sample is Buddhist Abhidharma).
  Adopted only as availability logging. Not built.
- Skipped, as before: confidence vector (7/11 unavailable), COMET (no torch), finetune builder, kanban.

## 3. Stale interpretations vanquished (2026-11-01)

- "One `[and]-` token per GRETIL whitespace token" (skeleton headers, old STATUS notes): superseded by
  pada-split + JSON-canonical (`LAYERS.md`). Skeleton headers rewritten to point at the contract.
- "MD is the artifact": superseded. JSON in `data/` is canonical; MD is a rendered view. Frozen T1 MDs
  are historical artifacts — left untouched, not edited.
- "L0 = single gloss": superseded by `options[]`. Single-gloss records remain valid (one option).
- "C1 = one essay": extended, not replaced. Standard render preserved; new renders require `maps_to`.
