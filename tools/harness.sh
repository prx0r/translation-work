#!/usr/bin/env bash
# harness.sh — ONE supervisor for the translation-work autonomous loop.
# Policy (owner-directed): beam is fragile — start ONE worker, add a second
# only while quota is healthy, never pound a throttled tier.
#
# Every pass (300s): health gate -> PAUSE-file discipline -> ensure the stack
# (continue.sh loop, watchdog.sh, tal driver) -> enforce worker policy ->
# assessor sweep (verdicts, escalations, lore-gap seeds) -> try assemble for
# complete-but-unassembled songs -> gate check -> heartbeat log.
# Idempotent; safe to kill and restart. Never marks PASS, never pushes
# (ralph.sh owns gated pushes).
#
# Usage: setsid nohup bash tools/harness.sh > process/beam/harness.log 2>&1 < /dev/null &
set -u
cd /root/translation-work || exit 1
export OPENCODE_GO_KEY="$(agent-vault vault credential get OPENCODE_GO_KEY --vault oracle)"
# Second Go account: beam_client rotates sessions across both keys and fails
# over on 429 before parking a model. Durable in the vault (fallback .env).
export OPENCODE_GO_KEY_BAK="$(agent-vault vault credential get OPENCODE_GO_KEY_BAK --vault oracle 2>/dev/null || true)"
LOGDIR=process/beam
HWORKERS="${HARNESS_WORKERS:-w1 w2}"   # default set; w3 added only if healthy
SLEEP_SECS=${HARNESS_SLEEP:-300}

log() { echo "[harness $(date -u +%FT%TZ)] $*"; }

health_ok() {
  python3 - <<'EOF' 2>/dev/null || return 1
import sys; sys.path.insert(0,'tools')
from beam_client import health
ok,_ = health(); sys.exit(0 if ok else 1)
EOF
}

ensure_proc() { # pattern, start-cmd...
  local pat="$1"; shift
  if ! pgrep -f "$pat" >/dev/null 2>&1; then
    # shellcheck disable=SC2068
    setsid nohup $@ >>"$LOGDIR/harness.log" 2>&1 < /dev/null &
    log "started: $*"
  fi
}

enforce_workers() { # exactly the HWORKERS set alive, nothing more
  local want alive w pid
  alive=""
  for w in w1 w2 w3 w4 w5; do
    if pgrep -f "beam_swarm.py worker $w" >/dev/null 2>&1; then
      alive="$alive $w"
    fi
  done
  # start missing wanted slots (staggered by the worker loop's own pacing)
  for w in $HWORKERS; do
    case "$alive" in *"$w"*) ;; *)
      setsid nohup python3 -u tools/beam_swarm.py worker "$w" > "$LOGDIR/$w.log" 2>&1 < /dev/null &
      log "started worker $w (policy set: $HWORKERS)"
      sleep 8
      ;;
    esac
  done
  # stop extras (exact PIDs only, never pkill): claims self-heal in 15 min
  for w in w1 w2 w3 w4 w5; do
    case " $HWORKERS " in *" $w "*) continue;; esac
    pid=$(pgrep -f "beam_swarm.py worker $w" | head -1)
    if [ -n "$pid" ]; then kill "$pid" 2>/dev/null && log "stopped extra worker $w (pid $pid, policy: $HWORKERS)"; fi
  done
}

try_assemble() { # complete-but-unassembled songs -> tal_stage single pass
  python3 - "$LOGDIR" <<'EOF'
import json, subprocess, sys
from pathlib import Path
ROOT = Path('.')
q = json.load(open('process/beam/queue.json'))
busy = {t['args'].get('song') for t in q if t.get('status') in ('pending','claimed') and t.get('kind')=='tal_triple'}
import sys as _s; _s.path.insert(0,'tools')
import workcfg
for work in sorted(p.name for p in ROOT.iterdir() if (p/'STATUS.json').exists() and p.name.startswith('tantraloka-a')):
    try: songs = workcfg.WORKS[work]['songs']
    except KeyError: continue
    for song in songs:
        if song in busy: continue
        dd = ROOT/work/'data'
        if (dd/(song+'.t1.json')).exists(): continue
        r = subprocess.run([sys.executable,'tools/tal_stage.py','--work',work,'--song',song],
                           capture_output=True, text=True, timeout=600)
        tail = (r.stdout+r.stderr).strip().splitlines()[-1:]
        print(f'assemble {song}: rc={r.returncode} {' '.join(tail)[:120]}', flush=True)
EOF
}

log "harness start (workers: $HWORKERS)"
i=0
while true; do
  i=$((i+1)); log "=== pass $i ==="
  # Re-assert the key every pass: supervisor env has been observed without
  # it (workers inherit from whoever starts them; beam_client self-heals too,
  # but keep the canonical export fresh regardless).
  if [ -z "${OPENCODE_GO_KEY:-}" ]; then
    export OPENCODE_GO_KEY="$(agent-vault vault credential get OPENCODE_GO_KEY --vault oracle 2>/dev/null || true)"
    export OPENCODE_GO_KEY_BAK="$(agent-vault vault credential get OPENCODE_GO_KEY_BAK --vault oracle 2>/dev/null || true)"
    [ -n "${OPENCODE_GO_KEY:-}" ] && log "key re-asserted" || log "key MISSING — beam calls will fail"
  fi
  if health_ok; then
    rm -f "$LOGDIR/PAUSED"
    log "beam healthy"
  else
    touch "$LOGDIR/PAUSED"
    log "beam down — PAUSED set (workers drain, no fresh claims)"
  fi
  # Disk guard (overnight safety): beam drafts thousands of run files; if the
  # disk is nearly full, stop fresh claims (PAUSED) so nothing corrupts git or
  # partial writes. Clears automatically once free space recovers.
  FREE_GB=$(df -Pk . 2>/dev/null | awk 'NR==2{printf "%d", $4/1024/1024}')
  FREE_GB=${FREE_GB:-999}
  if [ "$FREE_GB" -lt 2 ]; then
    touch "$LOGDIR/PAUSED"
    log "LOW DISK ${FREE_GB}GB free — PAUSED (workers drain, no new claims)"
  fi
  ensure_proc "tools/continue.sh" bash tools/continue.sh
  ensure_proc "tools/watchdog.sh" bash tools/watchdog.sh
  # Model loop (Ralph): restarts silently-dead LOOP.sh; promise/STOP file govern exit.
  if [ ! -f "$LOGDIR/LOOP.STOP" ]; then
    ensure_proc "LOOP.sh" bash LOOP.sh
  fi
  enforce_workers
  python3 tools/assessor_sweep.py 2>&1 | while IFS= read -r l; do log "sweep: $l"; done
  try_assemble 2>&1 | while IFS= read -r l; do log "$l"; done
  if python3 tools/validate_all.py --quick >/dev/null 2>&1; then
    log "gates: green"
  else
    log "gates: RED — holding, needs assessor"
  fi
  sleep "$SLEEP_SECS"
done
