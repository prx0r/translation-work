#!/usr/bin/env python3
"""tools/emit_tal.py — mechanical derive for Tantraloka gold works.

Reads hand-written layers, writes canonical data/*.json + T1 l0 files + SOURCE.
Hand-written inputs: working-t1/l0/argmap/l3, L2-<song>.md, L4-*.DRAFT.json,
c1/C1-<song>.md, data/<song>.essence.json (verse-ordered essence strings),
data/<song>.rasa.json {"dominant","sthayibhava","justification"}.

  python3 tools/emit_tal.py --work tantraloka-a20 --song tal-a20 --sha <argmap-sha>

Conventions (match GOLD #54/#55): cite split on ' | ' per GRETIL line;
T1 headers '## <song>-vNN'; L2 cites 'The Sanskrit: *...*'; supplied always [].
"""
from __future__ import annotations
import argparse, hashlib, json, re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(ROOT / 'tools'))
import workcfg


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True); ap.add_argument('--song', required=True)
    ap.add_argument('--sha', required=True)
    args = ap.parse_args()
    W = ROOT / args.work; S = args.song
    spans = workcfg.source_spans(args.work)
    assert spans, 'no spans for %s' % args.work
    verses = sorted(spans)

    l0 = json.loads((W / f'working-l0-{S}.json').read_text())
    t1 = json.loads((W / f'working-t1-{S}.json').read_text())
    am = json.loads((W / f'working-argmap-{S}.json').read_text())
    l3 = json.loads((W / f'working-l3-{S}.json').read_text())
    assert len(t1) == len(verses) == len(am) == len(l3), (len(t1), len(verses), len(am), len(l3))
    for e in t1:
        e['source_sha'] = args.sha
    (W / f'working-t1-{S}.json').write_text(json.dumps(t1, ensure_ascii=False, indent=1))

    dd = W / 'data'; dd.mkdir(exist_ok=True)
    json.dump(t1, open(dd / f'{S}.t1.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(l0, open(dd / f'{S}.l0.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(am, open(dd / f'{S}.argmap.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(l3, open(dd / f'{S}.l3.json', 'w'), ensure_ascii=False, indent=1)

    md = (W / f'L2-{S}.md').read_text()
    blocks = re.findall(r'## v\.(\d+)\n(.+?)\nThe Sanskrit: \*(.+?)\*', md)
    assert len(blocks) == len(verses), (len(blocks), len(verses))
    l2 = []
    for v, eng, cite in blocks:
        v = int(v); vid = '%s-v%02d' % (S, v)
        l2.append({"verse_id": vid, "song": S, "verse": v, "plain_english": eng.strip(),
                   "sanskrit_cite": cite.strip(),
                   "l0_ids": [e['id'] for e in l0 if e['verse_id'] == vid], "supplied": []})
    json.dump(l2, open(dd / f'{S}.l2.json', 'w'), ensure_ascii=False, indent=1)

    l4 = []
    for v in verses:
        vid = '%s-v%02d' % (S, v)
        d = json.loads((W / f'L4-{vid}.DRAFT.json').read_text())
        e = dict(d['l4'])
        e.update({"needs": ["human-review"], "notes": [], "fidelity": "preserved", "form": d['form']})
        l4.append(e)
    json.dump(l4, open(dd / f'{S}.l4.json', 'w'), ensure_ascii=False, indent=1)

    ESS = json.loads((dd / f'{S}.essence.json').read_text())
    assert len(ESS) == len(verses)
    c1md = (W / f'c1/C1-{S}.md').read_text()
    secs = {}
    for m in re.finditer(r'## ([A-Z ]+)\n\n(.+?)(?=\n## |\Z)', c1md, re.S):
        secs[m.group(1).strip()] = ' '.join(m.group(2).strip().split('\n'))
    assert set(secs) == {'SUMMARY', 'FUNCTION', 'KEY TERMS', 'LOCAL CONTEXT', 'EXPLANATION', 'BOUNDARY', 'RELATED'}, set(secs)
    rasa = json.loads((dd / f'{S}.rasa.json').read_text())
    json.dump({"song": S, "essence": ESS, "essence_source": "manual", "rasa": rasa,
               "renders": {"standard": {"kind": "standard", "label": "standard", "sections": secs}}},
              open(dd / f'{S}.c1.json', 'w'), ensure_ascii=False, indent=1)

    with open(W / f'T1-{S}.l0.jsonl', 'w') as f:
        for e in l0:
            f.write(json.dumps(e, ensure_ascii=False) + '\n')
    c = Counter(e['status'] for e in l0)
    (W / f'T1-{S}.l0.report.txt').write_text(
        'chunk: %s\ntokens: %d\n  PARSED: %d\n  AMBIGUOUS: %d\n  FAILED: %d\nlines: %d\n' % (
            S, len(l0), c.get('PARSED', 0), c.get('AMBIGUOUS', 0), c.get('FAILED', 0), len(t1)))

    src = Path(workcfg.WORKS[args.work]['source']).read_text().splitlines()
    ahnika = workcfg.WORKS[args.work]['ahnika']
    start = next(i for i, l in enumerate(src) if re.match(r'^:C%d\b' % ahnika, l.strip()))
    end = next((i for i in range(start + 1, len(src))
                if re.match(r'^:C\d+\b', src[i].strip())), len(src))
    chunk = [l for l in src[start:end] if l.strip()]
    title = chunk[0].lstrip(':')
    txt = 'Tantraloka, %s (%s)\n' % (title, S) + '\n'.join(chunk[1:]) + '\n'
    (W / 'SOURCE.txt').write_text(txt)
    (W / 'SOURCE.sha').write_text(hashlib.sha256(txt.encode()).hexdigest()[:12])
    print(f'{S}: data written t1={len(t1)} l0={len(l0)} am={len(am)} l2={len(l2)} l3={len(l3)} l4={len(l4)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
