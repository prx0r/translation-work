#!/usr/bin/env python3
"""Assessor hand-draft tal-a05 vv77-80 (gloss+cm+am). Part 2 of 3. See part 1 header."""
from __future__ import annotations
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "process" / "beam" / "runs"
SONG = "tal-a05"

V: dict[int, dict] = {
77: {
 "g": [
  ("tajjñeyaṃ", "that-knowable", "acc.sg.n tad+jñeya sandhi"),
  ("saṃvidākhyena", "by-consciousness-named", "instr.sg.m compound saṃvid-ākhya"),
  ("vahninā", "by-fire", "instr.sg.m; agent of dissolving"),
  ("pravilīyate", "is-dissolved-away", "3sg.pass prati-vi-√lī"),
  ("vilīnaṃ", "dissolved", "acc.sg.n ppp vi-√lī; subject of next clause"),
  ("tat", "that", "nom.sg.n pronoun"),
  ("trikoṇe@smiñśaktivahnau", "in-triangle-here-power-fire", "loc.sg.m with @ sandhi marks; fused span"),
  ("vilīyate", "dissolves", "3sg.pass √lī"),
 ],
 "m": [
  ("tajjñeyaṃ", "acc.sg.n", "object dissolved"),
  ("saṃvidākhyena", "instr.sg.m", "means: by consciousness-fire"),
  ("vahninā", "instr.sg.m", "fire as agent"),
  ("pravilīyate", "3sg.pass prati-vi-√lī", "undergoes dissolving"),
  ("vilīnaṃ", "acc.sg.n ppp", "object of second dissolving"),
  ("tat", "nom.sg.n", "subject pronoun"),
  ("trikoṇe@smiñśaktivahnau", "loc.sg.m (@ sandhi)", "locus; kept fused"),
  ("vilīyate", "3sg.middle √lī", "dissolves"),
 ],
 "a": {
  "question": "How does the knowable dissolve into the power-fire triangle?",
  "premises": [
   "That knowable is dissolved away by the consciousness-named fire",
   "Dissolved, it dissolves again in the power-fire of the triangle here",
   "Double dissolution leaves no remainder outside"],
  "inference": "Consciousness-fire dissolves the knowable twice over into the triangle.",
  "uncertainties": [],
  "plain_english": "That knowable is dissolved away by the consciousness-named fire; dissolved, it dissolves in the power-fire of the triangle here.",
 },
},
78: {
 "g": [
  ("tatra", "there", "indecl; in that dissolution"),
  ("saṃvedanodārabindusattāsunirvṛtaḥ", "perception-noble-drop-being-well-at-peace", "nom.sg.m long compound; state"),
  ("saṃhārabījaviśrānto", "rested-in-withdrawal-seed", "nom.sg.m compound; state"),
  ("yogī", "yogi", "nom.sg.m; subject"),
  ("paramayo", "supreme-measured", "nom.sg.m compound; epithet"),
  ("bhavet", "should-become", "3sg.opt √bhū"),
 ],
 "m": [
  ("tatra", "indecl.", "locus adverb"),
  ("saṃvedanodārabindusattāsunirvṛtaḥ", "nom.sg.m", "state; kept fused"),
  ("saṃhārabījaviśrānto", "nom.sg.m", "state; kept fused"),
  ("yogī", "nom.sg.m", "subject"),
  ("paramayo", "nom.sg.m", "epithet; of supreme measure"),
  ("bhavet", "3sg.opt √bhū", "result"),
 ],
 "a": {
  "question": "What becomes of the yogi rested in the withdrawal seed?",
  "premises": [
   "There, well at peace in noble perception-drop-being",
   "Rested in the withdrawal seed, the yogi holds",
   "Supreme-measured, he becomes the measure itself"],
  "inference": "Resting in withdrawal-seed perception, the yogi becomes supreme measure.",
  "uncertainties": ["exact scope of paramaya as epithet vs state"],
  "plain_english": "There, well at peace in noble perception-drop-being, rested in the withdrawal seed, the yogi becomes supreme-measured.",
 },
},
79: {
 "g": [
  ("antarbāhye", "in-inner-outer", "loc.sg.n compound antar-bāhya"),
  ("dvaye", "in-two", "loc.sg.n numeral dva"),
  ("vāpi", "even", "indecl vā+api"),
  ("sāmānyetarasundaraḥ", "common-other-beautiful", "nom.sg.m compound; subject epithet"),
  ("saṃvitspandastriśaktyātmā", "consciousness-throb-three-power-self", "nom.sg.m long compound; essence"),
  ("saṃkocapravikāsavān", "possessing-contraction-expansion", "nom.sg.m possessive compound"),
 ],
 "m": [
  ("antarbāhye", "loc.sg.n", "in both"),
  ("dvaye", "loc.sg.n", "in the two"),
  ("vāpi", "indecl.", "concessive"),
  ("sāmānyetarasundaraḥ", "nom.sg.m", "epithet; beautiful beyond common and uncommon"),
  ("saṃvitspandastriśaktyātmā", "nom.sg.m", "essence; kept fused"),
  ("saṃkocapravikāsavān", "nom.sg.m (-vat)", "possessing both movements"),
 ],
 "a": {
  "question": "How is the beautiful one both contracted and expanded?",
  "premises": [
   "In inner and outer both, beautiful beyond common and rare",
   "Its self is consciousness-throb of three powers",
   "It holds contraction and expansion together"],
  "inference": "The three-powered throb-self is beautiful in both movements at once.",
  "uncertainties": [],
  "plain_english": "In inner and outer both, beautiful beyond common and uncommon, the self of consciousness-throb and three powers holds contraction and expansion.",
 },
},
80: {
 "g": [
  ("asaṃkocavikāso@pi", "uncontracted-expansion-even", "nom.sg.m compound with @; subject"),
  ("tadābhāsanatastathā", "from-its-shining-forth-thus", "abl.sg -tas compound; source"),
  ("antarlakṣyo", "inner-aimed", "nom.sg.m compound antar-lakṣya"),
  ("bahirdṛṣṭiḥ", "outward-gazed", "nom.sg.f compound bahis-dṛṣṭi"),
  ("paramaṃ", "supreme", "acc.sg.n; agrees with padam"),
  ("padamaśnute", "reaches-state", "acc.sg.n pada + 3sg.mid √aś; fused"),
 ],
 "m": [
  ("asaṃkocavikāso@pi", "nom.sg.m (@ sandhi)", "subject; kept fused"),
  ("tadābhāsanatastathā", "abl.sg (-tas)", "source of shining"),
  ("antarlakṣyo", "nom.sg.m", "inward aim"),
  ("bahirdṛṣṭiḥ", "nom.sg.f", "outward gaze"),
  ("paramaṃ", "acc.sg.n", "supreme; agrees with state"),
  ("padamaśnute", "acc.sg.n + 3sg.mid", "reaches the state"),
 ],
 "a": {
  "question": "How does uncontracted expansion reach the supreme state?",
  "premises": [
   "Even uncontracted expansion shines forth from that thus",
   "Aimed within, gazing outward at once",
   "The supreme state is reached by this double posture"],
  "inference": "Inward aim with outward gaze carries expansion to the supreme state.",
  "uncertainties": [],
  "plain_english": "Even uncontracted expansion, from its shining forth thus, aimed within with outward gaze, reaches the supreme state.",
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
print(f"wrote {n} files (vv77-80 gloss+cm+am)")
