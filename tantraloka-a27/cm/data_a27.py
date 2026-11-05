"""a27 data (liṅga-pūjā, 59u/461tok). Populates TOK/CM/GLOSS/QE."""
import sys; sys.path.insert(0,'tools')
from workcfg import source_spans
spans = source_spans('tantraloka-a27')
TOK = {}; CM = {}; GLOSS = {}; QE = {}
ROWS = {}

# v1
ROWS[1]=[("athocyate","indecl","now-told"),("liṅgapūjā","f.nom.sg","liṅga-worship"),("sūcitā","f.nom.sg (sūc ppp)","hinted"),("mālinīmate","n.loc.sg","in-Mālinī-doctrine")]
GLOSS[1]=['now-told','liṅga-worship','hinted','in-Mālinī-doctrine']
QE[1]="Now the liṅga-worship hinted in the Mālinī doctrine is told."

# v2
ROWS[2]=[
 ("eteṣāmūrdhvaśāstroktamantrāṇāṃ","m.gen.pl","of-their-higher-śāstra-told-mantras"),
 ("na","particle","not"),
 ("pratiṣṭhitam","n.nom.sg (prati + sthā ppp)","is-installed"),
 ("bahiṣkuryāttato","opt + adv, fused","should-put-outside—then"),
 ("hyete","dem","these"),
 ("rahasyatvena","n.inst.sg","by-secrecy"),
 ("siddhidāḥ","m.nom.pl (√dā + ṇin)","givers-of-siddhi"),
]
GLOSS[2]=['of-their-higher-śāstra-told-mantras','not','is-installed','should-put-outside—then','these','by-secrecy','givers-of-siddhi']
QE[2]="Of their higher-śāstra-told mantras: not installed; should put outside, then: these, by secrecy, are givers of siddhi."

# v3
ROWS[3]=[
 ("svavīryānandamāhātmyapraveśavaśaśālinīm","f.acc.sg, giant compound","possessing-the-entry-into-the-greatness-of-own-vigor-bliss"),
 ("ye","rel","who"),
 ("siddhiṃ","f.acc.sg","siddhi"),
 ("dadate","3pl.pres (dā)","give"),
 ("teṣāṃ","gen.pl","of-them"),
 ("bāhyatvaṃ","n.nom.sg","externality"),
 ("rūpavicyutiḥ","f.nom.sg","form-loss"),
]
GLOSS[3]=['possessing-the-entry-into-the-greatness-of-own-vigor-bliss','who','siddhi','give','of-them','externality','form-loss']
QE[3]="Possessing the entry into the greatness of own vigor-bliss: who give siddhi — of them, externality is form-loss."

# v4
ROWS[4]=[
 ("kiṃca","particle","and-what"),
 ("coktaṃ","n.nom.sg ppp (vac)","was-said"),
 ("samāveśapūrṇo","m.nom.sg","full-of-samāveśa"),
 ("bhoktrātmakaḥ","m.nom.sg","enjoyer-natured"),
 ("śivaḥ","m.nom.sg","Śiva"),
 ("bhogalāmpaṭyabhāgbhogavicchede","m.loc.sg, giant compound","in-interruption-of-enjoyment-lust-enjoyment"),
 ("nigrahātmakaḥ","m.nom.sg","of-nature-of-restraint"),
]
GLOSS[4]=['and-what','was-said','full-of-samāveśa','enjoyer-natured','Śiva','in-interruption-of-enjoyment-lust-enjoyment','of-nature-of-restraint']
QE[4]="And what was said: Samāveśa-full, enjoyer-natured Śiva; in interruption of enjoyment-lust-enjoyment, of nature of restraint."

# v5
ROWS[5]=[
 ("śāntatvanyakkriyodbhūtajighatsāvṛṃhitaṃ","n.acc.sg, giant compound","produced-from-peace-surpassing-rite-hunger-increased"),
 ("vapuḥ","n.acc.sg","body"),
 ("svayaṃ","indecl","itself"),
 ("pratiṣṭhitaṃ","n.acc.sg (prati + sthā ppp)","installed"),
 ("yena","rel inst","by-which"),
 ("so@syābhoge","m.nom.sg + m.loc.sg, fused","he-in-enjoyment"),
 ("vinaśyati","3sg.pres (vi + naś)","perishes"),
]
GLOSS[5]=['produced-from-peace-surpassing-rite-hunger-increased','body','itself','installed','by-which','he-in-enjoyment','perishes']
QE[5]="Produced from peace-surpassing-rite-hunger-increased body, itself installed, by which he in enjoyment perishes."

# v6
ROWS[6]=[
 ("uktaṃ","n.nom.sg (vac ppp)","was-said"),
 ("jñānottarāyāṃ","f.loc.sg","in-Jñānottara"),
 ("ca","particle","and"),
 ("tadetatparameśinā","dem + m.inst.sg, fused","that-this-by-Supreme-Lord"),
 ("śivo","m.nom.sg","Śiva"),
 ("yāgapriyo","m.nom.sg","sacrifice-loving"),
 ("yasmādviśeṣānmātṛmadhyagaḥ","abl + adj, fused","from-which-especially-in-mothers-midst"),
]
GLOSS[6]=['was-said','in-Jñānottara','and','that-this-by-Supreme-Lord','Śiva','sacrifice-loving','from-which-especially-in-mothers-midst']
QE[6]="Was said in Jñānottara, and that this by Supreme Lord: Śiva sacrifice-loving, from which especially in mothers' midst."

# v7
ROWS[7]=[
 ("tasmādrahasyaśāstreṣu","m.loc.pl","therefore-in-secret-śāstras"),
 ("ye","rel","which"),
 ("mantrāstānbudho","m.acc.pl + m.nom.sg, fused","mantras-these-the-wise"),
 ("bahiḥ","adv","outside"),
 ("na","particle","not"),
 ("pratiṣṭhāpayejjātu","opt caus (prati + sthā) + particle, fused","should-install-ever"),
 ("viśeṣādvyaktarūpiṇaḥ","m.acc.pl","especially-manifest-formed"),
]
GLOSS[7]=['therefore-in-secret-śāstras','which','mantras-these-the-wise','outside','not','should-install-ever','especially-manifest-formed']
QE[7]="Therefore in secret śāstras: which mantras — these the wise — outside not should install ever, especially manifest-formed."

# v8
ROWS[8]=[
 ("ata","adv","hence"),
 ("eva","particle","indeed"),
 ("mṛtasyārthe","m.loc.sg","for-the-dead's-sake"),
 ("pratiṣṭhānyatra","f.nom.sg + adv, fused","installation-elsewhere"),
 ("yoditā","f.nom.sg (yuj? yuj ppp?)","was-enjoined"),
 ("sātra","dem + adv, fused","that-here"),
 ("śāstreṣu","n.loc.pl","in-śāstras"),
 ("no","particle","not"),
 ("kāryā","f.nom.sg (kṛ gerundive)","to-be-done"),
 ("kāryā","f.nom.sg (kṛ gerundive)","to-be-done"),
 ("sādhāraṇī","f.nom.sg","common"),
 ("punaḥ","adv","again"),
]
GLOSS[8]=['hence','indeed','for-the-deads-sake','installation-elsewhere','was-enjoined','that-here','in-śāstras','not','to-be-done','to-be-done','common','again']
QE[8]="Hence indeed for the dead's sake installation elsewhere was enjoined; that here in śāstras not to be done, to be done common again."

# v9
ROWS[9]=[
 ("ā","prep","up-to"),
 ("tanmayatvasaṃsiddherā","f.abl.sg","from-tanmayatva-accomplishment"),
 ("cābhīṣṭaphalodayāt","abl","from-desired-fruit-arising"),
 ("putrakaḥ","m.nom.sg","putraka"),
 ("sādhako","m.nom.sg","sādhaka"),
 ("vyaktamavyaktaṃ","n.acc.sg","manifest-unmanifest"),
 ("vā","particle","or"),
 ("samāśrayet","opt (sam + ā + śri)","should-resort-to"),
]
GLOSS[9]=['up-to','from-tanmayatva-accomplishment','from-desired-fruit-arising','putraka','sādhaka','manifest-unmanifest','or','should-resort-to']
QE[9]="Up to tanmayatva-accomplishment, from desired-fruit-arising: putraka, sādhaka, manifest-unmanifest, or should resort to."

# v10
ROWS[10]=[
 ("putrakairgururabhyarthyaḥ","m.nom.sg","by-putrakas-guru-is-to-be-requested"),
 ("sādhakastu","m.nom.sg + particle, fused","sādhaka-but"),
 ("svayaṃ","indecl","himself"),
 ("vidan","m.nom.sg pres.part (vid)","knowing"),
 ("yadi","particle","if"),
 ("tatsthāpayenno","opt caus + particle, fused","he-should-install-not"),
 ("cettenāpyarthyo","opt + particle + m.nom.sg, fused","if-then-also-to-be-requested"),
 ("gururbhavet","m.nom.sg (bhū) opt, fused","guru-should-become"),
]
GLOSS[10]=['by-putrakas-guru-is-to-be-requested','sādhaka-but','himself','knowing','if','he-should-install-not','if-then-also-to-be-requested','guru-should-become']
QE[10]="By putrakas guru is to be requested; sādhaka but himself knowing: if he should install not, if then also to be requested, guru should become."

# ---- populate ----
import sys
sys.path.insert(0, 'tools')
from workcfg import source_spans
spans = source_spans('tantraloka-a27')
for v in list(ROWS.keys()):
    TOK[v] = list(spans[v])
    assert TOK[v] == list(spans[v]), 'TOK mismatch v%d'%v
    assert len(ROWS[v]) == len(spans[v]), 'ROW COUNT v%d: %d vs %d'%(v,len(ROWS[v]),len(spans[v]))
    assert len(GLOSS[v]) == len(spans[v]), 'GLOSS COUNT v%d'%(v,)
    assert v in QE
    CM[v] = [r for r in ROWS[v]]
    assert all(isinstance(r,(list,tuple)) and len(r)==3 for r in CM[v])
print('a27 part1 verified: %d verses, %d tokens'%(len(TOK), sum(len(v) for v in TOK.values())))
