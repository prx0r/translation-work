#!/usr/bin/env python3
"""tools/passage_adapter.py — one boundary for verse IDs and prose chunk IDs.

Verse (existing): `<song>-v<number>` + workcfg registration → workcfg spans,
song JSON layers, byte-exact source text from spans.
Prose (IPVV): opaque chunk ID (e.g. `chunkA-svatyandya`) → published bundle +
volume source file, line-sequence match verified live, byte offsets computed
(not trusted from legacy coords). Layers resolve from `ipvv/data/<chunk>.*.json`
when present; absent layers → incomplete, never a verse proof reuse.

Returns normalized, hash-pinned artifacts; the auditor decides. No PASS here.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSEMATCH = re.compile(r'([a-z0-9][a-z0-9_-]*)-v(\d+)')
VOLFILE = {'M00020': 'ipvv-vol1.txt', 'M00021': 'ipvv-vol2.txt', 'M00022': 'ipvv-vol3.txt'}


class AdapterError(Exception):
    pass


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _vol_source(vol: str) -> tuple[Path, bytes]:
    name = VOLFILE.get(vol)
    if not name:
        raise AdapterError(f'unknown volume {vol!r}')
    p = ROOT.parent / 'ipvv' / 'site' / 'data' / 'sanskrit' / name
    try:
        raw = p.read_bytes()
        raw.decode('utf-8')
    except OSError as exc:
        raise AdapterError(f'volume source unavailable: {exc}') from exc
    except UnicodeDecodeError as exc:
        raise AdapterError('volume source is not UTF-8') from exc
    return p, raw


def _prose_spans(vol: str, bundle_text: str) -> tuple[int, int, int, int]:
    """Line-sequence exact match → (vol_line_start, vol_line_end, byte_start, byte_end).

    Tries trailing-newline variants; verifies raw[bs:be].decode == bundle text.
    Raises AdapterError on zero/multiple matches or byte mismatch.
    """
    _, raw = _vol_source(vol)
    vlines = raw.split(b'\n')
    blines = bundle_text.splitlines()
    if not blines:
        raise AdapterError('empty bundle text')
    first = blines[0]
    cands = [i for i, l in enumerate(vlines)
             if l.decode('utf-8', errors='ignore') == first]
    full = [c for c in cands
            if [x.decode('utf-8', errors='ignore') for x in vlines[c:c + len(blines)]] == blines]
    if not full:
        raise AdapterError('no exact line-sequence match in volume')
    if len(full) > 1:
        raise AdapterError(f'ambiguous match: {len(full)} candidates')
    a = full[0]
    off = [0]
    for ln in vlines:
        off.append(off[-1] + len(ln) + 1)
    for be in (off[a + len(blines)], off[a + len(blines)] - 1):
        if raw[off[a]:be].decode('utf-8') == bundle_text:
            return a + 1, a + len(blines), off[a], be
    raise AdapterError('line match found but byte round-trip failed')


def resolve(work: str, passage_id: str) -> dict:
    """Normalize one passage ID to hash-pinned artifacts for the auditor."""
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,79}', work):
        raise AdapterError('invalid work')
    m = VERSEMATCH.fullmatch(passage_id)
    if m and work != 'ipvv':
        import workcfg
        song, verse = m.group(1), int(m.group(2))
        if work not in workcfg.WORKS or song not in workcfg.WORKS[work].get('songs', {}):
            raise AdapterError('work or song is not registered with canonical workcfg')
        verses = workcfg.song_verses(work, song)
        spans = workcfg.source_spans(work)
        if not spans or verse not in verses or not set(verses).issubset(spans):
            raise AdapterError('source spans unavailable or incomplete')
        source_path = Path(workcfg.WORKS[work]['source'])
        return {'kind': 'verse', 'work': work, 'passage_id': passage_id,
                'song': song, 'verses': verses, 'verse': verse,
                'source_path': str(source_path), 'source_spans': spans,
                'source_evidence_state': 'WORKCFG_SPANS'}
    if work == 'ipvv':
        # Canonical passage_id drops the bundle `.md` suffix (IPVV-IMPORT);
        # on-disk files also replace `.` with `-` and append `-md.json`.
        # Accept either form.
        pid = passage_id[:-3] if passage_id.endswith('.md') else passage_id
        bundle_path = None
        tried = []
        for stem in (pid, pid.replace('.', '-')):
            for cand in (ROOT / 'ipvv' / 'published' / f'pt-passage-ipvv-{stem}.json',
                         ROOT / 'ipvv' / 'published' / f'pt-passage-ipvv-{stem}-md.json'):
                tried.append(cand.name)
                if cand.is_file():
                    bundle_path = cand
                    break
            if bundle_path is not None:
                break
        if bundle_path is None:
            raise AdapterError(f'unknown ipvv chunk {passage_id!r}')
        try:
            bundle = json.loads(bundle_path.read_bytes())
        except (OSError, ValueError) as exc:
            raise AdapterError(f'chunk bundle unreadable: {exc}') from exc
        src = bundle.get('source', {})
        vol = bundle.get('vol')
        if not isinstance(src.get('text'), str) or not vol:
            raise AdapterError('chunk bundle lacks source text/volume')
        _, raw = _vol_source(vol)
        vstart, vend, bs, be = _prose_spans(vol, src['text'])
        data = ROOT / 'ipvv' / 'data'
        layers = {}
        for name in ('t1', 'l0', 'argmap', 'l2', 'c1', 'l3', 'l4', 'c2'):
            p = data / f'{passage_id}.{name}.json'
            if p.is_file():
                raw_l = p.read_bytes()
                layers[name] = {'file_sha256': _digest(raw_l),
                                'canonical_json_sha256': _digest(
                                    json.dumps(json.loads(raw_l), sort_keys=True,
                                               separators=(',', ':'),
                                               ensure_ascii=False).encode('utf-8'))}
        return {'kind': 'prose', 'work': 'ipvv', 'passage_id': passage_id,
                'song': passage_id, 'vol': vol,
                'source_versions': [{'file': f'ipvv/site/data/sanskrit/{VOLFILE[vol]}',
                                     'sha256': _digest(raw), 'bytes': len(raw)}],
                'spans': [{'unit': 'utf8-byte', 'start': bs, 'end': be,
                           'vol_lines': [vstart, vend],
                           'legacy_coords': [src.get('start'), src.get('end')],
                           'text_sha256': _digest(src['text'].encode('utf-8'))}],
                'layer_objects': layers,
                'source_evidence_state': 'CANDIDATE_LINE_MATCH',
                'note': 'Legacy coords untrusted; bytes verified live. Absent layers = incomplete.'}
    raise AdapterError(f'cannot resolve {work}:{passage_id}')
