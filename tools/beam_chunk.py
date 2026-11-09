#!/usr/bin/env python3
"""Chunked beam drafting for monster verses (>400 tokens) that blow the
single-call output ceiling (beam returns 1-2 rows instead of N).

Splits a verse's tokens into contiguous chunks, runs the standard per-verse
gloss/CM packet per chunk, validates byte-exact surfaces per chunk, and
merges into the canonical runs/{song}-{kind}-v{verse}/ files. Meaning is
unchanged; only the output budget is sharded. Assessor reviews merged output.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from beam_client import beam
from beam_swarm import TAL_GLOSS_SYS, TAL_CM_SYS, TalGloss, TalCm  # noqa

RUNS = ROOT / 'process' / 'beam' / 'runs'
CHUNK = 120  # tokens per call — well under the truncation ceiling


def draft_gloss(work, song, verse, tokens, lore):
    surfs = [t['surface'] for t in tokens]
    rows = []
    for i in range(0, len(surfs), CHUNK):
        part = surfs[i:i + CHUNK]
        got = None
        for attempt in range(2):
            user = (f'Verse {verse} part {i // CHUNK + 1} ({len(part)} tokens, hyphen-split compounds):\n'
                    + '\n'.join(f'{j}: {s}' for j, s in enumerate(part))
                    + '\n\nGLOSS MEANING ONLY — never grammatical labels (no case/number/part-of-speech words).\n'
                    + (f'TRANSMISSION BRIEF:\n{lore[:2000]}\n\n' if lore else '')
                    + f'You MUST output EXACTLY {len(part)} rows, one per token above, in the same order. '
                      f'Reply ONLY JSON: {{"song": "...", "verse": N, "rows": [{{"surface": "...(exact)", "gloss": "...", "grounds": "..."}}]}}')
            text = beam(TAL_GLOSS_SYS, user, session=f'chunk-gloss-{song}-v{verse}-{i}-{attempt}', max_tokens=64000)
            a, b = text.find('{'), text.rfind('}')
            if a < 0:
                continue
            try:
                g = TalGloss.model_validate_json(text[a:b + 1])
            except Exception:
                continue
            rs = [r.surface for r in g.rows]
            if rs == part:
                got = g
                break
        if got is None:
            return None, f'surface drift chunk {i} after 2 tries'
        rows += [{'surface': r.surface, 'gloss': r.gloss, 'grounds': r.grounds} for r in got.rows]
    return {'song': song, 'verse': verse, 'rows': rows}, None


def draft_cm(work, song, verse, gloss_rows):
    rows = []
    for i in range(0, len(gloss_rows), CHUNK):
        part = gloss_rows[i:i + CHUNK]
        got = None
        for attempt in range(2):
            user = ('Verse tokens (surface = gloss):\n'
                    + '\n'.join(f"{r['surface']} = {r['gloss']}" for r in part)
                    + f'\n\nOne CM row per token IN ORDER: [lemma_iast, morph, grounds]. '
                      f'You MUST output EXACTLY {len(part)} rows, one per token above, in the same order. '
                      f'Grounds cite the gloss + form. Never invent; mark uncertainty in grounds. '
                      f'Reply ONLY JSON: {{"song": "...", "verse": N, "rows": [{{"lemma": "...", "morph": "...", "grounds": "..."}}]}}')
            text = beam(TAL_CM_SYS, user, session=f'chunk-cm-{song}-v{verse}-{i}-{attempt}', max_tokens=64000)
            a, b = text.find('{'), text.rfind('}')
            if a < 0:
                continue
            try:
                c = TalCm.model_validate_json(text[a:b + 1])
            except Exception:
                continue
            if len(c.rows) == len(part):
                got = c
                break
        if got is None:
            return None, f'row count chunk {i}: giving up after 2 tries'
        rows += [{'lemma': r.lemma, 'morph': r.morph, 'grounds': r.grounds or ''} for r in got.rows]
    return {'song': song, 'verse': verse, 'rows': rows}, None


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--song', required=True)
    ap.add_argument('--verse', type=int, required=True)
    ap.add_argument('--layer', choices=['gloss', 'cm'], required=True)
    a = ap.parse_args()
    wt = json.loads((ROOT / a.work / f'working-t1-{a.song}.json').read_text())
    e = next(x for x in wt if x['verse'] == a.verse)
    lp = ROOT / 'process' / 'beam' / 'lore' / f'{a.work}.md'
    lore = lp.read_text()[:4000] if lp.exists() else ''
    if a.layer == 'gloss':
        d, err = draft_gloss(a.work, a.song, a.verse, e['tokens'], lore)
        fn = 'gloss.json'
    else:
        gf = RUNS / f'{a.song}-gloss-v{a.verse:02d}' / 'gloss.json'
        if not gf.exists():
            print(f'need gloss first for {a.song} v{a.verse}'); return 2
        g = json.loads(gf.read_text())
        d, err = draft_cm(a.work, a.song, a.verse, g['rows'])
        fn = 'cm.json'
    if err:
        print(f'FAIL: {err}'); return 1
    outd = RUNS / f'{a.song}-{a.layer}-v{a.verse:02d}'
    outd.mkdir(parents=True, exist_ok=True)
    (outd / fn).write_text(json.dumps(d, indent=1, ensure_ascii=False))
    print(f'done {a.song} v{a.verse} {a.layer}: {len(d["rows"])} rows')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
