# LARGETEXT EXAMPLES — good/bad exhibits from live swarm runs, 2026-11-06

*Companion to `SKILL.md`. Every exhibit is verbatim from this repo's runs
(file + task ID given). GOOD = approved; BAD = bounced or reverted, with the
fix that actually worked.*

---

## Briefs (tal_brief)

**GOOD** (`process/beam/runs/tal-a12-brief/brief.json`, approved):
spans vv1-3 / vv4-5 / vv6-8 / vv9-13 / vv14-17 / vv18-22 / vv23-26 — 7 spans,
lengths {3,2,5,2,4}, all 26 verses covered, topics follow the argument
(worship-as-absorption → no-material-rule → tremor/doubt → praise).
*Why good: boundaries sit on topic shifts; every legacy-L2 term used
(absorption, kampa, dream, doubt) greps clean in `tantraloka-a12/L2-tal-a12.md`.*

**BAD** (tal-a06 window batch, bounced — mechanical uniformity):
32 spans, 31 of length exactly 8 (`vv1-8 … vv249-256`).
*Why bad: beam chunked blindly instead of reading. No topic drove any
boundary. Fix that worked: windowed tasks (≤60 verses) + explicit
"NEVER emit uniform blocks" + variety gate (>80% same-length = fail).*

**BAD** (tal-a03-w*, bounced — content-free):
37 spans all titled "Ahnika 3 summary unavailable".
*Why bad: the first packet carried no source (recon-stage ahnikas lack
`SOURCE.txt`). Beam honestly reported emptiness instead of inventing —
correct behavior, wrong packet. Fix that worked: build packets from
`workcfg.source_spans` (real GRETIL verse text), legacy L2 as secondary.*

**BAD** (format): spans `p01…p16`, or `v181-183` (single-v prefix).
*Fix that worked: validator normalizes `vA-B`→`vvA-B`; non-`vv` schemes fail
with the format spelled out. Never silently accept — bounce with the shape.*

---

## Passage argmaps (pilot_pair)

**GOOD-enough** (chunkB benchmark vs pilot gold):
beam drafted 19 premises tracking T1 faithfully, uncertainties honest
(truncation noted, garbled glosses flagged, missing Gītā development admitted).
Needed assessor redraft: question rewritten (beam's was meta — "what argument
does this passage make about…" — gold asks the passage's own question),
premises compressed 19→~8, paraphrase cut.
*Lesson: beam covers; the assessor sharpens. Budget review accordingly.*

**GOOD** (tsa-a02-v01 micro-argmap vs Tantrasara gold):
question equivalent, premises same content, inference equivalent, traces 4/4
identical, no invented cites. Untested on forked verses — do not generalize.

---

## Anti-patterns (reverted, never repeat)

**Lax promotion** (`tools/shastra_deambig.py` v1): prose-overlap + vote-count
promotion flipped 3,044 AMBIGUOUS→PARSED, including `omiti`→'the-manifestation'
and `apekṣāyā`→'not-verily' via repeated wrong votes. Caught by spot-read,
reverted in full. Survivor rule: unanimous-x3+-with-zero-dissent or
closed-class only (22 kept). *A vote is not evidence; agreement can be shared error.*

**Null content** (`finish=length`, empty message): beam burns the token budget
on hidden reasoning. Fix: `reasoning_effort: low` + large `max_tokens`.
Small budgets fail deterministically, not intermittently — do not retry-loop them.

**Stale claims**: dead workers (killed tool shells) left `claimed` tasks no
worker would touch. Fix: 15-min claim expiry + re-drive (see `claimable()`).
