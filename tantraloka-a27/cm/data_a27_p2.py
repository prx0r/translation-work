"""a27 v11-20 data."""
import sys; sys.path.insert(0,'tools')
from workcfg import source_spans
spans = source_spans('tantraloka-a27')
TOK = {}; CM = {}; GLOSS = {}; QE = {}
ROWS = {}

ROWS[11]=[
 ("guruścātra","m.nom.sg","guru-and-here"),
 ("nirodhākhye","m.loc.sg","in-so-called-nirodha"),
 ("kāla","m.nom.sg","time"),
 ("itthaṃ","adv","thus"),
 ("vibhau","m.loc.sg","in-the-Lord"),
 ("vadet","opt (vac)","he-should-say"),
 ("jīvatyasminphalāntaṃ","m.acc.sg","living-in-this-until-fruit-end"),
 ("tvaṃ","pron","you"),
 ("tiṣṭherjīvāvadhīti","opt + m.acc.sg, fused","should-stand-until-life-end—thus"),
 ("vā","particle","or"),
]
GLOSS[11]=['guru-and-here','in-so-called-nirodha','time','thus','in-the-Lord','he-should-say','living-in-this-until-fruit-end','you','should-stand-until-life-end—thus','or']
QE[11]="Guru and here in so-called nirodha: time thus in the Lord he should say; living in this until fruit-end, you should stand until life-end — or."

ROWS[12]=[
 ("liṅgaṃ","n.nom.sg","liṅga"),
 ("ca","particle","and"),
 ("bāṇaliṅgaṃ","n.nom.sg","Bāṇa-liṅga"),
 ("vā","particle","or"),
 ("ratnajaṃ","n.nom.sg","gem-born"),
 ("vātha","particle","or-then"),
 ("mauktikam","n.nom.sg","pearl"),
 ("pauṣpamānnamatho","n.nom.sg","flower-food-and"),
 ("vāstraṃ","n.nom.sg","cloth"),
 ("gandhadravyakṛtaṃ","n.nom.sg","scent-substance-made"),
 ("ca","particle","and"),
 ("vā","particle","or"),
]
GLOSS[12]=['liṅga','and','Bāṇa-liṅga','or','gem-born','or-then','pearl','flower-food-and','cloth','scent-substance-made','and','or']
QE[12]="Liṅga, and Bāṇa-liṅga, or gem-born, or-then pearl, flower-food-and, cloth, scent-substance-made, and or."

ROWS[13]=[
 ("natu","particle","but-not"),
 ("pāṣāṇajaṃ","n.nom.sg","stone-born"),
 ("liṅgaṃ","n.nom.sg","liṅga"),
 ("śilpyutthaṃ","n.nom.sg","sculptor-risen"),
 ("parikalpayet","opt (pari + kḷp)","should-consider"),
 ("dhātūtthaṃ","n.nom.sg","metal-risen"),
 ("ca","particle","and"),
 ("suvarṇotthavarjamanyadvivarjayet","m.acc.sg","gold-risen-except-other-reject"),
]
GLOSS[13]=['but-not','stone-born','liṅga','sculptor-risen','should-consider','metal-risen','and','gold-risen-except-other-reject']
QE[13]="But not stone-born liṅga, sculptor-risen should consider; metal-risen and gold-risen-except other reject."

ROWS[14]=[
 ("na","particle","not"),
 ("cātra","adv","and-here"),
 ("liṅgamānādi","n.nom.sg","liṅga-measure-and-the-rest"),
 ("kvacidapyupayujyate","pass + particle, fused","anywhere-is-used"),
 ("udāravīryairmantrairyadbhāsitaṃ","m.nom.sg","by-noble-vigor-mantras-what-is-shone"),
 ("phaladaṃ","m.nom.sg","fruit-giving"),
 ("hi","particle","for"),
 ("tat","dem","that"),
]
GLOSS[14]=['not','and-here','liṅga-measure-and-the-rest','anywhere-is-used','by-noble-vigor-mantras-what-is-shone','fruit-giving','for','that']
QE[14]="Not and here liṅga-measure-and-the-rest anywhere is used; by noble vigor-mantras what is shone, fruit-giving, for that."

ROWS[15]=[
 ("tasyāpi","gen.sg + particle, fused","of-it-also"),
 ("sthaṇḍilādyuktavidhinā","m.inst.sg","by-altar-and-the-rest-enjoined-rite"),
 ("śuddhimācaret","opt (śudh caus)","he-should-purify"),
 ("mantrārpaṇaṃ","n.nom.sg","mantra-offering"),
 ("tathaiva","adv","likewise"),
 ("syānnirodhastūktayuktitaḥ","opt + m.nom.sg, fused","should-be-nirodha-as-said-by-reason"),
]
GLOSS[15]=['of-it-also','by-altar-and-the-rest-enjoined-rite','he-should-purify','mantra-offering','likewise','should-be-nirodha-as-said-by-reason']
QE[15]="Of it also by altar-and-the-rest-enjoined-rite he should purify; mantra-offering likewise should be nirodha as said by reason."

ROWS[16]=[
 ("agnau","m.loc.sg","in-fire"),
 ("ca","particle","and"),
 ("tarpaṇaṃ","n.nom.sg","tarpaṇa"),
 ("bhūriviśeṣāddakṣiṇā","m.inst.sg","by-abundance-especially-dakṣiṇā"),
 ("guroḥ","m.gen.sg","of-guru"),
 ("dīnāditṛptirvibhavādyāga","m.nom.sg","poor-and-the-rest-satisfaction-abundance-sacrifice"),
 ("ityadhiko","n.nom.sg","thus-superior"),
 ("vidhiḥ","m.nom.sg","rite"),
]
GLOSS[16]=['in-fire','and','tarpaṇa','by-abundance-especially-dakṣiṇā','of-guru','poor-and-the-rest-satisfaction-abundance-sacrifice','thus-superior','rite']
QE[16]="In fire and tarpaṇa, by abundance especially dakṣiṇā of guru, poor-and-the-rest-satisfaction-abundance-sacrifice: thus superior rite."

ROWS[17]=[
 ("sarveṣvavyaktaliṅgeṣu","m.loc.pl","in-all-unmanifest-liṅgas"),
 ("pradhānaṃ","n.nom.sg","primary"),
 ("syādakalpitam","m.nom.sg","should-be-unconstructed"),
 ("tathā","adv","so"),
 ("ca","particle","and"),
 ("tatra","adv","there"),
 ("tatroktaṃ","n.nom.sg (vac ppp)","there-said"),
 ("lakṣaṇe","n.loc.sg","in-mark"),
 ("pārameśvare","n.loc.sg","in-Pārameśvara"),
]
GLOSS[17]=['in-all-unmanifest-liṅgas','primary','should-be-unconstructed','so','and','there','there-said','in-mark','in-Pārameśvara']
QE[17]="In all unmanifest liṅgas primary should be unconstructed; so and there there-said in mark in Pārameśvara."

ROWS[18]=[
 ("sūtre","n.loc.sg","in-thread"),
 ("pātre","n.loc.sg","in-vessel"),
 ("dhvaje","n.loc.sg","in-banner"),
 ("vastre","n.loc.sg","in-cloth"),
 ("svayambhūbāṇapūjite","m.loc.sg","in-svayambhū-Bāṇa-worshipped"),
 ("nadīprasravaṇotthe","m.loc.sg","in-river-spring-risen"),
 ("ca","particle","and"),
 ("nāhvānaṃ","n.nom.sg","no-calling"),
 ("nāpi","particle","nor-even"),
 ("kalpanā","f.nom.sg","construction"),
]
GLOSS[18]=['in-thread','in-vessel','in-banner','in-cloth','in-svayambhū-Bāṇa-worshipped','in-river-spring-risen','and','no-calling','nor-even','construction']
QE[18]="In thread, vessel, banner, cloth, svayambhū-Bāṇa-worshipped, river-spring-risen: and no calling, nor even construction."

ROWS[19]=[
 ("pīṭhaprasādamantrāṃśavelādiniyamo","m.nom.sg","seat-temple-mantra-portion-time-rule"),
 ("naca","particle","and-not"),
 ("vyaktaṃ","n.nom.sg","manifest"),
 ("vā","particle","or"),
 ("citrapustādau","m.loc.sg","in-painting-book-and-the-rest"),
 ("devadārusuvarṇajam","n.nom.sg","god-wood-gold-born"),
]
GLOSS[19]=['seat-temple-mantra-portion-time-rule','and-not','manifest','or','in-painting-book-and-the-rest','god-wood-gold-born']
QE[19]="Seat-temple-mantra-portion-time-rule, and not manifest or in painting-book-and-the-rest, god-wood-gold-born."

ROWS[20]=[
 ("atha","adv","now"),
 ("dīkṣitasacchilpikṛtaṃ","n.acc.sg","by-initiated-good-artisan-made"),
 ("sthāpayate","3sg.pres (sthā caus)","installs"),
 ("guruḥ","m.nom.sg","guru"),
 ("athavā","particle","or-else"),
 ("lakṣaṇopetamūrdhatatkarparāśritam","n.acc.sg","mark-endowed-head-shell-supported"),
]
GLOSS[20]=['now','by-initiated-good-artisan-made','installs','guru','or-else','mark-endowed-head-shell-supported']
QE[20]="Now by initiated good-artisan-made installs guru, or-else mark-endowed-head-shell-supported."

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
print('a27 part2 verified: %d verses, %d tokens'%(len(TOK), sum(len(v) for v in TOK.values())))
