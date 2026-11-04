# assemble u1-17 L0 cm (content hand-composed; this script only assembles + span-checks)
import json, sys
sys.path.insert(0, '/root/translation-work/tools')
from workcfg import source_spans
cm = json.load(open('/root/translation-work/tantrasara-a03/cm/p1-content.json'))
sp = source_spans('tantrasara-a03')
ok = True
for v in range(1, 18):
    span = [t for t in sp[v] if set(t) != {'|'} and t != '/']
    m = len(span) == len(cm[str(v)])
    ok = ok and m
    if not m:
        print('U', v, len(span), len(cm[str(v)]))
        for i in range(max(len(span), len(cm[str(v)]))):
            s = span[i] if i < len(span) else '---'
            c = cm[str(v)][i][0] if i < len(cm[str(v)]) else '---'
            print(' ', i, s, '|', c)
print('U1-17', 'ALIGNED' if ok else 'FIX')
if ok:
    json.dump(cm, open('/root/translation-work/tantrasara-a03/cm/p1.json', 'w'), ensure_ascii=False, indent=1)
    print('saved cm/p1.json')
