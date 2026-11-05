"""a27 v31-40 data."""
import sys; sys.path.insert(0,'tools')
from workcfg import source_spans
spans = source_spans('tantraloka-a27')
TOK = {}; CM = {}; GLOSS = {}; QE = {}
ROWS = {}

ROWS[31]=[
 ("akṣasūtraṃ","n.acc.sg","bead-thread"),
 ("kramotkṛṣṭaṃ","n.acc.sg","sequence-extracted"),
 ("raudrākṣaṃ","n.acc.sg","rudrākṣa"),
 ("vā","particle","or"),
 ("viśeṣataḥ","adv","especially"),
 ("śataṃ","n.acc.sg","hundred"),
 ("tithyuttaraṃ","n.acc.sg","tithi-superior"),
 ("yadvā","particle","or-even"),
 ("sāṣṭaṃ","n.acc.sg","with-eight"),
 ("yadvā","particle","or-even"),
 ("tadardhakam","n.acc.sg","its-half"),
]
GLOSS[31]=['bead-thread','sequence-extracted','rudrākṣa','or','especially','hundred','tithi-superior','or-even','with-eight','or-even','its-half']
QE[31]="Bead-thread, sequence-extracted, rudrākṣa, or especially hundred, tithi-superior, or-even with-eight, or-even its-half."

ROWS[32]=[
 ("tadardhaṃ","n.acc.sg","its-half"),
 ("vātha","particle","or-then"),
 ("pañcāśadyuktaṃ","n.acc.sg","fifty-joined"),
 ("tatparikalpayet","opt (pari + kḷp)","he-should-consider-that"),
 ("vaktrāṇi","n.acc.pl","mouths"),
 ("pañca","num","five"),
 ("citspandajñānecchākṛtisaṃgateḥ","m.abl.sg","from-consciousness-pulse-knowledge-will-action-union"),
]
GLOSS[32]=['its-half','or-then','fifty-joined','he-should-consider-that','mouths','five','from-consciousness-pulse-knowledge-will-action-union']
QE[32]="Its-half, or-then fifty-joined, he should consider that; mouths five, from consciousness-pulse-knowledge-will-action-union."

ROWS[33]=[
 ("pañcadhādyantagaṃ","n.acc.sg","fivefold-end-going"),
 ("caikyamityupāntyākṣago","n.acc.sg","unity-thus-penultimate-bead-going"),
 ("vidhiḥ","m.nom.sg","rite"),
 ("śaktitadvatprabhedena","m.inst.sg","by-śakti-and-its-division"),
 ("tatra","adv","there"),
 ("dvairūpyamucyate","3sg.pres.pass","two-form-is-said"),
]
GLOSS[33]=['fivefold-end-going','unity-thus-penultimate-bead-going','rite','by-śakti-and-its-division','there','two-form-is-said']
QE[33]="Fivefold-end-going, unity-thus-penultimate-bead-going, rite, by śakti-and-its-division: there two-form is said."

ROWS[34]=[
 ("tato","adv","then"),
 ("dviguṇamāne","m.loc.sg","in-double-measure"),
 ("tu","particle","but"),
 ("dvirūpaṃ","n.acc.sg","two-formed"),
 ("nyāsamācaret","opt (nyās)","he-should-perform-nyāsa"),
 ("tato@pi","adv","then-even"),
 ("dviguṇe","m.loc.sg","in-double"),
 ("sṛṣṭisaṃhṛtidvitayena","m.inst.sg","by-creation-dissolution-pair"),
 ("tam","m.acc.sg","him"),
]
GLOSS[34]=['then','in-double-measure','but','two-formed','he-should-perform-nyāsa','then-even','in-double','by-creation-dissolution-pair','him']
QE[34]="Then in double-measure but two-formed nyāsa he should perform; then even in double, by creation-dissolution-pair, him."

ROWS[35]=[
 ("mātṛkāṃ","f.acc.sg","Mātṛkā"),
 ("mālinīṃ","f.acc.sg","Mālinī"),
 ("vātha","particle","or-then"),
 ("nyasyetkhaśarasaṃmite","opt + m.loc.sg, fused","he-should-place-in-ether-sixteen-measured"),
 ("uttame","m.loc.sg","in-supreme"),
 ("tu","particle","but"),
 ("dvayīṃ","f.acc.sg","two"),
 ("nyasyennyasya","gerund + gerund, fused","having-placed-having-placed"),
 ("pūrvaṃ","adv","before"),
 ("pracoditān","m.acc.pl (pra + cod ppp)","impelled-ones"),
]
GLOSS[35]=['Mātṛkā','Mālinī','or-then','he-should-place-in-ether-sixteen-measured','in-supreme','but','two','having-placed-having-placed','before','impelled-ones']
QE[35]="Mātṛkā, Mālinī, or-then: he should place in ether-sixteen-measured; in supreme but two, having-placed-having-placed, before impelled-ones."

ROWS[36]=[
 ("dīkṣāyāṃ","f.loc.sg","in-initiation"),
 ("mukhyato","adv","primarily"),
 ("mantrāṃstānpañcadaśa","m.acc.pl","mantras-those-fifteen"),
 ("daiśikaḥ","m.nom.sg","the-daiśika"),
 ("yadi","particle","if"),
 ("vā","particle","or"),
 ("tattvabhuvanakalāmantrapadārṇajaiḥ","m.inst.pl","by-tattva-bhuvana-kalā-mantra-pada-phoneme"),
]
GLOSS[36]=['in-initiation','primarily','mantras-those-fifteen','the-daiśika','if','or','by-tattva-bhuvana-kalā-mantra-pada-phoneme']
QE[36]="In initiation primarily mantras those fifteen, the daiśika; if or by tattva-bhuvana-kalā-mantra-pada-phoneme."

ROWS[37]=[
 ("saṃkhyābhedaiḥ","m.inst.pl","by-number-differences"),
 ("kṛte","m.loc.sg (kṛ ppp)","in-made"),
 ("sūtre","n.loc.sg","in-thread"),
 ("taṃ","m.acc.sg","him"),
 ("taṃ","m.acc.sg","him"),
 ("nyāsaṃ","m.acc.sg","nyāsa"),
 ("guruścaret","opt (car)","guru-should-perform"),
 ("kṛtvākṣasūtraṃ","gerund + n.acc.sg, fused","having-made-bead-thread"),
 ("tasyāpi","gen.sg + particle, fused","of-it-also"),
 ("sarvaṃ","n.acc.sg","all"),
 ("sthaṇḍilavadbhavet","opt (bhū) + adv, fused","should-be-as-altar"),
]
GLOSS[37]=['by-number-differences','in-made','in-thread','him','him','nyāsa','guru-should-perform','having-made-bead-thread','of-it-also','all','should-be-as-altar']
QE[37]="By number-differences in made in thread: him him nyāsa guru should perform; having-made bead-thread, of it also all should be as altar."

ROWS[38]=[
 ("pūjitena","m.inst.sg","by-worshipped"),
 ("ca","particle","and"),
 ("tenaiva","m.inst.sg + particle, fused","by-that-very"),
 ("japaṃ","m.acc.sg","japa"),
 ("kuryādatandritaḥ","opt + adj, fused","should-perform-undistracted"),
 ("vidhiruktastvayaṃ","m.nom.sg + particle, fused","rite-said-this"),
 ("śrīmanmālinīvijayottare","n.loc.sg","in-venerable-Mālinīvijayottara"),
]
GLOSS[38]=['by-worshipped','and','by-that-very','japa','should-perform-undistracted','rite-said-this','in-venerable-Mālinīvijayottara']
QE[38]="By worshipped and by that very japa should perform undistracted: rite said this in venerable Mālinīvijayottara."

ROWS[39]=[
 ("cakravadbhramayannetadyadvakti","pres.part + dem + rel + pres, fused","wheel-like-whirling-this-what-he-says"),
 ("sa","dem","he"),
 ("japo","m.nom.sg","japa"),
 ("bhavet","opt (bhū)","would-be"),
 ("yadīkṣate","rel + pres (īkṣ)","if-he-sees"),
 ("juhotyetadbodhāgnau","opt (hu) + dem + n.loc.sg, fused","he-offers-this-in-awakening-fire"),
 ("saṃpraveśanāt","abl","from-entering"),
]
GLOSS[39]=['wheel-like-whirling-this-what-he-says','he','japa','would-be','if-he-sees','he-offers-this-in-awakening-fire','from-entering']
QE[39]="Wheel-like-whirling-this-what-he-says: he japa would be; if he sees, he offers this in awakening-fire, from entering."

ROWS[40]=[
 ("athavārghamahāpātraṃ","n.acc.sg","or-argha-great-vessel"),
 ("kuryāttaccottaraṃ","opt + n.acc.sg, fused","should-make-that-supreme"),
 ("param","adv","param"),
 ("nārikelamatho","n.acc.sg","coconut-and"),
 ("bailvaṃ","n.acc.sg","bilva"),
 ("sauvarṇaṃ","n.acc.sg","golden"),
 ("rājataṃ","n.acc.sg","silver"),
 ("ca","particle","and"),
 ("vā","particle","or"),
]
GLOSS[40]=['or-argha-great-vessel','should-make-that-supreme','param','coconut-and','bilva','golden','silver','and','or']
QE[40]="Or argha-great-vessel should make that supreme param; coconut-and, bilva, golden, silver, and or."

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
print('a27 part4 verified: %d verses, %d tokens'%(len(TOK), sum(len(v) for v in TOK.values())))
