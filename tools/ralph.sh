#!/bin/bash
# RALPH — autonomous swarm supervisor + assessor-batch machine.
# Safe to run, kill, and re-run: workers self-heal. PASS and publishing are
# never automated. Judgment stays queued for the
# assessor (pilot prose review, fork calls, signoff).
#
# Usage: setsid nohup bash tools/ralph.sh [max_iter] [sleep_secs] > process/beam/ralph.log 2>&1 < /dev/null &
# Defaults: 240 iterations x 180s ≈ 12h. Exits early when fully drained.
set -u
cd /root/translation-work || exit 1
export OPENCODE_GO_KEY="$(agent-vault vault credential get OPENCODE_GO_KEY --vault oracle)"
MAX_ITER=${1:-240}
SLEEP_SECS=${2:-180}
# Worker count: space-separated w-slots, MAX 3. Staggered: pass 1 starts w1 only,
# pass 2 adds w2, pass 3 adds w3 (user directive: start ONE, get it working, add up).
RALPH_WORKERS=${RALPH_WORKERS:-"w1 w2 w3"}
# Smart-beam reviewer competes with drafters for the free-tier quota. Off by
# default; set RALPH_BEAM_REVIEW=1 to enable (assessor reviews by hand otherwise).
RALPH_BEAM_REVIEW=${RALPH_BEAM_REVIEW:-0}

log() { echo "[ralph $(date -u +%FT%TZ)] $*"; }
log "start max_iter=$MAX_ITER sleep=$SLEEP_SECS"

for ((i = 1; i <= MAX_ITER; i++)); do
  log "--- pass $i ---"

  # 0. manifest freshness is a gate input — regen when canon changed, else
  # every content commit parks the next pass on a stale manifest.
  if [ -n "$(git status --porcelain | grep -v -E 'process/beam/(queue|claims|w[0-9]\.log|ralph\.log|continue\.log)|ipvv/cm/beam/')" ]; then
    python3 tools/manifest.py gen >/dev/null 2>&1 && log "manifest regenerated" || log "manifest gen FAILED — needs assessor"
  fi

  # 1. supervise beam drafters — STAGGERED: allow at most $i slots on pass $i,
  # capped at 3. So pass 1 = w1, pass 2 = w1+w2, pass 3+ = all three.
  SLOTS=0
  for w in $RALPH_WORKERS; do
    SLOTS=$((SLOTS+1))
    [ "$SLOTS" -gt 3 ] && break
    [ "$SLOTS" -gt "$i" ] && continue
    if ! pgrep -f "beam_swarm.py worker $w" >/dev/null 2>&1; then
      setsid nohup python3 tools/beam_swarm.py worker "$w" > "process/beam/$w.log" 2>&1 < /dev/null &
      log "restarted worker $w (slot $SLOTS, pass $i)"
    fi
  done

  # 2. assessor-batch: auto-approve gate-verified window briefs (never prose pilots)
  python3 tools/beam_swarm.py auto-review 2>&1 | while IFS= read -r l; do log "auto-review: $l"; done

  # 2b. assessor daemon: verdict new dones, escalate content-failures, seed
  # lore_queries for unbriefed fronts. Read-only + queue seeds + log only.
  python3 tools/assessor_sweep.py 2>&1 | while IFS= read -r l; do log "assessor-sweep: $l"; done

  # 2c. smart-beam reviewer (1/pass max, instant backoff on 429): checklist
  # verdicts on newest unreviewed dones. Bounce-only on mechanical fails;
  # NEVER approves prose (auto-review covers briefs, humans cover meaning).
  if [ "$RALPH_BEAM_REVIEW" = "1" ]; then
    timeout 240 python3 tools/beam_review.py --sweep --max 1 --apply 2>&1 | while IFS= read -r l; do log "beam-review: $l"; done
  fi

  # Conversion, proof, PASS, commit and push remain with the owner.
  log "machine-proposed work awaits owner review; no automatic conversion or publishing"
  if python3 tools/validate_all.py --quick >/dev/null 2>&1; then
    log "quick gate green (not a proof or publication approval)"
  else
    log "quick gate red — needs assessor"
  fi

  # 5. drained? (no pending/claimed worker tasks, no due conversions)
  PENDING=$(python3 -c "import json; q=json.load(open('process/beam/queue.json')); print(sum(1 for t in q if t['status'] in ('pending','claimed')))" 2>/dev/null || echo 1)
  log "queue pending/claimed=$PENDING"
  if [ "$PENDING" = "0" ]; then
    log "DRAINED — parking. Review queue: pilot prose + BLOCKEDs + owner items."
    break
  fi
  sleep "$SLEEP_SECS"
done
log "ralph exit"
