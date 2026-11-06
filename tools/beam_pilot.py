#!/usr/bin/env python3
"""beam_pilot — draft missing pilot prose (argmap + L2 read) with beam-free.

Beam drafts PROSE ONLY (never canonical JSON). Deterministic
shastra_convert_chunk.py assembles data/*.argmap/l2/c1.json; the assessor
(me) validates + proofs. Drafts land in ipvv/cm/beam/<LBL>/ for review.

Usage: python3 tools/beam_pilot.py --label V3B [--max-tokens 6000]
Needs $OPENCODE_GO_KEY.
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from workcfg import source_spans, data_dir, chunk_id_for  # noqa: E402
from beam_client import beam  # noqa: E402

SYS = ('You are drafting a philosophical argument map for the '
       'Isvarapratyabhijnavivrtivimarsini (Abhinavagupta, Trika Shaivism). '
       'Output ONLY the two requested markdown files, no commentary. '
       'Machine-proposed drafts; a scholar reviews. Never invent citations; '
       'mark genuine uncertainties in the uncertainties section.')

def hinge_glosses(song: str, cap: int = 400) -> str:
    pat = re.compile(r'kart|kalpita|hetu|saṃbandh|apekṣ|nanu|siddh|virodh|prasaṅg|bādh|abhāva|niścay|sāmānya|vyāpti|vyavahāra|vikalpa|jñātṛ|pratīti|ākāṅkṣ|maheśvar|prakāś|vimarś|pramey|māyā|śakti|jñāna|kriyā|darś|pratipād|lakṣaṇ|ahaṃ|svātman|satya|tattva|īśvara|pratyabhijñ|guru|śiṣy|upāya|mukti|śiva|citta|hetu|pakṣa|dṛṣṭānt|anumāna|vastu')
    l0 = json.loads((data_dir('ipvv', song) / f'{song}.l0.json').read_text())
    rows = []
    for o in l0:
        if pat.search(o['surface']):
            g = (o.get('options') or [{}])[0].get('gloss', '')
            rows.append(f"{o['surface']} = {g}")
        if len(rows) >= cap:
            break
    return '\n'.join(rows)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--label', required=True, help='pilot label e.g. V3B')
    ap.add_argument('--max-tokens', type=int, default=6000)
    a = ap.parse_args()
    # label -> (chunk_id, song, verse)
    table = json.load(open(ROOT / 'ipvv' / 'chunk-table.json'))
    mp = json.load(open(ROOT / 'ipvv' / 'chunk-song-map.json'))
    found = None
    for cid, song in mp.items():
        if cid.startswith('chunkV'):
            parts = cid.split('-')
            lbl = 'V' + parts[0][-1] + parts[1].upper()
        else:
            lbl = 'V1' + cid[5].upper()
        if lbl == a.label:
            found = (cid, song)
            break
    if not found:
        print(f'unknown label {a.label}')
        return 2
    cid, song = found
    verse = next(e['verse'] for e in table if e['song'] == song)
    t1md = (ROOT / 'ipvv' / cid / 'T1.md').read_text()
    src = ' '.join(source_spans('ipvv')[verse])
    # style model: V1J (proof PASS) pilot pair
    style_am = (ROOT / 'ipvv' / 'pilot' / 'pilot_V1J_ARGUMENT_MAP.md').read_text()[:6000]
    style_l2 = (ROOT / 'ipvv' / 'pilot' / 'pilot_V1J_L2_read.md').read_text()[:3000]
    lore_p = ROOT / 'process' / 'beam' / 'lore' / f'ipvv-{a.label}.md'
    lore_txt = lore_p.read_text()[:8000] if lore_p.exists() else ''
    user = f"""CHUNK {cid} ({song}), pilot label {a.label}. Source slice (first 4000 chars):
{src[:4000]}
{f'''
TRANSMISSION BRIEF (scholarly orientation — follow it):
{lore_txt}
''' if lore_txt else ''}
T1 PROSE TRANSLATION (the draft to map):
{t1md[:60000]}

KEY TERM GLOSSES (surface = gloss):
{hinge_glosses(song)}

STYLE MODEL (proof-PASS chunk V1J — copy its SHAPE, not content):
---ARGMAP---
{style_am}
---L2---
{style_l2}

Write TWO files.

FILE 1 (argument map), exact shape:
**The question:** <one sentence: what this passage argues>
## 2. <title>
<3-8 paragraphs, each >=8 words: speaker, then premises in order. Terse logical statements. No certainty labels.>
## 3. <title>
<numbered uncertainties, or '1. None recorded.'>
## 4. <title>
<2-4 paragraphs ending in the inference: what is established>

FILE 2 (L2 read): readable plain-English paragraphs of the passage, no headers needed.

Separate the files with a line containing exactly: ===FILE2===
Terse, philosophical, grounded ONLY in the materials above."""
    text = beam(SYS, user, session=f'ipvv-pilot-{a.label.lower()}-001', max_tokens=a.max_tokens)
    outd = ROOT / 'ipvv' / 'cm' / 'beam' / a.label
    outd.mkdir(parents=True, exist_ok=True)
    if '===FILE2===' in text:
        am, l2 = text.split('===FILE2===', 1)
    else:  # beam ignored separator: file everything as argmap, flag for assessor
        am, l2 = text, ''
    (outd / f'pilot_{a.label}_ARGUMENT_MAP.md').write_text(am.strip() + '\n')
    (outd / f'pilot_{a.label}_L2_read.md').write_text(l2.strip() + '\n')
    # self-check
    checks = {'has_question': '**The question:**' in am,
              'has_sec2': bool(re.search(r'## 2\.', am)),
              'has_sec4': bool(re.search(r'## 4\.', am)),
              'premises_ge2': len([p for p in re.split(r'\n\n+', am) if len(p.split()) >= 8]) >= 2,
              'l2_nonempty': len(l2.strip()) > 200}
    (outd / 'selfcheck.json').write_text(json.dumps(checks, indent=1))
    print(json.dumps({'label': a.label, 'checks': checks}, indent=1))
    return 0 if all(checks.values()) else 1

if __name__ == '__main__':
    raise SystemExit(main())
