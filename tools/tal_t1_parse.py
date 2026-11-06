#!/usr/bin/env python3
"""tal_t1_parse — legacy TAL T1.md chains -> per-verse token rows (no glosses yet).

Chain format: `## <song>-pNN (A.B-C.D)` header + ONE `[and]-`-prefixed line,
verses separated by `/`, `@` marks sandhi splits, `:Cxx` mangala headers.
Surfaces are verified against workcfg taloka spans with difflib (scaffold
pattern from shastra_merge): every span token must be covered exactly once;
unmatched heads are recorded as headers (mangala/rubrics, never glossed).

Output: <work>/working-t1-<song>.json [{verse_id, song, verse, tokens:
[{surface, quick_gloss: ''}], source_sha}] + <work>/T1.l0.report.txt style
report to stdout. quick_gloss filled later (beam tal_gloss / hand).
Usage: python3 tools/tal_t1_parse.py --work tantraloka-a23 --song tal-a23
"""
from __future__ import annotations
import argparse, hashlib, json, re, difflib, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import workcfg  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--song', required=True)
    a = ap.parse_args()
    w = ROOT / a.work
    text = (w / 'T1.md').read_text()
    secs = re.findall(r'## (\S+) \((.*?)\)\n(.*?)(?=\n## |\Z)', text, re.S)
    spans = workcfg.source_spans(a.work)
    verses = sorted(spans)
    all_toks = [t for v in verses for t in spans[v]]
    src_sha = hashlib.sha256(' '.join(all_toks).encode()).hexdigest()[:16]

    out, ptr, headers = [], 0, []
    for header, vrange, body in secs:
        m = re.search(r'(\d+)\.(\d+)-(\d+)\.(\d+)', vrange)
        if not m:
            print(f'SKIP {header}: unparsable range {vrange!r}')
            continue
        lo, hi = int(m.group(2)), int(m.group(4))
        want = [t for v in range(lo, hi + 1) for t in spans.get(v, [])]
        blob = re.sub(r'\[and\]-', ' ', body)
        blob = re.sub(r'\[is\]', ' ', blob)
        toks = [t for t in blob.split() if t not in ('/', '|')]
        sm = difflib.SequenceMatcher(None, want, toks, autojunk=False)
        w2t = {}
        for tag, a1, a2, b1, b2 in sm.get_opcodes():
            if tag == 'equal':
                for wa, wb in zip(range(a1, a2), range(b1, b2)):
                    w2t[wa] = wb
        if len(w2t) != len(want):
            missing = [want[i] for i in range(len(want)) if i not in w2t][:8]
            print(f'GAP {header}: covered {len(w2t)}/{len(want)} e.g. {missing}')
            return 1
        # slice per verse in span order
        k = 0
        for v in range(lo, hi + 1):
            sv = spans.get(v, [])
            vt = [toks[w2t[k + j]] for j in range(len(sv))]
            k += len(sv)
            out.append({'verse_id': f'{a.song}-v{v:02d}', 'song': a.song, 'verse': v,
                        'tokens': [{'surface': s, 'quick_gloss': ''} for s in vt],
                        'source_sha': src_sha})
        # header = toks before first matched token
        first_b = min(w2t.values())
        head = toks[:first_b]
        if head:
            headers.append((header, ' '.join(head)[:120]))
    (w / f'working-t1-{a.song}.json').write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f'wrote {len(out)} verses, source_sha={src_sha}')
    for h, txt in headers:
        print(f'HEADER {h}: {txt}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
