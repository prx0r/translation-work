#!/usr/bin/env python3
"""Build working-t1-{song}.json for gitarthasangraha from pinned segments.

Canonical intake builder (reusable): reads edition bytes + segments.json,
emits one working-t1 entry per content segment with song-local verse numbers.
Paratext policy: drop machine markers (standalone | / ||, verse locators
like 1-2, ### provenance lines). Keep ALL other words (mula, prose headers,
sangraha verses, colophon words) as content — coverage first; colophon
exclusions (if any) are an assessor act in review, never silent drops.
Each entry records its absolute span + byte offsets for provenance.
"""
from __future__ import annotations
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORK = ROOT / 'gitarthasangraha'
ED = WORK / 'source' / 'edition.txt'
SEG = WORK / 'source' / 'segments.json'

MARKER = re.compile(r'^\d+-\d+$')
_SPLIT = re.compile(r'\s*(?:\|\|?|!|\d+-\d+)\s*')


def cite_parts_of(text: str) -> list[str]:
    """Byte-exact cite chunks: source span split on markers. Each chunk is a
    verbatim source substring (whitespace-flattened at check time), so the
    assembled `sanskrit_cite` (joined by ' | ') always validates."""
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith('###')]
    parts = _SPLIT.split(' '.join(lines))
    out = []
    for p in (x.strip() for x in parts):
        if not p:
            continue
        if re.fullmatch(r'[\d\-|]+', p):
            continue
        out.append(p)
    return out


def tokens_of(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        if line.strip().startswith('###'):
            continue  # provenance block
        for w in line.split():
            if w in {'|', '||'}:
                continue
            if MARKER.fullmatch(w):
                continue  # verse locators (1-2); meaning lives in // N // prose
            out.append(w)
    return out


def main(argv: list[str]) -> int:
    only = set(argv[1:]) if len(argv) > 1 else None
    raw = ED.read_bytes()
    segs = json.loads(SEG.read_text())
    by_song: dict[str, list] = {}
    for s in segs:
        by_song.setdefault(s['song'], []).append(s)
    for song in sorted(by_song):
        if only and song not in only:
            continue
        outp = WORK / f'working-t1-{song}.json'
        if outp.exists():
            print(f'{song}: exists — skip (curated/hand-built working-t1 never overwritten)')
            continue
        entries = []
        v = 0
        for s in by_song[song]:
            text = raw[s['start']:s['end']].decode('utf-8')
            toks = tokens_of(text)
            if not toks:
                continue  # pure-paratext segment (provenance); excluded with note
            v += 1
            entries.append({
                'verse_id': f"{song}-v{v:02d}",
                'song': song, 'verse': v,
                'span': s.get('verse'), 'start': s['start'], 'end': s['end'],
                'label': s.get('label', ''),
                'source_sha': __import__('hashlib').sha256(text.encode('utf-8')).hexdigest()[:16],
                'cite_parts': cite_parts_of(text),
                'quick_english': 'SCAFFOLD pending (T1 drafted from runs at assemble)',
                'tokens': [{'surface': t, 'quick_gloss': ''} for t in toks],
            })
        (WORK / f'working-t1-{song}.json').write_text(
            json.dumps(entries, indent=1, ensure_ascii=False))
        print(f'{song}: {len(entries)} units, {sum(len(e["tokens"]) for e in entries)} tokens')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
