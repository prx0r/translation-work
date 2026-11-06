# RUNBOOK — running the translation machine, end to end

*Operator manual. The law lives in `skills/largetext/SKILL.md` (+`EXAMPLES.md`);
process notes in `BEAM-FLOW.md`; contracts in `DB-BACKBONE.md`,
`FORMAL-ALIGN.md`, `REGISTRY-FEDERATION.md`. This file is the hands-on-keyboard
order of operations. If it conflicts with the skill, the skill wins.*

## 0. Map of the machine

```
openpatala box DB ──dbread.py──▶ PLAN (registry_sync) ──seed──▶ queue.json
                                                              │
beam workers (nohup, beam-free, $0) ◀── ralph.sh supervises ──┤
  │ drafts prose/JSON shapes only          auto-review (windows ONLY)
  ▼                                        convert approved pilots
process/beam/runs/ ──assessor review──▶ approve | bounce ──▶ converters
  │                                        │         │
  │                              ipvv/pilot/      retry w/ note
  ▼
validate_song → proof_record → validate_all → MANIFEST → check.py → commit+push
LEDGER.jsonl logs everything · checkpoints chain it · mistakes.md learns from it
```

Roles: DUMB (beam) drafts, validators judge shape, assessor (you, batched)
judges meaning, ralph loops. Nothing canonical without the assessor; nothing
ships red.

## 1. Fresh box bring-up (from zero to running, ~30 min)

```bash
# 1. repos
for r in translation-work trika-x svread; do git clone --depth 1 https://github.com/prx0r/$r.git; done
# 2. keys (vault holds live creds; files on disk are stale by design)
agent-vault vault credential get OPENCODE_GO_KEY --vault oracle   # Go API (beam)
agent-vault vault credential get CLOUDFLARE_R2_S3_ACCESS_KEY --vault oracle
export OPENCODE_GO_KEY="$(agent-vault vault credential get OPENCODE_GO_KEY --vault oracle)"
# 3. portable DB (verify sha against manifest first)
aws --endpoint-url "$R2_ENDPOINT" s3 cp s3://patala/openpatala/box-2026-11-06/openpatala-box-2026-11-06.dump /tmp/
sha256sum openpatala-box-2026-11-06.dump   # must be 57d54032…
su postgres -c "createdb openpatala_box && pg_restore --no-owner -d openpatala_box <dump>"
su postgres -c "psql -d openpatala_box -tAc 'SELECT count(*) FROM works;'"  # 544
# 4. sanity
cd translation-work && python3 check.py        # CANONICAL, 0 failures
python3 tools/dbread.py coverage ipvv         # 49/49
python3 tools/validate_all.py --quick         # 0 failures
```

## 2. The button (normal operation)

```bash
# supervised single pass (review output, then decide):
bash tools/continue.sh once
# leave it running (supervises ralph + reseeds from registry):
setsid nohup bash tools/continue.sh > process/beam/continue.log 2>&1 < /dev/null &
```

`continue.sh once` does, in order: registry sync → seed swarm → ensure
workers → auto-review → convert due pilots → gate → commit+push → report.
Loop mode repeats this plus restarts ralph if dead. Watch it with:

```bash
tail -n 30 process/beam/continue.log   # supervisor
tail -n 30 process/beam/ralph.log      # work loop passes
python3 tools/beam_swarm.py status     # queue by state
python3 tools/beam_ledger.py tail 40   # what actually happened, latest first
```

## 3. Lanes (what runs right now, and how each finishes)

| lane | state | next machine step | assessor step |
|---|---|---|---|
| IPVV T1/L0 | 49/49 done, 48/49 PASS | V2-N char-offset coverage fill | review V2-N, sign off |
| IPVV argmap/L2/C1 | 48/49 converted+PASS | bounce redrafts for V3B-class gaps | rewrite flabby questions, compress premises, adjudicate forks |
| TAL briefs | 100+ window briefs approved | workers drain remainder | spot-read HOLD sample |
| TAL transform (a23 first) | T1 parsed (103v), lore briefed | tal_gloss → tal_cm → argmap drafts | write/adjudicate argmaps+L2+C1+L3/L4, emit_tal, proof |
| Gita endgame | recon approved w/ correction | workcfg intake registration | a01 48-unit pilot, then per-adhyāya pipeline |
| Factories/socials | spec only (REGISTRY-FEDERATION) | seed unit/book/draft queues on owner nod | lane-owner review |

Shortest-first within each lane. Mystics + tattvasandoha stay deferred (owner).

## 4. Task kinds (packet in, artifact out, gate that decides)

| kind | needs | produces | auto-gate | human gate |
|---|---|---|---|---|
| `recon` | source path | `runs/<id>/recon.json` + raw | schema + markers sane | verify vs known structure |
| `lore_queries` | topic + context | `queries.json` | schema (2–6 queries) | execute searches (assessor) |
| `lore_distill` | excerpts (≥200 chars) | `LORE_BRIEF.md` + json | schema | rewrite/approve into `process/beam/lore/` |
| `tal_brief` (window ≤60v) | GRETIL spans + legacy L2 + lore | `brief.json` + raw | schema + ≥90% coverage + anti-uniformity | spot-read sample; full briefs always held |
| `pilot_pair` | T1.md + L0 glosses + lore | 2 prose files + selfcheck | markers + lengths | full prose review, then approve→pilot/ |
| `tal_gloss` | verse tokens + L1/L2 prose | per-token glosses | count+format match | spot-read samples |
| `tal_cm` | tokens + glosses | CM rows | count + non-empty morph | morph audit sample |

New kinds: add runner + pydantic models + gate in `beam_swarm.py`, calibrate
against gold BEFORE scaling (skill §4), document here.

## 5. Transmission briefs (the quality lever)

Beam without scholarship produces geometry. Before queueing any front:

1. `lore_queries` task (or write queries by hand) → assessor runs 1-2 web
   searches → paste excerpts → `lore_distill` (or write `process/beam/lore/<front>.md`
   directly — faster and better).
2. Brief shape: what the text IS → numbered moves → traps (lookalikes,
   nearby-but-different targets, print damage) → approach rules.
3. Packets auto-inject matching briefs (`tal-<ahn>.md`, `ipvv-<LBL>.md`).
   No brief = expect a bounce cycle; write the brief.

## 6. Review batches (assessor, ~15 min per batch)

```bash
python3 tools/beam_swarm.py status                        # what's done/held/failed
python3 tools/beam_swarm.py review <id>                   # read draft + selfcheck
python3 tools/beam_swarm.py approve <id>                  # pilots/prose you endorse
python3 tools/beam_swarm.py bounce <id> "fix X concretely" # worker retries with note
python3 tools/beam_ledger.py errors                       # what failed, why, next action
```

Sampling rule: every 5th window brief auto-HOLDs for spot-read (hash-gated,
not discretionary). Pilot prose is NEVER auto-approved. Bounce notes must
name the defect and the fix ("partition vv40-60 by topic; current spans are
uniform 8s"). Vague bounces waste cycles.

## 7. Monitoring (is it healthy?)

- `beam_swarm.py status` — pending should drain; `failed` should only be
  tombstones (documented) or carry a next action.
- `beam_ledger.py tail/errors/task` — the audit trail (append-only,
  hash-chained; `checkpoint` writes merkle roots to `ledger-checkpoints.jsonl`).
- Worker logs `process/beam/wN.log` — last lines show current task; silent
  + claimed tasks = check the worker is alive (`pgrep -f beam_swarm`).
- `ralph.log` / `continue.log` — pass summaries, commits, parks.
- Red flags: same task failing 3× (prompt bug, not worker bug — fix the
  packet/template); `manifest-fresh` failing after clean runs (regen, don't
  waive); queue growing while workers idle (stale claims — they expire in
  15 min; if stuck, clear `process/beam/claims/`).

## 8. Failure playbook (seen before — do this, not something clever)

| symptom | cause (seen) | fix |
|---|---|---|
| `finish=length` + null content | reasoning budget eaten | `reasoning_effort: low` + large `max_tokens` (in client already) |
| uniform 8-block spans | unbriefed / too-large window | write lore brief; split to ≤60-verse windows |
| `vA`-style span rejects | validator strictness | normalize, don't punish (already in gate) |
| `unknown kind` failures | workers on old code | restart workers after every tool edit |
| queue stuck `claimed`, no workers | dead shell killed them | claims expire in 15 min; or clear `claims/` |
| `manifest-fresh` red after good run | content changed (normal) | `manifest.py gen` (ralph does this pre-gate) |
| `deambig`-style mass promotion urge | — | FORBIDDEN. Vote-counting launders error (mistakes #20). |
| beam invents identifiers/URLs | confabulation | reject the draft, never patch the ID in |

## 9. Recovery (box died / repo cloned fresh / swarm wedged)

1. Re-run §1 bring-up. 2. `init-queue` + reseed from PLAN (`registry_sync --seed`).
   Workers pick up pending tasks; `done` reruns are idempotent (outputs rewritten,
   never duplicated — claim files gate this). 3. Ledger replays history; checkpoints
   verify it (`beam_ledger.py checkpoint` after recovery, compare roots).
4. If queue.json is corrupt: restore from git (live state excluded from commits —
   only *approved* work is committed; re-queue the rest via `registry_sync --seed`).

## 10. Conventions (violations are defects, not shortcuts)

- Beam NEVER writes `data/`, `ipvv/pilot/`, proofs, signoffs, pushes, ISBNs,
  witness claims, or final marks. Assessor promotion only, via converter +
  validators + review.
- Everything beam touches is labeled machine-proposed until human review.
- AMBIGUOUS is a terminal state for genuine uncertainty (SHASTRA-MINIMAL §1);
  promoting it requires evidence, never votes.
- Lane rules: no writes to other repos; no auto-publish/spend/send (influence);
  no production cutovers (videofactory parity); no invented identifiers.
- Log every consequential step (`beam_ledger.py log`); curate learnings into
  mistakes.md + the skill (that file is the lab notebook, not a trophy shelf).

## 11. TAL campaign (autonomous minimal-gold) — how it runs

```bash
setsid nohup bash tools/tal_run_all.sh > process/beam/tal_campaign.log 2>&1 < /dev/null &
```

Per ahnika, `tools/tal_stage.py` runs: parse legacy T1 → seed **tal_triple**
tasks (12 verses per call: gloss+CM+argmap+L2 in one pass, one session per
ahnika for prompt-cache reuse, adaptive split on output-ceiling failures) →
wait (workers must be alive) → assemble working-t1/l0/argmap/l2 + data/*.json
→ `validate_song` → `proof_record --shastra` → STATUS/REGISTRY → manifest →
commit+push. Order is shortest-first; proof BLOCKED parks that ahnika and
moves on (never forced).

Task kinds per verse: `tal_gloss` (per-token gloss+grounds), `tal_cm`
(lemma/morph/grounds), `tal_am` (question/premises/inference/uncertainties/L2).
Gates: surfaces must equal the token list exactly; proper-noun capitals are
allowed (gold TAL glosses carry Kanyā, Bhagavan, Śrīkaṇṭha); compounds may run
to 15 hyphen-parts (gold max); no grammar-term leakage (genitive/nominative/
…/sandhi/compound) — use plain English instead; question is the verse's own
question, ≥5 words, never "what does verse N state".

Assessor residue (by design): hand-write verses the gates reject after
retries; spot-read PASS results; write/approve C1 essence (the driver derives
a provisional essence from argmap inferences when absent — flagged
"assessor review outstanding").

State: `tal-<ahnika>/data/*.json`, `STATUS.json`, `proof/`, REGISTRY entry.
Campaign log: `process/beam/tal_campaign.log`.

## 12. Model: beam-free, hardcoded

`tools/beam_client.py` pins `MODEL = 'beam-free'` — deliberately, with no env
override. Other models fail in this harness (owner directive 2026-11-06).
If the free tier is unavailable, the correct response is to pause the swarm
and queue work for the assessor, never to swap the model.

**Maximise context, minimise calls.** beam-free has a 1M context window, so
the campaign batches 12 verses per call (gloss+CM+argmap+L2 in one pass) and
keeps ONE session id per ahnika (`tal-triple-<song>`) so prompt cache and
accumulated understanding persist across calls. On output-ceiling failures
the runner halves the group and recurses — adaptive batching, no manual
tuning. Measured effect: ~12× fewer requests than per-verse stages.
