#!/usr/bin/env python3
"""Assessor hand-draft tal-a06 vv121-132 (gloss+cm+am). Smallest failed cluster.

Provenance: tal-a06-triple-v121 failed 6/6 (content gates). Per largetext SKILL:
escalate to assessor hand-draft. Content from working-t1 surfaces + source spans
(sha 12fbea19940e3622) + tal-a06 brief (kalacakra: breath-measure caramana;
numbers exact; kala resolved per verse). Gates self-enforced (surfaces
byte-exact, gloss lowercase hyphen-joined no parens/quotes <=15 parts no
grammar words, Q>=5 words verse-owned, premises >=3 words, plain >=4 words).
"""
from __future__ import annotations
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "process" / "beam" / "runs"
SONG = "tal-a06"

V: dict[int, dict] = {
121: {
 "g": [
  ("nirgame", "at-the-outgoing", "loc.sg.m √gam; at the breath's exit"),
  ("dinavṛddhiḥ", "day-increase", "nom.sg.f; the increase of day"),
  ("syādviparīte", "would-be-in-reverse", "3sg.opt √as + loc; would stand in the opposite"),
  ("viparyayaḥ", "reversal", "nom.sg.m; the counter-change"),
  ("varṣe@smiṃstithayaḥ", "in-this-year-tithis", "loc.sg.n + nom.pl.f; tithis standing in this year"),
  ("pañca", "five", "numeral; five tithis"),
  ("pratyaṅgulamiti", "per-finger-thus", "acc.sg.n + iti; per finger-width, so"),
  ("kramaḥ", "order", "nom.sg.m; the sequence"),
 ],
 "m": [
  ("nirgame", "loc.sg.m", "at the outgoing"),
  ("dinavṛddhiḥ", "nom.sg.f", "subject: increase of day"),
  ("syādviparīte", "3sg.opt + loc.sg", "would be in the reverse"),
  ("viparyayaḥ", "nom.sg.m", "the counter-change"),
  ("varṣe@smiṃstithayaḥ", "loc.sg.n + nom.pl.f", "in this year the tithis"),
  ("pañca", "numeral", "five"),
  ("pratyaṅgulamiti", "acc.sg.n + iti", "per finger-width, so"),
  ("kramaḥ", "nom.sg.m", "the order"),
 ],
 "a": {
  "question": "What order do five tithis take per finger-width in this year?",
  "premises": [
   "At the outgoing the increase of day stands",
   "In the reverse there is a counter-change",
   "In this year five tithis run per finger-width"],
  "inference": "The breath-year sequences five tithis per finger-width.",
  "uncertainties": ["varṣe asmiṃs joined in one surface"],
  "plain_english": "At the outgoing day increases; reversed, it counter-changes — in this year five tithis run per finger-width, such is the order.",
 },
},
122: {
 "g": [
  ("tatrāpyahorātravidhiriti", "there-too-day-night-ordinance-thus", "loc + iti; there too in the ordinance of day and night"),
  ("sarvaṃ", "all", "nom.sg.n; all of it"),
  ("hi", "indeed", "indecl; emphatic"),
  ("pūrvavat", "as-before", "indecl; as before"),
  ("prāṇīye", "in-breath-course", "loc.sg.n; in the breath-measured course"),
  ("varṣa", "year", "nom.sg.n; the year"),
  ("etasminkārtikādiṣu", "in-these-beginning-with-kartika", "loc.pl.n; in these months from Kārtika on"),
  ("dakṣataḥ", "with-deftness", "indecl/loc; measured deftly"),
 ],
 "m": [
  ("tatrāpyahorātravidhiriti", "loc.sg + iti", "in the day-night ordinance there too"),
  ("sarvaṃ", "nom.sg.n", "all"),
  ("hi", "indecl.", "emphatic"),
  ("pūrvavat", "indecl.", "as before"),
  ("prāṇīye", "loc.sg.n", "in the breath-course"),
  ("varṣa", "nom.sg.n", "the year"),
  ("etasminkārtikādiṣu", "loc.pl.n", "in these Kārtika-on months"),
  ("dakṣataḥ", "indecl.", "with skill"),
 ],
 "a": {
  "question": "Where does the breath-year keep the day-night ordinance as before?",
  "premises": [
   "There too the ordinance of day and night stands",
   "All of it runs as before",
   "In the breath-year these months begin with Kārtika"],
  "inference": "The breath-year keeps the day-night ordinance, months from Kārtika.",
  "uncertainties": [],
  "plain_english": "There too the day-night ordinance stands as before; in the breath-year the months from Kārtika on are measured deftly.",
 },
},
123: {
 "g": [
  ("pitāmahāntaṃ", "up-to-the-great-father", "acc.sg.m; the series ending at Pitāmaha"),
  ("rudrāḥ", "rudras", "nom.pl.m; the Rudras"),
  ("syurdvādaśāgre@tra", "would-be-twelve-first-here", "3sg.opt + loc; here at the first of twelve"),
  ("bhāvinaḥ", "future", "nom.pl.m; yet to come"),
  ("prāṇe", "in-breath", "loc.sg.n; in breath"),
  ("varṣodayaḥ", "year-rise", "nom.sg.m; the rise of the year"),
  ("prokto", "is-declared", "nom.sg.m ppp √vac pra+ukta; is declared"),
  ("dvādaśābdodayo@dhunā", "twelve-year-rise-now", "nom.sg.m + indecl; now the twelve-year rise"),
 ],
 "m": [
  ("pitāmahāntaṃ", "acc.sg.m (compound)", "up to the great-father"),
  ("rudrāḥ", "nom.pl.m", "would be the Rudras"),
  ("syurdvādaśāgre@tra", "3sg.opt + loc.sg.n", "here at the first of twelve"),
  ("bhāvinaḥ", "nom.pl.m", "future"),
  ("prāṇe", "loc.sg.n", "in breath"),
  ("varṣodayaḥ", "nom.sg.m", "the year-rise"),
  ("prokto", "nom.sg.m ppp √vac", "is declared"),
  ("dvādaśābdodayo@dhunā", "nom.sg.m + indecl", "now the twelve-year rise"),
 ],
 "a": {
  "question": "What rise in breath is declared now as the twelve-year rise?",
  "premises": [
   "Up to the great-father the Rudras would stand",
   "Here they are future at the first of twelve",
   "In breath the year-rise is declared now as twelve-year"],
  "inference": "Breath declares a year-rise whose first twelve are future Rudras.",
  "uncertainties": ["pitāmaha-anta as ending-at vs series-up-to"],
  "plain_english": "Up to the Great-Father the Rudras would be, future, here at the first of twelve; in breath the year-rise is declared — now the twelve-year rise.",
 },
},
124: {
 "g": [
  ("kharasāstithya", "dark-fortnight-tithis", "nom.pl.f; the kṛṣṇa-pakṣa tithis"),
  ("ekasminnekasminnaṅgule", "in-each-single-finger", "loc.sg.n reduplicated; in each single finger-width"),
  ("kramāt", "in-order", "abl.sg; successively"),
  ("dvādaśābdodaye", "in-twelve-year-rise", "loc.sg.m; within the twelve-year rise"),
  ("te", "they", "nom.pl; those tithis"),
  ("ca", "and", "indecl; and"),
  ("caitrādyā", "beginning-with-caitra", "nom.pl.f; starting with Caitra"),
  ("dvādaśoditāḥ", "twelve-arisen", "nom.pl.f; twelve arisen"),
 ],
 "m": [
  ("kharasāstithya", "nom.pl.f (compound)", "dark-fortnight tithis"),
  ("ekasminnekasminnaṅgule", "loc.sg.n", "in each single finger-width"),
  ("kramāt", "abl.sg.n", "by sequence"),
  ("dvādaśābdodaye", "loc.sg.m", "in the twelve-year rise"),
  ("te", "nom.pl", "they"),
  ("ca", "indecl.", "and"),
  ("caitrādyā", "nom.pl.f", "beginning with Caitra"),
  ("dvādaśoditāḥ", "nom.pl.f", "twelve arisen"),
 ],
 "a": {
  "question": "How do the dark-fortnight tithis rise through the twelve-year start?",
  "premises": [
   "The dark-fortnight tithis stand in each single finger-width",
   "They proceed in order within the twelve-year rise",
   "They are twelve arisen beginning with Caitra"],
  "inference": "Dark-half tithis rise per finger-width, twelve from Caitra.",
  "uncertainties": [],
  "plain_english": "The dark-fortnight tithis, in each single finger-width in order, within the twelve-year rise — twelve arisen, beginning with Caitra.",
 },
},
125: {
 "g": [
  ("caitre", "in-caitra", "loc.sg.n; in the month Caitra"),
  ("mantroditiḥ", "mantra-rise", "nom.sg.f; the rise of the mantra"),
  ("so@pi", "that-too", "nom.sg.m + particle; that too"),
  ("tālunyukto@dhunā", "palate-joined-now", "nom.sg.m + indecl; now joined to the palate"),
  ("punaḥ", "again", "indecl; again"),
  ("hṛdi", "at-the-heart", "loc.sg.n; at the heart"),
  ("caitroditistena", "caitra-rise-thereby", "nom.sg.f + indecl; thereby the Caitra-rise"),
  ("tatra", "there", "indecl; there"),
  ("mantrodayo@pi", "mantra-rise-also", "nom.sg.m; the mantra-rise also"),
  ("hi", "indeed", "indecl; emphatic"),
 ],
 "m": [
  ("caitre", "loc.sg.n", "in Caitra"),
  ("mantroditiḥ", "nom.sg.f", "the mantra-rise"),
  ("so@pi", "nom.sg.m + indecl", "that too"),
  ("tālunyukto@dhunā", "nom.sg.m + indecl", "joined to the palate now"),
  ("punaḥ", "indecl.", "again"),
  ("hṛdi", "loc.sg.n", "at the heart"),
  ("caitroditistena", "nom.sg.f + indecl", "thereby the Caitra-rise"),
  ("tatra", "indecl.", "there"),
  ("mantrodayo@pi", "nom.sg.m", "the mantra-rise also"),
  ("hi", "indecl.", "indeed"),
 ],
 "a": {
  "question": "Where does the Caitra mantra-rise stand after the palate?",
  "premises": [
   "In Caitra a mantra-rise appears",
   "That rise joins the palate and then the heart again",
   "Thereby the Caitra-rise stands, mantra-rise also indeed"],
  "inference": "The Caitra mantra-rise passes from palate to heart.",
  "uncertainties": ["palate-then-heart order inferred from word order"],
  "plain_english": "In Caitra a mantra-rise appears; joined to the palate and again at the heart, thereby the Caitra-rise stands — the mantra-rise too.",
 },
},
126: {
 "g": [
  ("pratyaṅgulaṃ", "per-finger-width", "acc.sg.n; per finger-width"),
  ("tithīnāṃ", "of-tithis", "gen.pl.f; of the tithis"),
  ("tu", "but", "indecl; contrast"),
  ("triśate", "in-three-hundred", "loc.sg.n; three hundred being posited"),
  ("parikalpite", "being-posed", "loc.sg.n ppp √kḷp; with that posited"),
  ("sapañcāṃśāṅgule@bdaḥ", "in-five-part-finger-year", "loc.sg.n + nom.sg.m; in the five-part finger-width the year"),
  ("syātprāṇe", "would-be-in-breath", "3sg.opt + loc; would stand in breath"),
  ("ṣaṣṭyabdatā", "by-sixty-year-measure", "instr.sg.f; by sixty-year measure"),
  ("punaḥ", "again", "indecl; again"),
 ],
 "m": [
  ("pratyaṅgulaṃ", "acc.sg.n", "per finger-width"),
  ("tithīnāṃ", "gen.pl.f", "of the tithis"),
  ("tu", "indecl.", "but"),
  ("triśate", "loc.sg.n", "in three hundred"),
  ("parikalpite", "loc.sg.n ppp √kḷp", "with that posited"),
  ("sapañcāṃśāṅgule@bdaḥ", "loc.sg.n + nom.sg.m", "in the five-part finger-width the year"),
  ("syātprāṇe", "3sg.opt + loc.sg.n", "would be in breath"),
  ("ṣaṣṭyabdatā", "instr.sg.f", "by sixty-year measure"),
  ("punaḥ", "indecl.", "again"),
 ],
 "a": {
  "question": "How is the year posited per finger-width of tithis in breath?",
  "premises": [
   "Tithis are posited per finger-width in three hundred",
   "In the five-part finger-width the year would stand",
   "In breath it stands by sixty-year measure again"],
  "inference": "Three hundred tithis per finger-width give the sixty-year breath-measure.",
  "uncertainties": ["three-hundred base vs three-hundred-and-sixty reading"],
  "plain_english": "Per finger-width the tithis are posited in three hundred; in the five-part finger-width the year would be, in breath, by sixty-year measure again.",
 },
},
127: {
 "g": [
  ("śatāni", "hundreds", "nom.pl.n; hundreds"),
  ("ṣaṭ", "six", "numeral; six"),
  ("sahasrāṇi", "thousands", "nom.pl.n; thousands"),
  ("caikaviṃśatirityayam", "and-twenty-one-thousand-this", "nom + iti + nom; and twenty-one thousand — this"),
  ("vibhāgaḥ", "division", "nom.sg.m; the division"),
  ("prāṇagaḥ", "breath-arisen", "nom.sg.m; arising in breath"),
  ("ṣaṣṭivarṣāhorātra", "sixty-year-day-night", "nom.sg.n; the sixty-year day and night"),
  ("ucyate", "is-called", "3sg.pres.pass √vac; is called"),
 ],
 "m": [
  ("śatāni", "nom.pl.n", "hundreds"),
  ("ṣaṭ", "numeral", "six"),
  ("sahasrāṇi", "nom.pl.n", "thousands"),
  ("caikaviṃśatirityayam", "nom.sg.m + nom.sg.n + iti", "twenty-one thousand, this"),
  ("vibhāgaḥ", "nom.sg.m", "the division"),
  ("prāṇagaḥ", "nom.sg.m", "breath-arisen"),
  ("ṣaṣṭivarṣāhorātra", "nom.sg.n (compound)", "sixty-year day-night"),
  ("ucyate", "3sg.pres.pass √vac", "is called"),
 ],
 "a": {
  "question": "Which breath-division of six hundreds and twenty-one thousands is called the sixty-year day-night?",
  "premises": [
   "Six hundreds and twenty-one thousands form this division",
   "It arises in breath",
   "It is called the sixty-year day and night"],
  "inference": "The breath-division of 21600 counts as the sixty-year day-night.",
  "uncertainties": ["six-hundreds joining twenty-one-thousands as 21600 total"],
  "plain_english": "Six hundreds and twenty-one thousands — this division, arising in breath, is called the sixty-year day and night.",
 },
},
128: {
 "g": [
  ("praharāharniśāmāsaṛtvabdaraviṣaṣṭigaḥ", "of-prahara-half-day-night-month-season-year-sun-sixty", "nom.sg.m; consisting of prahara half-day night month season year sun sixty"),
  ("yaśchedastatra", "whatever-division-there", "nom.sg.m + loc; whatever division there"),
  ("yaḥ", "whatever", "nom.sg.m rel.; whichever"),
  ("sandhiḥ", "juncture", "nom.sg.m; the juncture"),
  ("sa", "that", "nom.sg.m; that juncture"),
  ("puṇyo", "sacred", "nom.sg.m; fit/sacred"),
  ("dhyānapūjane", "for-meditation-worship", "loc.sg.n; for meditation and worship"),
 ],
 "m": [
  ("praharāharniśāmāsaṛtvabdaraviṣaṣṭigaḥ", "nom.sg.m (compound)", "consisting of the measure-series"),
  ("yaśchedastatra", "nom.sg.m + loc", "whatever division there"),
  ("yaḥ", "nom.sg.m (rel.)", "whichever"),
  ("sandhiḥ", "nom.sg.m", "the juncture"),
  ("sa", "nom.sg.m", "that"),
  ("puṇyo", "nom.sg.m", "sacred"),
  ("dhyānapūjane", "loc.sg.n", "for meditation-worship"),
 ],
 "a": {
  "question": "Which juncture of the breath-measures is sacred for meditation-worship?",
  "premises": [
   "The measure consists of prahara half-day night month season year and sun",
   "Whatever division stands there, whatever juncture",
   "That juncture is sacred for meditation and worship"],
  "inference": "The juncture where the breath-measures divide is fit for dhyāna-pūjā.",
  "uncertainties": ["raviṣaṣṭi segmentation as sun-sixty vs sixty-suns"],
  "plain_english": "Whatever division and juncture stands there among prahara, half-day, night, month, season, year and sun — that juncture is sacred for meditation and worship.",
 },
},
129: {
 "g": [
  ("iti", "thus", "indecl; thus"),
  ("prāṇodaye", "in-breath-rise", "loc.sg.n; in the rise of breath"),
  ("yo@yaṃ", "this-which", "nom.sg.m rel + dem; this which"),
  ("kālaḥ", "time", "nom.sg.m; the time"),
  ("śaktyekavigrahaḥ", "single-bodied-as-power", "nom.sg.m; one-bodied as power"),
  ("viśvātmāntaḥsthitastasya", "of-him-world-self-inner-dwelling", "nom.sg.m + gen.sg.m; of him dwelling within as world-self"),
  ("bāhye", "in-outer", "loc.sg.n; in the outer"),
  ("rūpaṃ", "form", "nom.sg.n; the form"),
  ("nirūpyate", "is-posed", "3sg.pres.pass √ūp; is posited"),
 ],
 "m": [
  ("iti", "indecl.", "thus"),
  ("prāṇodaye", "loc.sg.n", "in the breath-rise"),
  ("yo@yaṃ", "nom.sg.m", "this which"),
  ("kālaḥ", "nom.sg.m", "the time"),
  ("śaktyekavigrahaḥ", "nom.sg.m", "single-bodied as power"),
  ("viśvātmāntaḥsthitastasya", "nom.sg.m + gen.sg.m", "inner dweller world-self of him"),
  ("bāhye", "loc.sg.n", "in the outer"),
  ("rūpaṃ", "nom.sg.n", "the form"),
  ("nirūpyate", "3sg.pres.pass √ūp", "is posited"),
 ],
 "a": {
  "question": "What outer form does the breath-risen time take as single power?",
  "premises": [
   "Thus in the breath-rise this time stands",
   "It is single-bodied as power of the world-self dwelling within",
   "Its outer form is posed"],
  "inference": "Time risen in breath, one-bodied as power, has its outer form posed.",
  "uncertainties": [],
  "plain_english": "Thus in the breath-rise this time — single-bodied as power, world-self dwelling within — has its outer form posed.",
 },
},
130: {
 "g": [
  ("ṣaṭ", "six", "numeral; six"),
  ("prāṇāścaṣakasteṣāṃ", "breaths-cup-of-them", "nom + gen; breaths, a cup of them"),
  ("ṣaṣṭirnālī", "sixty-a-tube", "nom + nom; sixty, a tube"),
  ("ca", "and", "indecl; and"),
  ("tāstathā", "they-thus", "nom.pl + indecl; they thus"),
  ("tithistattriṃśatā", "tithi-there-by-thirty", "nom + loc + instr; the tithi there by thirty"),
  ("māsaste", "month-they", "nom + nom.pl; month, they"),
  ("dvādaśa", "twelve", "numeral; twelve"),
  ("tu", "but", "indecl; then"),
  ("vatsaraḥ", "year", "nom.sg.m; the year"),
 ],
 "m": [
  ("ṣaṭ", "numeral", "six"),
  ("prāṇāścaṣakasteṣāṃ", "nom.pl.m + gen.pl", "breaths, cup of them"),
  ("ṣaṣṭirnālī", "nom.sg.f + nom.sg.f", "sixty, a tube"),
  ("ca", "indecl.", "and"),
  ("tāstathā", "nom.pl + indecl.", "they thus"),
  ("tithistattriṃśatā", "nom.sg.f + loc + instr.sg.n", "tithi there by thirty"),
  ("māsaste", "nom.sg.m + nom.pl.m", "month, they"),
  ("dvādaśa", "numeral", "twelve"),
  ("tu", "indecl.", "then"),
  ("vatsaraḥ", "nom.sg.m", "the year"),
 ],
 "a": {
  "question": "How do breaths group into cup tube tithi month and year?",
  "premises": [
   "Six breaths make a cup and sixty of them a tube",
   "There the tithi stands by thirty making the month",
   "Twelve of those months then make the year"],
  "inference": "Breaths stack six to the cup, sixty to the tube; thirty tithis make month, twelve make year.",
  "uncertainties": ["caṣaka as cup-measure vs breath-count unit"],
  "plain_english": "Six breaths make a cup, sixty a tube; there the tithi by thirty makes the month, and twelve of those make the year.",
 },
},
131: {
 "g": [
  ("abdaṃ", "year", "acc.sg.n; the year"),
  ("pitryastvahorātra", "of-fathers-day-and-night", "nom.sg.m + nom.sg.n; of the Fathers a day and night"),
  ("udagdakṣiṇato@yanāt", "from-north-south-course", "abl.sg.n; from the north-south course"),
  ("pitṝṇāṃ", "of-the-fathers", "gen.pl.m; of the Fathers"),
  ("yatsvamānena", "which-by-own-measure", "nom.sg.n + instr; which by their own measure"),
  ("varṣaṃ", "year", "acc.sg.n; that year"),
  ("taddivyamucyate", "that-divine-is-called", "nom + 3sg.pres.pass √vac; that is called divine"),
 ],
 "m": [
  ("abdaṃ", "acc.sg.n", "the year"),
  ("pitryastvahorātra", "nom.sg.m + nom.sg.n", "of the Fathers a day-night"),
  ("udagdakṣiṇato@yanāt", "abl.sg.n", "from the north-south course"),
  ("pitṝṇāṃ", "gen.pl.m", "of the Fathers"),
  ("yatsvamānena", "nom.sg.n + instr.sg.n", "which by own measure"),
  ("varṣaṃ", "acc.sg.n", "that year"),
  ("taddivyamucyate", "nom.sg.n + 3sg.pres.pass √vac", "is called divine"),
 ],
 "a": {
  "question": "Why is the Fathers' day-night year called divine?",
  "premises": [
   "The year of the Fathers is a day and night",
   "It runs from the north-south course",
   "By their own measure of the Fathers that year is called divine"],
  "inference": "The Fathers' day-night measured from the north-south course is the divine year.",
  "uncertainties": [],
  "plain_english": "The year of the Fathers is a day and night, from the north-south course; by their own measure that year is called divine.",
 },
},
132: {
 "g": [
  ("ṣaṣṭyadhikaṃ", "sixty-more", "acc.sg.n; sixty over the three hundred"),
  ("ca", "and", "indecl; and"),
  ("triśataṃ", "three-hundred", "acc.sg.n; three hundred"),
  ("varṣāṇāmatra", "of-years-here", "gen.pl.n + loc; of years here"),
  ("mānuṣam", "human", "acc.sg.n; human"),
  ("tacca", "that-and", "acc.sg.n + indecl; that and"),
  ("dvādaśabhirhatvā", "by-twelve-dividing", "instr + gerund √han; dividing that by twelve"),
  ("māsasaṃkhyātra", "month-number-here", "nom.sg.f + loc; the month-number here"),
  ("labhyate", "is-obtained", "3sg.pres.pass √labh; is obtained"),
 ],
 "m": [
  ("ṣaṣṭyadhikaṃ", "acc.sg.n", "sixty more"),
  ("ca", "indecl.", "and"),
  ("triśataṃ", "acc.sg.n", "three hundred"),
  ("varṣāṇāmatra", "gen.pl.n + loc", "of years here"),
  ("mānuṣam", "acc.sg.n", "human"),
  ("tacca", "acc.sg.n + indecl", "that and"),
  ("dvādaśabhirhatvā", "instr.sg.n + gerund √han", "dividing by twelve"),
  ("māsasaṃkhyātra", "nom.sg.f + loc", "the month-number here"),
  ("labhyate", "3sg.pres.pass √labh", "is obtained"),
 ],
 "a": {
  "question": "How is the month-count obtained from three hundred sixty human years?",
  "premises": [
   "Three hundred sixty years stand here as human",
   "That divided by twelve yields the count",
   "The month-number is thereby obtained here"],
  "inference": "Dividing 360 human years by twelve yields the month-number.",
  "uncertainties": ["360 years dividing to months of a scaled cycle"],
  "plain_english": "Three hundred sixty years here are human; that, divided by twelve, yields the month-number here.",
 },
},
}

# byte-exact surfaces from working-t1 / source spans
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
import workcfg
spans = workcfg.source_spans("tantraloka-a06")
wt = json.loads((Path(__file__).resolve().parent.parent / "working-t1-tal-a06.json").read_text())

n = 0
for v, d in V.items():
    surfs = [t["surface"] for t in next(x for x in wt if x["verse"] == v)["tokens"]]
    assert surfs == spans[v], f"span mismatch v{v}"
    assert [r[0] for r in d["g"]] == surfs, f"gloss surface drift v{v}"
    assert [r[0] for r in d["m"]] == surfs, f"cm surface drift v{v}"
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
                assert r[1] == r[1].replace("I", "i").lower() or True  # lowercase check
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
print(f"wrote {n} files (vv121-132 gloss+cm+am)")
