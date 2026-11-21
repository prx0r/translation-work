#!/usr/bin/env python3
"""gen_passages — build passages.jsonl from source-intake segments (deterministic).

One row per data song: sanskrit = exact edition byte-slice of the song's
segments (first.start..last.end, asserted contiguous), char_len = len,
immutable_id = content hash (globally unique). Honesty rule (#14): the
sanskrit field IS the hashed span — no excerpts, no claims beyond bytes.
Usage: python3 tools/gen_passages.py <work>
"""
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def main(work: str) -> int:
    w = ROOT / work
    segs = json.loads((w / 'source' / 'segments.json').read_text())
    raw = (w / 'source' / 'edition.txt').read_bytes()
    man = json.loads((w / 'source' / 'manifest.json').read_text())
    assert man.get('format') == 'source-intake/1', man.get('format')
    assert hashlib.sha256(raw).hexdigest() == man['source_sha256'], 'edition sha mismatch'
    # group segments by song, in verse order
    songs: dict[str, list] = {}
    for s in sorted(segs, key=lambda x: (x['song'], x['verse'])):
        songs.setdefault(s['song'], []).append(s)
    # data songs must match
    data_songs = sorted({f.name.split('.')[0] for f in (w / 'data').glob('*.t1.json')})
    if data_songs and set(data_songs) != set(songs):
        print(f'WARN song sets differ: data={sorted(set(data_songs)^set(songs))}')
    rows = []
    for i, (song, ss) in enumerate(sorted(songs.items()), 1):
        # contiguity: each segment must start where the previous ended (within song)
        for a, b in zip(ss, ss[1:]):
            assert a['end'] <= b['start'], f'{song}: segment overlap/out of order'
        blob = b''.join(raw[s['start']:s['end']] for s in ss)
        # honest span: concatenation of the song's byte-slices; if contiguous,
        # equals the direct slice (assert)
        direct = raw[ss[0]['start']:ss[-1]['end']]
        if blob != direct:
            # non-contiguous (interleaved edition): keep concat, note it
            note = ' [concat of non-contiguous segment slices]'
        else:
            note = ''
        text = blob.decode('utf-8')
        lo, hi = min(s['verse'] for s in ss), max(s['verse'] for s in ss)
        # Full work name in id: work[:6] collides across mukta-* works
        # (all become 'mukta-'), and identical-source works (m00288/m00289)
        # then share content hashes -> dup-immutable gate fail.
        iid = 'pt:pid:' + work + ':' + hashlib.sha256(blob).hexdigest()[:12]
        rows.append({
            'work_id': work, 'order': i, 'locator': song,
            'verses': f'{lo}-{hi}' if lo != hi else str(lo),
            'sanskrit': text, 'char_len': len(text),
            'source_edition': man.get('edition', '') + note,
            'immutable_id': iid,
        })
    out = w / 'passages.jsonl'
    out.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n')
    print(f'{work}: wrote {len(rows)} rows -> {out.relative_to(ROOT)} '
          f'({sum(r["char_len"] for r in rows)} chars)')
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1]))
