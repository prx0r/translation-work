#!/usr/bin/env python3
"""tantraloka-a22/cm/l3l4_a22.py — L3/L4 data + build (hand-written)."""
import json
import sys
sys.path.insert(0, 'tools')
from l3l4_a22_data import C, L3L, L4L, CR, AGAIN
from workcfg import source_spans

S = 'tal-a22'
spans = source_spans('tantraloka-a22')
l3 = []
l0ids_all = {e['id'] for e in json.load(open('tantraloka-a22/working-l0-%s.json' % S))}
for v in range(1, 49):
    vid = '%s-v%02d' % (S, v)
    ids = ['%s-p%03d' % (vid, i) for i in range(len(spans[v]))]
    l3.append({"verse_id": vid, "song": S, "verse": v, "lines": L3L[v], "sanskrit_cite": C[v], "l0_ids": ids, "essence_maps": [v - 1], "fidelity": "preserved", "needs": ["human-review"], "notes": []})
json.dump(l3, open('tantraloka-a22/working-l3-%s.json' % S, 'w'), ensure_ascii=False, indent=1)
for v in range(1, 49):
    vid = '%s-v%02d' % (S, v)
    n = len(spans[v])
    keep = list(range(0, n, max(1, n // 3)))
    ids = ['%s-p%03d' % (vid, i) for i in keep]
    assert set(ids) <= l0ids_all, vid
    obj = {"craft_notes": CR[v], "form": "couplet" if len(L4L[v]) > 1 else "single",
           "l4": {"verse_id": vid, "song": S, "verse": v, "lines": L4L[v], "sanskrit_cite": C[v], "l0_ids": ids, "essence_maps": [v - 1]},
           "reads_against": {"argmap": AGAIN[v], "c1_essence": [AGAIN[v]]}, "status": "machine-proposed"}
    json.dump(obj, open('tantraloka-a22/L4-%s.DRAFT.json' % vid, 'w'), ensure_ascii=False, indent=1)
print('l3 + 48 DRAFTs written')
