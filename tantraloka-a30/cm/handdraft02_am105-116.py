#!/usr/bin/env python3
"""Assessor hand-draft for tal-a30 vv105-116 (am.json). Part 2 of 3.

Provenance: as in handdraft01 (429-storm failures at max, assessor escalation).
Section: Srisantati initiation (vv105-106) + three Vidyas (vv107-116) per
Dyczkowski Vol 11 TOC. Gates self-enforced as in part 1.
"""
from __future__ import annotations
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "process" / "beam" / "runs"
SONG = "tal-a30"

AM: dict[int, dict] = {
105: {
 "question": "When does the guru give the supreme-upanisad initiation?",
 "premises": [
  "The truth-knowing guru faces a disciple heart-set on liberation alone",
  "Skilled in bestowing liberation's gift, the guru acts indeed",
  "This initiation is stated in the supreme upanisad"],
 "inference": "The Srisantati initiation goes to the liberation-only disciple.",
 "uncertainties": ["whether paropanisad names a text or a rank"],
 "plain_english": "When the truth-knowing guru finds a disciple heart-made for liberation alone, skilled in liberation's sole gift, this is the supreme-upanisad initiation.",
},
106: {
 "question": "What becomes of one initiated who remembers the threefold vidya?",
 "premises": [
  "Initiated into this, remembering the threefold vidya in the heart",
  "Without any outer worship and the rest, he reaches the supreme abode",
  "The passage comes at the body's end"],
 "inference": "Heart-remembered threefold vidya carries beyond outer rite to liberation.",
 "uncertainties": [],
 "plain_english": "Initiated into this initiation, remembering this threefold vidya in the heart, without outer worship and the rest, he reaches the supreme abode at body's end.",
},
107: {
 "question": "How is the five-word mantra of the fire's beloved built?",
 "premises": [
  "Om and maya with bindu open the construction",
  "Three letters from the start shape five addressed words",
  "The fire-god's beloved closes the five-word mantra"],
 "inference": "Om-maya-bindu plus three opening letters yields five addressed words.",
 "uncertainties": ["identity of agnidayita (Svaha?)"],
 "plain_english": "Om and maya with bindu: make three letters from the start into five addressed words ending with the fire-god's beloved.",
},
108: {
 "question": "How does the cutting mantra join sound-brahman form?",
 "premises": [
  "The accomplished-accomplishing power comes first with sound-brahman form",
  "Joined with the word of every bond, it cuts",
  "The cutting operates through naming each fetter"],
 "inference": "Sound-brahman power plus all-bond-word cuts every bond.",
 "uncertainties": ["exact referent of siddha-sadhani as mantra name"],
 "plain_english": "The accomplished-accomplishing power in sound-brahman form, joined with the word of every bond, cuts.",
},
109: {
 "question": "How is the five-footed verse ordered by eights and threes?",
 "premises": [
  "In awakening, the invoked mother of Siva's true being presides",
  "Five feet follow the five-eight and three-eight orders",
  "The order itself empowers each foot"],
 "inference": "Mother-invoked five feet run on 5-8 and 3-8 letter orders.",
 "uncertainties": ["how the two counts distribute across five feet"],
 "plain_english": "In awakening, invoked by the mother of Siva's true being, the five-footed verse runs in five-eight and three-eight order.",
},
110: {
 "question": "Which supreme-brahman vidya gives liberation by desire?",
 "premises": [
  "The sky-five-syllable vidya of supreme brahman gives liberation",
  "Auspicious, it works in supreme desire with bell and thirteen tones",
  "Its sound completes the rite of release"],
 "inference": "Sky-five-syllable vidya liberates through supreme-desire sounding.",
 "uncertainties": ["reading of ghanta and trayodasa-susvara as ritual acts"],
 "plain_english": "The sky-five-syllable supreme-brahman vidya gives liberation, auspicious, in supreme desire with bell and thirteen tones.",
},
111: {
 "question": "How are the semivowel quartet and triangle-bindu joined?",
 "premises": [
  "At the three letters' end stand four semivowels ending in ta",
  "First-of-class and horse-letters join triangle and bindu",
  "Three letters after pa complete the set"],
 "inference": "Semivowel quartet plus class-leaders with triangle-bindu, sealed after pa.",
 "uncertainties": ["which letters asva denotes here"],
 "plain_english": "At the three letters' end the four semivowels ending in ta; first-of-class and horse with triangle-bindu joined, from three letters after pa.",
},
112: {
 "question": "What is the seven-syllable sin-destroying address?",
 "premises": [
  "The great-golden-sound mantra holds seven goddess-syllables",
  "Addressed with forgive-thus, its three syllables destroy sin",
  "The sin-ending power defines the mantra's use"],
 "inference": "Seven-syllable golden address: forgive-thus, sin destroyed.",
 "uncertainties": [],
 "plain_english": "The great-golden-sound seven-syllable mantra of the goddess, addressed forgive-thus in three syllables, ending sin.",
},
113: {
 "question": "How do the sin-word mantras command killing and shaking off?",
 "premises": [
  "The six-syllabled deluding word begins with the sinful word",
  "Then kill, shake off: twice-twice-ten syllables command likewise",
  "Each such word performs the destruction directly"],
 "inference": "Sin-word mantras order killing and shaking-off by syllable count.",
 "uncertainties": ["how dvir-dvir-dasa counts distribute"],
 "plain_english": "The six-syllabled deluding word beginning with the sinful word; then kill, shake off, in twice-twice-ten syllables, such is the word.",
},
114: {
 "question": "How does Rudra's power declare the one-syllable visarga-brahman?",
 "premises": [
  "By Rudra-Sakti power the six-letter form ends in fifth case",
  "Then the one syllable, the visarga-brahman, is declared",
  "The declaration seals the mantra's authority"],
 "inference": "Rudra-power six-letter form yields the declared one-syllable visarga-brahman.",
 "uncertainties": [],
 "plain_english": "By Rudra-Sakti power the six-letter form ending in fifth case; then the one syllable declared, the visarga-brahman.",
},
115: {
 "question": "How is this initiation-vidya recited in union?",
 "premises": [
  "In union with that very act the recitation proceeds",
  "Hole-ocean letters carry this vidya called initiation-knowledge",
  "The reciter holds the union while sounding each letter"],
 "inference": "Recite hole-ocean-letter vidya in union as initiation-knowledge.",
 "uncertainties": ["mapping of randhra-abdhi to counts"],
 "plain_english": "In union with that act recite: hole-ocean letters, this vidya called initiation-knowledge.",
},
116: {
 "question": "How do the three-foot and eight-syllable vidyas complete the set?",
 "premises": [
  "In supreme brahman, maya-syllable with four vidyas holds three feet",
  "Eight syllables then five carry the yoga-bearer name",
  "The set closes the three-vidya teaching"],
 "inference": "Maya-syllable four-vidya three feet plus eight-then-five yoga-bearer names.",
 "uncertainties": ["division between the enumerated vidyas"],
 "plain_english": "Maya-syllable in supreme brahman with four vidyas, three feet; eight syllables then five, named yoga-bearer.",
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
print(f"wrote {n} assessor am.json files (vv105-116)")
