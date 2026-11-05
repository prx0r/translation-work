"""a27 v21-30 data."""
import sys; sys.path.insert(0,'tools')
from workcfg import source_spans
spans = source_spans('tantraloka-a27')
TOK = {}; CM = {}; GLOSS = {}; QE = {}
ROWS = {}

ROWS[21]=[
 ("paṅkticakrakaśūlābjavidhinā","m.inst.sg","by-row-chakra-triśūla-lotus-rite"),
 ("tūramāśrayet","opt (ā + śri)","should-resort-to-tūra"),
 ("tallakṣaṇaṃ","n.acc.sg","its-mark"),
 ("bruve","1sg.pres (brū)","I-speak"),
 ("śrīmatpicuśāstre","n.loc.sg","in-venerable-Picu-śāstra"),
 ("nirūpitam","n.nom.sg (nir + rūp ppp)","was-set-forth"),
]
GLOSS[21]=['by-row-chakra-triśūla-lotus-rite','should-resort-to-tūra','its-mark','I-speak','in-venerable-Picu-śāstra','was-set-forth']
QE[21]="By row-chakra-triśūla-lotus-rite should resort to tūra; its mark I speak, in venerable Picu-śāstra was set forth."

ROWS[22]=[
 ("tūre","m.loc.sg","in-tūra"),
 ("yogaḥ","m.nom.sg","yoga"),
 ("sadā","adv","always"),
 ("śastaḥ","m.nom.sg (√śaṃs ppp)","is-praised"),
 ("siddhido","m.nom.sg","giver-of-siddhi"),
 ("doṣavarjite","m.loc.sg","in-faultless"),
 ("jālakairjarjarai","m.inst.pl","by-nets-torn"),
 ("randhrairdantairūnādhikai","m.inst.pl","by-holes-teeth-deficient-excess"),
 ("rujā","f.nom.sg","disease"),
]
GLOSS[22]=['in-tūra','yoga','always','is-praised','giver-of-siddhi','in-faultless','by-nets-torn','by-holes-teeth-deficient-excess','disease']
QE[22]="In tūra yoga always is praised, giver of siddhi in faultless; by nets-torn, by holes-teeth-deficient-excess disease."

ROWS[23]=[
 ("yukte","m.loc.sg","in-suitable"),
 ("ca","particle","and"),
 ("tūre","m.loc.sg","in-tūra"),
 ("hāniḥ","f.nom.sg","loss"),
 ("syāt","opt (bhū)","would-be"),
 ("taddhīne","m.loc.sg","in-its-deficient"),
 ("yāga","m.nom.sg","sacrifice"),
 ("uttamaḥ","m.nom.sg","supreme"),
 ("kāmya","m.nom.sg","desired"),
 ("eva","particle","indeed"),
 ("bhavettūramiti","opt + n.nom.sg + iti, fused","would-be-tūra—thus"),
 ("kecitprapedire","3pl.perf (pra + pad)","some-adopted"),
]
GLOSS[23]=['in-suitable','and','in-tūra','loss','would-be','in-its-deficient','sacrifice','supreme','desired','indeed','would-be-tūra—thus','some-adopted']
QE[23]="In suitable and in tūra loss would be, in its deficient sacrifice supreme; desired indeed would-be-tūra — thus some adopted."

ROWS[24]=[
 ("guravastu","m.nom.pl + particle, fused","gurus-but"),
 ("vidhau","m.loc.sg","in-rite"),
 ("kāmye","m.loc.sg","in-desired"),
 ("yatnāddoṣāṃstyajediti","abl + m.acc.pl + opt + iti, fused","from-effort-reject-faults—thus"),
 ("vyācakṣate","3pl.pres (vy + ā + cakṣ)","they-explain"),
 ("picuproktaṃ","n.acc.sg (vac ppp)","Picu-spoken"),
 ("na","particle","not"),
 ("nitye","m.loc.sg","in-obligatory"),
 ("karmaṇītyadaḥ","n.loc.sg + iti + dem, fused","in-rite—thus—this"),
]
GLOSS[24]=['gurus-but','in-rite','in-desired','from-effort-reject-faults—thus','they-explain','Picu-spoken','not','in-obligatory','in-rite—thus—this']
QE[24]="Gurus but in rite, in desired, from effort reject faults — thus they explain Picu-spoken; not in obligatory rite — thus this."

ROWS[25]=[
 ("śrīsiddhātantra","n.loc.sg","in-venerable-Siddhātantra"),
 ("uktaṃ","n.nom.sg (vac ppp)","was-said"),
 ("ca","particle","and"),
 ("tūralakṣaṇamuttamam","n.nom.sg","tūra-mark-supreme"),
 ("ekādikacatuṣkhaṇḍe","m.loc.sg","in-one-to-four-fragment"),
 ("gomukhe","m.loc.sg","in-cow-mouth"),
 ("pūrṇacandrake","m.loc.sg","in-full-moon"),
]
GLOSS[25]=['in-venerable-Siddhātantra','was-said','and','tūra-mark-supreme','in-one-to-four-fragment','in-cow-mouth','in-full-moon']
QE[25]="In venerable Siddhātantra was said and tūra-mark-supreme: in one-to-four-fragment, in cow-mouth, in full-moon."

ROWS[26]=[
 ("padmagorocanāmuktānīrasphaṭikasaṃnibhe","m.loc.sg, giant compound","in-lotus-go-rocanā-pearl-salt-crystal-like"),
 ("ekādipañcasadrandhravidyārekhānvite","m.loc.sg, giant compound","in-one-to-five-hundred-holes-vidyā-line-possessing"),
 ("śubhe","m.loc.sg","in-auspicious"),
]
GLOSS[26]=['in-lotus-go-rocanā-pearl-salt-crystal-like','in-one-to-five-hundred-holes-vidyā-line-possessing','in-auspicious']
QE[26]="In lotus-go-rocanā-pearl-salt-crystal-like, in one-to-five-hundred-holes-vidyā-line-possessing, in auspicious."

ROWS[27]=[
 ("na","particle","not"),
 ("rūkṣavakraśakaladīrghanimnasabinduke","m.loc.sg, giant compound","in-rough-crooked-fragment-long-depressed-with-bindu"),
 ("ślakṣṇayā","f.inst.sg","by-smooth"),
 ("vajrasūcyātra","f.inst.sg + adv, fused","by-diamond-needle-here"),
 ("sphuṭaṃ","adv","clearly"),
 ("devīgaṇānvitam","n.acc.sg","goddess-group-possessing"),
]
GLOSS[27]=['not','in-rough-crooked-fragment-long-depressed-with-bindu','by-smooth','by-diamond-needle-here','clearly','goddess-group-possessing']
QE[27]="Not in rough-crooked-fragment-long-depressed-with-bindu: by smooth, by diamond-needle here, clearly, goddess-group-possessing."

ROWS[28]=[
 ("sarvaṃ","n.acc.sg","all"),
 ("samālikhetpūjyaṃ","opt + n.acc.sg, fused","should-draw-worshipful"),
 ("sarvāvayavasundaram","n.acc.sg","all-limbs-beautiful"),
 ("etadevānusartavyamarghapātre@pi","n.acc.sg + particle, fused","this-very-should-follow-in-argha-vessel-also"),
 ("lakṣaṇam","n.nom.sg","mark"),
]
GLOSS[28]=['all','should-draw-worshipful','all-limbs-beautiful','this-very-should-follow-in-argha-vessel-also','mark']
QE[28]="All should draw worshipful, all-limbs-beautiful; this very should follow in argha-vessel also, mark."

ROWS[29]=[
 ("śrībrahmayāmale@pyuktaṃ","n.loc.sg + ppp, fused","in-venerable-Brahmayāmala-was-said"),
 ("pātraṃ","n.nom.sg","vessel"),
 ("gomukhamuttamam","n.nom.sg","cow-mouth-supreme"),
 ("gajakūrmatalaṃ","n.nom.sg","elephant-tortoise-base"),
 ("kumbhavṛttaśaktikajākṛti","n.nom.sg","pot-round-śakti-born-form"),
]
GLOSS[29]=['in-venerable-Brahmayāmala-was-said','vessel','cow-mouth-supreme','elephant-tortoise-base','pot-round-śakti-born-form']
QE[29]="In venerable Brahmayāmala was said: vessel, cow-mouth-supreme, elephant-tortoise-base, pot-round-śakti-born-form."

ROWS[30]=[
 ("akṣasūtramatho","n.acc.sg + adv, fused","bead-thread-and"),
 ("kuryāttatraivābhyarcayetkramam","opt + adv + opt + m.acc.sg, fused","should-make-there-indeed-worship-sequence"),
 ("vīradhātujalodbhūtamuktāratnasuvarṇajam","n.acc.sg","hero-substance-water-born-pearl-gem-gold-born"),
]
GLOSS[30]=['bead-thread-and','should-make-there-indeed-worship-sequence','hero-substance-water-born-pearl-gem-gold-born']
QE[30]="Bead-thread and should make there indeed worship sequence, hero-substance-water-born-pearl-gem-gold-born."

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
print('a27 part3 verified: %d verses, %d tokens'%(len(TOK), sum(len(v) for v in TOK.values())))
