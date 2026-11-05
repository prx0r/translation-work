#!/usr/bin/env python3
"""tools/build_source_records.py — write <work>/source/record.json for every work.

Uniform source record (source-record/1): edition, witness (always UNKNOWN
until resolved with evidence), openpatala mapping (from source-maps/
openpatala.json), rights (parsed from source headers, never assumed),
selectors, acquisition (UNKNOWN where not logged — never fabricated),
volumes[] linking the byte-span manifests (source/volumes/*.json or
source/manifest.json + segments.json).

Works with no resolvable source get an explicit NO-SOURCE-RECORD record, not
silence. Deterministic: rerun any time; refuses to overwrite a record whose
volume hashes changed without --update (prevents silent drift).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))

FORMAT = 'svatantrya-source-record/1'


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def header_lines(path: Path, n: int = 6) -> list[str]:
    try:
        return path.read_text(encoding='utf-8').splitlines()[:n]
    except (OSError, ValueError):
        return []


def rights_from_header(head: list[str]) -> dict:
    text = '\n'.join(head)
    if 'CC BY-NC-SA 4.0' in text:
        return {'status': 'KNOWN-NC',
                'statement_ref': 'CC BY-NC-SA 4.0 per source header (study-only; no commercial reuse incl. books)'}
    if 'CC BY-NC 4.0' in text:
        return {'status': 'KNOWN-NC',
                'statement_ref': 'CC BY-NC 4.0 per source header (study-only; no commercial reuse incl. books)'}
    return {'status': 'UNKNOWN',
            'statement_ref': 'no licence statement in source header — treat as ALL-RIGHTS-RESERVED until confirmed'}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--update', action='store_true',
                    help='rewrite records whose volume bytes changed')
    args = ap.parse_args()
    import workcfg
    registry = json.loads((ROOT / 'REGISTRY.json').read_text(encoding='utf-8'))
    names = set()
    for w in registry.get('works', []):
        if isinstance(w, dict) and (w.get('work') or w.get('id')):
            names.add(w.get('work') or w.get('id'))
    names.add('ipvv')
    try:
        omap = json.loads((ROOT / 'source-maps' / 'openpatala.json').read_text(
            encoding='utf-8'))['works']
    except (OSError, ValueError):
        omap = {}
    wrote, kept, missing = 0, 0, []
    for work in sorted(names):
        rec_path = ROOT / work / 'source' / 'record.json'
        volumes, edition, rights = [], {}, {'status': 'UNKNOWN',
                                            'statement_ref': 'unresolved (see per-volume notes)'}
        origin = 'UNKNOWN'
        try:
            cfg = workcfg.work_config(work)
        except Exception:
            cfg = None
        if cfg is not None and cfg.get('source'):
            src = Path(cfg['source'])
            if src.is_file() and src.suffix != '.md':
                raw = src.read_bytes()
                head = header_lines(src)
                prov = next((l for l in head if 'Provenance' in l), '')
                edition = {'label': re.sub(r'^#+\s*', '', prov) or src.name,
                           'status': 'candidate'}
                rights = rights_from_header(head)
                origin = ('GRETIL' if 'GRETIL' in prov else
                          'Mukhabodha' if 'Mukhabodha' in prov or 'Muktabodha' in prov
                          else 'SanskritDocuments' if 'anskritocument' in prov else 'UNKNOWN')
                try:
                    vmanifests = sorted((ROOT / work / 'source' / 'volumes').glob('*.json'))
                except OSError:
                    vmanifests = []
                for vm in vmanifests:
                    try:
                        m = json.loads(vm.read_text(encoding='utf-8'))
                    except ValueError:
                        continue
                    volumes.append({
                        'vol': m.get('vol', vm.stem),
                        'file': m.get('source_file', ''),
                        'sha256': m.get('content_sha256', ''),
                        'bytes': m.get('bytes', 0),
                        'spans_manifest': 'source/volumes/' + vm.name,
                        'spans': len(m.get('spans', [])),
                        'overlaps': len(m.get('overlaps', [])),
                        'gaps': len(m.get('gaps', []))})
            elif src is not None and src.suffix == '.md':
                head = header_lines(src)
                edition = {'label': (re.sub(r'^#+\s*', '', head[0])
                                     if head else src.name), 'status': 'staged-prior-translation'}
                rights = {'status': 'OUR-DRAFT-UNREVIEWED',
                            'statement_ref': 'staged prior translation, machine-proposed; not a source edition'}
                origin = 'in-repo-staged'
                try:
                    rel = src.relative_to(ROOT).as_posix()
                except ValueError:
                    rel = src.as_posix()
                raw = src.read_bytes()
                volumes.append({
                    'vol': 'staged', 'file': rel, 'sha256': sha(raw),
                    'bytes': len(raw), 'spans_manifest': '',
                    'spans': '', 'overlaps': '', 'gaps': '',
                    'note': 'staged reading doc, not byte-mapped; translation layers trace here until a source edition is intaked'})
        # legacy segments path (source/manifest.json + segments.json)
        man_path = ROOT / work / 'source' / 'manifest.json'
        if not volumes and man_path.is_file():
            try:
                man = json.loads(man_path.read_text(encoding='utf-8'))
                seg_path = ROOT / work / 'source' / 'segments.json'
                seg_bytes = seg_path.read_bytes() if seg_path.is_file() else b''
                edition = {'label': man.get('edition', ''), 'status': 'candidate'}
                origin = 'intake-manifest'
                volumes = [{'vol': 'main', 'file': 'source/edition.txt',
                            'sha256': man.get('source_sha256', ''),
                            'bytes': man.get('segments_sha256', '') and len(seg_bytes) or 0,
                            'spans_manifest': 'source/manifest.json',
                            'spans': '',
                            'overlaps': '', 'gaps': ''}]
                if 'CC BY-NC-SA' in man.get('license', '') or 'BY-NC-SA' in man.get('source_license', ''):
                    rights = {'status': 'KNOWN-NC',
                              'statement_ref': 'CC BY-NC-SA per intake manifest (study-only)'}
            except (OSError, ValueError):
                pass
        if work == 'ipvv' and not volumes:
            vols = {'M00020': 'ipvv-vol1.txt', 'M00021': 'ipvv-vol2.txt',
                    'M00022': 'ipvv-vol3.txt'}
            edition = {'label': 'Mukhabodha M00020/21/22 (Torella IPK base); Torella alignment unverified',
                       'status': 'candidate'}
            rights = {'status': 'KNOWN-NC',
                      'statement_ref': 'CC BY-NC 4.0 per volume headers (study-only; no commercial reuse)'}
            origin = 'Mukhabodha'
            for vol, fn in vols.items():
                p = ROOT.parent / 'ipvv' / 'site' / 'data' / 'sanskrit' / fn
                vm = ROOT / 'ipvv' / 'source' / 'volumes' / f'{vol}.json'
                m = json.loads(vm.read_text(encoding='utf-8')) if vm.is_file() else {}
                volumes.append({
                    'vol': vol, 'file': f'../ipvv/site/data/sanskrit/{fn}',
                    'sha256': sha(p.read_bytes()) if p.is_file() else '',
                    'bytes': p.stat().st_size if p.is_file() else 0,
                    'spans_manifest': f'source/volumes/{vol}.json',
                    'spans': len(m.get('spans', [])), 'overlaps': len(m.get('overlaps', [])),
                    'gaps': len(m.get('gaps', []))})
        om = omap.get(work, {})
        if not volumes:
            record = {'format': FORMAT, 'work': work, 'status': 'NO-SOURCE-RECORD',
                      'reason': 'no resolvable source bytes (no workcfg source, no manifest, no volumes)',
                      'witness': {'id': None, 'status': 'UNKNOWN'},
                      'openpatala': {'work_id': om.get('openpatala_work_id'),
                                     'mapping_status': om.get('mapping_status', 'UNMAPPED'),
                                     'evidence_refs': om.get('evidence_refs', [])}}
            missing.append(work)
        else:
            content = sha(json.dumps(
                sorted(v['sha256'] for v in volumes),
                sort_keys=True).encode())
            record = {
                'format': FORMAT, 'work': work, 'status': 'RECORDED',
                'source_id': f"{work}-{content[:16]}",
                'content_sha256': content,
                'bytes': sum(v['bytes'] for v in volumes if isinstance(v['bytes'], int)),
                'edition': edition,
                'witness': {'id': None, 'status': 'UNKNOWN'},
                'openpatala': {
                    'work_id': om.get('openpatala_work_id'),
                    'mapping_status': om.get('mapping_status', 'UNMAPPED'),
                    'scope': om.get('scope', 'work'),
                    'evidence_refs': om.get('evidence_refs', []),
                    'dossier_sha256': (om.get('dossier') or {}).get('sha256')},
                'rights': rights,
                'selectors': {'unit': 'utf8-byte', 'end': 'exclusive'},
                'acquisition': {
                    'origin': origin,
                    'retrieved_at': 'UNKNOWN (vendored before provenance logging; do not fabricate)',
                    'acquired_by': 'UNKNOWN'},
                'volumes': volumes,
            }
        if rec_path.is_file() and not args.update:
            try:
                prior = json.loads(rec_path.read_text(encoding='utf-8'))
            except ValueError:
                prior = None
            if prior == record:
                kept += 1
                continue
            if prior is not None and prior != record:
                print(f'skip (changed, needs --update): {work}')
                continue
        rec_path.parent.mkdir(parents=True, exist_ok=True)
        rec_path.write_text(json.dumps(record, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
        wrote += 1
    print(f'records: wrote {wrote}, kept {kept}, missing-source: {len(missing)} {missing[:10]}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
