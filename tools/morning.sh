#!/usr/bin/env bash
# Morning triage — one command after an overnight run.
cd /root/translation-work || exit 1
echo "=== service ==="; systemctl is-active tal-campaign
echo; echo "=== gold proofs (TAL) ==="
python3 - <<'PY'
import json, glob, os
rows=[]
for f in sorted(glob.glob('tantraloka-a*/STATUS.json')):
    w=os.path.dirname(f); d=json.load(open(f))
    pf=f'{w}/proof/proof-{os.path.basename(w).replace("tantraloka-","tal-")}.json'
    gate=None
    if os.path.exists(pf):
        gate=json.load(open(pf)).get('deterministic_gate')
    rows.append((w.replace('tantraloka-',''), d.get('counts',{}).get('verses','?'), gate or d.get('counts',{}).get('proof','-')))
for r in rows: print(f'{r[0]:5} verses={r[1]:>4} proof={r[2]}')
PY
echo; echo "=== campaign tail ==="; tail -15 process/beam/tal_campaign.log
echo; echo "=== watchdog tail ==="; tail -5 process/beam/watchdog.log
echo; echo "=== queue ==="; python3 - <<'PY'
import json, collections
q=json.load(open('process/beam/queue.json'))
print(dict(collections.Counter((t.get('kind'),t.get('status')) for t in q if t.get('kind','').startswith('tal_'))))
PY
echo; echo "=== parked/blocked ==="; grep -i "incomplete\|blocked\|parked" process/beam/tal_campaign.log | tail -10
echo; echo "=== git ==="; git log --oneline -10
