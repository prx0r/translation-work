"""Gap analysis for any shastra chunk (generic): scaffold coverage + gap token list."""
import json, sys, re, difflib
sys.path.insert(0, 'tools')
from workcfg import source_spans
song = sys.argv[1]; verse = int(sys.argv[2]); v1path = sys.argv[3]
sp = source_spans('ipvv')
src = sp[verse]
rows = [json.loads(l) for l in open(v1path)]
lem = [r.get('lemma_iast', '') for r in rows]
sm = difflib.SequenceMatcher(None, src, lem, autojunk=False)
cov = set()
for tag, a1, a2, b1, b2 in sm.get_opcodes():
    if tag == 'equal':
        cov.update(range(a1, a2))
def is_para(t):
    return (t in ('|', '||', '(page', '(saṃṣi.') or re.fullmatch(r'\(page \d+\)', t)
            or re.fullmatch(r'\(\d+\)?', t) or re.fullmatch(r'\d+\)?', t))
gaps = [i for i in range(len(src)) if i not in cov and not is_para(src[i])]
para = [i for i in range(len(src)) if i not in cov and is_para(src[i])]
print(f'{song}: src={len(src)} v1rows={len(rows)} covered={len(cov)} gaps={len(gaps)} paratext={len(para)}')
doc_cands = {}
for i in gaps:
    t = src[i]
    doc_cands[t] = doc_cands.get(t, 0) + 1
json.dump({'song': song, 'verse': verse, 'src_tokens': len(src), 'covered': len(cov),
           'gaps': gaps, 'paratext': para},
          open(f'/tmp/opencode/{song}-gap.json', 'w'))
print('first gaps:', [(i, src[i]) for i in gaps[:15]])
