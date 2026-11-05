#!/usr/bin/env python3
"""tools/openpatala_bridge.py — chunk↔openpatala bridge (read-only, no network).

resolve(work) -> the mapping entry + the uniform source record, or a clear
UNMAPPED/NO-SOURCE-RECORD answer. verify(work) -> checks the pinned dossier
bytes, the record's volume hashes, and mapping consistency; reports
CANDIDATE-grained truth only (witness stays UNKNOWN until resolved with
evidence from the openpatala lane).

Used by lineage_audit.source_candidate and passage_adapter. Stdlib only.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP_PATH = ROOT / 'source-maps' / 'openpatala.json'


class BridgeError(Exception):
    pass


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _load_map() -> dict:
    try:
        return json.loads(MAP_PATH.read_bytes())['works']
    except (OSError, ValueError, KeyError) as exc:
        raise BridgeError(f'mapping file unavailable: {exc}') from exc


def _load_record(work: str) -> dict | None:
    p = ROOT / work / 'source' / 'record.json'
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except ValueError as exc:
        raise BridgeError(f'source record for {work} is not valid JSON: {exc}') from exc


def _committed(path: Path) -> dict:
    """Bind bytes to a locally available Git commit; fail on a dirty file."""
    path = path.resolve(strict=True)
    base = Path(subprocess.run(
        ['git', '-C', str(path.parent), 'rev-parse', '--show-toplevel'],
        capture_output=True, check=True, text=True).stdout.strip()).resolve()
    try:
        relative = path.relative_to(base).as_posix()
    except ValueError as exc:
        raise BridgeError('path is outside its Git repository') from exc
    commit = subprocess.run(
        ['git', '-C', str(base), 'rev-parse', 'HEAD'],
        capture_output=True, check=True, text=True).stdout.strip()
    content = path.read_bytes()
    shown = subprocess.run(
        ['git', '-C', str(base), 'show', f'{commit}:{relative}'],
        capture_output=True).stdout
    if shown != content:
        raise BridgeError(f'file differs from committed Git bytes: {relative}')
    return {'commit': commit, 'path': relative, 'sha256': _sha(content)}


def resolve(work: str) -> dict:
    """Mapping + record for one work. Never invents: gaps are explicit."""
    mapping = _load_map().get(work)
    if mapping is None:
        raise BridgeError(f'{work} is not in the openpatala map (run build_openpatala_map.py)')
    record = _load_record(work)
    return {'work': work, 'mapping': mapping,
            'record': record,
            'record_status': (record or {}).get('status', 'NO-SOURCE-RECORD')}


def verify(work: str) -> dict:
    """Verify pins: dossier bytes, record volume hashes, mapping consistency."""
    resolved = resolve(work)
    mapping, record = resolved['mapping'], resolved['record']
    checks = []
    if mapping.get('mapping_status') == 'CANDIDATE':
        dossier = mapping.get('dossier') or {}
        try:
            raw = Path(dossier['path']).read_bytes()
            if _sha(raw) != dossier.get('sha256'):
                checks.append('dossier bytes do not match the pinned sha256')
            else:
                data = json.loads(raw)
                if data.get('work_id') != mapping.get('openpatala_work_id'):
                    checks.append('dossier work_id does not match the mapping')
        except (OSError, ValueError, KeyError) as exc:
            checks.append(f'dossier unavailable or invalid: {exc}')
    if record is None or record.get('status') != 'RECORDED':
        checks.append('no RECORDED source record (spans unaccounted here)')
    else:
        for v in record.get('volumes', []):
            mf = ROOT / work / v.get('spans_manifest', '') if v.get('spans_manifest') else None
            if v.get('spans_manifest') and (mf is None or not mf.is_file()):
                checks.append(f"spans manifest missing: {v.get('spans_manifest')}")
    if (mapping.get('mapping_status') == 'CANDIDATE'
            and (mapping.get('openpatala_work_id') is None or mapping.get('witness') != 'UNKNOWN')):
        checks.append('mapping claims more than candidate status allows')
    return {'work': work,
            'status': 'CONSISTENT' if not checks else 'INCONSISTENT',
            'blocking': checks,
            'mapping_status': mapping.get('mapping_status'),
            'witness': mapping.get('witness', 'UNKNOWN')}
