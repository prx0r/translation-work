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


"""a19 v11-20 data (sadyo-utkranti)."""

ROWS[11] = [
 ("kṛtvā", "gerund (kṛ)", "having performed"),
 ("pūrvoditaṃ", "m.acc.sg ppp", "aforesaid"),
 ("nyāsaṃ", "m.acc.sg", "nyāsa (object)"),
 ("kālānalasamaprabham", "m.acc.sg", "equal-to-fire-of-time"),
 ("saṃhṛtikramataḥ", "abl", "by withdrawal-sequence"),
 ("sārdhaṃ", "adv", "together"),
 ("sṛkchindiyugalena", "m.inst.sg", "with the two scissors"),
 ("tu", "particle", "and"),
]
GLOSS[11] = ['having-performed','aforesaid','nyāsa','equal-to-fire-of-time','by-withdrawal-sequence','together','with-the-two-scissors','and']
QE[11] = "Having performed all the aforesaid nyāsa, equal-to-fire-of-time, by withdrawal-sequence together with the two scissors."

ROWS[12] = [
 ("āgneyīṃ", "f.acc.sg", "fire-natured"),
 ("dhāraṇāṃ", "f.acc.sg", "dhāraṇā (object)"),
 ("kṛtvā", "gerund (kṛ)", "having performed"),
 ("sarvamarmapratāpanīm", "f.acc.sg", "all-marma-scorching"),
 ("pūrayedvāyunā", "opt caus + m.inst.sg, fused", "he should fill with breath"),
 ("dehamaṅguṣṭhānmastakāntakam", "m.acc.sg", "body from thumb to head-end"),
]
GLOSS[12] = ['fire-natured','dhāraṇā','having-performed','all-marma-scorching','he-should-fill-with-breath','body-from-thumb-to-head-end']
QE[12] = "Having performed fire-natured dhāraṇā, all-marma-scorching: he should fill the body with breath from thumb to head-end."

ROWS[13] = [
 ("tamutkṛṣya", "gerund (ut + kṛṣ)", "having drawn up"),
 ("tato@ṅguṣṭhādūrdhvāntaṃ", "abl + n.acc.sg, fused", "from thumb to upper-end"),
 ("vakṣyamāṇayā", "f.inst.sg (vac gerundive)", "by the to-be-spoken"),
 ("kṛntenmarmāṇi", "opt (kṛt) + n.acc.pl, fused", "he should cut the marmas"),
 ("randhrāntāt", "abl", "from the hole-end"),
 ("kālarātryā", "f.inst.sg", "by Kālarātrī"),
 ("visarjayet", "opt caus (vi + sṛj)", "he should dismiss"),
]
GLOSS[13] = ['having-drawn-up','from-thumb-to-upper-end','by-the-to-be-spoken','he-should-cut-the-marmas','from-the-hole-end','by-Kālarātrī','he-should-dismiss']
QE[13] = "Having drawn up from thumb to upper-end, by the to-be-spoken he should cut the marmas from the hole-end, by Kālarātrī dismiss."

ROWS[14] = [
 ("anena", "m.inst.sg", "by this"),
 ("kramayogena", "m.inst.sg", "through sequential yoga"),
 ("yojito", "m.nom.sg (yuj ppp)", "yoked"),
 ("hutivarjitaḥ", "m.nom.sg", "libation-abandoned"),
 ("samayyapyeti", "3sg.pres (sam + i)", "even samayin goes"),
 ("tāṃ", "f.acc.sg", "that"),
 ("dīkṣāmiti", "f.acc.sg + iti, fused", "initiation — thus"),
 ("śrīmālinīmate", "n.loc.sg", "in the Mālinī doctrine"),
]
GLOSS[14] = ['by-this','through-sequential-yoga','yoked','libation-abandoned','even-samayin-goes','that','initiation—thus','in-the-Mālinī-doctrine']
QE[14] = "By this sequential yoga, yoked, libation-abandoned: even the samayin goes to that initiation — thus in the Mālinī doctrine."

ROWS[15] = [
 ("ṣoḍaśādhāraṣaṭcakralakṣyatrayakhapañcakāt", "m.abl.sg, giant compound", "from sixteen-supports-six-wheels-three-targets-five-ether"),
 ("kvacidanyataratrātha", "adv", "or somewhere else"),
 ("prāguktapaśukarmavat", "adv", "as before the beast-rite"),
]
GLOSS[15] = ['from-sixteen-supports-six-wheels-three-targets-five-ether','or-somewhere-else','as-before-the-beast-rite']
QE[15] = "From sixteen-supports-six-wheels-three-targets-five-ether, or somewhere else, as before the beast-rite."

ROWS[16] = [
 ("praviśya", "gerund (pra + viś)", "having entered"),
 ("mūlaṃ", "n.acc.sg", "the root (object)"),
 ("kandādeśchindannaikyavibhāvanāt", "m.abl.sg + gerund, fused", "from the kanda-region, cutting, from non-difference-discernment"),
 ("pūrṇāhutiprayogeṇa", "m.inst.sg", "by full-oblation use"),
 ("sveṣṭe", "m.loc.sg", "in own-desired"),
 ("dhāmni", "n.loc.sg", "abode"),
 ("niyojayet", "opt caus (ni + yuj)", "he should join"),
]
GLOSS[16] = ['having-entered','the-root','from-the-kanda-region-cutting-from-non-difference-discernment','by-full-oblation-use','in-own-desired','abode','he-should-join']
QE[16] = "Having entered the root from the kanda-region, cutting from non-difference-discernment, by full-oblation use he should join in his own-desired abode."

ROWS[17] = [
 ("jñānatriśūlaṃ", "n.acc.sg", "knowledge-trident (object)"),
 ("saṃdīptaṃ", "n.acc.sg (sam + dīp ppp)", "blazing"),
 ("dīptacakratrayojjvalam", "n.acc.sg", "radiant-three-wheels-blazing"),
 ("cintayitvāmunā", "gerund + m.inst.sg, fused", "having meditated by that"),
 ("tasya", "gen.sg", "his"),
 ("vedanaṃ", "n.acc.sg", "feeling"),
 ("bodhanaṃ", "n.acc.sg", "awakening"),
 ("bhramam", "n.acc.sg", "whirling"),
]
GLOSS[17] = ['knowledge-trident','blazing','radiant-three-wheels-blazing','having-meditated-by-that','his','feeling','awakening','whirling']
QE[17] = "Knowledge-trident, blazing, radiant-three-wheels-blazing: having meditated by that, his feeling, awakening, whirling."

ROWS[18] = [
 ("dīpanaṃ", "n.acc.sg", "inflaming"),
 ("tāḍanaṃ", "n.acc.sg", "striking"),
 ("todaṃ", "n.acc.sg", "pricking"),
 ("calanaṃ", "n.acc.sg", "moving"),
 ("ca", "particle", "and"),
 ("punaḥ", "adv", "again"),
 ("punaḥ", "adv", "and again"),
 ("kandādicakragaṃ", "n.acc.sg", "from-kanda-wheel-going"),
 ("kuryādviśeṣeṇa", "opt + adv, fused", "he should perform specially"),
 ("hṛdambuje", "n.loc.sg", "in the heart-lotus"),
]
GLOSS[18] = ['inflaming','striking','pricking','moving','and','again','and-again','from-kanda-wheel-going','he-should-perform-specially','in-the-heart-lotus']
QE[18] = "Inflaming, striking, pricking, moving, again and again from-kanda-wheel-going: he should perform specially in the heart-lotus."

ROWS[19] = [
 ("dvādaśānte", "m.loc.sg", "at the twelve-end"),
 ("tataḥ", "adv", "then"),
 ("kṛtvā", "gerund (kṛ)", "having performed"),
 ("binduyugmagate", "m.loc.sg", "in the bindu-pair"),
 ("kṣipet", "opt (kṣip)", "he should cast"),
 ("nirlakṣye", "m.loc.sg", "in the unmarked"),
 ("vā", "particle", "or"),
 ("pare", "m.loc.sg", "in the supreme"),
 ("dhāmni", "n.loc.sg", "abode"),
 ("saṃyuktaḥ", "m.nom.sg (sam + yuj ppp)", "joined"),
 ("parameśvaraḥ", "m.nom.sg", "the Supreme Lord"),
]
GLOSS[19] = ['at-the-twelve-end','then','having-performed','in-the-bindu-pair','he-should-cast','in-the-unmarked','or','in-the-supreme','abode','joined','the-Supreme-Lord']
QE[19] = "At the twelve-end, then, having performed, in the bindu-pair he should cast: in the unmarked or supreme abode, joined to the Supreme Lord."

ROWS[20] = [
 ("na", "particle", "not"),
 ("tasya", "gen.sg", "his"),
 ("kuryātsaṃskāraṃ", "opt + m.acc.sg, fused", "should he perform saṃskāra"),
 ("kaṃcidityāha", "m.acc.sg + 3sg.pres, fused", "any — thus says"),
 ("gahvare", "n.loc.sg", "in the Gahvara"),
 ("devaḥ", "m.nom.sg", "the god"),
 ("kimasya", "interrog + gen.sg, fused", "what of his"),
 ("pūrṇasya", "gen.sg (pṛ ppp)", "of the full one"),
 ("śrāddhādyairiti", "n.inst.pl + iti, fused", "by śrāddha-and-the-rest — thus"),
 ("bhāvitaḥ", "m.nom.sg (bhū caus ppp)", "considered"),
]
GLOSS[20] = ['not','his','should-he-perform-saṃskāra','any—thus-says','in-the-Gahvara','the-god','what-of-his','of-the-full-one','by-śrāddha-and-the-rest—thus','considered']
QE[20] = "Not should he perform any saṃskāra for him: thus says the god in the Gahvara — what of his full one, by śrāddha-and-the-rest considered?"


"""a19 v21-30 data."""

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


"""a19 v31-40 data."""

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


"""a19 v41-50 data."""

ROWS[41]=[
 ("akṣānapekṣayaivāntaścicchaktyā","n.inst.sg","by-sense-independence-inner-consciousness-power"),
 ("svaprakāśayā","f.inst.sg","by-self-luminous"),
 ("prāgdehaṃ","m.acc.sg","prior-body"),
 ("kila","particle","indeed"),
 ("tityakṣurnottaraṃ","m.nom.sg","desiring-to-abandon-not-supreme"),
 ("cādhitaṣṭhivān","m.nom.sg","and-established"),
]
GLOSS[41]=['by-sense-independence-inner-consciousness-power','by-self-luminous','prior-body','indeed','desiring-to-abandon-not-supreme','and-established']
QE[41]="By sense-independence inner consciousness-power, by self-luminous: prior body indeed desiring to abandon not supreme, and established."

ROWS[42]=[
 ("madhye","m.loc.sg","in-the-middle"),
 ("prabodhakabalāt","abl","from-awakening-force"),
 ("pratibudhyet","opt pass (budh)","would-awaken"),
 ("pudgalaḥ","m.nom.sg","the-person"),
 ("mantrāḥ","m.nom.pl","mantras"),
 ("śabdamayāḥ","m.nom.pl","sound-made"),
 ("śuddhavimarśātmatayā","f.inst.sg","by-pure-reflection-nature"),
 ("svayam","indecl","itself"),
]
GLOSS[42]=['in-the-middle','from-awakening-force','would-awaken','the-person','mantras','sound-made','by-pure-reflection-nature','itself']
QE[42]="In the middle, from awakening-force, would awaken the person: mantras, sound-made, by pure-reflection-nature itself."

ROWS[43]=[
 ("arthātmanā","m.inst.sg","by-meaning-self"),
 ("cāvabhāntastadarthapratibodhakāḥ","m.nom.pl","and-shining-that-meaning-awakening"),
 ("tenāsya","m.inst.sg + gen.sg, fused","by-that-his"),
 ("galitākṣasya","gen.sg","of-dissolved-eyed"),
 ("prabodho","m.nom.sg","awakening"),
 ("jāyate","3sg.pres.mid (jan)","arises"),
 ("svayam","indecl","itself"),
]
GLOSS[43]=['by-meaning-self','and-shining-that-meaning-awakening','by-that-his','of-dissolved-eyed','awakening','arises','itself']
QE[43]="By meaning-self, and shining that meaning-awakening: by that his, of dissolved-eyed, awakening arises itself."

ROWS[44]=[
 ("svacitsamānajātīyamantrāmarśanasaṃnidheḥ","m.abl.sg","from-self-consciousness-same-kind-mantra-reflection-proximity"),
 ("yathā","rel adv","as"),
 ("hyalpajavo","m.nom.sg","indeed-small-speed"),
 ("vāyuḥ","m.nom.sg","wind"),
 ("sajātīyavimiśritaḥ","m.nom.sg","same-kind-mixed"),
]
GLOSS[44]=['from-self-consciousness-same-kind-mantra-reflection-proximity','as','indeed-small-speed','wind','same-kind-mixed']
QE[44]="From self-consciousness-same-kind-mantra-reflection-proximity: as indeed-small-speed wind, same-kind-mixed."

ROWS[45]=[
 ("javī","m.nom.sg","speedy"),
 ("tathātmā","m.nom.sg","so-self"),
 ("saṃsuptāmarśo@pyevaṃ","m.nom.sg + particle, fused","sleeping-reflection-even-thus"),
 ("prabudhyate","3sg.pres.pass (pra + budh)","awakens"),
 ("prabuddhaḥ","m.nom.sg (pra + budh ppp)","awakened"),
 ("sa","dem","he"),
 ("ca","particle","and"),
 ("saṃjāto","m.nom.sg (sam + jan ppp)","born"),
 ("na","particle","not"),
 ("cādīkṣita","m.nom.sg","and-uninitiated"),
 ("ucyate","3sg.pres.pass (vac)","is-called"),
]
GLOSS[45]=['speedy','so-self','sleeping-reflection-even-thus','awakens','awakened','he','and','born','not','and-uninitiated','is-called']
QE[45]="Speedy, so-self: sleeping-reflection even thus awakens; awakened he and born, not and-uninitiated, is called."

ROWS[46]=[
 ("dīkṣā","f.nom.sg","initiation"),
 ("hi","particle","for"),
 ("nāma","n.nom.sg","name"),
 ("saṃskāro","m.nom.sg","saṃskāra"),
 ("na","particle","not"),
 ("tvanyatso@sti","dem + particle, fused","but-other-is"),
 ("cāsya","particle + gen.sg, fused","and-his"),
 ("hi","particle","for"),
 ("ata","adv","hence"),
 ("eva","particle","indeed"),
 ("nijaṃ","n.acc.sg","own"),
 ("śāstraṃ","n.acc.sg","scripture"),
 ("paṭhati","3sg.pres (paṭh)","reads"),
 ("kvāpi","adv","somewhere"),
 ("sāmaye","m.loc.sg","in-samaya"),
]
GLOSS[46]=['initiation','for','name','saṃskāra','not','but-other-is','and-his','for','hence','indeed','own','scripture','reads','somewhere','in-samaya']
QE[46]="Initiation, for, name, saṃskāra: not but-other-is, and-his, for, hence indeed, own scripture reads somewhere in samaya."

ROWS[47]=[
 ("tacchrutvā","gerund (śru)","having-heard-that"),
 ("ko@pi","interrog + particle, fused","someone"),
 ("dhanyaścenmucyate","opt + 3sg.pres.pass, fused","if-fortunate-is-liberated"),
 ("nāsya","particle + gen.sg, fused","not-his"),
 ("sā","f.nom.sg","that"),
 ("kṣatiḥ","f.nom.sg","loss"),
 ("śāstranindāṃ","f.acc.sg","scripture-censure"),
 ("maiṣa","prohib + dem, fused","let-not-this"),
 ("kārṣīddvayoḥ","opt (kṛ) + gen.du, fused","one-do—of-two"),
 ("pātityadāyinīm","f.acc.sg","fall-giving"),
]
GLOSS[47]=['having-heard-that','someone','if-fortunate-is-liberated','not-his','that','loss','scripture-censure','let-not-this','one-do—of-two','fall-giving']
QE[47]="Having heard that, someone if fortunate is liberated, not his that loss; scripture-censure let not this one do — of two fall-giving."

ROWS[48]=[
 ("ityevaṃparametannādīkṣitāgre","adv + m.loc.sg, fused","thus-supreme-this-not-uninitiated-before"),
 ("paṭhediti","opt + iti, fused","should-read—thus"),
 ("yathā","rel adv","as"),
 ("ca","particle","and"),
 ("samayī","m.nom.sg","samayin"),
 ("kāṣṭhe","n.loc.sg","in-wood"),
 ("loṣṭe","n.loc.sg","in-clod"),
 ("vā","particle","or"),
 ("mantrayojanām","f.acc.sg","mantra-joining"),
]
GLOSS[48]=['thus-supreme-this-not-uninitiated-before','should-read—thus','as','and','samayin','in-wood','in-clod','or','mantra-joining']
QE[48]="Thus supreme this, not uninitiated before, should read thus: as and samayin in wood, in clod, or mantra-joining."

ROWS[49]=[
 ("kurvaṃstasmiṃścalatyeti","pres.part + m.loc.sg + pres, fused","doing-in-that-flutters-thus"),
 ("na","particle","not"),
 ("lopaṃ","m.acc.sg","loss"),
 ("tadvadatra","adv + adv, fused","likewise-here"),
 ("hi","particle","for"),
 ("yato@sya","rel + gen.sg, fused","since-his"),
 ("pratyayaprāptiprepsoḥ","gen.sg","proof-arrival-desiring"),
 ("samayinastathā","m.gen.sg + adv, fused","of-samayin—thus"),
]
GLOSS[49]=['doing-in-that-flutters-thus','not','loss','likewise-here','for','since-his','proof-arrival-desiring','of-samayin—thus']
QE[49]="Doing in that flutters thus: not loss, likewise here, for since his proof-arrival-desiring, of samayin thus."

ROWS[50]=[
 ("pravṛttasya","gen.sg (pra + vṛt ppp)","of-one-engaged"),
 ("svabhāvena","n.inst.sg","by-nature"),
 ("tasminmukte","m.loc.sg (muc ppp)","in-that-released"),
 ("na","particle","not"),
 ("vai","particle","indeed"),
 ("kṣatiḥ","f.nom.sg","loss"),
 ("sādhakastu","m.nom.sg + particle, fused","but-the-sādhaka"),
 ("sadā","adv","always"),
 ("sādhye","m.loc.sg (sādh gerundive)","in-the-to-be-accomplished"),
 ("phale","n.loc.sg","fruit"),
 ("niyatiyantraṇāt","abl","from-rule-constraint"),
]
GLOSS[50]=['of-one-engaged','by-nature','in-that-released','not','indeed','loss','but-the-sādhaka','always','in-the-to-be-accomplished','fruit','from-rule-constraint']
QE[50]="Of one engaged, by nature, in that released: not indeed loss. But the sādhaka always in the to-be-accomplished fruit, from rule-constraint."

# v51-56
ROWS[51]=[
 ("makṣikāśrutamantro@pi","m.nom.sg","even-fly-heard-mantra"),
 ("prāyaścittaucitīṃ","f.acc.sg","expiation-fitness"),
 ("caret","opt (car)","should-perform"),
 ("itthaṃ","adv","thus"),
 ("sadyaḥsamutkrāntiryoktā","f.nom.sg","immediate-departure-is-spoken"),
 ("tāmājñayā","f.inst.sg","by-that-command"),
 ("guroḥ","m.gen.sg","of-the-guru"),
]
GLOSS[51]=['even-fly-heard-mantra','expiation-fitness','should-perform','thus','immediate-departure-is-spoken','by-that-command','of-the-guru']
QE[51]="Even fly-heard mantra: expiation-fitness should perform. Thus immediate-departure is spoken, by that command of the guru."

ROWS[52]=[
 ("samayyādirapi","m.nom.sg + particle, fused","samayin-and-the-rest-even"),
 ("proktakāle","m.loc.sg","at-the-spoken-time"),
 ("proktārthasiddhaye","f.dat.sg","for-the-spoken-meaning's-accomplishment"),
 ("svayaṃ","indecl","himself"),
 ("kuryātsamabhyastaprāṇacāragamāgamaḥ","opt + m.nom.sg, fused","should-perform-practiced-prāṇa-conduct-going-coming"),
]
GLOSS[52]=['samayin-and-the-rest-even','at-the-spoken-time','for-the-spoken-meanings-accomplishment','himself','should-perform-practiced-prāṇa-conduct-going-coming']
QE[52]="Samayin and the rest even, at the spoken time, for the spoken meaning's accomplishment: himself should perform practiced prāṇa-conduct going-coming."

ROWS[53]=[
 ("akṛtādhikṛtirvāpi","m.nom.sg","unmade-authorized-or-even"),
 ("guruḥ","m.nom.sg","the-guru"),
 ("samayaśuddhaye","f.dat.sg","for-samaya-purity"),
 ("adhastanapadāvastho","m.nom.sg","in-lower-state"),
 ("natu","particle","but-not"),
 ("jñāneddhacetanaḥ","m.nom.sg","knowledge-kindled-conscious"),
]
GLOSS[53]=['unmade-authorized-or-even','the-guru','for-samaya-purity','in-lower-state','but-not','knowledge-kindled-conscious']
QE[53]="Unmade-authorized or even the guru, for samaya-purity, in lower-state: but not knowledge-kindled-conscious."

ROWS[54]=[
 ("itīyaṃ","dem + f.nom.sg, fused","thus-this"),
 ("sadya+utkrāntiḥ","f.nom.sg","immediate-departure"),
 ("sūcitā","f.nom.sg (sūc ppp)","hinted"),
 ("mālinīmate","n.loc.sg","in-Mālinī-doctrine"),
 ("svayaṃ","indecl","himself"),
 ("vā","particle","or"),
 ("guruṇā","m.inst.sg","by-the-guru"),
 ("vātha","particle","or-then"),
 ("kāryatvena","n.inst.sg","as-to-be-performed"),
 ("maheśinā","m.inst.sg","by-the-Great-Lord"),
]
GLOSS[54]=['thus-this','immediate-departure','hinted','in-Mālinī-doctrine','himself','or','by-the-guru','or-then','as-to-be-performed','by-the-Great-Lord']
QE[54]="Thus this immediate-departure hinted in Mālinī-doctrine: himself or by the guru or then as to be performed by the Great Lord."

ROWS[55]=[
 ("sarvaṃ","n.acc.sg","all"),
 ("bhogaṃ","m.acc.sg","enjoyment"),
 ("virūpaṃ","m.acc.sg","ugly"),
 ("tu","particle","but"),
 ("matvā","gerund (man)","having-deemed"),
 ("dehaṃ","m.acc.sg","body"),
 ("tyajedyadi","opt + particle, fused","should-abandon-if"),
 ("tadā","adv","then"),
 ("tena","m.inst.sg","by-that"),
 ("krameṇāśu","adv","quickly-by-sequence"),
 ("yojitaḥ","m.nom.sg (yuj ppp)","joined"),
 ("samayī","m.nom.sg","samayin"),
 ("śivaḥ","m.nom.sg","Śiva"),
]
GLOSS[55]=['all','enjoyment','ugly','but','having-deemed','body','should-abandon-if','then','by-that','quickly-by-sequence','joined','samayin','Śiva']
QE[55]="All enjoyment ugly, but having deemed, body should abandon if: then by that, quickly by sequence, joined, samayin, Śiva."

ROWS[56]=[
 ("ukteyaṃ","dem + f.nom.sg, fused","spoken-this"),
 ("sadya+utkrāntiryā","f.nom.sg + rel, fused","immediate-departure-which"),
 ("gopyā","f.nom.sg (gup gerundive)","to-be-guarded"),
 ("prāṇavadbudhaiḥ","m.inst.pl","by-the-wise-like-life"),
]
GLOSS[56]=['spoken-this','immediate-departure-which','to-be-guarded','by-the-wise-like-life']
QE[56]="Spoken this immediate-departure, which to-be-guarded, by the wise like life."



# ---- populate TOK/CM/GLOSS/QE from ROWS (all verses) ----
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
print('a19 ALL verified: %d verses, %d tokens'%(len(TOK), sum(len(v) for v in TOK.values())))
