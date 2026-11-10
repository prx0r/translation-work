#!/usr/bin/env python3
"""registry_sync — openpatala DB × translation-work REGISTRY → ranked PLAN + swarm seeds.

The DB is the universe (544 works, passage counts). REGISTRY.json + local
STATUS files are the truth of what's done. PRIORITY (below, editable) is the
strategy: Trika core authors first, untranslated before polish, shortest
first within tiers. Mystics + sourceless works stay deferred (owner gate).

Output: process/beam/PLAN.json — ranked items
  {db_work, local_work, tier, kind, reason}
kind: recon | brief | pilot | lore | transform | convert | review | proof | deferred
Swarmable kinds (recon/brief/pilot/lore) auto-seed the swarm queue with
--seed. transform/convert/review/proof are assessor-lane (listed, not queued).

Usage:
  python3 tools/registry_sync.py [--seed] [--db DSN]
"""
from __future__ import annotations
import json, os, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))

# --- priority config (edit me; owner wins ties) ---
TIER_ABHINAVAGUPTA = 'T0-abhinavagupta'   # finish the core author first
TIER_TRIKA = 'T1-trika-circle'             # Ksemaraja / Utpaladeva gaps
TIER_OTHER = 'T2-other'                   # rest of the canon, shortest-first
TIER_DEFERRED = 'T3-deferred'             # needs owner nod / missing prereq

ABHINAVAGUPTA = {'tantrasara', 'tantraloka', 'paramarthasara', 'paratrimshika',
                 'dehastha', 'bodhapancadasika', 'anuttarastika', 'paramarthacarca',
                 'anubhavanivedana', 'gitarthasangraha', 'ipvv'}
                 # NOTE (NEVER.md, owner 2026-11-10): 'abhinavabharati' removed —
                 # non-Trika (poetics) + source unready. Never re-add without owner order.
TRIKA_CIRCLE = {'sivasutra', 'spanda', 'sivasutravimarsini', 'spandasandoha',
                'svabodhasiddhi', 'saktavijnana', 'bodhavilasa', 'bhairavanukarana',
                'ajadapramatrsiddhi', 'isvarasiddhi', 'sambandhasiddhi',
                'sivastotravali', 'stavacintamani', 'kramastotra', 'phrdaya',
                'malinivijayavarttika'}
DEFERRED = {'lalded', 'rupabhavani', 'parmanand', 'nundrishi', 'santosh'}
            # mystics need Kashmiri stage (see NEVER.md — permanently out of scope).
            # tattvasandoha graduated 2026-11-10 (mula minimal-gold); commentary
            # still needs Muktabodha M00151 bytes (owner-gated).


def tier_of(db_work: str) -> str:
    base = db_work.split('-')[0] if '-' not in ('tantrasara', 'tantraloka', 'ipvv') else db_work
    stem = db_work.split('-')[0]
    if db_work in DEFERRED or stem in DEFERRED:
        return TIER_DEFERRED
    if stem in ABHINAVAGUPTA or db_work in ABHINAVAGUPTA:
        return TIER_ABHINAVAGUPTA
    if stem in TRIKA_CIRCLE or db_work in TRIKA_CIRCLE:
        return TIER_TRIKA
    return TIER_OTHER


def find_source(db_work: str) -> str:
    """Best-effort source file for a DB work in known mirrors."""
    import glob as _g
    cands = []
    cands += _g.glob(f'/root/ipvv/site/data/sanskrit/{db_work}.txt')
    cands += _g.glob(f'/root/ipvv/site/data/sanskrit/*{db_work}*.txt')
    cands += _g.glob(f'/root/translation-work/source-maps/{db_work}*')
    return cands[0] if cands else ''


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', action='store_true')
    ap.add_argument('--db', default=os.environ.get('OPENPATALA_DSN',
        'postgresql://patala:patala@localhost:5432/openpatala_box'))
    a = ap.parse_args()
    import psycopg2
    con = psycopg2.connect(a.db)
    cur = con.cursor()
    cur.execute('SELECT id FROM works ORDER BY id')
    db_works = [r[0] for r in cur.fetchall()]
    cur.execute('SELECT work_id, count(*) FROM passages GROUP BY work_id')
    pcounts = dict(cur.fetchall())
    con.close()

    reg = json.load(open(ROOT / 'REGISTRY.json'))
    local = {}
    for w in reg['works']:
        local[w['work']] = w
    # ipvv is a program dir, not a REGISTRY work: derive from its STATUS
    ipvv_st = ROOT / 'ipvv' / 'STATUS.json'
    if ipvv_st.exists():
        st = json.load(open(ipvv_st))
        npp = len(st.get('counts', {}).get('shastra_pass', []))
        local['ipvv'] = {'work': 'ipvv', 'status': 'shastra-minimal program',
                         'gold': npp >= 49,
                         'note': f"{npp}/49 shastra PASS; T1/L0 49/49 closed"}
    # local STATUS proof state
    from workcfg import chunk_id_for  # noqa  (validates mapping only)
    _ = chunk_id_for

    plan = []
    for dw in sorted(db_works):
        tier = tier_of(dw)
        # map DB work -> local work dir (same id for tsa/tal flat works; ipvv single work)
        lw = 'ipvv' if dw == 'ipvv' else dw
        entry = local.get(lw)
        npass = pcounts.get(dw, 0)
        if tier == TIER_DEFERRED:
            plan.append({'db_work': dw, 'local_work': lw, 'tier': tier,
                         'kind': 'deferred', 'reason': 'owner-gated (mystics stage / no source)'})
            continue
        if not entry:
            if npass == 0:
                continue  # container/parent DB entry with no passages and no local work: nothing to do
            plan.append({'db_work': dw, 'local_work': lw, 'tier': tier,
                         'kind': 'recon',
                         'reason': f'in DB ({npass} passages), no local work dir — intake first'})
            continue
        if not entry.get('gold'):
            note = (entry.get('note') or '')[:80]
            kind = 'transform' if 'recon complete' in (entry.get('status') or '') else 'translate'
            plan.append({'db_work': dw, 'local_work': lw, 'tier': tier,
                         'kind': kind, 'reason': f'pending: {entry.get("status")}; {note}'})
            continue
        # gold: check proof state via STATUS.json
        sp = ROOT / lw / 'STATUS.json'
        needs = ''
        if sp.exists():
            st = json.load(open(sp))
            needs = str(st.get('next', ''))[:100]
        plan.append({'db_work': dw, 'local_work': lw, 'tier': tier,
                     'kind': 'review', 'reason': f'gold; next: {needs}'})

    order = {TIER_ABHINAVAGUPTA: 0, TIER_TRIKA: 1, TIER_OTHER: 2, TIER_DEFERRED: 3}
    plan.sort(key=lambda e: (order[e['tier']], 0 if e['kind'] in ('recon', 'transform', 'convert') else 1, e['db_work']))
    out = ROOT / 'process' / 'beam' / 'PLAN.json'
    out.write_text(json.dumps({'generated': __import__('datetime').datetime.now().isoformat(timespec='seconds'),
                               'items': plan}, indent=1))
    kinds: dict[str, int] = {}
    for e in plan:
        kinds[e['kind']] = kinds.get(e['kind'], 0) + 1
    print(f'PLAN: {len(plan)} db works -> {json.dumps(kinds)}')
    for e in [x for x in plan if x['kind'] in ('recon', 'transform', 'convert')][:15]:
        print(f"  [{e['tier']}] {e['kind']:9} {e['db_work']:28} {e['reason'][:70]}")

    if a.seed:
        qpath = ROOT / 'process' / 'beam' / 'queue.json'
        q = json.loads(qpath.read_text()) if qpath.exists() else []
        have = {t['id'] for t in q}
        import datetime
        now = datetime.datetime.now().isoformat(timespec='seconds')
        added = 0
        for e in plan:
            if e['kind'] != 'recon':
                continue
            tid = f"recon-{e['db_work']}"
            if tid in have:
                continue
            src = find_source(e['db_work'])
            if not src:
                continue  # assessor resolves source layout first; stays listed, unqueued
            q.append({'id': tid, 'kind': 'recon', 'args': {'path': src, 'topic': e['db_work']},
                      'status': 'pending', 'attempts': 0, 'max_attempts': 3,
                      'worker': '', 'note': '', 'created': now, 'updated': now})
            added += 1
        json.dump(q, open(qpath, 'w'), indent=1)
        print(f'seeded {added} recon tasks (source auto-resolved; rest await assessor)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
