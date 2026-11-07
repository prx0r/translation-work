# HANDOVER — 2026-11-07 (MCP + lore + minimal promotions, assessor session)

*Machine-proposed throughout. No pushes (another agent active in repo).*

## shastra MCP (new: `mcp_server.py`, 11 tools, FastMCP stdio)
- Lanes: crystal-ipvv small (`status/validate/lore/concepts/skill`) + largetext
  swarm (`swarm_status/swarm_seed/swarm_review/swarm_decide/promote`) + `gates`.
- Rules enforced in code: lore required before seeding (mistakes #21); bounce
  notes must be actionable; approve limited to brief/pilot/distill kinds;
  `promote` refuses on gate failure, writes STATUS+REGISTRY+MANIFEST, never
  pushes/signs-off. Registered in `~/.config/opencode/opencode.jsonc` as
  `shastra` (restart opencode to load). All 11 tools verified live.
- `skill(crystal-ipvv|largetext)` serves SKILL.md + EXAMPLES — callers get
  the law with the tools.

## Lore: transmission coverage now 15/16 pending fronts (+2 bonus)
- This session: a17 (putraka thread), a30 (mantra compendium, Vol 11),
  a05 (anavopaya ladder, Vol 4+TAA CH5), a31 (Trident mandalas, Vol 11),
  a06 (kalacakra, Vol 4), a04 (saktopaya+12 Kalis, Vol 3+TAA CH4),
  a10 (7 perceivers+vastupramana, Vol 6+TAA CH10), a16 (putraka frame, Vol 9),
  a09 (36 tattvas, Vol 6+TAA CH9+TAB-kośa), a01 (foundation+means definitions,
  Vol 1), a13 (saktipata/tirodhana, Vol 7+TAA CH13). One scholarship search
  per front. Files: `process/beam/lore/tal-aNN.md`.

## Infra fixes (assessor-owned, logged in assessor-reviews.jsonl)
1. Lore NEVER injected: `beam_swarm.py` looked up `tal-{N}.md`, files are
   `tal-a{N}.md` (3 sites fixed; window-brief path already correct).
2. `STALE_CLAIM_SECS` 25min vs documented 15min → set 15 (stale a16 claims
   reclaimed immediately after).
3. Triple group default 12 → 24 (auto-halve on ceiling covers oversize).

## Queue triage
- 13x 429-transient at max (a05x11, a30x2) reset to pending/max-8; promptly
  re-429'd (free-tier quota exhausted) — watchdog pausing 30m correctly.
  Do NOT hand-fix these; they are infra, not content.
- 26x content-gate at max (a29/a10/a04/a16/a06 premise/question/row clusters)
  escalated to assessor hand-draft backlog — never auto-retry (mistakes #20).
- a30: 123/111/99 (2 groups 429-blocked). a05: 87/87/87 (11 groups 429-blocked).

## Minimal promotions (proof PASS, machine-proposed)
- a17 (122v, putraka thread): validate 0, proof 1.0 — via MCP promote.
- a31 (164v, mandala catalogue): assemble+validate+proof via tal_stage,
  promoted via MCP. Largest minimal yet.
- REGISTRY: 101 works / 73 gold / 28 pending. MANIFEST fresh (rev aac24be5).
  `validate_all --quick` 0 failures.

## Standing items for owner/next
- 429 quota is the binding constraint (not workers, not payload — 28k-token
  24v groups fit fine). Watchdog backoff is correct; leave it.
- Duplicate `tal_run_all.sh` drivers observed (2 PIDs) — verify single driver.
- Hand-draft backlog: 26 content-failed groups, shortest-first a30/a05.
- Full-gold upgrades (C1-7part+rasa+L3/L4) untouched — minimal first, per plan.

## Addendum — process flaws found + fixed (assessor audit, 2026-11-07)

1. Claims went stale mid-task (429 backoff sleeps outlast 15-min window) → worker heartbeat touches claim flag every 5 min; death stops it (self-heal preserved).
2. Duplicate tal_run_all.sh drivers → flock singleton in watchdog start_driver.
3. ralph hardcoded 5 workers → RALPH_WORKERS env (default 5; run "w1 w2 w3").
4. Queue notes unbounded (history append) → capped at 400 chars in mark().
5. No automated review → tools/assessor_sweep.py (verdicts + escalations + lore-gap seeding), wired into ralph.sh every pass.
6. REGISTRY header counters rotted → promote recomputes gold/pending/totals.
7. `review_sweep` MCP tool (16 tools total) — the loop's eyes, callable.
8. Help/docs drift (triple group 4→24) → tal_stage help + SKILL §14 updated.
9. watchdog pkill'd workers mid-task → PAUSE-file convention (drain between tasks); reap comment documents heartbeat design.
10. Beam health probe used 32 tokens (deterministic null, mistakes #22) → 2000-token probe.

All fixes verified: syntax OK (py + bash -n), gates green, MCP handshake 16/16.

## Addendum — autonomous grind (2026-11-07 ~10:20Z)
- Per-verse fallback seeded across 7 fronts (gloss→cm→am staging); workers draining ~290 glosses/25min.
- a05 promoted (159v, PASS 1.0); a06 promoted (252v, PASS 1.0). REGISTRY 101/79/22.
- a01 parse gap fixed (parser gap-tolerant + 13 hand-filled verses, 333/333, seeded).
- a30 hand-drafted 24v by assessor (3 provenance scripts); a05 hand-drafted 24v; a06 hand-draft top-ups by loop iterations.
- MCP at 16 tools (recon/assemble/supervise/swarm_workers/review_sweep added); MCP.md expansive; registered as shastra.
- Harness live: 2-worker policy, PAUSE-file, heartbeat claims, flocked driver, assessor sweep wired into ralph.
- LOOP.sh model loop running (PROMPT.md + promise gate); iteration 5+ completed, loop restarted once after silent death — needs a watchdog (see below).
- Open threads: duplicate supervisors respawn (ralph/watchdog/LOOP doubles observed — kill by exact PID, keep newest+working); tal_run_all.sh ×2 (flock prevents third); a05/a30 429-failed groups need quota-window resets.
