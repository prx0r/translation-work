# GLOSS-BACKLOG — T1 gloss tasks exhausted on CONTENT failures (not retryable)

*2026-11-15. Every task below hit `max_attempts` for a **content** reason —
re-running with the same packet would fail again. Per mistakes.md #20 (the
3,044-row lesson) these **escalate to the hand-draft / packet-fix lane**; they
are never auto-retried and never vote-promoted. This file exists so they are not
silently lost when the queue drains.*

## Why they failed (classification of all 200 tasks)

| class | count | what the beam did |
|---|---|---|
| `gloss-format (schema)` | 76 | glosses carry banned grammatical labels / over-hyphenated segments, e.g. `genitive-use`, `causative-meaning-there`, `support-power-loc-dual` — barred by the T1 selfcheck (hyphen-count + grammar-word list) |
| `surface-drift` | 124 | emitted Sanskrit surfaces that do not match the source tokens, e.g. `aparakāśo` vs source `aprakāśo` |

Not transport/429: those are the retryable class and were already recycled.

## The 8 blocked songs (8 × 25 = 200 tasks)

| work | song | failed | gloss-format | surface-drift |
|---|---|---|---|---|
| `mukta-m00521` | `mukta-m0-p359` | 25 | 9 | 16 |
| `mukta-m00521` | `mukta-m0-p362` | 25 | 16 | 9 |
| `mukta-m00521` | `mukta-m0-p392` | 25 | 12 | 13 |
| `mukta-m00521` | `mukta-m0-p402` | 25 | 12 | 13 |
| `mukta-m00521` | `mukta-m0-p407` | 25 | 8 | 17 |
| `mukta-m00521` | `mukta-m0-p412` | 25 | 8 | 17 |
| `mukta-m00521` | `mukta-m0-p435` | 25 | 9 | 16 |
| `mukta-m00195` | `mukta-m0-p470` | 25 | 22 | 3 |

These are **attempts-exhausted**, so `stage_seed` will not re-create them (it
skips ids already present in the queue regardless of status) — which is correct:
they need a changed packet or a human, not another identical try.

## How to clear one (in order of preference)

1. **Fix the packet, then retest.** `python3 tools/beam_swarm.py retest <task-id>`
   mints a fresh id with attempts reset (ceiling 3 total). Do this ONLY after
   changing something real — a stricter gloss-format note in the prompt, a
   smaller window, or an enriched brief. Retesting unchanged input is the
   forbidden loop.
2. **Hand-draft.** `tools/review_inbox.py verse <work> <n>` to see source +
   existing layers, then author the gloss rows. 8 songs × 25 verses is the
   expected cost.
3. **Supersede** if the work is out of scope:
   `python3 tools/beam_swarm.py supersede <task-id> <why>`.

## Related

- `HAND-DRAFT-MVV` precedent: `process/beam/hand-draft-mvv-backlog.md`.
- Failure-class telemetry: `shastra.health` / `tools/watchdog_progress.py`
  (`question rejected`, `premise too short`, `l2 too short`, `surface drift`,
  `schema fail`).
- Retest policy: `MCP.md` §6 troubleshooting, "Driver spins, seeds 0…" row.
