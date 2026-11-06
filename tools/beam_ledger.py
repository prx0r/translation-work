#!/usr/bin/env python3
"""beam_ledger — append-only, hash-chained event log for the translation machine.

Every consequential step appends one JSON line to process/beam/LEDGER.jsonl:
worker claims/dones/fails, approvals, bounces, conversions, validations,
proofs, lore fetches, commits, manifest gens. Each event carries the sha256
of the previous line (prev_sha) — tamper-evident, same idea as openpatala
ledger_checkpoints.merkle. Field names mirror openpatala derivation_activities
(activity_type/inputs/outputs/actor_id/software/run_id) and raw_observations
(provider/endpoint/uri) so a future trika-x loader can ingest without
translation-work ever writing the DB (lane rule stands).

Error taxonomy (use exactly these classes in `error.class`):
  format-fail | coverage-fail | schema-fail | gate-fail | stale-state |
  provider-fail | budget-fail | assessor-hold
Each error must name the failing gate and the next action (retry-with-note,
bounce, escalate). An error without a next action is an unfinished log entry.

Usage:
  python3 tools/beam_ledger.py tail [N]
  python3 tools/beam_ledger.py errors [--since TS]
  python3 tools/beam_ledger.py task <task-id>
  python3 tools/beam_ledger.py fetch --provider websearch --query "..." --payload <file>
  python3 tools/beam_ledger.py checkpoint   # merkle root over new events -> checkpoints.jsonl
Python API: from beam_ledger import log; log(kind, task=..., actor=..., inputs=..., outputs=..., detail=..., error=...)
"""
from __future__ import annotations
import argparse, datetime, hashlib, json, os, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = ROOT / 'process' / 'beam' / 'LEDGER.jsonl'
CKPTS = ROOT / 'process' / 'beam' / 'ledger-checkpoints.jsonl'
RUN_ID = os.environ.get('BEAM_RUN_ID', f"ralph-{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d')}")


def _prev_sha() -> str:
    if not LEDGER.exists() or LEDGER.stat().st_size == 0:
        return 'GENESIS'
    last = None
    with open(LEDGER, 'rb') as f:
        try:
            f.seek(-4096, os.SEEK_END)
        except OSError:
            f.seek(0)
        for line in f.read().decode(errors='replace').splitlines():
            if line.strip():
                last = line
    if not last:
        return 'GENESIS'
    return hashlib.sha256(last.encode()).hexdigest()


def log(kind: str, task: str = '', actor: str = '', inputs: dict | None = None,
        outputs: dict | None = None, detail: str = '', error: dict | None = None,
        activity: str = '') -> dict:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    ev = {
        'ts': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
        'run_id': RUN_ID,
        'lane': 'translation-work',
        'kind': kind,                       # task.claimed|task.done|task.failed|...
        'activity_type': activity or kind,   # openpatala derivation_activities vocab
        'task': task,
        'actor_id': actor,                   # worker name | assessor | ralph | script
        'inputs': inputs or {},
        'outputs': outputs or {},
        'detail': detail[:500],
        'error': error or {},
        'prev_sha': _prev_sha(),
    }
    with open(LEDGER, 'a') as f:
        f.write(json.dumps(ev, ensure_ascii=False) + '\n')
    return ev


def cmd_tail(n: int) -> None:
    if not LEDGER.exists():
        print('(empty ledger)')
        return
    lines = LEDGER.read_text().splitlines()
    for line in lines[-n:]:
        e = json.loads(line)
        err = f" !!{e['error'].get('class')}" if e.get('error') else ''
        print(f"{e['ts']} {e['kind']:16} {e['task'][:28]:28} {e['actor_id'][:8]:8} {e['detail'][:90]}{err}")


def cmd_errors(since: str = '') -> None:
    if not LEDGER.exists():
        return
    for line in LEDGER.read_text().splitlines():
        e = json.loads(line)
        if e.get('error') and (not since or e['ts'] >= since):
            print(f"{e['ts']} {e['task']} :: {e['error'].get('class')}: {str(e['error'].get('message'))[:160]}")
            print(f"   next: {e['error'].get('next', '?')} (detail: {e['detail'][:120]})")


def cmd_task(tid: str) -> None:
    if not LEDGER.exists():
        return
    for line in LEDGER.read_text().splitlines():
        e = json.loads(line)
        if e.get('task') == tid:
            print(f"{e['ts']} {e['kind']:16} {e['actor_id']:10} {e['detail'][:110]}"
                  + (f" !!{e['error']}" if e.get('error') else ''))


def cmd_fetch(provider: str, query: str, payload: str) -> None:
    p = pathlib.Path(payload)
    h = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else 'missing'
    log('fetch', task=query[:60], actor='assessor',
        inputs={'provider': provider, 'requested_uri': query},
        outputs={'payload_artifact': str(p), 'sha256': h},
        detail=f'{provider} fetch, payload sha {h[:12]}')
    print(f'logged fetch {h[:12]}')


def cmd_checkpoint() -> None:
    lines = LEDGER.read_text().splitlines() if LEDGER.exists() else []
    root = hashlib.sha256(''.join(lines).encode()).hexdigest() if lines else 'empty'
    last_ck = 0
    if CKPTS.exists():
        for line in CKPTS.read_text().splitlines():
            try:
                last_ck = max(last_ck, json.loads(line).get('last_event_cursor', 0))
            except ValueError:
                pass
    ck = {'id': f'ck-{len(lines)}-{root[:8]}', 'previous_checkpoint_id': None,
          'first_event_cursor': last_ck + 1 if lines else 0, 'last_event_cursor': len(lines),
          'event_count': len(lines) - last_ck, 'merkle': {'root': root, 'algo': 'sha256-lines'},
          'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
          'signatures': []}
    if ck['event_count']:
        with open(CKPTS, 'a') as f:
            f.write(json.dumps(ck) + '\n')
    print(json.dumps(ck, indent=1)[:400])


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='c', required=True)
    t = sub.add_parser('tail');
    t.add_argument('n', nargs='?', type=int, default=20)
    e = sub.add_parser('errors');
    e.add_argument('--since', default='')
    k = sub.add_parser('task');
    k.add_argument('id')
    f = sub.add_parser('fetch');
    f.add_argument('--provider', required=True)
    f.add_argument('--query', required=True)
    f.add_argument('--payload', required=True)
    sub.add_parser('checkpoint')
    a = ap.parse_args()
    if a.c == 'tail':
        cmd_tail(a.n)
    elif a.c == 'errors':
        cmd_errors(a.since)
    elif a.c == 'task':
        cmd_task(a.id)
    elif a.c == 'fetch':
        cmd_fetch(a.provider, a.query, a.payload)
    elif a.c == 'checkpoint':
        cmd_checkpoint()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
