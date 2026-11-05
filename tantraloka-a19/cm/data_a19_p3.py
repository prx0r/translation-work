"""a19 v21-30 data."""
import sys; sys.path.insert(0,'tools')
from workcfg import source_spans
spans = source_spans('tantraloka-a19')
TOK = {}; CM = {}; GLOSS = {}; QE = {}
ROWS = {}

ROWS[21]=[
 ("śrīmaddīkṣottare","n.loc.sg","in-the-venerable-Dīkṣottara"),
 ("tveṣa","dem","this"),
 ("vidhirvahnipuṭīkṛtaḥ","m.nom.sg","rite-fire-put-in"),
 ("haṃsaḥ","m.nom.sg","haṃsa"),
 ("pumānadhastasya","m.nom.sg","man-below-his"),
 ("rudrabindusamanvitaḥ","m.nom.sg","with-Rudra-bindu"),
]
GLOSS[21]=['in-the-venerable-Dīkṣottara','this','rite-fire-put-in','haṃsa','man-below-his','with-Rudra-bindu']
QE[21]="In the venerable Dīkṣottara this rite, fire-put-in: haṃsa, man below his, with Rudra-bindu."

ROWS[22]=[
 ("śiṣyadehe","n.loc.sg","in-the-disciples-body"),
 ("niyojyaitadanudvagnaḥ","m.nom.sg","joined-this-unagitated"),
 ("śataṃ","n.acc.sg","a-hundred"),
 ("japet","opt (jap)","should-mutter"),
 ("utkramyordhvanimeṣeṇa","gerund + m.inst.sg, fused","having-departed-by-upward-blink"),
 ("śiṣya","m.nom.sg","the-disciple"),
 ("itthaṃ","adv","thus"),
 ("paraṃ","m.acc.sg","supreme"),
 ("vrajet","opt (vraj)","may-go"),
]
GLOSS[22]=['in-the-disciples-body','joined-this-unagitated','a-hundred','should-mutter','having-departed-by-upward-blink','the-disciple','thus','supreme','may-go']
QE[22]="In the disciple's body joined, this unagitated: a hundred should he mutter; having departed by upward blink, the disciple thus may go supreme."

ROWS[23]=[
 ("eṣa","dem","this"),
 ("eva","particle","indeed"),
 ("vidhiḥ","m.nom.sg","rite"),
 ("śrīmatsiddhayogīśvarīmate","n.loc.sg","in-the-venerable-Siddhayogīśvarī-doctrine"),
 ("iyamutkrāmaṇī","f.nom.sg","this-departure"),
 ("dīkṣā","f.nom.sg","initiation"),
 ("kartavyā","f.nom.sg (kṛ gerundive)","to-be-performed"),
 ("yogino","m.gen.sg","of-the-yogin"),
 ("guroḥ","m.gen.sg","of-the-guru"),
]
GLOSS[23]=['this','indeed','rite','in-the-venerable-Siddhayogīśvarī-doctrine','this-departure','initiation','to-be-performed','of-the-yogin','of-the-guru']
QE[23]="This indeed is the rite in the venerable Siddhayogīśvarī doctrine: this departure-initiation to be performed by the yogin's guru."

ROWS[24]=[
 ("anabhyastaprāṇacāraḥ","m.nom.sg","unpracticed-in-prāṇa-conduct"),
 ("kathamenāṃ","interrog + f.acc.sg, fused","how-this"),
 ("kariṣyati","3sg.fut (kṛ)","will-he-perform"),
 ("vakṣyamāṇāṃ","f.acc.sg (vac gerundive)","to-be-spoken"),
 ("brahmavidyāṃ","f.acc.sg","Brahma-vidyā"),
 ("sakalāṃ","f.acc.sg","with-parts"),
 ("niṣkalombhitām","f.acc.sg","partless-included"),
]
GLOSS[24]=['unpracticed-in-prāṇa-conduct','how-this','will-he-perform','to-be-spoken','Brahma-vidyā','with-parts','partless-included']
QE[24]="Unpracticed in prāṇa-conduct, how will he perform this? The to-be-spoken Brahma-vidyā, with parts, partless-included."

ROWS[25]=[
 ("karṇe@sya","m.loc.sg","in-his-ear"),
 ("vā","particle","or"),
 ("paṭhedbhūyo","opt + adv, fused","should-read-again"),
 ("bhūyo","adv","again"),
 ("vāpyatha","particle + adv, fused","or-then"),
 ("pāṭhayet","opt caus (paṭh)","should-cause-to-read"),
 ("svayaṃ","indecl","himself"),
 ("ca","particle","and"),
 ("karma","n.acc.sg","rite"),
 ("kurvīta","opt (kṛ)","should-perform"),
 ("tattvaśuddhyādikaṃ","n.acc.sg","tattva-purity-and-the-rest"),
 ("guruḥ","m.nom.sg","the-guru"),
]
GLOSS[25]=['in-his-ear','or','should-read-again','again','or-then','should-cause-to-read','himself','and','rite','should-perform','tattva-purity-and-the-rest','the-guru']
QE[25]="In his ear, or should read again, again, or then should cause to read; himself and rite should perform, tattva-purity-and-the-rest, the guru."

ROWS[26]=[
 ("mantrakriyābalātpūrṇāhutyetthaṃ","m.inst.sg","by-mantra-rite-force-full-oblation-thus"),
 ("yojayetpare","opt caus + m.loc.sg, fused","he-should-join-to-supreme"),
 ("yogābhyāsamakṛtvāpi","gerund + particle, fused","without-yoga-practice-even"),
 ("sadya+utkrāntidāṃ","f.acc.sg","immediate-departure-giving"),
 ("guruḥ","m.nom.sg","the-guru"),
]
GLOSS[26]=['by-mantra-rite-force-full-oblation-thus','he-should-join-to-supreme','without-yoga-practice-even','immediate-departure-giving','the-guru']
QE[26]="By mantra-rite-force, full-oblation-thus, he should join to the supreme; without yoga-practice even, immediate-departure-giving, the guru."

ROWS[27]=[
 ("jñānamantrakriyādhyānabalātkartuṃ","m.inst.sg","by-knowledge-mantra-rite-meditation-force-to-perform"),
 ("bhavetprabhuḥ","opt + m.nom.sg, fused","should-be-able"),
 ("anayotkramyate","3sg.pres.pass (anu + ut + kram)","by-this-is-departed"),
 ("śiṣyo","m.nom.sg","the-disciple"),
 ("balādevaikakaṃ","adv","by-force-alone-one"),
 ("kṣaṇam","n.acc.sg","moment"),
]
GLOSS[27]=['by-knowledge-mantra-rite-meditation-force-to-perform','should-be-able','by-this-is-departed','the-disciple','by-force-alone-one','moment']
QE[27]="By knowledge-mantra-rite-meditation-force to perform: should be able; by this is departed the disciple, by force alone, one moment."

ROWS[28]=[
 ("kālasyollaṅghya","gerund (ullaṅgh)","having-transgressed-time"),
 ("bhogo","m.nom.sg","enjoyment"),
 ("hi","particle","for"),
 ("kṣaṇiko@syāstu","m.nom.sg + particle, fused","is-momentary"),
 ("kiṃ","interrog","what"),
 ("tataḥ","adv","then"),
 ("sadya+utkrāntidā","f.nom.sg","immediate-departure-giving"),
 ("cānyā","f.nom.sg","and-another"),
 ("yasyāṃ","f.loc.sg","in-which"),
 ("pūrṇāhutiṃ","f.acc.sg","full-oblation"),
 ("tadā","adv","then"),
]
GLOSS[28]=['having-transgressed-time','enjoyment','for','is-momentary','what','then','immediate-departure-giving','and-another','in-which','full-oblation','then']
QE[28]="Having transgressed time, enjoyment is momentary; what then? Immediate-departure-giving and another, in which full-oblation then."

ROWS[29]=[
 ("dadyādyadāsya","opt + rel + gen.sg, fused","should-give-when-his"),
 ("prāṇāḥ","m.nom.pl","life-breaths"),
 ("syurdhruvaṃ","opt + adv, fused","would-be-certainly"),
 ("niṣkramaṇecchavaḥ","m.nom.pl","desiring-to-depart"),
 ("vināpi","prep + particle, fused","even-without"),
 ("kriyayā","f.inst.sg","rite"),
 ("bhāvibrahmavidyābalādguruḥ","m.inst.sg","by-forthcoming-Brahma-vidyā-force-the-guru"),
]
GLOSS[29]=['should-give-when-his','life-breaths','would-be-certainly','desiring-to-depart','even-without','rite','by-forthcoming-Brahma-vidyā-force-the-guru']
QE[29]="Should give when his life-breaths would certainly be desiring to depart: even without rite, by forthcoming Brahma-vidyā force, the guru."

ROWS[30]=[
 ("karṇajāpaprayogeṇa","m.inst.sg","by-ear-muttering-use"),
 ("tattvakañcukajālataḥ","abl","from-tattva-armor-net"),
 ("niḥsārayanyathābhīṣṭe","gerund + adv, fused","liberating-as-desired"),
 ("sakale","m.loc.sg","in-with-parts"),
 ("niṣkale","m.loc.sg","in-partless"),
 ("dvaye","m.loc.sg","in-both"),
]
GLOSS[30]=['by-ear-muttering-use','from-tattva-armor-net','liberating-as-desired','in-with-parts','in-partless','in-both']
QE[30]="By ear-muttering use, from tattva-armor-net, liberating as desired: in with-parts, in partless, in both."

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
print('a19 part3 verified: %d verses, %d tokens'%(len(TOK), sum(len(v) for v in TOK.values())))
