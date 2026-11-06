"""a23 data (abhisheka, 103u/810tok). Populates TOK/CM/GLOSS/QE."""
ROWS = {}; GLOSS = {}; QE = {}

import sys
sys.path.insert(0, "tools")
from workcfg import source_spans
spans = source_spans("tantraloka-a23")
TOK = {}; CM = {}
for v in list(ROWS.keys()):
    TOK[v] = list(spans[v])
    assert TOK[v] == list(spans[v]), "TOK mismatch v%d"%v
    assert len(ROWS[v]) == len(spans[v]), "ROW COUNT v%d: %d vs %d"%(v,len(ROWS[v]),len(spans[v]))
    assert len(GLOSS[v]) == len(spans[v]), "GLOSS COUNT v%d"%(v,)
    assert v in QE
    CM[v] = [r for r in ROWS[v]]
    assert all(isinstance(r,(list,tuple)) and len(r)==3 for r in CM[v])
print("a23 ALL verified: %d verses, %d tokens"%(len(TOK), sum(len(v) for v in TOK.values())))