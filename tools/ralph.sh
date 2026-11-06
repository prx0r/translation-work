#!/bin/bash
# RALPH — autonomous swarm supervisor + assessor-batch machine.
# Safe to run, kill, and re-run: every step is idempotent, nothing marks
# PASS without validators, workers self-heal. Judgment stays queued for the
# assessor (pilot prose review, fork calls, signoff).
#
# Usage: setsid nohup bash tools/ralph.sh [max_iter] [sleep_secs] > process/beam/ralph.log 2>&1 < /dev/null &
# Defaults: 240 iterations x 180s ≈ 12h. Exits early when fully drained.
set -u
cd /root/translation-work || exit 1
export OPENCODE_GO_KEY="$(agent-vault vault credential get OPENCODE_GO_KEY --vault oracle)"
MAX_ITER=${1:-240}
SLEEP_SECS=${2:-180}

log() { echo "[ralph $(date -u +%FT%TZ)] $*"; }
log "start max_iter=$MAX_ITER sleep=$SLEEP_SECS"

for ((i = 1; i <= MAX_ITER; i++)); do
  log "--- pass $i ---"

  # 0. manifest freshness is a gate input — regen when canon changed, else
  # every content commit parks the next pass on a stale manifest.
  if [ -n "$(git status --porcelain | grep -v -E 'process/beam/(queue|claims|w[0-9]\.log|ralph\.log|continue\.log)|ipvv/cm/beam/')" ]; then
    python3 tools/manifest.py gen >/dev/null 2>&1 && log "manifest regenerated" || log "manifest gen FAILED — needs assessor"
  fi

  # 1. supervise beam drafters (restart dead, keep 5)
  for w in w1 w2 w3 w4 w5; do
    if ! pgrep -f "beam_swarm.py worker $w" >/dev/null 2>&1; then
      setsid nohup python3 tools/beam_swarm.py worker "$w" > "process/beam/$w.log" 2>&1 < /dev/null &
      log "restarted worker $w"
    fi
  done

  # 2. assessor-batch: auto-approve gate-verified window briefs (never prose pilots)
  python3 tools/beam_swarm.py auto-review 2>&1 | while IFS= read -r l; do log "auto-review: $l"; done

  # 3. convert approved pilots whose canonical JSON is missing
  python3 tools/ralph_convert.py 2>&1 | while IFS= read -r l; do log "convert: $l"; done

  # 4. commit + push material changes (never queue/logs/claims/staging)
  git add -A >/dev/null 2>&1
  git reset -q process/beam/queue.json process/beam/claims process/beam/w1.log process/beam/w2.log process/beam/w3.log process/beam/w4.log process/beam/w5.log process/beam/ralph.log ipvv/cm/beam 2>/dev/null
  if ! git diff --cached --quiet; then
    if python3 tools/validate_all.py --quick >/dev/null 2>&1; then
      git commit -qm "ralph pass $i: swarm progress (machine-proposed)" && git push -q origin master 2>&1 | while IFS= read -r l; do log "push: $l"; done
      log "committed+pushed pass $i"
    else
      log "validate_all (--quick) FAILED — holding commit, needs assessor"
    fi
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
