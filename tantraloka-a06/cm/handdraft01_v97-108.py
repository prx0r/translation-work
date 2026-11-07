#!/usr/bin/env python3
"""Assessor hand-draft tal-a06 vv97-108 (gloss+cm+am). Smallest failed cluster.

Provenance: tal-a06-triple-v97 failed 6/6 (content gates). Per largetext SKILL:
escalate to assessor hand-draft. Content from working-t1 surfaces + source spans
(sha 12fbea19940e3622) + tal-a06 brief (kalacakra: time-in-breath; astrology
terms transliterated + function-glossed; numbers exact). Gates self-enforced
(surfaces byte-exact, gloss paren-free <=15 parts no grammar words, Q>=5 words
verse-owned, premises >=3 words).
"""
from __future__ import annotations
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "process" / "beam" / "runs"
SONG = "tal-a06"

V: dict[int, dict] = {
97: {
 "g": [
  ("evaṃ", "thus", "indecl adverb; resumes prior count"),
  ("kalāḥ", "digits", "f.nom.pl kalā; lunar digits"),
  ("pañcadaśa", "fifteen", "numeral in compound sense; agrees with digits"),
  ("kṣīyante", "are-consumed", "3pl.pres.pass √kṣi; passive of wasting"),
  ("śaśinaḥ", "of-the-moon", "gen.sg.m śaśin; moon's digits"),
  ("kramāt", "in-order", "abl.sg; sequential consumption"),
  ("āpyāyinyamṛtābrūpatādātmyātṣoḍaśī", "sixteenth-by-nourishing-immortal-nature-identity", "nom.sg.f long compound; the sixteenth is amṛta-natured, not consumed"),
  ("na", "not", "indecl negation"),
  ("tu", "but", "indecl particle; contrast with prior"),
 ],
 "m": [
  ("evaṃ", "indecl.", "adverb of manner"),
  ("kalāḥ", "f.nom.pl", "subject: lunar digits"),
  ("pañcadaśa", "numeral", "attributive fifteen"),
  ("kṣīyante", "3pl.pres.pass √kṣi", "passive: are worn away"),
  ("śaśinaḥ", "gen.sg.m", "possessor: of the moon"),
  ("kramāt", "abl.sg", "source/sequence: by stages"),
  ("āpyāyinyamṛtābrūpatādātmyātṣoḍaśī", "nom.sg.f (compound)", "the sixteenth; identity with nourishing-immortal form"),
  ("na", "indecl.", "negation"),
  ("tu", "indecl.", "contrast particle"),
 ],
 "a": {
  "question": "Which lunar digit is not consumed when the fifteen waste away?",
  "premises": [
   "The fifteen digits of the moon are consumed in order",
   "The sixteenth stands in identity with nourishing immortal form",
   "That sixteenth alone is not worn away"],
  "inference": "Fifteen digits waste; the sixteenth amṛta-digit endures.",
  "uncertainties": ["compound segmentation of the long sixteenth-word approximate"],
  "plain_english": "Thus the fifteen digits of the moon are consumed in order; the sixteenth, identical with nourishing immortal form, is not consumed.",
 },
},
98: {
 "g": [
  ("tatra", "there", "indecl locative; at that juncture"),
  ("pañcadaśī", "fifteen-digit-portion", "nom.sg.f; the fifteen-digit span"),
  ("yāsau", "which-that", "nom.sg.f relative; identifies the portion"),
  ("tuṭiḥ", "moment-fraction", "nom.sg.f; tuṭi measure of breath-time"),
  ("prakṣīṇacandramāḥ", "with-moon-waned", "nom.sg.m compound; moon past its wane"),
  ("tadūrdhvagaṃ", "its-upper-going", "acc.sg.n? or nom; upper reach of the tuṭi"),
  ("yattuṭyardhaṃ", "which-tuti-half", "nom.sg.n relative compound; the half-tuti"),
  ("pakṣasaṃdhiḥ", "fortnight-juncture", "nom.sg.m compound; boundary of the paksa"),
  ("sa", "that", "nom.sg.m; agrees with juncture"),
  ("kīrtitaḥ", "is-called", "nom.sg.m ppp √kīrt; passivedenomination"),
 ],
 "m": [
  ("tatra", "indecl.", "locative sense: there"),
  ("pañcadaśī", "nom.sg.f", "the fifteen-digit span"),
  ("yāsau", "nom.sg.f (rel.)", "which; deictic yad + sa"),
  ("tuṭiḥ", "nom.sg.f", "moment-fraction measure"),
  ("prakṣīṇacandramāḥ", "nom.sg.m (compound)", "moon in its waned state"),
  ("tadūrdhvagaṃ", "nom.sg.n / acc", "upper reach of that fraction"),
  ("yattuṭyardhaṃ", "nom.sg.n (rel. compound)", "the half of the tuṭi"),
  ("pakṣasaṃdhiḥ", "nom.sg.m", "fortnight-juncture"),
  ("sa", "nom.sg.m", "demonstrative: that"),
  ("kīrtitaḥ", "nom.sg.m ppp √kīrt", "is said to be"),
 ],
 "a": {
  "question": "What is called the fortnight-juncture of the waned moon?",
  "premises": [
   "There the fifteen-digit portion is the tuṭi of the waned moon",
   "The upper going of that tuṭi is its half",
   "That half-tuti is named the fortnight-juncture"],
  "inference": "The upper half of the waned moon's tuṭi is the pakṣa-sandhi.",
  "uncertainties": [],
  "plain_english": "There the fifteen-digit portion is the tuṭi of the waned moon; its upper half is called the fortnight-juncture.",
 },
},
99: {
 "g": [
  ("tasmādviśramatuṭyardhādāmāvasyaṃ", "therefore-from-rest-in-tuti-half-new-moon", "abl.sg long compound; from the rest in the half-tuti at new moon"),
  ("purādalam", "prior-half", "acc.sg.n compound puraḥ + ardha; the first half"),
  ("paraṃ", "supreme", "acc.sg.n adj; modifies prātipada"),
  ("prātipadaṃ", "on-pratipada-day", "acc.sg.n tithi name; new-moon fortnight day"),
  ("cārdhamiti", "and-half-thus", "indecl + acc; cā + ardham + iti formula"),
  ("saṃdhiḥ", "juncture", "nom.sg.m; the sandhi under definition"),
  ("sa", "that", "nom.sg.m; agrees with juncture"),
  ("kalpyate", "is-posed", "3sg.pres.pass √kḷp; postulated"),
 ],
 "m": [
  ("tasmādviśramatuṭyardhādāmāvasyaṃ", "abl.sg (compound)", "from rest in the half-tuti at new moon"),
  ("purādalam", "acc.sg.n", "prior half; object of the juncture"),
  ("paraṃ", "acc.sg.n adj", "supreme; modifies pratipada"),
  ("prātipadaṃ", "acc.sg.n", "the pratipada tithi"),
  ("cārdhamiti", "indecl.", "and-half-thus; formulaic"),
  ("saṃdhiḥ", "nom.sg.m", "subject: the juncture"),
  ("sa", "nom.sg.m", "demonstrative"),
  ("kalpyate", "3sg.pres.pass √kḷp", "is postulated"),
 ],
 "a": {
  "question": "What juncture is posited from the half-tuti rest at new moon?",
  "premises": [
   "From rest in the half-tuti at new moon the prior half is taken",
   "The supreme pratipada day enters the formula with the other half",
   "That juncture of halves is therefore postulated"],
  "inference": "Half-tuti rest plus pratipada posits the new-moon juncture.",
  "uncertainties": ["whether puraḥ-ardha is strictly the prior half of the day or of the tuṭi"],
  "plain_english": "Therefore from rest in the half-tuti at new moon, the prior half, the supreme pratipada, and the other half — that juncture is posited.",
 },
},
100: {
 "g": [
  ("tatra", "there", "indecl locative"),
  ("prātipade", "on-pratipada", "loc.sg.n; locative of the tithi"),
  ("tasmiṃstuṭyardhārdhe", "in-that-tuti-half-prior-half", "loc.sg.n long; locative compound of the half-tuti"),
  ("purādalam", "prior-half", "acc.sg.n; new-moon prior half"),
  ("āmāvasyaṃ", "new-moon", "acc.sg.n; amāvāsyā tithi"),
  ("tithicchedātkuryātsūryagrahaṃ", "by-lunar-day-cut-one-should-do-solar-eclipse", "abl + 3sg.opt; by tithi-cut one performs graha entry"),
  ("viśat", "enter", "3sg.pres.act √viś; imperative force with kuryāt"),
 ],
 "m": [
  ("tatra", "indecl.", "locative"),
  ("prātipade", "loc.sg.n", "on the pratipada"),
  ("tasmiṃstuṭyardhārdhe", "loc.sg.n (compound)", "in that half-tuti prior-half"),
  ("purādalam", "acc.sg.n", "prior half object"),
  ("āmāvasyaṃ", "acc.sg.n", "new-moon day"),
  ("tithicchedātkuryātsūryagrahaṃ", "abl + 3sg.opt + acc", "by lunar-day-cut one should perform solar eclipse"),
  ("viśat", "3sg.pres.act √viś", "enter; with optative force"),
 ],
 "a": {
  "question": "What rite does one enter on pratipada by lunar-day-cut?",
  "premises": [
   "On pratipada, in that prior half of the half-tuti",
   "The new-moon day is taken with the prior half",
   "By lunar-day-cut one performs and enters the solar eclipse"],
  "inference": "Lunar-day-cut on new-moon pratipada opens solar-eclipse entry.",
  "uncertainties": ["exact ritual force of viśat as enter vs perform"],
  "plain_english": "There on pratipada, that prior half of the half-tuti being new-moon, by lunar-day-cut one performs and enters the solar eclipse.",
 },
},
101: {
 "g": [
  ("tatrārkamaṇḍale", "there-in-solar-disc", "loc.sg.n compound; in the sun's mandala"),
  ("līnaḥ", "dissolved", "nom.sg.m ppp √lī; moon dissolved in sun"),
  ("śaśī", "moon", "nom.sg.m; subject dissolving"),
  ("sravati", "drips", "3sg.pres.act √sru; flows out honey"),
  ("yanmadhu", "whose-honey", "acc.sg.n relative; madhu of the moon"),
  ("taptatvāttatpibedindusahabhūḥ", "having-been-heated-that-should-drink-sun-companion", "abs + 3sg.opt; after heating the sun-companion drinks it"),
  ("siṃhikāsutaḥ", "son-of-Simhika", "nom.sg.m; Rahu, son of Simhika"),
 ],
 "m": [
  ("tatrārkamaṇḍale", "loc.sg.n (compound)", "in the solar disc"),
  ("līnaḥ", "nom.sg.m ppp √lī", "having dissolved"),
  ("śaśī", "nom.sg.m", "subject: the moon"),
  ("sravati", "3sg.pres.act √sru", "drips / flows"),
  ("yanmadhu", "acc.sg.n (rel.)", "whose honey; object of dripping"),
  ("taptatvāttatpibedindusahabhūḥ", "abs + 3sg.opt", "once heated, that the sun-companion should drink"),
  ("siṃhikāsutaḥ", "nom.sg.m", "Rahu as son of Simhika"),
 ],
 "a": {
  "question": "Who drinks the moon's honey once it dissolves in the solar disc?",
  "premises": [
   "There in the solar disc the moon dissolves",
   "The dissolved moon drips its honey",
   "Once heated, the sun-companion — Simhika's son — drinks it"],
  "inference": "Rahu as sun's companion drinks the honey of the dissolved moon.",
  "uncertainties": ["whether madhu is nectar-of-moon or simply the moon's sap"],
  "plain_english": "There in the solar disc the moon, dissolved, drips its honey; once heated, the sun-companion — Simhika's son — drinks that honey.",
 },
},
102: {
 "g": [
  ("arkaḥ", "sun", "nom.sg.m; the solar graha as measure"),
  ("pramāṇaṃ", "measure", "acc.sg.n; standard of measuring"),
  ("somastu", "moon-but", "nom.sg.m + tu; the moon as measurable"),
  ("meyaṃ", "measurable", "acc.sg.n ppp √mā; what is measured"),
  ("jñānakriyātmakau", "knowledge-action-natured-pair", "nom.dv.n long compound; sun and moon as jnana-kriya"),
  ("rāhurmāyāpramātā", "Rahu-maya-observer", "nom.sg.m compound; Rahu as maya-pramata"),
  ("syāttadācchādanakovidaḥ", "would-be-that-covering-skilled", "3sg.opt + nom; skilled at covering them"),
 ],
 "m": [
  ("arkaḥ", "nom.sg.m", "sun; subject"),
  ("pramāṇaṃ", "acc.sg.n", "measure; object of solar role"),
  ("somastu", "nom.sg.m + particle", "moon but; contrast"),
  ("meyaṃ", "acc.sg.n ppp √mā", "the measurable"),
  ("jñānakriyātmakau", "nom.dv.n (compound)", "both as knowledge-action-natured"),
  ("rāhurmāyāpramātā", "nom.sg.m (compound)", "Rahu as observer of maya"),
  ("syāttadācchādanakovidaḥ", "3sg.opt √as + nom", "would be skilled at covering that"),
 ],
 "a": {
  "question": "How do sun as measure and moon as measurable relate under Rahu?",
  "premises": [
   "The sun is the measure, the moon the measurable",
   "Both are knowledge-and-action in nature",
   "Rahu the maya-observer is skilled at covering them"],
  "inference": "Sun measures, moon is measured; Rahu covers both as maya-pramata.",
  "uncertainties": ["jnanakriyatmakau taken as dual referring to sun and moon together"],
  "plain_english": "The sun is the measure, the moon the measurable, both knowledge-and-action-natured; Rahu the maya-observer is skilled at covering them.",
 },
},
103: {
 "g": [
  ("tata", "thence", "indecl ablative; from that conjunction"),
  ("eva", "indeed", "indecl emphatic"),
  ("tamorūpo", "darkness-natured", "nom.sg.m compound; Rahu's nature"),
  ("vilāpayitumakṣamaḥ", "to-melt-unable", "inf + nom; incapable of melting them"),
  ("tatsaṃghaṭṭādvayollāso", "from-clash-of-two-union", "abl.sg long; from the conjunction of the two"),
  ("mukhyo", "primary", "nom.sg.m; chief agent"),
  ("mātā", "measurer", "nom.sg.f; the matr principle"),
  ("vilāpakaḥ", "melter", "nom.sg.m agent noun; one who dissolves"),
 ],
 "m": [
  ("tata", "indecl.", "ablative: from that"),
  ("eva", "indecl.", "emphatic"),
  ("tamorūpo", "nom.sg.m (compound)", "darkness-natured: Rahu"),
  ("vilāpayitumakṣamaḥ", "inf + nom.sg.m", "unable to melt"),
  ("tatsaṃghaṭṭādvayollāso", "abl.sg (compound)", "from the clash-union of the two"),
  ("mukhyo", "nom.sg.m", "primary; agrees with mata"),
  ("mātā", "nom.sg.f", "the measurer"),
  ("vilāpakaḥ", "nom.sg.m", "the melter; agent noun"),
 ],
 "a": {
  "question": "Who melts the pair when darkness-natured Rahu cannot?",
  "premises": [
   "Thence the darkness-natured one is unable to melt them",
   "From the clash-union of the two a primary agent arises",
   "That measurer is the melter"],
  "inference": "From sun-moon-Rahu clash the primary mata becomes the melter.",
  "uncertainties": ["identity of mukhya mata left open — maya-power or ritual measurer"],
  "plain_english": "From that clash, the darkness-natured one cannot melt them; from the union of the two, the primary measurer is the melter.",
 },
},
104: {
 "g": [
  ("arkendurāhusaṃghaṭṭāt", "from-clash-of-sun-moon-Rahu", "abl.sg long compound; triple conjunction"),
  ("pramāṇaṃ", "measure", "acc.sg.n; standard"),
  ("vedyavedakau", "knowable-knower-pair", "nom.dv.n; the two as object and subject"),
  ("advayena", "by-non-duality", "instr.sg; as non-dual"),
  ("tatastena", "thence-thereby", "indecl abl + instr; because of that"),
  ("puṇya", "meritorious", "nom.sg.n; result is punya"),
  ("eṣa", "this", "nom.sg.m; agrees with graha"),
  ("mahāgrahaḥ", "great-graha", "nom.sg.m; the eclipse as maha-graha"),
 ],
 "m": [
  ("arkendurāhusaṃghaṭṭāt", "abl.sg (compound)", "from the triple clash"),
  ("pramāṇaṃ", "acc.sg.n", "measure; object"),
  ("vedyavedakau", "nom.dv.n", "knowable and knower as dual"),
  ("advayena", "instr.sg", "by non-duality; instrument"),
  ("tatastena", "indecl. (abl+instr)", "from that / thereby"),
  ("puṇya", "nom.sg.n", "meritorious result"),
  ("eṣa", "nom.sg.m", "this; deictic"),
  ("mahāgrahaḥ", "nom.sg.m", "the great graha / eclipse"),
 ],
 "a": {
  "question": "Why is the triple clash of sun moon and Rahu meritorious?",
  "premises": [
   "From the clash of sun, moon and Rahu comes measure",
   "Knowable and knower stand as non-dual there",
   "Therefore this great graha is meritorious"],
  "inference": "Non-dual knower-known in the eclipse makes the graha punya.",
  "uncertainties": [],
  "plain_english": "From the clash of sun, moon and Rahu: measure, knowable and knower as non-dual — therefore this great graha is meritorious.",
 },
},
105: {
 "g": [
  ("amāvasyāṃ", "on-new-moon", "loc.sg.f; amāvāsyā tithi"),
  ("vināpyeṣa", "even-without-this", "indecl prep + nom; even so this"),
  ("saṃghaṭṭaścenmahāgrahaḥ", "clash-if-great-graha", "nom.sg.m conditional; if clash, a maha-graha"),
  ("yathārke", "as-when-sun", "loc.sg.m comparative; as at solar position"),
  ("meṣage", "in-Aries", "loc.sg.m; Mesha rasi"),
  ("rāhāvaśvinīsthe@śvinīdine", "Rahu-in-Asvini-on-Asvini-day", "loc compound with @; Rahu in Asvini on an Asvini day"),
 ],
 "m": [
  ("amāvasyāṃ", "loc.sg.f", "on new-moon day"),
  ("vināpyeṣa", "indecl. + nom.sg.m", "even so this one"),
  ("saṃghaṭṭaścenmahāgrahaḥ", "nom.sg.m + cond.", "if clash, a great graha"),
  ("yathārke", "loc.sg.m (comp.)", "as when sun [stands]"),
  ("meṣage", "loc.sg.m", "in Aries"),
  ("rāhāvaśvinīsthe@śvinīdine", "loc.sg.m + loc.sg.m", "Rahu in Asvini on Asvini day"),
 ],
 "a": {
  "question": "When does a clash without new-moon still count as great graha?",
  "premises": [
   "Even without new-moon a clash may be a great graha",
   "As when the sun stands in Aries",
   "And Rahu in Asvini on an Asvini day"],
  "inference": "Rahu in Asvini with sun in Aries makes eclipse-class clash.",
  "uncertainties": ["whether vinapi marks absence of amāvāsyā or mere concession"],
  "plain_english": "Even without new-moon this clash is a great graha — as when the sun is in Aries and Rahu in Asvini on an Asvini day.",
 },
},
106: {
 "g": [
  ("āmāvāsyaṃ", "new-moon", "acc.sg.n; the amāvāsyā condition"),
  ("yadā", "when", "indecl relative; temporal clause"),
  ("tvardhaṃ", "half-its", "acc.sg.n + poss; the half of it"),
  ("līnaṃ", "dissolved", "acc.sg.n ppp √lī; dissolved state"),
  ("prātipade", "on-pratipada", "loc.sg.n; locative"),
  ("dale", "in-half", "loc.sg.n; in the dala / half"),
  ("pratipacca", "and-pratipadi", "indecl + nom; and the pratipadi tithi"),
  ("viśuddhā", "fully-pure", "nom.sg.f ppp; pure state"),
  ("syāttanmokṣo", "would-be-that-liberation", "3sg.opt + nom; that is moksa"),
  ("dūrage", "in-distant-rite", "loc.sg.m; distant observance"),
  ("vidhau", "in-rite", "loc.sg.m; in the vidhi"),
 ],
 "m": [
  ("āmāvāsyaṃ", "acc.sg.n", "new-moon as object"),
  ("yadā", "indecl.", "when"),
  ("tvardhaṃ", "acc.sg.n", "its half"),
  ("līnaṃ", "acc.sg.n ppp √lī", "dissolved"),
  ("prātipade", "loc.sg.n", "on pratipada"),
  ("dale", "loc.sg.n", "in the half"),
  ("pratipacca", "indecl. + nom.sg.f", "and the pratipadi"),
  ("viśuddhā", "nom.sg.f ppp", "fully pure"),
  ("syāttanmokṣo", "3sg.opt √as + nom.sg.m", "that would be liberation"),
  ("dūrage", "loc.sg.m", "in the distant rite"),
  ("vidhau", "loc.sg.m", "in the observance"),
 ],
 "a": {
  "question": "When does the dissolved half at new-moon become liberation?",
  "premises": [
   "When new-moon's half is dissolved on pratipada",
   "In that half the pratipadi stands fully pure",
   "In the distant rite that state is called liberation"],
  "inference": "Pure pratipadi half at new-moon is moksha in the distant rite.",
  "uncertainties": ["dūra-ga taken as distant-rite locus, not merely far-off"],
  "plain_english": "When on new-moon the half is dissolved in the half of pratipada and the pratipadi is fully pure — that is liberation in the distant rite.",
 },
},
107: {
 "g": [
  ("grāsamokṣāntare", "between-eclipse-and-liberation", "loc.sg.n compound; the interval"),
  ("snānadhyānahomajapādikam", "bathing-meditation-homa-japa-etc", "acc.sg.n long compound; the ritual set"),
  ("laukikālaukikaṃ", "worldly-and-otherworldly", "acc.sg.n dvandva; both classes"),
  ("bhūyaḥphalaṃ", "further-fruit", "acc.sg.n; further result"),
  ("syātpāralaukikam", "would-be-beyond-worldly", "3sg.opt + acc; becomes para-laukika"),
 ],
 "m": [
  ("grāsamokṣāntare", "loc.sg.n (compound)", "between eclipse and liberation"),
  ("snānadhyānahomajapādikam", "acc.sg.n (compound)", "bathing etc. as object"),
  ("laukikālaukikaṃ", "acc.sg.n (dvandva)", "worldly and unworldly pair"),
  ("bhūyaḥphalaṃ", "acc.sg.n", "further fruit"),
  ("syātpāralaukikam", "3sg.opt √as + acc.sg.n", "would become beyond-worldly"),
 ],
 "a": {
  "question": "What fruit follows the rites between eclipse and liberation?",
  "premises": [
   "Between eclipse and liberation stands the ritual set",
   "Bathing meditation homa japa and the rest, worldly and unworldly",
   "Their further fruit becomes beyond-worldly"],
  "inference": "Eclipse-interval rites lift worldly fruit to para-laukika.",
  "uncertainties": [],
  "plain_english": "Between eclipse and liberation: bathing, meditation, homa, japa and the rest — worldly and unworldly — their further fruit becomes beyond-worldly.",
 },
},
108: {
 "g": [
  ("grāsyagrāsakatākṣobhaprakṣaye", "in-dissolution-of-eclipsed-eclipsor-disturbance", "loc.sg.n long compound; moment of eclipse-possessed and possessor disturbance"),
  ("kṣaṇamāviśan", "entering-the-moment", "acc.sg.m + 3pl.pres.act √viś; entering that instant"),
  ("mokṣabhāgdhyānapūjādi", "liberation-share-meditation-worship-etc", "acc.sg.n compound; the moksa-bhaga practices"),
  ("kurvaṃścandrārkayorgrahe", "doing-at-moon-sun-eclipse", "3pl.pres.act + loc; performing at the candra-arka graha"),
 ],
 "m": [
  ("grāsyagrāsakatākṣobhaprakṣaye", "loc.sg.n (compound)", "in the dissolution of the disturbance"),
  ("kṣaṇamāviśan", "acc.sg.m + 3pl.pres.act", "entering the moment"),
  ("mokṣabhāgdhyānapūjādi", "acc.sg.n (compound)", "liberation-share meditation-worship etc."),
  ("kurvaṃścandrārkayorgrahe", "3pl.pres.act + loc.sg.n", "doing at the moon-sun eclipse"),
 ],
 "a": {
  "question": "What practices enter the moment at the moon-sun eclipse?",
  "premises": [
   "Entering the moment when eclipsed and eclipsor dissolve",
   "One performs liberation-share meditation and worship",
   "All at the graha of moon and sun"],
  "inference": "At eclipse-moment dissolution the liberation-share rites are done.",
  "uncertainties": ["moksa-bhaga as share-of-liberation vs portion-of-liberation"],
  "plain_english": "Entering the moment of dissolution of the eclipsed and eclipsor disturbance, one performs liberation-share meditation, worship and the rest at the moon-sun eclipse.",
 },
},
}

n = 0
for v, d in V.items():
    assert d["a"]["question"].endswith("?") and len(d["a"]["question"].split()) >= 5, v
    assert all(len(p.split()) >= 3 for p in d["a"]["premises"]), v
    assert len(d["a"]["plain_english"].split()) >= 4, v
    lq = d["a"]["question"].lower()
    assert "does verse" not in lq and "this verse" not in lq and "is being told" not in lq, v
    for sub, rows, keys in (("gloss", d["g"], ("surface", "gloss", "grounds")),
                            ("cm", d["m"], ("lemma", "morph", "grounds"))):
        for r in rows:
            assert len(r) == 3 and all(s.strip() for s in r), (v, sub, r)
            if sub == "gloss":
                assert "(" not in r[1] and ")" not in r[1] and '"' not in r[1], (v, r)
                assert len(r[1].split("-")) <= 15, (v, r)
                LEAK = ("genitive", "nominative", "accusative", "instrumental", "dative",
                        "ablative", "locative", "vocative", "singular", "plural", "dual",
                        "participle", "passive", "causative", "optative", "imperative",
                        "sandhi", "compound")
                assert not any(w in r[1].lower().split("-") for w in LEAK), (v, r)
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
print(f"wrote {n} files (vv97-108 gloss+cm+am)")
