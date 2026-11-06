#!/usr/bin/env python3
"""beam_swarm — 3 cheap beam-free workers draft, assessor (me) decides.

Workers (nohup'd) pull tasks from process/beam/queue.json, draft with
beam-free, pydantic-validate the draft SHAPE, and park outputs for review.
Workers NEVER write canonical data/ and NEVER mark PASS. The assessor
reviews (beam_swarm.py review), approves into ipvv/pilot/ (or bounces with
a note the worker must address on retry).

Usage:
  python3 tools/beam_swarm.py init-queue        # seed demo batch (idempotent)
  nohup python3 tools/beam_swarm.py worker w1 > process/beam/w1.log 2>&1 &
  python3 tools/beam_swarm.py status
  python3 tools/beam_swarm.py review <task-id>
  python3 tools/beam_swarm.py approve <task-id> # pilot_pair only: pilot->ipvv/pilot/
  python3 tools/beam_swarm.py bounce <task-id> "note"
Needs $OPENCODE_GO_KEY for workers.
"""
from __future__ import annotations
import argparse, datetime, json, os, pathlib, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
STATE = ROOT / 'process' / 'beam'
QFILE = STATE / 'queue.json'

try:
    from pydantic import BaseModel, Field, ValidationError
except ImportError:
    print('pydantic required', file=sys.stderr)
    raise SystemExit(2)

# ---------- schemas ----------

class Task(BaseModel):
    id: str
    kind: str  # pilot_pair | tal_brief
    args: dict = Field(default_factory=dict)
    status: str = 'pending'  # pending|claimed|done|failed|approved|bounced
    attempts: int = 0
    max_attempts: int = 3
    worker: str = ''
    note: str = ''
    created: str = ''
    updated: str = ''


class PilotSelfCheck(BaseModel):
    has_question: bool
    has_sec2: bool
    has_sec4: bool
    premises_ge2: bool
    l2_nonempty: bool


class BriefItem(BaseModel):
    span: str  # e.g. "vv1-3"
    topic: str
    gist: str


class TalBrief(BaseModel):
    ahnika: str
    items: list[BriefItem] = Field(min_length=1)


# ---------- queue ----------

def load_q() -> list[dict]:
    for _ in range(20):
        try:
            if not QFILE.exists():
                return []
            return json.loads(QFILE.read_text())
        except json.JSONDecodeError:
            time.sleep(0.25)  # writer mid-replace; retry
    return json.loads(QFILE.read_text())

def save_q(tasks: list[dict]) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    tmp = QFILE.with_suffix('.tmp')
    tmp.write_text(json.dumps(tasks, indent=1))
    os.replace(tmp, QFILE)  # atomic: readers never see partial JSON

STALE_CLAIM_SECS = 15 * 60  # a claim older than this is dead; steal it

def claimable(t: dict) -> bool:
    if t['attempts'] >= t['max_attempts']:
        return False
    if t['status'] == 'pending':
        return True
    if t['status'] == 'claimed':
        # dead worker left it claimed: re-drive only if no live flag
        flag = STATE / 'claims' / (t['id'] + '.json')
        try:
            return time.time() - flag.stat().st_mtime >= STALE_CLAIM_SECS
        except FileNotFoundError:
            return True
    return False

def claim(tasks: list[dict], worker: str) -> dict | None:
    for t in tasks:
        if claimable(t):
            flag = STATE / 'claims' / (t['id'] + '.json')
            try:
                fd = os.open(flag, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, json.dumps({'worker': worker}).encode())
                os.close(fd)
            except FileExistsError:
                try:
                    if time.time() - flag.stat().st_mtime < STALE_CLAIM_SECS:
                        continue
                    flag.unlink()  # stale: previous worker died
                except FileNotFoundError:
                    continue
                try:
                    fd = os.open(flag, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                    os.write(fd, json.dumps({'worker': worker}).encode())
                    os.close(fd)
                except FileExistsError:
                    continue
            t['status'] = 'claimed'
            t['worker'] = worker
            t['attempts'] += 1
            t['updated'] = datetime.datetime.now().isoformat(timespec='seconds')
            save_q(tasks)
            return t
    return None

def mark(tasks: list[dict], tid: str, status: str, note: str = '') -> None:
    for t in tasks:
        if t['id'] == tid:
            t['status'] = status
            if note:
                t['note'] = (t.get('note', '') + ' | ' + note).strip(' |')
            t['updated'] = datetime.datetime.now().isoformat(timespec='seconds')
    save_q(tasks)
    try:
        (STATE / 'claims' / (tid + '.json')).unlink()
    except FileNotFoundError:
        pass

# ---------- task impls ----------

TAL_SYS = ('You summarize Tantraloka passages for a translation pipeline. '
           'Output ONLY JSON matching the requested schema. No commentary. '
           'Machine-proposed; a scholar reviews.')

def run_pilot_pair(t: dict) -> tuple[bool, str]:
    lbl = t['args']['label']
    env = dict(os.environ)
    p = subprocess.run([sys.executable, 'tools/beam_pilot.py', '--label', lbl],
                       cwd=ROOT, capture_output=True, text=True, env=env, timeout=900)
    if p.returncode != 0:
        return False, (p.stdout + p.stderr)[-600:]
    return True, 'selfcheck gate in beam_pilot passed'

def run_tal_brief(t: dict) -> tuple[bool, str]:
    import re as _re
    from beam_client import beam
    ahn = t['args']['ahnika']  # e.g. a18
    wdir = ROOT / f'tantraloka-{ahn}'
    # Real GRETIL verse text via workcfg (primary); legacy L2 as secondary.
    import workcfg as _w
    try:
        verses_all = _w.song_verses(f'tantraloka-{ahn}', f'tal-{ahn}')
        spans_all = _w.source_spans(f'tantraloka-{ahn}')
    except KeyError:
        return False, f'unknown ahnika {ahn} in workcfg'
    lo, hi = int(t['args'].get('lo', verses_all[0])), int(t['args'].get('hi', verses_all[-1]))
    verses = [v for v in verses_all if lo <= v <= hi]
    lines = [f"v{v}: {' '.join(spans_all[v])}" for v in verses if v in spans_all]
    src = '\n'.join(lines)[:45000]
    want = set(verses)
    tag = f'{ahn}-vv{lo}-{hi}'
    l2 = ''
    for cand in (wdir / f'L2-tal-{ahn}.md', wdir / 'L2.md'):
        if cand.exists() and cand.stat().st_size > 2000:
            l2 = cand.read_text()[:15000]
            break
    prev = (t.get('note') or '').split(' | ')[-1]
    user = (f'AHNIKA {ahn} — WINDOW vv{lo}-{hi} (final verse of window: v{hi}). VERSE TEXT (vN: tokens):\n{src}\n\n'
            + (f'TRANSMISSION BRIEF (scholarly orientation — follow it):\n{(STATE / "lore" / f"tal-{ahn}.md").read_text()[:8000]}\n\n' if (STATE / 'lore' / f'tal-{ahn}.md').exists() else '')
            + (f'LEGACY ENGLISH READ (excerpt):\n{l2[:15000]}\n\n' if l2 else '')
            + (f'PREVIOUS ATTEMPT NOTE (fix this): {prev}\n\n' if prev and 'attempt failed' not in prev and len(prev) > 5 else '')
            + f'Partition THIS WINDOW ONLY (vv{lo}-{hi}) into passage spans of 1-8 verses each. '
              'Follow TOPIC shifts: a new span starts where the subject changes. '
              'NEVER emit uniform blocks — if spans look mechanical, repartition by topic. '
              'The last span MUST end at v{hi}. Cover every verse in the window, no gaps, no overlaps. '
              'For each: topic (<=8 words) and gist (1-2 sentences: what is argued). '
              'Reply ONLY with JSON: {"ahnika": "<id>", "items": [{"span":..., "topic":..., "gist":...}]}')
    text = beam(TAL_SYS, user, session=f'tal-brief-{tag}-001', max_tokens=8000)
    start, end = text.find('{'), text.rfind('}')
    if start < 0:
        return False, 'no JSON object in reply: ' + text[:300]
    try:
        brief = TalBrief.model_validate_json(text[start:end + 1])
    except ValidationError as e:
        return False, f'schema fail: {e.errors()[:2]} | raw: {text[start:start + 300]}'
    # coverage + variety gates (span prefixes normalized: vA-B -> vvA-B)
    covered: set[int] = set()
    lens: list[int] = []
    normed = 0
    for it in brief.items:
        s = it.span.strip()
        m = _re.fullmatch(r'vv(\d+)-(\d+)', s)
        if not m:
            m2 = _re.fullmatch(r'v(\d+)-v?(\d+)', s)
            if m2:
                it.span = f'vv{m2.group(1)}-{m2.group(2)}'
                m, normed = m2, normed + 1
        if not m:
            return False, f'bad span format {it.span!r}; use vvA-B'
        a, b = int(m.group(1)), int(m.group(2))
        covered.update(range(a, b + 1))
        lens.append(b - a + 1)
    if want:
        missing = sorted(set(want) - covered)
        if len(covered & want) < 0.9 * len(want):
            return False, (f'coverage {len(covered & want)}/{len(want)} '
                           f'missing e.g. {missing[:8]}; partition EVERY verse 1-8 per span')
    if len(lens) > 5:
        from collections import Counter as _C
        top, cnt = _C(lens).most_common(1)[0]
        if cnt / len(lens) > 0.8:
            return False, (f'mechanical spans ({cnt}/{len(lens)} are length {top}); '
                           'repartition by TOPIC shifts, vary span lengths')
    outd = ROOT / 'process' / 'beam' / 'runs' / t['id']
    outd.mkdir(parents=True, exist_ok=True)
    (outd / 'brief.json').write_text(brief.model_dump_json(indent=1))
    (outd / 'raw.txt').write_text(text)
    return True, f'{len(brief.items)} spans'

def worker_loop(name: str) -> int:
    from beam_client import chat  # noqa: F401  (fail fast if key missing)
    import beam_client as _b
    _b._key()
    while True:
        tasks = load_q()
        t = claim(tasks, name)
        if not t:
            print(f'[{name}] queue empty, exiting')
            return 0
        print(f'[{name}] claimed {t["id"]} ({t["kind"]}) try {t["attempts"]}', flush=True)
        try:
            if t['kind'] == 'pilot_pair':
                ok, msg = run_pilot_pair(t)
            elif t['kind'] == 'tal_brief':
                ok, msg = run_tal_brief(t)
            else:
                ok, msg = False, f'unknown kind {t["kind"]}'
        except Exception as e:  # noqa: BLE001
            ok, msg = False, f'{type(e).__name__}: {str(e)[:300]}'
        tasks = load_q()
        if ok:
            mark(tasks, t['id'], 'done', msg)
            print(f'[{name}] done {t["id"]}: {msg}', flush=True)
        else:
            left = t['attempts'] < t['max_attempts']
            mark(tasks, t['id'], 'pending' if left else 'failed', f'attempt failed: {msg}')
            print(f'[{name}] fail {t["id"]}: {msg[:200]}', flush=True)
        time.sleep(2)

# ---------- CLI ----------

def cmd_init_queue() -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / 'claims').mkdir(exist_ok=True)
    (STATE / 'runs').mkdir(exist_ok=True)
    tasks = load_q()
    have = {t['id'] for t in tasks}
    now = datetime.datetime.now().isoformat(timespec='seconds')
    seed = [
        {'id': 'v3b-pilot', 'kind': 'pilot_pair', 'args': {'label': 'V3B'}},
        {'id': 'tal-a18-brief', 'kind': 'tal_brief', 'args': {'ahnika': 'a18'}},
        {'id': 'tal-a12-brief', 'kind': 'tal_brief', 'args': {'ahnika': 'a12'}},
    ]
    for s in seed:
        if s['id'] not in have:
            tasks.append(Task(id=s['id'], kind=s['kind'], args=s['args'],
                              created=now, updated=now).model_dump())
    save_q(tasks)
    print(f'queue: {len(tasks)} tasks')

def cmd_status() -> None:
    for t in load_q():
        print(f"{t['id']:16} {t['kind']:11} {t['status']:9} try={t['attempts']} worker={t.get('worker','')} :: {(t.get('note') or '')[:80]}")

def cmd_review(tid: str) -> None:
    t = next((x for x in load_q() if x['id'] == tid), None)
    if not t:
        print('unknown task'); return
    print(json.dumps(t, indent=1)[:800])
    if t['kind'] == 'pilot_pair':
        d = ROOT / 'ipvv' / 'cm' / 'beam' / t['args']['label']
        for f in ['selfcheck.json']:
            p = d / f
            if p.exists():
                print(f'--- {f} ---'); print(p.read_text()[:600])
        am = d / f"pilot_{t['args']['label']}_ARGUMENT_MAP.md"
        if am.exists():
            print(f'--- argmap head ({am.stat().st_size}B) ---')
            print(am.read_text()[:2500])
    else:
        r = STATE / 'runs' / tid / 'brief.json'
        if r.exists():
            print(r.read_text()[:3000])

def cmd_approve(tid: str) -> None:
    tasks = load_q()
    t = next((x for x in tasks if x['id'] == tid), None)
    if not t or t['status'] != 'done':
        print('approve needs status=done'); return
    if t['kind'] == 'pilot_pair':
        lbl = t['args']['label']
        d = ROOT / 'ipvv' / 'cm' / 'beam' / lbl
        for f in [f'pilot_{lbl}_ARGUMENT_MAP.md', f'pilot_{lbl}_L2_read.md']:
            (ROOT / 'ipvv' / 'pilot' / f).write_text((d / f).read_text())
        print(f'placed pilot_{lbl}_* into ipvv/pilot/ — next: converter + validate + proof')
    mark(tasks, tid, 'approved', 'assessor approved')

def cmd_bounce(tid: str, note: str) -> None:
    tasks = load_q()
    mark(tasks, tid, 'pending', 'bounce: ' + note)
    print(f'{tid} bounced with note for worker retry')

def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='c', required=True)
    sub.add_parser('init-queue')
    w = sub.add_parser('worker'); w.add_argument('name')
    sub.add_parser('status')
    r = sub.add_parser('review'); r.add_argument('id')
    a = sub.add_parser('approve'); a.add_argument('id')
    b = sub.add_parser('bounce'); b.add_argument('id'); b.add_argument('note')
    args = ap.parse_args()
    if args.c == 'init-queue':
        cmd_init_queue()
    elif args.c == 'worker':
        return worker_loop(args.name)
    elif args.c == 'status':
        cmd_status()
    elif args.c == 'review':
        cmd_review(args.id)
    elif args.c == 'approve':
        cmd_approve(args.id)
    elif args.c == 'bounce':
        cmd_bounce(args.id, args.note)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
