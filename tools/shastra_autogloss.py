#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, sys, difflib, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from workcfg import source_spans

ROOT = pathlib.Path(__file__).resolve().parent.parent


def parse_t1doc(path):
    text = path.read_text(encoding='utf-8')
    out = []
    for m in re.finditer(r'\[and\]-(.*?)\(\s*([^()\n]{1,120}?)\s*\)', text, re.S):
        pre, surf = m.group(1), m.group(2).strip()
        tail = pre.strip().split('\n')[-1]
        tail = re.sub(r'^"(?:\[and\]-)?', '', tail).strip()
        tail = re.sub(r'^\[and\]-', '', tail).strip()
        gloss = tail.strip("'\" ").strip()
        ln = text[:m.start()].count('\n') + 1
        if surf and gloss and '(' not in surf and ')' not in surf and '(' not in gloss:
            out.append((surf, gloss, ln))
    return out


def is_paratext(t):
    return (t in ('|', '||', '|]', '(page', '(saṃṣi.', 'END', 'OF', 'FILE')
            or re.fullmatch(r'#+', t) or re.fullmatch(r'\([a-z]+\.', t)
            or re.fullmatch(r'\(page \d+\)', t) or re.fullmatch(r'\(\d+\)?', t)
            or re.fullmatch(r'\(\d+\|\d+\|\d+\)', t) or re.fullmatch(r'\d+\)?', t)
            or re.fullmatch(r'[a-zā-īūṛḷṃḥṅñṭḍṇśṣ]{1,4}\.', t))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--song', required=True)
    ap.add_argument('--verse', type=int, required=True)
    ap.add_argument('--v1', required=True)
    ap.add_argument('--work', default='ipvv')
    ap.add_argument('--mod', default=None, help='output module name (valid python ident)')
    args = ap.parse_args()
    src = source_spans(args.work)[args.verse]
    mp = json.loads((ROOT / args.work / 'chunk-song-map.json').read_text())
    chunk_id = next(c for c, s in mp.items() if s == args.song)
    t1path = ROOT / args.work / f'T1-{chunk_id}.md'
    doc = parse_t1doc(t1path)
    dlem = [d[0] for d in doc]
    sm = difflib.SequenceMatcher(None, src, dlem, autojunk=False)
    mapping = {}
    for tag, a1, a2, b1, b2 in sm.get_opcodes():
        if tag == 'equal':
            for a, b in zip(range(a1, a2), range(b1, b2)):
                mapping[a] = doc[b]
    rows = [json.loads(l) for l in open(args.v1)]
    v1lem = [r.get('lemma_iast', '') for r in rows]
    sm2 = difflib.SequenceMatcher(None, src, v1lem, autojunk=False)
    v1map = {}
    for tag, a1, a2, b1, b2 in sm2.get_opcodes():
        if tag == 'equal':
            for a, b in zip(range(a1, a2), range(b1, b2)):
                v1map[a] = rows[b]
    G = []
    for i, tok in enumerate(src):
        if is_paratext(tok):
            continue
        if i in mapping:
            surf, gloss, ln = mapping[i]
            if '(' not in gloss and ')' not in gloss:
                G.append((i, gloss, f'T1D L{ln} (matched {surf})'))
                continue
        if i in v1map:
            r = v1map[i]
            g = r.get('literal_gloss', '')
            if g and '(' not in g and ')' not in g:
                G.append((i, g, f"v1 rows ({r.get('id','?')})"))
    mod = args.mod or ('Gauto_' + args.song.replace('-', '_'))
    out = ROOT / args.work / 'cm' / f'{mod}.py'
    lines = ['Gauto = [']
    for i, gl, gr in G:
        lines.append(f' ({i}, {repr(gl)}, {repr(gr)}),')
    lines.append(']')
    out.write_text('\n'.join(lines) + '\n')
    print(f'{args.song}: src={len(src)} doc_pairs={len(doc)} mapped={len(mapping)} v1mapped={len(v1map)} G={len(G)} mod={mod}')


if __name__ == '__main__':
    main()
