"""a19 v11-20 data (sadyo-utkranti)."""
import sys; sys.path.insert(0,'tools')
from workcfg import source_spans
spans = source_spans('tantraloka-a19')
TOK = {}; CM = {}; GLOSS = {}; QE = {}
ROWS = {}

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

# ---- populate ----
import sys
sys.path.insert(0, 'tools')
from workcfg import source_spans
spans = source_spans('tantraloka-a19')
for v in ROWS:
    TOK[v] = list(spans[v])
    assert TOK[v] == list(spans[v]), 'TOK mismatch v%d'%v
    assert len(ROWS[v]) == len(spans[v]), 'ROW COUNT v%d: %d vs %d'%(v,len(ROWS[v]),len(spans[v]))
    assert len(GLOSS[v]) == len(spans[v]), 'GLOSS COUNT v%d'%(v,)
    assert v in QE
    CM[v] = [r for r in ROWS[v]]
    assert all(isinstance(r,(list,tuple)) and len(r)==3 for r in CM[v])
print('a19 part2 verified: %d verses, %d tokens'%(len(TOK), sum(len(v) for v in TOK.values())))
