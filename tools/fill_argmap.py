#!/usr/bin/env python3
"""tools/fill_argmap.py --work vbt --song vbt-p01 [--song ...]

Fills traces.l0_ids (from working-l0-*.json) and sanskrit_sha (per-song
sha256[:16] over joined source tokens) on working-argmap-<song>.json,
then runs schemas.argmap.validate + shared-sentence scan. Content
(question/premises/inference) is hand-written; this only completes the
mechanical fields and gates them.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'schemas'))
import workcfg
from argmap import validate


def norm(s: str) -> str:
    return re.sub(r'[^a-z0-9 ]', '', s.lower()).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--song', action='append', required=True)
    args = ap.parse_args()

    sp = workcfg.source_spans(args.work)
    allsp = workcfg.source_spans(args.work)
    l0_ids, l0_by, t1v = set(), {}, set()
    w = ROOT / args.work
    for f in sorted(w.glob('working-l0-*.json')):
        for r in json.loads(f.read_text(encoding='utf-8')):
            l0_ids.add(r['id']); l0_by[r['id']] = r
    for f in sorted(w.glob('working-t1-*.json')):
        for e in json.loads(f.read_text(encoding='utf-8')):
            t1v.add(e['verse_id'])

    all_sents = {}
    rc = 0
    for song in args.song:
        p = w / ('working-argmap-%s.json' % song)
        am = json.loads(p.read_text(encoding='utf-8'))
        vs = workcfg.song_verses(args.work, song)
        src = {v: t for v, t in allsp.items() if v in vs}
        sh = hashlib.sha256((' '.join(' '.join(t) for v, t in sorted(src.items()))).encode()).hexdigest()[:16]
        errs = []
        for o in am:
            vid = o['verse_id']
            ids = sorted((r for r in l0_ids if r.startswith(vid + '-p')),
                         key=lambda x: int(x.rsplit('-p', 1)[1]))
            o['traces']['l0_ids'] = ids
            o['sanskrit_sha'] = sh
            errs += validate(o, vid, l0_ids, t1v, sh, l0_by)
            for s in o.get('premises', []) + [o.get('inference', '')]:
                if s and len(s.split()) >= 8:
                    all_sents.setdefault(norm(s), []).append((song, vid))
        p.write_text(json.dumps(am, ensure_ascii=False, indent=1), encoding='utf-8')
        print('%s: %d argmaps, sha=%s, errors=%d' % (song, len(am), sh, len(errs)))
        for e in errs[:6]:
            print('   -', e)
        rc += len(errs)
    dups = {s: v for s, v in all_sents.items() if len(v) > 1}
    if dups:
        print('SHARED LONG SENTENCES:')
        for s, v in list(dups.items())[:8]:
            print('   ', v, '|', s[:90])
        rc += len(dups)
    print('gate:', 'PASS' if rc == 0 else 'FAIL(%d)' % rc)
    return 0 if rc == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
