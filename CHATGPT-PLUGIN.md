# shastra MCP — ChatGPT connector / plugin spec

*The translation machine as a remote MCP server. ChatGPT can connect to it,
call its tools, and (via the repo) edit and extend it.*

## 1. Connect (5 minutes)

Remote MCP URL (streamable HTTP, no auth yet):

```
https://mcp.svatantrya.net/mcp
```

In ChatGPT: **Settings → Connectors → Add custom connector → MCP server URL**
paste the URL above. Tools appear as `shastra__*`.
This is a **permanent named tunnel** on svatantrya.net — the URL does not
change across restarts or reboots. Serving chain: `tw-mcp.service`
(127.0.0.1:8930) → named tunnel `94250caf…` → `mcp.svatantrya.net`.

## 2. What it exposes (18 tools)

Read/status: `status`, `recon`, `gates`, `swarm_status`, `swarm_workers`,
`supervise`, `queue_guard`, `concepts`, `lore`, `skill`
Write/act (assessor acts): `swarm_seed`, `swarm_review`, `swarm_decide`,
`assemble`, `promote`, `validate`, `review_sweep`, `beam_review`

Safety: beam never writes `data/`, never marks PASS; promotion is an
assessor act; no tool pushes to git.

## 3. Where everything lives (for editing)

Repo: `https://github.com/prx0r/translation-work` (branch `burn/muktabodha`,
PR #18). On the box: `/root/translation-work/`.

| Concern | File |
|---|---|
| MCP tools | `mcp_server.py` (FastMCP; add a tool = `@mcp.tool() def name(...)`) |
| Worker/drafting | `tools/beam_swarm.py` (TAL_TRIPLE_SYS prompt, 24-verse windows) |
| Seeding | `tools/auto_burn.py`, `tools/onboard_wave.py` |
| Assembly→gold | `tools/assemble_all.py`, `tools/tal_stage.py`, `tools/build_l0.py` |
| Failure recycling | `tools/recycle_failed.py` (20-min systemd timer) |
| Queue hygiene | `tools/queue_guard.py` (unique ids, no overlapping ranges, ≥24 window) |
| Status truth | `tools/work_state.py` (+ `process/beam/work_aliases.json` FIRST) |
| Procedure | `MUKTABODHA-RUNBOOK.md` (canonical), `BUGS.md` (root causes) |
| Briefs/lore | `process/beam/lore/<work>.md` (brief + knowledge core in ONE file) |

## 4. How ChatGPT should monitor (scheduled tasks)

- **Daily 08:00**: `shastra.status` per active work → flag any that are
  not `machine-complete` and have no pending queue items.
- **Every 6h**: `shastra.gates` → if RED, run `shastra.review_sweep` and
  report the failing song (do not auto-approve prose).
- **Weekly**: `shastra.swarm_status` → worker liveness, failure classes;
  if >20% of the last 50 tasks failed with one class, report it (prompt fix).
- Never let ChatGPT call `promote` unattended — that is the human gate.

## 5. Rebuild as a ChatGPT app/plugin (if wanted)

The MCP is already the plugin surface. For an Apps-SDK app you additionally
need: a manifest (name, description, logo, `mcp.server_url`), 5–10 example
prompts, and privacy/terms URLs. The tool schemas come from FastMCP
automatically. Publish via the Apps SDK; the MCP URL above is the backend.

## 6. Auth (before public use)

Currently open (quick tunnel + no token). Before wider sharing: put the MCP
behind a token (FastMCP `auth=` / a Cloudflare Access policy on the tunnel)
and rotate the tunnel to a named one (`cloudflared tunnel create`).
