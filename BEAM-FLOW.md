# BEAM-FLOW — cheap beam-free drafters + assessor gate quality

*Authoritative spec: `skills/largetext/SKILL.md` (+ `EXAMPLES.md`, mistakes.md
#20–22). This file is the operator's runbook; the skill is the law.*

*2026-11-06. Status: SPEC + WORKING (swarm live). All beam output is
machine-proposed. Beam NEVER writes canonical `data/`, NEVER marks PASS.
Only the assessor (Muse Spark session) promotes.*

## 0. The shape (3 drafters → 1 checker)

```
beam w1..wN (nohup, beam-free, $0)      assessor (this session, quality)
  pull task from process/beam/queue.json
  draft PROSE ONLY ──parse/shape──►       review: structure, traces, honesty
  pydantic self-check                       approve → ipvv/pilot/ (argmaps)
  park in cm/beam/ or process/beam/runs/    bounce → note → worker retries
                                            promote: converter + validate + proof
```

Deterministic scripts assemble (converters, mergers); validators judge
(`validate_song`, `proof_record --shastra`, `check.py`); beam reasons in
prose; the assessor decides. That split is the whole trick.

## 0a. Transmission briefs (scholarship in, quality out)

Beam drafts from T1+L0 alone are competent but blunt (benchmark: 19 premises
where 8 would do, flabby question). The fix is the transmission pattern:
**the assessor web-searches scholarship, distills a 1-page brief (what the
text is, the moves, the traps, how to approach), and the packet carries it.**
Briefs live in `process/beam/lore/` (`ipvv-<LABEL>.md`, `tal-<ahn>.md`) and
are injected automatically when present. Seeded: `ipvv-V3B.md` (Torella
IPK/kriyā frame, Bhāskarī witness note), `tal-a15.md` (phonematic emanation,
Jayaratha joints, anti-uniform-chunking rule). Write one per front before
queueing its tasks — 10 minutes of searching saves hours of bounce cycles.

## 1. Setup (once per machine)

```bash
# key lives in vault, never in repo
agent-vault vault credential set "OPENCODE_GO_KEY=<oc_sk_...>" --vault oracle
export OPENCODE_GO_KEY="$(agent-vault vault credential get OPENCODE_GO_KEY --vault oracle)"
python3 tools/beam_swarm.py init-queue
for w in w1 w2 w3 w4 w5; do
  setsid nohup python3 tools/beam_swarm.py worker $w > process/beam/$w.log 2>&1 < /dev/null &
done; disown -a
```

Endpoint: `https://opencode.ai/inference/go/openai/v1/chat/completions`,
model `beam-free`, OpenAI-compatible. Required headers (already in
`tools/beam_client.py`): own `User-Agent: translation-work-harness/1.0` +
stable `x-opencode-session` per conversation. Beam-free = free, unlimited,
limited time + limited regions (not ZDR — 30-day retention; never send keys).

## 2. Operating

```bash
python3 tools/beam_swarm.py status          # queue at a glance
python3 tools/beam_swarm.py review <id>     # read draft + selfcheck
python3 tools/beam_swarm.py approve <id>    # pilot_pair: place into ipvv/pilot/
python3 tools/beam_swarm.py bounce <id> "note"  # back to queue with fix order
# then, assessor side:
python3 tools/shastra_convert_chunk.py --song S --verse N --v1 <rows> --layers-only
python3 tools/validate_song.py --song S --work ipvv
python3 tools/proof_record.py --song S --work ipvv --shastra
```

Queue mechanics: atomic claims (`O_EXCL` + 15-min stale-claim expiry, so dead
workers self-heal), `max_attempts: 3` then escalate to assessor. Workers poll,
exit when empty — relaunch per batch. Logs: `process/beam/wN.log`.

## 3. What beam is FOR vs NOT FOR (benchmarked 2026-11-06)

Benchmark: blind drafts vs gold — tsa-a02-v01 (full-stack micro-verse) and
chunkB passage (IPVV minimal), scored by the assessor.

| Task | Verdict |
|---|---|
| TAL passage briefs (spans/topics/gists) | **GOOD** — a18 (3 spans), a12 (7 spans): complete tiling, terms ground to legacy L2. Direct transform input. |
| IPVV passage-argmap prose (question/premises/inference) | **USEFUL FIRST DRAFT** — chunkB: 19 premises faithful to T1 (beats the 3-premise pilot on coverage) but flabby question, paraphrase mixed with argument. Needs assessor redraft (question rewrite, compress to ~8). |
| Full-stack micro-verse argmap (traces + adjudication) | **SURPRISINGLY CLOSE** on easy verses (tsa-a02-v01 matched gold traces 4/4, equivalent inference). Untested on forked verses. |
| Fork adjudication, lore grounding, PASS calls | **NOT FOR BEAM** — stays manual. Beam must never mint forks or cite witnesses. |
| Canonical JSON, data/ writes, signoff | **NEVER** — converters assemble, assessor promotes. |

Rule of thumb: **beam narrates, scripts assemble, assessor judges.**
IPVV argmaps are NOT too manual for beam — but only as first-draft prose,
never as final argument. The manual core (question sharpness, premise
compression, fork calls) is the assessor's 10 minutes per chunk, not beam's.

## 4. Scaling (this is the IPVV-finish / TAL engine)

- IPVV: pilots exist for 43/44 chunks → converter sweep is deterministic
  (assessor batch). Beam handles V3B (missing pair) + all BOUNCE redrafts.
- TAL: 18 briefs queued → briefs become transform packets alongside legacy
  L2/SOURCE. Beam drafts, assessor transforms (emit_tal path), gates decide.
- Workers 3–5; free tier unlimited — throttle by politeness (2s spacing),
  not budget. Distinct session IDs per task (`ipvv-pilot-<lbl>`,
  `tal-brief-<ahn>`); one conversation per task for prompt caching.
- Throughput observed: brief ~2 min/worker; V3B-size prose ~5–10 min.
  5 workers ≈ a full TAL-brief batch per half hour.

## 5. Failure modes seen (and fixed)

- `finish=length` + empty content on huge packets → cap T1 excerpt, raise
  `max_tokens`, retry (beam_client handles).
- Non-atomic queue.json → partial-read crashes → atomic `os.replace` + retrying load.
- Stale `claimed` after dead workers → 15-min expiry + re-drive.
- Lax auto-promotion launders errors (deambig incident: `omiti`→'the-manifestation'
  via repeated votes) → unanimous-x3+/closed-class rule only; bulk promotion
  of uncertain rows is FORBIDDEN. AMBIGUOUS stays until genuinely resolved.

## 6. Definition of done (per chunk/ahnika)

Draft exists → selfcheck green → assessor review → (approve|bounce×N) →
converter → `validate_song` 0 errors → `proof_record --shastra` PASS/BLOCKED⁺ →
STATUS/queue updated → nothing pushed by workers, ever.
⁺BLOCKED with recorded disposition is a finished state; faked PASS is dismissal.
