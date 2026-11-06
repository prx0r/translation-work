#!/usr/bin/env python3
"""Convert one IPVV chunk to the shastra-minimal canonical stack (T1/L0/argmap/L2/C1 + proof).

Usage:
  python3 tools/shastra_convert_chunk.py --song <song> --verse <N> --v1 <rows.jsonl>
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from workcfg import source_spans, data_dir

IPVV = ROOT / 'ipvv'


def chunk_id_of(song):
    mp = json.loads((IPVV / 'chunk-song-map.json').read_text())
    return next(c for c, s in mp.items() if s == song)


def pilot_label(chunk_id):
    # chunkA -> V1A, chunkV2-A -> V2A, chunkV3-P -> V3P
    if chunk_id.startswith('chunkV'):
        parts = chunk_id.split('-')
        return 'V' + parts[0][-1] + parts[1].upper()
    return 'V1' + chunk_id[5].upper()  # chunkA -> V1A, chunkJ -> V1J


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print('CMD FAILED:', ' '.join(cmd))
        print(r.stdout[-500:])
        print(r.stderr[-500:])
        raise SystemExit(r.returncode)
    return r


def parse_pilot_argmap(path):
    text = path.read_text(encoding='utf-8')
    # question
    qm = re.search(r'\*\*The question:\*\*\s*(.*?)(?=\n\n|\n\*\*|\n##)', text, re.S)
    question = qm.group(1).strip() if qm else ''
    # premises: paragraphs in section 2
    sec2 = re.search(r'## 2\. (.*?)(?=\n## 3\.|\Z)', text, re.S)
    premises = []
    if sec2:
        for para in re.split(r'\n\n+', sec2.group(1)):
            para = para.strip()
            if not para or para.startswith('##') or para.startswith('**The question'):
                continue
            # drop bold lead labels like "**The spontaneity...:**"
            para = re.sub(r'^\*\*[^*]+\*\*:?\s*', '', para)
            if len(para.split()) >= 8:
                premises.append(para)
    # inference from section 4
    sec4 = re.search(r'## 4\. (.*?)(?=\n## |\Z)', text, re.S)
    inference = ''
    if sec4:
        paras = [p.strip() for p in re.split(r'\n\n+', sec4.group(1)) if p.strip()]
        # last substantial paragraph
        for p in reversed(paras):
            if len(p.split()) >= 8 and not p.startswith('##'):
                inference = p
                break
    # uncertainties from section 3
    sec3 = re.search(r'## 3\. (.*?)(?=\n## 4\.|\Z)', text, re.S)
    uncertainties = []
    if sec3:
        for line in sec3.group(1).splitlines():
            line = line.strip()
            m = re.match(r'\d+\.\s*(.*)', line)
            if m:
                uncertainties.append(m.group(1).strip())
    # speaker
    speaker = 'Abhinavagupta (commentator voice)'
    sm = re.search(r'speaker[:\s]+([^\n]+)', text, re.I)
    if sm:
        speaker = sm.group(1).strip()
    return question, premises, inference, uncertainties, speaker


def parse_pilot_l2(path):
    text = path.read_text(encoding='utf-8')
    # strip markdown headers and horizontal rules
    lines = []
    for line in text.splitlines():
        if line.startswith('#') or line.strip() == '---' or line.startswith('*2026'):
            continue
        lines.append(line)
    prose = '\n'.join(lines).strip()
    # collapse 3+ newlines
    prose = re.sub(r'\n{3,}', '\n\n', prose)
    return prose


def hinge_ids(l0):
    pat = re.compile(r'kart|kalpita|hetu|saṃbandh|apekṣ|nanu|siddh|virodh|prasaṅg|dūṣaṇ|bādh|abhāva|niścay|dviṣṭha|sāmānya|vyāpti|vyavahāra|vikalpa|jñātṛ|śabda|vyāpāra|kāraṇ|kārya|rāj|saṃgati|pratīti|ākāṅkṣ|aikya|maheśvar|prakāś|vimarś|pramey|māyā|śakti|buddh|sāṃkhya|vaiśeṣika|puruṣ|jñāna|kriyā|vāda|darś|ukt|pratipād|lakṣaṇ|ahaṃ|svātman|para|satya|bhav|syāt|yadi|katham|tat|evaṃ|tasm|yatas|iti|smṛti|vikalpa|apoha|antarābhāsa|naisargika|sarvajña|kṣetrajña|bhāva|pramāṇ|tattva|īśvara|pratyabhijñ|guru|śiṣy|saṃpradāya|colophon|samāpt|nigaman|upāya|yoga|yogin|mukti|jīvan|mārga|mukta|śiva|śakti|citta|dhātu|nyāy|hetu|vyāp|dhūm|pratijñ|pakṣa|dṛṣṭānt|anumāna|śabda|bhāva|abhāva|vastu|tattva|īśvara|pratyabhijñ|vimarś|maheśvar|guru|śiṣy|saṃpradāya|colophon|samāpt|nigaman')
    return [o['id'] for o in l0 if pat.search(o['surface'])]


def sha(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--song', required=True)
    ap.add_argument('--verse', type=int, required=True)
    ap.add_argument('--v1', required=True)
    ap.add_argument('--work', default='ipvv')
    ap.add_argument('--layers-only', action='store_true', help='skip T1/L0 build (data already filled by shastra_charfill+merge)')
    args = ap.parse_args()
    song = args.song
    verse = args.verse
    work = args.work
    w = ROOT / work
    sp = source_spans(work)[verse]
    src_sha = sha(' '.join(sp))
    # 1. T1+L0 (skipped with --layers-only: charfill+merge already ran)
    if not args.layers_only:
        run(['python3', 'tools/shastra_autogloss.py', '--song', song, '--verse', str(verse),
             '--v1', args.v1, '--work', work, '--mod', song.replace('-', '_') + '_Gauto'])
        modname = song.replace('-', '_') + '_Gauto'
        run(['python3', 'tools/shastra_merge.py', '--song', song, '--verse', str(verse),
             '--v1', args.v1, '--gtables', modname, '--work', work])
    # 2. argmap + L2 + C1
    chunk_id = chunk_id_of(song)
    label = pilot_label(chunk_id)
    am_path = IPVV / 'pilot' / f'pilot_{label}_ARGUMENT_MAP.md'
    l2_path = IPVV / 'pilot' / f'pilot_{label}_L2_read.md'
    question, premises, inference, uncertainties, speaker = parse_pilot_argmap(am_path)
    prose = parse_pilot_l2(l2_path)
    t1 = json.loads((data_dir(work, song) / f'{song}.t1.json').read_text())
    l0 = json.loads((data_dir(work, song) / f'{song}.l0.json').read_text())
    l0_ids = {o['id'] for o in l0}
    key_ids = hinge_ids(l0)
    # argmap
    am = [{
        'verse_id': f'{song}-v{verse}', 'song': song, 'verse': verse,
        'scope': 'passage', 'structured': True,
        'speaker': speaker or 'Abhinavagupta (commentator voice)',
        'question': question,
        'premises': premises if premises else [question],
        'inference': inference if inference else (premises[-1] if premises else question),
        'uncertainties': uncertainties,
        'option_choices': [],
        'traces': {'t1_verse': f'{song}-v{verse}', 'l0_ids': key_ids, 'sanskrit_sha': src_sha},
        'sanskrit_sha': src_sha,
    }]
    (data_dir(work, song) / f'{song}.argmap.json').write_text(json.dumps(am, indent=1, ensure_ascii=False))
    # L2
    cite = ' | '.join(sp[:12])
    l2 = [{
        'verse_id': f'{song}-v{verse}', 'song': song, 'verse': verse,
        'plain_english': prose,
        'sanskrit_cite': cite,
        'l0_ids': key_ids if key_ids else [l0[0]['id']],
        'supplied': [], 'fidelity': 'preserved',
    }]
    (data_dir(work, song) / f'{song}.l2.json').write_text(json.dumps(l2, indent=1, ensure_ascii=False))
    # C1 essence: from argmap question + inference, stripped of quotes
    essence = []
    for s in [question, inference] + (premises[:2] if premises else []):
        s = s.strip()
        if not s:
            continue
        # take first sentence
        first = re.split(r'(?<=[.!?])\s+', s)[0]
        first = first.replace('"', '').replace('“', '').replace('”', '')
        if first and first not in essence:
            essence.append(first)
    essence = essence[:5]
    if len(essence) < 3:
        essence += ['The chunk closes its own argument; see the argument map for the full chain.']
    c1 = {'song': song, 'essence': essence, 'essence_only': True, 'renders': {}}
    (data_dir(work, song) / f'{song}.c1.json').write_text(json.dumps(c1, indent=1, ensure_ascii=False))
    # 3. validate + proof
    run(['python3', 'tools/validate_song.py', '--song', song, '--work', work])
    run(['python3', 'tools/proof_record.py', '--song', song, '--work', work, '--shastra'])
    print(f'CONVERTED {song}: PASS')


if __name__ == '__main__':
    main()
