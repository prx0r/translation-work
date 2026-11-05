#!/usr/bin/env python3
"""tools/source_volumes.py — versioned add-source path for existing works.

intake.initialize() creates a work; it refuses existing dirs and enforces
verse-shaped IDs. Commentary prose (IPVV: 3 volumes, 49 chunks, opaque chunk
IDs, legacy line coords) needs a different contract: one manifest per volume
with verified byte spans, explicit gaps, and no verse-ID mangling.

record_volume() validates and writes `<work>/source/volumes/<vol>.json`:
  {format, work, vol, source_id, content_sha256, bytes, edition, license,
   spans: [{passage_id, start, end, vol_lines, legacy_coords, text_sha256}],
   gaps: [{start, end, note}], supersedes}

Rules: raw must be UTF-8; each span must lie within raw and its bytes must
equal the supplied bundle text (no silent normalization). Prose commentary
chunks may share boundary lines, so spans may overlap: every overlap is
recorded explicitly in `overlaps`, and `gaps` accounts for non-whitespace
bytes covered by no span (union coverage). Existing volume file is never
overwritten (pass supersedes to link a revision).
Writes no data/proof records and never implies PASS.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMAT = 'svatantrya-source-volume/1'


class VolumeError(Exception):
    pass


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def record_volume(work: str, vol: str, raw: bytes, spans: list[dict],
                  gaps: list[dict] | None = None, edition: str = "",
                  source_license: str = "", source_url: str = "",
                  supersedes: str | None = None) -> Path:
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', work or ''):
        raise VolumeError('work must be a lowercase slug')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', vol or ''):
        raise VolumeError('vol must be a safe volume id')
    if not edition.strip() or not source_license.strip():
        raise VolumeError('edition and source-license statements are required')
    try:
        raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise VolumeError('source must be UTF-8') from exc
    if not spans:
        raise VolumeError('spans must be a non-empty list')
    gaps = gaps or []
    seen = set()
    for i, s in enumerate(spans):
        label = f'span {i + 1}'
        if not isinstance(s, dict):
            raise VolumeError(f'{label} must be an object')
        pid, bs, be = s.get('passage_id'), s.get('start'), s.get('end')
        text = s.get('text')
        if (not isinstance(pid, str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_.-]*', pid)
                or pid in seen):
            raise VolumeError(f'{label} needs a unique passage_id')
        seen.add(pid)
        if (not isinstance(bs, int) or isinstance(bs, bool)
                or not isinstance(be, int) or isinstance(be, bool)
                or not (0 <= bs < be <= len(raw))):
            raise VolumeError(f'{label} offsets out of range')
        try:
            seg = raw[bs:be].decode('utf-8')
        except UnicodeDecodeError as exc:
            raise VolumeError(f'{label} offsets must end at UTF-8 boundaries') from exc
        if not isinstance(text, str) or seg != text:
            raise VolumeError(f'{label} bytes do not equal the bundle text')
    ordered = sorted(spans, key=lambda s: (s['start'], s['end']))
    overlaps, covered = [], []
    for s in ordered:
        for c in covered:
            lo, hi = max(s['start'], c[0]), min(s['end'], c[1])
            if lo < hi:
                overlaps.append({'a': c[2], 'b': s['passage_id'],
                                 'start': lo, 'end': hi, 'bytes': hi - lo})
        covered.append((s['start'], s['end'], s['passage_id']))
    covered.sort()
    union, cur = [], None
    for bs, be, _ in covered:
        if cur is None or bs > cur[1]:
            if cur is not None:
                union.append(cur)
            cur = [bs, be]
        else:
            cur[1] = max(cur[1], be)
    if cur is not None:
        union.append(cur)
    autgaps, prev = [], 0
    for bs, be in union:
        if raw[prev:bs].decode().strip():
            autgaps.append({'start': prev, 'end': bs,
                            'note': 'non-whitespace bytes in no chunk span',
                            'preview': raw[prev:bs].decode()[:80]})
        prev = be
    if raw[prev:].decode().strip():
        autgaps.append({'start': prev, 'end': len(raw),
                        'note': 'trailing non-whitespace in no chunk span',
                        'preview': raw[prev:].decode()[:80]})
    gaps = [*gaps, *autgaps]
    out_dir = ROOT / work / 'source' / 'volumes'
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f'{vol}.json'
    if path.exists() and supersedes is None:
        raise VolumeError(f'{vol} already recorded; pass supersedes to link a revision')
    manifest = {
        'format': FORMAT, 'work': work, 'vol': vol,
        'source_id': f'{work}-{vol}-{_sha(raw)[:16]}',
        'content_sha256': _sha(raw), 'bytes': len(raw),
        'edition': edition, 'license': source_license, 'source_url': source_url,
        'spans': [{'passage_id': s['passage_id'], 'start': s['start'],
                   'end': s['end'], 'vol_lines': s.get('vol_lines'),
                   'legacy_coords': s.get('legacy_coords'),
                   'text_sha256': _sha(s['text'].encode('utf-8'))} for s in spans],
        'overlaps': overlaps,
        'gaps': gaps, 'supersedes': supersedes,
    }
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + '\n')
    return path
