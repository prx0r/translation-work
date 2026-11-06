"""Per-chunk IPVV remaining-work measurement: source tokens vs convertible L0 rows."""
import json, sys, re, difflib, glob, pathlib
sys.path.insert(0, 'tools')
from workcfg import source_spans
sp = source_spans('ipvv')
lines = [json.loads(l) for l in open('ipvv/passages.jsonl')]
smap = json.load(open('ipvv/chunk-song-map.json'))

def rows_for(cid):
    p1 = f'/tmp/opencode/r2/v1/translations/_stack/ipvv/l0_v1/{cid}.l0.jsonl'
    p2 = f'/tmp/opencode/r2/full/translations/_stack/ipvv/l0/{cid}.l0.jsonl'
    for p in (p1, p2):
        if pathlib.Path(p).exists():
            return [json.loads(l) for l in open(p)]
    return None

def normtoks(toks):
    return [re.sub(r'\s+', ' ', t) for t in toks]

print(f"{'chunk':55s} {'src_tok':>7s} {'rows':>6s} {'covered':>7s} {'gap':>6s}  argmap")
# pilot argmap presence
pilots = set()
for f in glob.glob('ipvv/pilot/*_ARGUMENT_MAP.md'):
    n = pathlib.Path(f).stem.replace('_ARGUMENT_MAP', '')
    pilots.add(n)  # V1A, V2B, V3B_S7 ...
tot_src = tot_row = tot_cov = 0
for i, c in enumerate(lines, start=1):
    cid = c['chunk_id']
    src = sp[i]
    rows = rows_for(cid)
    nrow = len(rows) if rows else 0
    if rows:
        lem = [r.get('lemma_iast', '') for r in rows]
        sm = difflib.SequenceMatcher(None, src, lem, autojoin=False) if False else difflib.SequenceMatcher(None, src, lem, autojunk=False)
        cov = sum(i2 - i1 for t, i1, i2, *_ in sm.get_opcodes() if t == 'equal')
    else:
        cov = 0
    tot_src += len(src); tot_row += nrow; tot_cov += cov
    print(f"{cid:55s} {len(src):7d} {nrow:6d} {cov:7d} {len(src)-cov:6d}  {'Y' if True else ''}")
print(f"{'TOTAL':55s} {tot_src:7d} {tot_row:6d} {tot_cov:7d} {tot_src-tot_cov:6d}")
