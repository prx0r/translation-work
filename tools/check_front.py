#!/usr/bin/env python3
"""Swarm-readiness gate for a new front (prevents repeat incidents).

Checks, in order:
 1. work registered in workcfg with non-empty source spans
 2. transmission brief present (tal-aNN.md for tantraloka, {work}.md else)
 3. working-t1-{song}.json exists and is non-empty
 4. window sizing sane: largest unit tokens vs model output (warn >400)
 5. no deadlock: failed-at-max tasks for this song (needs retest/hand-draft)

Exit 0 = seedable (warnings allowed); exit 2 = blocked (missing inputs).
swarm_seed runs this and surfaces warnings; tantraloka keeps its hard
lore refusal.
"""
from __future__ import annotations
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import workcfg  # noqa: E402

STATE = ROOT / 'process' / 'beam'
TOKEN_WARN = 400


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--song', required=True)
    a = ap.parse_args()
    warns, errs = [], []
    try:
        spans = workcfg.source_spans(a.work)
    except (KeyError, AttributeError, ValueError):
        spans = {}
    if not spans:
        errs.append(f'work {a.work!r} not registered or spans empty (run recon/intake first)')
    else:
        try:
            vs = workcfg.song_verses(a.work, a.song)
            print(f'verses: {len(vs)} spans mapped')
        except (KeyError, AttributeError, ValueError):
            warns.append(f'song {a.song!r} has no verse map (generic song-local numbering assumed)')
    # lore
    ahn = a.work.split('tantraloka-a')[-1] if a.work.startswith('tantraloka-a') else ''
    lp = STATE / 'lore' / (f'tal-a{ahn}.md' if ahn else f'{a.work}.md')
    if lp.exists():
        print(f'brief: {lp.relative_to(ROOT)} ({lp.stat().st_size} bytes)')
    else:
        (warns if not ahn.startswith('tantraloka') else errs).append(
            f'no transmission brief at {lp.relative_to(ROOT)} — write lore first (unbriefed beam degenerates)')
    # working-t1
    wt = ROOT / a.work / f'working-t1-{a.song}.json'
    if not wt.exists():
        errs.append(f'missing {wt.relative_to(ROOT)} (build working-T1 before seeding)')
    else:
        try:
            units = json.loads(wt.read_text())
        except ValueError:
            units = []
            errs.append(f'{wt.relative_to(ROOT)} is not valid JSON')
        if not units:
            errs.append(f'{wt.relative_to(ROOT)} is empty')
        else:
            mx = max(len(e.get('tokens', [])) for e in units)
            print(f'units: {len(units)}, largest unit: {mx} tokens')
            if mx > TOKEN_WARN:
                warns.append(f'largest unit {mx} tokens > {TOKEN_WARN} — use token-budget windows (<=6 spans worked for Gita prose)')
    # deadlock scan
    qf = STATE / 'queue.json'
    if qf.exists():
        try:
            q = json.loads(qf.read_text())
        except ValueError:
            q = []
        dead = sorted(t['id'] for t in q
                      if t.get('args', {}).get('song') == a.song
                      and t.get('status') == 'failed'
                      and t.get('attempts', 0) >= t.get('max_attempts', 3))
        if dead:
            warns.append(f'{len(dead)} failed-at-max tasks will block reseeding (retest protocol or hand-draft): {dead[:5]}')
    for w in warns:
        print(f'WARN: {w}')
    for e in errs:
        print(f'BLOCKED: {e}')
    return 2 if errs else 0


if __name__ == '__main__':
    raise SystemExit(main())
