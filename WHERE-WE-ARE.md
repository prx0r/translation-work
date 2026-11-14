# WHERE-WE-ARE — read this first (updated 2026-11-14)

*Orientation for any agent landing in `/root/translation-work`. Machine-proposed
throughout. Deep docs: `PROCESS-NOTES-2026-11-14.md` (how to do the work),
`CORE-VALIDATION-2026-11-14.md` (current proof state), `PROVE-EXPOSE.md`
(publish/serve), `skills/proof/SKILL.md` (what a proof is), `MCP.md` (tools).*

## The goal

Not volume. **The Trika core is the product; proving it and serving it to
ChatGPT correctly is the job.** The Muktabodha burn runs in the background
(beam loop) but is lower priority than core correctness.

## State at a glance

| Thing | Value |
|---|---|
| Trika core | **95 works / 322 songs**; **318 proved, 4 out-of-scope, 0 defects** (`verify_core`) |
| Proofs (corpus-wide) | ~639 PASS / ~180 BLOCKED (BLOCKED ≈ burn-era backlog) |
| Kularnavatantra | 79/83 gold (p49/p69/p64/p77 draining in the loop) |
| Served to ChatGPT | 92/144 works readable; 112 scholar projections |
| MCP | **37 tools** on `shastra` (public: https://shastra.svatantrya.net/mcp) |
| Gates | `validate_all --quick` 0 failures; `check.py` CANONICAL |
| Loop | systemd `tal-campaign` alive, 3 beam workers, queue ~6.8k pending |

## The one command that tells you the truth

```bash
python3 tools/verify_core.py      # or shastra.verify_core via MCP
```
Re-derives every core proof from current bytes. `GATE-OK` = true; any
`REGRESSION` = a "gold" claim that is false. **Trap:** two proof modes
(shastra = data JSON, classic = MD) — mode is read from each proof's
`lineage`; never force one mode across both.

## What's genuinely open

1. **Representation unification** (design, owner call): 266 classic-mode vs
   552 shastra-mode proofs; some works carry both representations, so proof
   and serving could drift. Pick one canonical side per work.
2. **4 out-of-scope songs** (not defects): `spanda` later niḥṣyandas, and
   `sivasutra` 76–77 beyond the 75-sutta recension.
3. **Burn backlog**: ~180 BLOCKED songs await assessor repair (~400 T1-repair
   verses), netra/svacchanda re-intake, kularnava p49/p69/p64/p77 drain.
4. **Owner lane**: merge PRs #15 (trika-x), #48 (svread), #21 (stale snapshot —
   mainline has everything); L4 voice verdicts; video MCP Access; re-run the
   external audit against `burn/muktabodha` (an audit saw `master`, ~1,000
   commits stale).

## Hard rules (carried)

Machine proposes; humans dispose. PASS ≠ scholarly correctness. Never fabricate
Sanskrit to green a gate. Never mass-promote by vote. Scripts assemble/verify,
never author prose. BLOCKED with named `needs[]` is an honest state.
