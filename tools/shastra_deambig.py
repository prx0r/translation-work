#!/usr/bin/env python3
"""shastra_deambig — strict machine audit promoting AMBIGUOUS -> PARSED only
where the row's own evidence already expresses confidence.

Promote iff ALL hold:
  - surface is clean IAST (letters/diacritics only, no dash-runs/pipes/digits/?/parens)
  - gloss clean (no uncertain/unparsed/unknown/illegible/damaged/gap/? markers)
  - grounds contain no hedge words (uncertain/unclear/damaged/illegible/truncated/
    guess/unsure/doubtful/corrupt/broken/obscure/tentative/elision/uncertainty)
  - AND one support: (a) exact surface agrees in >=2 other PARSED rows (distinct songs),
    or (b) T1.md prose contains the gloss's content words near the surface stem,
    or (c) surface in CLOSED particle/pronoun list with canonical sense.
Else stays AMBIGUOUS. Never invents. Appends audit note to history.
Usage: python3 tools/shastra_deambig.py [--only song]
"""
from __future__ import annotations
import json, re, sys, glob, pathlib
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from workcfg import data_dir

HEDGE = ('uncertain', 'unclear', 'damaged', 'illegible', 'truncated', 'guess',
         'unsure', 'doubt', 'corrupt', 'broken', 'obscure', 'tentative',
         'elision', 'gap', 'unknown', 'unparsed', 'illegib', 'missing')
CLOSED = {
 'eva': 'indeed', 'ca': 'and', 'vā': 'or', 'va': 'or', 'na': 'not',
 'tu': 'but', 'hi': 'for', 'iti': 'thus', 'api': 'too', 'cet': 'if',
 'nanu': 'surely', 'atha': 'now', 'tatra': 'there', 'yatra': 'where',
 'yathā': 'as', 'tathā': 'thus', 'evam': 'thus', 'khalu': 'indeed',
 'vai': 'indeed', 'kila': 'indeed', 'nūnam': 'surely', 'punaḥ': 'again',
 'punar': 'again', 'saha': 'with', 'vinā': 'without', 'adhunā': 'now',
 'idānīm': 'now', 'tat': 'that', 'tad': 'that', 'etad': 'this', 'etat': 'this',
 'idam': 'this', 'ayam': 'this', 'iyam': 'this', 'etat': 'this',
 'aham': 'i', 'tvam': 'you', 'vayam': 'we', 'yūyam': 'you-pl',
 'kim': 'what', 'katham': 'how', 'kva': 'where', 'kadācit': 'sometimes',
 'sarvatra': 'everywhere', 'sarvathā': 'in-every-way', 'tataḥ': 'thence',
 'yataḥ': 'from-which', 'ataḥ': 'hence', 'tāvat': 'so-long', 'yāvat': 'as-far-as',
}

def clean_surf(s: str) -> bool:
    if not re.fullmatch(r'[a-zāīūṛṝḷḹēōṃḥṅñṭḍṇśṣ]+', s):
        return False
    if len(s) > 40:
        return False
    return True

def clean_gloss(g: str) -> bool:
    gl = g.lower()
    if any(h in gl for h in HEDGE) or '?' in g:
        return False
    if not re.fullmatch(r"[a-zāīūṛṃḥ\-\/ ]+", gl):
        return False
    return True

def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default=None)
    a = ap.parse_args()
    # agreement index from PARSED rows (excluding squeeze/hand promotions? include all PARSED)
    agree = defaultdict(set)
    for f in glob.glob(str(ROOT / 'ipvv' / '*' / 'data' / '*.l0.json')):
        song = pathlib.Path(f).stem
        for r in json.load(open(f)):
            if r.get('status') == 'PARSED':
                g = (r.get('options') or [{}])[0].get('gloss', '')
                if g and '(' not in g:
                    agree[r['surface']].add((g, song))
    table = json.load(open(ROOT / 'ipvv' / 'chunk-table.json'))
    tot = Counter()
    for e in table:
        song = e['song']
        if a.only and song != a.only:
            continue
        dd = data_dir('ipvv', song)
        tp, lp = dd / f'{song}.t1.json', dd / f'{song}.l0.json'
        t1, l0 = json.load(open(tp)), json.load(open(lp))
        # doc text for (b): prose words set
        import workcfg as _w
        cid = _w.chunk_id_for('ipvv', song)
        doctext = (ROOT / 'ipvv' / cid / 'T1.md').read_text().lower() if cid else ''
        docwords = set(re.findall(r'[a-z]{3,}', doctext))
        ch = 0
        for tok, row in zip(t1[0]['tokens'], l0):
            if row.get('status') != 'AMBIGUOUS':
                continue
            o = (row.get('options') or [{}])[0]
            g, gr, s = o.get('gloss', ''), o.get('grounds', ''), tok['surface']
            if not (clean_surf(s) and clean_gloss(g)):
                continue
            grl = gr.lower()
            if any(h in grl for h in HEDGE):
                continue
            ok, why = False, ''
            cands = agree.get(s, set())
            gs = {gg for gg, _ in cands}
            if len(gs) == 1 and len({so for _, so in cands}) >= 3:
                # unanimous: every PARSED row with this surface uses this gloss, 3+ songs
                ok, why = True, f'exact-surface unanimous x{len(cands)} in {len({so for _, so in cands})} songs'
            elif s in CLOSED and CLOSED[s] in g.lower().replace('-', ' '):
                ok, why = True, 'closed-class canonical sense'
            # (b) prose-overlap rule REMOVED 2026-11-06: too lax, launders
            # mismatches into PARSED (e.g. omiti->the-manifestation).
            # Prose-supported rows stay AMBIGUOUS with their cited gloss.
            if ok:
                row['status'] = 'PARSED'
                o['grounds'] = gr + f' [deambig audit: {why}; machine-proposed]'
                tok['quick_gloss'] = g
                ch += 1
                tot['parsed'] += 1
            else:
                tot['stays'] += 1
        if ch:
            t1[0]['history'].append({'gloss': f'deambig audit: +{ch} AMBIGUOUS->PARSED (strict evidence rule)', 'reason': 'machine audit, machine-proposed', 'date': '2026-11-06'})
            json.dump(t1, open(tp, 'w'), indent=1, ensure_ascii=False)
            json.dump(l0, open(lp, 'w'), indent=1, ensure_ascii=False)
        print(f'{song}: promoted {ch}')
    print('TOTAL', dict(tot))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
