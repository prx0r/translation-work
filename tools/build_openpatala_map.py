#!/usr/bin/env python3
"""tools/build_openpatala_map.py — (re)build source-maps/openpatala.json.

Deterministic from live inputs: openpatala gold dossiers (external GRETIL
IDs), our workcfg sources, REGISTRY works. No hand edits — rerun instead.
Mapping is CANDIDATE (ID match only, never witness attestation) or UNMAPPED.
Tantrasara ahnikas map PART-OF the whole-text dossier (scope: part).
Legacy source-maps/<work>.json files stay untouched (old receipts pin them).
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import workcfg  # noqa: E402

OPENPATALA = Path('/root/openpatala')
FORMAT = 'svatantrya-openpatala-map/1'


def dossier_gretil_ids() -> dict[str, dict]:
    out = {}
    for f in sorted((OPENPATALA / 'data' / 'gold').glob('*.json')):
        try:
            d = json.loads(f.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            continue
        for x in d.get('external_identifiers', []) or []:
            if x.get('scheme') == 'GRETIL' and x.get('identifier'):
                out[x['identifier']] = {
                    'work_id': d.get('work_id'), 'path': str(f),
                    'sha256': hashlib.sha256(f.read_bytes()).hexdigest(),
                    'language_assertions': sorted({
                        str(a.get('literal')) for a in d.get('assertions', [])
                        if a.get('predicate') == 'LANGUAGE'}),
                }
    return out


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r'^sa_', '', s)
    return re.sub(r'[^a-z]', '', s)


def header_evidence(*paths: Path) -> list[str]:
    """External-ID mentions from source-file header lines (evidence, not identity)."""
    found: list[str] = []
    for p in paths:
        try:
            if not (p and p.is_file()):
                continue
            head = '\n'.join(p.read_text(encoding='utf-8').splitlines()[:8])
        except (OSError, ValueError):
            continue
        for m in re.finditer(r'Muktab?odha\s+(M\d+)', head):
            tag = 'MUKHABODHA:' + m.group(1)
            if tag not in found:
                found.append(tag)
        for m in re.finditer(r'\bsa_[A-Za-z-][A-Za-z-]*\b', head):
            tag = 'GRETIL-mention:' + m.group(0)
            if tag not in found:
                found.append(tag)
        if 'sanskritdocuments' in head.lower() and not any(
                t.startswith('SANSKRITDOCUMENTS') for t in found):
            found.append('SANSKRITDOCUMENTS:edition-cited-in-header')
    return found


def main() -> int:
    dossiers = dossier_gretil_ids()
    registry = json.loads((ROOT / 'REGISTRY.json').read_text(encoding='utf-8'))
    names = set()
    for w in registry.get('works', []):
        if isinstance(w, dict) and (w.get('work') or w.get('id')):
            names.add(w.get('work') or w.get('id'))
    names.add('ipvv')
    entries = {}
    for work in sorted(names):
        src = None
        try:
            cfg = workcfg.work_config(work)
            if cfg and cfg.get('source'):
                src = Path(cfg['source'])
        except Exception:
            cfg = None
        entry = {'work': work, 'openpatala_work_id': None, 'scope': 'work',
                 'mapping_status': 'UNMAPPED', 'external_identifier': None,
                 'evidence_refs': [],
                 'dossier': None, 'witness': 'UNKNOWN',
                 'edition_verified': False, 'language_conflict': None,
                 'note': 'no Work-level openpatala ID found'}
        if src is not None and src.is_file():
            try:
                rel = src.relative_to(ROOT)
                in_repo_staged = True
            except ValueError:
                in_repo_staged = False
            if in_repo_staged:
                entry['note'] = ('in-repo staged source (T1.md/edition.txt); '
                                 'no Work-level openpatala ID — UNMAPPED until assigned')
                ev = header_evidence(src)
                if ev:
                    entry['evidence_refs'] = ev
                    entry['note'] = ('in-repo staged source; header cites '
                                     + ', '.join(ev)
                                     + ' — recorded as evidence, still UNMAPPED (no dossier)')
                if cfg and cfg.get('kind') == 'segments':
                    man = ROOT / work / 'source' / 'manifest.json'
                    try:
                        ed = json.loads(man.read_text(encoding='utf-8')).get('edition', '')
                    except (OSError, ValueError):
                        ed = ''
                    m = re.search(r'\bsa_[A-Za-z-][A-Za-z-]*', ed)
                    if m:
                        gid = next((g for g in dossiers
                                    if norm(g) == norm(m.group(0))), None)
                        if gid is not None:
                            d = dossiers[gid]
                            entry.update({
                                'openpatala_work_id': d['work_id'], 'scope': 'work',
                                'mapping_status': 'CANDIDATE',
                                'external_identifier': ['GRETIL', gid],
                                'dossier': {'path': d['path'], 'sha256': d['sha256']},
                                'language_conflict': bool(
                                    d['language_assertions']
                                    and 'sa' not in d['language_assertions']),
                                'note': ('manifest edition names a GRETIL e-text; candidate work '
                                         'mapping only — does not authenticate edition or witness'),
                            })
                        else:
                            entry.update({
                                'external_identifier': ['GRETIL', m.group(0)],
                                'note': ('manifest edition names GRETIL e-text '
                                         + m.group(0) + '; no openpatala dossier yet — UNMAPPED'),
                            })
            else:
                base = norm(src.stem)
                for gid, d in dossiers.items():
                    g = norm(gid)
                    if len(base) < 6 or len(g) < 6:
                        continue
                    strong = (base == g or
                              (len(base) >= 10 and base in g) or
                              (len(g) >= 10 and g in base))
                    if not strong:
                        continue
                    # Tantrasara ahnikas share the whole-text source file.
                    scope = 'part' if re.fullmatch(r'tantrasara-a\d+', work) else 'work'
                    entry.update({
                        'openpatala_work_id': d['work_id'], 'scope': scope,
                        'mapping_status': 'CANDIDATE',
                        'external_identifier': ['GRETIL', gid],
                        'dossier': {'path': d['path'], 'sha256': d['sha256']},
                        'language_conflict': bool(
                            d['language_assertions']
                            and 'sa' not in d['language_assertions']),
                        'note': ('GRETIL external-ID match; candidate work mapping only — '
                                 + ('ahnika of the whole text; ' if scope == 'part' else '')
                                 + 'does not authenticate edition or witness'),
                    })
                    break
            for tag in header_evidence(src):
                if tag not in entry['evidence_refs']:
                    entry['evidence_refs'].append(tag)
        entries[work] = entry
    out = {'format': FORMAT,
           'note': 'CANDIDATE = shared external ID only. Witness stays UNKNOWN until resolved with evidence.',
           'works': entries}
    path = ROOT / 'source-maps' / 'openpatala.json'
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
    n_cand = sum(1 for e in entries.values() if e['mapping_status'] == 'CANDIDATE')
    print(f'{path}: {len(entries)} works, {n_cand} CANDIDATE')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
