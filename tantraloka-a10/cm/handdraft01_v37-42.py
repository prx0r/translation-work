#!/usr/bin/env python3
"""Assessor hand-draft tal-a10 vv37-42 (gloss+cm+am). Smallest failed cluster.

Provenance: tal-a10-triple-v37 failed 6/6 (content gates: bad row 'ṇyarthaḥ'
gloss with LEAK 'causative' x2, surface drift, question rejected, split after
schema fail). Per largetext SKILL: escalate to assessor hand-draft. Content
from working-t1 surfaces + source spans (concat-sha ed6a1ec39b514274) +
tal-a10 brief (vastudharma engine 19-78: prakāśa/vetrüchtigkeit argument;
pramatr taxonomy kept exact; ṇy-artha section vv36-49: causal sense literal
for inert objects, figurative with consciousness — Caitra/master example
vv39-40). Gates self-enforced (surfaces byte-exact, gloss lowercase
hyphen-joined no parens/quotes <=15 parts no grammar words, Q>=5 words
verse-owned, premises >=3 words each >=3 premises, plain >=4 words,
uncertainties honest). Cluster vv37-48: 43-48 already run + pass; this
completes the song's runs for the task.
"""
from __future__ import annotations
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "process" / "beam" / "runs"
SONG = "tal-a10"

V: dict[int, dict] = {
37: {
 "g": [
  ("tathā", "thus", "indecl tathā; continues the showing just argued"),
  ("cedaṃ", "and-this", "ca + idam n; and this (thing shown); conditional ce also possible"),
  ("darśayāmaḥ", "we-show", "1pl.pres.act √dṛś with -aya stem; we make it seen"),
  ("kiṃ", "what", "indecl interrog; what then?"),
  ("prakāśaḥ", "light", "m.nom.sg prakāśa; the light, the luminous"),
  ("prakāśate", "shines", "3sg.pres.mid √prakāś; it shines"),
  ("aprakāśo@pi", "even-not-luminous", "aprakāśa + api; even non-luminous"),
  ("naivāsau", "not-indeed-it", "na + eva + asau; that is not [so] at all"),
  ("tathāapi", "and-so-also", "tathā + api; and so also, likewise"),
  ("ca", "and", "indecl; and"),
  ("na", "not", "indecl; not"),
  ("kiṃcana", "anything-at-all", "indecl kiṃcana; anything whatsoever"),
 ],
 "m": [
  ("tathā", "indecl.", "thus"),
  ("cedaṃ", "n.nom/acc.sg + indecl. (ca + idam)", "and this"),
  ("darśayāmaḥ", "1pl.pres.act √dṛś", "we show"),
  ("kiṃ", "indecl.", "what"),
  ("prakāśaḥ", "m.nom.sg", "light"),
  ("prakāśate", "3sg.pres.mid √prakāś", "it shines"),
  ("aprakāśo@pi", "m.nom.sg + indecl. (aprakāśa + api)", "even non-luminous"),
  ("naivāsau", "indecl. + m.nom.sg (na + eva + asau)", "not indeed it"),
  ("tathāapi", "indecl. (tathā + api)", "and so also"),
  ("ca", "indecl.", "and"),
  ("na", "indecl.", "not"),
  ("kiṃcana", "indecl.", "anything at all"),
 ],
 "a": {
  "question": "Does light shine on it when nothing at all is unlit?",
  "premises": [
   "We show this thing before us",
   "Light itself is what would have to shine on it",
   "That thing is not without its own light",
   "Nothing at all stands without light"],
  "inference": "Since nothing is unlit, showing requires no second light.",
  "uncertainties": ["cedaṃ read ca + idam; conditional ce + idam also possible"],
  "plain_english": "And so we show this: what, does light shine? That thing is not without light either — and so nothing at all is.",
 },
},
38: {
 "g": [
  ("tarhi", "then", "indecl tarhi; at this point in the debate"),
  ("loke", "in-world", "loc.sg.n loka; in worldly usage"),
  ("kathaṃ", "how", "indecl interrog; how then"),
  ("ṇyarthaḥ", "causal-sense", "m.nom.sg ṇy-artha; the -ṇy verbal derivative's force"),
  ("ucyate", "is-spoken", "3sg.pres.mid √vac; is spoken of"),
  ("cetanasthitau", "in-conscious-standing", "loc.sg.f cetana-sthiti; as regards what abides as consciousness"),
  ("mukhyo", "primary", "m.nom.sg mukhya; primary, literal"),
  ("ṇyarthasya", "of-causal-sense", "gen.sg.m ṇy-artha; of the causal sense"),
  ("viṣayo", "field", "m.nom.sg viṣaya; the proper domain"),
  ("jaḍeṣu", "among-inert-things", "loc.pl.n jaḍa; among inert things"),
  ("tvaupacārikaḥ", "but-figurative", "tu + upacārika m.nom.sg; toward the conscious only figurative"),
 ],
 "m": [
  ("tarhi", "indecl.", "then"),
  ("loke", "loc.sg.n", "in worldly usage"),
  ("kathaṃ", "indecl.", "how"),
  ("ṇyarthaḥ", "m.nom.sg", "causal sense"),
  ("ucyate", "3sg.pres.mid √vac", "is spoken of"),
  ("cetanasthitau", "loc.sg.f (cetana-sthiti)", "as regards what abides in consciousness"),
  ("mukhyo", "m.nom.sg", "primary"),
  ("ṇyarthasya", "gen.sg.m", "of the causal sense"),
  ("viṣayo", "m.nom.sg", "field"),
  ("jaḍeṣu", "loc.pl.n", "among inert things"),
  ("tvaupacārikaḥ", "m.nom.sg (tu + upacārika)", "but figurative"),
 ],
 "a": {
  "question": "How then is causal sense used in the case of what abides in consciousness?",
  "premises": [
   "In worldly usage causal sense is spoken of with consciousness",
   "Its primary field lies among the inert things",
   "Toward what abides in consciousness it is only figurative"],
  "inference": "Causal agency is literal for the inert and figurative for consciousness.",
  "uncertainties": ["cetanasthitau scope (as regards the conscious agent or object) left open", "tvaupacārikaḥ read tu + upacārikaḥ"],
  "plain_english": "Then how is causal sense spoken of in the world when what abides is conscious? Its primary field is among the inert; toward consciousness it is only figurative.",
 },
},
39: {
 "g": [
  ("tathāhi", "thus-for-instance", "tathā + hi; for instance"),
  ("gantuṃ", "to-go", "inf. √gam; to go"),
  ("śakto@pi", "able-even", "śakta + api m.nom.sg; though able"),
  ("caitro@nyāyattatāṃ", "caitra-reliance-on-other", "caitraḥ + anyāyattatām acc.f; Caitra's reliance on another"),
  ("gateḥ", "of-going", "gen.sg.f gati; of the going"),
  ("manvāna", "thinking", "m.nom.sg pres.ptcp √man; thinking it so"),
  ("eva", "indeed", "indecl; emphatic"),
  ("vaktyasmi", "he-speaks-i-am", "vakti + asmi; he speaks: I am... quotation opens"),
  ("gamitaḥ", "gone", "m.nom.sg √gam; gone, arrived"),
  ("svāmineti", "o-master-quoted", "svāmin voc + iti; Master! + quotation particle"),
  ("hi", "indeed", "indecl; verily"),
 ],
 "m": [
  ("tathāhi", "indecl. (tathā + hi)", "for instance"),
  ("gantuṃ", "inf. (√gam)", "to go"),
  ("śakto@pi", "m.nom.sg + indecl. (śakta + api)", "though able"),
  ("caitro@nyāyattatāṃ", "m.nom.sg + acc.sg.f (caitra + anyāyattatā)", "Caitra's reliance on another"),
  ("gateḥ", "gen.sg.f", "of the going"),
  ("manvāna", "m.nom.sg pres.ptcp (√man)", "thinking"),
  ("eva", "indecl.", "indeed"),
  ("vaktyasmi", "3sg.pres.act (√vac) + 1sg.pres (√as)", "he speaks: I am"),
  ("gamitaḥ", "m.nom.sg (√gam)", "gone"),
  ("svāmineti", "voc.sg.m + indecl. (svāmin + iti)", "master! + quotation"),
  ("hi", "indecl.", "indeed"),
 ],
 "a": {
  "question": "What does Caitra say when he takes his going to depend on another?",
  "premises": [
   "Though able to go Caitra takes the going as another's",
   "Thinking that dependence he speaks out",
   "He names himself gone before his master"],
  "inference": "Caitra casts his own going as another's act.",
  "uncertainties": ["vaktyasmi segmented vakti + asmi with the quotation opening at asmi", "anyāyattatāṃ construction with genitive gateḥ — dependence-of-the-going reading kept"],
  "plain_english": "Thus though Caitra is able to go, taking the going as dependent on another, thinking so he speaks: I am gone, master.",
 },
},
40: {
 "g": [
  ("svāmyapyasya", "master-also-his", "svāmī + api + asya gen; the master too, of his going"),
  ("gatau", "in-going", "loc.sg.f gati; in the going"),
  ("śaktiṃ", "power", "acc.sg.f √śak; the capacity"),
  ("buddhvā", "having-known", "gerund √budh; having known"),
  ("svādhīnatāṃ", "dependence", "acc.sg.f sva-ādhīna-tā; dependence on the other"),
  ("sphuṭam", "clearly", "indecl; plainly, clearly"),
  ("paśyannivṛttimāśaṃkya", "seeing-cessation-fearing", "paśyan + nivṛttim + āśaṃkya ger.; seeing cessation and fearing it"),
  ("gamayāmīti", "i-shall-make-go", "gamayāmi + iti; I shall cause to go + quotation"),
  ("bhāṣate", "speaks", "3sg.pres.mid √bhāṣ; he says"),
 ],
 "m": [
  ("svāmyapyasya", "m.nom.sg + gen.sg.m (svāmī + api + asya)", "the master too, his"),
  ("gatau", "loc.sg.f", "in the going"),
  ("śaktiṃ", "acc.sg.f", "power"),
  ("buddhvā", "gerund (√budh)", "having known"),
  ("svādhīnatāṃ", "acc.sg.f (sva-ādhīna-tā)", "dependence"),
  ("sphuṭam", "indecl.", "clearly"),
  ("paśyannivṛttimāśaṃkya", "m.nom.sg + acc.sg.f + gerund (paśyan + nivṛtti + āśaṃk)", "seeing cessation and fearing it"),
  ("gamayāmīti", "1sg.pres.act (√gam, gamayāmi) + indecl. (iti)", "I shall make go + quotation"),
  ("bhāṣate", "3sg.pres.mid √bhāṣ", "he says"),
 ],
 "a": {
  "question": "What does the master declare after knowing the power and fearing the stop?",
  "premises": [
   "The master too knows the power in that going",
   "He sees dependence clearly before him",
   "Fearing the stop he says he will make him go"],
  "inference": "The master casts himself as doer of a power that is another's.",
  "uncertainties": ["svādhīnatāṃ whose dependence — master's on Caitra or the reverse — left open", "asya gatau read as Caitra's power in the going"],
  "plain_english": "The master too, knowing the power in that going, seeing dependence plainly and fearing the stop, speaks: I shall make him go.",
 },
},
41: {
 "g": [
  ("preryaprerakayorevaṃ", "of-moved-and-mover-thus", "prerya-prerakayoḥ gen.dual + evam; of moved and mover, thus"),
  ("maulikī", "primary", "f.nom.sg maulika; original, primary"),
  ("ṇyarthasaṃgatiḥ", "causal-sense-connection", "f.nom.sg ṇy-artha-saṅgati; the connection of the causal sense"),
  ("tadabhiprāyato@nyo@pi", "another-also-from-his-intent", "tad-abhiprāyataḥ + anyaḥ + api; another too according to that intention"),
  ("loke", "in-world", "loc.sg.n loka; in worldly dealings"),
  ("vyavaharettathā", "would-act-thus", "3sg.opt.mid √vyavahṛ + tathā; would deal in the world accordingly"),
 ],
 "m": [
  ("preryaprerakayorevaṃ", "gen.dual (prerya-preraka) + indecl. (evam)", "of moved and mover, thus"),
  ("maulikī", "f.nom.sg", "primary"),
  ("ṇyarthasaṃgatiḥ", "f.nom.sg (ṇy-artha-saṅgati)", "causal connection"),
  ("tadabhiprāyato@nyo@pi", "indecl. (tad-abhiprāyataḥ) + m.nom.sg + indecl.", "another too from that intention"),
  ("loke", "loc.sg.n", "in worldly dealings"),
  ("vyavaharettathā", "3sg.opt.mid (√vyavahṛ) + indecl.", "would act accordingly"),
 ],
 "a": {
  "question": "Between moved and mover how does the causal connection primarily stand?",
  "premises": [
   "The causal connection is primary between moved and mover",
   "Another person too in the world acts accordingly",
   "He proceeds from that intention in the same way"],
  "inference": "The causal tie belongs to mover and moved; others follow by intention.",
  "uncertainties": ["tadabhiprāyataḥ read ablative via -tataḥ ('according to that intention') — segmentation open", "optative vyavaharet rendered conditionally"],
  "plain_english": "Thus the causal connection is primary between the moved and the mover; another too, in the world, acts accordingly, from that intention.",
 },
},
42: {
 "g": [
  ("śaraṃ", "arrow", "acc.sg.m śara; the arrow"),
  ("gamayatītyatra", "causes-to-go-here", "gamayati + iti + atra; he makes (it) go — here"),
  ("punarvegākhyasaṃskriyām", "again-impetus-named-operation", "punaḥ + vegākhyā-saṃskriyām acc.f; again the operation named impetus"),
  ("vidadhatprerakammanya", "posits-mover-thinking", "vidadhat + prerakam + manya; positing a mover, thinking it so"),
  ("upacāreṇa", "by-figuration", "instr.sg.n upacāra; by figurative attribution"),
  ("jāyate", "is-born", "3sg.pres.mid √jan; is born, arises"),
 ],
 "m": [
  ("śaraṃ", "acc.sg.m", "the arrow"),
  ("gamayatītyatra", "3sg.pres.act (√gam, gamayati) + indecl. + indecl.", "he makes go — here"),
  ("punarvegākhyasaṃskriyām", "acc.sg.f (punaḥ + vegākhyā-saṃskriyā)", "again the operation named impetus"),
  ("vidadhatprerakammanya", "m.nom.sg + acc.sg.m + m.nom.sg (vidadhat + preraka + manya)", "positing a mover, thinking it so"),
  ("upacāreṇa", "instr.sg.n", "by figuration"),
  ("jāyate", "3sg.pres.mid √jan", "it arises"),
 ],
 "a": {
  "question": "Who is posited as mover when one says the arrow is made to go?",
  "premises": [
   "In the phrase he makes the arrow go one posits",
   "An operation named impetus and takes it for the mover",
   "That posited mover arises only by figurative use"],
  "inference": "The mover here is born of attribution, not of agency.",
  "uncertainties": ["vidadhat read as present participle 'one who posits' — finite reading possible", "vega rendered impetus; momentum/speed also possible"],
  "plain_english": "Here, in the words he makes the arrow go, one who posits the operation named impetus, thinking it the mover — that mover arises by figuration alone.",
 },
},
}

# byte-exact surfaces from working-t1 / source spans
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
import workcfg
spans = workcfg.source_spans("tantraloka-a10")
wt = json.loads((Path(__file__).resolve().parent.parent / "working-t1-tal-a10.json").read_text())

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
print(f"wrote {n} files (vv37-42 gloss+cm+am) — self-gate PASS surfaces/Q/premises")
