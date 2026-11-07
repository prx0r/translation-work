#!/usr/bin/env bash
# LOOP.sh — the Ralph loop: same prompt, fresh agent, until the promise.
# while :; do cat PROMPT.md | claude ; done  (Huntley) — opencode edition.
#
# Usage: setsid nohup bash LOOP.sh > process/beam/loop.log 2>&1 < /dev/null &
# Stop: touch process/beam/LOOP.STOP  (checked between iterations)
#   or: pkill -f "opencode-ai run" -- exact PID preferred (see log header).
#
# Each iteration: fresh `opencode run` reads PROMPT.md + repo state (files/git
# are the memory), does ONE work item, exits. Promise tag in output ends loop.
set -u
cd /root/translation-work || exit 1
export OPENCODE_API_KEY="$(agent-vault vault credential get OPENCODE_API_KEY --vault oracle 2>/dev/null || true)"
if [ -z "${OPENCODE_API_KEY:-}" ]; then
  echo "[loop] FATAL: no OPENCODE_API_KEY in vault (oracle). Aborting." >&2
  exit 1
fi
MAX_ITERS=${MAX_ITERS:-100}
MODEL=${MODEL:-"opencode-go/mimo-v2.6-flash"}
PROMISE="${PROMISE:-TANTRALOKA-FINISHED}"
LOGDIR=process/beam
echo "[loop $$] start max=$MAX_ITERS model=$MODEL (log: $LOGDIR/loop.log)"

i=0
while [ "$i" -lt "$MAX_ITERS" ]; do
  i=$((i + 1))
  if [ -f "$LOGDIR/LOOP.STOP" ]; then echo "[loop] STOP file present — exiting."; break; fi
  echo "[loop] === iteration $i/$MAX_ITERS $(date -u +%FT%TZ) ==="
  out="$(cat PROMPT.md | timeout 5400 npx -y opencode-ai run --auto -m "$MODEL" --dir /root/translation-work 2>>"$LOGDIR/loop.log")"
  echo "$out" | tail -n 20 >>"$LOGDIR/loop.log"
  if printf '%s' "$out" | grep -q "<promise>$PROMISE</promise>"; then
    echo "[loop] PROMISE $PROMISE seen — Tantraloka finished set COMPLETE."
    break
  fi
  echo "[loop] iteration $i done, no promise — looping."
  sleep 10
done
echo "[loop] exit after $i iterations."
