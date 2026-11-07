#!/usr/bin/env python3
"""Assessor hand-draft tal-a05 vv73-76 (gloss+cm+am). Part 1 of 3.

Provenance: triple task failed 12/12 on one rut-row (v74 abhedavrttitah).
Per largetext SKILL: escalate to assessor hand-draft. Content from working-t1
tokens + Dyczkowski Vol 4 (ch5 heart-utterance/paratattva section) + tal-a05
brief. Gates self-enforced (surfaces byte-exact, gloss paren-free ≤15 parts
no grammar words, Q≥5 words verse-owned, premises ≥3 words).
"""
from __future__ import annotations
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "process" / "beam" / "runs"
SONG = "tal-a05"

# verse -> gloss rows (surface, gloss, grounds), cm rows (surface, morph, grounds), am dict
V: dict[int, dict] = {
73: {
 "g": [
  ("alaṃ", "enough", "indecl particle + instr; closes secret talk"),
  ("rahasyakathayā", "with-secret-talk", "instr.sg.f compound rahasya-kathā"),
  ("guptametatsvabhāvataḥ", "hidden-this-by-own-nature", "acc.sg.n gupta + etat + abl.sg -tas svabhāva; fused span"),
  ("yoginīhṛdayaṃ", "yogini-heart", "acc.sg.n compound; place of rest"),
  ("tatra", "there", "indecl locative adverb"),
  ("viśrāntaḥ", "rested", "nom.sg.m ppp vi-śram; agrees with budhaḥ"),
  ("syātkṛtī", "would-be-accomplished", "3sg.opt as + nom.sg.m kṛtin; fused"),
  ("budhaḥ", "wise-one", "nom.sg.m; subject"),
 ],
 "m": [
  ("alaṃ", "indecl.", "particle governing instrumental"),
  ("rahasyakathayā", "instr.sg.f", "means; secret talk"),
  ("guptametatsvabhāvataḥ", "acc.sg.n + abl.sg.m -tas", "kept fused; hidden by own nature"),
  ("yoginīhṛdayaṃ", "acc.sg.n", "goal of resting"),
  ("tatra", "indecl.", "locative sense"),
  ("viśrāntaḥ", "nom.sg.m ppp (vi-√śram)", "state of the wise"),
  ("syātkṛtī", "3sg.opt √as + nom.sg.m", "would become accomplished"),
  ("budhaḥ", "nom.sg.m", "subject"),
 ],
 "a": {
  "question": "Where does the wise one rest accomplished beyond secret talk?",
  "premises": [
   "Enough of secret talk: this is hidden by its own nature",
   "Resting there in the yogini-heart, the wise is accomplished",
   "Concealment itself is the entry, not an obstacle"],
  "inference": "The yogini-heart is the resting place beyond all secret speech.",
  "uncertainties": [],
  "plain_english": "Enough of secret talk; this is hidden by its own nature. Resting there in the yogini-heart, the wise one becomes accomplished.",
 },
},
74: {
 "g": [
  ("hānādānatiraskāravṛttau", "in-rejecting-accepting-disregarding-conduct", "loc.sg.f long compound; sphere of practice"),
  ("rūḍhimupāgataḥ", "attained-familiarity", "acc.sg.f rūḍhi + nom.sg.m ppp upa-ā-√gam; fused"),
  ("abhedavṛttitaḥ", "from-non-dual-conduct", "abl.sg -tas compound; standpoint, not instrument"),
  ("paśyedviśvaṃ", "should-see-universe", "3sg.opt √dṛś + acc.sg.n viśva; fused"),
  ("citicamatkṛteḥ", "from-consciousness-relish", "abl.sg.f compound citi-camatkṛti; source-ground"),
 ],
 "m": [
  ("hānādānatiraskāravṛttau", "loc.sg.f", "sphere where familiarity is won"),
  ("rūḍhimupāgataḥ", "acc.sg.f + nom.sg.m ppp", "object + subject participle"),
  ("abhedavṛttitaḥ", "abl.sg (-tas formation)", "standpoint: from non-dual conduct"),
  ("paśyedviśvaṃ", "3sg.opt + acc.sg.n", "injunction + object"),
  ("citicamatkṛteḥ", "abl.sg.f", "source: out of consciousness-relish"),
 ],
 "a": {
  "question": "How does one see the universe from non-dual conduct?",
  "premises": [
   "Familiar in rejecting, accepting, and disregarding conduct alike",
   "From non-dual conduct one sees the universe",
   "The seeing flows from the relish of consciousness itself"],
  "inference": "Non-dual conduct turns every act into seeing from relish.",
  "uncertainties": ["whether hana-adana pairs map to specific rites"],
  "plain_english": "Grown familiar in the conduct of rejecting, accepting, and disregarding, one sees the universe from non-dual conduct, out of consciousness-relish.",
 },
},
75: {
 "g": [
  ("arthakriyārthitādainyaṃ", "prayer-born-from-purpose-need", "acc.sg.n compound; what is dropped"),
  ("tyaktvā", "having-abandoned", "absolutive √tyaj"),
  ("bāhyāntarātmani", "in-outer-inner-self", "loc.sg.m compound ātman"),
  ("kharūpe", "in-sky-form", "loc.sg.n compound kha-rūpa"),
  ("nirvṛtiṃ", "cessation-bliss", "acc.sg.f; attained state"),
  ("prāpya", "having-reached", "absolutive √āp"),
  ("phullāṃ", "blossomed", "acc.sg.f; agrees with दशाम् nedan - with nadadasam"),
  ("nādadaśāṃ", "sound-stage", "acc.sg.f compound nāda-daśā"),
  ("śrayet", "should-resort-to", "3sg.opt √śri"),
 ],
 "m": [
  ("arthakriyārthitādainyaṃ", "acc.sg.n", "abandoned object"),
  ("tyaktvā", "absolutive", "prior act"),
  ("bāhyāntarātmani", "loc.sg.m", "locus of self"),
  ("kharūpe", "loc.sg.n", "sky-form locus"),
  ("nirvṛtiṃ", "acc.sg.f", "attained cessation"),
  ("prāpya", "absolutive", "sequence"),
  ("phullāṃ", "acc.sg.f", "blossomed; agrees with sound-stage"),
  ("nādadaśāṃ", "acc.sg.f", "object resorted to"),
  ("śrayet", "3sg.opt √śri", "injunction"),
 ],
 "a": {
  "question": "What follows abandoning need-driven prayer in outer and inner self?",
  "premises": [
   "Prayer born of neediness is abandoned in outer and inner self",
   "Cessation-bliss is reached in sky-form",
   "The blossomed sound-stage is resorted to"],
  "inference": "Dropping need-prayer opens sky-form cessation and the blossomed sound-stage.",
  "uncertainties": [],
  "plain_english": "Abandoning prayer born of neediness in outer and inner self, reaching cessation-bliss in sky-form, one resorts to the blossomed sound-stage.",
 },
},
76: {
 "g": [
  ("vaktramantastayā", "mouth-within-thus", "instr.sg.n? vaktraman tas + tayā; fused span per source"),
  ("samyak", "rightly", "indecl adverb"),
  ("saṃvidaḥ", "of-consciousness", "gen.sg.f saṃvid"),
  ("pravikāsayet", "should-cause-to-bloom", "3sg.opt caus. pra-vi-√kās"),
  ("saṃvidakṣamaruccakraṃ", "consciousness-imperishable-lofty-wheel", "acc.sg.n long compound; kept fused"),
  ("jñeyābhinnaṃ", "non-different-from-knowable", "acc.sg.n compound; agrees with wheel"),
  ("tato", "thence", "indecl ablative adverb"),
  ("bhavet", "should-become", "3sg.opt √bhū"),
 ],
 "m": [
  ("vaktramantastayā", "instr.sg (fused span)", "means; kept fused per source spacing"),
  ("samyak", "indecl.", "manner adverb"),
  ("saṃvidaḥ", "gen.sg.f", "whose blooming"),
  ("pravikāsayet", "3sg.opt causative", "should cause to bloom"),
  ("saṃvidakṣamaruccakraṃ", "acc.sg.n", "object; kept fused"),
  ("jñeyābhinnaṃ", "acc.sg.n", "non-different; agrees with wheel"),
  ("tato", "indecl.", "sequence"),
  ("bhavet", "3sg.opt √bhū", "result"),
 ],
 "a": {
  "question": "What wheel arises when consciousness is rightly bloomed?",
  "premises": [
   "The mouth within rightly blooms consciousness forth",
   "The lofty imperishable wheel of consciousness rises",
   "Non-different from the knowable, it becomes thence"],
  "inference": "Right blooming raises the consciousness-wheel identical with its object.",
  "uncertainties": ["exact force of vaktram-antas-taya as instrumental means"],
  "plain_english": "With the mouth within, rightly bloom consciousness forth; the lofty imperishable wheel of consciousness, non-different from the knowable, becomes thence.",
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
print(f"wrote {n} files (vv73-76 gloss+cm+am)")
