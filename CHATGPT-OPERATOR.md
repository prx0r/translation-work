# CHATGPT OPERATOR — take over the translation machine

*You (ChatGPT) are the assessor/driver. The beams (3 free workers) do the
drafting; systemd keeps them alive. You control via the MCP tools below.*

## 0. Connect

MCP URL (streamable HTTP): `https://mcp.svatantrya.net/mcp`
Tools appear as `shastra__*`. Permanent: `https://mcp.svatantrya.net/mcp` (named tunnel, survives reboots).

## 1. Your control surface (MCP tools)

| Tool | Use |
|---|---|
| `shastra.progress` / `shastra.watchdog` | health line: queue, workers, failure classes, host, **flags** |
| `shastra.swarm_workers` `{action:"start"/"stop"/"status", target:"3"}` | start/stop beams |
| `shastra.swarm_status` | queue by kind/status + worker liveness |
| `shastra.swarm_seed` `{work,song}` | seed triples (24-verse windows default) |
| `shastra.recycle` | halve + requeue retryable failures |
| `shastra.queue_guard` `{fix:true}` | duplicate/overlap/undersized check |
| `shastra.assemble` `{work,song}` | assemble a completed song → validate → proof |
| `shastra.validate` | deterministic gates for one song |
| `shastra.gates` | global gate (manifest/proof/coverage) |
| `shastra.review_sweep` | mechanical review of DONE tasks |
| `shastra.status` `{work}` | one work's truth |
| `shastra.supervise` | supervisor/worker state |

## 2. Hourly scheduled task (paste this)

1. `shastra.progress` → if `flags` non-empty: act on them:
   - `NO_WORKERS_WITH_PENDING_QUEUE` → `swarm_workers start target=3`
   - `NO_BEAM_CALLS_RECORDED` → check `swarm_status`; if pending>0 and
     workers>0, wait one cycle; else `swarm_workers start`
   - `LOW_DISK` / `LOW_MEM` → report to owner, do not start new work
2. If `queue.pending < 40` → `recycle` then `swarm_status`; if still <40,
   ask owner which works to onboard next (never onboard without a
   researched brief — see §4).
3. Report one line: done Δ, pending, workers, assembled songs, top failure.

## 3. Weekly task

`gates` → if RED, `review_sweep` then `validate` the failing song; report
only (never promote prose unattended). `swarm_status` → if one failure
class >20% of last 50, flag a prompt fix (do not lower the review bar).

## 4. Hard rules you must not break

1. **Never seed a work with no researched brief** in
   `process/beam/lore/<work>.md` containing `## A.` FACTS + `## D. TRAPS`
   + a Ledger. Scaffolds are forbidden (owner 2026-11-11).
2. **24-verse windows default**, ≤60 max, halve only on bounce.
3. **Never mark PASS / never push** — promotion is owner-only; commits are
   the owner's.
4. **Duplicate prevention**: `queue_guard` before any bulk seeding;
   `work_aliases.json` wins over titles (vbt IS Vijñānabhairava).
5. Beam is **free-tier only**; never add paid models.

## 5. If something is broken

Read `BUGS.md` (root causes + fixes) then `MUKTABODHA-RUNBOOK.md` (the
canonical procedure). Code map: `tools/beam_swarm.py` (prompt + worker),
`tools/auto_burn.py` (T1→seed), `tools/assemble_all.py` (gold),
`tools/recycle_failed.py`, `tools/queue_guard.py`, `tools/work_state.py`.

## 6. Current backlog you inherit

- Queue: ~177 pending triples (Kularnava/Svacchanda/Netra/KJN/VTN)
- Assembled gold: kularnava p01–p04
- Briefs researched: Kularnava, Netra, Svacchanda, Kaulajñāna, Vātūlanātha,
  Mahānayaprakāśa, Cidgaganacandrikā, Mahārthamañjarī, Yoginīhṛdaya,
  Vāmakeśvarīmata, Tantrarāja, Mṛgendra, Kiraṇa, Kālottara, Somaśambhu
- Briefs still to research: Kubjikā, Siddhilakṣmī, Bṛhattantrasāra, Tārā,
  Kalpavṛkṣa, Janmamaraṇavicāra, Kiñcitatantra
