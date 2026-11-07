# MCP.md — shastra MCP: translation-work as callable tools

*2026-11-07. Server: `mcp_server.py` (FastMCP stdio, 14 tools). Registered as
`shastra` in `~/.config/opencode/opencode.jsonc` — restart opencode to load.
This file is the documentation: what each tool is FOR, WHEN to use it, how the
lanes and the autonomous loop fit, and what to do when things break. The law
behind the tools lives in the skills — fetch it with `skill` before acting.*

## 0. The shape (two lanes, one gate)

```
SMALL (crystal-ipvv — the ONLY path to gold)     LARGE (largetext swarm)
  status → recon → lore → hand-draft               status → recon → lore → swarm_seed
  → validate → gates                                 → workers draft → swarm_review
                                                     → swarm_decide → assemble
                                                     → validate → promote → gates
```

- **DUMB (beam drafters):** prose + coverage. Stateless, no judgment.
- **SMART (you, the caller):** transmission briefs, reviews, forks, PASS calls.
- **Scripts (tools/*):** assemble, validate, prove. Never author.
- **Gates decide green; humans dispose.** Every promotion is machine-proposed.

## 1. Skills (the law — load first)

| skill tool arg | File | When |
|---|---|---|
| `crystal-ipvv` | `skills/crystal-ipvv/SKILL.md` (+`EXAMPLES.md`) | ANY translation act: the 11-step drill, layer contracts, gates, one-work-at-a-time rule |
| `largetext` | `skills/largetext/SKILL.md` (+`EXAMPLES.md`) | ANY swarm act: DUMB/SMART split, transmission, windows ≤60, size routing, calibration, autonomy loop |

`shastra.skill` serves both texts verbatim. Read crystal-ipvv before touching a
verse; read largetext before seeding a batch. On conflict, SKILL.md + LAYERS.md
win (after the 2026-11-01 User Directive in AGENTS.md).

## 2. Tool reference — WHEN to use each

| Tool | Kind | When to use |
|---|---|---|
| `status(work, song?)` | read | FIRST call on any work: REGISTRY + STATUS + data counts + proof state + lore presence + size routing (`<1k` tokens assessor-direct, `>1k` swarm-first) |
| `recon(work)` | read | New front: spans census, workcfg registration, legacy T1, beam coverage. Never queue tasks blind — recon first |
| `lore(work)` | read | Before seeding AND before drafting: returns the cached 1-page brief (IS/MOVES/TRAPS/APPROACH). No brief → write one from web scholarship (10 min saves hours of bounce), then seed |
| `concepts(term)` | read | Hand-glossing: MITRA ranked senses + concept-DB entry = the `grounds+source` L0 options need. Unknown headwords return [] — never invent |
| `skill(name)` | read | Before any lane act (see §1) |
| `swarm_seed(work, song, group=24)` | queue-only | After lore exists. Idempotent (only missing groups). Refuses unbriefed fronts |
| `swarm_status()` | read | Queue by kind + worker liveness. Workers exit when empty — relaunch per batch, don't panic |
| `swarm_review(task_id)` | read | Every DONE task before use: draft + 5-point meaning checklist (verse-owned Q? terse premises? honest uncertainties? no forks/witnesses/PASS? traces byte-exact?) |
| `swarm_decide(task, approve|bounce, note)` | queue-only | approve: brief/pilot/distill kinds only. bounce: note MUST be actionable (span format, missing verses, flabby Q, paraphrase-not-argument), ≥10 chars. Max attempts → escalate to hand-draft, never auto-retry content (mistakes #20) |
| `assemble(work, song)` | write (working+data) | Runs complete → working-T1/L0 + data t1/l0/argmap/l2 (+C1-essence skeleton) → validate + proof. Machine-proposed |
| `validate(work, song)` | read | `validate_song` (schemas + cross-layer invariants) + `proof_record --shastra`. Fixes nothing — reports |
| `promote(work, song)` | write (STATUS/REGISTRY/MANIFEST) | validate 0 + proof PASS required, else REFUSES. Records minimal gold (L3/L4 waived), machine-proposed. Never pushes, never signs off |
| `gates()` | read | The one gate: manifest freshness + proof sweep + passages ledger + dbread. Green = shippable |
| `supervise(start_missing?)` | read (+start) | The autonomy button: reports continue/ralph/watchdog/driver/workers; optionally (re)starts absent supervisors without duplicating. Never pushes itself |

## 3. Standard flows

**Small work / single verse (assessor-direct):**
`status` → `recon` → `lore` (write if missing) → `concepts` per hard token →
hand-write T1→L0→argmap→L2→C1 per crystal-ipvv drill → `validate` → `gates` →
STATUS/REGISTRY as machine-proposed → human review.

**Large work (swarm):**
`status` → `recon` → `lore` (mandatory — unbriefed seeds degenerate,
mistakes #21) → `swarm_seed` (windows ≤60 auto? No — seed per song; keep songs
≤60 verses or split windows first) → workers draft (supervise) →
`swarm_review` each DONE → `swarm_decide` (bounce actionable / approve briefs) →
`assemble` when runs complete → `validate` → `promote` → `gates`.

**Autonomy (leave-it-running):**
`supervise(start_missing=true)` → continue.sh (300s: sync+seed, keeps ralph
alive) → ralph.sh (180s × 240: 5 workers, auto-review briefs ONLY, convert,
gate+push on green, drain-parks) → watchdog.sh (429 health-pause 30m,
stale-claim reap, tal driver). Pilots/prose/forks/PASS queue for the assessor;
the loop never judges meaning.

## 4. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| 429 Too Many Requests everywhere | Free-tier quota exhausted (binding constraint — not workers, not payload) | NOTHING to fix in code: watchdog pauses 30m, client backs off 180s×attempt. Reduce concurrency only if self-inflicted (5 workers bursting). Never swap models (beam-free hardcoded, owner directive) |
| Workers exit instantly ("queue empty") | Nothing claimable: queue drained OR claims fresh-held by dead workers | Check `swarm_status`: if `claimed>0`, wait for 15-min stale expiry (self-heals) or confirm worker PIDs dead. Don't hammer restarts |
| `finish=length` / null content | Small `max_tokens` vs hidden reasoning budget | `reasoning_effort: low` + generous `max_tokens` (triple uses 131072). Never retry-loop small budgets (mistakes #22) |
| Uniform 8-blocks / "summary unavailable" | Unbriefed beam doing geometry, not reading | Write the lore brief first; window tasks ≤60 verses; variety gate rejects >80% same-length spans (mistakes #21) |
| `premise too short` / `question rejected` / `bad row` at max attempts | Content failure, not infra | ESCALATE to hand-draft backlog. Never auto-retry, never vote-promote (mistakes #20) |
| Brief exists but drafts ignore it | Lore-lookup filename mismatch (this exact bug bit us: `tal-{N}` vs `tal-a{N}`) | Filenames MUST be `tal-aNN.md`; lookups in beam_swarm.py must match. Regression test: `recon` reports `lore_brief`, seeds inject |
| `promote` refuses | validate errors or proof BLOCKED without disposition | Fix data (assessor hand-work), or record BLOCKED disposition via proof tools — never force PASS |
| `gates()` manifest-fresh red | New canonical files (passages.jsonl etc.) unregistered | `promote` regenerates manifest automatically; manual: `tools/manifest.py gen` |
| Duplicate drivers (2× tal_run_all.sh) | Raced starts across sessions | Harmless (seeding is idempotent via have-check) but wasteful: keep the newest, kill the older by exact PID (never pkill) |
| ralph pushed something surprising | Push-on-green is the documented contract (machine-proposed commits) | Review `git log`; revert or amend by hand. To hold pushes: stop ralph (`kill <pid>`), work, restart. Never silently rewrite pushed history |

## 5. Boundaries (hard — encoded where possible)

- Beam NEVER writes `data/`, NEVER mints forks/cites, NEVER marks PASS.
  Only `assemble`/`promote` (assessor acts) write canonical files.
- `swarm_decide approve` refuses triple kinds (they promote via `assemble`).
- Bounce without actionable note is rejected by the tool.
- Transient (429/transport) failures must not consume the content budget:
  reset to pending with raised max, don't count against the 3-attempt rule.
- Content-gate failures at max escalate to hand-draft — never vote-counted
  into PARSED (mistakes #20: 3,044-row lesson).
- No tool pushes, signs off, or marks final. COMPLETE = machine-proposed,
  needs human review. Always.
