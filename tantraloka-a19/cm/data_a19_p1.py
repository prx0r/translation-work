"""a19 v1-10 data (sadyo-utkranti, 56u/453tok)."""
import sys; sys.path.insert(0,'tools')
from workcfg import source_spans
spans = source_spans('tantraloka-a19')
TOK = {}; CM = {}; GLOSS = {}; QE = {}
ROWS = {}

# v1
v=1
ROWS[1]=[
 ("atha", "indecl", "now (opener)"),
 ("sadyaḥ-samutkrānti-pradā", "f.nom.sg (pra + dā)", "giving immediate departure"),
 ("dīkṣā", "f.nom.sg", "initiation (subject)"),
 ("nirūpyate", "3sg.pres.pass (nir + rūp)", "is set forth"),
 ("tatkṣaṇāt + ca + upabhoga + advā", "abl + particle + m.abl.sg + particle, fused", "from that moment — or from enjoyment"),
 ("deha-pāta", "m.loc.sg", "at body's fall"),
 ("śivaṃ", "m.acc.sg", "Śiva (object)"),
 ("vrajet", "opt (vraj)", "may go"),
 ("iti + uktyā", "particle + f.inst.sg, fused", "thus by saying"),
 ("mālinī-śāstra", "n.loc.sg", "in the Mālinīśāstra"),
 ("sūcitā + asau", "f.nom.sg ppp + dem, fused", "hinted — it"),
 ("maheśinā", "m.inst.sg", "by the Great Lord"),
]
GLOSS[1]=['now','giving-immediate-departure','initiation','is-set-forth','from-that-moment-or-from-enjoyment','at-bodys-fall','Śiva','may-go','thus-by-saying','in-Mālinīśāstra','hinted—it','by-Great-Lord']
QE[1]="Now the initiation giving immediate departure is set forth: from that moment, or from enjoyment, at body's fall one may go to Śiva — so hinted in the Mālinīśāstra by the Great Lord."
# v2
v=2
ROWS[2]=[
 ("deha-pāta", "m.loc.sg", "at body's fall"),
 ("samīpasthe", "m.loc.sg (samīpa + stha)", "when death is near"),
 ("śaktipāta-sphuṭatvataḥ", "abl", "from śaktipāta's clearness"),
 ("āsādya", "gerund (ā + sad)", "having obtained"),
 ("śāṃkarīṃ", "f.acc.sg", "Śāṃkara (initiation)"),
 ("dīkṣāṃ", "f.acc.sg", "initiation (object)"),
 ("tasmāddīkṣākṣaṇātparam", "adv + abl + adv, fused", "hence from initiation-moment supreme"),
]
GLOSS[2]=['at-bodys-fall','when-death-is-near','from-śaktipātas-clearness','having-obtained','Śāṃkara','initiation','hence-from-initiation-moment-supreme']
QE[2]="At body's fall, when death is near, from śaktipāta's clearness, having obtained Śāṃkara initiation: hence from the initiation-moment, the supreme."
# v3
v=3
ROWS[3]=[
 ("śivaṃ", "m.acc.sg", "Śiva (object)"),
 ("vrajedityartho@tra", "opt + particle, fused (print @ = elided-a)", "may go — the meaning here"),
 ("pūrva-apara-vivecanāt", "abl", "from prior-posterior discernment"),
 ("vyākhyātaḥ", "m.nom.sg (vi + ā + khyā ppp)", "was explained"),
 ("śrīmatāsmākaṃ", "m.inst.sg + gen.pl, fused", "by the venerable our"),
 ("guruṇā", "m.inst.sg", "by the guru"),
 ("śambhu-mūrtinā", "m.inst.sg", "by Śambhu-formed (Śambhunātha)"),
]
GLOSS[3]=['Śiva','may-go-the-meaning-here','from-prior-posterior-discernment','was-explained','by-the-venerable-our','by-the-guru','by-Śambhu-formed']
QE[3]="The meaning 'may go to Śiva' was explained here, from prior-posterior discernment, by our venerable guru Śambhunātha."
# v4
v=4
ROWS[4]=[
 ("yadā + hi", "rel adv + particle, fused", "when — for"),
 ("āsanna-maraṇe", "m.loc.sg", "when death is near"),
 ("śaktipātaḥ", "m.nom.sg", "śaktipāta (subject)"),
 ("prajāyate", "3sg.pres.mid (pra + jan)", "arises"),
 ("tatra", "adv", "there"),
 ("mande + atha", "m.loc.sg + adv, fused", "in mild — then"),
 ("guru-ādi-sevayā + āyuḥ", "f.inst.sg + n.nom.sg, fused", "by guru-and-the-rest service — life"),
 ("kṣayaṃ", "m.acc.sg", "to diminution (object)"),
 ("vrajet", "opt (vraj)", "may go"),
]
GLOSS[4]=['when—for','when-death-is-near','śaktipāta','arises','there','in-mild—then','by-guru-and-the-rest-service—life','to-diminution','may-go']
QE[4]="When death is near and śaktipāta arises, there, in mild cases, by guru-service life may go to diminution."
# v5
v=5
ROWS[5]=[
 ("athavā", "particle", "or else"),
 ("bandhu-mitrādi-dvārā", "m.inst.sg", "through kin-friends-and-the-rest"),
 ("sā + asya", "f.nom.sg + gen.sg, fused", "she — of his"),
 ("vibhoḥ", "m.gen.sg", "of the Omnipresent"),
 ("patet", "3sg.pres (pat)", "falls"),
 ("pūrvaṃ", "adv", "before"),
 ("vā", "particle", "or"),
 ("samayī", "m.nom.sg", "samayin"),
 ("na + eva", "particle + particle, fused", "not at all"),
 ("parāṃ", "f.acc.sg", "supreme"),
 ("dīkṣāmavāptavān", "f.acc.sg + m.nom.sg ppp, fused", "initiation — has obtained"),
]
GLOSS[5]=['or-else','through-kin-friends-and-the-rest','she—of-his','of-the-Omnipresent','falls','before','or','samayin','not-at-all','supreme','initiation—has-obtained']
QE[5]="Or else, through kin-friends-and-the-rest, the Omnipresent's [grace] falls; or before, the samayin has not at all obtained supreme initiation."
# v6
v=6
ROWS[6]=[
 ("āpta-dīkṣaḥ + api", "m.nom.sg + particle, fused", "initiated even"),
 ("vā", "particle", "or"),
 ("prāṇān + jihāsuḥ", "m.acc.pl + m.nom.sg (hā desid.), fused", "desiring to abandon life-breaths"),
 ("kleśa-varjita", "m.nom.sg", "freed from affliction"),
 ("antya + guru + tadā", "adj + m.nom.sg + adv, fused", "the final guru — then"),
 ("kuryāt + sadya + utkrānti + dīkṣaṇa", "opt + adj + f.acc.sg + n.acc.sg, fused", "should perform — immediate-departure initiation"),
]
GLOSS[6]=['initiated-even','or','desiring-to-abandon-life-breaths','freed-from-affliction','the-final-guru—then','should-perform—immediate-departure-initiation']
QE[6]="Even the initiated, desiring to abandon life-breaths, freed from affliction: the final guru should then perform immediate-departure initiation."
# v7
v=7
ROWS[7]=[
 ("na + tu + apakva-male", "particle + particle + m.loc.sg, fused", "but not — in immature impurity"),
 ("na + api", "particle + particle, fused", "nor even"),
 ("śeṣa-kārmika-vigraha", "m.loc.sg", "in remaining-karmic-body"),
 ("kuryādutkramaṇaṃ", "opt + n.acc.sg, fused (print form)", "should perform departure"),
 ("śrīmat + gahvara", "n.loc.sg + n.loc.sg, fused", "in the venerable Gahvara"),
 ("ca", "particle", "and"),
 ("nirūpita", "n.nom.sg (nir + rūp ppp)", "was set forth"),
]
GLOSS[7]=['but—not—in-immature-impurity','nor-even','in-remaining-karmic-body','should-perform-departure','in-the-venerable-Gahvara','and','was-set-forth']
QE[7]="But not in immature impurity, nor even in remaining-karmic-body, should departure be performed: so set forth in the venerable Gahvara."
# v8
v=8
ROWS[8]=[
 ("dṛṣṭvā", "gerund (dṛś)", "having seen"),
 ("śiṣyaṃ", "m.acc.sg", "the disciple"),
 ("jarā-grasta", "m.acc.sg", "age-seized"),
 ("vyādhinā", "m.inst.sg", "by disease"),
 ("paripīḍita", "m.acc.sg (pari + pīḍ ppp)", "oppressed"),
 ("utkramayya", "gerund (ut + kram caus)", "having made depart"),
 ("tatastvenaṃ", "adv + m.acc.sg + m.acc.sg, fused", "then — him — this"),
 ("paratattve", "n.loc.sg", "in the supreme principle"),
 ("niyojayet", "opt caus (ni + yuj)", "he should join"),
]
GLOSS[8]=['having-seen','the-disciple','age-seized','by-disease','oppressed','having-made-depart','then—him—this','in-the-supreme-principle','he-should-join']
QE[8]="Having seen the disciple age-seized, oppressed by disease, having made depart, then he should join this one in the supreme principle."
# v9
v=9
ROWS[9]=[
 ("viśeṣaṇaviśeṣyatve", "n.loc.sg", "in the qualifier-qualified relation"),
 ("kāmacāravidhānataḥ", "abl", "from desire-conduct-arrangement"),
 ("pūrvoktamarthajātaṃ", "n.acc.sg ppp", "aforesaid things"),
 ("śrīśambhunātra", "m.inst.sg + adv, fused", "by venerable Śambhunātha here"),
 ("nirūpitam", "n.nom.sg (nir + rūp ppp)", "was set forth"),
]
GLOSS[9]=['in-the-qualifier-qualified-relation','from-desire-conduct-arrangement','aforesaid-things','by-venerable-Śambhunātha-here','was-set-forth']
QE[9]="In the qualifier-qualified relation, from desire-conduct-arrangement, the aforesaid things were here set forth by venerable Śambhunātha."
# v10
v=10
ROWS[10]=[
 ("vidhiṃ", "m.acc.sg", "the rite (object)"),
 ("pūrvoditaṃ", "m.acc.sg ppp", "aforesaid"),
 ("sarvaṃ", "n.acc.sg", "all"),
 ("kṛtvā", "gerund (kṛ)", "having performed"),
 ("samayaśuddhitaḥ", "abl", "from samaya-purity"),
 ("kṣurikāmasya", "f.acc.sg + gen.sg, fused", "his knife"),
 ("vinyasyejjvalantīṃ", "opt + f.acc.sg, fused", "he should place blazing"),
 ("marmakartarīm", "f.acc.sg", "the marma-scissors"),
]
GLOSS[10]=['the-rite','aforesaid','all','having-performed','from-samaya-purity','his-knife','he-should-place-blazing','the-marma-scissors']
QE[10]="Having performed all the aforesaid rite, from samaya-purity, he should place his blazing marma-scissors knife."

# ---- populate TOK/CM/GLOSS/QE from ROWS (v1-10) ----
import sys
sys.path.insert(0, 'tools')
from workcfg import source_spans
spans = source_spans('tantraloka-a19')
for v in list(ROWS.keys()):
    TOK[v] = list(spans[v])
    assert TOK[v] == list(spans[v]), 'TOK mismatch v%d'%v
    assert len(ROWS[v]) == len(spans[v]), 'ROW COUNT v%d: %d vs %d'%(v,len(ROWS[10]),len(spans[v]))
    assert len(GLOSS[v]) == len(spans[v]), 'GLOSS COUNT v%d'%(v,)
    assert v in QE
    CM[v] = [r for r in ROWS[v]]
    assert all(isinstance(r,(list,tuple)) and len(r)==3 for r in CM[v])
print('a19 part1 verified: %d verses, %d tokens'%(len(TOK), sum(len(v) for v in TOK.values())))
