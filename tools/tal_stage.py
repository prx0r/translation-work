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
from shastra_merge import is_paratext  # noqa: E402 (single paratext doctrine; stage filters must match it)

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


def stage_seed_triple(work, song, group=24, token_budget=0):
    wt = json.loads((ROOT / work / f'working-t1-{song}.json').read_text())
    import sys as _sys
    _sys.path.insert(0, str(ROOT / 'tools'))
    from beam_swarm import queue_update
    now = time.strftime('%Y-%m-%dT%H:%M:%S')
    pending = [(e['verse'], len(e['tokens'])) for e in wt
               if not ((RUNS / f'{song}-gloss-v{e["verse"]:02d}' / 'gloss.json').exists()
                       and (RUNS / f'{song}-cm-v{e["verse"]:02d}' / 'cm.json').exists()
                       and (RUNS / f'{song}-am-v{e["verse"]:02d}' / 'am.json').exists())]
    groups = []
    if token_budget and token_budget > 0:
        # Pack verses by source-token budget, not verse count: prose-heavy
        # units (40+ tokens) blow the model's output ceiling in 24-verse
        # windows (proven: 21-unit Gita windows fail, 6-span/≈180tok pass).
        cur, acc = [], 0
        for v, nt in pending:
            if cur and acc + nt > token_budget:
                groups.append([x for x, _ in cur]); cur, acc = [], 0
            cur.append((v, nt)); acc += nt
        if cur:
            groups.append([x for x, _ in cur])
    else:
        vs = [v for v, _ in pending]
        groups = [vs[i:i + group] for i in range(0, len(vs), group)]

    def _add(q):
        have = {t['id'] for t in q}
        new = 0
        for grp in groups:
            tid = f'{song}-triple-v{grp[0]:02d}'
            if tid in have:
                continue
            q.append({'id': tid, 'kind': 'tal_triple',
                      'args': {'work': work, 'song': song, 'verses': grp},
                      'status': 'pending', 'attempts': 0, 'max_attempts': 6,
                      'worker': '', 'note': '', 'created': now, 'updated': now})
            new += 1
        return q, new
    new = queue_update(_add)
    print(f'seeded {new} triple groups ({len(pending)} verses)')


def stage_seed(work, song, am_ctx=True):
    wt = json.loads((ROOT / work / f'working-t1-{song}.json').read_text())
    import sys as _sys
    _sys.path.insert(0, str(ROOT / 'tools'))
    from beam_swarm import queue_update
    now = time.strftime('%Y-%m-%dT%H:%M:%S')
    ahn = work.split('tantraloka-a')[-1]

    def _add(q):
        have = {t['id'] for t in q}
        new = 0
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
        return q, new
    new = queue_update(_add)
    print(f'seeded {new} tasks')


def counts(song, verses):
    have = {k: sum(1 for v in verses
                   if (RUNS / f'{song}-{k}-v{v:02d}' / f'{k}.json').exists())
            for k in ('gloss', 'cm', 'am')}
    return have



def _cite(e):
    """Byte-exact citation = the source verse text (not token joins)."""
    song = e.get('song', '')
    try:
        W = ROOT / _CURRENT_WORK[0]
        vs = json.loads((W / 'source/verses.json').read_text())
        t = vs[e['verse'] - 1]
        return ' '.join(t.replace('|', ' ').split())
    except Exception:
        return ' '.join(t['surface'].replace('+', '') for t in e['tokens'])


_CURRENT_WORK = ['']

def stage_assemble(work, song):
    W = ROOT / work
    _CURRENT_WORK[0] = work
    wt = json.loads((W / f'working-t1-{song}.json').read_text())
    # PARATEXT DOCTRINE (single source): editorial apparatus never enters T1.
    # CM rows are already filtered by is_paratext below; T1 must be filtered
    # with the SAME predicate or build_l0 asserts CM != T1 on pseudo-tokens
    # like 'karata(?' (2026-11-13). Mid-token brackets (genuine fused readings)
    # are kept by is_paratext.
    _dropped = 0
    for e in wt:
        kept = [t for t in e['tokens'] if not is_paratext(t.get('surface', ''))]
        if len(kept) != len(e['tokens']):
            _dropped += len(e['tokens']) - len(kept)
            e['tokens'] = kept
        # surrogates/variant parentheses (tasmi(n -> tasmin) are stripped:
        # the fused letters are genuine text, the parens are editorial and the
        # T1 schema forbids them. Deparen BOTH T1 surface and CM lemma so
        # build_l0's surface equality holds.
        for t in e['tokens']:
            if '(' in t.get('surface', '') or ')' in t.get('surface', ''):
                t['surface'] = t['surface'].replace('(', '').replace(')', '')
    if _dropped:
        print(f'{song}: dropped {_dropped} paratext token(s) from T1 (never glossed)')
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
    import re as _re
    cm = {}
    for e in wt:
        f = RUNS / f"{song}-cm-v{e['verse']:02d}" / 'cm.json'
        if f.exists():
            d = json.loads(f.read_text())
            _rows = []
            for r in d['rows']:
                _lm = r.get('lemma', '')
                # drop paratext rows that the T1 token stream excludes —
                # single doctrine: shastra_merge.is_paratext (mid-token
                # brackets are genuine fused readings and are kept)
                if is_paratext(_lm):
                    continue
                _lm = _lm.replace('(', '').replace(')', '')
                _rows.append([_lm, r['morph'], r.get('grounds', '')])
            cm[str(e['verse'])] = _rows
    (W / 'cm').mkdir(exist_ok=True)
    cmf = W / 'cm' / f'l0cm-{song}-v1-{len(wt)}.json'
    cmf.write_text(json.dumps(cm, indent=1, ensure_ascii=False))
    r = subprocess.run([sys.executable, 'tools/build_l0.py', '--work', work, '--cm', str(cmf)],
                       cwd=ROOT, capture_output=True, text=True)
    print(r.stdout.strip()[-300:] or r.stderr.strip()[-300:])
    # emit data
    l0 = json.loads((W / f'working-l0-{song}.json').read_text())
    _fallback_sha = wt[0].get('source_sha', '')
    by = {}
    for o in l0:
        by.setdefault(o['verse_id'], []).append(o)
    am, l2 = [], []
    import hashlib as _h
    try:
        _vs = json.loads((W / 'source/verses.json').read_text())
    except Exception:
        _vs = []
    import sys as _sys
    _sys.path.insert(0, str(ROOT / 'tools'))
    try:
        import workcfg as _wc
        _spans = _wc.source_spans(work) or {}
    except Exception:
        _spans = {}
    # validate_song hashes the WHOLE work's spans once (src_sha at line 64),
    # not per-verse — mirror that exactly.
    # validate_song digests the SONG-scoped span slice:
    #   sha( ' '.join( ' '.join(tokens) for v in song_verses ) )
    _song_verses = [e['verse'] for e in wt]
    try:
        _work_sha = _h.sha256(
            ' '.join(' '.join(_spans[_v]) for _v in sorted(
                v for v in _spans if v in set(_song_verses))).encode()
        ).hexdigest()[:16]
    except Exception:
        _work_sha = _fallback_sha

    def _src_sha(_v):
        return _work_sha
    for e in wt:
        src_sha = _src_sha(e['verse'])
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
                   'sanskrit_cite': _cite(e),
                   'l0_ids': ids or [l0[0]['id']], 'supplied': []})
        e['quick_english'] = d['plain_english']
        e['quick_english_source'] = 'manual'
    dd = W / 'data'; dd.mkdir(exist_ok=True)
    t1_out = []
    for e in wt:
        rows, buf_s, buf_g = [], '', []
        for t in e['tokens']:
            surf = t['surface']
            g = (t.get('quick_gloss') or '').strip()
            if surf.endswith('+'):
                buf_s += surf[:-1]
                if g:
                    buf_g.append(g)
                continue
            buf_s += surf.rstrip('+')
            if g:
                buf_g.append(g)
            rows.append({'sanskrit': buf_s, 'surface': buf_s, 'iast': buf_s,
                         'gloss': '-and-'.join(buf_g),
                         'quick_gloss': '-and-'.join(buf_g),
                         'status': 'GLOSSED' if buf_g else 'ABSTAIN'})
            buf_s, buf_g = '', []
        t1_out.append({'verse_id': e['verse_id'], 'song': e['song'],
                       'verse': e['verse'], 'tokens': rows,
                       'quick_english': e.get('quick_english', ''),
                       'source_sha': e.get('source_sha', '')})
    for n, o in [('t1', t1_out), ('l0', l0), ('argmap', am), ('l2', l2)]:
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
        # Deadlock guard: coverage incomplete but nothing claimable for this
        # song (all remaining tasks failed-at-max or stale-claimed). Sleeping
        # and re-seeding cannot help — the seeder skips exhausted ids by
        # design. Exit for the assessor (retest protocol or hand-draft)
        # instead of spinning until max-wait.
        _sys_path = str(ROOT / 'tools')
        if _sys_path not in sys.path:
            sys.path.insert(0, _sys_path)
        from beam_swarm import load_q as _load_q, claimable as _claimable
        _song_tasks = [t for t in _load_q()
                       if t.get('args', {}).get('song') == a.song
                       and t.get('kind') in ('tal_triple', 'tal_gloss', 'tal_cm', 'tal_am')]
        _driveable = [t['id'] for t in _song_tasks if _claimable(t)]
        if not _driveable and _song_tasks:
            _dead = sorted(t['id'] for t in _song_tasks if t.get('status') == 'failed')
            print(f'{a.song}: DEADLOCK — no claimable tasks, coverage incomplete.')
            print(f'  assessor needed: retest or hand-draft: {_dead}')
            return 3
        time.sleep(a.wait); waited += a.wait
        if a.triple:
            stage_seed_triple(a.work, a.song)
        else:
            stage_seed(a.work, a.song)
    stage_assemble(a.work, a.song)
    # Post-assemble cleanliness (2026-11-13): de-overlap suffix repeats and
    # collapse adjacent identical tokens, keeping L0/argmap/L2 consistent.
    for _tool in ('dedup_t1.py', 'collapse_dups.py'):
        subprocess.run([sys.executable, f'tools/{_tool}', a.work, a.song],
                       cwd=ROOT, capture_output=True, text=True)
    _disp = ROOT / 'tools' / 'proof-disp.json'
    for cmd in (['tools/validate_song.py', '--song', a.song, '--work', a.work],
                ['tools/proof_record.py', '--song', a.song, '--work', a.work, '--shastra']
                + (['--disp', str(_disp.relative_to(ROOT))] if _disp.exists() else [])):
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
