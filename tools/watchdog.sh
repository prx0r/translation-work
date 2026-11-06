#!/usr/bin/env bash
# watchdog.sh — keep the TAL campaign alive, unattended, overnight.
# Every pass: ensure driver, ensure workers, detect stalls, rotate logs,
# heartbeat. Idempotent; safe to kill and restart. Never forces a PASS.
set -u
cd /root/translation-work || exit 1
WORKERS=${WORKERS:-3}
STALL_MINS=${STALL_MINS:-25}
LOGDIR=process/beam
WD_LOG=$LOGDIR/watchdog.log
export OPENCODE_GO_KEY="$(agent-vault vault credential get OPENCODE_GO_KEY --vault oracle)"

log(){ echo "[wd $(date -u +%FT%TZ)] $*" | tee -a "$WD_LOG"; }

start_workers(){
  for w in $(seq 1 "$WORKERS"); do
    if ! pgrep -f "beam_swarm.py worker w$w" >/dev/null 2>&1; then
      setsid nohup python3 tools/beam_swarm.py worker "w$w" > "$LOGDIR/w$w.log" 2>&1 < /dev/null &
      log "started worker w$w"
    fi
  done
}

start_driver(){
  if ! pgrep -f "tal_run_all.sh" >/dev/null 2>&1; then
    setsid nohup bash tools/tal_run_all.sh >> "$LOGDIR/tal_campaign.log" 2>&1 < /dev/null &
    log "started driver"
  fi
}

reap_stale_claims(){
  python3 - <<'PY' 2>/dev/null
import json, os, time, glob
p='process/beam/queue.json'
q=json.load(open(p)); n=0
now=time.time()
for t in q:
    if t.get('status')!='claimed': continue
    f=f"process/beam/claims/{t['id']}.json"
    try: age=now-os.path.getmtime(f)
    except OSError: age=9999
    if age > 1500:  # 25 min: owner dead (24-verse calls can take 10)
        t['status']='pending'; t['attempts']=min(t.get('attempts',0),2); n+=1
        try: os.unlink(f)
        except OSError: pass
if n:
    json.dump(q,open(p,'w'),indent=1)
    print(f"reaped {n} stale claims")
PY
}

# stalled = tasks claimed but no worker log growth for STALL_MINS
check_stall(){
  local newest
  newest=$(ls -t "$LOGDIR"/w*.log 2>/dev/null | head -1)
  [ -z "$newest" ] && return
  local age=$(( ( $(date +%s) - $(stat -c %Y "$newest") ) / 60 ))
  local claimed
  claimed=$(python3 - <<'PY' 2>/dev/null || echo 0
import json
q=json.load(open('process/beam/queue.json'))
print(sum(1 for t in q if t.get('status')=='claimed'))
PY
)
  if [ "$claimed" -gt 0 ] && [ "$age" -ge "$STALL_MINS" ]; then
    log "STALL: $claimed claimed, logs idle ${age}m — restarting workers"
    pkill -f "beam_swarm.py worker" 2>/dev/null
    sleep 2
    rm -f process/beam/claims/*.json
    python3 - <<'PY' 2>/dev/null
import json
p='process/beam/queue.json'; q=json.load(open(p))
for t in q:
    if t.get('status')=='claimed':
        t['status']='pending'; t['attempts']=min(t.get('attempts',0), 2)
json.dump(q,open(p,'w'),indent=1)
PY
    start_workers
  fi
}

rotate_logs(){
  for f in "$LOGDIR"/w*.log "$LOGDIR"/tal_campaign.log "$WD_LOG"; do
    [ -f "$f" ] || continue
    if [ "$(stat -c %s "$f")" -gt 52428800 ]; then
      tail -c 5000000 "$f" > "$f.tmp" && mv "$f.tmp" "$f"
      log "rotated $f"
    fi
  done
}

log "watchdog start (workers=$WORKERS stall=${STALL_MINS}m pid=$$)"
while true; do
  start_driver
  start_workers
  reap_stale_claims
  check_stall
  rotate_logs
  # progress snapshot
  python3 - <<'PY' >> "$WD_LOG" 2>/dev/null
import json, collections, time
try:
    q=json.load(open('process/beam/queue.json'))
except Exception:
    raise SystemExit
c=collections.Counter((t.get('kind'),t.get('status')) for t in q if t.get('kind')=='tal_triple')
print(f"[wd {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}] triples {dict(c)}")
PY
  sleep 60
done
