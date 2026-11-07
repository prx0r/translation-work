#!/usr/bin/env python3
"""Assessor hand-draft tal-a06 vv217-228 (gloss+cm+am). Smallest failed cluster.

Provenance: tal-a06-triple-v217 failed 6/6 (content gates: question rejected,
premise too short, bad row 'ikārokārayorādisandhau' gloss with LEAK 'sandhi').
Per largetext SKILL: escalate to assessor hand-draft. Content from working-t1
surfaces + source spans (sha 12fbea19940e3622) + tal-a06 brief (kalacakra:
letters/praveśa arising in breath-flow; numbers exact; śabdādhvā varṇa section
vv211-252). Gates self-enforced (surfaces byte-exact, gloss lowercase
hyphen-joined no parens/quotes <=15 parts no grammar words, Q>=5 words
verse-owned, premises >=3 words each >=3 premises, plain >=4 words,
uncertainties honest). Last cluster on a06: completes the song's runs.
"""
from __future__ import annotations
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "process" / "beam" / "runs"
SONG = "tal-a06"

V: dict[int, dict] = {
217: {
 "g": [
  ("eko", "one", "m.nom.sg eka; the single letter"),
  ("nādātmako", "nāda-essenced", "m.nom.sg nāda-ātman; whose self is the primal hum"),
  ("varṇaḥ", "letter", "m.nom.sg varṇa; the phoneme at issue"),
  ("sarvavarṇāvibhāgavān", "all-letters-undivided", "m.nom.sg sarva-varṇa-avibhāga-vān; bearing no division among all letters"),
  ("so@nastamitarūpatvādanāhata", "unstruck-because-its-form-never-sets", "saḥ + anastamita-rūpatvāt + anāhata; its form never sets, hence unstruck"),
  ("ihoditaḥ", "arisen-here", "iha + uditaḥ m.nom.sg; manifested in this breath-flow"),
 ],
 "m": [
  ("eko", "m.nom.sg", "one"),
  ("nādātmako", "m.nom.sg (nāda-ātman)", "hum-essenced"),
  ("varṇaḥ", "m.nom.sg", "letter"),
  ("sarvavarṇāvibhāgavān", "m.nom.sg (sarva-varṇa-avibhāga)", "undivided across all letters"),
  ("so@nastamitarūpatvādanāhata", "m.nom.sg (saḥ + anastamita-rūpatvāt + anāhata)", "unstruck because its form does not set"),
  ("ihoditaḥ", "m.nom.sg (iha + uditaḥ)", "arisen here"),
 ],
 "a": {
  "question": "What is the one letter arisen here that never sets and is unstruck?",
  "premises": [
   "One letter has the nāda hum as its very self",
   "It bears no division among all the letters",
   "Because its form never sets it is the unstruck one"],
  "inference": "The nāda-letter stands undivided and unstruck, arisen in the breath-flow.",
  "uncertainties": ["so@nastamitarūpatvādanāhata causal reading (anastamita-rūpatvāt + anāhata) approximate"],
  "plain_english": "One letter, whose self is the nāda hum, bears all letters undivided; because its form never sets, it is the unstruck one arisen here.",
 },
},
218: {
 "g": [
  ("sa", "he", "m.nom.sg sa; resumes the letter just named"),
  ("tu", "but", "indecl; pivot"),
  ("bhairavasadbhāvo", "bhairava-being", "m.nom.sg bhairava-sadbhāva; the very being of Bhairava"),
  ("mātṛsadbhāva", "mother-being", "m.nom.sg mātṛ-sadbhāva; the very being of the Mother"),
  ("eṣa", "this", "m.nom.sg eṣa; this one"),
  ("saḥ", "he", "m.nom.sg saḥ; he"),
  ("parā", "supreme", "f.nom.sg parā; Parā, the highest power"),
  ("saikākṣarā", "one-letter-possessing", "f.nom.sg sa-ekākṣarā; together with a single letter"),
  ("devī", "goddess", "f.nom.sg devī"),
  ("yatra", "where", "indecl rel; in whom"),
  ("līnaṃ", "dissolved", "n.nom.sg √lī; absorbed (with carācaram)"),
  ("carācaram", "moving-and-unmoving", "n.nom.sg cara-acara; the mobile and the immobile"),
 ],
 "m": [
  ("sa", "m.nom.sg", "he"),
  ("tu", "indecl.", "but"),
  ("bhairavasadbhāvo", "m.nom.sg (bhairava-sadbhāva)", "Bhairava-being"),
  ("mātṛsadbhāva", "m.nom.sg (mātṛ-sadbhāva)", "Mother-being"),
  ("eṣa", "m.nom.sg", "this"),
  ("saḥ", "m.nom.sg", "he"),
  ("parā", "f.nom.sg (Parā)", "the supreme"),
  ("saikākṣarā", "f.nom.sg (sa-ekākṣarā)", "with a single letter"),
  ("devī", "f.nom.sg", "goddess"),
  ("yatra", "indecl. (rel.)", "where"),
  ("līnaṃ", "n.nom.sg (√lī)", "dissolved"),
  ("carācaram", "n.nom.sg (cara-acara)", "moving and unmoving"),
 ],
 "a": {
  "question": "Who is the one-lettered Goddess in whom the moving and unmoving dissolve?",
  "premises": [
   "That letter is Bhairava's very being and the Mother's being",
   "Parā is the Goddess together with the single letter",
   "In her the moving and unmoving are absorbed"],
  "inference": "The single letter names Bhairava and Mother; all motion rests dissolved in Parā.",
  "uncertainties": ["saikākṣarā may qualify devī alone or the pair — agreement left open"],
  "plain_english": "That is Bhairava's being and the Mother's being: Parā, the Goddess with the single letter, in whom the moving and unmoving dissolve.",
 },
},
219: {
 "g": [
  ("hrasvārṇatrayamekaikaṃ", "three-short-letters-one-each", "n.nom.sg hrasva-varṇa-traya + ekaika; three short letters, one each"),
  ("ravyaṅgulamathetarat", "sun-aṅgula-and-other", "n.nom.sg ravi-aṅgula + atha + itara; the solar aṅgula-measure and the other — segmentation open"),
  ("praveśa", "entry", "m.nom.sg praveśa; the entering of the letters"),
  ("iti", "thus", "indecl; names the entry"),
  ("ṣaḍvarṇāḥ", "six-letters", "m.nom.pl ṣaṭ-varṇa; the six letters"),
  ("sūryendupathagāḥ", "sun-and-moon-path-going", "m.nom.pl sūrya-indu-patha-ga; traveling the solar and lunar paths"),
  ("kramāt", "in-order", "abl.sg krama; step by step"),
 ],
 "m": [
  ("hrasvārṇatrayamekaikaṃ", "n.nom.sg (hrasva-varṇa-traya + ekaika)", "three short letters one each"),
  ("ravyaṅgulamathetarat", "n.nom.sg (ravi-aṅgula + atha + itara)", "the solar measure and the other"),
  ("praveśa", "m.nom.sg", "entry"),
  ("iti", "indecl.", "thus"),
  ("ṣaḍvarṇāḥ", "m.nom.pl (ṣaṭ-varṇa)", "the six letters"),
  ("sūryendupathagāḥ", "m.nom.pl (sūrya-indu-patha-ga)", "going sun- and moon-path"),
  ("kramāt", "abl.sg", "in order"),
 ],
 "a": {
  "question": "How do the six letters enter by sun and moon paths in order?",
  "premises": [
   "Three short letters come one each with the solar measure and the other",
   "Entering thus the six letters go the sun and moon paths",
   "They proceed in fixed order one after another"],
  "inference": "Entry sequences the six letters across solar and lunar measures in order.",
  "uncertainties": ["ravyaṅgulamathetarat segmentation open (ravi-aṅgula + atha + itara); 'the other' may be the lunar measure"],
  "plain_english": "Three short letters, one each, with the solar aṅgula and the other: entering, the six letters go the sun- and moon-paths in order.",
 },
},
220: {
 "g": [
  ("ikārokārayorādisandhau", "first-join-of-i-and-u", "loc.sg.n ikāra-ukārayoḥ + ādi-saṃdhi; in the first joining of i and u"),
  ("saṃdhyakṣaradvayam", "joint-letter-pair", "n.nom.sg saṃdhyā-akṣara-dvaya; the two transitional letters"),
  ("e+o", "e-and-o", "the pair e and o as written"),
  ("iti", "thus", "indecl; names the pair"),
  ("praveśe", "at-entry", "loc.sg.m praveśa; in the entering"),
  ("tu", "but", "indecl; contrast"),
  ("ai+au", "ai-and-au", "the pair ai and au as written"),
  ("iti", "thus", "indecl; names the pair"),
  ("dvayaṃ", "the-pair", "n.nom.sg dvaya; the pair"),
  ("viduḥ", "they-know", "3pl.pres.act √vid; the knowing ones know"),
 ],
 "m": [
  ("ikārokārayorādisandhau", "loc.sg.n (ikāra-ukāra + ādi-saṃdhi)", "at the first join of i and u"),
  ("saṃdhyakṣaradvayam", "n.nom.sg (saṃdhyā-akṣara-dvaya)", "the joint-letter pair"),
  ("e+o", "letter pair (e + o)", "e and o"),
  ("iti", "indecl.", "thus"),
  ("praveśe", "loc.sg.m", "at entry"),
  ("tu", "indecl.", "but"),
  ("ai+au", "letter pair (ai + au)", "ai and au"),
  ("iti", "indecl.", "thus"),
  ("dvayaṃ", "n.nom.sg", "the pair"),
  ("viduḥ", "3pl.pres.act √vid", "they know"),
 ],
 "a": {
  "question": "Which joint letters do the wise know at the first entry of i and u?",
  "premises": [
   "At the first joining of i and u stand two junction letters",
   "These two are named e and o at entry",
   "At entry ai and au make up the further pair"],
  "inference": "Entry combines i and u into e and o, with ai and au as the second pair.",
  "uncertainties": ["whether e and o arise before entry or at it remains text-ambiguous"],
  "plain_english": "At the first joining of i and u stand the two joint letters e and o; at entry the wise know the pair ai and au.",
 },
},
221: {
 "g": [
  ("ṣaṇṭhārṇāni", "six-placed-letters", "n.nom.pl; reading open — likely ṣaṣ sthā-varṇāni, the six-placed letters (cf. v222 sasthāna)"),
  ("praveśe", "at-entry", "loc.sg.m; in the entering"),
  ("tu", "but", "indecl; contrast"),
  ("dvādaśāntalalāṭayoḥ", "twelve-end-and-forehead", "loc.dual dvādaśānta + lalāṭa; at the dvādaśānta and the forehead"),
  ("gale", "at-throat", "loc.sg.n gala; at the throat"),
  ("hṛdi", "at-heart", "loc.sg.n hṛd; at the heart"),
  ("ca", "and", "indecl"),
  ("bindvarṇavisargau", "bindu-letter-and-visarga", "nom.dual bindu-varṇa + visarga; the bindu letter and the visarga"),
  ("paritaḥsthitau", "standing-around", "nom.dual paritaḥ-sthita; standing on both sides"),
 ],
 "m": [
  ("ṣaṇṭhārṇāni", "n.nom.pl (reading open)", "six-placed letters — segmentation flagged"),
  ("praveśe", "loc.sg.m", "at entry"),
  ("tu", "indecl.", "but"),
  ("dvādaśāntalalāṭayoḥ", "loc.dual (dvādaśānta + lalāṭa)", "at twelve-end and forehead"),
  ("gale", "loc.sg.n", "at throat"),
  ("hṛdi", "loc.sg.n", "at heart"),
  ("ca", "indecl.", "and"),
  ("bindvarṇavisargau", "nom.dual (bindu-varṇa + visarga)", "bindu letter and visarga"),
  ("paritaḥsthitau", "nom.dual (paritaḥ-sthita)", "standing around"),
 ],
 "a": {
  "question": "Where do the bindu letter and visarga stand at entry in the body?",
  "premises": [
   "At entry the six-placed letters stand at the twelve-end and forehead",
   "They stand at the throat and at the heart as well",
   "The bindu letter and the visarga stand around those places"],
  "inference": "Entry seats bindu and visarga around forehead, throat, and heart — the letter's bodily stations.",
  "uncertainties": ["ṣaṇṭhārṇāni reading open — likely six-placed letters (cf. v222), possibly a letter-series"],
  "plain_english": "At entry the letters stand at the twelve-end, forehead, throat, and heart, with bindu and visarga stationed around them.",
 },
},
222: {
 "g": [
  ("kādipañcakamādyasya", "first-of-the-ka-five", "gen.sg.m kādi-pañcaka + ādya; of the first of the five starting with ka"),
  ("varṇasyāntaḥ", "within-the-letter", "gen.sg varṇa + antaḥ; inside that letter"),
  ("sadoditam", "always-arisen", "n.nom.sg sadā + udita; ever-arising"),
  ("evaṃ", "thus", "indecl"),
  ("sasthānavarṇānāmantaḥ", "within-six-placed-letters", "gen.pl sa-sthāna-varṇa + antaḥ; within the six-placed letters"),
  ("sā", "that", "f.nom.sg sā; that"),
  ("sārṇasantatiḥ", "letter-matched-continuity", "f.nom.sg sa-arṇa-santati; the succession bearing the same letters"),
 ],
 "m": [
  ("kādipañcakamādyasya", "gen.sg.m (kādi-pañcaka + ādya)", "first of the ka-five"),
  ("varṇasyāntaḥ", "gen.sg + adv.", "within the letter"),
  ("sadoditam", "n.nom.sg (sadā + udita)", "always arisen"),
  ("evaṃ", "indecl.", "thus"),
  ("sasthānavarṇānāmantaḥ", "gen.pl (sa-sthāna-varṇa) + adv.", "within six-placed letters"),
  ("sā", "f.nom.sg", "that"),
  ("sārṇasantatiḥ", "f.nom.sg (sa-arṇa-santati)", "the same-lettered succession"),
 ],
 "a": {
  "question": "How does the letter-line run within the six-placed letters of the ka-five?",
  "premises": [
   "Within the letter at the head of the ka-group of five it always arises",
   "Thus within the six-placed letters runs that same line of letters",
   "That continuity bears the same letters throughout"],
  "inference": "The ever-arising letter threads the six-placed series as one same-lettered line.",
  "uncertainties": ["sārṇasantatiḥ taken as 'succession bearing the same letters' — sa-arṇa segmentation assumed"],
  "plain_english": "Within the first letter of the ka-five, ever-arising, that same letter-continuity runs inside the six-placed letters.",
 },
},
223: {
 "g": [
  ("hṛdyeṣa", "in-heart-this", "loc.sg.n hṛdi + eṣa; in the heart this one"),
  ("prāṇarūpastu", "breath-form-however", "nom.sg.m prāṇa-rūpa + tu; as breath-form however"),
  ("sakāro", "the-s-letter", "nom.sg.m sa-kāra; the letter s"),
  ("jīvanātmakaḥ", "life-essenced", "nom.sg.m jīva-ātmaka; having life as its self"),
  ("binduḥ", "the-bindu", "nom.sg.m bindu; the dot-letter"),
  ("prakāśo", "light", "nom.sg.m prakāśa; radiance"),
  ("hārṇaśca", "and-the-hārṇa", "nom.sg.m hārṇa + ca; and hārṇa — letter-name not securely identified, left open"),
  ("pūraṇātmatayā", "as-fullness", "instr.sg.f pūraṇa-ātmatā; by being fullness"),
  ("sthitaḥ", "stands", "nom.sg.m √sthā; stands there"),
 ],
 "m": [
  ("hṛdyeṣa", "loc + nom (hṛdi eṣa)", "in the heart this"),
  ("prāṇarūpastu", "nom.sg.m (prāṇa-rūpa) + particle", "as breath-form however"),
  ("sakāro", "nom.sg.m (sa-kāra)", "the s-letter"),
  ("jīvanātmakaḥ", "nom.sg.m (jīva-ātmaka)", "life-essenced"),
  ("binduḥ", "nom.sg.m", "bindu"),
  ("prakāśo", "nom.sg.m", "light"),
  ("hārṇaśca", "nom.sg.m (hārṇa) + particle", "and hārṇa"),
  ("pūraṇātmatayā", "instr.sg.f (pūraṇa-ātmatā)", "as fullness"),
  ("sthitaḥ", "nom.sg.m (√sthā)", "stands"),
 ],
 "a": {
  "question": "What three stand in the heart as life, light, and fullness?",
  "premises": [
   "In the heart this one takes breath-form with the s-letter alive with life",
   "The bindu is light and the hārṇa stands as fullness",
   "All three stand there by being completion itself"],
  "inference": "Heart-s as life, bindu as light, and hārṇa as fullness stand completed there.",
  "uncertainties": ["hārṇa letter-name not securely identified — possibly the ha beyond the mātṛkā; left open", "pūraṇātmatayā read as 'by being fullness'"],
  "plain_english": "In the heart the s-letter is life in breath-form, the bindu light, and the hārṇa stands as fullness itself.",
 },
},
224: {
 "g": [
  ("uktaḥ", "spoken-of", "nom.sg.m ppp √vad; is spoken of"),
  ("paro@yamudayo", "this-highest-arising", "nom.sg.m paraḥ + ayam + udaya; this highest arising"),
  ("varṇānāṃ", "of-letters", "gen.pl varṇa"),
  ("sūkṣma", "subtle", "nom.sg.m sūkṣma"),
  ("ucyate", "is-called", "3sg.pres.pass √vac"),
  ("praveśe", "at-entry", "loc.sg.m praveśa"),
  ("ṣoḍaśaunmukhye", "facing-sixteen", "loc.sg.n ṣoḍaśa-anmukhya; facing the sixteen"),
  ("ravayaḥ", "the-solar-ones", "nom.pl.m ravi; the solar ones — whether solar letters or the ra-series stays open"),
  ("ṣaṇṭhavarjitāḥ", "except-ṣaṇṭhā", "nom.pl.m -varjita; excluding the ṣaṇṭhā set (see v221)"),
 ],
 "m": [
  ("uktaḥ", "nom.sg.m (ppp √vad)", "spoken of"),
  ("paro@yamudayo", "nom.sg.m (paraḥ + ayam + udaya)", "this highest arising"),
  ("varṇānāṃ", "gen.pl", "of letters"),
  ("sūkṣma", "nom.sg.m", "subtle"),
  ("ucyate", "3sg.pres.pass √vac", "is called"),
  ("praveśe", "loc.sg.m", "at entry"),
  ("ṣoḍaśaunmukhye", "loc.sg.n (ṣoḍaśa-anmukhya)", "facing sixteen"),
  ("ravayaḥ", "nom.pl.m (ravi)", "the solar ones"),
  ("ṣaṇṭhavarjitāḥ", "nom.pl.m (ṣaṇṭha-varjita)", "excluding the ṣaṇṭhā"),
 ],
 "a": {
  "question": "Which arising of letters is called the subtle one at entry?",
  "premises": [
   "This highest arising of the letters is called the subtle one",
   "At entry facing the sixteen stand the solar ones",
   "Those solar ones stand apart from the ṣaṇṭhā set"],
  "inference": "The subtle letter-arising is the highest, entered sixteen-facing with the solar ones.",
  "uncertainties": ["ravayaḥ taken as 'the solar ones' — possibly the ra-letters; referent open", "ṣaṇṭha-varjitāḥ points back to v221's letter set"],
  "plain_english": "This highest arising of letters is called subtle: at entry, sixteen-facing, the solar ones stand apart from the ṣaṇṭhā.",
 },
},
225: {
 "g": [
  ("tadevendvarkamatrānye", "these-are-moon-sun-measures", "tad eva + indv-arka-mātrāṇy + (e)te; those very measures of moon and sun — segmentation approximate"),
  ("varṇāḥ", "letters", "nom.pl.m varṇa"),
  ("sūkṣmodayastvayam", "this-subtle-arising", "nom.sg.m sūkṣma-udaya + tu + ayam; this subtle arising"),
  ("kālo@rdhamātraḥ", "half-measure-time", "nom.sg.m kāla + ardamātra; time of half a mātrā"),
  ("kādīnāṃ", "of-the-ka-series", "gen.pl kādi; of those beginning with ka"),
  ("trayastriṃśata", "thirty-three", "gen. of trayastriṃśat; thirty-three of them"),
  ("ucyate", "is-called", "3sg.pres.pass √vac"),
 ],
 "m": [
  ("tadevendvarkamatrānye", "nom.pl (compound, segmentation open)", "those very moon-sun measures"),
  ("varṇāḥ", "nom.pl.m", "letters"),
  ("sūkṣmodayastvayam", "nom.sg.m (sūkṣma-udaya) + particle", "this subtle arising"),
  ("kālo@rdhamātraḥ", "nom.sg.m (kāla + ardamātra)", "half-measure time"),
  ("kādīnāṃ", "gen.pl (kādi)", "of the ka-series"),
  ("trayastriṃśata", "gen. (trayastriṃśat)", "thirty-three"),
  ("ucyate", "3sg.pres.pass √vac", "is called"),
 ],
 "a": {
  "question": "How is half-measure time reckoned for the thirty-three ka-series letters?",
  "premises": [
   "Those very letters are the measures of moon and sun",
   "This subtle arising is time of half a measure",
   "Of the ka-series thirty-three letters are so called"],
  "inference": "Half-measure time names the subtle arising across thirty-three ka-letters.",
  "uncertainties": ["tadevendvarkamatrānye segmentation (tad eva indv-arka-mātrāṇy ete?) approximate", "trayastriṃśata read as genitive partitive 'of thirty-three'"],
  "plain_english": "These letters are the moon-sun measures; this subtle arising is half-measure time — thirty-three of the ka-series, it is called.",
 },
},
226: {
 "g": [
  ("mātrā", "measures", "f.nom.pl mātrā; the vowel-measures"),
  ("hrasvāḥ", "short-ones", "nom.pl.m hrasva; the short measures"),
  ("pañca", "five", "indecl num; five"),
  ("dīrghāṣṭakaṃ", "eight-long", "n.nom.sg dīrgha-aṣṭaka; the eight long ones"),
  ("dvistriḥ", "twice-thrice", "indecl dvi-tri; twice, thrice"),
  ("plutaṃ", "prolated", "n.nom.sg pluta; the prolated three-mora measure"),
  ("tu", "but", "indecl"),
  ("lṝ", "lṝ-letter", "the letter lṝ, long vocalic r, counted among the measures"),
  ("ekāśītimimāmardhamātrāṇāmāha", "says-these-eighty-one-half-measures", "āha + imām + ekāśītim + gen.pl ardhamātrā; he says these eighty-one of the half-measures"),
  ("no", "our", "gen.pl naḥ; our"),
  ("guruḥ", "the-teacher", "nom.sg.m guru"),
 ],
 "m": [
  ("mātrā", "f.nom.pl", "the measures"),
  ("hrasvāḥ", "nom.pl.m", "short ones"),
  ("pañca", "indecl.", "five"),
  ("dīrghāṣṭakaṃ", "n.nom.sg (dīrgha-aṣṭaka)", "eight long"),
  ("dvistriḥ", "indecl. (dvi-tri)", "twice thrice"),
  ("plutaṃ", "n.nom.sg", "pluta"),
  ("tu", "indecl.", "but"),
  ("lṝ", "letter (lṝ)", "the letter lṝ"),
  ("ekāśītimimāmardhamātrāṇāmāha", "3sg.perf √ah + gen.pl", "says these eighty-one half-measures"),
  ("no", "gen.pl", "our"),
  ("guruḥ", "nom.sg.m", "the teacher"),
 ],
 "a": {
  "question": "How many half-measures does the guru count among the vowel measures?",
  "premises": [
   "The measures are five short and eight long",
   "Twice and thrice and pluta and lṝ follow them",
   "Our guru calls these eighty-one of the half-measures"],
  "inference": "Five short, eight long, with twice, thrice, pluta, and lṝ yield eighty-one half-measures.",
  "uncertainties": ["dvistriḥ taken as 'twice, thrice'; exact count depends on how pluta and lṝ are reckoned"],
  "plain_english": "Shorts are five, longs eight, with twice, thrice, pluta, and lṝ: our guru calls these eighty-one half-measures.",
 },
},
227: {
 "g": [
  ("yadvaśādbhagavānekāśītikaṃ", "by-whose-will-lord-the-eighty-one", "abl yad-vaśāt + nom bhagavān + adj ekāśītikam; by whose will the Lord — the eighty-one(-letter one)"),
  ("mantramabhyadhāt", "uttered-the-mantra", "acc.sg.m mantra + 3sg.aor √ādh abhyadhāt; he set forth the mantra"),
  ("ekāśītipadā", "of-eighty-one-words", "f.nom.sg parā-stem ekāśīti-pada; the eighty-one-worded — stem read open"),
  ("devī", "goddess", "f.nom.sg devī"),
  ("śaktiḥ", "power", "f.nom.sg śakti"),
  ("proktā", "is-called", "f.nom.sg ppp √vad"),
  ("śivātmikā", "śiva-essenced", "f.nom.sg śiva-ātmikā; having Śiva as her self"),
 ],
 "m": [
  ("yadvaśādbhagavānekāśītikaṃ", "abl.sg + nom.sg.m + adj.", "by whose will the Lord the eighty-one"),
  ("mantramabhyadhāt", "acc.sg.m + 3sg.aor √ādh", "uttered the mantra"),
  ("ekāśītipadā", "f.nom.sg? (parā-stem, read open)", "the eighty-one-worded"),
  ("devī", "f.nom.sg", "goddess"),
  ("śaktiḥ", "f.nom.sg", "power"),
  ("proktā", "f.nom.sg (ppp √vad)", "is called"),
  ("śivātmikā", "f.nom.sg (śiva-ātmikā)", "Śiva-essenced"),
 ],
 "a": {
  "question": "By whose will did the Lord utter the eighty-one-worded mantra of the Goddess?",
  "premises": [
   "By her will the Lord uttered the eighty-one-letter mantra",
   "The Goddess of eighty-one words is called the power",
   "That power has Śiva as her very self"],
  "inference": "The eighty-one-word mantra proceeds from the Śiva-bodied Goddess at the willing of the Lord.",
  "uncertainties": ["yad-vaśāt antecedent (guru, Bhagavatī) not named in the couplet", "ekāśītipadā stem read as parā-compound — open"],
  "plain_english": "By whose will the Lord uttered the eighty-one-letter mantra: the Goddess of eighty-one words is the power, told of as Śiva's own.",
 },
},
228: {
 "g": [
  ("śrīmātaṅge", "in-glorious-mātaṅga", "loc.sg.n śrī-mātaṅga; in the glorious Mātaṅga"),
  ("tathā", "likewise", "indecl"),
  ("dharmasaṃghātātmā", "dharma-mass-essenced", "nom.sg.m dharma-saṅghāta-ātman; whose self is the mass of dharmas"),
  ("śivo", "śiva", "nom.sg.m śiva before yataḥ"),
  ("yataḥ", "from-whom", "indecl rel abl; from whom"),
  ("tathā", "likewise", "indecl"),
  ("tathā", "likewise", "indecl; repeated as written"),
  ("parāmarśaśakticakreśvaraḥ", "lord-of-the-reflective-power-wheel", "nom.sg.m parāmarśa-śakti-cakra-īśvara; the lord of the wheel of reflective power"),
  ("prabhuḥ", "the-ruler", "nom.sg.m prabhu; the ruler"),
 ],
 "m": [
  ("śrīmātaṅge", "loc.sg.n (mātaṅga)", "in the glorious Mātaṅga"),
  ("tathā", "indecl.", "likewise"),
  ("dharmasaṃghātātmā", "nom.sg.m (dharma-saṅghāta-ātman)", "dharma-mass-essenced"),
  ("śivo", "nom.sg.m", "Śiva"),
  ("yataḥ", "indecl. (rel.)", "from whom"),
  ("tathā", "indecl.", "likewise"),
  ("tathā", "indecl.", "likewise (repeated)"),
  ("parāmarśaśakticakreśvaraḥ", "nom.sg.m (parāmarśa-śakti-cakra-īśvara)", "lord of the reflective-power wheel"),
  ("prabhuḥ", "nom.sg.m", "the ruler"),
 ],
 "a": {
  "question": "Who is the lord of the wheel of reflective power in the Mātaṅga?",
  "premises": [
   "In the glorious Mātaṅga whose self is the dharma-mass",
   "Śiva is he from whom this is told",
   "The lord of the parāmarśa-power wheel is the ruler"],
  "inference": "Mātaṅga grounds the reflective-power wheel whose lord is Śiva the ruler.",
  "uncertainties": ["dharmasaṃghātātmā compound read as dharma-saṅghāta-ātman — open", "tathā repeated in the verse as written"],
  "plain_english": "In the glorious Mātaṅga, whose self is the dharma-mass, is Śiva, from whom it comes — the parāmarśa wheel's lord, the ruler.",
 },
},
}

# byte-exact surfaces from working-t1 / source spans
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
import workcfg
spans = workcfg.source_spans("tantraloka-a06")
wt = json.loads((Path(__file__).resolve().parent.parent / "working-t1-tal-a06.json").read_text())

LEAK = ("genitive", "nominative", "accusative", "instrumental", "dative",
        "ablative", "locative", "vocative", "singular", "plural", "dual",
        "participle", "passive", "causative", "optative", "imperative",
        "sandhi", "compound")
META = ("does verse", "this verse", "is being told", "what argument does this passage",
        "what does this passage say about")

n = 0
for v, d in V.items():
    surfs = [t["surface"] for t in next(x for x in wt if x["verse"] == v)["tokens"]]
    assert surfs == spans[v], f"span mismatch v{v}"
    assert [r[0] for r in d["g"]] == surfs, f"gloss surface drift v{v}"
    assert [r[0] for r in d["m"]] == surfs, f"cm surface drift v{v}"
    q = d["a"]["question"]
    assert q.endswith("?") and len(q.split()) >= 5, (v, q)
    assert not any(p in q.lower() for p in META), (v, q)
    assert len(d["a"]["premises"]) >= 3 and all(len(p.split()) >= 3 for p in d["a"]["premises"]), v
    assert len(d["a"]["plain_english"].split()) >= 4, v
    assert d["a"]["uncertainties"], f"no uncertainties v{v}"
    assert d["a"]["inference"].strip(), v
    for sub, rows, keys in (("gloss", d["g"], ("surface", "gloss", "grounds")),
                            ("cm", d["m"], ("lemma", "morph", "grounds"))):
        for r in rows:
            assert len(r) == 3 and all(s.strip() for s in r), (v, sub, r)
            if sub == "gloss":
                assert "(" not in r[1] and ")" not in r[1] and '"' not in r[1], (v, r)
                assert len(r[1].split("-")) <= 15, (v, r)
                assert not any(w in r[1].lower().split("-") for w in LEAK), (v, r)
                assert r[1].lower() == r[1], (v, r)
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
print(f"wrote {n} files (vv217-228 gloss+cm+am) — self-gate PASS surfaces/Q/premises")
