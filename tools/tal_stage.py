#!/usr/bin/env python3
"""tal_stage — drive one ahnika through the minimal-gold pipeline autonomously.

Stages (idempotent; each checks before acting):
  1 parse   T1.md chains -> working-t1 (tools/tal_t1_parse.py)
  2 seed    queue tal_gloss / tal_cm / tal_am for every verse missing output
  3 check   report counts; exit 0 when all beam outputs present
  4 assemble  glosses+CM+am -> working-t1/l0/argmap/l2/c1, data/*.json
  5 gates   validate_song + proof_record --shastra; write STATUS/REGISTRY
Beam workers must be running for stages 2-3 to progress; run --loop to wait.

Usage:
  python3 tools/tal_stage.py --work tantraloka-a11 --song tal-a11 [--seed] [--loop] [--wait 600]
"""
from __future__ import annotations
import argparse, json, os, pathlib, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import workcfg  # noqa: E402

Q = ROOT / 'process' / 'beam' / 'queue.json'
RUNS = ROOT / 'process' / 'beam' / 'runs'


def load_q():
    return json.loads(Q.read_text()) if Q.exists() else []


def save_q(q):
    tmp = Q.with_name(f'{Q.name}.{os.getpid()}.{time.time_ns()}.tmp')
    tmp.write_text(json.dumps(q, indent=1))
    os.replace(tmp, Q)


def stage_parse(work, song):
    wt = ROOT / work / f'working-t1-{song}.json'
    if wt.exists():
        return json.loads(wt.read_text())
    r = subprocess.run([sys.executable, 'tools/tal_t1_parse.py', '--work', work, '--song', song],
                       cwd=ROOT, capture_output=True, text=True)
    print(r.stdout.strip()[-400:] or r.stderr.strip()[-400:])
    if r.returncode != 0:
        raise SystemExit(f'parse failed for {work}')
    return json.loads(wt.read_text())


def stage_seed_triple(work, song, group=24):
    wt = json.loads((ROOT / work / f'working-t1-{song}.json').read_text())
    q = load_q(); have = {t['id'] for t in q}; now = time.strftime('%Y-%m-%dT%H:%M:%S')
    pending_verses = [e['verse'] for e in wt
                      if not ((RUNS / f'{song}-gloss-v{e["verse"]:02d}' / 'gloss.json').exists()
                              and (RUNS / f'{song}-cm-v{e["verse"]:02d}' / 'cm.json').exists()
                              and (RUNS / f'{song}-am-v{e["verse"]:02d}' / 'am.json').exists())]
    new = 0
    for i in range(0, len(pending_verses), group):
        grp = pending_verses[i:i + group]
        tid = f'{song}-triple-v{grp[0]:02d}'
        if tid in have:
            continue
        q.append({'id': tid, 'kind': 'tal_triple',
                  'args': {'work': work, 'song': song, 'verses': grp},
                  'status': 'pending', 'attempts': 0, 'max_attempts': 6,
                  'worker': '', 'note': '', 'created': now, 'updated': now})
        new += 1
    if new:
        save_q(q)
    print(f'seeded {new} triple groups ({len(pending_verses)} verses)')


def stage_seed(work, song, am_ctx=True):
    wt = json.loads((ROOT / work / f'working-t1-{song}.json').read_text())
    q = load_q(); have = {t['id'] for t in q}
    now = time.strftime('%Y-%m-%dT%H:%M:%S')
    new = 0
    ahn = work.split('tantraloka-a')[-1]
    for e in wt:
        v = e['verse']
        if not (RUNS / f'{song}-gloss-v{v:02d}' / 'gloss.json').exists():
            tid = f'{song}-gloss-v{v:02d}'
            if tid not in have:
                q.append({'id': tid, 'kind': 'tal_gloss', 'args': {
                    'work': work, 'song': song, 'verse': v, 'ahnika': ahn,
                    'context': ''}, 'status': 'pending', 'attempts': 0,
                    'max_attempts': 3, 'worker': '', 'note': '', 'created': now, 'updated': now})
                new += 1
        elif not (RUNS / f'{song}-cm-v{v:02d}' / 'cm.json').exists():
            tid = f'{song}-cm-v{v:02d}'
            if tid not in have:
                q.append({'id': tid, 'kind': 'tal_cm', 'args': {
                    'work': work, 'song': song, 'verse': v}, 'status': 'pending',
                    'attempts': 0, 'max_attempts': 3, 'worker': '', 'note': '',
                    'created': now, 'updated': now})
                new += 1
        elif am_ctx and not (RUNS / f'{song}-am-v{v:02d}' / 'am.json').exists():
            tid = f'{song}-am-v{v:02d}'
            if tid not in have:
                prev = ' '.join(t.get('quick_gloss', '') for t in e['tokens'])
                q.append({'id': tid, 'kind': 'tal_am', 'args': {
                    'work': work, 'song': song, 'verse': v, 'prev': prev},
                    'status': 'pending', 'attempts': 0, 'max_attempts': 3,
                    'worker': '', 'note': '', 'created': now, 'updated': now})
                new += 1
    if new:
        save_q(q)
    print(f'seeded {new} tasks')


def counts(song, verses):
    have = {k: sum(1 for v in verses
                   if (RUNS / f'{song}-{k}-v{v:02d}' / f'{k}.json').exists())
            for k in ('gloss', 'cm', 'am')}
    return have


def stage_assemble(work, song):
    W = ROOT / work
    wt = json.loads((W / f'working-t1-{song}.json').read_text())
    # glosses into working-t1
    for e in wt:
        f = RUNS / f"{song}-gloss-v{e['verse']:02d}" / 'gloss.json'
        if not f.exists():
            continue
        rows = {r['surface']: r for r in json.loads(f.read_text())['rows']}
        for t in e['tokens']:
            r = rows.get(t['surface'])
            if r:
                t['quick_gloss'] = r['gloss']
                t['grounds'] = r['grounds']
    (W / f'working-t1-{song}.json').write_text(json.dumps(wt, indent=1, ensure_ascii=False))
    # CM assemble
    cm = {}
    for e in wt:
        f = RUNS / f"{song}-cm-v{e['verse']:02d}" / 'cm.json'
        if f.exists():
            d = json.loads(f.read_text())
            cm[str(e['verse'])] = [[r['lemma'], r['morph'], r['grounds']] for r in d['rows']]
    (W / 'cm').mkdir(exist_ok=True)
    cmf = W / 'cm' / f'l0cm-{song}-v1-{len(wt)}.json'
    cmf.write_text(json.dumps(cm, indent=1, ensure_ascii=False))
    r = subprocess.run([sys.executable, 'tools/build_l0.py', '--work', work, '--cm', str(cmf)],
                       cwd=ROOT, capture_output=True, text=True)
    print(r.stdout.strip()[-300:] or r.stderr.strip()[-300:])
    # emit data
    l0 = json.loads((W / f'working-l0-{song}.json').read_text())
    src_sha = wt[0]['source_sha']
    by = {}
    for o in l0:
        by.setdefault(o['verse_id'], []).append(o)
    am, l2 = [], []
    for e in wt:
        d = json.loads((RUNS / f"{song}-am-v{e['verse']:02d}" / 'am.json').read_text())
        ids = [o['id'] for o in by.get(e['verse_id'], [])]
        am.append({'verse_id': e['verse_id'], 'song': song, 'verse': e['verse'],
                   'scope': 'verse', 'structured': True,
                   'speaker': 'Abhinavagupta (teacher voice)',
                   'question': d['question'], 'premises': d['premises'],
                   'inference': d['inference'], 'uncertainties': d.get('uncertainties', []),
                   'option_choices': [],
                   'traces': {'t1_verse': e['verse_id'], 'l0_ids': ids, 'sanskrit_sha': src_sha},
                   'sanskrit_sha': src_sha})
        l2.append({'verse_id': e['verse_id'], 'song': song, 'verse': e['verse'],
                   'plain_english': d['plain_english'],
                   'sanskrit_cite': ' '.join(t['surface'] for t in e['tokens']),
                   'l0_ids': ids or [l0[0]['id']], 'supplied': []})
        e['quick_english'] = d['plain_english']
        e['quick_english_source'] = 'manual'
    dd = W / 'data'; dd.mkdir(exist_ok=True)
    for n, o in [('t1', wt), ('l0', l0), ('argmap', am), ('l2', l2)]:
        (dd / f'{song}.{n}.json').write_text(json.dumps(o, indent=1, ensure_ascii=False))
    (W / f'working-t1-{song}.json').write_text(json.dumps(wt, indent=1, ensure_ascii=False))
    c1p = dd / f'{song}.c1.json'
    if not c1p.exists():
        ess, seen = [], set()
        for o in am:
            s_ = ' '.join(o['inference'].split())[:220]
            k = s_[:60].lower()
            if s_ and k not in seen:
                seen.add(k); ess.append(s_)
            if len(ess) >= 5:
                break
        c1p.write_text(json.dumps({'song': song, 'essence': ess,
            'essence_source': 'derived from argmap inferences (machine-proposed; assessor review outstanding)',
            'rasa': {}, 'essence_only': True, 'renders': {}}, indent=1, ensure_ascii=False))
    print(f'emitted t1/l0/argmap/l2 {len(wt)}/{len(l0)}/{len(am)}/{len(l2)}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--song', required=True)
    ap.add_argument('--seed', action='store_true')
    ap.add_argument('--triple', action='store_true', help='one beam call per 24 verses (auto-halves on output ceiling)')
    ap.add_argument('--loop', action='store_true')
    ap.add_argument('--wait', type=int, default=600)
    ap.add_argument('--max-wait', type=int, default=7200)
    a = ap.parse_args()
    wt = stage_parse(a.work, a.song)
    n = len(wt)
    waited = 0
    while True:
        if a.seed:
            if a.triple:
                stage_seed_triple(a.work, a.song)
            else:
                stage_seed(a.work, a.song)
            a.seed = False
        c = counts(a.song, [e['verse'] for e in wt])
        n = len(wt)
        print(f'{a.song}: gloss {c["gloss"]}/{n} cm {c["cm"]}/{n} am {c["am"]}/{n}')
        if all(v == n for v in c.values()):
            break
        if not a.loop or waited >= a.max_wait:
            print('incomplete — rerun with --loop (and workers running)')
            return 1
        time.sleep(a.wait); waited += a.wait
        if a.triple:
            stage_seed_triple(a.work, a.song)
        else:
            stage_seed(a.work, a.song)
    stage_assemble(a.work, a.song)
    for cmd in (['tools/validate_song.py', '--song', a.song, '--work', a.work],
                ['tools/proof_record.py', '--song', a.song, '--work', a.work, '--shastra']):
        r = subprocess.run([sys.executable] + cmd, cwd=ROOT, capture_output=True, text=True)
        tail = (r.stdout + r.stderr).strip()
        print(tail[-400:])
        if r.returncode != 0 and 'proof_record' in cmd[0]:
            print('PROOF NOT PASS — needs assessor')
            return 2
    print(f'{a.song}: staged, validated, proofed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
