# WHERE-WE-ARE — read this first (updated 2026-11-14)

*Orientation for any agent landing in `/root/translation-work`. Machine-proposed
throughout. Deep docs: `PROCESS-NOTES-2026-11-14.md` (how to do the work),
`CORE-VALIDATION-2026-11-14.md` (current proof state), `PROVE-EXPOSE.md`
(publish/serve), `skills/proof/SKILL.md` (what a proof is), `MCP.md` (tools).*

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
| Trika core | **95 works / 322 songs**; **318 proved, 4 out-of-scope, 0 defects** (`verify_core`) |
| Proofs (corpus-wide) | ~639 PASS / ~180 BLOCKED (BLOCKED ≈ burn-era backlog) |
| Kularnavatantra | 79/83 gold (p49/p69/p64/p77 draining in the loop) |
| Served to ChatGPT | 92/144 works readable; 112 scholar projections |
| MCP | **37 tools** on `shastra` (public: https://shastra.svatantrya.net/mcp) |
| Gates | `validate_all --quick` 0 failures; `check.py` CANONICAL |
| Loop | systemd `tal-campaign` (harness) + `tw-wave` (burn) alive |
| Burn (T1+L0) | **~97% of Muktabodha glossed** (162k/167k verses); ~197 songs left |

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

1. **Representation unification** (design, owner call): 266 classic-mode vs
   552 shastra-mode proofs; some works carry both representations, so proof
   and serving could drift. Pick one canonical side per work.
2. **4 out-of-scope songs** (not defects): `spanda` later niḥṣyandas, and
   `sivasutra` 76–77 beyond the 75-sutta recension.
3. **T1+L0 tail**: ~197 songs (~4.6k verses) still need gloss/cm; then the
   corpus foundation is complete. Interpretive layers (argmap/L2/C1) are the
   assessor lane, built per work after a post-hoc brief.
4. **Owner lane**: merge PRs #15 (trika-x), #48 (svread), #21 (stale snapshot —
   mainline has everything); L4 voice verdicts; video MCP Access; re-run the
   external audit against `burn/muktabodha` (an audit saw `master`, ~1,000
   commits stale).

## Hard rules (carried)

Machine proposes; humans dispose. PASS ≠ scholarly correctness. Never fabricate
Sanskrit to green a gate. Never mass-promote by vote. Scripts assemble/verify,
never author prose. BLOCKED with named `needs[]` is an honest state.
