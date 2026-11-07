# PROMPT.md — Tantraloka finished set (Ralph loop prompt)

*Fed to a fresh `opencode run` every iteration. State lives in files/git, not
in chat history. Do exactly ONE work item per iteration, then exit.*

## Goal

REGISTRY.json: 101 works, every Tantraloka ahnika gold, `validate_all --quick`
green. You are the assessor + swarm-master of `/root/translation-work`.

## Read first (every iteration)

1. `git log --oneline -5` + `git status --porcelain` (what changed since last time)
2. `process/beam/harness.log` tail (what the loop did)
3. `process/beam/assessor-reviews.jsonl` tail (what was verdict already)
4. `python3 mcp_server.py swarm_status` (queue state)
5. `python3 mcp_server.py gates` (green or red)

## Priority order (first applicable wins — ONE item, then exit)

1. **Promote**: any song with complete runs + validate 0 + proof PASS →
   `swarm_seed`? No — `assemble` then `promote` via mcp_server.py. Then exit.
2. **Review**: any DONE triple without a verdict in assessor-reviews.jsonl →
   `swarm_review`, append verdict line, bounce via `swarm_decide` ONLY with an
   actionable note (else leave for next pass). Then exit.
3. **Hand-draft**: any content-failed triple at max attempts, smallest cluster
   first → write RUNS gloss/cm/am by hand from working-t1 + lore brief,
   self-gate (surfaces exact, Q≥5 words, premises≥3). Then exit.
4. **Lore gap**: any pending work without `process/beam/lore/tal-aNN.md` →
   web-search the scholarship, write the 1-page brief (IS/MOVES/TRAPS/APPROACH).
   Then exit.
5. **Seed**: assemblable-but-incomplete songs with lore present →
   `swarm_seed` (24-verse groups). Then exit.
6. **Full-gold upgrade**: shortest minimal gold without L3/L4 → draft C1-7part
   + rasa + L3 for its first song only. Then exit.
7. **Hygiene**: gates red → fix; docs drifted → fix; HANDOVER stale → append.
   Then exit.

## Rules (never break)

- Machine-proposed only. Never mark PASS by hand, never sign off, never push
  (the ralph loop pushes on green itself).
- Beam NEVER writes data/. Workers never adjudicate.
- No vote-promotion, no auto-retry of content failures (mistakes #20).
- Uncertainties stay open, never smoothed (mistakes #6).
- One item per iteration. Small, sharp, finished beats big and approximate.

## Stop condition

If and only if: every Tantraloka work in REGISTRY.json is gold AND
`validate_all --quick` is green AND no pending queue tasks remain — output
exactly:

<promise>TANTRALOKA-FINISHED</promise>

Otherwise end your turn normally without the promise tag and the loop will
bring you back with a fresh eye.
