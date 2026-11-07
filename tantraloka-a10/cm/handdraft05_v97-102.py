#!/usr/bin/env python3
"""Assessor hand-draft tal-a10 vv97-102 (cm+am only; gloss already present).

Provenance: tal-a10-triple-v97 failed 6/6 (question rejected / premise too short).
Per largetext SKILL: escalate to assessor hand-draft. Content from working-t1
surfaces + source spans (sha 3ceb9fa7761df0d1) + tal-a10 brief (tattvabheda:
perceptibility doctrine, sakala 15 aspects, six sheaths, fixed terms
vedyatā/pramātā/sakala). vv103-108 already have cm+am from prior runs.
Gates self-enforced: surfaces byte-exact, gloss paren-free no-LEAK, Q>=5
verse-owned, premises >=3 words each and >=3 count, plain >=4 words.
"""
from __future__ import annotations
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "process" / "beam" / "runs"
SONG = "tal-a10"

# cm rows: (lemma, morph, grounds) — lemma == surface exactly
# am: question / premises / inference / uncertainties / plain_english
V: dict[int, dict] = {
97: {
 "m": [
  ("avedyameva", "nom.sg.n + indecl.", "a-vedya + eva; perception is imperceptible"),
  ("bhānaṃ", "nom.sg.n", "perception; subject of the claim"),
  ("hi", "indecl.", "emphatic particle"),
  ("tathā", "indecl.", "thus; manner of inquiry"),
  ("kamanuyuñjmahe", "1pl.pres.mid √anuyuj", "we inquire into it"),
  ("evaṃ", "indecl.", "in this way"),
  ("pañcadaśātmeyaṃ", "nom.sg.n (compound)", "this fifteen-aspected; pañcadaśa-ātman-idam"),
  ("dharā", "nom.sg.f", "earth; first tattva in the series"),
  ("tadvajjalādayaḥ", "nom.pl.n (compound)", "water and the like; tadvat-jala-ādi"),
 ],
 "a": {
  "question": "What does the inquiry establish about perceptibility of the fifteen-aspected earth?",
  "premises": [
   "Perception itself is imperceptible indeed",
   "We inquire into it in this way",
   "This fifteen-aspected earth and waters are endowed"],
  "inference": "Perception is imperceptible; the fifteen-aspected earth and waters are the field.",
  "uncertainties": ["kamanuyuñjmahe segmentation: kam + anuyuñjmahe vs kama- compound"],
  "plain_english": "Indeed perception itself is imperceptible; in this way we inquire — this fifteen-aspected earth, and water and the like.",
 },
},
98: {
 "m": [
  ("avyaktāntā", "nom.sg.n (compound)", "unmanifest-end; avyakta-anta"),
  ("yato@styeṣāṃ", "gen.pl + 3sg.pres", "from whom of them; yatas + asti + eṣām"),
  ("sakalaṃ", "acc.sg.m", "sakala; fixed perceiver name, object of prati"),
  ("prati", "indecl. (prep.)", "toward; governs sakalaṃ"),
  ("vedyatā", "nom.sg.f", "perceptibility; fixed epistemic term"),
  ("yattūcyate", "3sg.pres.pass √vac", "that which is said; yat + tu + ucyate"),
  ("kalādyena", "inst.sg.n (compound)", "from kalā; kalā-ādi, start of tattva range"),
  ("dharāntena", "inst.sg.n (compound)", "to earth; dharā-anta, end of range"),
  ("samanvitāḥ", "nom.pl.m ppp √sam-anv-āp", "endowed with; agrees with vedyatā"),
 ],
 "a": {
  "question": "What perceptibility is said to extend from unmanifest-end down to earth?",
  "premises": [
   "From the unmanifest-end of them",
   "Perceptibility toward sakala is said",
   "Endowed from kalā down to earth"],
  "inference": "Sakala's perceptibility runs from kalā through to earth.",
  "uncertainties": ["avyaktāntā scope: end-of-unmanifest as source vs locus"],
  "plain_english": "From their unmanifest-end, perceptibility toward sakala is said — endowed from kalā down to earth.",
 },
},
99: {
 "m": [
  ("sakalā", "nom.sg.f", "Sakala; perceiver name, feminine surface form"),
  ("iti", "indecl.", "quotation/summary marker"),
  ("tatkośaṣaṭkodrekopalakṣaṇam", "nom.sg.n (compound)", "marked by excess of its six sheaths"),
  ("udbhūtāśuddhacidrāgakalādirasakañcukāḥ", "nom.pl.m (compound)", "sheaths of arisen impure consciousness attachment kalā rasa"),
 ],
 "a": {
  "question": "Why is sakala characterized by the excess of its six sheaths?",
  "premises": [
   "Sakala is thus named",
   "Marked by the excess of its six sheaths",
   "Sheaths of arisen impure consciousness attachment kalā rasa"],
  "inference": "Sakala's name rests on the surplus of the six sheaths.",
  "uncertainties": ["sakalā case: nominative name vs genitive of sakala", "six-sheath list segmentation approximate"],
  "plain_english": "Sakala is so called by the excess of its six sheaths — the sheaths of arisen impure consciousness, attachment, kalā and the rest, of rasa.",
 },
},
100: {
 "m": [
  ("sakalālayasaṃjñāstu", "nom.pl.f (compound) + indecl.", "the ones named sakala-abode; plus tu"),
  ("nyagbhūtākhilakañcukāḥ", "nom.pl.n (compound)", "all sheaths subdued; nyag-bhūta + akhila + kañcuka"),
  ("jñānākalāstu", "nom.pl.f (compound) + indecl.", "knowledge-akalās; plus tu"),
  ("dhvastaitatkañcukā", "nom.sg.f (compound)", "that sheath destroyed; dhvasta + etat + kañcukā"),
  ("iti", "indecl.", "thus; conclusion marker"),
  ("nirṇayaḥ", "nom.sg.m", "conclusion"),
 ],
 "a": {
  "question": "What conclusion follows for sakala-abode and knowledge-akalā?",
  "premises": [
   "The ones named sakala-abode have all sheaths subdued",
   "Knowledge-akalās have that sheath destroyed",
   "Thus is the conclusion"],
  "inference": "Sakala-abode subdues all sheaths; jñānākalā destroys that sheath — so the conclusion.",
  "uncertainties": [],
  "plain_english": "The ones named sakala-abode have all sheaths subdued; the knowledge-akalās have that sheath destroyed — thus the conclusion.",
 },
},
101: {
 "m": [
  ("tena", "inst.sg.m", "by that; causal connective"),
  ("pradhāne", "loc.sg.n", "in pradhāna; pradhāna as object"),
  ("vedye@pi", "loc.sg.n + indecl.", "even when known; vedyatva + pi"),
  ("pumānudbhūtakañcukaḥ", "nom.sg.m (compound)", "man with arisen sheath"),
  ("pramātāstyeva", "nom.sg.m + 3sg.pres + indecl.", "the perceiver is indeed; pramātā + asti + eva"),
  ("sakalaḥ", "nom.sg.m", "sakala; fixed perceiver name"),
  ("pāñcadaśyamataḥ", "gen.sg.n (compound)", "according to fifteen-aspect doctrine; pāñcadaśya + mataḥ"),
  ("sthitam", "nom.sg.n ppp √sthā", "established"),
 ],
 "a": {
  "question": "Which perceiver stands established by the fifteen-aspect doctrine?",
  "premises": [
   "Therefore even in pradhāna as object",
   "The man with arisen sheath is the perceiver indeed sakala",
   "Established according to fifteen-aspect doctrine"],
  "inference": "Even knowing pradhāna, the perceiver with sheath is sakala by fifteen-aspect doctrine.",
  "uncertainties": ["pumān scope: individual puruṣa vs generic man"],
  "plain_english": "Therefore even in pradhāna as object, the man with arisen sheath — the perceiver is indeed sakala, established according to the fifteen-aspect doctrine.",
 },
},
102: {
 "m": [
  ("pāñcadaśyaṃ", "nom/acc.sg.n", "fifteen-fold; adjective from pāñcadaśa"),
  ("dharādhantarniviṣṭe", "loc.sg.n (compound)", "situated within earth to its end"),
  ("sakale@pi", "loc.sg.n + indecl.", "even in sakala; sandhi sakale + pi"),
  ("ca", "indecl.", "and"),
  ("sakalāntaramastyeva", "nom.sg.n + 3sg.pres + indecl.", "there is indeed an interior of sakala"),
  ("prameye@trāpi", "loc.sg.n + indecl.", "even in the object of knowledge; prameya + tra + api"),
  ("mātṛ", "nom.sg.m", "knower; perceiver taxonomy term"),
  ("hi", "indecl.", "indeed"),
 ],
 "a": {
  "question": "Where does the knower appear even within the object of knowledge?",
  "premises": [
   "The fifteen-fold sakala situated within earth to its end",
   "Even in sakala there is an interior of sakala",
   "Even in the object of knowledge the knower is indeed"],
  "inference": "Sakala nests within earth and within itself; the knower stands even in the object.",
  "uncertainties": ["dharādhantarniviṣṭe: within-earth-until-end vs within-earth-interior"],
  "plain_english": "The fifteen-fold sakala, situated within earth to its end, even in sakala has an interior of sakala; even in the object of knowledge the knower is indeed.",
 },
},
}

# gloss rows already on disk for vv97-102; rewrite them byte-identical from working-t1
# so the cluster is fully owned by this hand-draft (surfaces must match exactly).
GLOSS_SOURCE = {
97: [
  ("avedyameva", "not-perceptible-indeed", "morphology: a-vedya-m + eva; brief places verse 97 in perceptibility doctrine"),
  ("bhānaṃ", "perception", "morphology: bhāna (shining/perception)"),
  ("hi", "indeed", "particle hi"),
  ("tathā", "thus", "adverb tathā"),
  ("kamanuyuñjmahe", "we-inquire", "morphology: first-person plural verb anuyuj"),
  ("evaṃ", "thus", "adverb evam"),
  ("pañcadaśātmeyaṃ", "this-fifteen-aspect", "morphology: pañcadaśa + ātman + idam"),
  ("dharā", "earth", "noun dharā"),
  ("tadvajjalādayaḥ", "water-and-the-like", "morphology: tadvat + jala + ādi"),
],
98: [
  ("avyaktāntā", "unmanifest-ending", "compound avyakta+anta; perceptibility doctrine context"),
  ("yato@styeṣāṃ", "from-whom-of-them", "sandhi yatas teṣām"),
  ("sakalaṃ", "sakala", "fixed pramatr name from brief"),
  ("prati", "toward", "preposition with vedyatā"),
  ("vedyatā", "perceptibility", "fixed epistemic term from brief"),
  ("yattūcyate", "that-which-is-said", "sandhi yat tu ucyate"),
  ("kalādyena", "from-kalā", "compound kalā+ādi; tattva range"),
  ("dharāntena", "to-earth", "compound dharā+anta"),
  ("samanvitāḥ", "endowed-with", "participle samanvita"),
],
99: [
  ("sakalā", "sakala", "feminine surface of fixed pramatr name sakala"),
  ("iti", "thus", "quotation/summary marker"),
  ("tatkośaṣaṭkodrekopalakṣaṇam", "marked-by-excess-of-six-sheaths", "compound tat-kośa-ṣaṭka-udreka-upalakṣaṇam"),
  ("udbhūtāśuddhacidrāgakalādirasakañcukāḥ", "arisen-impure-consciousness-attachment-kalā-sheaths", "compound udbhūta-aśuddha-cid-rāga-kalā-ādi-rasa-kañcukāḥ"),
],
100: [
  ("sakalālayasaṃjñāstu", "sakala-abode-named-ones", "compound sakala+ālaya+saṃjñā plus tu"),
  ("nyagbhūtākhilakañcukāḥ", "all-coverings-subdued", "compound nyag-bhūta+akhila+kañcuka"),
  ("jñānākalāstu", "knowledge-akalās", "compound jñāna+akalā plus tu; vidya/akala rung"),
  ("dhvastaitatkañcukā", "that-covering-destroyed", "compound dhvasta+etat+kañcukā"),
  ("iti", "thus", "indeclinable particle"),
  ("nirṇayaḥ", "conclusion", "noun nominative singular"),
],
101: [
  ("tena", "by-that", "instrumental of tad"),
  ("pradhāne", "in-principal", "locative of pradhāna"),
  ("vedye@pi", "even-when-known", "vedya + pi; sandhi form"),
  ("pumānudbhūtakañcukaḥ", "man-with-manifested-sheath", "compound pumān + udbhūta + kañcuka"),
  ("pramātāstyeva", "perceiver-is-indeed", "pramātā + asti + eva; perceiver taxonomy"),
  ("sakalaḥ", "sakala-perceiver", "fixed pramatr term; nominative sakala"),
  ("pāñcadaśyamataḥ", "according-to-fifteen-aspect-doctrine", "pāñcadaśya + mataḥ; sakala has 15 aspects"),
  ("sthitam", "established", "past participle of sthā"),
],
102: [
  ("pāñcadaśyaṃ", "fifteen-fold", "neuter adjective from pāñcadaśa; sakala has 15 aspects"),
  ("dharādhantarniviṣṭe", "situated-within-earth", "compound dharā-adha-antar-niviṣṭe"),
  ("sakale@pi", "even-in-sakala", "locative sakale + sandhi pi"),
  ("ca", "and", "conjunction"),
  ("sakalāntaramastyeva", "there-is-indeed-interior-of-sakala", "compound sakala-antaram + asti eva"),
  ("prameye@trāpi", "even-in-object-of-knowledge", "locative prameye + sandhi trāpi"),
  ("mātṛ", "knower", "nominative mātṛ; perceiver taxonomy"),
  ("hi", "indeed", "indeclinable particle"),
],
}


def main() -> None:
    # load working-t1 surfaces for byte-exact check
    wt = json.loads(
        (Path(__file__).resolve().parent.parent / "working-t1-tal-a10.json").read_text()
    )
    byv = {e["verse"]: e for e in wt}
    n = 0
    for v, d in V.items():
        surfs = [t["surface"] for t in byv[v]["tokens"]]
        # gloss
        grows = GLOSS_SOURCE[v]
        assert [g[0] for g in grows] == surfs, (v, "gloss surface drift")
        for r in grows:
            assert len(r) == 3 and all(s.strip() for s in r), (v, "gloss row", r)
            g = r[1]
            assert "(" not in g and ")" not in g and '"' not in g, (v, g)
            assert len(g.split("-")) <= 15, (v, g)
            LEAK = ("genitive", "nominative", "accusative", "instrumental", "dative",
                    "ablative", "locative", "vocative", "singular", "plural", "dual",
                    "participle", "passive", "causative", "optative", "imperative",
                    "sandhi", "compound")
            assert not any(w in g.lower().split("-") for w in LEAK), (v, g)
        # cm
        mrows = d["m"]
        assert [m[0] for m in mrows] == surfs, (v, "cm surface drift")
        for r in mrows:
            assert len(r) == 3 and all(s.strip() for s in r), (v, "cm row", r)
        # am gates
        a = d["a"]
        assert a["question"].endswith("?") and len(a["question"].split()) >= 5, v
        lq = a["question"].lower()
        assert "does verse" not in lq and "this verse" not in lq and "is being told" not in lq, v
        assert len(a["premises"]) >= 3, v
        assert all(len(p.split()) >= 3 for p in a["premises"]), v
        assert len(a["plain_english"].split()) >= 4, v
        # write gloss
        gd = RUNS / f"{SONG}-gloss-v{v:02d}"
        gd.mkdir(parents=True, exist_ok=True)
        (gd / "gloss.json").write_text(json.dumps(
            {"song": SONG, "verse": v,
             "rows": [{"surface": s, "gloss": g, "grounds": gr} for s, g, gr in grows]},
            indent=1, ensure_ascii=False))
        n += 1
        # write cm
        cd = RUNS / f"{SONG}-cm-v{v:02d}"
        cd.mkdir(parents=True, exist_ok=True)
        (cd / "cm.json").write_text(json.dumps(
            {"song": SONG, "verse": v,
             "rows": [{"lemma": s, "morph": m, "grounds": gr} for s, m, gr in mrows]},
            indent=1, ensure_ascii=False))
        n += 1
        # write am
        ad = RUNS / f"{SONG}-am-v{v:02d}"
        ad.mkdir(parents=True, exist_ok=True)
        (ad / "am.json").write_text(json.dumps(
            {"song": SONG, "verse": v, **a}, indent=1, ensure_ascii=False))
        n += 1
    print(f"wrote {n} files (vv97-102 gloss+cm+am)")


if __name__ == "__main__":
    main()
