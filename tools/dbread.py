#!/usr/bin/env python3
"""dbread — read-only bridge from translation-work to the portable openpatala box DB.

The box DB (s3://patala/openpatala/box-2026-11-06/, restored locally as
`openpatala_box`) is the identity spine: works / editions / etexts /
passages. translation-work owns its files; this tool only READS the DB to
answer: what is this work (identity), what spans need translation (passages),
is our coverage complete, and what IDs stamp provenance at bundle time
(BACKBONE §5 spec #3).

DSN: $OPENPATALA_DSN, default postgresql://patala:patala@localhost:5432/openpatala_box
(Read-only by convention; this tool issues SELECT only. Writes go through
trika-x loaders, never from here.)

Usage:
  python3 tools/dbread.py works [--q foo]
  python3 tools/dbread.py work <db-work-id>          # work + editions + etexts + passage count
  python3 tools/dbread.py passages <db-work-id>      # citation_value list (spans to translate)
  python3 tools/dbread.py coverage <tw-work>         # DB passages vs local data files
  python3 tools/dbread.py ids <tw-work>              # provenance triple for bundles
Work keys: DB uses clean ids (tantrasara, tantraloka-a15, ipvv, <song-work>).
<tw-work> is a translation-work dir (ipvv, tantrasara-a01, ajadapramatrsiddhi...).
"""
from __future__ import annotations
import argparse, json, os, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DSN = os.environ.get('OPENPATALA_DSN',
                      'postgresql://patala:patala@localhost:5432/openpatala_box')

try:
    import psycopg2
except ImportError:
    print('need psycopg2', file=sys.stderr)
    raise SystemExit(2)


def con():
    return psycopg2.connect(DSN)


def cmd_works(q: str | None):
    c = con()
    cur = c.cursor()
    if q:
        cur.execute("SELECT id, preferred_title FROM works WHERE id ILIKE %s OR preferred_title ILIKE %s ORDER BY id LIMIT 30",
                    (f'%{q}%', f'%{q}%'))
    else:
        cur.execute("SELECT id, preferred_title FROM works ORDER BY id LIMIT 50")
    for wid, t in cur.fetchall():
        print(f'{wid} :: {t}')
    c.close()


def cmd_work(wid: str):
    c = con()
    cur = c.cursor()
    cur.execute("SELECT id, preferred_title FROM works WHERE id = %s", (wid,))
    w = cur.fetchone()
    if not w:
        print(f'unknown work {wid!r}')
        return 1
    print(json.dumps({"work": {"id": w[0], "title": w[1]}}, indent=1))
    cur.execute("SELECT id, title FROM editions WHERE work_id = %s", (wid,))
    print('editions:', json.dumps([{"id": e[0], "title": e[1]} for e in cur.fetchall()], indent=1)[:800])
    cur.execute("SELECT provider_id, artifact_id, text_format FROM etexts WHERE work_id = %s", (wid,))
    print('etexts:', json.dumps([{"provider": e[0], "artifact": e[1], "format": e[2]} for e in cur.fetchall()], indent=1)[:800])
    cur.execute("SELECT count(*) FROM passages WHERE work_id = %s", (wid,))
    print('passages:', cur.fetchone()[0])
    c.close()
    return 0


def db_passages(wid: str) -> list[str]:
    c = con()
    cur = c.cursor()
    cur.execute("SELECT citation_value FROM passages WHERE work_id = %s ORDER BY citation_value", (wid,))
    out = [r[0] for r in cur.fetchall()]
    c.close()
    return out


def local_songs(tw: str) -> set[str]:
    """Song ids translation-work already has data files for."""
    import sys as _s
    _s.path.insert(0, str(ROOT / 'tools'))
    from workcfg import data_dir
    songs: set[str] = set()
    if tw == 'ipvv':
        table = json.loads((ROOT / 'ipvv' / 'chunk-table.json').read_text())
        for e in table:
            dd = data_dir('ipvv', e['song'])
            if (dd / f"{e['song']}.t1.json").exists():
                songs.add(e['song'])
        return songs
    d = ROOT / tw
    if not (d / 'data').exists():
        return songs
    for f in (d / 'data').glob('*.t1.json'):
        songs.add(f.name[:-len('.t1.json')])
    return songs


def tw_to_db(tw: str) -> str:
    # DB work ids match translation-work dirs for TAL/TSA and flat works; ipvv is one DB work.
    return 'ipvv' if tw == 'ipvv' else tw


def cmd_passages(wid: str):
    for p in db_passages(wid):
        print(p)


def normalize_locator(tw: str, loc: str, chunk_map: dict | None = None) -> str:
    """DB citation_value -> translation-work song guess.
    ipvv: chunkId form (chunkA-svatyandya) via chunk-song-map (authoritative).
    tsa: tsa01-p01 -> tsa-a01 (one song per ahnika). tal: tal-a15-p01 -> tal-a15."""
    import re as _re
    if tw == 'ipvv' and chunk_map:
        hit = chunk_map.get(loc)
        if hit:
            return hit
        m = _re.fullmatch(r'chunk([A-Z])-(.*)', loc)
        if m:
            return f'chunk-{m.group(1).lower()}-{m.group(2)}'.replace('.', '-')
        return loc.lower().replace('.', '-')
    m = _re.fullmatch(r'tsa(\d+)-p\d+', loc)
    if m:
        return f'tsa-a{int(m.group(1)):02d}'
    m = _re.fullmatch(r'(tal-a\d+)-p\d+', loc)
    if m:
        return m.group(1)
    return loc


def cmd_coverage(tw: str):
    wid = tw_to_db(tw)
    want = db_passages(wid)
    have = local_songs(tw)
    cmap = None
    if tw == 'ipvv':
        cmap = json.loads((ROOT / 'ipvv' / 'chunk-song-map.json').read_text())
    missing = [p for p in want if normalize_locator(tw, p, cmap) not in have]
    extra = 'n/a (DB passages are finer-grained than songs for tsa/tal)'
    print(json.dumps({"work": tw, "db_work": wid, "db_passages": len(want),
                      "local_songs": len(have), "missing": missing}, indent=1))
    return 0 if not missing else 1


def cmd_ids(tw: str):
    """Provenance triple for bundle-time stamping (BACKBONE §5.3)."""
    wid = tw_to_db(tw)
    c = con()
    cur = c.cursor()
    cur.execute("SELECT id FROM works WHERE id = %s", (wid,))
    w = cur.fetchone()
    cur.execute("SELECT id FROM editions WHERE work_id = %s ORDER BY id", (wid,))
    eds = [r[0] for r in cur.fetchall()]
    c.close()
    from workcfg import data_dir  # noqa: E402  (import after sys.path above is fine)
    _ = data_dir
    ledger = None
    if tw == 'ipvv':
        ledger = 'ipvv/chunk-table.json'
    else:
        cand = ROOT / tw / 'passages.jsonl'
        ledger = f'{tw}/passages.jsonl' if cand.exists() else None
    out = {"openpatala_work_id": w[0] if w else None,
           "edition_ids": eds,
           "ledger": ledger}
    print(json.dumps(out, indent=1))
    return 0 if w else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='c', required=True)
    w = sub.add_parser('works');
    w.add_argument('--q', default=None)
    o = sub.add_parser('work');
    o.add_argument('id')
    p = sub.add_parser('passages');
    p.add_argument('work')
    c = sub.add_parser('coverage');
    c.add_argument('work')
    i = sub.add_parser('ids');
    i.add_argument('work')
    a = ap.parse_args()
    sys.path.insert(0, str(ROOT / 'tools'))
    if a.c == 'works':
        cmd_works(a.q)
    elif a.c == 'work':
        return cmd_work(a.id)
    elif a.c == 'passages':
        cmd_passages(a.work)
    elif a.c == 'coverage':
        return cmd_coverage(a.work)
    elif a.c == 'ids':
        return cmd_ids(a.work)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
