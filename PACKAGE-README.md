> **STATUS 2026-11-11:** steps/commands live in MUKTABODHA-RUNBOOK.md. This file supplies detail/reasoning only; runbook wins on procedure.

# translation-work — agent package (read this first)

*The Sanskrit translation machine: beam drafters + assessor gates + MCP
interface. This package is the whole system minus git history and worker
drafts (both recoverable — see §6). Machine proposes, human disposes;
DONE = machine-translated per owner directive (no review gate blocks).*

## 1. What's inside

| Path | What |
|---|---|
| `mcp_server.py` | MCP interface (17 tools: status/validate/lore/seed/review/decide/promote/…) |
| `MCP.md` | Full MCP docs: when-to-use, troubleshooting, autonomy wiring |
| `tools/` | Pipeline: `beam_client.py` (free-model chat), `beam_swarm.py` (workers), `spanda_t1_parse.py` + `prioritize_mukta.py` + `mukta_deepfind_batch.py` (Muktabodha burn), `validate_song.py`, `proof_record.py`, `check_front.py` |
| `schemas/` | Validators (t1/l0/argmap/l2/c1/c2). Schemas are truth. |
| `skills/` | `crystal-ipvv` (single-verse gold drill) + `largetext` (swarm law) |
| `lore/` | Grounds: concepts, witnesses, rasa, trika glossary |
| `process/beam/` | Live state: `queue.json` (tasks), `lore/` (transmission briefs), `mukta_priority_queue.json` + `ranked_burn.json` (burn order), `translation_audit.json` |
| `<work>/` (90+ dirs) | Per-text: `passages.jsonl`, `source/`, T1/L0/L2/C1 layers, `data/*.json`, `STATUS.json` (ground truth per work — read it first) |
| `AGENTS.md` | Operating rules. `FINAL-PROCESS.md` = canonical pipeline. `RUNBOOK.md` = bring-up/monitoring. `check.py` = gate (exit 0 = canonical). |

## 2. Prereqs

- Python ≥ 3.11, ~2 GB disk for the tree (works carry translation data).
- `pip install -r requirements.txt` (only fastmcp/pydantic/psycopg2; rest stdlib).
- One secret, never shipped: `OPENCODE_GO_KEY` (opencode-go inference).
  Export it: `export OPENCODE_GO_KEY='<key>'`. Beam calls fail without it
  (harness logs "key MISSING"). No other keys needed for translation.

## 3. Run it (three doors)

```bash
# A. MCP server (for Muse/ChatGPT/pi agents)
python3 mcp_server.py --serve        # stdio
python3 mcp_server.py --list         # 17 tools

# B. CLI single tool (testing)
python3 mcp_server.py shastra.status '{"work":"spanda"}'

# C. Workers (autonomous drafting on free beam)
bash tools/continue.sh               # supervised loop (or systemd unit tal-campaign)
python3 tools/beam_swarm.py worker w1   # one worker; w1..w3 max (free-tier throttle)
```

## 4. Translate something (the loop)

1. `shastra.recon {"work":"<dir>"}` — verse census + state (read-only).
2. Missing lore brief? Write `process/beam/lore/<song>.md` first
   (WHAT IT IS / MOVES / TRAPS / APPROACH + ledger — unbriefed seeds
   degenerate; see `lore/spanda.md` for the pattern).
3. T1 (verse draft + pada glosses) → parse to `working-t1-<song>.json`
   (see `tools/spanda_t1_parse.py`; coverage-gate ≥0.85 vs passages).
4. Seed: `{"kind":"tal_triple","args":{"work":…, "song":…, "verses":[…]},
   "status":"pending"}` in `process/beam/queue.json` — ≤12 verses/group
   (25s bounce in review).
5. Workers draft → `process/beam/runs/` → assemble → `data/*.json` →
   `validate_song` + `proof_record` → update work `STATUS.json`.
6. `python3 check.py` must exit 0 before commit.

## 5. Laws (short version — AGENTS.md is binding)

- Free models ONLY (`beam_client.MODELS` — beam-free → iceman failover).
  Anything billing Go allowance is forbidden; the client enforces it.
- Beam NEVER writes `data/`, NEVER marks PASS. Promotion is assessor act.
- T1 must cover the FULL source (verse count vs source, not tool reports).
- No pushes, no signoffs. Commit locally; owner merges.
- `/tmp` is NEVER used for translation files (scratch policy).

## 6. What's NOT in the package (and how to get it)

- `.git` history → `git clone https://github.com/prx0r/translation-work`
  (package manifest records the exact commit it was cut from).
- `process/beam/runs/` worker drafts → regenerate by re-seeding
  (assembled `data/` + `working-*.json` ARE included, so nothing final
  is lost).
- R2 snapshot of this box (full restore): `r2:opencode2-root/fs/root/`
  (see `/root/r2root-RESTORE.md` on the source box).

## 7. Pull from R2 (no git needed)

```
rclone copy r2:opencode2-root/packages/translation-work/2026-11-11/ /work/tw/ --progress
cd /work/tw && tar -xzf translation-work-2026-11-11.tar.gz
# or: rclone cat r2:.../manifest.json   (sha256 + commit + file count)
```
Manifest is authoritative: verify sha256 before use. `.env` and worker
drafts (`process/beam/runs/`) are deliberately excluded — request
OPENCODE_GO_KEY from the owner; drafts regenerate by re-seeding.
