# CHATGPT-OPERATOR.md — run the translation machine from ChatGPT (MCP)

*You are the operator/assessor. You monitor the free beam workers hourly, keep the
queue healthy, review drafts, assemble/promote machine-proposed results, and
troubleshoot — all through MCP tool calls. You do NOT sign off, mint PASS, or
publish; the human holds those. Machine-proposed means needs-human-review.*

---

## 0. Connect (once)

ChatGPT → **Settings → Connectors → Add custom connector**.

| Purpose | MCP URL | Tools |
|---|---|---|
| **Operator (this doc)** | `https://shastra.svatantrya.net/mcp` | 29 — swarm/ops + bibliography |
| Site federation (openpatala/scholar/formal) | `https://mcp.svatantrya.net/mcp` | 40 — read sheaf |
| Book factory | `https://book.svatantrya.net/mcp` | 22 |
| Video factory | `https://video.svatantrya.net/mcp` | 18 |
| OpenPatala REST (not MCP) | `https://patala.svatantrya.net` | 46 `/v1/*` |

On `shastra.svatantrya.net` tool names are bare (`progress`, `swarm_status`, …).
ChatGPT may display them as `shastra__progress`.

If a scripted client gets `403`, it sent `User-Agent: Python-urllib/…` (edge
filter). Use any real UA.

---

## 1. What you can and cannot do

**CAN:** monitor health/queue/workers; start/stop beam workers; seed draft tasks;
recycle dead tasks; run queue hygiene; mechanical review sweep; bounce bad drafts
with notes; assemble completed songs; validate; run the global gate; promote
**after owner review**; look up bibliography/priority/availability.

**CANNOT / MUST NOT:** mint PASS, sign off, publish, push to git, or call
`promote` without the owner's go-ahead. The beams (free tier) do the drafting;
you direct and check.

---

## 2. The hourly loop (copy this as a scheduled task)

**Every hour, run exactly this and report one line:**

1. **`progress`** — read `queue`, `workers_alive`, `last_beam_call`, `flags`,
   `host`. Act on flags:
   - `NO_WORKERS_WITH_PENDING_QUEUE` → `swarm_workers {action:"start", target:"1"}`
     (add `w2`,`w3` only if `progress` shows beam healthy and pending > 80).
   - `NO_BEAM_CALLS_RECORDED` → check `swarm_status`; if pending>0 and workers>0,
     wait one cycle; else `swarm_workers {action:"start", target:"1"}`.
   - `LOW_MEM`/`LOW_DISK` → report to owner, do not start work.
2. **`swarm_status`** — if `pending < 40`:
   - `recycle {dry_run:false}` (halve + requeue retryable failures), then re-read.
   - still `< 40` → **ask the owner which works to onboard** (never onboard without
     a researched brief — `onboard_wave` enforces `brief_gate`).
3. **`gates`** — if RED (non-empty failures), run `review_sweep`, then report the
   failing song; do not auto-approve prose.
4. **Failure triage** — if `failure_classes_top5` shows one class >20% of recent
   failures, run `beam_review {max_new:2}`; if it is mechanical (session
   hypothesis), report "prompt fix: <class>" to the owner.
5. **Queue hygiene** — weekly (or when overlaps suspected): `queue_guard {fix:true}`.
6. **Report one line:** `doneΔ / pending / workers / assembled / top-failure / flags`.

Scheduled-task prompt (paste into ChatGPT tasks):
```
Every hour: call progress, swarm_status, gates on shastra.svatantrya.net.
Act on flags per CHATGPT-OPERATOR.md §2 (start ≤1 worker first; recycle if
pending<40; review_sweep if gates red). Never promote/publish. Reply with one
status line: done / pending / workers / assembled / top-failure / flags.
```

---

## 3. Driving a translation (when the owner picks a work)

```
priority {limit:10}                     → pick next (untranslated, shortest first)
bibliography {catalog:"M00xxx"}         → what translations already exist
recon {work:"mukta-m00xxx"}             → source spans, songs, what's missing
swarm_seed {work, song, group:24}       → queue draft tasks (needs a lore brief)
swarm_status                            → watch progress
swarm_review {task_id}                  → read a DONE draft + checklist
swarm_decide {task_id, verdict:"approve"|"bounce", note:"…"}  → queue verdict
assemble {work, song}                   → working T1/L0 + data (machine-proposed)
validate {work, song}                   → deterministic gates
promote {work, song}                    → ONLY after owner review
gates                                   → global gate green?
```

`swarm_seed` requires a transmission brief; if `recon`/`lore` shows none, tell the
owner a brief is owed (you may draft it from web scholarship, owner approves).

---

## 4. Troubleshooting playbook

| Symptom (`progress`/`swarm_status`) | Cause | Action |
|---|---|---|
| `workers_alive:0`, `pending>0` | workers exited/crashed | `swarm_workers {action:"start", target:"1"}` |
| `last_beam_call` old, workers alive | beam throttled (429) | wait one cycle; if still stale, `swarm_workers {action:"status"}`, start one |
| one task re-claimed forever, same verse error | poison (schema/premise) | `recycle {dry_run:false}`; if persists, owner/escalate |
| `failed` climbing, one class dominant | prompt/packet issue | `beam_review`, report "prompt fix" |
| `pending` overlaps/dupes | seeder bug | `queue_guard {fix:true}` |
| gates RED (manifest/proof) | drift or unshipped | `review_sweep`; report failing song; do NOT approve prose |
| `LOW_MEM`/`LOW_DISK` | box pressure | stop starting work; report |

Failure classes seen: `question rejected`, `premise too short`, `schema fail`,
`surface drift`, `l2 too short`. All are RETRYABLE at a smaller window →
`recycle` halves them.

---

## 5. Tool reference (operator surface, 29)

Health/ops: `progress`, `watchdog` (alias), `supervise`, `swarm_status`,
`swarm_workers {action:status|start|stop, target:"1|2|3|w4,w5"}`, `recycle
{dry_run}`, `queue_guard {fix}`, `gates`.
Drafting: `swarm_seed`, `swarm_review`, `swarm_decide`, `review_sweep`,
`beam_review`, `assemble`, `validate`, `promote`.
Per-work: `status`, `recon`, `lore`, `skill {name:"crystal-ipvv"|"largetext"}`,
`concepts {term}`.
Bibliography/priority: `bibliography`, `priority`, `schema`, `stats`, `works`,
`editions`, `links`, `availability`.

Skill law lives in `skills/crystal-ipvv/SKILL.md` (single-work quality) and
`skills/largetext/SKILL.md` (swarm). Fetch with `skill` before judging a draft.

---

## 6. Safety / boundaries

- Machine-proposed only. `promote` needs owner confirmation.
- No git push, no PASS mint, no publish, no schedule-the-owner's-money.
- The queue/queue files are shared; never edit them by hand — use the tools.
- If the free tier is throttled, pause (progress flags) — do not hammer.

---

## 7. Self-check (run after connecting)

```
progress   → JSON with queue/workers/flags
gates      → "VALIDATE_ALL: N failures"
priority   → ranked rows (burn_rank, T_why)
```
If all three answer, you are the operator. Start the hourly loop.
