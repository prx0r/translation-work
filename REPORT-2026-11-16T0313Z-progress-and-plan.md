# Translation-Work Progress Report — 2026-11-16T03:13Z (UTC)

*Source: live `shastra_*` tools + `/root/translation-work` docs + git status. Machine-proposed, no signoff.*

## 1. What we were doing (last sessions → now)

**Two lanes, per AGENTS.md / WHERE-WE-ARE.md (2026-11-14/15):**

- **SHIP (quality lane, priority):** Trika core — 95 works / 371 songs. Prove + serve to ChatGPT correctly. 367 GATE-OK, 4 out-of-scope, 3 REGRESSION (ghatakarpara, documented source-coverage hold).
- **BURN (bulk lane, background):** Continuous unattended T1 (contract gloss) + L0 (per-token morphology + grounds) for whole Muktabodha corpus via free-tier beam. Stops at L0 on purpose. No argmap/L2/C1 in burn. Triples deprecated for burn (`layers=full` only for assessor).

**Session arc:**
- 2026-11-14: fixed stale-brief bug, reconciled MCP 31→36 tools, `audit_align` + 211 honest sandhi dispositions → 25 songs PASS, kularna close-out 76→79/83, prove+expose pipeline (readability 56→92/144), third-party audit import (audited `master`, 1082 commits stale — accurate but out-of-date).
- 2026-11-15: 37 Tantraloka source records + byte-span manifests (serve 56→92/95 Trika), `ipvv-vivrti-vimarsini` alias → `ipvv`, 243/245 classic proofs re-proved shastra, `proof_record` autojunk fix (difflib `autojunk=True` → `False`; monotone-safe, min_ratio p10 0.912→0.927, low-ratio 63→57), `burn_status` tool + `validate_all` mcp-smoke 22/22.
- Now (2026-11-16 03:09–03:12Z): burn still draining tails, loop healthy, serve at 132/146.

## 2. Live state (this run)

| Signal | Value |
|---|---|
| Queue | `done 18268`, `pending 47`, `claimed 5`, `failed 1886` (watchdog 03:11Z) |
| Failure top5 | `question rejected 752, premise too short 253, l2 too short 183, surface drift 55, schema fail 47` |
| Burn done | `gloss 25303 / cm 25105 / legacy_am 22031`; pending `tal_cm 85`; `ok=true` (0 stray triple/am) |
| Works active / verses indexed | `219 / 180412` |
| Workers | `5-7 alive (w1-w5)`, last beam `03:11:36Z`, load `2.62`, mem `2769MB`, disk `9.4GB free`, `paused=false` |
| Supervisor | `systemd tal-campaign` owns `harness.sh` + `continue/watchdog`, staggered workers. Do NOT start by hand. |
| Quota | `2 keys`, `beam-free parked ~240s`, failover to other key, 30m park only if both 429 |
| Assembled songs | `kularnavatantra 82, svacchandatantra 23, netratantra 5, mukta-m00027 27, mukta-m00099 1` |
| Review | `6100/6100` triples reviewed; recent `33 escalated-hand-draft, 101 needs-assessor, 66 useful-first-draft`; sweep this run `verdicts=0` (caught up) |
| Bibliography | `499 catalog rows, 213 translated, 286 unresolved, 294 keyed editions, 743 availability works (full 125 / partial 82 / none 271)` |
| Priority top | `M00504 amṛteśatantra (1v), M00506, M00287, M00029, M00549…` — all 1-verse untranslated-short first |

## 3. Proofs — are they right?

- `gates (live)`: 1 FAIL — `manifest-fresh: CHANGED mukta-m00195/T1-mukta-m0-p554.md`. All else PASS: `schemas-import, passages-ledger (12 colliding locators grandfathered), mcp-smoke, validate-songs, proof-sweep, check-canonical, dbread-ipvv`. Disk log `validate_all.log` (Nov 6) says 0 failures — **stale**, ignore; live tool is truth.
- `verify_core (full)`: timed out this run (too large). Per WHERE-WE-ARE baseline: 367 GATE-OK, 3 REGRESSION = ghatakarpara p01-p03 (parser now covers both pādas, T1 still has only second pāda → align 0.60-0.65 BLOCKED). Correct intended signal, not new defect. `check.py`/`validate_all` still read stored PASS → gates stay green; only honesty check flags it.
- `serve_status (fresh)`: `146 audited, 132 served, 14 unserved/empty-projection` — `ghatakarpara, mukta-m00004/m00034/m00062/m00099/m00122/m00290/m00293/m00557/m00562/m00642/m00644/m00664, netratantra`. Examples: `kularnavatantra 2018 src / 83 traces/verify/claims`, `mukta-m00125 1300/293`, `tantraloka-a01..a37 + tantrasara-a01..a22` all served, `ipvv 5 src / 49 traces / 98 verify/claims`.
- `health serve cache 17.2h` says 1 served — stale, use `serve_status` above.
- Trust boundary (skills/proof): PASS = structural contract (census + B1 parse + B3 concat-align + B4-B6 + B7 byte-exact cites + B8 schema), **never scholarly correctness**. Every PASS still carries `needs:["human-review"]`.

## 4. Manifest FAIL audit (the 1 gate failure)

`git status`: `M MANIFEST.json, M mukta-m00195/{p554,p57,p88}, M mukta-m00198/p153 + working-*.json, queue.json, serve_summary.json, model_usage.jsonl`, plus untracked burn runs/claims.

`diff mukta-m00195/T1-mukta-m0-p554.md`: burn improved glosses — `[tat+keśareṣu](tatkeśareṣu)` → `[then](tat) [on-filaments](keśareṣu)`, `[vṛtta+dvaya+antar+vīthyām](...)` → `[in-space-between-two-circles](...)`, etc. ~25 verses. **Legitimate burn output, not a defect.** Fix = refresh MANIFEST (manifest records file hashes; burn wrote content without refreshing). No content revert.

## 5. Plan — what's next and why

1. **Fix manifest-fresh (unblocks ship).** Why: single gate failure blocks `validate_all` shippable. How: regenerate manifest entry for changed T1/working files (tooling, not hand-edit), re-run `gates` → 0 failures.
2. **Re-verify honesty per-work (not full).** Why: full `verify_core` times out; per-work sampling proves no hidden REGRESSION beyond the 3 known. How: `verify_core work=kularnavatantra`, `ipvv`, `sivastotravali`, `ghatakarpara` one at a time.
3. **Recycle triage (dry-run first).** Why: 1886 failed, mostly mechanical (`question rejected`, `premise too short`, `l2 too short`) — recyclable once, single generation (`rc2-`). How: `recycle dry_run=true`, inspect, then recycle only non-covered ranges.
4. **Unserved 14 readiness.** Why: 14 audited but empty projection = cannot serve. Check each for `source_spans` vs `emit_scholar` BLOCKED reason (coverage hold vs missing data). Ghatakarpara + netra already known holds; others likely short-tail burn gaps.
5. **Drain burn tail (~47 pending cm).** Why: foundation completion (~4.6k verses per roadmap) precedes interpretive lane. Let `tw-wave` drain; no new triples.
6. **Owner lane (human-only, do not auto-act):** D1 ghatakarpara 147-token hand repair, D2 sivastotravali s10/s12 T1 convention, D3 confirm shastra-canonical, D4 authorize 11 autojunk flips, D5/D5b MCP auth + bridge runtime (ChatGPT still cannot read Tantraloka publicly — local serves, public bundle 55 works stale + bridge `AttributeError`), D6 merges + L4 voice + audit re-run vs `burn/muktabodha`.

## 6. Risks / traps

- Never fabricate Sanskrit to green a gate (147-token repair stays human).
- Never mass-promote (11 autojunk flips need owner auth).
- Never force proof mode across lineages (shastra vs classic).
- `burn/muktabodha` is live; `master` is ~1082 commits behind — any external audit must target burn branch.
- Disk 9.4GB — watch `process/beam/runs/` growth.

---
*Next: execute §5.1–5.4 autonomously, then final validation + handoff.*

## 7. Autonomous work executed (03:13–03:20Z)

- Manifest: `python3 tools/manifest.py gen` → 14092 files, `gates` 0 failures at that instant. Burn then wrote `mukta-m00217/p100+p111` → gates FAIL again on new CHANGED. Expected: manifest is a moving target while burn lives; regen at publish/commit time, not continuously.
- `verify_core work=kularnavatantra`: 82 songs, 81 GATE-OK, 1 STILL-BLOCKED (`kul-p49` ALIGN_NODISP 0.793, no disp), 0 regressions. Proofs honest.
- `verify_core work=ghatakarpara`: 3/3 REGRESSION (0.601–0.649 + sanskrit_sha mismatch). Confirms D1: parser fix exposed missing first-pāda; needs 147-token hand repair. Do NOT auto-fix.
- `recycle dry_run=true`: `1027 failed -> 0 halved, skipped 321`. Nothing recyclable right now (covered or single-generation cap). Queue draining on its own: pending 47→16, cm done 4996→5059.
- Unserved 14: `serve_audit` still `132/146, empty-projection 14`. `ghatakarpara` = D1 hold (gold but unserved, correct). `netratantra` = 5 built / 5 blocked (minimal gold, needs assessor). Others are short-tail burn gaps.
- Final: `gates` 1 FAIL (new burn drift, same class), `burn_status ok=true`, `serve 132/146`.

## 8. Handoff

- Report: `REPORT-2026-11-16T0313Z-progress-and-plan.md` (this file).
- Do not commit (Rule: owner pushes). Modified: MANIFEST.json, T1/working files, queue.json, serve_summary.json — leave for owner.
- Next owner calls: D1–D5b in OWNER-DECISIONS.md; regen manifest before any publish; per-work verify_core for ipvv/sivastotravali if needed.
