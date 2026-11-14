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

## 12. Models: beam-free first, free-tier cycling (owner-authorized 2026-11-08)

`tools/beam_client.py` keeps `beam-free` FIRST (all benchmarks were cut
against it — calibration continuity), then fails over across verified-free
Go models: `deepseek-v4.1-flash` (384k out) → `mimo-v2.6-flash` →
`glm-5.3-flash` → `qwen3.8-flash` → `kimi-k3` → `minimax-m3.1-flash`
(512k out). This supersedes the 2026-11-06 beam-free-only hardening, by
explicit owner order, after live verification that every fallback returns
HTTP 200 + well-formed JSON on this box while beam-free 429s.

Mechanics: a model that 429s is parked 30 min in
`process/beam/model_health.json` (shared, so all workers agree) and the
call fails over immediately — no more 12-minute sleeps per call. Every
served call is appended to `process/beam/model_usage.jsonl`
{ts, session, model} for per-model calibration audit. Untested models are
NOT trusted for meaning: pydantic gates + assessor review apply equally.

**Maximise context, minimise calls.** beam-free has a 1M context window, so
the campaign batches 12 verses per call (gloss+CM+argmap+L2 in one pass) and
keeps ONE session id per ahnika (`tal-triple-<song>`) so prompt cache and
accumulated understanding persist across calls. On output-ceiling failures
the runner halves the group and recurses — adaptive batching, no manual
tuning. Measured effect: ~12× fewer requests than per-verse stages.

## 13. Beam-free hard limits (probed 2026-11-06)

`GET /inference/go/openai/v1/models` → beam-free: **context 1,048,576**,
**output 131,072**. The client uses the output ceiling (`MAX_OUTPUT`), not a
timid 16k. Consequences:

- 12–24 verses per `tal_triple` call is conservative; a full ahnika of 100
  verses (~35k output) fits in ONE call. Groups are configurable in
  `tal_stage.stage_seed_triple(group=N)`; the runner halves on failure.
- Fewer, bigger calls also dodge the 429 (`rate_limit_error`) that many
  small calls trigger — the client backs off 45 s × attempt on 429.
- One session per ahnika (`tal-triple-<song>`) keeps the prompt cache warm;
  with 1M context the whole ahnika + lore + prior outputs can stay resident.
- Quality guard still applies: a giant group that returns sloppy output is a
  wasted call, so start at 24, raise to 48–64 once a few runs are clean.

## 14. Overnight / unattended (watchdog + systemd)

```bash
# installed service (survives logout, reboot, SSH drop):
sudo cp tools/tal-campaign.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now tal-campaign
systemctl status tal-campaign        # active
journalctl -u tal-campaign -f        # or: tail -f process/beam/watchdog.log
```

`tools/watchdog.sh` every 60 s: starts the campaign driver if absent, keeps
N workers alive (`WORKERS=3`), detects stalls (claimed tasks + no log growth
for 25 min → restarts workers and returns claims to pending), rotates logs
> 50 MB, and appends a per-minute progress snapshot.

Safety properties for an unattended night:
- Nothing marks PASS without `validate_song` + `proof_record`; blocked ahnikas
  are parked, not forced.
- Commits are gated on `check.py` inside the driver; a red gate parks the
  commit while work continues.
- Rate limits (429) back off 45 s × attempt; exhausted tasks stop retrying.
- Everything is idempotent: killing any component and restarting resumes.
- Morning triage: `tail -50 process/beam/tal_campaign.log`,
  `tail -30 process/beam/watchdog.log`, `git log --oneline -10`,
  `python3 tools/beam_swarm.py status`, then review any parked/BLOCKED ahnika.

## 15. When beam-free runs out (observed 2026-11-06 15:30 UTC;
   cycling added 2026-11-08)

Symptom: `{"error":{"type":"rate_limit_error"}}` / HTTP 429 on a trivial
64-token ping **with zero workers running**. That is account/region tier
exhaustion, not our concurrency — do not "fix" it by adding workers.

Policy (owner directive 2026-11-08, supersedes beam-free-only): cycle the
verified-free models instead of idling. The watchdog probes health before
every pass; on total failure it logs `PAUSING 30m`, stops workers,
preserves the queue, and retries every 30 minutes. On recovery it logs
`RESUMING` and continues exactly where it stopped (everything is
idempotent).

Queue state is durable (`process/beam/queue.json`, untracked/live) and every
completed verse is on disk under `process/beam/runs/` and committed once an
ahnika assembles. Nothing is lost by pausing for hours.

## 16. Unattended operation — the full stack (2026-11-13)

Six systemd units run the whole loop. Nothing here needs a human to advance;
humans only review meaning and approve PASS.

| Unit | Role | What it does |
|---|---|---|
| `tw-wave.service` | **queue filler** | `burn_wave.sh` → `auto_burn.py` over every `mukta-m*` work: builds working-T1 (beam) → coverage gate → seeds 12–24v `tal_triple` tasks. Restarts always, so a second pass re-seeds anything missed. |
| `tal-campaign.service` | **drafting supervisor** | `harness.sh`: health-gates beam, keeps `continue/watchdog/LOOP` alive, enforces workers `w1..w3` (staggered), runs assessor sweep, tries assembly, logs gates. |
| `tw-assemble.service` | **auto-closer** | `assemble_all.py`: dynamically discovers every `working-t1-<song>.json`; when all verses have gloss+cm+am runs, runs `tal_stage` (assemble→validate→proof, dispositions honoured) and records PASS/BLOCKED. Fixed 2026-11-13 (was crashing on `Path.glob(recursive=)`; now covers ALL fronts, not a hardcoded 3). |
| `tw-recycle.timer` | **failure recycler** | `recycle_failed.py`: halves + requeues retryable failed triples. |
| `tw-watchdog.timer` | **heartbeat** | one JSON line to `process/beam/watchdog-progress.jsonl`. |
| `tw-mcp.service` | **API** | `mcp_server.py --serve-http :8930` (tunnel → `mcp.svatantrya.net`). `promote`/`validate`/`assemble` all pass `--disp tools/proof-disp.json`. |

Health check (30 seconds):
```bash
for u in tw-wave tal-campaign tw-assemble tw-mcp tw-recycle.timer tw-watchdog.timer; do
  printf '%-18s ' $u; systemctl is-active $u; done
python3 -c "import json;q=json.load(open('process/beam/queue.json'));from collections import Counter;print(Counter(t['status'] for t in q))"
tail -3 /root/assemble_all.log; tail -3 process/beam/harness.log
```

Intervene only when: (a) `tw-wave` REFUSED a work (brief gate — write
`process/beam/lore/<work>.md` with FACTS/TRAPS/Ledger), (b) a song is assembled
but proof BLOCKED (assessor: dispositions in `tools/proof-disp.json` for
verified sandhi, or fix the real defect), or (c) beam is paused >2h (account
tier — wait, do not add workers).

**Expansion / lore supply:** `tools/gen_briefs.py --apply` writes grounded
per-work briefs (bibliography + tradition doctrine) for any onboarded front
lacking one; `tools/onboard_wave.py --n N --max-verses M` onboards the next
short untranslated works (brief first, then T1+seed) so the queue never starves.
Both are idempotent and safe to run while workers drain.

**Backup:** the loop commits locally each pass and `git push origin HEAD` (was
hardcoded `master`; fixed 2026-11-13 so `burn/muktabodha` actually backs up).
Full-disk mirror on R2: `r2:opencode2-root/fs` (r2root.sh) + package snapshots.
