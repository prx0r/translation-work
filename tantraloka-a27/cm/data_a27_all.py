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


"""a27 v11-20 data."""

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


"""a27 v21-30 data."""

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


"""a27 v31-40 data."""

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


"""a27 v41-59 data."""

ROWS[41]=[
 ("tasyāpyeṣa","gen.sg + dem, fused","of-it-also-this"),
 ("vidhiḥ","m.nom.sg","rite"),
 ("sarvaḥ","m.nom.sg","all"),
 ("pratiṣṭhādau","m.loc.sg","in-installation-beginning"),
 ("prakīrtitaḥ","m.nom.sg (pra + kīrt ppp)","was-declared"),
 ("tanniṣkamparasaiḥ","m.inst.pl","by-its-unshaking-fluids"),
 ("pūrṇaṃ","n.acc.sg","full"),
 ("kṛtvāsminpūjayetkramam","gerund + m.loc.sg + opt + m.acc.sg, fused","having-made-in-this-worship-sequence"),
]
GLOSS[41]=['of-it-also-this','rite','all','in-installation-beginning','was-declared','by-its-unshaking-fluids','full','having-made-in-this-worship-sequence']
QE[41]="Of it also this rite all in installation-beginning was declared; by its unshaking fluids full, having made in this worship sequence."

ROWS[42]=[
 ("adhomukhaṃ","n.acc.sg","downward-faced"),
 ("sadā","adv","always"),
 ("sthāpyaṃ","n.nom.sg (sthā gerundive)","to-be-placed"),
 ("pūjitaṃ","n.acc.sg (pūj ppp)","worshipped"),
 ("pūjane","m.loc.sg","in-worship"),
 ("punaḥ","adv","again"),
 ("tatpātramunmukhaṃ","n.acc.sg","that-vessel-upward-faced"),
 ("tacca","dem + particle, fused","and-that"),
 ("riktaṃ","n.acc.sg (ric ppp)","empty"),
 ("kuryānna","opt + particle, fused","should-make-not"),
 ("tādṛśam","dem","such"),
]
GLOSS[42]=['downward-faced','always','to-be-placed','worshipped','in-worship','again','that-vessel-upward-faced','and-that','empty','should-make-not','such']
QE[42]="Downward-faced always to be placed; worshipped in worship again, that vessel upward-faced; and that empty should make not, such."

ROWS[43]=[
 ("pūjānte","m.loc.sg","at-worship-end"),
 ("tadrasāpūrṇamātmānaṃ","m.acc.sg","that-fluid-full-self"),
 ("pravidhāya","gerund (pra + vi + dhā)","having-disposed"),
 ("tat","dem","that"),
 ("adhomukhaṃ","n.acc.sg","downward-faced"),
 ("ca","particle","and"),
 ("saṃpūjya","gerund (sam + pūj)","having-fully-worshipped"),
 ("sthāpayet","opt (sthā caus)","he-should-place"),
 ("vicakṣaṇaḥ","m.nom.sg","the-wise"),
]
GLOSS[43]=['at-worship-end','that-fluid-full-self','having-disposed','that','downward-faced','and','having-fully-worshipped','he-should-place','the-wise']
QE[43]="At worship-end, that-fluid-full-self having disposed, that downward-faced and having fully worshipped, he should place, the wise."

ROWS[44]=[
 ("khaṅgaṃ","n.acc.sg","sword"),
 ("kṛpāṇikāṃ","f.acc.sg","dagger"),
 ("yadvā","particle","or-even"),
 ("kartarīṃ","f.acc.sg","scissors"),
 ("makuraṃ","n.acc.sg","mirror"),
 ("ca","particle","and"),
 ("vā","particle","or"),
 ("vimalaṃ","n.acc.sg","pure"),
 ("tattathā","adv","so-thus"),
 ("kuryācchrīmatkālīmukhoditam","opt + n.acc.sg, fused","should-make-as-venerable-Kālī-mouth-spoken"),
]
GLOSS[44]=['sword','dagger','or-even','scissors','mirror','and','or','pure','so-thus','should-make-as-venerable-Kālī-mouth-spoken']
QE[44]="Sword, dagger, or-even scissors, mirror, and or, pure, so-thus should make as venerable Kālī-mouth spoken."

ROWS[45]=[
 ("śrībhairavakule@pyuktaṃ","n.loc.sg + ppp, fused","in-venerable-Bhairavakula-was-said"),
 ("kulaparvaprapūjane","m.loc.sg","in-Kula-festival-pre-worship"),
 ("sthaṇḍile@gnau","m.loc.sg","on-altar-in-fire"),
 ("paṭe","m.loc.sg","on-cloth"),
 ("liṅge","m.loc.sg","on-liṅga"),
 ("pātre","m.loc.sg","on-vessel"),
 ("padme@tha","m.loc.sg","on-lotus-then"),
 ("maṇḍale","m.loc.sg","on-maṇḍala"),
]
GLOSS[45]=['in-venerable-Bhairavakula-was-said','in-Kula-festival-pre-worship','on-altar-in-fire','on-cloth','on-liṅga','on-vessel','on-lotus-then','on-maṇḍala']
QE[45]="In venerable Bhairavakula was said in Kula-festival-pre-worship: on altar-in-fire, on cloth, on liṅga, on vessel, on lotus-then, on maṇḍala."

ROWS[46]=[
 ("mūrtau","m.loc.sg","on-image"),
 ("ghaṭe@strasaṃghāte","m.loc.sg","on-pot-in-heap"),
 ("dhaṭe","m.loc.sg","on-brick"),
 ("sūtre@tha","m.loc.sg","on-thread-then"),
 ("pūjayet","opt (pūj)","should-worship"),
 ("svena","m.inst.sg","by-own"),
 ("svenopacāreṇa","m.inst.sg","by-own-service"),
 ("saṅkaraṃ","m.acc.sg","mixture"),
 ("varjayediti","opt (varj) + iti, fused","should-reject—thus"),
]
GLOSS[46]=['on-image','on-pot-in-heap','on-brick','on-thread-then','should-worship','by-own','by-own-service','mixture','should-reject—thus']
QE[46]="On image, on pot-in-heap, on brick, on thread-then: should worship by own, by own service; mixture should reject — thus."

ROWS[47]=[
 ("yathāpsu","m.loc.sg","as-in-waters"),
 ("śāntaye","f.dat.sg","for-peace"),
 ("mantrāstadvadastrādiṣu","m.nom.pl","mantras-so-in-weapons-and-the-rest"),
 ("dhruvam","adv","certainly"),
 ("śatrucchedādikartāraḥ","m.nom.pl","enemy-cutting-and-the-rest-doers"),
 ("kāmyo@taḥ","m.nom.sg","desired-from"),
 ("saṅkarojjhitaḥ","m.nom.sg","mixture-abandoned"),
]
GLOSS[47]=['as-in-waters','for-peace','mantras-so-in-weapons-and-the-rest','certainly','enemy-cutting-and-the-rest-doers','desired-from','mixture-abandoned']
QE[47]="As in waters for peace, mantras so in weapons and the rest certainly; enemy-cutting-and-the-rest-doers, desired from, mixture abandoned."

ROWS[48]=[
 ("akāmasya","m.gen.sg","of-the-desireless"),
 ("tu","particle","but"),
 ("te","dem","they"),
 ("tattatsthānopādhivaśāddhruvam","abl","from-that-that-place-condition-power-certainly"),
 ("pāśakartanasaṃśuddhatattvāpyāyādikāriṇaḥ","m.nom.pl","fetter-cutting-purified-tattva-nourishing-and-the-rest-doers"),
]
GLOSS[48]=['of-the-desireless','but','they','from-that-that-place-condition-power-certainly','fetter-cutting-purified-tattva-nourishing-and-the-rest-doers']
QE[48]="Of the desireless but they, from that-that-place-condition-power certainly: fetter-cutting-purified-tattva-nourishing-and-the-rest-doers."

ROWS[49]=[
 ("athavā","particle","or-else"),
 ("pustakaṃ","n.acc.sg","book"),
 ("tādṛgrahaḥśāstrakramombhitam","n.acc.sg","such-seizing-śāstra-sequence-possessing"),
 ("suśuddhaṃ","n.acc.sg","well-purified"),
 ("dīkṣitakṛtaṃ","n.acc.sg","by-initiated-made"),
 ("tatrāpyeṣa","adv + dem, fused","there-also-this"),
 ("vidhiḥ","m.nom.sg","rite"),
 ("smṛtaḥ","m.nom.sg (smṛ ppp)","is-remembered"),
]
GLOSS[49]=['or-else','book','such-seizing-śāstra-sequence-possessing','well-purified','by-initiated-made','there-also-this','rite','is-remembered']
QE[49]="Or-else book, such-seizing-śāstra-sequence-possessing, well-purified, by-initiated-made: there also this rite is remembered."

ROWS[50]=[
 ("itthaṃ","adv","thus"),
 ("svayaṃpratiṣṭheṣu","m.loc.pl","in-self-installations"),
 ("yāvadyāvatsthitirbhavet","rel + f.nom.sg + opt, fused","as-long-as-standing-is"),
 ("vibhavaistarpaṇaṃ","n.acc.sg","by-abundance-tarpaṇa"),
 ("śuddhistāvadvicchedavarjanam","n.acc.sg","purity-so-long-interruption-avoidance"),
]
GLOSS[50]=['thus','in-self-installations','as-long-as-standing-is','by-abundance-tarpaṇa','purity-so-long-interruption-avoidance']
QE[50]="Thus in self-installations, as long as standing is: by abundance tarpaṇa, purity so long interruption-avoidance."

ROWS[51]=[
 ("ata","adv","hence"),
 ("eva","particle","indeed"),
 ("yadā","rel adv","when"),
 ("bhūridinaṃ","n.acc.sg","many-days"),
 ("maṇḍalakalpanam","n.nom.sg","maṇḍala-construction"),
 ("tadā","adv","then"),
 ("dine","m.loc.sg","in-day"),
 ("dine","m.loc.sg","in-day"),
 ("kuryādvibhavaistarpaṇaṃ","opt + n.acc.sg, fused","should-perform-by-abundance-tarpaṇa"),
 ("bahu","n.acc.sg","much"),
]
GLOSS[51]=['hence','indeed','when','many-days','maṇḍala-construction','then','in-day','in-day','should-perform-by-abundance-tarpaṇa','much']
QE[51]="Hence indeed when many-days maṇḍala-construction: then in-day in-day should perform by abundance tarpaṇa, much."

ROWS[52]=[
 ("pratiṣṭhāyāṃ","f.loc.sg","in-installation"),
 ("ca","particle","and"),
 ("sarvatra","adv","everywhere"),
 ("guruḥ","m.nom.sg","guru"),
 ("pūrvoditaṃ","n.acc.sg ppp","aforesaid"),
 ("param","n.acc.sg","supreme"),
 ("satattvamanusandhāya","gerund (sam + ni + dhā)","having-sought-true-reality"),
 ("saṃnidhiṃ","m.acc.sg","presence"),
 ("sphuṭamācaret","opt + adv, fused","he-should-make-clear"),
]
GLOSS[52]=['in-installation','and','everywhere','guru','aforesaid','supreme','having-sought-true-reality','presence','he-should-make-clear']
QE[52]="In installation and everywhere guru, aforesaid supreme, having sought true reality, presence he should make clear."

ROWS[53]=[
 ("siddhe","m.loc.sg (sidh ppp)","in-accomplished"),
 ("tu","particle","but"),
 ("tanmayībhāve","m.loc.sg","in-tanmayatva-state"),
 ("phale","n.loc.sg","in-fruit"),
 ("putrakasādhakaiḥ","m.inst.pl","by-putraka-sādhakas"),
 ("anyasmai","m.dat.sg","to-another"),
 ("taddvayādanyatarasmai","m.dat.sg","from-that-pair-to-either"),
 ("tatsamarpyate","3sg.pres.pass (sam + ṛp)","that-is-offered"),
]
GLOSS[53]=['in-accomplished','but','in-tanmayatva-state','in-fruit','by-putraka-sādhakas','to-another','from-that-pair-to-either','that-is-offered']
QE[53]="In accomplished but in tanmayatva-state in fruit, by putraka-sādhakas to another, from that pair to either, that is offered."

ROWS[54]=[
 ("tasyāpyeṣa","gen.sg + dem, fused","of-it-also-this"),
 ("vidhiḥ","m.nom.sg","rite"),
 ("sarvastadalābhe","m.nom.sg + abl, fused","all-in-its-absence"),
 ("tu","particle","but"),
 ("sarvathā","adv","in-every-way"),
 ("agādhe@mbhasi","m.loc.sg","in-deep-water"),
 ("tatkṣepyaṃ","n.acc.sg","it-to-be-cast"),
 ("kṣamayitvā","gerund (kṣam)","having-asked-pardon"),
 ("visṛjya","gerund (vi + sṛj)","having-dismissed"),
 ("ca","particle","and"),
]
GLOSS[54]=['of-it-also-this','rite','all-in-its-absence','but','in-every-way','in-deep-water','it-to-be-cast','having-asked-pardon','having-dismissed','and']
QE[54]="Of it also this rite all in its absence but in every way: in deep water it to be cast, having asked pardon, having dismissed, and."

ROWS[55]=[
 ("ityeṣa","dem + n.nom.sg, fused","thus-this"),
 ("svapratiṣṭhānavidhiḥ","m.nom.sg","self-installation-rite"),
 ("śivanirūpitaḥ","m.nom.sg (nir + rūp ppp)","Śiva-set-forth"),
 ("parapratiṣṭhite","m.loc.sg","in-other-installed"),
 ("liṅge","m.loc.sg","in-liṅga"),
 ("bāṇīye@tha","m.loc.sg","in-Bāṇa-then"),
 ("svayaṃbhuvi","m.loc.sg","in-svayambhū"),
]
GLOSS[55]=['thus-this','self-installation-rite','Śiva-set-forth','in-other-installed','in-liṅga','in-Bāṇa-then','in-svayambhū']
QE[55]="Thus this self-installation-rite, Śiva-set-forth: in other-installed in liṅga, in Bāṇa-then, in svayambhū."

ROWS[56]=[
 ("sarvamāsanapakṣe","m.loc.sg","in-all-asana-side"),
 ("prāṅnyasya","gerund (ni + as)","having-placed-before"),
 ("saṃpūjayetkramam","opt + m.acc.sg, fused","should-worship-sequence"),
 ("śuddhāśuddhādhvajāḥ","m.nom.pl","pure-impure-adhva-ones"),
 ("sarve","m.nom.pl","all"),
 ("mantrāḥ","m.nom.pl","mantras"),
 ("sarvaḥ","m.nom.sg","all"),
 ("śivāntakaḥ","m.nom.sg","Śiva-ending"),
]
GLOSS[56]=['in-all-asana-side','having-placed-before','should-worship-sequence','pure-impure-adhva-ones','all','mantras','all','Śiva-ending']
QE[56]="In all-asana-side, having placed before, should worship sequence: pure-impure-adhva-ones, all mantras, all Śiva-ending."

ROWS[57]=[
 ("adhvā","m.nom.sg","adhva"),
 ("cehāsane","m.loc.sg","and-here-in-seat"),
 ("proktastatsarvatrārcayedidam","m.nom.sg + particle, fused","was-said-that-everywhere-worship-this"),
 ("āvāhanavisṛṣṭī","f.nom.du","invocation-dismissal"),
 ("tu","particle","but"),
 ("tatra","adv","there"),
 ("prāgvatsamācaret","opt + adv, fused","as-before-should-perform"),
]
GLOSS[57]=['adhva','and-here-in-seat','was-said-that-everywhere-worship-this','invocation-dismissal','but','there','as-before-should-perform']
QE[57]="Adhva and here in seat was said that everywhere worship this; invocation-dismissal but there as before should perform."

ROWS[58]=[
 ("uktaṃ","n.nom.sg (vac ppp)","was-said"),
 ("tantre@pyaghoreśe","n.loc.sg","in-tantra-also-Aghoreśa"),
 ("svacchande","n.loc.sg","in-Svacchanda"),
 ("vibhunā","m.inst.sg","by-Lord"),
 ("tathā","adv","so"),
 ("athavā","particle","or-else"),
 ("pratyahaṃ","adv","daily"),
 ("proktamānārdhārdhaniyogataḥ","adv","as-said-by-half-half-portion-appointment"),
]
GLOSS[58]=['was-said','in-tantra-also-Aghoreśa','in-Svacchanda','by-Lord','so','or-else','daily','as-said-by-half-half-portion-appointment']
QE[58]="Was said in tantra also Aghoreśa, in Svacchanda, by Lord; so or-else daily as said by half-half-portion-appointment."

ROWS[59]=[
 ("kṛtveṣṭaṃ","gerund (kṛ) + n.acc.sg, fused","having-made-desired"),
 ("maṇḍalaṃ","n.acc.sg","maṇḍala"),
 ("tatra","adv","there"),
 ("samastaṃ","n.acc.sg","all"),
 ("kramamarcayet","opt + m.acc.sg, fused","sequence-should-worship"),
 ("bahuprakārabhinnasya","gen.sg","of-much-kind-different"),
 ("liṅgasyārcā","f.nom.sg","liṅga-worship"),
 ("nirūpitā","f.nom.sg (nir + rūp ppp)","was-set-forth"),
]
GLOSS[59]=['having-made-desired','maṇḍala','there','all','sequence-should-worship','of-much-kind-different','liṅga-worship','was-set-forth']
QE[59]="Having made desired maṇḍala there, all sequence should worship, of much kind different, liṅga-worship was set forth."



# ---- populate TOK/CM/GLOSS/QE from ROWS (all verses) ----
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
print('a27 ALL verified: %d verses, %d tokens'%(len(TOK), sum(len(v) for v in TOK.values())))
