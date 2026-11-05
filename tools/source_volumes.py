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


def record_work_volume(work: str, edition: str = "", source_license: str = "",
                       source_url: str = "") -> Path:
    """Record one source-volume manifest for a workcfg verse work.

    Verse blocks come from the work's own kind parser (the same code that
    feeds workcfg.source_spans), so block lines match translation coverage by
    construction. passage_ids come from data/<song>.t1.json rows on disk.
    Blocks may share boundary lines (recorded in overlaps); inter-block
    non-whitespace becomes gaps. No data/proof writes, never PASS.
    """
    import sys
    sys.path.insert(0, str(ROOT / 'tools'))
    import workcfg
    try:
        import proof_record
    except ImportError:  # pragma: no cover
        proof_record = None
    cfg = workcfg.work_config(work)
    if cfg is None:
        raise VolumeError(f'unknown work {work}')
    if cfg.get('kind') == 'segments':
        raise VolumeError(f'{work} already has an intake source manifest')
    src = Path(cfg['source'])
    try:
        raw = src.read_bytes()
        raw.decode('utf-8')
    except OSError as exc:
        raise VolumeError(f'source unavailable: {exc}') from exc
    except UnicodeDecodeError as exc:
        raise VolumeError('source must be UTF-8') from exc
    kind = cfg.get('kind')
    blocks: dict[tuple[str, int], tuple[int, int]] = {}
    if kind == 'utsst':
        if proof_record is None:
            raise VolumeError('proof_record unavailable for utsst blocks')
        songs = sorted(p.stem.split('.')[0]
                       for p in (ROOT / work / 'data').glob('*.t1.json'))
        for song in songs:
            for v, (_, lr) in proof_record.load_gretil_spans(
                    src, int(song[1:])).items():
                blocks[(song, v)] = (lr[0], lr[1])
    else:
        from pathlib import Path as _P  # noqa, local clarity
        parsers = {
            'utajp': (workcfg.parse_utajp, False),
            'sambandha': (workcfg.parse_sambandha, True),
            'isvara': (workcfg.parse_isvara, True),
            'parapravesika': (workcfg.parse_parapravesika, True),
            'bodhapanca': (workcfg.parse_bodhapanca, True),
            'phrdaya': (workcfg.parse_phrdaya, True),
            'krama': (workcfg.parse_krama, True),
            'bodhavilasa': (workcfg.parse_bodhavilasa, True),
            'bhairavanukarana': (workcfg.parse_bhairavanukarana, True),
            'paryanta': (workcfg.parse_paryanta, True),
            'paramartha': (workcfg.parse_paramartha, True),
            'ghata': (workcfg.parse_ghata, True),
            'spanda': (workcfg.parse_spanda, True),
            't1md': (workcfg.parse_t1md, True),
        }
        if kind == 'abhts':
            units, _ = workcfg.parse_abhts(src)
            ahnika = cfg.get('ahnika', 1)
            parsed = {num: val for (a, num), val in units.items()
                      if a == ahnika}
        elif kind in parsers:
            fn, paired = parsers[kind]
            parsed = fn(src)
            if paired:
                parsed, _ = parsed
        else:
            raise VolumeError(f'no block parser for kind {kind!r}')
        songs = (sorted(cfg.get('songs', {}).keys())
                 or sorted({s for s, _ in _song_keys(work)}))
        for song in songs:
            for v in workcfg.song_verses(work, song):
                if v in parsed:
                    _, lr = parsed[v]
                    blocks[(song, v)] = (lr[0], lr[1])
    lines = raw.split(b'\n')
    off = [0]
    for ln in lines:
        off.append(off[-1] + len(ln) + 1)
    vid: dict[tuple[str, int], str] = {}
    for t1f in sorted((ROOT / work / 'data').glob('*.t1.json')):
        try:
            rows = json.loads(t1f.read_bytes())
        except ValueError:
            continue
        for r in rows:
            if isinstance(r, dict) and r.get('verse_id') and isinstance(
                    r.get('verse'), int):
                vid[(r.get('song', t1f.stem.split('.')[0]), r['verse'])] = \
                    r['verse_id']
    spans = []
    for (song, v), (a, b) in sorted(blocks.items()):
        if a < 1 or b > len(lines) or a > b:
            raise VolumeError(f'block out of range: {song} v{v}')
        bs, be = off[a - 1], off[b]
        text = raw[bs:be].decode('utf-8')
        if not text.strip():
            raise VolumeError(f'empty block: {song} v{v}')
        pid = vid.get((song, v), f'{song}-v{v:02d}')
        spans.append({'passage_id': pid, 'start': bs, 'end': be,
                      'vol_lines': [a, b], 'legacy_coords': None,
                      'text': text})
    if not spans:
        raise VolumeError(f'no verse blocks resolved for {work}')
    stem = src.stem
    vol = stem if src.parent != ROOT / work else f'{work}-{stem}'
    try:
        source_ref = src.relative_to(ROOT).as_posix()
    except ValueError:
        source_ref = '../' + src.relative_to(ROOT.parent).as_posix()
    note = [l for l in raw.decode('utf-8').splitlines()[:3]
            if l.startswith('###')]
    return record_volume(work, vol, raw, spans, [],
                         edition=edition or ' '.join(note) or
                         f'{src.name} as vendored (see file header)',
                         source_license=source_license or
                         'see lore/links.json; rights UNKNOWN until confirmed',
                         source_url=source_url, source_path=source_ref)


def _song_keys(work: str) -> list[tuple[str, int]]:
    return []


def record_volume(work: str, vol: str, raw: bytes, spans: list[dict],
                  gaps: list[dict] | None = None, edition: str = "",
                  source_license: str = "", source_url: str = "",
                  supersedes: str | None = None,
                  source_path: str = "") -> Path:
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
    try:
        source_ref = source_path or ""
    except Exception:
        source_ref = ""
    manifest = {
        'format': FORMAT, 'work': work, 'vol': vol,
        'source_file': source_ref,
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
