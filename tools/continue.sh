#!/usr/bin/env bash
# continue.sh — THE BUTTON. Sync openpatala registry -> seed swarm -> run.
# Idempotent. Safe to press twice. Never pushes on red, never marks PASS.
# Usage: setsid nohup bash tools/continue.sh > process/beam/continue.log 2>&1 < /dev/null &
#   (or run in foreground for one supervised pass: bash tools/continue.sh once)
set -u
cd /root/translation-work || exit 1
ONCE=${1:-loop}
export OPENCODE_GO_KEY="$(agent-vault vault credential get OPENCODE_GO_KEY --vault oracle)"

log() { echo "[continue $(date -u +%FT%TZ)] $*"; }

step_sync_seed() {
  log "registry sync + seed"
  python3 tools/registry_sync.py --seed 2>&1 | while IFS= read -r l; do log "sync: $l"; done
}

step_workers() {
  for w in w1 w2 w3 w4 w5; do
    if ! pgrep -f "beam_swarm.py worker $w" >/dev/null 2>&1; then
      setsid nohup python3 tools/beam_swarm.py worker "$w" > "process/beam/$w.log" 2>&1 < /dev/null &
      log "started worker $w"
    fi
  done
}

step_assess() {
  python3 tools/beam_swarm.py auto-review 2>&1 | while IFS= read -r l; do log "assess: $l"; done
  python3 tools/ralph_convert.py 2>&1 | while IFS= read -r l; do log "convert: $l"; done
}

step_gates_commit() {
  if python3 tools/validate_all.py --quick >/dev/null 2>&1; then
    git add -A >/dev/null 2>&1
    git reset -q process/beam/queue.json process/beam/claims process/beam/w1.log process/beam/w2.log process/beam/w3.log process/beam/w4.log process/beam/w5.log process/beam/ralph.log process/beam/continue.log process/beam/validate_all.log ipvv/cm/beam process/beam/runs 2>/dev/null
    if ! git diff --cached --quiet; then
      git commit -qm "continue: swarm progress (machine-proposed)" && git push -q origin master && log "pushed"
    else
      log "clean tree, nothing to push"
    fi
  else
    log "gates red — holding, needs assessor"
  fi
}

step_status() {
  python3 tools/beam_swarm.py status 2>&1 | awk '{print $3}' | sort | uniq -c | tr '\n' ' ' | while IFS= read -r l; do log "queue:$l"; done
}

if [ "$ONCE" = "once" ]; then
  step_sync_seed; step_workers; sleep 5; step_assess; step_gates_commit; step_status
  log "single pass done"
  exit 0
fi

# loop mode: keep the registry fresh + seeded, let ralph.sh run the work loop.
# One loop implementation only (ralph.sh); this button supervises it.
i=0
while true; do
  i=$((i + 1)); log "=== pass $i ==="
  step_sync_seed
  if ! pgrep -f "tools/ralph.sh" >/dev/null 2>&1; then
    setsid nohup bash tools/ralph.sh 240 180 > process/beam/ralph.log 2>&1 < /dev/null &
    log "started ralph.sh"
  fi
  step_status
  sleep 300
done
