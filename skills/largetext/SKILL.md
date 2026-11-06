# SKILL: largetext — the swarm process for huge texts

*Companion law to `skills/crystal-ipvv/SKILL.md`, never a replacement.
crystal-ipvv is the ONLY path to gold. largetext produces machine-proposed
scaffolding that ENTERS the crystal pipeline — recon packets, first-draft
prose, planning briefs — and stops at the assessor's gate. Nothing beam
writes is canonical. Nothing beam writes is PASS. Read crystal-ipvv SKILL.md,
LAYERS.md, FINAL-PROCESS.md, mistakes.md, and SHASTRA-MINIMAL.md first;
this file only adds the swarm layer on top.*

*Why it exists: a 613-verse ahnika or a 49-chunk commentary cannot be
hand-drafted end to end in one session. The swarm drafts volume; the
assessor spends judgment only where judgment lives. Throughput without it:
one ahnika per session. With it: a full TAL-brief batch per half hour,
assessor review ~3 minutes per item.*

## 0. Scope boundary (read twice)

largetext MAY produce: passage briefs (spans/topics/gists), pilot-style
argmap prose, L2-read first drafts, essence first drafts, coverage/gap
reports, citation harvests, validation sweeps.
largetext MUST NEVER produce: canonical `data/*.json`, fork adjudications,
witness citations, PASS verdicts, signoffs, pushes.
Every beam artifact lands in `process/beam/` or `ipvv/cm/beam/` and is
labeled machine-proposed. Promotion into `ipvv/pilot/` or `data/` is an
assessor act (`beam_swarm.py approve` + converter + validators), never a
worker act. Violating this boundary is the same class of sin as mistakes.md
#10 (scripts as authors).

## 1. The cast

- **Beam drafters (N=3–5, nohup, beam-free, $0).** Dumb, fast, obedient.
  They hold no doctrine; they follow packets. One task, one session ID.
- **The assessor (this agent, full knowledge).** Holds the whole text, the
  scholarship, and the gates. Reviews every item, approves or bounces with a
  targeted note, runs converters and proofs, owns every PASS.
- **Deterministic scripts.** Assemble (converters, mergers), never author.
  Pydantic validates SHAPE (schema, spans, markers); only the assessor
  validates MEANING.

## 2. Transmission (the step that makes it work)

Never send beam raw source. Every packet carries a 1-page transmission
brief the assessor writes FIRST (`process/beam/lore/<task>.md`):

1. **Web-search the scholarship** for this exact text (editions, translations,
   witnesses: Torella, Dyczkowski, Gnoli, Sanderson, Bhāskarī…). One focused
   search per front, not per chunk.
2. Distill: **what the text is** (1 para) → **the moves to look for**
   (numbered) → **the traps** (terms that look alike, nearby-but-different
   targets, print damage) → **how to approach** (scope, span rules, what
   honesty looks like here).
3. Brief goes in the packet automatically when present (`beam_pilot.py`,
   `run_tal_brief` both inject it). No brief → expect a bounce cycle;
   10 minutes of searching saves hours of redraft.

Rule: transmission tells beam what the text IS, what to look FOR, and how to
approach it — never what conclusion to reach. A brief that dictates the
inference is fabrication outsourcing. (Benchmark: briefed chunkB draft tracked
T1 faithfully with honest uncertainties; unbriefed TAL windows degenerated to
uniform 8-blocks.)

## 3. Task kinds + gates (mechanical first, meaning last)

| kind | beam writes | pydantic/shape gate | assessor gate |
|---|---|---|---|
| `pilot_pair` (IPVV argmap+L2 prose) | 2 prose files + selfcheck | markers (`**The question:**`, `## 2./3./4.`), ≥2 premises ≥8 words, L2 non-empty | prose review → approve to `ipvv/pilot/` → converter → `validate_song` → `proof_record --shastra` |
| `tal_brief` (ahnika/window spans) | `brief.json` + raw | schema + ≥90% verse coverage + anti-uniformity (no >80% same-length spans) | tiling check + term-grounding grep vs legacy L2 + spot-read gists |

**Window rule (proven 2026-11-06):** tasks over ~60 verses degenerate (lazy
uniform 8-blocks, early stopping at v80, content-free "unavailable"
summaries). Split large texts into ≤60-verse window tasks (`lo`/`hi` args),
one task per window, then stitch. Windowed TAL batches tile at 100% with
topical spans. Never queue a 600-verse ahnika as one task.

Bounce notes must be actionable (span format, missing verses, flabby
question, paraphrase-not-argument). Max 3 attempts, then escalate to
assessor hand-draft. Failed tasks keep their notes as history.

## 4. Calibration (prove the tool before scaling it)

Before scaling ANY new task kind, benchmark beam against gold:

1. Pick a gold item of that kind (Tantrasara-gold for argmaps: tsa-a02-v01;
   IPVV PASS pilot for passage maps: chunkB).
2. Blind draft (withhold the gold), then score: traces resolve · no invented
   cites · fork discipline (no new forks, matches adjudication) · prose bars
   (no certainty labels, no metacommentary) · premise soundness (assessor reads).
3. Record verdict in this skill's log (§6) and BEAM-FLOW.md. Scale only kinds
   that pass; keep the rest manual.

Standing results 2026-11-06: TAL briefs GOOD on small ahnikas (need windows
past ~60 verses); IPVV passage drafts USEFUL FIRST DRAFT (compress 19→~8,
rewrite question); micro-argmaps SURPRISINGLY CLOSE (4/4 traces, equivalent
inference) — untested on forked verses, assumed weak until proven.

## 5. Autonomy loop (how a batch runs while the assessor reviews)

```bash
python3 tools/beam_swarm.py init-queue        # or seed task kind (see §3)
export OPENCODE_GO_KEY="$(agent-vault vault credential get OPENCODE_GO_KEY --vault oracle)"
for w in w1 w2 w3 w4 w5; do
  setsid nohup python3 tools/beam_swarm.py worker $w > process/beam/$w.log 2>&1 < /dev/null &
done; disown -a
# assessor, in parallel:
python3 tools/beam_swarm.py status
python3 tools/beam_swarm.py review <id>       # read draft + selfcheck
python3 tools/beam_swarm.py approve <id>      # or:
python3 tools/beam_swarm.py bounce <id> "fix X"  # worker retries with note
```

Self-healing built in: atomic queue writes, 15-min stale-claim expiry,
per-task session IDs (`ipvv-pilot-<lbl>`, `tal-<ahn>-w<lo>-<hi>`), vault-held
key (never in repo). Workers exit on empty queue; relaunch per batch.
Endpoint: `https://opencode.ai/inference/go/openai/v1/chat/completions`,
model `beam-free`, `reasoning_effort: low` + generous `max_tokens` (the model
burns budget on hidden reasoning — small budgets return null content).

## 6. Gold-standard bar (unchanged — the swarm feeds it, never lowers it)

An item is DONE only when, after assessor promotion: `validate_song`
0 errors · `proof_record --shastra` PASS (or recorded BLOCKED disposition) ·
`check.py` CANONICAL · STATUS/queue updated · everything still labeled
machine-proposed pending human review. Forks are minted by the assessor
with grounds or not at all. AMBIGUOUS is a legitimate terminal state for
genuinely uncertain tokens (SHASTRA-MINIMAL §1: FAILED=0 bar); promoting
uncertainty to PARSED by vote-counting is fabrication — it was tried,
it laundered real errors (`omiti`→'the-manifestation'), it was reverted
(mistakes.md #20).

## 7. Failure log (largetext's own — see mistakes.md #20–22)

- Lax auto-promotion launders errors (reverted 3,044 rows).
- Unbriefed beam degenerates to uniform output (8-block spans).
- Small reasoning budgets return null content (fix: `reasoning_effort: low`).
- Stale claims jam queues after dead workers (fix: 15-min expiry).
- Span-format strictness rejects valid work (fix: normalize `vA-B`→`vvA-B`).
