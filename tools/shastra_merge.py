#!/usr/bin/env python3
"""tools/shastra_merge.py — merge hand-gloss tables into shastra chunk T1+L0 data.

Usage:
  python3 tools/shastra_merge.py --song <song> --verse <N> --v1 <rows.jsonl> --gtables <mod1,mod2..> [--cm-dir ipvv/cm]

Each G table module must define G = [(src_idx, gloss, grounds)] and optionally
<MOD>_STATUS = {src_idx: status}. New tokens are inserted in source order; L0 ids
rebuilt as {verse_id}-p{NNN}; STATUS_OVR sidecar (cm/<song>-status.json) persists
AMBIGUOUS flags across re-runs; covered idx tracked in cm/<song>-covered.json.

Coverage rule (FINAL-PROCESS): T1 must face every source pada. Paratext
(daṇḍas, page/verse numbers, editorial marks) is excluded with note, per
parapravesika precedent — never glossed, never faked.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys, difflib, pathlib
from importlib import import_module

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from workcfg import source_spans, data_dir


def is_paratext(t: str) -> bool:
    """Editorial apparatus is never glossed (contract: paratext never enters T1/L0).
    NOTE (2026-11-08, tal-a10 v207/v211/v224/v272): brackets *inside* a Sanskrit
    token mark supplied aksaras (śiva(śakti)rūpaiva), NOT apparatus — the fused
    reading is genuine text and IS glossed. Only tokens that *are* apparatus
    (fullmatch patterns below) filter out; mid-token brackets never filter."""
    if '|' in t:
        return True  # ASCII pipe never in Sanskrit: editorial refs (3|249), daṇda splits
    if re.search(r'\([^)]*[?]', t):
        return True  # editorial uncertainty: bādhe.....(?)
    return bool(
        t in ('|', '||', '|]', '/', '//', '(page', '(saṃṣi.', 'END', 'OF', 'FILE')
        or re.fullmatch(r'#+', t)
        or re.fullmatch(r'\([a-zā-īūṛḷṃḥṅñṭḍṇśṣ]+\.', t)
        or re.fullmatch(r'\(page \d+\)', t)
        or re.fullmatch(r'\(\d+\)?', t)
        or re.fullmatch(r'\(\d+\|\d+\|\d+\)', t)
        or re.fullmatch(r'\([^)]{1,24}\)', t)
        or re.fullmatch(r'[a-zā-īūṛḷṃḥṅñṭḍṇśṣ]{1,4}\.', t)
        or re.fullmatch(r'\d+\)?', t)
        or re.fullmatch(r'\d+-\d+', t)
        or re.fullmatch(r'\[AgMsv_\d+\.\d+\]', t)
    )



def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--song", required=True)
    ap.add_argument("--verse", type=int, required=True)
    ap.add_argument("--v1", required=True, help="draft L0 rows jsonl (v1/full tarball)")
    ap.add_argument("--gtables", required=True, help="comma-separated G table modules (importable)")
    ap.add_argument("--cm-dir", default="ipvv/cm")
    ap.add_argument("--work", default="ipvv")
    args = ap.parse_args()
    sys.path.insert(0, args.cm_dir)
    song, verse = args.song, args.verse
    vid = f"{song}-v{verse}"
    sp = source_spans(args.work)
    src = sp[verse]
    rows = [json.loads(l) for l in open(args.v1)]
    lem = [r.get('lemma_iast', '') for r in rows]
    sm = difflib.SequenceMatcher(None, src, lem, autojunk=False)
    G: dict = {}
    STATUS: dict = {}
    GROUNDS: dict = {}
    for mod in args.gtables.split(','):
        m = import_module(mod.strip())
        for name in dir(m):  # any G/G1..Gn/Gchar/Gauto table the module exposes
            if name in ('G', 'Gchar', 'Gauto', 'Ghand') or re.fullmatch(r'G\d+', name):
                val = getattr(m, name)
                if isinstance(val, list):
                    for e in val:
                        G[e[0]] = (e[1], e[2] if len(e) > 2 else '')
            if name == 'STATUS' or re.fullmatch(r'(G\d*_STATUS|G_STATUS)', name):
                val = getattr(m, name)
                if isinstance(val, dict):
                    STATUS.update(val)
        GROUNDS.update(getattr(m, 'GROUNDS', {}))
        import re as _re
        for name in dir(m):
            if _re.fullmatch(r'(G\d*_GROUNDS_\d+|GROUNDS_\d+)', name):
                GROUNDS[int(name.rsplit('_', 1)[1])] = getattr(m, name)
    # scaffold: sequential matches (v1 order, source order)
    scaf = []
    for tag, a1, a2, b1, b2 in sm.get_opcodes():
        if tag == 'equal':
            scaf += list(zip(range(a1, a2), [rows[b] for b in range(b1, b2)]))
    data_p = data_dir(args.work, song) / f"{song}.t1.json"
    cov_p = ROOT / args.cm_dir / f"{song}-covered.json"
    st_p = ROOT / args.cm_dir / f"{song}-status.json"
    if data_p.exists():
        t1 = json.loads(data_p.read_text())
        l0old = json.loads((data_dir(args.work, song) / f"{song}.l0.json").read_text())
        # data is the artifact: re-derive covered idx by ordered surface match
        # (tolerates stale sidecars, e.g. after a paratext cleanup)
        covered = set()
        _si = 0
        for _t in t1[0]['tokens']:
            _si = src.index(_t['surface'], _si) if _t['surface'] in src[_si:] else -1
            assert _si >= 0, f"surface not found in order: {_t['surface'][:40]}"
            covered.add(_si)
            _si += 1
        sc_by_idx = {}
        # rebuild scaffold map: current data order == source order of covered idx
        cov_sorted = sorted(covered)
        assert len(cov_sorted) == len(t1[0]['tokens']) == len(l0old), \
            (len(cov_sorted), len(t1[0]['tokens']), len(l0old))
        sc_by_idx = dict(zip(cov_sorted, zip(t1[0]['tokens'], l0old)))
    else:
        t1 = [{'verse_id': vid, 'song': song, 'verse': verse,
               'quick_english': 'SCAFFOLD pending (T1 prose doc holds the full draft).',
               'tokens': [], 'source_sha': hashlib.sha256(' '.join(src).encode()).hexdigest()[:16],
               'history': []}]
        sc_by_idx = dict(zip([a for a, _ in scaf],
                             [({'surface': src[a], 'quick_gloss': r['literal_gloss']},
                               {'verse_id': vid, 'pada_index': 0, 'surface': src[a],
                                'citation': f"draft rows ({r.get('id', '?')})",
                                'morph': 'pending verification',
                                'options': [{'gloss': r['literal_gloss'], 'rank': 1,
                                             'source': 't1-draft',
                                             'grounds': 'draft-row extraction; hand-written gloss in frozen T1 doc, verification pending'}],
                                'chosen_index': 0, 'status': r.get('status', 'PARSED'),
                                'fork': 'none'}) for a, r in scaf]))
    # validate scaffold glosses
    for i, (t, o) in sc_by_idx.items():
        assert t['surface'] and t['quick_gloss'], (i, t)
        if is_paratext(t['surface']):
            continue  # dropped in the merge loop below; never glossed
        assert '(' not in t['surface'] and ')' not in t['surface'], (i, t)
    new_toks, new_l0, new_src_idx, skipped, still = [], [], [], [], []
    k = 0
    for i, tok in enumerate(src):
        if is_paratext(tok):
            skipped.append((i, tok))
            continue
        if i in sc_by_idx:
            t, o = sc_by_idx[i]
            new_toks.append(t)
            o['id'] = f'{vid}-p{k:03d}'; o['pada_index'] = k; o['verse_id'] = vid
            new_l0.append(o); new_src_idx.append(i); k += 1
        elif i in G:
            gl, gr = G[i]
            assert gl and '(' not in gl and ')' not in gl, (i, tok)
            new_toks.append({'surface': tok, 'quick_gloss': gl})
            new_l0.append({'id': f'{vid}-p{k:03d}', 'verse_id': vid, 'pada_index': k,
                           'surface': tok, 'citation': f'hand-gloss (source token {i})',
                           'morph': 'pending verification',
                           'options': [{'gloss': gl, 'rank': 1, 'source': 't1-draft',
                                        'grounds': GROUNDS.get(i, gr)}],
                           'chosen_index': 0, 'status': STATUS.get(i, 'PARSED'),
                           'fork': 'none'})
            new_src_idx.append(i); k += 1
        elif is_paratext(tok):
            skipped.append((i, tok))
        else:
            still.append((i, tok))
    # persist statuses
    st = {}
    if st_p.exists():
        st = json.loads(st_p.read_text())
    st.update({str(k_): v for k_, v in STATUS.items()})
    for _tok, _si, _o in zip(new_toks, new_src_idx, new_l0):
        if str(_si) in st:
            _o['status'] = st[str(_si)]
    st_p.write_text(json.dumps(st, indent=1, sort_keys=True))
    t1[0]['tokens'] = new_toks
    t1[0]['history'].append({'gloss': f"merge: +{len(G)} hand glosses; paratext excluded ({len(skipped)}); still open ({len(still)})",
                            'reason': 'shastra authoring, machine-proposed', 'date': '2026-11-06'})
    dd = data_dir(args.work, song)
    (dd / f"{song}.t1.json").write_text(json.dumps(t1, indent=1, ensure_ascii=False))
    (dd / f"{song}.l0.json").write_text(json.dumps(new_l0, indent=1, ensure_ascii=False))
    (ROOT / args.cm_dir / f"{song}-covered.json").write_text(json.dumps(sorted(set(new_src_idx))))
    print(f'merged toks: {len(new_toks)} | paratext skipped: {len(skipped)} | still gap: {len(still)}')
    if still:
        print('first still-gap:', still[:8])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
