# WHERE-WE-ARE — read this first (updated 2026-11-14)

*Orientation for any agent landing in `/root/translation-work`. Machine-proposed
throughout. Deep docs: `PROCESS-NOTES-2026-11-14.md` (how to do the work),
`CORE-VALIDATION-2026-11-14.md` (current proof state), `PROVE-EXPOSE.md`
(publish/serve), `skills/proof/SKILL.md` (what a proof is), `MCP.md` (tools).*

## Trika scope freeze (current priority)

1. The 95-work Trika gold corpus is frozen for expansion-sensitive work:
   repair, verify, serve, and human-review it first.
2. The background burn remains T1+L0-only infrastructure and must not create
   new Trika translations, proofs, claims, or external-literature intakes.
3. Non-Muktabodha additions such as Jayadrathayamala remain deferred until all
   95 Trika works are served and their blockers are resolved or explicitly
   assigned to a human owner.
4. No work is “done” when machine-proposed; it is done only after the review
   step its status already requires.

## The goal

Not volume. **The Trika core is the product; proving it and serving it to
ChatGPT correctly is the job.** A bulk lane ("the burn") runs in the
background but is **lower priority than core correctness**.

## What "the burn" is (canonical definition — 2026-11-15)

**BURN = the continuous, unattended bulk lane that produces T1 + L0 only**
— T1 (contract gloss rows, every pada faced) and L0 (per-token morphology +
ranked grounds) — for the whole Muktabodha corpus, using free-tier beam
models, at scale.

- It **stops at L0 on purpose.** It does **not** produce argmap, L2, or C1.
- Those interpretive layers need a **post-hoc, web-researched brief** (written
  *after* the T1/L0 output) and are the **assessor / human lane**.
- A brief is **not required to run the burn**; it is written afterwards, from
  the machine output.
- Batch *triples* (gloss+cm+argmap+L2 in one call) are **deprecated for the
  burn** — they blended shallow argmap/L2 into the corpus and made "assembled"
  look like quality. Triples now survive only as the assessor `layers=full`
  path in `swarm_seed`.
- Runner: `tools/burn_wave.sh` → `tools/auto_burn.py` (seeds `tal_gloss` then
  `tal_cm`); supervised by systemd `tw-wave` (Restart=always).
- Monitor: `shastra.burn_status` (or `python3 tools/burn_status.py`). `ok`
  means **zero pending triples/tal_am**.


## State at a glance

| Thing | Value |
|---|---|
| Trika core | **95 works / 371 songs**; **367 GATE-OK, 4 out-of-scope, 3 REGRESSION** (`verify_core`) |
| The 3 REGRESSIONs | `ghatakarpara/{ghat-p01,p02,p03}` = the documented source-coverage hold, now **tool-detected** (see below) |
| Proof mode | 243/245 classic songs re-proved **shastra**; `sivastotravali/{s10,s12}` held (see below) |
| Proofs (corpus-wide) | ~690 PASS / ~300 BLOCKED (BLOCKED ≈ burn-era backlog) |
| Kularnavatantra | 81/83 gold (p49 blocked on a real T1 duplication; p64 draining) |
| Served to ChatGPT | **132/146 works readable**; 146 projections, 0 stale |
| MCP | **39 tools** on `shastra` (public: https://shastra.svatantrya.net/mcp) |
| Gates | `validate_all --quick` 0 failures; `check.py` CANONICAL; `mcp_smoke` 22/22 |
| Loop | systemd `tal-campaign` (harness) + `tw-wave` (burn) alive |
| Burn (T1+L0) | T1+L0 running; `burn_status.ok` = no pending triples/tal_am |

### Two findings from the 2026-11-15 proof pass (read before reacting to REGRESSIONs)

1. **`proof_record` B3 used `difflib` autojunk (default `True`) — every other
   comparator in the repo passes `autojunk=False`.** autojunk drops tokens that
   occur in >1% of a long string, i.e. it silently discarded real frequent
   Sanskrit (`ca`/`na`/`iti`/…) and tanked alignment on long prose: 7 IPVV
   chunks read 0.079–0.811 instead of **0.993–0.999**. Fixed (proof_record +
   audit_align both). **Monotone-safe**: can only raise a ratio, so no
   previously-PASS song can regress from it. Side-effect: `min_ratio` p10 rose
   0.912 → 0.927 and low-ratio songs 63 → 57.
2. **Ghatakarpara's source span covered HALF of every verse.** `parse_ghata`
   read only the `// Ghk_N //` marker line, dropping the first pāda (the line
   ending in `/` above it) — all 21 verses. The prose hold in
   `emit_scholar.SOURCE_COVERAGE_HOLDS` documented this; the parser is now
   fixed so `source_spans` covers both pādas. **The 3 REGRESSIONs are the
   correct, intended signal**: with complete source, T1 (which still has only
   the second pāda) reads 0.60–0.65 → BLOCKED. `check.py` and
   `validate_all` still read the *stored* PASS, so gates stay green — only
   `verify_core` (the honesty check) flags it. **Not a new defect; a known one
   becoming mechanically visible.** Removing the REGRESSION requires the
   content repair: author ~147 first-pāda tokens into T1+L0, rebuild the
   argmap `sanskrit_sha`, re-trace L2/argmap `l0_ids`, re-proof. That is a
   hand-crafted work unit (AGENTS: one work at a time), queued — **never
   bulk-minted.**

## The one command that tells you the truth

```bash
python3 tools/verify_core.py      # or shastra.verify_core via MCP
```
Re-derives every core proof from current bytes. `GATE-OK` = true; any
`REGRESSION` = a "gold" claim that is false. **Trap:** two proof modes
(shastra = data JSON, classic = MD) — mode is read from each proof's
`lineage`; never force one mode across both.

## Brief quality (2026-11-15)
Briefs are **post-hoc now**: they feed the assessor lane (argmap/L2/C1), not
the burn. All 10 actively-drafting fronts have researched briefs; 110 of 200
remain auto-scaffold. Because the burn is T1+L0 only, an auto-scaffold brief
no longer degrades bulk output — it only matters when a work is taken into
the interpretive lane, and is upgraded before then.

## What\'s genuinely open

1. **Representation: 243/245 unified to shastra** (this session). Two held:
   `sivastotravali/{s10,s12}` — shastra recompute BLOCKED at 0.838/0.886
   while classic reads 0.994/0.997. Root cause is `is_paratext` deleting a
   real token that carries a glued editorial `(?)`, while that work's T1
   stripped only the marker. Two T1 conventions coexist (strip vs drop);
   deciding which is canon is an assessor call — **not** auto-dispositionable.
2. **Ghatakarpara content repair** (the 3 REGRESSIONs): author ~147 first-pāda
   tokens → T1, rebuild L0 + argmap `sanskrit_sha`, re-trace L2/argmap ids,
   re-proof. Hand-crafted, one work at a time.
3. **IPVV: 44/49 songs unwrappable at root** — their `argmap/l2/c1` live in
   `ipvv/chunk*/data/`, not `ipvv/data/`. `data_dir()` resolves them, so
   `verify_core` now covers all 49 (367 GATE-OK). No action needed unless you
   want a flat layout.
4. **4 out-of-scope songs** (not defects): `spanda` later niḥṣyandas, and
   `sivasutra` 76–77 beyond the 75-sutta recension.
5. **T1+L0 tail**: ~197 songs (~4.6k verses) still need gloss/cm; then the
   corpus foundation is complete. Interpretive layers (argmap/L2/C1) are the
   assessor lane, built per work after a post-hoc brief.
6. **Owner lane**: merge PRs #15 (trika-x), #48 (svread), #21 (stale snapshot —
   mainline has everything); L4 voice verdicts; video MCP Access; re-run the
   external audit against `burn/muktabodha` (an audit saw `master`, ~1,000
   commits stale).

### Done this session (2026-11-15)
- **37 Tantraloka source records** + byte-span manifests (all 37 now `audited`,
  **all 37 served** — this alone took Trika serve coverage from 56 → 92 of 95).
- **`ipvv-vivrti-vimarsini` alias resolves to `ipvv`** (`workcfg.resolve_alias`,
  wired into `verify_core` / `serve_audit` / `emit_scholar` + a REGISTRY
  `alias_of` field). No second ledger or projection — immutable_ids stay unique.
- **243 classic proofs re-proved shastra**; `verify_core` clean apart from the
  3 Ghatakarpara hold signals.
- **`proof_record` autojunk fix** (see above).
- **`burn_status` MCP tool + `tools/burn_status.py`**; `validate_all` gained a
  `mcp-smoke` stage (22/22 green).

## Hard rules (carried)

Machine proposes; humans dispose. PASS ≠ scholarly correctness. Never fabricate
Sanskrit to green a gate. Never mass-promote by vote. Scripts assemble/verify,
never author prose. BLOCKED with named `needs[]` is an honest state.
