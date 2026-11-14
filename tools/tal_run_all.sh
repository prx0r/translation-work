#!/usr/bin/env bash
# TAL campaign driver: shortest-first through every pending ahnika.
# Each ahnika: parse -> seed -> wait for beam -> assemble -> validate.
# Proof, PASS, promotion, commits and pushes require owner review.
set -u
cd /root/translation-work || exit 1
export OPENCODE_GO_KEY="$(agent-vault vault credential get OPENCODE_GO_KEY --vault oracle)"
ORDER="a11 a17 a30 a05 a31 a06 a04 a29 a10 a16 a09 a01 a03 a13 a28 a08 a15"
log(){ echo "[tal $(date -u +%FT%TZ)] $*"; }
for a in $ORDER; do
  W="tantraloka-$a"; S="tal-$a"
  if [ -f "$W/data/$S.argmap.json" ] && python3 -c "
import json,sys
d=json.load(open('$W/STATUS.json'))
sys.exit(0 if d.get('counts',{}).get('proof')=='PASS' else 1)" 2>/dev/null; then
    log "$a already PASS — skip"; continue
  fi
  log "$a start"
  python3 tools/tal_stage.py --work "$W" --song "$S" --seed --triple --loop --wait 300 --max-wait 14400 2>&1 | while IFS= read -r l; do log "  $l"; done
  rc=${PIPESTATUS[0]}
  if [ "$rc" = "0" ]; then
    log "$a assembled and validated as machine-proposed — owner proof and promotion required"
  else
    log "$a INCOMPLETE/BLOCKED (rc=$rc) — assessor needed"
  fi
done
log "campaign pass done"
