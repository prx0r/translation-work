#!/usr/bin/env python3
"""Build working-t1-{song}.json for sivasutravimarsini from pinned segments.

Token rules (KSTS/Muktabodha print conventions):
- join wrap-hyphen continuations (xxx- + yyy -> xxxyyy)
- drop standalone daṇḍas (|, ||), page markers (p. N)), locators (N, N-M)
- strip [ ] bracket chars (keep the gloss words — they are Kṣemarāja's own)
- drop ### provenance lines
Everything else (mula + commentary prose + colophons) is content.
"""
from __future__ import annotations
import json, pathlib, re, sys, hashlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORK = ROOT / 'sivasutravimarsini'


def tokens_of(text: str) -> list[str]:
    words = []
    for line in text.splitlines():
        if line.strip().startswith('###'):
            continue
        # page markers like 'p. 4)' live on own lines — drop the line
        if re.fullmatch(r'\s*p\.\s*\d+\)\s*', line):
            continue
        words.extend(line.split())
    # join wrap-hyphens
    joined, i = [], 0
    while i < len(words):
        w = words[i]
        if w.endswith('-') and i + 1 < len(words):
            nxt = words[i + 1]
            if nxt not in {'|', '||'} and not re.fullmatch(r'\d+\)?', nxt):
                joined.append(w[:-1] + nxt)
                i += 2
                continue
        joined.append(w)
        i += 1
    out = []
    for w in joined:
        if w in {'|', '||'}:
            continue
        if re.fullmatch(r'\d+-\d+', w):
            continue
        if re.fullmatch(r'\d+\)?', w):
            continue
        w = w.replace('[', '').replace(']', '')
        if not w:
            continue
        out.append(w)
    return out


def main(argv: list[str]) -> int:
    only = set(argv[1:]) if len(argv) > 1 else None
    sys.path.insert(0, str(ROOT / 'tools'))
    import workcfg
    raw = (WORK / 'source' / 'edition.txt').read_bytes()
    txt = raw.decode('utf-8')
    segs = json.loads((WORK / 'source' / 'segments.json').read_text())
    # Song-level source sha (matches validate_song/proof computation over
    # workcfg spans, markers included).
    spans = workcfg.source_spans('sivasutravimarsini') or {}
    by = {}
    for s in segs:
        by.setdefault(s['song'], []).append(s)
    song_sha = {}
    for song, items in by.items():
        vs = sorted({x['verse'] for x in items})
        song_sha[song] = hashlib.sha256(
            ' '.join(' '.join(spans[v]) for v in vs).encode()).hexdigest()[:16]
    for song in sorted(by):
        if only and song not in only:
            continue
        outp = WORK / f'working-t1-{song}.json'
        if outp.exists():
            print(f'{song}: exists — skip')
            continue
        entries = []
        for s in by[song]:
            text = raw[s['start']:s['end']].decode('utf-8')
            toks = tokens_of(text)
            if not toks:
                continue
            entries.append({
                'verse_id': s['verse_id'], 'song': song, 'verse': s['verse'],
                'span': s['verse'], 'start': s['start'], 'end': s['end'],
                'label': s.get('label', ''),
                'source_sha': song_sha[song],
                'cite_parts': [text.strip()],
                'quick_english': 'SCAFFOLD pending',
                'tokens': [{'surface': t, 'quick_gloss': ''} for t in toks],
            })
        outp.write_text(json.dumps(entries, indent=1, ensure_ascii=False))
        print(f'{song}: {len(entries)} units, {sum(len(e["tokens"]) for e in entries)} tokens')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
