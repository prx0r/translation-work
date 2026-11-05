"""a19 v31-40 data."""
import sys; sys.path.insert(0,'tools')
from workcfg import source_spans
spans = source_spans('tantraloka-a19')
TOK = {}; CM = {}; GLOSS = {}; QE = {}
ROWS = {}

ROWS[31]=[
 ("tattve","n.loc.sg","in-tattva"),
 ("vā","particle","or"),
 ("yatra","rel adv","wherever"),
 ("kutrāpi","adv","anywhere"),
 ("yojayetpudgalaṃ","opt caus + m.acc.sg, fused","he-should-join-the-person"),
 ("kramāt","adv","in-sequence"),
 ("samayī","m.nom.sg","samayin"),
 ("putrako","m.nom.sg","putraka"),
 ("vāpi","particle","or-even"),
 ("paṭhedvidyāmimāṃ","opt + f.acc.sg, fused","should-read-this-vidyā"),
 ("tathā","adv","thus"),
]
GLOSS[31]=['in-tattva','or','wherever','anywhere','he-should-join-the-person','in-sequence','samayin','putraka','or-even','should-read-this-vidyā','thus']
QE[31]="In tattva, wherever, anywhere, he should join the person in sequence: samayin or putraka should read this vidyā, thus."

ROWS[32]=[
 ("tatpāṭhāttu","abl + particle, fused","from-its-reading-but"),
 ("samayyuktāṃ","f.acc.sg","samaya-joined"),
 ("rudrāṃśāpattimaśnute","3sg.pres (aś)","attains-Rudra-share-arrival"),
 ("etau","m.nom.du","these-two"),
 ("jape","m.loc.sg","in-japa"),
 ("cādhyayane","m.loc.sg","and-in-study"),
 ("yasmādadhikṛtāvubhau","rel + m.nom.du, fused","since-both-authorized"),
]
GLOSS[32]=['from-its-reading-but','samaya-joined','attains-Rudra-share-arrival','these-two','in-japa','and-in-study','since-both-authorized']
QE[32]="From its reading but, samaya-joined attains Rudra-share-arrival: these two in japa and in study, since both authorized."

ROWS[33]=[
 ("nādhyāpanopadeśe","m.loc.sg","in-teaching-or-instructing"),
 ("vā","particle","or"),
 ("sa","dem","he"),
 ("eṣo@dhyayanādṛte","m.nom.sg","this-study-excepted"),
 ("paṭhatostvanayorvastusvabhāvāttasya","m.gen.du + n.abl.sg, fused","of-these-two-reading-by-its-nature-his"),
 ("sā","f.nom.sg","that"),
 ("gatiḥ","f.nom.sg","course"),
]
GLOSS[33]=['in-teaching-or-instructing','or','he','this-study-excepted','of-these-two-reading-by-its-nature-his','that','course']
QE[33]="In teaching or instructing, or: he, this study excepted — of these two reading, by its nature his, that course."

ROWS[34]=[
 ("yathā","rel adv","as"),
 ("niṣiddhabhūtādikarmā","m.nom.sg","forbidden-beings-and-the-rest-actions"),
 ("mantraṃ","m.acc.sg","mantra"),
 ("smaransvayam","pres.part + indecl, fused","remembering-himself"),
 ("āviṣṭe@pi","m.loc.sg + particle, fused","even-when-possessed"),
 ("kvacinnaiti","adv + pres, fused","somewhere-does-not-go"),
 ("lopaṃ","m.acc.sg","loss"),
 ("kartṛtvavarjanāt","abl","from-doership-abandoning"),
]
GLOSS[34]=['as','forbidden-beings-and-the-rest-actions','mantra','remembering-himself','even-when-possessed','somewhere-does-not-go','loss','from-doership-abandoning']
QE[34]="As forbidden-beings-and-the-rest actions, mantra remembering himself: even when possessed, somewhere does not go loss, from doership-abandoning."

ROWS[35]=[
 ("yathā","rel adv","as"),
 ("ca","particle","and"),
 ("vācayañśāstraṃ","pres.part (vac caus) + n.acc.sg, fused","causing-to-recite-scripture"),
 ("samayī","m.nom.sg","samayin"),
 ("śūnyaveśmani","n.loc.sg","in-empty-dwelling"),
 ("na","particle","not"),
 ("lupyate","3sg.pres.pass (lup)","is-lost"),
 ("tadantaḥsthaprāṇivargopakārataḥ","abl","from-that-inner-beings-group-benefiting"),
]
GLOSS[35]=['as','and','causing-to-recite-scripture','samayin','in-empty-dwelling','not','is-lost','from-that-inner-beings-group-benefiting']
QE[35]="As, and causing-to-recite scripture, samayin in empty-dwelling: not is lost, from that inner-beings-group-benefiting."

ROWS[36]=[
 ("tathā","adv","thus"),
 ("svayaṃ","indecl","himself"),
 ("paṭhanneṣa","m.nom.sg pres.part (paṭh)","reading-this"),
 ("vidyāṃ","f.acc.sg","vidyā"),
 ("vastusvabhāvataḥ","abl","from-thing-nature"),
 ("tasminmukte","m.loc.sg (muc ppp)","in-that-released"),
 ("na","particle","not"),
 ("lupyeta","opt pass (lup)","would-be-lost"),
 ("yato","rel adv","since"),
 ("kiṃcitkaro@tra","pres.part + adv, fused","doing-something-here"),
 ("saḥ","m.nom.sg","he"),
]
GLOSS[36]=['thus','himself','reading-this','vidyā','from-thing-nature','in-that-released','not','would-be-lost','since','doing-something-here','he']
QE[36]="Thus himself reading this vidyā, from thing-nature: in that released not would be lost, since doing-something-here he."

ROWS[37]=[
 ("nanu","particle","indeed"),
 ("cādīkṣitāgre","m.loc.sg","before-the-uninitiated"),
 ("sa","dem","he"),
 ("noccarecchāstrapaddhatim","opt + f.acc.sg, fused","should-not-recite-scripture-method"),
]
GLOSS[37]=['indeed','before-the-uninitiated','he','should-not-recite-scripture-method']
QE[37]="Indeed before the uninitiated he should not recite scripture-method."

ROWS[38]=[
 ("hanta","particle","well"),
 ("kuḍyāgrato@pyasya","m.loc.sg + particle, fused","before-the-wall-even-his"),
 ("niṣedhastvatha","m.nom.sg + adv, fused","prohibition-but-now"),
 ("kathyate","3sg.pres.pass (kath)","is-told"),
 ("paryudāsena","m.inst.sg","by-exception"),
 ("yaḥ","rel","who"),
 ("śrotumavadhārayituṃ","inf + inf, fused","to-hear-to-ascertain"),
 ("kṣamaḥ","m.nom.sg","is-capable"),
]
GLOSS[38]=['well','before-the-wall-even-his','prohibition-but-now','is-told','by-exception','who','to-hear-to-ascertain','is-capable']
QE[38]="Well, before the wall even his: prohibition but now is told by exception, who to hear to ascertain is capable."

ROWS[39]=[
 ("sa","dem","he"),
 ("evātra","dem + adv, fused","indeed-here"),
 ("niṣiddho","m.nom.sg (ni + sidh ppp)","is-forbidden"),
 ("no","particle","not"),
 ("kuḍyakīṭapatatriṇaḥ","m.nom.pl","walls-insects-birds"),
 ("tarhi","adv","then"),
 ("pāṣāṇatulyo@sau","m.nom.sg","stone-like-he"),
 ("vilīnendriyavṛttikaḥ","m.nom.sg","dissolved-sense-activity"),
]
GLOSS[39]=['he','indeed-here','is-forbidden','not','walls-insects-birds','then','stone-like-he','dissolved-sense-activity']
QE[39]="He indeed here is forbidden, not walls-insects-birds; then stone-like he, dissolved-sense-activity."

ROWS[40]=[
 ("tasyāgre","m.loc.sg","before-him"),
 ("paṭhatastasya","m.gen.sg pres.part (paṭh)","of-him-reading"),
 ("niṣedhollaṅghanā","f.nom.sg","prohibition-transgression"),
 ("katham","interrog","how"),
 ("sa","dem","he"),
 ("tu","particle","but"),
 ("vastusvabhāvena","n.inst.sg","by-thing-nature"),
 ("galitākṣo@pi","m.nom.sg + particle, fused","even-dissolved-eyed"),
 ("budhyate","3sg.pres.mid (budh)","awakens"),
]
GLOSS[40]=['before-him','of-him-reading','prohibition-transgression','how','he','but','by-thing-nature','even-dissolved-eyed','awakens']
QE[40]="Before him, of him reading, prohibition-transgression how? He but, by thing-nature, even dissolved-eyed awakens."

# ---- populate ----
import sys
sys.path.insert(0, 'tools')
from workcfg import source_spans
spans = source_spans('tantraloka-a19')
for v in list(ROWS.keys()):
    TOK[v] = list(spans[v])
    assert TOK[v] == list(spans[v]), 'TOK mismatch v%d'%v
    assert len(ROWS[v]) == len(spans[v]), 'ROW COUNT v%d: %d vs %d'%(v,len(ROWS[v]),len(spans[v]))
    assert len(GLOSS[v]) == len(spans[v]), 'GLOSS COUNT v%d'%(v,)
    assert v in QE
    CM[v] = [r for r in ROWS[v]]
    assert all(isinstance(r,(list,tuple)) and len(r)==3 for r in CM[v])
print('a19 part4 verified: %d verses, %d tokens'%(len(TOK), sum(len(v) for v in TOK.values())))
