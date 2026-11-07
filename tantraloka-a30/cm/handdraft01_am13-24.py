#!/usr/bin/env python3
"""Assessor hand-draft for tal-a30 vv13-24 (am.json). Part 1 of 3.

Provenance: beam triple tasks failed at max (429 storm). Per largetext SKILL
(escalate to assessor hand-draft, never auto-retry), content composed by hand
from working-t1 tokens + Dyczkowski Vol 11 TOC + tal-a30 lore brief.
Uncertainties stay open (mistakes #6). Gates self-enforced: Q verse-owned >=5
words, premises >=3 words, plain_english >=4 words.
"""
from __future__ import annotations
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "process" / "beam" / "runs"
SONG = "tal-a30"

AM: dict[int, dict] = {
13: {
 "question": "By what names is the consciousness-attainment procedure established?",
 "premises": [
  "The procedure casts illumination and establishment through consciousness-awakening",
  "That consciousness and its attainment are named by the stated terms",
  "The naming fixes the procedure as received doctrine rather than invention"],
 "inference": "The rite is established under the stated names of consciousness-attainment.",
 "uncertainties": ["exact force of ksepa-akranti within the compound"],
 "plain_english": "The procedure of throwing over, overcoming, awakening and establishing consciousness is thus named: that consciousness, that attainment.",
},
14: {
 "question": "How is the great pervasion proclaimed and sealed with salutation?",
 "premises": [
  "Such is the great pervasion, proclaimed as embodied here",
  "Its transformation and dissolution are sealed with salutation",
  "The seal is spoken as the rite's closing affirmation"],
 "inference": "The pervasion teaching closes by naming transformation-dissolution as salutation.",
 "uncertainties": [],
 "plain_english": "Such is the great pervasion, proclaimed as embodied here; transformation and its dissolution are called salutation.",
},
15: {
 "question": "How are the six limbs and faces of the mantra constructed?",
 "premises": [
  "The three-syllable mantra is joined below with six long vowels",
  "From this joining the six limbs beginning with the Heart are formed",
  "Its faces are likewise constructed in order"],
 "inference": "Vowel-joining below the three syllables yields six limbs and faces.",
 "uncertainties": ["whether adhastat governs each syllable or the whole"],
 "plain_english": "The three-syllable mantra, joined below with six long vowels, yields the six limbs beginning with the Heart; construct its faces likewise.",
},
16: {
 "question": "Which blazing seeds carry the withdrawal breath of dissolution?",
 "premises": [
  "The seeds of destruction-sound shine adorned with the drop",
  "The syllable jha holds the life-breath of withdrawal",
  "Sa with the sixth vowel and drop completes the set"],
 "inference": "Blazing bindu-crowned seeds including jha embody the dissolution breath.",
 "uncertainties": ["exact reading of ksayara-vala sequence as seed names"],
 "plain_english": "With destruction-sound seeds blazing and bindu-adorned, with jha as the breath of withdrawal, and sa with sixth vowel and drop.",
},
17: {
 "question": "Which mantras of the Bhairava abode were already proclaimed?",
 "premises": [
  "This is the abode of Bhairava adorned with half-moon and the rest",
  "The matrka and malini mantras belong to this abode",
  "Both were proclaimed earlier in the teaching"],
 "inference": "The Bhairava-abode mantras are matrka and malini, already taught.",
 "uncertainties": [],
 "plain_english": "This is the abode of Bhairava adorned with half-moon and the rest; the matrka and malini mantras were proclaimed before.",
},
18: {
 "question": "How is the seed mantra ordered for Ganesha and the rest?",
 "premises": [
  "Om comes first, then the dative name in order",
  "Obeisance follows the same order among Ganesha and the rest",
  "The seed stands as mantra wherever no other is declared"],
 "inference": "Om plus dative name plus obeisance is the default seed-mantra order.",
 "uncertainties": ["scope of natiriti across the listed deities"],
 "plain_english": "Then om, the name in fourth-case ending, obeisance thus in order; among Ganesha and the rest the seed is mantra where none is declared.",
},
19: {
 "question": "How is the seed of all seeds illuminated?",
 "premises": [
  "The name's first letter joined with a, bindu and moon-illumination",
  "This is the seed of all seeds indeed",
  "It is joined with fourteen and with sixty"],
 "inference": "First-letter plus a-bindu-moon forms the universal seed with fourteen and sixty.",
 "uncertainties": ["what fourteen and sixty count"],
 "plain_english": "The name's first letter illumined with a, bindu and moon is the seed of all seeds, joined with fourteen and sixty.",
},
20: {
 "question": "Which seeds arise in order for the Aghora triad?",
 "premises": [
  "The triad beginning with the invoked Ghora yields seeds in order",
  "Visarga-bearing seeds carry maya, hum and ha with visarga",
  "Each seed holds its ritual position in the sequence"],
 "inference": "Ordered visarga seeds with maya-hum-ha serve the invoked triad.",
 "uncertainties": ["resolution of amantritanya within the compound"],
 "plain_english": "Of the triad beginning with the invoked Ghora, seeds arise in order: visarga-bearing maya, hum, and ha with visarga.",
},
21: {
 "question": "What are the three invocations of the three goddesses?",
 "premises": [
  "Again three invocations address the three goddesses in order",
  "In the second word the ka-form carries the e-sound here",
  "The tradition records this arrangement as fixed"],
 "inference": "Three ordered invocations with the e-sounding ka-form in the second word.",
 "uncertainties": ["exact syllable meant by dvitiyasmin pade akara"],
 "plain_english": "Again three invocations of the three goddesses in order; in the second word the ka-form with e-sound is recorded here.",
},
22: {
 "question": "How is the two-power mantra formed with fire letters?",
 "premises": [
  "The mantra of the two powers drops its final letter there",
  "Both fire letters stand joined with five vowels",
  "The two distant ones are kept separate"],
 "inference": "Two-power mantra: final dropped, fire letters with five vowels, two held apart.",
 "uncertainties": ["identity of the two distant ones"],
 "plain_english": "Then the two-power mantra with its final letter omitted; both fire letters joined with five vowels, the two distant ones separate.",
},
23: {
 "question": "How is the astra mantra built with hum and the arrow?",
 "premises": [
  "The astra endowed with a joins hum, ha and the visarga-bearer",
  "The arrow returns again with Tara",
  "Vasu-fire letters with two half-syllables exceed the measure"],
 "inference": "Astra from a-hum-ha-visarga plus arrow-with-Tara, exceeding by two half-syllables.",
 "uncertainties": ["numeral force of vasu-agni-varna counting"],
 "plain_english": "The astra endowed with a joins hum, ha and the visarga-bearer; the arrow again with Tara, exceeding by two half-syllables of vasu-fire letters.",
},
24: {
 "question": "What is the Parapara vidya and its letter-count verse?",
 "premises": [
  "This is the vidya of the supreme-inferior goddess in Trika teaching",
  "Its verse carries the five-six-five-veda-eye-fire count",
  "The count seals the mantra's completeness"],
 "inference": "Parapara vidya: goddess-formula with the stated letter-count seal.",
 "uncertainties": ["mapping of veda-aksi-vahni-netra to digits"],
 "plain_english": "This is the vidya of the supreme-inferior goddess in the Trika teaching, a verse of five-six-five-veda-eye-fire-eye letters.",
},
}

n = 0
for v, d in AM.items():
    assert d["question"].endswith("?") and len(d["question"].split()) >= 5, v
    assert all(len(p.split()) >= 3 for p in d["premises"]), v
    assert len(d["plain_english"].split()) >= 4, v
    adir = RUNS / f"{SONG}-am-v{v:02d}"
    adir.mkdir(parents=True, exist_ok=True)
    (adir / "am.json").write_text(json.dumps(
        {"song": SONG, "verse": v, **d}, indent=1, ensure_ascii=False))
    n += 1
print(f"wrote {n} assessor am.json files (vv13-24)")
