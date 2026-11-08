# HANDOVER — 2026-11-08 — Tantraloka campaign: 6 promotions, free-only cycling, mass-retest wave

*Machine-proposed throughout. REGISTRY 101/85/16. Gates green, 0 failures.*

## TL;DR state

- **6 promotions this session (#80–#85):** a10 (310u), a04 (279u), a16 (311u),
  a29 (292u), a09 (314u), a13 (362u). Each: assemble → validate 0 errors →
  proof PASS (align 1.0; a13 0.975 from fused compounds) → `promote`.
- **Total hand-drafted: ~650 verse-layers** (gloss+cm+am) when beam-free was
  hard-429ing all session. Then free-model cycling was discovered and the
  strategy flipped to beam-first + assessor-review.
- **Free-only cycling LIVE:** beam-free (primary, calibration) → iceman-free
  (only other $0 model on the endpoint). Workers drafting on iceman now.
  The /go catalogue lists 30 models; everything else bills Go allowance —
  NEVER use them (one wrong turn into deepseek/mimo/glm/qwen/kimi/minimax
  was caught and reverted same-session; audit in model_usage.jsonl).
- **Mass-retest verdict: enriched packets convert old content-fails.**
  104 failed triples reset with full lore + legacy hints + neighbours +
  384k cap now pass first-try on free models. Remaining queue: ~1,700 tasks
  (gloss backlog + per-verse cm/am cascade + ~30 retests).

## How to continue (next agent)

1. **Monitor, don't hand-draft.** The loop is self-driving:
   `systemd tal-campaign` → `harness.sh` (health gate, staggered w1→w2→w3
   cap 3, sweep, try_assemble, gates) + `continue.sh`/`watchdog.sh`/`ralph`
   underneath. Check with `shastra.supervise` (MCP) or
   `tail process/beam/service.log` (harness log) + `tail process/beam/harness.log`.
2. **Review incoming drafts:** `shastra.swarm_review(task_id)` on each new
   DONE triple (assessor_sweep logs mechanical verdicts automatically; you
   read for MEANING). Bounce only with actionable notes; content-fails at
   max attempts go to the hand-draft backlog — but TRY A RETEST FIRST now.
3. **Retest protocol (new, proven):** clone the failed task with a fresh id
   (`<id>-retry1`), reset attempts, keep the enriched packet. 5/5 retests
   passed first try on 2026-11-08 (a30, a29×2, a04, a01). Only hand-draft
   what fails twice under the enriched packet.
4. **Assemble + promote per completed ahnika:**
   `shastra.assemble(work,song)` → `shastra.validate` (0 errors) →
   `shastra.promote` (refuses unless proof PASS) → `shastra.gates`.
   Never push; never mark final (all MACHINE-PROPOSED pending human review).
5. **Remaining order (shortest-first):** a28 (retests in flight, ~158 am to
   go) → a03 (10 triples in flight) → a01 (retests landing) → a08 → a15
   Everest (613u; retest vv1-24 queued as calibration probe; then windowed
   triples per §4 of RUNBOOK).
6. **LOOP.sh stays STOPped** (`process/beam/LOOP.STOP` exists) while an
   assessor drives — it duplicates review/assemble and overwrote hand-drafts
   twice. Remove the STOP file only when stepping away.

## Traps & fixes banked this session

- **Model choice is a billing choice, not a quality choice.** /go endpoint
  models are Go-allowance billed EXCEPT beam-free + iceman-contributor-free
  (crouton-alpha-free exists but is region-blocked here: RegionError).
  Verify $0 status via GET /models `limit` + a live PONG before trusting any
  new model name.
- **Enriched packet beats raw retries.** Old failures (thin packet: bare
  tokens, 6k budget, no lore) pass with: full transmission brief + legacy
  per-token hints + 2 neighbouring verses each side + 384k cap. The single
  biggest quality lever in the whole harness.
- **Surface drift has 3 distinct causes — diagnose before re-queueing:**
  (a) beam splits fused sandhi → fixed by explicit no-split + @-mark
  explanation in prompt; (b) avagraha variants (', ', U+02BC) →
  `norm_surface()` comparison in beam_swarm.py; (c) GRETIL editorial parens
  `śiva(śakti)rūpaiva` → fuse to reading + `deparen()` in proof_record.py +
  `is_paratext` narrowing in shastra_merge.py (affects ONLY a10: verified
  no other work has mid-token parens). Grammar-term leakage and thin
  questions/premises are CONTENT fails → bounce once with the specific fix,
  then hand-draft if it fails again.
- **Queue vs runs coherence:** workers overwrite runs/ files on redo;
  hand-drafts get overwritten too. Rule: hand-draft ONLY verses with no
  pending/claimed triple task. Before seeding, check coverage with
  review_inbox.py; after hand-drafting, mark overlapping queued tasks done
  (see 2026-11-08 reconciliation: 147 stale). Validate with
  `tools/handdraft.py` (enforces byte-exact surfaces + shape gates).
- **Duplicate supervisors kill throughput.** Exactly ONE: systemd unit →
  harness.sh. Kill strays by exact PID, never pkill patterns (it hangs in
  this environment). `supervise(start_missing=true)` now targets the unit.
- **Assemble needs complete runs** (gloss+cm+am per verse) — it does NOT
  wait; incomplete → `INCOMPLETE/BLOCKED, assessor needed`. The per-verse
  fallback (seeded via tal_stage --seed) covers what triples miss.
- **L3/L4/C2 are waived** by owner directive (minimal gold = T1/L0/argmap/
  L2/C1-essence + proof PASS). 19 ahnikas already carry L3/L4 from earlier
  work; do not retrofit the rest unless the owner reverses this.

## Quality bar (unchanged from Tantrasara gold, minus waived layers)

- T1 span-exact, L0 100% PARSED (stem-level morph preferred; thin grounds
  flagged not failed), argmaps with verse-owned questions (≥5 words, never
  "what does verse N state"), premises ≥3 words, honest uncertainties
  (generic "compound boundaries" tolerated but weak — push for specifics),
  L2 ≥4 words cited byte-exact.
- C1 essences on minimal golds are DERIVED placeholders ("The verse
  states...") — the acknowledged gap. Full 7-part+rasa upgrade is a
  separate project; do not confuse minimal gold with full gold.

## Files & entry points

- Queue/pipeline: `tools/beam_swarm.py` (workers), `tools/tal_stage.py`
  (seed/assemble), `tools/beam_client.py` (free-only cycling + audit).
- Review: `tools/review_inbox.py coverage|verse|next|newest <work> [v]`.
- Hand-draft: `tools/handdraft.py` (validates; never bypass it by hand-writing JSON).
- State: `process/beam/queue.json` (live), `model_usage.jsonl` (audit),
  `model_health.json` (per-model 429 cooldowns), `process/beam/LOOP.STOP`
  (remove to resume autonomous LOOP agent).
- Registry: REGISTRY.json + todoregistry.md (this file's addenda are the
  running log; update per promotion).
