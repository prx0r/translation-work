#!/usr/bin/env python3
"""ralph_convert — convert approved pilot prose to canonical JSON (assessor lane).

For every queue task with status approved + kind pilot_pair whose song still
lacks data/<song>.argmap.json: run shastra_convert_chunk.py --layers-only
(convert + validate + proof). Records PASS/BLOCKED honestly; BLOCKED stays
BLOCKED with its disposition need — never forced. Prints a summary line per
chunk for the ralph log.
"""
from __future__ import annotations
import json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from workcfg import data_dir  # noqa: E402

def main() -> int:
    qpath = ROOT / 'process' / 'beam' / 'queue.json'
    if not qpath.exists():
        print('ralph_convert: no queue')
        return 0
    tasks = json.loads(qpath.read_text())
    table = {e['song']: e for e in json.loads((ROOT / 'ipvv' / 'chunk-table.json').read_text())}
    mp = json.loads((ROOT / 'ipvv' / 'chunk-song-map.json').read_text())
    done = 0
    for t in tasks:
        if not (t['status'] == 'approved' and t['kind'] == 'pilot_pair'):
            continue
        lbl = t['args']['label']
        song = None
        for cid, s in mp.items():
            if cid.startswith('chunkV'):
                parts = cid.split('-')
                if ('V' + parts[0][-1] + parts[1].upper()) == lbl:
                    song = s
                    break
            elif ('V1' + cid[5].upper()) == lbl:
                song = s
                break
        if song is None:
            print(f'ralph_convert: cannot resolve label {lbl}')
            continue
        if list(data_dir('ipvv', song).glob(f'{song}.argmap.json')):
            continue
        e = table[song]
        cid = next(c for c, s in mp.items() if s == song)
        p = subprocess.run(
            [sys.executable, 'tools/shastra_convert_chunk.py', '--song', song,
             '--verse', str(e['verse']), '--v1', f'ipvv/{cid}/T1.l0.jsonl',
             '--layers-only'],
            cwd=ROOT, capture_output=True, text=True, timeout=600)
        tail = (p.stdout + p.stderr).strip().splitlines()
        print(f'ralph_convert {song}: rc={p.returncode} :: {(tail[-1] if tail else "")[:160]}')
        done += 1
    if not done:
        print('ralph_convert: nothing due')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
