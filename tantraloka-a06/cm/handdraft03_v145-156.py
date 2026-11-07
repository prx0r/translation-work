#!/usr/bin/env python3
"""Assessor hand-draft tal-a06 vv145-156 (gloss+cm+am). Smallest failed cluster.

Provenance: tal-a06-triple-v145 failed 6/6 (content gates). Per largetext SKILL:
escalate to assessor hand-draft. Content from working-t1 surfaces + source spans
(sha 12fbea19940e3622) + tal-a06 brief (kalacakra: cosmic cycles as breath-
phases; Viṣṇu/Rudra century ends; Śrīkaṇṭha dissolution; numbers exact).
Gates self-enforced (surfaces byte-exact, gloss lowercase hyphen-joined no
parens/quotes <=15 parts no grammar words, Q>=5 words verse-owned, premises
>=3 words, plain >=4 words).
"""
from __future__ import annotations
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "process" / "beam" / "runs"
SONG = "tal-a06"

V: dict[int, dict] = {
145: {
 "g": [
  ("niśākṣaye", "at-nights-end", "loc.sg.f niśā-kṣaya; at the decay of night"),
  ("punaḥ", "again", "indecl; renewed creation"),
  ("sṛṣṭiṃ", "creation", "acc.sg.f √sṛj; object made"),
  ("kurute", "makes", "3sg.pres.mid √kṛ; he effects"),
  ("tāmasāditaḥ", "begun-from-darkness", "nom.sg.m; origin in tamas"),
  ("svakavarṣaśatānte@sya", "at-his-own-hundred-years-end", "loc.sg.n compound + gen; at his own century-end"),
  ("kṣayastadvaiṣṇavaṃ", "destruction-that-vishnu-day", "nom.sg.m + acc; that ruin is the Vaiṣṇava day"),
  ("dinam", "day", "acc.sg.n; the day so named"),
 ],
 "m": [
  ("niśākṣaye", "loc.sg.f", "at night's ending"),
  ("punaḥ", "indecl.", "again"),
  ("sṛṣṭiṃ", "acc.sg.f", "object: creation"),
  ("kurute", "3sg.pres.mid √kṛ", "he makes"),
  ("tāmasāditaḥ", "nom.sg.m", "begun from darkness"),
  ("svakavarṣaśatānte@sya", "loc.sg.n + gen.sg", "at the end of his own hundred years"),
  ("kṣayastadvaiṣṇavaṃ", "nom.sg.m + acc.sg.n", "that destruction is the Vaiṣṇava day"),
  ("dinam", "acc.sg.n", "day"),
 ],
 "a": {
  "question": "What day arises at the end of Brahmā's own hundred years?",
  "premises": [
   "At night's end creation is made again, begun from darkness",
   "At the end of his own hundred years stands that ruin",
   "That ruin is named the Vaiṣṇava day"],
  "inference": "Night's end restarts creation; the century-end ruin is Vaiṣṇava day.",
  "uncertainties": ["svakavarṣaśatānte segmentation approximate (sva-varṣa-śata-ante)"],
  "plain_english": "At night's end he makes creation again, begun from darkness; at the end of his own hundred years stands that ruin — the Vaiṣṇava day.",
 },
},
146: {
 "g": [
  ("rātriśca", "and-night", "nom.sg.f + ca; the night likewise"),
  ("tāvatītyevaṃ", "thus-much-thus", "nom.sg.f + iti + evam; of that measure, so"),
  ("viṣṇurudraśatābhidhāḥ", "named-vishnu-rudra-hundreds", "nom.pl.m compound; the hundreds named Viṣṇu and Rudra"),
  ("kramātsvasvaśatānteṣu", "in-order-at-each-hundreds-end", "abl + loc.pl; in order at each own-century end"),
  ("naśyantyatrāṇḍalopataḥ", "perish-here-with-egg-loss", "3pl.pres √naś + loc; perish here with the egg's waning"),
 ],
 "m": [
  ("rātriśca", "nom.sg.f + particle", "and the night"),
  ("tāvatītyevaṃ", "nom.sg.f + indecl", "of that measure, thus"),
  ("viṣṇurudraśatābhidhāḥ", "nom.pl.m (compound)", "the hundreds named Viṣṇu and Rudra"),
  ("kramātsvasvaśatānteṣu", "abl.sg + loc.pl", "in order at each one's hundred-end"),
  ("naśyantyatrāṇḍalopataḥ", "3pl.pres √naś + loc", "perish here with the egg's loss"),
 ],
 "a": {
  "question": "Who perishes in order at each own-century end with the egg?",
  "premises": [
   "The night is of that measure, thus stated",
   "The hundreds named Viṣṇu and Rudra stand in sequence",
   "Each perishes at its own hundred-end with the egg's waning"],
  "inference": "Viṣṇu and Rudra by hundreds perish in turn at century-ends.",
  "uncertainties": [],
  "plain_english": "And the night is of that measure — thus the hundreds named Viṣṇu and Rudra, in order at each one's own hundred-end, perish here with the egg's waning.",
 },
},
147: {
 "g": [
  ("abādyavyaktatattvānteṣvitthaṃ", "thus-at-ends-of-unmanifest-tattva-from-start", "loc.pl compound; at those unmanifest-tattva ends from the beginning"),
  ("varṣaśataṃ", "hundred-years", "acc.sg.n; a century of years"),
  ("kramāt", "in-order", "abl.sg; sequential measure"),
  ("dinarātrivibhāgaḥ", "day-night-division", "nom.sg.m; the day-night split"),
  ("syāt", "would-be", "3sg.opt √as; would obtain"),
  ("svasvāyuḥśatamānataḥ", "measured-by-each-hundreds-lifespan", "abl compound; by each own hundred-year span"),
 ],
 "m": [
  ("abādyavyaktatattvānteṣvitthaṃ", "loc.pl (compound) + adv", "thus at the unmanifest-tattva ends"),
  ("varṣaśataṃ", "acc.sg.n", "a hundred years"),
  ("kramāt", "abl.sg", "by sequence"),
  ("dinarātrivibhāgaḥ", "nom.sg.m", "the day-night division"),
  ("syāt", "3sg.opt √as", "would be"),
  ("svasvāyuḥśatamānataḥ", "abl.sg (compound)", "by each own hundred-year measure"),
 ],
 "a": {
  "question": "How is the day-night division measured at unmanifest-tattva ends?",
  "premises": [
   "At the unmanifest-tattva ends from the start a hundred years stand",
   "In order the day-night division would so obtain",
   "Each is measured by its own hundred-year lifespan"],
  "inference": "Century-measured day-night splits follow each own lifespan at unmanifest ends.",
  "uncertainties": ["abādi segmentation (from-start vs an-ādi) approximate"],
  "plain_english": "Thus at the ends of the unmanifest tattva from the start, a hundred years in order — the day-night division would so obtain, measured by each one's own hundred-year span.",
 },
},
148: {
 "g": [
  ("brahmaṇaḥ", "of-brahma", "gen.sg.m; of Brahmā"),
  ("pralayollāsasahasraistu", "but-by-thousands-of-dissolution-joy", "instr.pl + tu; by thousands of dissolution-joys"),
  ("rasāgnibhiḥ", "by-subterranean-fires", "instr.pl; with the rasāgni fires"),
  ("avyaktastheṣu", "in-the-unmanifest-standing", "loc.pl; among those abiding in avyakta"),
  ("rudreṣu", "in-the-rudras", "loc.pl; among the Rudras"),
  ("dinaṃ", "day", "acc.sg.n; the day"),
  ("rātriśca", "and-night", "acc.sg.f + ca; and the night"),
  ("tāvatī", "of-that-measure", "nom.sg.f; of that extent"),
 ],
 "m": [
  ("brahmaṇaḥ", "gen.sg.m", "of Brahmā"),
  ("pralayollāsasahasraistu", "instr.pl + particle", "by thousands of dissolution-joys"),
  ("rasāgnibhiḥ", "instr.pl", "with the rasāgni fires"),
  ("avyaktastheṣu", "loc.pl", "among the unmanifest-standing"),
  ("rudreṣu", "loc.pl", "among the Rudras"),
  ("dinaṃ", "acc.sg.n", "day"),
  ("rātriśca", "acc.sg.f + particle", "and night"),
  ("tāvatī", "nom.sg.f", "of that measure"),
 ],
 "a": {
  "question": "How long is day and night among the Rudras in the unmanifest?",
  "premises": [
   "By thousands of Brahmā's dissolution-joys with rasāgni fires",
   "Among the Rudras standing in the unmanifest",
   "Day and night are each of that same measure"],
  "inference": "Among unmanifest Rudras day-night equals Brahmā's joy-fire measure.",
  "uncertainties": ["rasāgni as subterranean fire vs rasa-kindled fire"],
  "plain_english": "By thousands of Brahmā's dissolution-joys with the rasāgni fires — among the Rudras standing in the unmanifest, day and night are each of that measure.",
 },
},
149: {
 "g": [
  ("tadā", "then", "indecl; at that time"),
  ("śrīkaṇṭha", "shrikantha", "nom.sg.m; the blue-throated lord"),
  ("eva", "alone", "indecl; emphatic alone"),
  ("syātsākṣātsaṃhārakṛtprabhuḥ", "would-be-directly-destruction-doing-lord", "3sg.opt + nom; would be the lord directly doing dissolution"),
  ("sarve", "all", "nom.pl.m; all of them"),
  ("rudrāstathā", "rudras-likewise", "nom.pl.m + tathā; the Rudras likewise"),
  ("mūle", "at-the-root", "loc.sg.n; at the root"),
  ("māyāgarbhādhikāriṇaḥ", "charged-with-mayas-womb", "nom.pl.m; officers of māyā's womb"),
 ],
 "m": [
  ("tadā", "indecl.", "then"),
  ("śrīkaṇṭha", "nom.sg.m", "subject: Śrīkaṇṭha"),
  ("eva", "indecl.", "alone"),
  ("syātsākṣātsaṃhārakṛtprabhuḥ", "3sg.opt + nom.sg.m", "would be the direct dissolution-lord"),
  ("sarve", "nom.pl.m", "all"),
  ("rudrāstathā", "nom.pl.m + adv", "the Rudras likewise"),
  ("mūle", "loc.sg.n", "at the root"),
  ("māyāgarbhādhikāriṇaḥ", "nom.pl.m (compound)", "charged with māyā's womb"),
 ],
 "a": {
  "question": "Who stands as the direct lord of dissolution at that time?",
  "premises": [
   "Then Śrīkaṇṭha alone would be the lord doing dissolution",
   "All the Rudras likewise stand at the root",
   "They are charged with the womb of māyā"],
  "inference": "Śrīkaṇṭha is direct dissolution-lord; Rudras hold māyā's root charge.",
  "uncertainties": [],
  "plain_english": "Then Śrīkaṇṭha alone would be the lord directly doing dissolution; all the Rudras likewise at the root are charged with māyā's womb.",
 },
},
150: {
 "g": [
  ("avyaktākhye", "in-the-one-named-unmanifest", "loc.sg.n; in avyakta so named"),
  ("hyāviriñcācchrīkaṇṭhena", "indeed-with-shrikantha-of-brahma", "hi + prep + gen + instr; with Śrīkaṇṭha of Brahmā's line"),
  ("sahāsate", "sits-together", "3sg.pres √as + saha; sits together"),
  ("nivṛttādhaḥsthakarmā", "whose-lower-work-is-withdrawn", "nom.sg.m compound; lower function withdrawn"),
  ("hi", "indeed", "indecl; for"),
  ("brahmā", "brahma", "nom.sg.m; Brahmā"),
  ("tatrādhare", "there-in-the-lower", "loc + adj; there in the lower"),
  ("dhiyaḥ", "of-mind", "gen.sg.f; of the thought"),
 ],
 "m": [
  ("avyaktākhye", "loc.sg.n", "in the so-named unmanifest"),
  ("hyāviriñcācchrīkaṇṭhena", "prep + gen + instr.sg.m", "with Śrīkaṇṭha of Brahmā"),
  ("sahāsate", "3sg.pres √as", "sits together"),
  ("nivṛttādhaḥsthakarmā", "nom.sg.m (compound)", "lower work withdrawn"),
  ("hi", "indecl.", "indeed"),
  ("brahmā", "nom.sg.m", "Brahmā"),
  ("tatrādhare", "loc + loc.sg", "there in the lower"),
  ("dhiyaḥ", "gen.sg.f", "of the thought"),
 ],
 "a": {
  "question": "With whom does Śrīkaṇṭha sit in the avyakta when lower work is withdrawn?",
  "premises": [
   "In the one named avyakta he sits with Śrīkaṇṭha of Brahmā",
   "His lower function stands withdrawn",
   "Brahmā is there in the lower reach of thought"],
  "inference": "Śrīkaṇṭha sits with Brahmā in avyakta, lower work withdrawn.",
  "uncertainties": ["āviriñcāt as of-Brahmā vs from-Brahmā's side"],
  "plain_english": "In the one named avyakta he indeed sits with Śrīkaṇṭha of Brahmā's line, lower work withdrawn — for Brahmā is there in the lower reach of thought.",
 },
},
151: {
 "g": [
  ("na", "not", "indecl negation"),
  ("bhoktā", "experiencer", "nom.sg.m; the enjoyer"),
  ("jño@dhikāre", "knower-in-office", "nom.sg.m + loc; the knower in the office"),
  ("tu", "but", "indecl contrast"),
  ("vṛtta", "having-turned", "nom.sg.m ppp √vṛt; having become"),
  ("eva", "only", "indecl; sheer"),
  ("śivībhavet", "becomes-shiva", "3sg.opt √bhū + śiva; would become Śiva"),
  ("sa", "he", "nom.sg.m; that one"),
  ("eṣo@vāntaralayastatkṣaye", "this-intermediate-dissolution-at-its-end", "nom.sg.m compound; this intermediate laya at its end"),
  ("sṛṣṭirucyate", "creation-is-called", "nom.sg.f + 3sg.pres.pass √vac; creation is said"),
 ],
 "m": [
  ("na", "indecl.", "not"),
  ("bhoktā", "nom.sg.m", "the experiencer"),
  ("jño@dhikāre", "nom.sg.m + loc.sg", "the knower in office"),
  ("tu", "indecl.", "but"),
  ("vṛtta", "nom.sg.m ppp √vṛt", "having become"),
  ("eva", "indecl.", "only"),
  ("śivībhavet", "3sg.opt √bhū", "would become Śiva"),
  ("sa", "nom.sg.m", "he"),
  ("eṣo@vāntaralayastatkṣaye", "nom.sg.m (compound)", "this intermediate laya at its end"),
  ("sṛṣṭirucyate", "nom.sg.f + 3sg.pres.pass", "creation is called"),
 ],
 "a": {
  "question": "What is called creation at the end of the intermediate dissolution?",
  "premises": [
   "The knower in office is not merely the experiencer",
   "Having turned only to Śiva he would become Śiva",
   "At this intermediate laya's end that becoming is called creation"],
  "inference": "Becoming Śiva at intermediate-laya's end is named creation.",
  "uncertainties": ["force of vṛtta eva as having-turned vs sheer-becoming"],
  "plain_english": "The knower in office is not the mere experiencer; having turned only to Śiva he would become Śiva — this intermediate laya at its end is called creation.",
 },
},
152: {
 "g": [
  ("sāṃkhyavedādisaṃsiddhāñchrīkaṇṭhastadaharmukhe", "those-perfected-in-samkhya-veda-etc-shrikantha-at-that-days-face", "acc.pl + nom; Śrīkaṇṭha at that day's onset toward those perfected"),
  ("sṛjatyeva", "indeed-creates", "3sg.pres √sṛj + eva; he creates indeed"),
  ("punastena", "again-thereby", "punaḥ + tena; again by that"),
  ("na", "not", "indecl negation"),
  ("samyaṅmuktirīdṛśī", "complete-liberation-of-this-kind", "nom.sg.f; liberation complete is not of this kind"),
 ],
 "m": [
  ("sāṃkhyavedādisaṃsiddhāñchrīkaṇṭhastadaharmukhe", "acc.pl + nom + loc", "Śrīkaṇṭha at that day's face toward the perfected"),
  ("sṛjatyeva", "3sg.pres √sṛj + particle", "he creates indeed"),
  ("punastena", "adv + instr", "again by that"),
  ("na", "indecl.", "not"),
  ("samyaṅmuktirīdṛśī", "nom.sg.f", "liberation of this kind complete"),
 ],
 "a": {
  "question": "What kind of liberation follows from Śrīkaṇṭha's creation at that day?",
  "premises": [
   "Śrīkaṇṭha at that day's face creates toward those perfected in Sāṃkhya and Vedas",
   "He creates again by that onset",
   "Complete liberation is not of this kind"],
  "inference": "Śrīkaṇṭha's day-creation does not yield complete liberation.",
  "uncertainties": ["whether na negates only samyak-mukti or the whole resultant"],
  "plain_english": "At that day's face Śrīkaṇṭha creates again toward those perfected in Sāṃkhya, Vedas, and the rest — yet complete liberation is not of this kind.",
 },
},
153: {
 "g": [
  ("pradhāne", "in-pradhana", "loc.sg.n; in primordial nature"),
  ("yadahorātraṃ", "which-day-and-night", "nom.sg.n rel; which day-night"),
  ("tajjaṃ", "born-of-that", "acc.sg.n; born of it"),
  ("varṣaśataṃ", "hundred-years", "acc.sg.n; a hundred years"),
  ("vibhoḥ", "of-the-lord", "gen.sg.m; of the Lord"),
  ("śrīkaṇṭhasyāyuretacca", "and-this-is-shrikanthas-lifespan", "gen + acc + ca; and this is Śrīkaṇṭha's span"),
  ("dinaṃ", "day", "acc.sg.n; the day"),
  ("kañcukavāsinām", "of-kañcuka-dwellers", "gen.pl.m; of those dwelling in the kañcukas"),
 ],
 "m": [
  ("pradhāne", "loc.sg.n", "in pradhāna"),
  ("yadahorātraṃ", "nom.sg.n (rel.)", "which day-night"),
  ("tajjaṃ", "acc.sg.n", "born of that"),
  ("varṣaśataṃ", "acc.sg.n", "a hundred years"),
  ("vibhoḥ", "gen.sg.m", "of the Lord"),
  ("śrīkaṇṭhasyāyuretacca", "gen + acc + particle", "this is Śrīkaṇṭha's lifespan"),
  ("dinaṃ", "acc.sg.n", "day"),
  ("kañcukavāsinām", "gen.pl.m", "of the kañcuka-dwellers"),
 ],
 "a": {
  "question": "Whose day and hundred-year span is born in pradhāna?",
  "premises": [
   "In pradhāna stands a day-night born of that",
   "A hundred years of the Lord's day",
   "This is Śrīkaṇṭha's lifespan and the day of kañcuka-dwellers"],
  "inference": "Pradhāna's century-day is Śrīkaṇṭha's span for kañcuka-dwellers.",
  "uncertainties": ["whether varṣaśataṃ measures Śrīkaṇṭha alone or the class"],
  "plain_english": "In pradhāna the day-night born of it — a hundred years of the Lord — is Śrīkaṇṭha's lifespan, the day of those dwelling in the kañcukas.",
 },
},
154: {
 "g": [
  ("tatkramānniyatiḥ", "from-that-sequence-niyati", "abl + nom; Niyati from that sequence"),
  ("kālo", "kala-time", "nom.sg.m; Kāla"),
  ("rāgo", "raga", "nom.sg.m; Rāga"),
  ("vidyā", "knowledge", "nom.sg.f; Vidyā"),
  ("kaletyamī", "kala-these", "nom.sg.f + iti + amī; Kalā — these"),
  ("yāntyanyonyaṃ", "go-one-anothers", "3pl.pres + acc; enter one another's"),
  ("layaṃ", "dissolution", "acc.sg.m; dissolution"),
  ("teṣāmāyurgāhanikaṃ", "their-lifespan-dense-day", "gen + acc; their lifespan is the dense day"),
  ("dinam", "day", "acc.sg.n; day so measured"),
 ],
 "m": [
  ("tatkramānniyatiḥ", "abl.sg + nom.sg.f", "Niyati from that sequence"),
  ("kālo", "nom.sg.m", "Kāla"),
  ("rāgo", "nom.sg.m", "Rāga"),
  ("vidyā", "nom.sg.f", "Vidyā"),
  ("kaletyamī", "nom.sg.f + indecl", "Kalā — these"),
  ("yāntyanyonyaṃ", "3pl.pres + acc.sg.m", "enter one another's"),
  ("layaṃ", "acc.sg.m", "dissolution"),
  ("teṣāmāyurgāhanikaṃ", "gen + acc.sg.n", "their lifespan the dense day"),
  ("dinam", "acc.sg.n", "day"),
 ],
 "a": {
  "question": "Which powers enter one another's dissolution as the dense day?",
  "premises": [
   "From that sequence stand Niyati, Kāla, Rāga, Vidyā, Kalā",
   "These enter one another's dissolution",
   "Their lifespan is the dense day of that measure"],
  "inference": "The five powers pass into each other's laya as a dense day-long span.",
  "uncertainties": ["gahanika as dense/deep vs a proper measure-name"],
  "plain_english": "From that sequence Niyati, Kāla, Rāga, Vidyā, and Kalā enter one another's dissolution; their lifespan is the dense day.",
 },
},
155: {
 "g": [
  ("taddinaprakṣaye", "at-that-days-wasting", "loc.sg.n; when that day is spent"),
  ("viśvaṃ", "universe", "acc.sg.n; the world"),
  ("māyāyāṃ", "in-maya", "loc.sg.f; in māyā"),
  ("pravilīyate", "dissolves-in", "3sg.pres.pass √lī; is dissolved into"),
  ("kṣīṇāyāṃ", "having-wasted", "loc.sg.f ppp √kṣi; spent"),
  ("niśi", "in-night", "loc.sg.f; in the night"),
  ("tāvatyāṃ", "of-that-measure", "loc.sg.f; of that extent"),
  ("gahaneśaḥ", "lord-of-the-dense", "nom.sg.m; Gahaneśa, lord of the gahana"),
  ("sṛjetpunaḥ", "should-create-again", "3sg.opt √sṛj + punaḥ; should create anew"),
 ],
 "m": [
  ("taddinaprakṣaye", "loc.sg.n", "at that day's wasting"),
  ("viśvaṃ", "acc.sg.n", "the universe"),
  ("māyāyāṃ", "loc.sg.f", "in māyā"),
  ("pravilīyate", "3sg.pres.pass √lī", "dissolves"),
  ("kṣīṇāyāṃ", "loc.sg.f ppp", "having wasted"),
  ("niśi", "loc.sg.f", "in night"),
  ("tāvatyāṃ", "loc.sg.f", "of that measure"),
  ("gahaneśaḥ", "nom.sg.m", "Gahaneśa"),
  ("sṛjetpunaḥ", "3sg.opt √sṛj", "should create again"),
 ],
 "a": {
  "question": "What does Gahaneśa do when that day is spent in māyā-night?",
  "premises": [
   "At that day's wasting the universe dissolves in māyā",
   "The night stands of that same spent measure",
   "Gahaneśa should create the world again"],
  "inference": "Māyā-night dissolves the world; Gahaneśa re-creates it.",
  "uncertainties": ["gahaneśa as epithet of Śiva in the dense gahana"],
  "plain_english": "At that day's wasting the universe dissolves in māyā; in the night of that measure Gahaneśa should create again.",
 },
},
156: {
 "g": [
  ("evamavyaktakālaṃ", "thus-unmanifest-time", "adv + acc.sg.n; thus the avyakta-time"),
  ("tu", "but", "indecl contrast"),
  ("parārdhairdaśabhirjahi", "by-ten-parardhas-conquer", "instr.pl + imp √han/jahā?; by ten parārdhas it is struck through"),
  ("māyāhastāvatī", "of-maya-that-much", "gen + nom.sg.f; māyā's night is of that much"),
  ("rātrirbhavetpralaya", "night-would-be-dissolution", "nom.sg.f + 3sg.opt; the night would be dissolution"),
  ("eṣa", "this", "nom.sg.m; this"),
  ("saḥ", "that", "nom.sg.m; that one"),
 ],
 "m": [
  ("evamavyaktakālaṃ", "adv + acc.sg.n", "thus the unmanifest time"),
  ("tu", "indecl.", "but"),
  ("parārdhairdaśabhirjahi", "instr.pl + 2sg.imp", "by ten parārdhas — strike through"),
  ("māyāhastāvatī", "gen + nom.sg.f", "of māyā, of that much"),
  ("rātrirbhavetpralaya", "nom.sg.f + 3sg.opt", "the night would be dissolution"),
  ("eṣa", "nom.sg.m", "this"),
  ("saḥ", "nom.sg.m", "that"),
 ],
 "a": {
  "question": "How is the avyakta-time reckoned against ten parārdhas?",
  "premises": [
   "Thus the unmanifest time is struck through by ten parārdhas",
   "Māyā's night stands of that same measure",
   "That night would be the dissolution so named"],
  "inference": "Ten parārdhas measure avyakta-time; māyā's night of that span is dissolution.",
  "uncertainties": ["jahi as imperative strike vs corrupted jayati (conquers)"],
  "plain_english": "Thus the unmanifest time is struck through by ten parārdhas; māyā's night of that measure would be the dissolution — that is the one so named.",
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
print(f"wrote {n} files (vv145-156 gloss+cm+am)")
