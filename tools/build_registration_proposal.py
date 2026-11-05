#!/usr/bin/env python3
"""tools/build_registration_proposal.py — openpatala registration PROPOSAL.

We do not edit openpatala's data (its availability file is a Postgres
projection — "translation-availability is a projection, not primary truth").
This file proposes entries their lane can ingest: per work, factory states in
their vocabulary + our translation with rights + evidence pointers.

Vocabulary (theirs): factory t1/l2/c1 ∈ UNKNOWN/NOT_STARTED/MODERN_PRESENT/
LEGACY_PRESENT; next_action ∈ null/BUILD_L0_SOURCE_MODE/imported/
ACQUIRE_SOURCE; tier ∈ A/B/C/D; type scholarly|traditional|independent.
Ours: gold (human-reviewed) → MODERN_PRESENT tier A; gold machine-proposed →
MODERN_PRESENT tier B; legacy/staged (incl. ipvv T1+L2, unproven) →
LEGACY_PRESENT; pending/no-source → NOT_STARTED + ACQUIRE_SOURCE.
complete=true only when every data song carries a PASS proof.
"""
from __future__ import annotations

import glob
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))

OUT = ROOT / 'openpatala-registration.json'
FORMAT = 'svatantrya-openpatala-registration-proposal/1'


def proof_fresh(work: str, song: str) -> bool:
    """PASS proof whose recorded layer hashes match current data (emit rule)."""
    import hashlib
    def sha(o):
        return hashlib.sha256(json.dumps(o, sort_keys=True, separators=(',', ':'),
                                         ensure_ascii=False).encode()).hexdigest()
    try:
        p = json.loads((ROOT / work / 'proof' / f'proof-{song}.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return False
    if p.get('deterministic_gate') != 'PASS':
        return False
    rec = p.get('layer_sha256', {})
    cur = {}
    for layer in ('t1', 'l0', 'argmap', 'l2', 'c1', 'l3', 'l4', 'c2'):
        fp = ROOT / work / 'data' / f'{song}.{layer}.json'
        if fp.is_file():
            try:
                cur[layer] = sha(json.loads(fp.read_text(encoding='utf-8')))
            except ValueError:
                return False
    if not {'t1', 'l0', 'argmap', 'l2', 'c1'}.issubset(cur):
        return False
    return rec == cur


def proof_pass(work: str, song: str) -> bool:
    try:
        p = json.loads((ROOT / work / 'proof' / f'proof-{song}.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return False
    return p.get('deterministic_gate') == 'PASS'


def main() -> int:
    registry = json.loads((ROOT / 'REGISTRY.json').read_text(encoding='utf-8'))
    try:
        omap = json.loads((ROOT / 'source-maps' / 'openpatala.json').read_text(
            encoding='utf-8'))['works']
    except (OSError, ValueError):
        omap = {}
    existing_avail = set()
    proposals = []
    names = set()
    for w in registry.get('works', []):
        if isinstance(w, dict) and (w.get('work') or w.get('id')):
            names.add(w.get('work') or w.get('id'))
    names.add('ipvv')
    for work in sorted(names):
        status = next((w.get('status', '') for w in registry.get('works', [])
                       if isinstance(w, dict) and (w.get('work') == work or w.get('id') == work)), '')
        data_songs = sorted({os.path.basename(p).split('.')[0]
                             for p in glob.glob(str(ROOT / work / 'data' / '*.t1.json'))})
        songs = data_songs or []
        complete = bool(songs) and all(
            proof_fresh(work, s) for songs in [songs] for s in songs)
        mapping = omap.get(work, {})
        if status == 'gold':
            factory = {'t1': 'MODERN_PRESENT', 'l2': 'MODERN_PRESENT',
                       'c1': 'MODERN_PRESENT', 'next_action': None}
            tier, ttype = 'A', 'scholarly'
        elif status == 'gold (machine-proposed)':
            factory = {'t1': 'MODERN_PRESENT', 'l2': 'MODERN_PRESENT',
                       'c1': 'MODERN_PRESENT', 'next_action': None}
            tier, ttype = 'B', 'scholarly'
        elif work == 'ipvv' or status.startswith('legacy') or songs:
            factory = {'t1': 'LEGACY_PRESENT', 'l2': 'LEGACY_PRESENT',
                       'c1': 'LEGACY_PRESENT', 'next_action': 'BUILD_L0_SOURCE_MODE'}
            tier, ttype = 'C', 'scholarly'
        else:
            factory = {'t1': 'NOT_STARTED', 'l2': 'NOT_STARTED',
                       'c1': 'NOT_STARTED', 'next_action': 'ACQUIRE_SOURCE'}
            tier, ttype = 'D', 'scholarly'
        entry = {
            'key': work,
            'mapping_status': mapping.get('mapping_status', 'UNMAPPED'),
            'openpatala_work_id': mapping.get('openpatala_work_id'),
            'witness': 'UNKNOWN',
            'proposed_factory': factory,
            'proposed_translation': None if factory['t1'] == 'NOT_STARTED' else {
                'language': 'en',
                'translator': 'translation-work gold lane (machine-proposed until human review signs off)',
                'coverage': 'all data songs' if songs else 'no contract rows yet',
                'complete': complete,
                'type': ttype, 'tier': tier,
                'url': None,
                'url_note': 'served from svread Scholar hub (/data/scholar/<work>.json); deployment URL varies — resolve at ingest; reader verifies projection_sha256',
                'source': 'translation-work (this proposal)',
                'copyright_hint': 'UNDETERMINED (our English per emit rights is free use; source Sanskrit is NC-licensed; confirm per work before commercial use)',
            },
            'rights_note': ('source Sanskrit NC (GRETIL/Mukhabodha); our English free-use per emit; '
                            'commercial use needs per-work confirmation'),
            'evidence': {'dossier_sha256': (mapping.get('dossier') or {}).get('sha256'),
                         'evidence_refs': mapping.get('evidence_refs', [])},
        }
        proposals.append(entry)
    doc = {'format': FORMAT,
           'note': ('PROPOSAL only — openpatala availability is a Postgres projection; nothing here '
                    'edits their data. Tiers: A = human-reviewed gold, B = machine-proposed gold, '
                    'C = staged/legacy incl. IPVV (unproven), D = not started. complete=true only when '
                    'every data song carries a PASS proof.'),
           'works': proposals}
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
    by = {}
    for p in proposals:
        by[p['mapping_status']] = by.get(p['mapping_status'], 0) + 1
    print(f'{OUT}: {len(proposals)} proposed entries {by}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
