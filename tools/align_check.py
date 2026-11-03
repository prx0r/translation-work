"""Strict-monotonic T1<->source span alignment (sandhi-tolerant).
Pass 1: monotonic matching (multi<->multi spans, many-to-one allowed).
Pass 2: locate unmapped T1 tokens anywhere (later = inversion).
Usage: python3 tools/align_check.py [work song]"""
import json
import re
import sys

sys.path.insert(0, 'tools')
from workcfg import source_spans


def norm_tok(t):
    # Sandhi-tolerant token form (matching only — never stored):
    # strip separators; fold anusvara; strip trailing sibilant (visarga/sandhi);
    # expand long vowels (sandhi a+ā); o/e -> a (nom/indecl endings).
    t = re.sub(r"[\s\-'’.,:;|/]", '', t)
    t = t.replace('ṃ', 'm')
    t = t.replace('ḥ', '')
    t = re.sub(r'[sśṣ]$', '', t)
    t = t.replace('ā', 'aa').replace('ī', 'ii').replace('ū', 'uu')
    t = t.replace('o', 'a').replace('e', 'a')
    return t


def norm(s):
    return norm_tok(s)


def join_norm(toks):
    return ''.join(norm_tok(t) for t in toks)


def align(toks, src):
    nt = [norm_tok(t) for t in toks]
    ns = [norm_tok(t) for t in src]
    cur = 0
    covered = []  # accepted spans, for many-to-one fallback
    mapping = []
    for ti, key in enumerate(nt):
        if not key:
            mapping.append(None)
            continue
        best = None
        # fresh spans starting in [cur, cur+5): best ratio wins
        for s in range(cur, min(cur + 5, len(ns))):
            for L in range(1, 7):
                if s + L > len(ns):
                    break
                cand = ''.join(ns[s:s + L])
                if not cand:
                    continue
                if key in cand or cand in key:
                    r = max(len(key), len(cand)) / max(1, min(len(key), len(cand)))
                    if r < 2.5 and (best is None or r < best[0] or
                                    (r == best[0] and s < best[1][0])):
                        best = (r, (s, s + L))
        if best is not None:
            _, span = best
            mapping.append(span)
            covered.append(span)
            if span[1] > cur:
                cur = span[1]
            continue
        # fallback: many-to-one inside already-covered span (sandhi splits)
        done = False
        for (s, e) in covered:
            if key and key in ''.join(ns[s:e]):
                mapping.append((s, e))
                done = True
                break
        if not done:
            mapping.append(None)
    return mapping


def report(work, song, verses=None):
    spans = source_spans(work)
    t1 = {o['verse']: o for o in json.load(open(f'{work}/data/{song}.t1.json'))}
    allok = True
    for v in sorted(spans):
        if verses and v not in verses:
            continue
        toks = [t['surface'] for t in t1[v]['tokens']]
        src = spans[v]
        mapping = align(toks, src)
        # pass 2: locate unmapped
        unm, inv = [], []
        for ti, m in enumerate(mapping):
            if m is not None:
                continue
            key = norm(toks[ti])
            found = [s for s in range(len(src)) if key and key in norm(src[s])]
            unm.append((toks[ti], found))
            # inversion if found far ahead while later tokens matched before it
            later = [s for tj, m in enumerate(mapping) if m is not None
                     and tj > ti for s in [m[0]]]
            if found and later and min(found) > max(later):
                inv.append((toks[ti], found[0], max(later)))
        covered = set()
        for m in mapping:
            if m:
                covered.update(range(m[0], m[1]))
        gaps = [src[i] for i in range(len(src)) if i not in covered]
        ok = not inv and not unm and not gaps
        allok = allok and ok
        print(f'v{v}: {"OK" if ok else "ISSUES"} inv={len(inv)} '
              f'unmapped={len(unm)} gaps={len(gaps)} '
              f'({len(toks)} T1 toks, {len(src)} src toks)')
        for t, f, l in inv[:8]:
            print(f'   INV: {t[:40]!r} at src {f}, after src {l}')
        for t, f in unm[:10]:
            print(f'   UNMAPPED: {t[:50]!r} found@{f[:4]}')
        if gaps:
            print('   GAPS:', gaps[:10])
    return allok


if __name__ == '__main__':
    work = sys.argv[1] if len(sys.argv) > 1 else 'tantrasara-a01'
    song = sys.argv[2] if len(sys.argv) > 2 else 'tsa-a01'
    ok = report(work, song)
    print('ALIGN:', 'CLEAN' if ok else 'HAS ISSUES')
