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

**Size routing (argmaps, benchmarked 2026-11-06):** beam drafts earn their
keep on LONG passages (V3B, 5862 tokens: 19 premises, faithful coverage the
assessor compresses to ~8 — the draft is a guided tour worth more than the
read time). On SHORT verses (tsa-a02-v01, 4 tokens) the assessor writes
directly — reviewing costs more than drafting. Rule of thumb: <1k tokens of
source, write it; >1k, beam drafts first, assessor redacts. Never the reverse.

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

**THE BUTTON: `tools/continue.sh`.** One command syncs the openpatala registry
(`tools/registry_sync.py` → `process/beam/PLAN.json`, tier-ordered: Trika
core first, untranslated before polish, shortest-first, mystics deferred),
seeds swarmable tasks, ensures workers + ralph are alive, runs one supervised
pass (`once`) or loops (`continue.sh` with no args supervises ralph
indefinitely). Press it, walk away; the review queue is waiting on return.

```bash
bash tools/continue.sh once   # single supervised pass
setsid nohup bash tools/continue.sh > process/beam/continue.log 2>&1 < /dev/null &  # leave it
```

**Leave-it-running mode: `tools/ralph.sh`.** The autonomous supervisor —
keeps 5 workers alive, runs `auto-review` (window briefs ONLY, never prose
pilots), converts due approved pilots (`tools/ralph_convert.py`), gates every
commit on `check.py`, pushes on green, parks on red, exits drained with the
review queue for the assessor:

```bash
setsid nohup bash tools/ralph.sh 240 180 > process/beam/ralph.log 2>&1 < /dev/null &
```

`auto-review` re-verifies each DONE window brief from disk (tiling 100% +
variety + schema) before approving; anything else is HELD for assessor eyes.
Full-ahnika briefs, pilot prose, fork calls, PASS calls: never automated.

**Ralph-loop canon alignment.** This is Huntley's loop with one adaptation:
the completion promise is per-task and mechanical (validators green +
selfcheck green = `<promise>DONE</promise>` equivalent); workers are
stateless per task (fresh context every claim — no compaction drift);
learnings compound into mistakes.md + this skill (the AGENT.md rule).
The adaptation: meaning-judgment has no mechanical proxy, so the promise
covers SHAPE only — the assessor holds the MEANING gate, batched, on wake.
A loop that auto-approved meaning would converge to plausible mush (proven:
uniform briefs passed pydantic; vote-counting laundered errors).

**Beam-led lore (query proposal).** Beam cannot browse, but it can say what
it needs: `lore_queries` tasks have beam propose 2-6 scholarship searches
per front → assessor executes them (one search round) → `lore_distill`
drafts the brief from excerpts → assessor reviews into `process/beam/lore/`.
Legwork to beam, sources to the assessor, judgment stays human-side.

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

## 8. The two roles (formal)

**DUMB (beam-free or any free model): cheapest that can still follow a packet.**
Drafts prose, fills JSON schemas, tiles spans. Stateless per task, no memory,
no tools, no judgment. Allowed: structure, coverage, first-draft reasoning.
Forbidden: canon, adjudication, witnesses, PASS, signoff, push. When it
fails, it fails mechanically (format, coverage, uniformity) — fix the packet,
not the model.

**SMART (the assessor session): judge, web-searcher, organiser.**
Holds the whole text + scholarship. Writes transmission briefs (web search
first), reviews every draft (spot-read + gates), adjudicates forks, runs
converters + proofs, owns PASS, curates this skill. Irreplaceable because
meaning has no mechanical proxy (uniform briefs passed pydantic; vote-counts
laundered errors). The day a model can be trusted with fork adjudication it
will have proven it against Tantrasara gold — not before.

Rule of staffing: DUMB scales horizontally (3–5 workers, free). SMART scales
by batching (review queues, never one-offs). Never trade one for the other.

## 9. Endgame: pointing this at a new big text (Gita pattern)

0. **DB first.** `tools/dbread.py coverage <tw-dir>` against the portable box
   (`DB-BACKBONE.md`) tells you what exists and what's missing before any
   drafting. Intake registers spans in workcfg; the DB stays the identity
   spine (read-only — this skill never writes it).

1. `recon` task: marker census + structure hypothesis of the source file.
   Assessor verifies (known structure: 18 adhyāyas / ~700 Gītā verses +
   Abhinavagupta's commentary + colophons) → workcfg intake registration.
2. `lore_queries` → assessor searches → `lore_distill` → approved brief
   in `process/beam/lore/` (Torella IPK frame, Sharma/Supersite collation for
   the 5 LIVE Gītā forks per handover).
3. T1+L0 via charfill + hand pattern (Ghand2 ledger), same as IPVV 49/49.
4. `pilot_pair` per adhyāya (a01 = 48-unit pilot first) → converter →
   validate → proof. `tal_brief`-style windows only if an adhyāya exceeds
   ~60 verses of commentary span.
5. Gold-standard bar (§6) unchanged. Nothing in this pipeline marks COMPLETE;
   REGISTRY tracks gold, never the swarm.

## 10. Formalisation: hashes, one gate, Lean-compat (2026-11-06)

The swarm is only half the machine. The other half makes every output
content-addressed, singly-gated, and consumable by the Lean formal lane:

- **Manifest** (`tools/manifest.py gen|check`): sha256 of every canonical
  file (per-work `data/*.json`, `T1*.md`, `STATUS.json`, `passages.jsonl`,
  `GATE.json`, `cm/*_G*.py` authoring tables, root pinned docs) into
  `MANIFEST.json` with the git rev. Consumers (bridge snapshot, Lean
  EVIDENCE, ralph commits) pin bytes, not vibes. Drift = fail.
- **One gate** (`tools/validate_all.py [--quick]`): schemas → manifest
  freshness → per-song `validate_song` across ALL data songs → proof sweep
  (PASS, or BLOCKED only with a recorded `proof/<song>.disp.json`
  disposition — unrecorded BLOCKED fails) → `check.py` CANONICAL →
  `dbread coverage` (warn-only). Exit 0 = shippable. ralph.sh gates commits
  on `--quick`; full runs happen on assessor wake and before pushes.
- **Lean-compat contract** (translation-work side): stable locators +
  `immutable_id` in every work's `passages.jsonl` (what `evidence_check.py`
  resolves); `layer_sha256` in every proof record; MANIFEST rev pinned by
  downstream. We never write Lean or EVIDENCE entries — trika-x owns those;
  we guarantee the bytes they point at.
- **Lesson that built this** (mistakes.md #23): the B3 align gate compared
  T1 surfaces against RAW source including paratext the contract excludes —
  7 byte-perfect chunks BLOCKED at 0.076–0.796. The proxy measured the wrong
  thing. Fixed (`is_paratext` filter), all flipped to PASS. When a gate
  fails on clean data, interrogate the gate before the data.

## 11. Porting the loop to factories (video / books / socials)

The pattern is lane-agnostic; the gates are lane-specific. Full contract:
`REGISTRY-FEDERATION.md`. Rules for porting:

1. The factory keeps its gate (`check.py`, contract suites, runtime law).
   The swarm only feeds drafts + planning inputs. Never the reverse.
2. Queue from the openpatala registry: unrendered series units, unbuilt
   book entries, unscheduled drafts — ranked, shortest-first, deferred
   categories explicit (mystics, sourceless works, owner-gated cutovers).
3. Beam drafts prose/assets ONLY: glossary entries, headnotes, post copy
   variants. Never timing/cues, never ISBNs, never rights statements,
   never sends/spends. A draft that invents an identifier is rejected,
   not fixed.
4. Deterministic assemblers stay the factory's own (builders, factory.py,
   runtime). Validators stay the factory's own. The assessor role transfers
   to the lane owner on their wake cycle — same batched review, same
   approve/bounce, same machine-proposed labels.
5. Asset identity is `openpatala_work_id` everywhere (`dbread ids` resolves
   it). Missing/UNRESOLVED/TBD = draft-only, in every lane, no exceptions.

## 12. Approved trika-x references (read-only, never authority)

trika-x is another lane's repo — translation-work READS, never writes. Two
artifacts are cleared for use as *pointers*, never as grounds:

- **EVIDENCE.json entries** (theorem → chunk locators + tier + note, e.g.
  `tsa08-p02` = mala doctrine). Use for (a) prioritization — chunks pinned
  by formal interest translate first within their tier; (b) lore-brief
  topics. Never as gloss grounds: a formal claim about a chunk is not a
  reading of its Sanskrit. Cite the entry, then verify against T1/L0.
- **vocab.py term list** (pramātṛ, kañcuka, mala…) as a *consistency
  checklist* for key-term glosses across chunks (same term → same English
  unless the passage forces otherwise, flagged in grounds). Formal
  stipulation ≠ philology: on conflict, the text wins and the deviation is
  recorded — exactly like a fork.

Forbidden: copying doctrine into argmaps, citing theorems as witness, letting
formal categories rename what the verse says. BLIND.md's rule cuts both ways.

## 13. Agent keys (the brief is the unlock, C1 stays the reader's)

The transmission brief is a *decode key for the machine*, not a reader's
essay. C1 is untouched: it states the matters for humans, with rasa, under
the crystal-ipvv bars. Do not merge them.

Key contract (per front, `process/beam/lore/<front>.md`):
1. what the text IS (position in the arc, base edition/scholarship)
2. numbered MOVES (the argument's order)
3. TRAPS (lookalike terms, nearby-but-different targets, print damage,
   genuine textual variants to record rather than smooth)
4. APPROACH (scope rules, span discipline, honesty rules)

Keys are written by the assessor from web scholarship, cached per front, and
auto-injected. Writing them IS the high-value work: 10 min of search +
distillation buys hours of usable beam output. A future C1-esque "terse key"
layer may formalize these as data — if so it is an ADDITIVE layer beside C1,
never a replacement, and it never carries reader-facing prose.
