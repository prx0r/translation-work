#!/usr/bin/env python3
"""manifest — content-hash ledger for every canonical file (Lean-compat pinning).

Canonical = what proofs and the bridge resolve: per work `data/*.json`,
`T1*.md`, `STATUS.json`, `passages.jsonl`, `GATE.json` (when present).
Scratch (cm/, pilot/, runs/, logs, drafts, (_,_Gfull tables excluded as
authoring ledger? NO — G tables ARE the authoring ledger, include them))
is excluded EXCEPT ipvv/cm/*_G*.py authoring tables (kept: provenance).

Hmm — keep it simple and auditable: include data/, T1*.md, STATUS.json,
passages.jsonl, GATE.json, cm/*_G*.py + cm/*.json sidecars? Sidecars churn
every merge (covered/status jsons). Those are pipeline state, not canon:
EXCLUDE cm/*.json + cm/*.py? But G tables are the gloss provenance...
Decision: include cm/*_G*.py (authored ledger, stable once written) and
EXCLUDE cm/*-covered.json, *-status.json, *.charfill.json, *.handpacket.json,
fullclose/squeeze reports, beam outputs (process/beam). Rationale: canon =
inputs a verifier needs; state = regenerable.

Usage:
  python3 tools/manifest.py gen     # write MANIFEST.json
  python3 tools/manifest.py check   # recompute; exit 1 + list drift
MANIFEST.json: {"rev": git-sha, "at": ts, "files": {path: {sha256, bytes}}}
"""
from __future__ import annotations
import datetime, hashlib, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAN = ROOT / 'MANIFEST.json'
EXCLUDE_DIRS = {'cm', 'pilot', 'runs', '.git', '__pycache__', 'node_modules',
                'site', 'lore', 'logs', 'process', 'skills'}
EXCLUDE_SUFFIX = ('.log', '.tmp', '.draft')


def work_dirs() -> list[pathlib.Path]:
    out = []
    for p in sorted(ROOT.iterdir()):
        if p.name.startswith('.') or not p.is_dir() or p.name in EXCLUDE_DIRS:
            continue
        if (p / 'data').is_dir():
            out.append(p)
    # ipvv is per-chunk (tantrasara layout): each chunk dir is a work
    ipvv = ROOT / 'ipvv'
    if ipvv.is_dir():
        for c in sorted(ipvv.iterdir()):
            if c.is_dir() and (c / 'data').is_dir():
                out.append(c)
    return out


def canon_files() -> list[pathlib.Path]:
    out = []
    for work in work_dirs():
        dd = work / 'data'
        out += sorted(dd.glob('*.json'))
        out += sorted(work.glob('T1*.md'))
        for f in ('STATUS.json', 'passages.jsonl', 'GATE.json'):
            if (work / f).exists():
                out.append(work / f)
        # authoring ledger (stable once written)
        if (work / 'cm').is_dir():
            out += sorted((work / 'cm').glob('*_G*.py'))
    # repo-root canonical docs pinned by check.py
    for f in ('stack.json', 'DATATYPES.json', 'REGISTRY.json', 'INDEX.json'):
        if (ROOT / f).exists():
            out.append(ROOT / f)
    return [p for p in out if not p.name.endswith(EXCLUDE_SUFFIX)]


def sha(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def gen() -> None:
    try:
        rev = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                             capture_output=True, text=True).stdout.strip()
    except Exception:
        rev = 'nogit'
    files = {}
    for p in canon_files():
        files[str(p.relative_to(ROOT))] = {'sha256': sha(p), 'bytes': p.stat().st_size}
    MAN.write_text(json.dumps({'rev': rev,
                               'at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                               'files': files}, indent=1))
    print(f'manifest: {len(files)} files rev={rev[:8]}')


def check() -> int:
    if not MAN.exists():
        print('MANIFEST.json missing — run: python3 tools/manifest.py gen')
        return 1
    old = json.loads(MAN.read_text())['files']
    new = {}
    for p in canon_files():
        new[str(p.relative_to(ROOT))] = sha(p)
    drift = [k for k in set(old) | set(new)
             if old.get(k, {}).get('sha256') != new.get(k)]
    if drift:
        print(f'MANIFEST DRIFT ({len(drift)} files) — regen: python3 tools/manifest.py gen')
        for k in sorted(drift)[:20]:
            print('  ', 'MISSING' if k not in new else ('NEW' if k not in old else 'CHANGED'), k)
        return 1
    print(f'manifest clean: {len(new)} files')
    return 0


if __name__ == '__main__':
    raise SystemExit(gen() if (sys.argv[1:] or ['gen'])[0] == 'gen' else check())
