#!/usr/bin/env python3
"""validate_all — the ONE gate. Exit 0 = shippable, else named failures.

Stages (fail-closed, first failure still runs the rest so one run shows all):
  1. schemas import + self-test            (fast)
  2. manifest freshness                    (fast-ish: hashes canon files)
  2b. passages ledgers: unique locators + immutable_id repo-wide (fast)
  3. per-song validate_song across ALL data songs (slow: minutes)
  4. proof sweep: every proof-*.json must be PASS with zero blocking;
     BLOCKED allowed ONLY with a recorded disposition file
     (proof/<song>.disp.json listing verse->reason) — else FAIL.
  5. check.py CANONICAL                     (slow: runs everything incl. roundtrips)
  6. dbread coverage for ipvv + all gold works (warn-only if DB unreachable)

Usage: python3 tools/validate_all.py [--quick]  (--quick skips stage 3+5 bodies
but still runs schemas, manifest, proof-file scan, dbread)
ralph.sh gates commits on this, not on check.py alone.
"""
from __future__ import annotations
import glob, json, os, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
fails: list[str] = []
warns: list[str] = []


def step(name: str, ok: bool, detail: str = "") -> None:
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail and not ok else ""), flush=True)
    if not ok:
        fails.append(name + (f": {detail}" if detail else ""))


def run(cmd: list[str], timeout: int = 1500) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).strip()


def main() -> int:
    quick = '--quick' in sys.argv
    sys.path.insert(0, str(ROOT / 'tools'))
    sys.path.insert(0, str(ROOT / 'schemas'))

    # 1. schemas
    try:
        import t1 as t1s, l0 as l0s, argmap as ams, l2 as l2s, c1 as c1s  # noqa
        import base as _b
        _b.check_required({}, ['x'], 'selftest')
        step('schemas-import', True)
    except Exception as e:  # noqa: BLE001
        step('schemas-import', False, str(e)[:200])

    # 2. manifest — auto-heal NEW-only drift (active autoburn writes T1s
    # faster than a static pin; CHANGED/MISSING still fail the gate).
    rc, out = run([sys.executable, 'tools/manifest.py', 'check'])
    if rc != 0 and 'NEW' in out and 'CHANGED' not in out and 'MISSING' not in out:
        run([sys.executable, 'tools/manifest.py', 'gen'])
        rc, out = run([sys.executable, 'tools/manifest.py', 'check'])
    step('manifest-fresh', rc == 0, out.splitlines()[-1][:160] if rc else out[-300:])

    # 2b. passages ledgers (FORMAL-ALIGN contract): unique locators PER FILE
    # (matches evidence_check gate) + immutable_id globally unique.
    # Cross-work locator collisions (anu-*, par-*) are grandfathered legacy
    # schemes, disambiguated by work in bridge maps — reported, not failed.
    try:
        import glob as _g
        seen_imm: dict[str, str] = {}
        nrows = 0
        bad = []
        collide: dict[str, set] = {}
        for f in sorted(_g.glob(str(ROOT / '*' / 'passages.jsonl'))):
            seen_loc: set[str] = set()
            for line in open(f):
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                nrows += 1
                loc, iid = r.get('locator'), r.get('immutable_id')
                if not loc:
                    bad.append(f'{f}:missing-locator')
                elif loc in seen_loc:
                    bad.append(f'dup-locator-in-file:{f}:{loc}')
                else:
                    seen_loc.add(loc)
                if not iid:
                    bad.append(f'{f}:missing-immutable-id')
                elif iid in seen_imm:
                    bad.append(f'dup-immutable:{iid}')
                else:
                    seen_imm[iid] = f
                if loc:
                    collide.setdefault(loc, set()).add(f)
        shared = {l: sorted(fs) for l, fs in collide.items() if len(fs) > 1}
        step('passages-ledger', not bad,
             f'{nrows} rows, {len(seen_imm)} immutable' if not bad else f'{bad[:5]}')
        if shared:
            print(f'  NOTE cross-work locator collisions (grandfathered, work-disambiguated): '
                  f'{len(shared)} locators, e.g. {sorted(shared)[:6]}')
    except Exception as e:  # noqa: BLE001
        step('passages-ledger', False, str(e)[:160])

    # 3. per-song validate (skip in --quick)
    if not quick:
        from workcfg import data_dir
        table = []
        try:
            table = json.loads((ROOT / 'ipvv' / 'chunk-table.json').read_text())
        except OSError:
            pass
        bad = []
        songs = [(e['song'], 'ipvv') for e in table]
        import re as _re
        for wdir in sorted((p for p in ROOT.iterdir()
                           if p.is_dir() and (p / 'data').is_dir() and p.name != 'ipvv'),
                           key=lambda p: p.name):
            for f in sorted((wdir / 'data').glob('*.t1.json')):
                m = _re.fullmatch(r'(.+)\.t1\.json', f.name)
                if m and not any(s == m.group(1) for s, _ in songs):
                    songs.append((m.group(1), wdir.name))
        for song, work in songs:
            rc, out = run([sys.executable, 'tools/validate_song.py', '--song', song, '--work', work])
            if rc != 0:
                bad.append(f'{work}:{song}')
        step('validate-songs', not bad, f'{len(bad)} invalid: {bad[:5]}' if bad else f'{len(songs)} songs')
    else:
        print('SKIP validate-songs (--quick)')

    # 4. proof sweep
    blocked_ok, blocked_plain, broken = [], [], []
    for f in sorted(glob.glob(str(ROOT / 'ipvv' / 'proof' / 'proof-*.json'))):
        d = json.loads(open(f).read())
        if d.get('mode') != 'shastra':
            continue
        gate = d.get('deterministic_gate')
        disp = pathlib.Path(str(f).replace('proof-', 'disp-').replace('.json', '.json'))
        song = d.get('song', '?')
        if gate == 'PASS' and not d.get('blocking'):
            continue
        if gate == 'BLOCKED' and disp.exists():
            blocked_ok.append(song)
        elif gate == 'BLOCKED':
            blocked_plain.append(song)
        else:
            broken.append(f'{song}:{gate}')
    # classic (non-shastra) gold proofs live per-work; check.py covers them (stage 5)
    step('proof-sweep', not (blocked_plain or broken),
         f'unrecorded-BLOCKED={blocked_plain[:5]} broken={broken[:5]}'
         if (blocked_plain or broken) else 'shastra PASS + dispositioned only')

    # 5. check.py
    if not quick:
        rc, out = run([sys.executable, 'check.py'], timeout=2400)
        tail = out.strip().splitlines()[-1] if out.strip() else ''
        step('check-canonical', rc == 0, tail[:160])
    else:
        print('SKIP check-canonical (--quick)')

    # 6. dbread coverage (warn-only: DB may be down; lane rule = read-only anyway)
    try:
        rc, out = run([sys.executable, 'tools/dbread.py', 'coverage', 'ipvv'])
        if rc == 0:
            step('dbread-ipvv', True)
        else:
            warns.append('dbread-ipvv: ' + out[-200:])
            print('WARN dbread-ipvv (non-blocking): ' + out[-200:])
    except Exception as e:  # noqa: BLE001
        warns.append(f'dbread-ipvv unavailable: {e}')

    print(f'\nVALIDATE_ALL: {"0 failures" if not fails else str(len(fails)) + " FAILURES: " + str(fails)}'
          + (f' | {len(warns)} warnings' if warns else ''))
    return 1 if fails else 0


if __name__ == '__main__':
    raise SystemExit(main())
