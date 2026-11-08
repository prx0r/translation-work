# HANDOVER — canonical entry point (updated 2026-11-08)

New agent? Read this first. 5 minutes. Everything else branches from here.

## Where we are

- **REGISTRY: 101 works / 86 gold / 15 pending.** Minimal gold = done
  (T1/L0/argmap/L2/C1-essence + proof PASS; L3/L4/C2 waived by owner).
- **Tantraloka: 33/37 gold (5,864 verses).** 132 verses left across
  a08 (12), a01 (24), a15 (36), a03 (60). Overnight loop grinding them.
- **Tantrasara: 22/22 COMPLETE.** Stotras/VBT/Sutra-Spanda mula: gold.
- **Sanskrit queue:** IPVV (48/49 PASS, V2-N gap) → sivasutravimarsini →
  gitarthasangraha → mvv → bharati → tattvasandoha (NO SOURCE).
- **Out of scope:** 5 mystics (Kashmiri; Sanskrit-only directive).
- Session detail: `HANDOVER-2026-11-08-TAL-CAMPAIGN.md`, `todoregistry.md`.

## The 10 todos (in order)

1. Overnight: loop grinds 132 TAL verses (free-only, local commits) — IN PROGRESS
2. Promote a08/a01/a15/a03 as each completes (assemble→validate→proof→promote)
3. TAL 37/37 verification + push
4. IPVV V2-N coverage fix (T1 38% → full)
5. IPVV proof sweep + promote to gold
6. sivasutravimarsini campaign (recon → swarm → gold)
7. gitarthasangraha campaign (Gita)
8. mvv → bharati queue (tattvasandoha needs source)
9. Acquire tattvasandoha source
10. Keep REGISTRY + docs current (no stale entries) — DONE this session

## How the machine runs

- **Single supervisor:** `systemd tal-campaign.service` → `tools/harness.sh`
  (staggered w1→w2→w3, cap 3). LOOP.sh is STOPPED (`process/beam/LOOP.STOP`)
  — never run two supervisors (worker collisions).
- **Assessor loop (you):** monitor → `review_inbox.py newest` →
  `shastra_swarm_review` → assemble → `shastra_validate` → proof →
  `shastra_promote` → update docs. No hand-drafting unless double-fail.
- **Promote order:** a08 → a01 → a15 → a03 (shortest-first).

## Iron rules

1. **FREE MODELS ONLY.** Allowlist = `beam-free` + `iceman-contributor-free`
   (both $0). Everything else on /go bills allowance — NEVER touch.
   Enforced in `tools/beam_client.py` (no override). Audit:
   `process/beam/model_usage.jsonl`.
2. **Never push unless owner says so.** Loop commits locally; pushes are manual.
3. **Schemas are truth** (`schemas/`). Pipelines pure. Observations immutable.
4. **Surface fidelity:** exact GRETIL tokens, `@` sandhi kept, no parens in
   gloss (deparen), avagraha variants normalized (norm_surface).
5. **Minimal gold only** unless owner upgrades: T1/L0/argmap/L2/C1-essence +
   proof PASS. L3/L4/C2 waived.

## Key files

- `REGISTRY.json` — truth (101 works). `todoregistry.md` — running log.
- `tools/beam_client.py` — free-only cycling. `tools/beam_swarm.py` — workers.
- `tools/review_inbox.py` — coverage/verse/next/newest. `tools/handdraft.py`
- `MCP.md` — 17 shastra tools. `RUNBOOK.md` §12/§15, `BEAM-FLOW.md` §7.
- Lore: `process/beam/lore/tal-a*.md`. Queue: `process/beam/queue.json`.

## Overnight state (2026-11-08)

Workers w1–w3 drafting on iceman (beam-free cooling). 2,923 tasks done
today. a01 retry2 seeded WITH norm_surface fix (unblocks vv169-192).
Morning: check completions, promote, push.
