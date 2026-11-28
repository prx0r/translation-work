#!/usr/bin/env bash
# TAL campaign driver: shortest-first through every pending ahnika.
# Each ahnika: parse -> seed -> wait for beam -> assemble -> validate -> proof.
# Proof BLOCKED parks that ahnika (logged) and moves on; never forces a PASS.
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
    python3 - <<PY
import json
p='$W/STATUS.json'
d=json.load(open(p)); d.setdefault('counts',{})['proof']='PASS'; d['updated']='2026-11-06'
d['next']='minimal gold complete; L3/L4 waived; human review pending'
json.dump(d,open(p,'w'),indent=1,ensure_ascii=False)
PY
    python3 - <<PY
import json
r=json.load(open('REGISTRY.json'))
n=$(( $(python3 -c "import json;print(len(json.load(open('$W/data/$S.t1.json'))))") ))
done_=False
for w in r['works']:
    if w['work']=='$W':
        w.update({'status':'gold (machine-proposed, minimal: L3/L4 waived)','gold':True,'verses':n,
                  'note':'minimal gold via largetext swarm: T1/L0/argmap/L2/C1-essence, proof PASS; L3/L4 waived.'}); done_=True
if not done_:
    r['works'].append({'work':'$W','status':'gold (machine-proposed, minimal: L3/L4 waived)','gold':True,'verses':n,
                       'note':'minimal gold via largetext swarm'})
json.dump(r,open('REGISTRY.json','w'),indent=1,ensure_ascii=False)
PY
    python3 tools/manifest.py gen >/dev/null 2>&1
    git add -A ':!process/beam/queue.json' ':!process/beam/claims/*' ':!process/beam/runs/*' ':!ipvv/cm/beam/*' ':!process/beam/w*.log' 2>/dev/null
    git commit -qm "TAL $a minimal gold (machine-proposed)" && git push -q origin HEAD
    log "$a PASS — committed"
  else
    log "$a INCOMPLETE/BLOCKED (rc=$rc) — assessor needed"
  fi
done
log "campaign pass done"
