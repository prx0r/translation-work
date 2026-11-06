# HANDOVER — 2026-11-06 — TAL campaign (overnight autonomous build)

*Read this first. Then `RUNBOOK.md` §11–15 (campaign, model policy, overnight,
free-tier exhaustion), `skills/largetext/SKILL.md` §14, `mistakes.md` #25.*

## TL;DR state

- **Tantraloka: 22/37 gold.** 19 pre-existing + **a11 (118v)** + **a17 (122v)**,
  both minimal-gold, `proof PASS`, align **1.0**, cites 100%, committed.
- **a23 (103v)** minimal-gold earlier today (same standard).
- **a30 (123v) is PARTIAL**: ~5 beam groups done (≈60 verses) in
  `process/beam/runs/tal-a30-triple-*`; remainder queued, not lost.
- **Remaining after a30** (shortest-first): a05(159) → a31(164) → a06(252) →
  a04(279) → a29(292) → a03(295) → a10(310) → a16(311) → a09(314) →
  a01(333) → a13(362) → a28(435) → a08(452) → a15(613).
- **Blocked on infrastructure, not code:** beam-free returns HTTP 429
  `rate_limit_error` even with zero workers (probed 15:30 UTC, repeated).
  Per owner directive: **beam-free only, hardcoded, never swap models.**
  Watchdog therefore PAUSES 30 min, preserves the queue, and retries.

## What is running right now

```
systemd: tal-campaign.service  (enabled, active, Restart=always)
  └─ tools/watchdog.sh  (loop 60s)
       ├─ health probe every pass; on 429 → PAUSING 30m, stops workers, retries
       ├─ keeps 2 workers alive (WORKERS=2; more = more 429)
       ├─ reaps stale claims >25 min
       ├─ stall detection (claimed tasks + idle logs 25m → restart workers)
       ├─ log rotation >50MB
       └─ appends a progress snapshot each minute to process/beam/watchdog.log
```

The campaign driver (`tools/tal_run_all.sh`) walks the ORDER, runs
`tools/tal_stage.py --seed --triple --loop` per ahnika, and on success does
validate → proof → STATUS/REGISTRY → manifest → commit → push. BLOCKED parks
the ahnika and moves on. Nothing forces a PASS.

## Morning: pick up in one command

```bash
cd /root/translation-work && bash tools/morning.sh
```

Shows service state, per-ahnika proof gates, campaign tail, watchdog tail,
queue counts, parked items, recent commits.

Then:
1. `grep -E "PAUSING|RESUMING" process/beam/watchdog.log | tail -3`
   - **RESUMING** present → it is already working; check `git log`.
   - still **PAUSING** → probe manually (RUNBOOK §15), and if 200:
     `systemctl restart tal-campaign`.
2. Review the newest golds (judgment, not mechanical):
   `python3 tools/validate_song.py --song tal-a30 --work tantraloka-a30` once
   it completes; read `data/tal-a30.c1.json` — **essences are
   machine-derived from argmap inferences** and carry
   `essence_source: derived from argmap inferences (assessor review outstanding)`.
   a11/a17/a23 have real assessor essences; the driver-generated ones need
   your read or a rewrite.
3. Optional: change order or concurrency
   (`ORDER=` in `tools/tal_run_all.sh`, `WORKERS=` in the unit env) then
   `systemctl restart tal-campaign`.

## Quality contract actually applied

- **tal_triple**: one beam call per 12 verses returns glosses + morphology +
  argmap + L2 in a single pass; per-worker session ids (a shared session
  caused 429s); output ceiling 131,072; adaptive split when a group fails.
- **Gates**: exact surface match to the token list; compounds to 15 parts;
  proper-noun capitals allowed (gold TAL has them); grammar-term leakage
  banned; question must be the verse's own (≥5 words, never "what does
  verse N state"); premise ≥3 words; L2 ≥4 words.
- **Assessor residue so far**: 5 verses hand-written (a23 v8/9/17/60,
  a17 v40), 3 hand glosses (a17 v11/22/116), 1 sandhi tokenisation fix
  (a17 v22), 38 meta-question rewrites via gate.
- **No forks** in these ahnikas, so `option_choices` is empty everywhere;
  the converter warns loudly if that ever changes (it must not be silent).

## Known risks / open items

1. **Free tier is the only real blocker.** Per owner: do not swap models.
   If the window never reopens, the campaign is paused, not broken.
2. **C1 quality is uneven**: a11/a17/a23 = assessor essence; a30+ (when it
   completes) = derived. Review before counting them as final gold.
3. **Lore coverage**: 17 distill briefs banked (machine-drafted from TOC +
   scholarship pointers). Only `tal-a23.md` is deep assessor prose
   (Dupuche/Kāmika/adhva-sandhāna/dīpa-dīpavat). Others deserve a pass —
   this is the highest-leverage quality work left.
4. **a15 (613v)** is the long pole; expect ~26 triple calls at 24v/12v groups.
5. **429 policy**: never "fix" throttling by raising WORKERS; that is what
   produced the earlier storm.

## File map (new this session)

| path | what |
|---|---|
| `tools/tal_stage.py` | per-ahnika stager (parse→seed→assemble→emit→validate→proof) |
| `tools/tal_run_all.sh` | campaign driver, shortest-first ORDER, commits on PASS |
| `tools/watchdog.sh` | health gate, worker/driver supervision, stale-claim reaping |
| `tools/tal-campaign.service` | systemd unit (enabled) |
| `tools/morning.sh` | one-command triage |
| `tools/beam_client.py` | beam-free client: hardcoded model, 131k output, 429 backoff, health() |
| `tools/beam_swarm.py` | task kinds incl. `tal_triple` (batch of 12 verses) |
| `process/beam/queue.snapshot.json` | committed task snapshot (recovery) |
| `process/beam/tal_campaign.log`, `watchdog.log` | run logs |
| `process/beam/lore/tal-*.md` | transmission briefs per ahnika |
| `tantraloka-a{11,17,23}/` | the three new minimal-gold works |

## If the box reboots

```bash
systemctl status tal-campaign      # enabled → auto-starts
# if not: sudo systemctl start tal-campaign
bash tools/morning.sh
```
Everything is idempotent; re-running never duplicates outputs.
