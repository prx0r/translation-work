# MCP.md — shastra MCP: translation-work as callable tools

*2026-11-08. Server: `mcp_server.py` v3.4.7 (FastMCP stdio, **17 tools**). Registered as
`shastra` in `~/.config/opencode/opencode.jsonc` — restart opencode to load.
This file is the complete manual: concepts, lanes, every tool with WHEN and
worked examples, the autonomous loop, troubleshooting, and boundaries. The law
behind the tools lives in the skills — fetch it with `shastra.skill` before
acting. On any conflict between this file and the skills, the skills win
(after the 2026-11-01 User Directive in AGENTS.md).*

## Contents

1. Concepts — DUMB/SMART/scripts, machine-proposed, the layers
2. Skills — the law, and how to load it
3. Tool reference — all 17 tools: purpose, args, returns, WHEN, example
4. Standard flows — small work, large work, autonomy (with worked sessions)
5. Decision trees — which lane, which tool next
6. Troubleshooting — symptoms, causes, fixes
7. Autonomy wiring — the supervisors and how they fit
8. Boundaries — what the MCP will never do
9. FAQ

---

## 1. Concepts

**DUMB (beam drafters, `beam-free`, $0).** Fast, obedient, stateless. One task,
one session ID, no memory, no tools, no judgment. Allowed: prose drafts,
coverage, span tiling, first-draft reasoning. Forbidden: canon, adjudication,
witnesses, PASS, signoff, push. When it fails, it fails mechanically (format,
uniformity, thin premises) — fix the packet (brief, windows, group size),
not the model. Throughput: a full TAL-brief batch per half hour; prose
~5–10 min per 24-verse group.

**SMART (you, the caller).** Holds the whole text, the scholarship, and the
gates. Writes transmission briefs (web search first), reviews every draft,
adjudicates forks, runs converters and proofs, owns every PASS. Irreplaceable
because meaning has no mechanical proxy: uniform briefs pass pydantic schema
checks, and vote-counting once laundered 3,044 real errors (mistakes #20).

**Scripts (`tools/*`).** Assemble (converters, mergers), never author.
Pydantic validates SHAPE; only the assessor validates MEANING.

**Machine-proposed.** Everything the swarm produces is labeled machine-proposed
pending human review. Promotion into canonical `data/` is an assessor act
(`swarm_decide approve` + converters + validators), never a worker act.
COMPLETE always means "machine-proposed, needs human review" until a human
signs off. No exceptions.

**The layers (what each one is).** SOURCE (sha-pinned) → T1 (fast
verse-draft + per-token quick gloss; coverage before sharpness) → L0 (term
audit: morphology + ranked options with grounds; forks live HERE only) →
ARGMAP (whole-verse argument, adjudicates forks on the record) → L2 (plain
read prose, every clause traces to L0, byte-exact cites) → C1 (essence +
7-part essay; states the matters, never the document) → L3 (frozen final
verse) → L4 (song; music never doctrine) → proof (B1–B8 machine checks) →
site. Minimal gold = T1/L0/argmap/L2/C1-essence + proof PASS with L3/L4
waived. Full gold adds the 7-part C1 + rasa + L3 + L4.

## 2. Skills (the law — load first)

| `shastra.skill` arg | File | Load it when |
|---|---|---|
| `crystal-ipvv` (or `crystal`) | `skills/crystal-ipvv/SKILL.md` + `EXAMPLES.md` | Before ANY translation act: the 11-step drill, layer contracts, per-layer prompts with good/bad exhibits, gates, one-work-at-a-time |
| `largetext` (or `large`) | `skills/largetext/SKILL.md` + `EXAMPLES.md` | Before ANY swarm act: DUMB/SMART split, transmission briefs, window rule (≤60 verses), size routing, calibration benchmarks, autonomy loop, factory porting |

`shastra.skill` serves both texts verbatim (truncated at 12k chars each —
read the files directly for the full text). Also canonical: `FINAL-PROCESS.md`
(the process), `LAYERS.md` (contracts), `crystal.md` (finished-work standard),
`mistakes.md` (26 binding failure rules), `BEAM-FLOW.md` (operator runbook).

## 3. Tool reference

Conventions: all tools take a single JSON object; all return JSON. `work` is
the directory name (`tantraloka-a17`); `song` is the verse-addressed unit
(`tal-a17`). Read tools never write. Write tools never push, sign off, or
mark final.

### `status(work, song?)` — read. The entry point. Call FIRST on any work.

Returns: REGISTRY row, STATUS.json, per-layer data counts (`data_counts`),
proof record, lore-brief path (or null), `source_tokens`, and `routing`:
`assessor-direct (<1k)` — write it by hand; `swarm-first (>1k)` — seed beam
first, redacting after. (Threshold counts Sanskrit whitespace tokens; a 122v
ahnika ≈ 930 tokens sits on the line — route by judgment, defaulting to swarm
for passages, hand for single verses.)

Example — `{"work": "tantraloka-a17", "song": "tal-a17"}` returns registry
status, 122/930/122/122 counts, proof PASS 1.0, brief path, routing.

### `recon(work)` — read. New-front intake report.

Returns: workcfg registration + kind + per-song verse counts, span/token
census, legacy T1 filenames, lore presence, existing `data/*.t1.json` counts.
Use before queuing anything: it tells you what exists, what's missing, and
whether a brief is owed. Never queue tasks blind — recon first.

### `lore(work)` — read. The transmission brief (or its absence).

Returns the cached 1-page brief: what the text IS → numbered MOVES → TRAPS →
APPROACH. Returns `brief: null` + available list when missing — that is an
instruction, not an error: spend 10 minutes on web scholarship, write
`process/beam/lore/tal-aNN.md`, then seed. Unbriefed seeds degenerate into
uniform geometry (mistakes #21). Briefs are cached per front — write once,
every later packet injects automatically.

### `concepts(term, top=5)` — read. Grounds for hand-glossing.

Returns MITRA frequency-ranked senses with attestations + concept-DB entry.
Output is the `grounds + source` shape L0 options require. Unknown headwords
return [] — look it up elsewhere, never invent. This is legwork support for
the assessor's morphology, not a promotion path.

### `skill(name)` — read. The law, verbatim.

### `swarm_seed(work, song, group=24)` — queue-only. Idempotent.

Seeds triple tasks (gloss+CM+argmap+L2 per verse-group) for missing coverage
only. REFUSES unbriefed Tantraloka fronts. Default 24 verses/group; oversize
groups auto-halve on output ceiling. Seeding is free — workers + quota are the
constraints, not tasks.

### `swarm_status()` — read. Queue by kind × status + worker liveness.

Workers exit when empty — that is normal, not a crash; relaunch per batch
(the supervisors do this). `claimed` older than 15 min = dead worker;
self-heals on next claim (stale-flag steal).

### `swarm_review(task_id)` — read. The assessor's review packet.

Returns the task + all per-verse drafts (gloss/cm/am) + the 5-point meaning
checklist: (1) question is the verse's OWN, never meta; (2) premises terse
logical steps, never paraphrase; (3) uncertainties honest and specific;
(4) no fork adjudication, witness cites, or PASS language; (5) surfaces
byte-exact, rows cover every token. Read the drafts against the checklist,
then decide.

### `swarm_decide(task_id, approve|bounce, note)` — queue-only.

- `approve`: brief/pilot/distill kinds ONLY. Triple output never approves —
  it assembles via `assemble`.
- `bounce`: note MUST be actionable (≥10 chars enforced): span format,
  missing verses, flabby question, paraphrase-not-argument, bad row with the
  offending surface named. Vague notes are rejected by the tool.
- At max attempts the task escalates to the assessor hand-draft backlog —
  the tool reports it; never auto-retry content failures (mistakes #20).

### `assemble(work, song)` — write (working + data). Machine-proposed.

Beam runs → working-T1/L0 + data t1/l0/argmap/l2 (+C1-essence skeleton) →
validate + proof. Requires complete runs; reports incompleteness instead of
partial-assembling. Pair with `promote`.

### `validate(work, song)` — read. The deterministic gates.

`validate_song` (schemas + the 6 cross-layer invariants: chosen==gloss,
coverage==source, traces resolve, cites byte-exact, ...) + `proof_record
--shastra` (alignment, C1/L2 overlap, quotes, metacommentary, cites). Reports
only — fixes nothing. Nonzero payload on errors.

### `promote(work, song)` — write (STATUS + REGISTRY + MANIFEST).

Demands validate 0 errors AND proof PASS, else REFUSES with reasons. Records
minimal gold (L3/L4 waived), updates STATUS + REGISTRY + MANIFEST. Labels
everything machine-proposed, needs human review. Never pushes, never signs.

### `gates()` — read. The one gate.

Manifest freshness + proof sweep + passages ledger + dbread coverage. Exit
nonzero in payload when unshippable. Run after every promotion; green means
the tree is coherent.

### `supervise(start_missing=false)` — read (+start). The autonomy button.

Reports the loop: systemd unit `tal-campaign` state, watchdog/ralph/continue/
tal drivers, and live workers. With `start_missing=true` it (re)starts the
**systemd unit** if inactive (the single supervisor) — it does NOT spawn
continue.sh/ralph.sh by hand; never pushes. See §7.

### `swarm_workers(action="status", target="1")` — the throttle.

`status`: live workers + what each holds. `start`: launch up to `target`
free slots (numbers 1..5; house policy is ≤3), staggered ~8s, HEALTH-GATED
(refuses while beam is down).
`stop`: kill named slots (`target: "w4,w5"`) — claims self-heal via stale
expiry. Doctrine: start ONE; add a second only if quota is healthy; never
pound a throttled tier. Supervisors (ralph/watchdog) keep their own workers —
use this tool for deliberate single-worker operation, not to fight them.

### `review_sweep()` — read + log + queue-seed. The assessor daemon.

Mechanical verdicts for new DONE triples (question/premise/uncertainty shape),
escalation of content-failures-at-max to the hand-draft backlog, `lore_queries`
seeding for unbriefed fronts. Never bounces, never approves prose, never
writes data/. Runs inside ralph every pass — the loop's eyes while the model
sleeps; meaning judgment stays queued.

### `beam_review(task_id="", max_new=1, apply=false)` — SMART-beam reviewer.

One cheap "dumb+smart" pass over the newest unreviewed DONE drafts, bouncing
ONLY mechanical fails with an actionable note (never approves prose, never
touches meaning). `task_id` reviews one specific task; omit to sweep. Off by
default in ralph (`RALPH_BEAM_REVIEW=0`) so it does not steal quota from the
drafters; turn on when the tier is quiet. Logs every verdict to
`process/beam/assessor-reviews.jsonl`.

### Review console (CLI, not an MCP tool) — `tools/review_inbox.py`

The assessor's hands-on view while beam drafts: no model calls, reads only
`process/beam/runs/`. Use it to drive quality by hand.

```
python3 tools/review_inbox.py coverage tantraloka-a13   # per-layer done/missing + task status
python3 tools/review_inbox.py verse    tantraloka-a13 58 # source + gloss/cm/am for one verse
python3 tools/review_inbox.py next     tantraloka-a13    # first verse missing a layer, shown
python3 tools/review_inbox.py newest                     # newest am drafts across fronts
```

## 4. Standard flows (with worked sessions)

**Small work — one verse by hand (assessor-direct).**
1. `status` → `recon` → `lore` (write the brief if null — even single verses
   benefit: traps + approach).
2. `concepts` for each hard token (grounds, not answers).
3. Hand-write T1 → L0 (morph + ranked options, forks with analyzed morph) →
   argmap (terse Q/premises/inference, adjudicate forks) → L2 (rasa-carried,
   traced, byte-exact cites) → C1 (essence + 7-part, 0 quotes/meta/shared).
4. `validate` → fix → `gates` → STATUS/REGISTRY as machine-proposed.
5. Human review. (C2 renders only after essence is reviewed.)

**Large work — one ahnika via swarm (worked session: tal-a31, 164v).**
1. `status(tantraloka-a31, tal-a31)` → recon: 164 spans, legacy T1 present.
2. `lore` → brief existed (Trident mandalas, Vol 11, tantra-source spans).
3. `swarm_seed` → groups queued; workers drafted gloss/cm/am per verse.
4. `swarm_review` per DONE task (checklist; bounce actionable, max 3).
5. `assemble` when runs complete (164/164/164) → validate 0 + proof PASS.
6. `promote` → REGISTRY minimal gold. 7. `gates` → 0 failures.

**Triage — quota storm (worked session: a05/a30 429s).**
1. `swarm_status` shows mass `failed` with `beam chat failed … 429`.
2. Distinguish: transient (transport/429 notes) vs content (premise/question/
   row notes). Transients reset to pending with raised max — infra failures
   must not consume the content budget. Content-at-max escalates to the
   hand-draft backlog — never retried, never vote-promoted.
3. Workers + watchdog pause on 429 by health gate; resume on reset. Do not
   hammer restarts; do not swap models.

**Autonomy — leave it running.**
1. `supervise(start_missing=true)` once.
2. continue.sh (300s): registry sync → seed → keeps ralph alive.
3. ralph.sh (180s × 240): workers → auto-review (briefs only) → convert →
   gate → push on green → drain-parks.
4. watchdog.sh: 429 health-pause + stale-claim reap + tal driver.
5. Assessors review queued prose/forks/BLOCKEDs on wake. The loop never judges
   meaning — sampling (1-in-5 + all full-ahnika briefs) is the only content
   check in the autonomous path.

## 5. Decision trees

**Which lane?**
```
<1k source tokens, single verse/passage → assessor-direct (SMALL flow)
>1k tokens, or >1 verse-group → swarm-first (LARGE flow)
philosophical density high (proofs, taxonomies) → swarm drafts, assessor redacts heavily
fork-heavy / witness-dependent → assessor-direct regardless of size
```

**Which tool next?**
```
new front → status → recon → lore? (null → write brief) → seed|draft
task DONE → swarm_review → (clean → leave for assemble) | (fixable → swarm_decide bounce) | (failed-at-max → backlog, hands off)
runs complete → assemble → validate clean? → promote → gates green? → next front
anything red → read the error, fix the layer, re-validate (never force)
```

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| 429 Too Many Requests everywhere | Free-tier quota exhausted — the binding constraint (not workers, not payload; model window is 1M in / 384k out, 24-verse groups fit easily) | Nothing to fix in code. Watchdog pauses 30m; client backs off 180s×attempt. Don't hammer restarts, don't swap models (beam-free hardcoded, owner directive) |
| Workers exit instantly ("queue empty") | Nothing claimable: drained, or claims fresh-held | `swarm_status`: `claimed>0` + workers 0 → wait for 15-min stale expiry (self-heals). Pending 0 + failed-at-max only → seed more or hand-draft the backlog |
| `finish=length` / null content | Small `max_tokens` vs hidden reasoning budget | `reasoning_effort: low` + generous budget (per-verse 64k, triple 384k = full model output). Never retry-loop small budgets (mistakes #22) |
| Uniform 8-blocks / "summary unavailable" | Unbriefed beam doing geometry | Write the lore brief; windows ≤60; variety gate rejects >80% same-length spans (mistakes #21) |
| `premise too short` / `question rejected` / `bad row` at max | Content failure | Hand-draft backlog. Never auto-retry, never vote-promote (mistakes #20: the 3,044-row lesson) |
| Brief exists, drafts ignore it | Lookup/filename mismatch (this exact bug: `tal-{N}` vs `tal-a{N}`) | Convention is `tal-aNN.md` everywhere; `recon` reports the resolved path — verify it before seeding |
| `promote` refuses | validate errors or BLOCKED without disposition | Fix the data layer, or record a BLOCKED disposition via proof tooling. Never force PASS |
| `gates()` manifest-fresh red | New canonical files unregistered | `promote` regenerates automatically; manual: `tools/manifest.py gen` |
| Duplicate drivers / double seeding | Raced starts across sessions | Seeding is idempotent (have-check) so harmless; keep newest, kill older by exact PID (never pkill) |
| Surprise push from the loop | Push-on-green is the contract (machine-proposed commits) | Review `git log`; to hold pushes, stop ralph, work, restart. Never rewrite pushed history |

## 7. Autonomy wiring

```
continue.sh (300s loop) ── sync registry → PLAN.json → seed
      │                      └─ ensures ralph.sh alive
      ▼
ralph.sh (180s × 240) ── manifest → workers ($RALPH_WORKERS, default 3, staggered 1→2→3)
      │                   → auto-review (briefs only) → assessor_sweep (verdicts
      │                     + escalations + lore-gap seeding, log only)
      │                   → convert pilots → validate_all --quick → push on green
      │                   → drain → park with review queue for assessor
      ▼
watchdog.sh ── 429 health gate (pause 30m, PAUSE-file: workers drain between
      │           tasks, never killed mid-call) → stale-claim reap → tal driver
      │           (flock singleton)
      ▼
tal_run_all.sh / tal_stage.py --loop ── seed → wait → assemble → validate → proof
      ▼
assessor (you, on wake) ── lore briefs → swarm_review/decide → hand-draft backlog
                          → assemble/promote → HANDOVER → human review queue
```

Workers heartbeat their claim flags every 5 min during long beam calls, so a
24-verse task in 429-backoff is never stolen mid-task; dead workers' claims
self-heal at 15-min stale expiry.

**Deployment note (2026-11-08).** On this box the *only* supervisor is
`systemd` unit `tal-campaign.service` (Restart=always) → `watchdog.sh`. The
watchdog is the single health-gated authority: it probes beam, PAUSEs 30m on
429, starts the `tal_run_all` driver once (flock), and brings workers up
**staggered — one new slot per healthy 60s pass, hard cap 3**
(`WORKERS=3`). Do not also launch `continue.sh`/`ralph.sh` by hand alongside
it; that creates duplicate supervisors. Use `supervise` to inspect, and let
the unit own the loop. Worker cap and stagger are set in the unit env +
`watchdog.sh::start_workers`.

`shastra.supervise` reports and (re)starts this stack. Judgment stays queued:
pilot prose, fork calls, BLOCKED dispositions, signoffs. Sampling (1-in-5
window briefs, all full-ahnika briefs) is the only content check in the loop —
without it the loop certifies its own homework (mistakes #24).

## 8. Boundaries (hard — encoded where possible)

1. Beam NEVER writes `data/`, mints forks, cites witnesses, or marks PASS.
   Only `assemble`/`promote` (assessor acts) write canonical files.
2. `swarm_decide approve` refuses triple kinds; triples promote via `assemble`.
3. Bounce notes must be actionable (tool-enforced); vague notes rejected.
4. Transient failures reset with raised max; content failures escalate.
   Agreement is never evidence; repeated error is never consensus.
5. No tool pushes, signs off, or marks final. COMPLETE = machine-proposed,
   needs human review. The gate is a proxy; the rule is the law.

## 9. FAQ

**Why two lanes?** Volume. A 613-verse ahnika cannot be hand-drafted in one
session; a 4-token verse should never cost a swarm round-trip. Size routing
(<1k tokens hand / >1k swarm) puts judgment where judgment lives.

**Why not let beam adjudicate forks?** Untested on forked verses; votes
launder shared error. Proven on easy verses only (tsa-a02-v01 4/4 traces) —
assumed weak until proven otherwise.

**Why 24 verses per triple call?** Fewer, bigger requests: the model gives
1M-token context and 384k-token output; each triple packet carries the FULL
transmission brief + legacy per-token hints + neighbouring verses. Oversize
groups auto-halve on the output ceiling. Seeding is free; quota is not.

**Why do workers keep dying?** They exit when nothing is claimable — by
design. Supervisors relaunch per batch. A dead worker's claim self-heals via
15-min stale expiry. Check `swarm_status` before intervening.

**Where do I start on a new front?** `status` → `recon` → `lore`. Always in
that order. Ten minutes of scholarship before queuing beats hours of bounce
cycles after.

**What counts as DONE?** Draft → selfcheck green → assessor review →
(approve|bounce×N) → converter → `validate_song` 0 errors → `proof_record
--shastra` PASS (or recorded BLOCKED disposition) → STATUS/REGISTRY updated →
still labeled machine-proposed. Faked PASS is dismissal-worthy.
