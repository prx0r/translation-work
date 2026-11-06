#!/usr/bin/env python3
"""dump_unparsed — emit hand-gloss work packets for remaining *-unparsed rows.

Usage: python3 tools/dump_unparsed.py <song>  (or --all)
Writes ipvv/cm/<song>.handpacket.json:
  [{i, surface, prev: [[surf,gloss]...], next: [[surf,gloss]...]}]
prev/next = up to 3 neighboring L0 rows with their current glosses.
"""
from __future__ import annotations
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from workcfg import data_dir

def packet(song: str):
    dd = data_dir('ipvv', song)
    t1 = json.load(open(dd / f'{song}.t1.json'))
    l0 = json.load(open(dd / f'{song}.l0.json'))
    covered = json.load(open(ROOT / 'ipvv' / 'cm' / f'{song}-covered.json'))
    out = []
    for k, row in enumerate(l0):
        o = (row.get('options') or [{}])[0]
        if row.get('status') == 'AMBIGUOUS' and o.get('gloss', '').endswith('-unparsed'):
            prev = [[l0[j]['surface'], (l0[j].get('options') or [{}])[0].get('gloss', '')]
                    for j in range(max(0, k - 3), k)]
            nxt = [[l0[j]['surface'], (l0[j].get('options') or [{}])[0].get('gloss', '')]
                   for j in range(k + 1, min(len(l0), k + 4))]
            out.append({'k': k, 'i': covered[k], 'surface': row['surface'],
                        'prev': prev, 'next': nxt})
    p = ROOT / 'ipvv' / 'cm' / f'{song}.handpacket.json'
    p.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f'{song}: {len(out)} unparsed -> {p.name}')
    return len(out)

def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('song', nargs='?', default=None)
    ap.add_argument('--all', action='store_true')
    a = ap.parse_args()
    if a.all:
        table = json.load(open(ROOT / 'ipvv' / 'chunk-table.json'))
        tot = sum(packet(e['song']) for e in table)
        print('TOTAL', tot)
    elif a.song:
        packet(a.song)
    else:
        ap.error('give SONG or --all')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
