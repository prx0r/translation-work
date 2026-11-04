#!/usr/bin/env python3
"""tools/build_l0.py — build working-L0 JSON from CM citation/morph data + T1.

  python3 tools/build_l0.py --work vbt --cm vbt/cm/l0cm-v61-70.DRAFT.json [--cm ...]

CM format (one JSON file, keys = verse numbers):
  {"61": [["lemma1", "morph string", "grounds or \\"\\""], ...], ...}
One entry per span token, ORDER == workcfg.source_spans(work) (separators
'/' and '|' filtered). The builder asserts 3-way length and surface equality
CM vs span vs T1, then inherits the gloss from T1 (never re-typed).

Output: work/working-l0-<song>.json (merge semantics — verses named in --cm
are replaced, other verses of an existing song file are kept). After a batch:
  1) schema-validate:   python3 -c "from schemas.l0 import validate; ..."
  2) drift-check vs T1  (surface + chosen gloss identical)
  3) commit
"""
from __future__ import annotations
import argparse, glob, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import workcfg


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--cm', action='append', required=True,
                    help='CM JSON path (repeatable; later files override earlier)')
    args = ap.parse_args()

    sp = workcfg.source_spans(args.work)
    if not sp:
        print('ERROR: no source spans (intake source/segments missing?)', file=sys.stderr)
        return 1

    t1 = {}          # verse -> T1 record
    for f in sorted((ROOT / args.work).glob('working-t1-*.json')):
        for e in json.loads(f.read_text(encoding='utf-8')):
            t1[e['verse']] = e
    if not t1:
        print('ERROR: no working-t1-*.json found', file=sys.stderr)
        return 1

    cm: dict[int, list] = {}
    for path in args.cm:
        d = json.loads(Path(path).read_text(encoding='utf-8'))
        for k, v in d.items():
            cm[int(k)] = v
    print('CM verses:', len(cm))

    built: dict[str, list[tuple[int, list]]] = {}
    for v in sorted(cm):
        span = [t for t in sp[v] if set(t) != {'|'} and t != '/']
        rec_t1 = t1.get(v)
        assert rec_t1 is not None, f'no T1 record for verse {v}'
        cms = cm[v]
        assert len(cms) == len(span), (v, 'CM', len(cms), 'span', len(span))
        assert len(rec_t1['tokens']) == len(span), (v, 'T1', len(rec_t1['tokens']), 'span', len(span))
        song = rec_t1['verse_id'].rsplit('-v', 1)[0]
        recs = []
        for i, (c, s, tk) in enumerate(zip(cms, span, rec_t1['tokens'])):
            assert s == tk['surface'], (v, i, s, tk['surface'])
            assert len(c) >= 2, (v, i, c)
            o = {'gloss': tk['quick_gloss'], 'rank': 1, 'source': 't1-draft'}
            if len(c) > 2 and c[2]:
                o['grounds'] = c[2]
            recs.append({
                'id': f'{song}-v{v:02d}-p{i:03d}',
                'verse_id': f'{song}-v{v:02d}',
                'pada_index': i, 'surface': s,
                'citation': c[0], 'morph': c[1],
                'options': [o], 'chosen_index': 0,
                'status': 'PARSED', 'fork': 'none',
            })
        built.setdefault(song, []).append((v, recs))

    for song, pairs in sorted(built.items()):
        out = ROOT / args.work / f'working-l0-{song}.json'
        old = []
        if out.exists():
            old = json.loads(out.read_text(encoding='utf-8'))
        covered = {v for v, _ in pairs}
        kept = [r for r in old
                if int(r['verse_id'].rsplit('-v', 1)[1]) not in covered]
        flat = kept + [r for _, recs in sorted(pairs) for r in recs]
        flat.sort(key=lambda r: (int(r['verse_id'].rsplit('-v', 1)[1]), r['pada_index']))
        out.write_text(json.dumps(flat, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'{song}: +{sum(len(recs) for _, recs in pairs)} records '
              f'({len(kept)} kept) -> {out.relative_to(ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
