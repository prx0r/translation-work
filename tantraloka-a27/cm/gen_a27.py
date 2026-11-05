#!/usr/bin/env python3
"""tantraloka-a27/cm/gen_a27.py — CM+T1 source tables (hand-written) + build."""
import json
import sys
sys.path.insert(0, 'tools')
from workcfg import source_spans

import sys as _sys; _sys.path.insert(0, "tantraloka-a27/cm")
import data_a27_all as _d
TOK = dict(_d.TOK)
CM = dict(_d.CM)
GLOSS = dict(_d.GLOSS)
QE = dict(_d.QE)

def main() -> None:
    spans = source_spans('tantraloka-a27')
    assert {int(k): v for k, v in TOK.items()} == {k: v for k, v in spans.items()}, 'TOKENS DRIFT'
    assert all(len(TOK[v]) == len(CM[v]) == len(GLOSS[v]) for v in TOK), 'ROW DRIFT'
    json.dump({str(k): v for k, v in TOK.items()}, open('tantraloka-a27/cm/spans-tal-a27.json', 'w'), ensure_ascii=False, indent=1)
    cm = {}
    for v in TOK:
        cm[str(v)] = [[CM[v][i][0], CM[v][i][1], CM[v][i][2]] for i in range(len(TOK[v]))]
    json.dump(cm, open('tantraloka-a27/cm/l0cm-v1-59.json', 'w'), ensure_ascii=False, indent=1)
    t1 = [{"verse_id": "tal-a27-v%02d" % v, "song": "tal-a27", "verse": v, "quick_english": QE[v], "quick_english_source": "manual", "tokens": [{"surface": TOK[v][i], "quick_gloss": GLOSS[v][i]} for i in range(len(TOK[v]))]} for v in sorted(TOK)]
    json.dump(t1, open('tantraloka-a27/working-t1-tal-a27.json', 'w'), ensure_ascii=False, indent=1)
    md = '# Tantraloka-a27 — T1\n*Source: GRETIL tantraloka (KSTS) via workcfg taloka. Span-exact vs source_spans. Machine-proposed, needs human review.*\n'
    for v in sorted(TOK):
        md += '\n\n## tal-a27-v%02d\n' % v
        md += ' '.join('[and]-%s (%s)' % (GLOSS[v][i], TOK[v][i]) for i in range(len(TOK[v]))) + ' // %d //\n' % v
    open('tantraloka-a27/T1-tal-a27.md', 'w').write(md)
    print('cm+t1 written, verses:', len(t1), 'tokens:', sum(len(x) for x in TOK.values()))


if __name__ == '__main__':
    main()
