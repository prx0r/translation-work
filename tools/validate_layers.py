#!/usr/bin/env python3
"""validate_layers.py — deterministic validation of the translations we already have.

No model, no generation, no network. Every l3/l2 row in translation-work names
the L0 segments it answers (`l0_ids`) and every work has an `.l0.json` that
enumerates the source segments. That is enough to check the failures that
actually ship:

  COVERAGE   every L0 segment of the song is referenced by some translated row
             (a dropped clause is invisible in prose, fatal in a claim)
  PHANTOM    a row cites an L0 id that does not exist in the source
  DOUBLE     one L0 id is answered by two rows (or two rows claim the same id)
  EMPTY      a row renders nothing
  RATIO      English chars / Sanskrit chars outside a sane band, per row
  CITE       informational only: cites are sandhi-restored while L0 surfaces are
             grammatical words (tanuś vs tanuḥ), so a mismatch is expected and
             means "look here", never a defect

Output: a per-work table plus a JSON summary. Exit 0 when there are no
COVERAGE/PHANTOM/DOUBLE/EMPTY defects; RATIO and CITE are warnings (they need
eyes, not a gate).

  python3 tools/validate_layers.py                 # all works
  python3 tools/validate_layers.py --work spanda   # one work
  python3 tools/validate_layers.py --json out.json
"""
from __future__ import annotations
import argparse
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RATIO_LO, RATIO_HI = 0.15, 6.0


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r'\[[^\]]*\]', ' ', s)          # editorial brackets
    return re.sub(r'[^a-zāīūṛṝḷḹṃḥñṅśṣṭḍṇ]+', '', s)


def load(p: Path):
    try:
        d = json.loads(p.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return []
    return d if isinstance(d, list) else []


def text_of(row: dict) -> str:
    parts = []
    for k in ('l3', 'plain_english', 'lines'):
        v = row.get(k)
        if isinstance(v, list):
            parts += [str(x) for x in v]
        elif isinstance(v, str):
            parts.append(v)
    return ' '.join(parts).strip()


def check_song(work: Path, song: str, rows_path: Path) -> dict:
    rows = [r for r in load(rows_path) if isinstance(r, dict)]
    l0_path = rows_path.with_name(song + '.l0.json')
    l0 = [r for r in load(l0_path) if isinstance(r, dict)]
    out = {'work': work.name, 'song': song, 'layer': rows_path.name.rsplit('.', 2)[1],
           'rows': len(rows), 'l0_segments': len(l0),
           'empty': [], 'phantom': [], 'double': [], 'missing': [], 'ratio': [],
           'cite_miss': [], 'overlap': 0}
    if not rows:
        out['empty'].append('<no rows>')
        return out
    if not l0:
        out['l0_segments'] = None
        return out

    known = {str(r.get('id')) for r in l0 if r.get('id')}
    surfaces = ' '.join(norm(str(r.get('surface', ''))) for r in l0)
    surfaces_flat = ''.join(norm(str(r.get('surface', ''))) for r in l0)
    seen: dict[str, int] = {}
    for i, r in enumerate(rows):
        t = text_of(r)
        if not t:
            out['empty'].append(r.get('verse_id') or f'row{i}')
            continue
        ids = [str(x) for x in (r.get('l0_ids') or [])]
        for x in ids:
            if x not in known:
                out['phantom'].append(x)
            seen[x] = seen.get(x, 0) + 1
        src = str(r.get('sanskrit_cite') or '')
        if src and surfaces:
            ns = norm(src)
            if len(ns) >= 12 and ns not in surfaces_flat:
                # sources are split across segments; check word-level presence
                words = [w for w in re.split(r'\s+', src) if len(norm(w)) >= 4]
                if words and sum(1 for w in words if norm(w) in surfaces) < len(words) * 0.6:
                    out['cite_miss'].append(r.get('verse_id') or f'row{i}')
            if src:
                ratio = len(t) / max(1, len(src))
                if not (RATIO_LO <= ratio <= RATIO_HI):
                    out['ratio'].append({'id': r.get('verse_id') or f'row{i}',
                                         'ratio': round(ratio, 2)})
    out['double'] = [k for k, v in seen.items() if v > 1]
    out['missing'] = sorted(known - set(seen)) if seen else sorted(known)
    out['overlap'] = round(len(known & set(seen)) / len(known), 3) if known else 0.0
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--work')
    ap.add_argument('--match', help='only work dirs whose name starts with this')
    ap.add_argument('--json')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()

    works = [Path(d) for d in glob.glob(str(ROOT / '*')) if (Path(d) / 'data').is_dir()]
    if a.work:
        works = [w for w in works if w.name == a.work]
    if a.match:
        works = [w for w in works if w.name.startswith(a.match)]
    results = []
    for w in sorted(works):
        for rows_path in sorted((w / 'data').glob('*.l3.json')):
            song = rows_path.name.split('.')[0]
            if rows_path.with_name(song + '.l0.json').exists():
                results.append(check_song(w, song, rows_path))
        for rows_path in sorted((w / 'data').glob('*.l2.json')):
            song = rows_path.name.split('.')[0]
            if (w / 'data' / f'{song}.l3.json').exists():
                continue
            if rows_path.with_name(song + '.l0.json').exists():
                results.append(check_song(w, song, rows_path))
    if not results:
        print('validate_layers: nothing to check (need .l0.json beside .l3/.l2)',
              file=sys.stderr)
        return 1

    defects = sum(len(r['missing']) + len(r['phantom']) + len(r['double']) + len(r['empty'])
                  for r in results)
    warned = sum(len(r['ratio']) for r in results)
    cite_notes = sum(len(r['cite_miss']) for r in results)

    if not a.quiet:
        print(f"{'WORK':28} {'LAYER':3} {'ROWS':>4} {'L0':>5} {'COVER':>6} "
              f"{'MISS':>5} {'PHAN':>4} {'DBL':>4} {'EMPTY':>5} {'RATIO':>5} {'CITE':>4}")
        for r in results:
            print(f"{r['work'][:28]:28} {r['layer']:3} {r['rows']:4} "
                  f"{str(r['l0_segments']):>5} {r['overlap']*100:5.1f}% "
                  f"{len(r['missing']):5} {len(r['phantom']):4} {len(r['double']):4} "
                  f"{len(r['empty']):5} {len(r['ratio']):5} {len(r['cite_miss']):4}")

    complete = [r for r in results if r['l0_segments'] and not (
        r['missing'] or r['phantom'] or r['double'] or r['empty'])]
    print(f"\n{len(results)} songs checked · {len(complete)} structurally clean · "
          f"{defects} defects (missing/phantom/double/empty) · {warned} ratio warnings · "
          f"{cite_notes} cite-variant notes (informational)")

    if a.json:
        Path(a.json).write_text(json.dumps(
            {'songs': len(results),
             'clean': len(complete),
             'defects': defects,
             'warnings': warned,
             'cite_variant_notes': cite_notes,
             'results': results}, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f'wrote {a.json}')
    return 0 if defects == 0 else 2


if __name__ == '__main__':
    raise SystemExit(main())
