#!/usr/bin/env python3
"""Assessor hand-draft tal-a05 vv81-84 (gloss+cm+am). Part 3 of 3. See part 1 header."""
from __future__ import annotations
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "process" / "beam" / "runs"
SONG = "tal-a05"

V: dict[int, dict] = {
81: {
 "g": [
  ("tataḥ", "then", "indecl; sequence"),
  ("svātantryanirmeye", "in-freedom-unmeasured", "loc.sg.n compound svātantrya-nirmaya"),
  ("vicitrārthakriyākṛti", "wondrous-purpose-act-form", "nom.sg.f compound; subject"),
  ("vimarśanaṃ", "reflecting", "acc.sg.n; object"),
  ("viśeṣākhyaḥ", "called-distinct", "nom.sg.m compound; epithet of spanda"),
  ("spanda", "throb", "nom.sg.m; subject"),
  ("aunmukhyasaṃjñitaḥ", "named-eagerness", "nom.sg.m compound; epithet"),
 ],
 "m": [
  ("tataḥ", "indecl.", "sequence"),
  ("svātantryanirmeye", "loc.sg.n", "in unmeasured freedom"),
  ("vicitrārthakriyākṛti", "nom.sg.f", "wondrous-formed act"),
  ("vimarśanaṃ", "acc.sg.n", "reflecting as object"),
  ("viśeṣākhyaḥ", "nom.sg.m", "called distinct"),
  ("spanda", "nom.sg.m", "subject throb"),
  ("aunmukhyasaṃjñitaḥ", "nom.sg.m", "named eagerness"),
 ],
 "a": {
  "question": "What is the distinct throb named eagerness?",
  "premises": [
   "Then in unmeasured freedom the wondrous act takes form",
   "Reflecting, the distinct-named throb stirs",
   "Eagerness names its forward lean"],
  "inference": "In freedom, reflecting throb leans forward as eagerness.",
  "uncertainties": [],
  "plain_english": "Then in unmeasured freedom, the wondrous-purpose-act-form reflecting, the distinct throb named eagerness stirs.",
 },
},
82: {
 "g": [
  ("tatra", "there", "indecl; in that eagerness"),
  ("viśrāntimāgacchedyadvīryaṃ", "should-come-to-rest-whose-vigor", "3sg.opt ā-√gam + relative + acc.sg.n vīrya; fused"),
  ("mantramaṇḍale", "in-mantra-circle", "loc.sg.n compound"),
  ("śāntyādisiddhayastattadrūpatādātmyato", "peace-etc-powers-from-that-form-identity", "nom.pl.f long compound + abl.sg -tas; kept fused"),
  ("yataḥ", "since", "indecl causal"),
 ],
 "m": [
  ("tatra", "indecl.", "locus"),
  ("viśrāntimāgacchedyadvīryaṃ", "3sg.opt + rel. + acc.sg.n", "fused verb chain; kept fused"),
  ("mantramaṇḍale", "loc.sg.n", "in the mantra-circle"),
  ("śāntyādisiddhayastattadrūpatādātmyato", "nom.pl.f + abl.sg -tas", "powers from form-identity; kept fused"),
  ("yataḥ", "indecl.", "grounds-cause"),
 ],
 "a": {
  "question": "Why do peace powers arise from resting in the mantra-circle?",
  "premises": [
   "Resting there, vigor comes to rest in the mantra-circle",
   "Peace and the rest of the powers follow",
   "They arise from identity with each respective form"],
  "inference": "Rest in the mantra-circle yields powers through form-identity.",
  "uncertainties": ["scope of yadvīryam within the optative chain"],
  "plain_english": "There, coming to rest whose vigor in the mantra-circle, since peace and the powers come from identity with each respective form.",
 },
},
83: {
 "g": [
  ("divyo", "divine", "nom.sg.m; agrees with group"),
  ("yaścākṣasaṃgho@yaṃ", "and-which-eye-multitude-this", "rel + ca + akṣa-saṃgha + idam with @; fused"),
  ("bodhasvātantryasaṃjñakaḥ", "awareness-freedom-named", "nom.sg.m compound; epithet"),
  ("so@nimīlita", "he-unclosed", "nom.sg.m sa + animīlita with @; fused"),
  ("evaitat", "just-this", "indecl eva + acc.sg.n etat; fused"),
  ("kuryātsvātmamayaṃ", "should-make-self-formed", "3sg.opt √kṛ + acc.sg.n svātma-maya; fused"),
  ("jagat", "world", "acc.sg.n; object"),
 ],
 "m": [
  ("divyo", "nom.sg.m", "divine"),
  ("yaścākṣasaṃgho@yaṃ", "rel + nom.sg.m + dem (@ sandhi)", "which eye-multitude this; kept fused"),
  ("bodhasvātantryasaṃjñakaḥ", "nom.sg.m", "named awareness-freedom"),
  ("so@nimīlita", "nom.sg.m (@ sandhi)", "he unclosed; kept fused"),
  ("evaitat", "indecl + acc.sg.n", "just this"),
  ("kuryātsvātmamayaṃ", "3sg.opt + acc.sg.n", "should make self-formed"),
  ("jagat", "acc.sg.n", "world as object"),
 ],
 "a": {
  "question": "How does the unclosed eye-host make the world of oneself?",
  "premises": [
   "Divine is this eye-multitude named awareness-freedom",
   "Unclosed, he makes just this world self-formed",
   "Open eyes, not shut, perform the making"],
  "inference": "The unclosed awareness-eye makes the world out of oneself.",
  "uncertainties": [],
  "plain_english": "Divine is this eye-multitude named awareness-freedom; unclosed, he makes just this world self-formed.",
 },
},
84: {
 "g": [
  ("mahāsāhasasaṃyogavilīnākhilavṛttikaḥ", "great-venture-union-dissolved-all-activities", "nom.sg.m long compound; state"),
  ("puñjībhūte", "in-heaped", "loc.sg.m ppp puñjī-bhūta"),
  ("svaraśmyoghe", "in-self-ray-flood", "loc.sg.m compound svara-śmi-ogha"),
  ("nirbharībhūya", "having-become-full", "absolutive nirbhara-√bhū"),
  ("tiṣṭhati", "stands", "3sg.pres √sthā"),
 ],
 "m": [
  ("mahāsāhasasaṃyogavilīnākhilavṛttikaḥ", "nom.sg.m", "state; kept fused"),
  ("puñjībhūte", "loc.sg.m ppp", "in the heaped mass"),
  ("svaraśmyoghe", "loc.sg.m", "in the flood of own rays"),
  ("nirbharībhūya", "absolutive", "having become full"),
  ("tiṣṭhati", "3sg.pres √sthā", "main verb; stands"),
 ],
 "a": {
  "question": "How does one stand full in the flood of own rays?",
  "premises": [
   "All activities dissolved in union of great venture",
   "Heaped in the flood of own rays",
   "Having become full, he stands"],
  "inference": "Dissolved activities heaped in own-ray flood: standing full.",
  "uncertainties": [],
  "plain_english": "With all activities dissolved in union of great venture, heaped in the flood of own rays, having become full, he stands.",
 },
},
}

n = 0
for v, d in V.items():
    assert d["a"]["question"].endswith("?") and len(d["a"]["question"].split()) >= 5
    assert all(len(p.split()) >= 3 for p in d["a"]["premises"])
    for sub, rows, keys in (("gloss", d["g"], ("surface", "gloss", "grounds")),
                            ("cm", d["m"], ("lemma", "morph", "grounds"))):
        for r in rows:
            assert len(r) == 3 and all(s.strip() for s in r), (v, sub, r)
            if sub == "gloss":
                assert "(" not in r[1] and ")" not in r[1] and len(r[1].split("-")) <= 15, (v, r)
        dd = RUNS / f"{SONG}-{sub}-v{v:02d}"
        dd.mkdir(parents=True, exist_ok=True)
        (dd / f"{sub}.json").write_text(json.dumps(
            {"song": SONG, "verse": v,
             "rows": [{k: val for k, val in zip(keys, r)} for r in rows]},
            indent=1, ensure_ascii=False))
        n += 1
    ad = RUNS / f"{SONG}-am-v{v:02d}"
    ad.mkdir(parents=True, exist_ok=True)
    (ad / "am.json").write_text(json.dumps(
        {"song": SONG, "verse": v, **d["a"]}, indent=1, ensure_ascii=False))
    n += 1
print(f"wrote {n} files (vv81-84 gloss+cm+am)")
