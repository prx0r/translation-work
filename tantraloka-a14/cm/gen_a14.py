#!/usr/bin/env python3
"""tantraloka-a14/cm/gen_a14.py — build CM+T1 from tables_a14 (verified)."""
import json
import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, 'tantraloka-a14/cm')
from tables_a14 import TOK, CM, GLOSS, QE
from workcfg import source_spans


def main() -> None:
    spans = source_spans('tantraloka-a14')
    assert {int(k): v for k, v in TOK.items()} == {k: v for k, v in spans.items()}, 'TOKENS DRIFT'
    assert all(len(TOK[v]) == len(CM[v]) == len(GLOSS[v]) for v in TOK), 'ROW DRIFT'
    json.dump({str(k): v for k, v in TOK.items()}, open('tantraloka-a14/cm/spans-tal-a14.json', 'w'), ensure_ascii=False, indent=1)
    cm = {}
    for v in TOK:
        cm[str(v)] = [[CM[v][i][0], CM[v][i][1], CM[v][i][2]] for i in range(len(TOK[v]))]
    json.dump(cm, open('tantraloka-a14/cm/l0cm-v1-47.json', 'w'), ensure_ascii=False, indent=1)
    t1 = [{"verse_id": "tal-a14-v%02d" % v, "song": "tal-a14", "verse": v, "quick_english": QE[v], "quick_english_source": "manual", "tokens": [{"surface": TOK[v][i], "quick_gloss": GLOSS[v][i]} for i in range(len(TOK[v]))]} for v in sorted(TOK)]
    json.dump(t1, open('tantraloka-a14/working-t1-tal-a14.json', 'w'), ensure_ascii=False, indent=1)
    md = '# Tantraloka-a14 — T1\n*Source: GRETIL tantraloka (KSTS) via workcfg taloka. Span-exact vs source_spans. Machine-proposed, needs human review.*\n'
    for v in sorted(TOK):
        md += '\n\n## tal-a14-v%02d\n' % v
        md += ' '.join('[and]-%s (%s)' % (GLOSS[v][i], TOK[v][i]) for i in range(len(TOK[v]))) + ' // %d //\n' % v
    open('tantraloka-a14/T1-tal-a14.md', 'w').write(md)
    print('cm+t1 written, verses:', len(t1), 'tokens:', sum(len(x) for x in TOK.values()))


if __name__ == '__main__':
    main()
