#!/usr/bin/env python3
"""shastra_charfill — assemble glosses for uncovered REAL tokens of one IPVV chunk.

Sources, in priority order (assemblage only — nothing is authored here):
  1. v1/full tarball L0 rows by char-span overlap on the bundle source text
     (measured 89% real-token coverage repo-wide)
  2. exact (normalized) surface match in the frozen T1-*.md paren glosses
  3. standard-particle dictionary
Everything else goes to <song>-residual.json for hand glossing (never faked).

Output: ipvv/cm/<song>_Gchar.py — entries for tokens NOT already in data.
Run shastra_merge.py --gtables <song>_Gchar afterwards to fold them in.
"""
from __future__ import annotations
import argparse, json, re, sys, glob, pathlib, difflib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from workcfg import source_spans

ROOT = pathlib.Path(__file__).resolve().parent.parent

PARTICLES = {
    'iti': 'thus', 'ca': 'and', 'tu': 'but', 'hi': 'for', 'api': 'too', 'eva': 'indeed',
    'tatra': 'there', 'yadi': 'if', 'nanu': 'surely', 'atha': 'now', 'vā': 'or', 'na': 'not',
    'no': 'not', 'mā': 'not', 'katham': 'how', 'kasmāt': 'why', 'kim': 'what', 'kaḥ': 'who',
    'kā': 'who', 'ke': 'who', 'kecit': 'some', 'kaścit': 'someone', 'saḥ': 'he', 'sā': 'she',
    'tat': 'that', 'te': 'they', 'tān': 'them', 'tam': 'him', 'tām': 'her', 'etad': 'this',
    'etat': 'this', 'idam': 'this', 'idaṃ': 'this', 'iyam': 'this', 'ayam': 'this',
    'atra': 'here', 'yatra': 'where', 'sarva': 'all', 'sarve': 'all', 'yataḥ': 'thence',
    'tataḥ': 'thence', 'tatas': 'thence', 'yatas': 'from-which', 'tasmāt': 'thence',
    'yathā': 'as', 'tathā': 'thus', 'evam': 'thus', 'sati': 'being', 'asti': 'is',
    'syāt': 'would-be', 'bhavati': 'becomes', 'āha': 'says', 'brūte': 'says', 'ucyate': 'is-said',
    'kācit': 'some', 'yā': 'which', 'yaḥ': 'who', 'yad': 'which', 'yat': 'which',
    'sac': 'and', 'sa': 'it', 'sā': 'she', 'tasya': 'of-that', 'tasyāḥ': 'of-that',
    'yasya': 'of-which', 'kasya': 'of-whom', 'asya': 'of-this', 'eṣa': 'this', 'eṣā': 'this',
    'ka': 'what', 'kva': 'where', 'kutra': 'where', 'kvacin': 'sometimes', 'kadācit': 'sometimes',
    'nūnam': 'surely', 'vai': 'indeed', 'nu': 'indeed', 'dhi': 'indeed', 'caḥ': 'and',
    'iti': 'thus', 'cau': 'and', 'tu': 'but', 'api': 'too', 'eva': 'indeed',
}


def is_paratext(t: str) -> bool:
    """Editorial apparatus is never glossed (contract: paratext never enters T1/L0)."""
    if '|' in t:
        return True  # ASCII pipe never in Sanskrit: editorial refs (3|249), daṇda splits
    if re.search(r'\([^)]*[?]', t):
        return True  # editorial uncertainty: bādhe.....(?)
    return bool(
        t in ('|', '||', '|]', '(page', '(saṃṣi.', 'END', 'OF', 'FILE')
        or re.fullmatch(r'#+', t)
        or re.fullmatch(r'\([a-zā-īūṛḷṃḥṅñṭḍṇśṣ]+\.', t)
        or re.fullmatch(r'\(page \d+\)', t)
        or re.fullmatch(r'\(\d+\)?', t)
        or re.fullmatch(r'\(\d+\|\d+\|\d+\)', t)
        or re.fullmatch(r'\([^)]{1,24}\)', t)
        or re.fullmatch(r'[a-zā-īūṛḷṃḥṅñṭḍṇśṣ]{1,4}\.', t)
        or re.fullmatch(r'\d+\)?', t)
    )



def find_bundle(chunk_id: str):
    # bundle filenames hyphenate dots: chunkG-k1.2.7... -> chunkG-k1-2-7-...
    for cand in (chunk_id, chunk_id.replace('.', '-')):
        p = ROOT / 'ipvv' / 'published' / f'pt-passage-ipvv-{cand}-md.json'
        if p.exists():
            return json.loads(p.read_text())
    hits = glob.glob(str(ROOT / 'ipvv' / 'published' / f'pt-passage-ipvv-{chunk_id.split("-")[0]}-*.json'))
    return json.loads(open(hits[0]).read_text()) if hits else None


def find_rows(chunk_id: str):
    for d in ('/tmp/opencode/r2/v1/translations/_stack/ipvv/l0_v1',
              '/tmp/opencode/r2/full/translations/_stack/ipvv/l0'):
        for v in (chunk_id, chunk_id.replace('.', '-')):
            p = pathlib.Path(d) / f'{v}.l0.jsonl'
            if p.exists():
                return p
    return None


def doc_paren_index(chunk_id: str):
    """normalized surface -> (gloss, line) from the frozen T1 doc, first occurrence wins."""
    p = ROOT / 'ipvv' / f'T1-{chunk_id}.md'
    out = {}
    if not p.exists():
        return out
    text = p.read_text(encoding='utf-8')
    for m in re.finditer(r'\[and\]-(.*?)\(\s*([^()\n]{1,120}?)\s*\)', text, re.S):
        pre, surf = m.group(1), m.group(2).strip()
        tail = pre.strip().split('\n')[-1]
        tail = re.sub(r'^"(?:\[and\]-)?', '', tail).strip()
        tail = re.sub(r'^\[and\]-', '', tail).strip()
        gloss = tail.strip("'\" ").strip()
        ln = text[:m.start()].count('\n') + 1
        if surf and gloss and '(' not in gloss and ')' not in gloss:
            key = re.sub(r'[^a-zā-īūṛḷṃḥṅñṭḍṇśṣ]', '', surf.lower())
            out.setdefault(key, (gloss, ln, surf))
    return out


def covered_from_data(song: str, src):
    """Re-derive source idx covered by current data (order-preserving surface match)."""
    tp = ROOT / 'ipvv' / 'data' / f'{song}.t1.json'
    if not tp.exists():
        return set()
    t1 = json.loads(tp.read_text())
    covered, ptr = set(), 0
    for tok in t1[0]['tokens']:
        s = tok['surface']
        try:
            ptr = src.index(s, ptr)
        except ValueError:
            continue
        covered.add(ptr)
        ptr += 1
    return covered


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--song', required=True)
    ap.add_argument('--verse', type=int, required=True)
    ap.add_argument('--work', default='ipvv')
    args = ap.parse_args()
    mp = json.loads((ROOT / args.work / 'chunk-song-map.json').read_text())
    chunk_id = next(c for c, s in mp.items() if s == args.song)
    src = source_spans(args.work)[args.verse]
    bundle = find_bundle(chunk_id)
    rows_p = find_rows(chunk_id)
    covered = covered_from_data(args.song, src)

    # 1) char-span v1 rows -> token map (best overlap wins)
    charmap = {}
    v1count = 0
    if bundle:
        st = bundle['source']['text']
        spans = [(m.start(), m.end()) for m in re.finditer(r'\S+', st)]
        assert len(spans) == len(src), f'token mismatch {len(spans)} vs {len(src)}'
        rows = [json.loads(l) for l in open(rows_p)] if rows_p else []
        v1count = len(rows)
        for i, tok in enumerate(src):
            if is_paratext(tok) or i in covered:
                continue
            s, e = spans[i]
            best = None
            for r in rows:
                if r.get('status') == 'FAILED':
                    continue  # never launder FAILED into coverage
                ov = max(0, min(e, r['char_end']) - max(s, r['char_start']))
                if ov > 0 and (best is None or ov > best[0]):
                    best = (ov, r)
            if best:
                charmap[i] = best[1]

    # 2) T1-doc normalized exact index
    docidx = doc_paren_index(chunk_id)

    G, residual, src_flags = [], [], {'v1': 0, 'doc': 0, 'part': 0}
    for i, tok in enumerate(src):
        if is_paratext(tok) or i in covered:
            continue
        gl = None
        r = charmap.get(i)
        if r:
            g = r.get('literal_gloss', '')
            if g and '(' not in g and ')' not in g:
                gl = (g, f"v1 rows {r.get('id','?')} char-span {r.get('char_start')}-{r.get('char_end')}")
                src_flags['v1'] += 1
        if gl is None:
            key = re.sub(r'[^a-zā-īūṛḷṃḥṅñṭḍṇśṣ]', '', tok.lower()).rstrip('mḥḥ')
            hit = docidx.get(key) or docidx.get(re.sub(r'[^a-zā-īūṛḷṃḥṅñṭḍṇśṣ]', '', tok.lower()))
            if hit:
                g, ln, surf = hit
                gl = (g, f'T1D L{ln} ({surf}) exact-surface')
                src_flags['doc'] += 1
        if gl is None:
            ptok = tok.strip(',;:')
            pg = PARTICLES.get(ptok) or PARTICLES.get(ptok.lower())
            if pg and re.fullmatch(r'[a-zā-īūṛḷṃḥṅñṭḍṇśṣ]+', ptok, re.I):
                gl = (pg, 'standard-particle (grammar)')
                src_flags['part'] += 1
        if gl:
            G.append((i, gl[0], gl[1]))
        else:
            residual.append({'i': i, 'surface': tok})

    mod = args.song.replace('-', '_') + '_Gchar'
    out = ROOT / args.work / 'cm' / f'{mod}.py'
    lines = [f'Gchar = [']
    for i, g, gr in sorted(G):
        lines.append(f' ({i}, {g!r}, {gr!r}),')
    lines.append(']')
    out.write_text('\n'.join(lines) + '\n')
    (ROOT / args.work / 'cm' / f'{args.song}-residual.json').write_text(
        json.dumps({'song': args.song, 'residual': residual}, indent=1, ensure_ascii=False))
    real = sum(1 for t in src if not is_paratext(t))
    stats = {'song': args.song, 'verse': args.verse, 'chunk_id': chunk_id,
             'v1_path': str(rows_p) if rows_p else None, 'mod': mod,
             'real': real, 'covered': len(covered), 'gchar': len(G),
             'residual': len(residual), 'v1rows': v1count, 'sources': src_flags}
    (ROOT / args.work / 'cm' / f'{args.song}.charfill.json').write_text(
        json.dumps(stats, indent=1, ensure_ascii=False))
    print(f'{args.song}: real={real} covered={len(covered)} +Gchar={len(G)} '
          f'({src_flags}) residual={len(residual)} v1rows={v1count} mod={mod}')
    if v1count == 0:
        print(f'FAIL: no v1/full rows found for {chunk_id} — re-provide row tarballs '
              f'(/tmp/opencode/r2/{{v1,full}}/translations/_stack/ipvv/) before continuing')
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
