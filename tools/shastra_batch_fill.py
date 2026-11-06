#!/usr/bin/env python3
"""shastra_batch_fill — fold available L0 row glosses into every chunk's T1+L0 data.

Per chunk: shastra_charfill (gloss assembly) -> shastra_merge (fold into data).
No layers, no proof — translation content only. Failures are logged per chunk
and never abort the batch. Writes ipvv/cm/batch-fill-report.json.
"""
from __future__ import annotations
import json, pathlib, subprocess, sys, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent


def run(cmd, env=None) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env=env)
    return p.returncode, (p.stdout + p.stderr).strip()


def main() -> int:
    table = json.load(open(ROOT / 'ipvv' / 'chunk-table.json'))
    st = json.load(open(ROOT / 'ipvv' / 'STATUS.json'))
    done = set(st['counts']['shastra_pass'])
    only = None
    if len(sys.argv) > 1:  # optional: --only song
        only = sys.argv[1]

    results = []
    for e in table:
        song, verse = e['song'], e['verse']
        if only and song != only:
            continue
        if song in done:
            results.append({'song': song, 'status': 'skip-pass'})
            continue
        # 1. charfill
        rc, out = run(['python3', 'tools/shastra_charfill.py', '--song', song, '--verse', str(verse)])
        if rc != 0:
            results.append({'song': song, 'status': 'charfill-fail', 'log': out[-500:]})
            print(f'CHARFILL-FAIL {song}: {out.splitlines()[-1] if out else "?"}', flush=True)
            continue
        stats = json.loads((ROOT / 'ipvv' / 'cm' / f'{song}.charfill.json').read_text())
        # 2. merge (Gchar + Ghand if present)
        gtables = stats['mod']
        if (ROOT / 'ipvv' / 'cm' / f"{song.replace('-', '_')}_Ghand.py").exists():
            gtables += ',' + song.replace('-', '_') + '_Ghand'
        import os
        env = dict(os.environ, PYTHONPATH=str(ROOT / 'ipvv' / 'cm'))
        rc, out = run(['python3', 'tools/shastra_merge.py', '--song', song, '--verse', str(verse),
                       '--v1', stats['v1_path'], '--gtables', gtables], env=env)
        if rc != 0:
            results.append({'song': song, 'status': 'merge-fail', 'log': out[-500:]})
            print(f'MERGE-FAIL {song}: {out.splitlines()[-1] if out else "?"}', flush=True)
            continue
        merged_line = next((l for l in out.splitlines() if l.startswith('merged toks')), out)
        results.append({'song': song, 'status': 'ok',
                        'real': stats['real'], 'covered_before': stats['covered'],
                        'gchar': stats['gchar'], 'residual': stats['residual'],
                        'merged': merged_line})
        print(f'OK {song}: {merged_line}', flush=True)

    report = {'at': datetime.datetime.now().isoformat(timespec='seconds'),
              'results': results}
    (ROOT / 'ipvv' / 'cm' / 'batch-fill-report.json').write_text(
        json.dumps(report, indent=1, ensure_ascii=False))
    ok = sum(1 for r in results if r['status'] == 'ok')
    fail = [r for r in results if r['status'].endswith('fail')]
    print(f'\nBATCH DONE: ok={ok} failed={len(fail)} skipped={sum(1 for r in results if r["status"]=="skip-pass")}')
    for r in fail:
        print(f'  FAILED {r["song"]}: {r["status"]}')
    return 1 if fail else 0


if __name__ == '__main__':
    raise SystemExit(main())
