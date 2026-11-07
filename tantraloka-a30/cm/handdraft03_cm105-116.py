#!/usr/bin/env python3
"""Assessor hand-draft for tal-a30 vv105-116 (cm.json). Part 3 of 3.

Provenance: as in parts 1-2. Morphology by hand: regular nominal/verbal forms
analyzed; mantra seed-syllables (bija, pranava, hum) as indeclinable; fused
compounds kept whole per fused-span rule (described, not split). Lemma equals
surface (triple-convention). Grounds cite gloss + form.
"""
from __future__ import annotations
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "process" / "beam" / "runs"
SONG = "tal-a30"

# verse -> list of (surface, morph, grounds)
CM: dict[int, list[tuple[str, str, str]]] = {
105: [
 ("guruṇā", "instr.sg.m (√gṝ guru)", "agent of giving; gloss by-guru"),
 ("tattvavidā", "instr.sg.m/f (tattva-vid)", "co-agent; gloss by-truth-knower"),
 ("kila", "indecl.", "emphatic particle; gloss indeed"),
 ("śiṣyo", "nom.sg.m (śiṣya)", "subject; gloss student"),
 ("yadi", "indecl.", "condition; gloss if"),
 ("mokṣamātrakṛtahṛdayaḥ", "nom.sg.m compound (mātra-kṛta-hṛdaya)", "agrees with śiṣyaḥ; kept fused"),
 ("mokṣaikadānacaturā", "nom.sg.f compound (eka-dāna-caturā)", "agrees with dīkṣā; kept fused"),
 ("dīkṣā", "nom.sg.f", "subject complement; gloss initiation"),
 ("seyaṃ", "nom.sg.f (sā+iyam sandhi)", "points to dīkṣā; gloss this"),
 ("paropaniṣaduktā", "nom.sg.f compound (para-upaniṣad-uktā)", "agrees with dīkṣā; kept fused"),
],
106: [
 ("etaddīkṣādīkṣita", "nom.sg.m compound (etad-dīkṣā-dīkṣita)", "subject; kept fused"),
 ("etadvidyātrayaṃ", "acc.sg.n compound (etad-vidyā-traya)", "object of smaran; kept fused"),
 ("smaran", "pres.part nom.sg.m (√smṛ)", "agrees with subject; gloss remembering"),
 ("hṛdaye", "loc.sg.n (hṛdaya)", "place of remembering; gloss in-heart"),
 ("bāhyārcādi", "acc.sg.n compound (bāhya-arcā-ādi)", "object governed by vinā; kept fused"),
 ("vinaiva", "indecl. (vinā+eva)", "exclusion; gloss without-indeed"),
 ("hi", "indecl.", "emphatic; gloss indeed"),
 ("vrajati", "3sg.pres.act (√vraj)", "main verb; gloss goes"),
 ("paraṃ", "acc.sg.n (para)", "agrees with dhāma; gloss supreme"),
 ("dhāma", "acc.sg.n", "goal; gloss abode"),
 ("dehānte", "loc.sg.m compound (deha-anta)", "time; kept fused"),
],
107: [
 ("praṇavo", "nom.sg.m (pra-ṇava, oṃ)", "subject mantra; gloss om"),
 ("māyā", "nom.sg.f", "seed syllable as deity; gloss illusion"),
 ("bindurvarṇatrayamāditaḥ", "compound (bindu-varṇa-traya-āditaḥ)", "kept fused; dot plus three letters"),
 ("kuryāt", "3sg.opt.act (√kṛ)", "injunction; gloss should-make"),
 ("padapañcakasya", "gen.sg.n compound (pada-pañcaka)", "of five words; kept fused"),
 ("saṃbodhanayuktasyāgnidayitānte", "compound (saṃbodhana-yukta-agni-dayitā-ante)", "kept fused; vocative-joined ending"),
],
108: [
 ("siddhasādhani", "nom.sg.f compound (siddha-sādhanī)", "mantra name; kept fused"),
 ("tatpūrvaṃ", "acc.sg.n/indecl. (tad-pūrva)", "priority adverb; gloss before-that"),
 ("śabdabrahmasvarūpiṇi", "loc.sg.f compound (śabda-brahma-svarūpin)", "abode of power; kept fused"),
 ("samastabandhaśabdena", "instr.sg.m compound (samasta-bandha-śabda)", "means; kept fused"),
 ("sahitaṃ", "acc.sg.n (sahita)", "joined; gloss together-with"),
 ("ca", "indecl.", "conjunction; gloss and"),
 ("nikṛntani", "nom.sg.f? imperative force (ni-kṛnt)", "cutting act; gloss cutting"),
],
109: [
 ("bodhani", "loc.sg.f (bodhanī)", "in awakening; gloss in-awakening"),
 ("śivasadbhāvajananyāmantritaṃ", "acc.sg.n compound (śiva-sadbhāva-jananī-āmantrita)", "object; kept fused"),
 ("ca", "indecl.", "conjunction; gloss and"),
 ("tat", "nom/acc.sg.n (tad)", "pronoun; gloss that"),
 ("pañcāṣṭarandhratryaṣṭārṇakrameṇa", "instr.sg.m compound (numeral-orders)", "means/order; kept fused"),
 ("padapañcakam", "acc.sg.n compound (pada-pañcaka)", "object; gloss five-footed-verse"),
],
110: [
 ("khapañcārṇā", "nom.sg.f compound (kha-pañca-arṇa)", "vidya name; kept fused"),
 ("parabrahmavidyeyaṃ", "nom.sg.f compound (para-brahma-vidyā-iyam)", "subject; kept fused"),
 ("mokṣadā", "nom.sg.f (mokṣa-dā)", "liberation-giving; agrees with vidyā"),
 ("śivā", "nom.sg.f", "auspicious; gloss auspicious"),
 ("anuttarecche", "loc.sg.f compound (anuttara-icchā)", "context; kept fused"),
 ("ghāntaśca", "nom.sg.m (ghaṇṭa+ca)", "bell-and; gloss bell-and"),
 ("satrayodaśasusvaraḥ", "nom.sg.m compound (su-svara order)", "kept fused; thirteen tones"),
],
111: [
 ("asya", "gen.sg.m/n (idam)", "of-this; gloss of-this"),
 ("varṇatrayasyānte", "loc.sg.m compound (varṇa-traya-anta)", "place; kept fused"),
 ("tvantaḥsthānāṃ", "gen.pl.f compound (tav-antahstha)", "of semivowels; kept fused"),
 ("catuṣṭayam", "acc.sg.n (catuṣṭaya)", "quartet; gloss four"),
 ("vargādyaśvau", "nom.du.m compound (varga-ādya-aśva)", "two leaders; kept fused"),
 ("tryasrabinduyuk", "nom.sg.m compound (tryasra-bindu-yuj)", "joined; kept fused"),
 ("pānto@rṇatrayādataḥ", "compound with @ sandhi (pa-anta-arṇa-traya)", "kept fused with @ mark"),
],
112: [
 ("mahāhāṭakaśabdādyamīśvarītyarṇasaptakam", "acc.sg.n long compound (mahā-hāṭaka-śabda-ādi-īśvarī-arṇa-saptaka)", "object mantra; kept fused"),
 ("āmantritaṃ", "acc.sg.n (āmantrita)", "addressed; agrees with object"),
 ("kṣamasveti", "indecl. (kṣamasva+iti)", "forgive-thus; gloss forgive-thus"),
 ("tryarṇaṃ", "acc.sg.n (tri-arṇa)", "three-syllable; gloss three-syllable"),
 ("pāpāntakāriṇi", "loc.sg.f (pāpa-anta-kāriṇī)", "context; gloss sin-destroying"),
],
113: [
 ("ṣaḍarṇaṃ", "acc.sg.n (ṣaḍ-arṇa)", "object; gloss six-syllabled"),
 ("pāpaśabdādivimohanipadaṃ", "acc.sg.n long compound", "object; kept fused"),
 ("tataḥ", "indecl.", "sequence; gloss then"),
 ("pāpaṃ", "acc.sg.n (pāpa)", "object; gloss sin"),
 ("hana", "2sg.imp.act (√han)", "command; gloss kill"),
 ("dhuna", "2sg.imp.act (√dhū)", "command; gloss shake-off"),
 ("dvirdvirdaśārṇaṃ", "acc.sg.n numeral compound", "measure; kept fused"),
 ("padamīdṛśam", "acc.sg.n (pada-īdṛśa)", "such word; gloss such-word"),
],
114: [
 ("pañcamyantaṃ", "acc.sg.n compound (pañcamī-anta)", "ending; gloss fifth-case-ending"),
 ("ṣaḍarṇaṃ", "acc.sg.n (ṣaḍ-arṇa)", "object; gloss six-letter"),
 ("syādrudraśaktivaśāditi", "compound (syād-rudra-śakti-vaśād-iti)", "kept fused; by-power-thus"),
 ("tata", "indecl.", "sequence (tatas); gloss then"),
 ("ekākṣaraṃ", "acc.sg.n (eka-akṣara)", "object; gloss one-syllable"),
 ("yattadvisargabrahma", "acc.sg.n compound (yad-tad-visarga-brahman)", "object; kept fused"),
 ("kīrtitam", "acc.sg.n (kīrtita)", "declared; agrees with object"),
],
115: [
 ("tadanackatakāreṇa", "instr.sg.m compound (uncertain reading)", "means; kept fused; reading uncertain"),
 ("sahaikībhāvataḥ", "indecl. compound (saha-ekībhāva-tas)", "from-union; kept fused"),
 ("paṭhet", "3sg.opt.act (√paṭh)", "injunction; gloss should-recite"),
 ("randhrābdhivarṇā", "nom.sg.f numeral compound (randhra-abdhi-varṇa)", "letters; kept fused"),
 ("vidyeyaṃ", "nom.sg.f (vidyā-iyam)", "subject; gloss this-knowledge"),
 ("dīkṣāvidyeti", "nom.sg.f (dīkṣā-vidyā-iti)", "as-initiation-knowledge; gloss as-initiation-knowledge"),
 ("kīrtitā", "nom.sg.f (kīrtitā)", "is-called; agrees with vidyā"),
],
116: [
 ("māyārṇañca", "acc.sg.m (māyā-arṇa+ca)", "syllable-and; gloss maya-arna-and"),
 ("pare", "loc.sg.m/n (para)", "context; gloss supreme"),
 ("brahme", "loc.sg.n (brahman)", "in brahman; gloss brahman-in"),
 ("caturvidye", "loc.sg.f (catur-vidyā)", "context; gloss four-vidya-in"),
 ("padatrayam", "acc.sg.n (pada-traya)", "object; gloss three-foot"),
 ("aṣṭārṇamatha", "acc.sg.n (aṣṭa-arṇa+atha)", "object; gloss eight-syllable-and"),
 ("pañcārṇaṃ", "acc.sg.n (pañca-arṇa)", "object; gloss five-syllable"),
 ("yogadhāriṇisaṃjñitam", "acc.sg.n compound (yoga-dhārin-saṃjñita)", "named; kept fused"),
],
}

n = 0
for v, rows in CM.items():
    assert all(m.strip() and g.strip() for _, m, g in rows), v
    cdir = RUNS / f"{SONG}-cm-v{v:02d}"
    cdir.mkdir(parents=True, exist_ok=True)
    (cdir / "cm.json").write_text(json.dumps(
        {"song": SONG, "verse": v,
         "rows": [{"lemma": s, "morph": m, "grounds": g} for s, m, g in rows]},
        indent=1, ensure_ascii=False))
    n += 1
print(f"wrote {n} assessor cm.json files (vv105-116)")
