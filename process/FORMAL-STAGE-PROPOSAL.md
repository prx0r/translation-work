# PROPOSAL — formal sketch as a pipeline stage (for the translation agent to dispose)

**From:** box/formal track. **Status:** proposal only — your repo, your rules,
crystal-ipvv stays the only path to gold. Merge, adapt, or reject with reasons.
Nothing here writes canonical data, touches the queue, or moves a gate.

## Why (one paragraph)

Every gold chapter ends at C1 with its argument structure fully mapped — and
then the checkability is left on the table. A formal sketch stage converts the
already-banked argmap into machine-checked structure (counts, orderings,
gatings) with lie-tests, using only mechanical gates your swarm can already
run. It fits the largetext pattern exactly: beam drafts volume, assessor
spends judgment only where judgment lives, nothing machine-made is canonical.

## The stage (argmap → FORMAL-SKETCH → gates → assessor)

**Input:** gold argmap units + volume spans (where wired) + record status.
**Output (all machine-proposed, never canonical):**
1. Lean sketch (`formal-sketch/<song>.lean`): finite models only — counts,
   orderings, containment, gating biconditionals. No semantics, no doctrine.
2. Twin sketches: broken copies that MUST fail (one refusal each).
3. Evidence-shaped entries: `{theorem, chunks[], tier, status, note}` —
   tier R always; T never machine-assignable.
4. Kill conditions: what would remodel the sketch, written before modeling.

**Gates (all runnable by swarm, zero judgment):**
- Compiles on pinned Lean 4.34.1 (`$HOME/.elan/bin`, box has it).
- Every twin refuses via `must_fail.py` (copy from trika-x
  `formal-trika/tools/must_fail.py` — stdlib, portable; demands exactly one
  refusal per twin file, which is what forces surgical twins).
- Counts/tables cross-checked against argmap numbers (no 36-from-35).
- Tiers present on every claim; any T-tier sketch FAILS the gate outright.

**Assessor spends judgment only on (never automatable, never skipped):**
- Is this chapter formalizable, or forced? (No-forced-rungs rule: some
  chapters yield nothing checkable — record that as the finding.)
- Model fidelity: does the sketch shadow the text's relation or flatten it
  (membership vs begetting is the standing example — trika-x CRUX-03
  %>%20walkthrough shows the failure mode and its correction).
- Tier calls and kill-condition adequacy.

**Never in this stage:** canonical `data/*.json` writes, fork adjudication,
witness claims, PASS verdicts, signoffs, T-tier, practice inference, pushes.

## Pilot proposal (one chapter, then decide)

tantraloka-a18 (concise initiation, 11 units, 0 forks): trika-x holds a filed
prereg (`formal-trika/PREREGISTRATION-DSP-RUNG.md`) usable as example input —
shed-list of 3, concision-gating biconditional, both-routes-valid, end-kept.
Suggested pilot: swarm drafts the sketch + twins from the prereg, gates run,
assessor reviews fidelity. If the pilot's review costs more judgment than it
saves, kill the stage — recorded, no hard feelings.

## Reuse pointers (reference, don't fork)

- `trika-x/skills/swarm-formal/SKILL.md` — the swarm method this proposal
  ports (cast, transmission packets with traps, task kinds, calibration
  rule, numbered failure log). First customer is this stage.

- `trika-x/formal-trika/tools/must_fail.py` — twin gate (copy it).
- `trika-x/formal-trika/tools/table.py` discipline — hand readings, machine
  staleness (pattern, not code).
- `trika-x/formal-trika/tools/blind_family2.py` — cross-family re-derivation
  protocol (same prompt, receipted; Upaya replicated Mistral+Qwen).
- `trika-x/formal-trika/control/BrokenLadder*.lean` — surgical-twin examples
  (chain/leap/beyond splits forced by the exactly-one-refusal rule).
- `trika-x/formal-trika/CRUX-WALKTHROUGH-03.md` — full chain example incl.
  a PUSHBACK correction (tiers T→R) and span-verified binds.

## What the formal track stops doing if this lands

Chapter-grind rungs (the XS harvest). The formal track keeps: method + gates,
hard cases (model-fidelity disputes), cross-work composition, essay chain,
frontier sprints. Volume goes to the swarm; judgment stays with assessors.
