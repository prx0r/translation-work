#!/usr/bin/env python3
"""shastra_squeeze — Tiered honest upgrade of AMBIGUOUS *-unparsed placeholders.

Tier 1: exact surface + >=2 agreeing PARSED glosses elsewhere -> PARSED.
Tier 2: exact surface single-source or majority gloss -> AMBIGUOUS w/ cited gloss.
Tier 3: T1-doc prose mining "English (Sanskrit)" + inflection-tolerant stem match
        -> AMBIGUOUS w/ doc-cited gloss.
Tier 4: inflection-strip stem lookup in PARSED lexicon -> AMBIGUOUS composed.
Else: stays *-unparsed.

Never invents PARSED except Tier 1. All machine-proposed, needs human review.
Usage: python3 tools/shastra_squeeze.py [--only song]
Writes: per-chunk data T1/L0 in place + cm/<song>.squeeze.json report.
"""
from __future__ import annotations
import json, re, sys, glob, pathlib
from collections import defaultdict, Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from workcfg import source_spans, data_dir, chunk_id_for

ENDINGS = ['ābhyām', 'ebhyaḥ', 'ebhya', 'ānām', 'ānāṃ', 'ān', 'ena', 'eṇa', 'āya', 'asya',
           'asya', 'asya', 'sya', 'eṣu', 'eṣu', 'āni', 'āni', 'aḥ', 'āḥ', 'am', 'ām',
           'aṃ', 'āṃ', 'e', 'o', 'au', 'ai', 'ti', 'nti', 'te', 'nte', 'ate', 'yate',
           'tvena', 'tvena', 'tayā', 'taya', 'tvam', 'tvā', 'enaṃ', 'enam']

def strip_end(s: str) -> list[str]:
    out = [s]
    for e in sorted(ENDINGS, key=len, reverse=True):
        if s.endswith(e) and len(s) - len(e) >= 3:
            out.append(s[:-len(e)])
            break
    # sandhi-collapsed trailing m/n
    if s.endswith('ṃ') or s.endswith('m'):
        out.append(s[:-1])
    return out

def norm(s: str) -> str:
    return re.sub(r'[^a-zāīūṛṝḷḹēōṃḥṅñṭḍṇśṣ]', '', s.lower())

def build_parsed_lex():
    lex = defaultdict(list)  # surface -> [(gloss, srcfile)]; ONE entry per row
    seen_rows = set()
    for f in glob.glob(str(ROOT / 'ipvv' / '*' / 'data' / '*.l0.json')):
        for r in json.load(open(f)):
            if r.get('status') == 'PARSED' and 'squeeze' not in r.get('citation', ''):
                o = (r.get('options') or [{}])[0]
                g = o.get('gloss', '')
                if g and not g.endswith('-unparsed') and '(' not in g and ')' not in g:
                    key = (f, r.get('id'))
                    if key in seen_rows:
                        continue
                    seen_rows.add(key)
                    lex[r['surface']].append((g, f))
                    if norm(r['surface']) != r['surface']:
                        lex[norm(r['surface'])].append((g, f))
    return lex

def build_doc_index():
    """English (Sanskrit) prose pairs from all T1.md, first occurrence wins."""
    idx = {}
    for md in glob.glob(str(ROOT / 'ipvv' / 'chunk*' / 'T1.md')):
        text = open(md).read()
        for m in re.finditer(r'([A-Za-z][A-Za-z ,\-/]{2,60}?)\(\s*([a-zāīūṛḷṃḥṅñṭḍṇśṣ\-]{3,40})\s*\)', text):
            eng, san = m.group(1).strip(), m.group(2).strip()
            eng = re.sub(r'^(the|a|an|of|in|by|with|as|is|are|that|this)\s+', '', eng, flags=re.I).strip()
            gloss = re.sub(r'\s+', '-', eng.lower()).strip('-')[:60]
            if gloss and '(' not in gloss:
                idx.setdefault(norm(san), (gloss, f'{pathlib.Path(md).parent.name}/T1.md'))
    return idx

def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default=None)
    a = ap.parse_args()
    lex = build_parsed_lex()
    doc = build_doc_index()
    print(f'lexicon: {len(lex)} keys; doc pairs: {len(doc)}')
    table = json.load(open(ROOT / 'ipvv' / 'chunk-table.json'))
    tot = Counter()
    for e in table:
        song = e['song']
        if a.only and song != a.only:
            continue
        dd = data_dir('ipvv', song)
        tp, lp = dd / f'{song}.t1.json', dd / f'{song}.l0.json'
        t1 = json.load(open(tp)); l0 = json.load(open(lp))
        changed = 0
        for tok, row in zip(t1[0]['tokens'], l0):
            o = (row.get('options') or [{}])[0]
            if row.get('status') != 'AMBIGUOUS' or not o.get('gloss', '').endswith('-unparsed'):
                continue
            surf = tok['surface']
            cands = lex.get(surf, []) or lex.get(norm(surf), [])
            if cands:
                c = Counter(g for g, _ in cands)
                (top, n) = c.most_common(1)[0]
                nsongs = len(set(s for g, s in cands if g == top))
                if len(c) == 1 and nsongs >= 2:
                    ng, st, gr = top, 'PARSED', f'cross-chunk exact x{n} in {nsongs} songs agree ({top}); machine-proposed'
                    tier = 't1'
                else:
                    ng, st = top, 'AMBIGUOUS'
                    gr = f'cross-chunk exact ({n}/{len(cands)} agree: {top}); AMBIGUOUS, needs hand check (machine-proposed)'
                    tier = 't2'
            else:
                # Tier 3: doc prose stem
                hit = None
                for cand in [norm(surf)] + strip_end(norm(surf)):
                    if cand in doc:
                        hit = (cand, doc[cand]); break
                if hit:
                    ng = hit[1][0]
                    st, gr, tier = 'AMBIGUOUS', f'T1-doc prose ({hit[1][1]}): ({hit[0]}); stem-matched to {surf}; AMBIGUOUS (machine-proposed)', 't3'
                else:
                    # Tier 4: stem lexicon
                    hit2 = None
                    for cand in strip_end(norm(surf)):
                        if cand in lex and cand != norm(surf):
                            cc = Counter(lex[cand])
                            hit2 = (cand, cc.most_common(1)[0][0], len(lex[cand])); break
                    if hit2:
                        ng = hit2[1]
                        st, gr, tier = 'AMBIGUOUS', f'stem {hit2[0]} x{hit2[2]} PARSED rows ({hit2[1]}); inflection-strip from {surf}; AMBIGUOUS (machine-proposed)', 't4'
                    else:
                        continue
            tok['quick_gloss'] = ng
            row['options'] = [{'gloss': ng, 'rank': 1, 'source': 't1-draft', 'grounds': gr}]
            row['status'] = st
            row['citation'] = f'squeeze {tier} (was *-unparsed placeholder)'
            changed += 1
            tot[tier] += 1
        if changed:
            t1[0]['history'].append({'gloss': f'squeeze: {changed} AMBIGUOUS upgraded (t1/t2/t3/t4, machine-proposed)', 'reason': 'tiered honest scripting', 'date': '2026-11-06'})
            json.dump(t1, open(tp, 'w'), indent=1, ensure_ascii=False)
            json.dump(l0, open(lp, 'w'), indent=1, ensure_ascii=False)
        print(f'{song}: upgraded {changed}')
    print('TOTAL', dict(tot))
    json.dump(dict(tot), open(ROOT / 'ipvv' / 'cm' / 'squeeze-report.json', 'w'), indent=1)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
