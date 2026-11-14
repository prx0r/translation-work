#!/usr/bin/env python3
"""Add verified translations to the cumulative PR18 499-row bibliography, batch v5.
Do not conflate related texts, editions, and translations of recensions.
Repeat execution idempotently; preserve previous records and source metadata.
"""
import csv,json,pathlib,shutil,collections
P=pathlib.Path(__file__).resolve().parent
C=P/'burn_research.csv'; E=P/'translation_editions.jsonl'; L=P/'manual_leads_and_exceptions.jsonl'
# One-time previous snapshot for independent validation, not a replacement of the live CSV.
for now,old in [(C,P/'burn_research.pre-v5.csv'),(E,P/'translation_editions.pre-v5.jsonl')]:
 if not old.exists():shutil.copyfile(now,old)
with C.open(newline='',encoding='utf8') as f:
 d=csv.DictReader(f);fields=d.fieldnames;rows=list(d)
with E.open(encoding='utf8') as f: eds=[json.loads(s) for s in f if s.strip()]
with L.open(encoding='utf8') as f: leads=[json.loads(s) for s in f if s.strip()]
byid={r['catalog']:r for r in rows if r['catalog']}
origpos={r['catalog'] for r in rows if r['has_translation']=='TRUE'}
keys={(e['catalog'],e['translator'],e['year'],e['scope'],e['info_url']) for e in eds}
RESEARCHER='ChatGPT manual bibliography research, continuation v5'
def add(cid,translator,year,scope,url,publisher,language='en',evidence='',corroboration='',access='BUY',confidence='high',source='university_library',download=''):
 assert cid in byid,cid
 assert url.startswith('https://'),url
 r=byid[cid];key=(cid,translator,str(year),scope,url)
 if key in keys:return
 keys.add(key)
 e={'access_mode':'ONLINE_HTML' if access=='HTML' else ('ONLINE_PDF' if access=='PDF' else access),'access_tier':'DIRECT' if download else ('' if access in ('HTML','PDF') else access),'catalog':cid,'confidence':confidence,'corroboration_url':corroboration,'download_url':download,'evidence':evidence,'info_url':url,'language':language,'publication_status':'published','publisher':publisher,'researcher':RESEARCHER,'scope':scope,'source_type':source,'title':r['title'],'translator':translator,'verification_status':'BIBLIOGRAPHICALLY_VERIFIED','verified_at':'2026-11-11','year':str(year)}
 eds.append(e)
 if r['has_translation']!='TRUE':
  assert all(not r[x] for x in ('translator','year','scope_full_partial_chapters','info_url')),cid
  r.update(has_translation='TRUE',translator=translator,year=str(year),scope_full_partial_chapters=scope,access_tier=e['access_tier'],download_url=download,publisher=publisher,info_url=url,evidence_notes=evidence+' [Other versions and scope details in translation_editions.jsonl.]',researcher=RESEARCHER,verified_at='2026-11-11')
def lead(cid,status,note,urls):
 assert cid in byid,cid
 if any(x.get('catalog')==cid and x.get('status')==status for x in leads):return
 leads.append({'catalog':cid,'title':byid[cid]['title'],'status':status,'note':note,'links':urls})

# The primary printed Pandey translation, the 1998 second edition, and a modern reissue.
for year,url,pub,ev in [
 (1954,'https://ge.nii.ac.jp/ncid/BA63362076','Lucknow University / Princess of Wales Saraswati Bhavana Texts','CiNii university library catalogue explicitly identifies v.3 (1954) as English translation of Abhinavagupta’s Īśvarapratyabhijñāvimarśinī with Sanskrit.'),
 (1998,'https://ci.nii.ac.jp/ncid/BB21125650','Sampurnanand Sanskrit University, Sarasvati Bhavana texts 84','CiNii explicitly lists second edition 1998, Part 3, Kanti Chandra Pandey, English translation of Īśvarapratyabhijñāvimarśinī.'),
 (2021,'https://books.google.com/books/about/Bh%C4%81skar%C4%AB.html?id=MeQ8zwEACAAJ','Sampurnanand Sanskrit Vishvavidyalaya, Institute of Academic Research & Publication','Google Books 2021 Bhāskarī identifies an English translation in title; modern reissue with editor Hareram Tripathi, independently distinguish from Pandey translation.')]:
 add('M00019','Kanti Chandra Pandey',year,'full: Abhinavagupta Īśvarapratyabhijñāvimarśinī English translation, volume 3 (Bhāskarī); additional Bhāskarakaṇṭha Sanskrit commentary not proven translated',url,pub,evidence=ev,source='university_library' if year<2021 else 'book_bibliography',access='PRINT' if year==1954 else 'BUY')
# Two independent, catalogued translations, and a documented 1961 reprint.
for cid in ('M00025','M00282'):
 add(cid,'Arthur Avalon (John Woodroffe)',1922,'full: original Kāmakalāvilāsa root English translation with Naṭanānanda commentary; two Muktabodha IDs may encode different recensions', 'https://ge.nii.ac.jp/ncid/BA56893742','Āgamānusandhāna Samiti / Luzac, Tantrik Texts vol. 10',evidence='CiNii catalog labels 1922 edition translated by Arthur Avalon and notes Sanskrit and English; commentary not automatically all translated.',access='PRINT')
 add(cid,'Arthur Avalon (John Woodroffe)',1961,'full: third-edition reprint of Avalon Kāmakalāvilāsa English translation', 'https://ci.nii.ac.jp/ncid/BA77547885','Ganesh & Co, Madras',evidence='CiNii university library explicitly labels this 1961 third edition as with English translation and notes.',access='PRINT')
 add(cid,'Rāmāyaṇa Prasāda Dvivedī and Sudhākara Mālavīya',2004,'full: Kāmakalāvilāsa root with Naṭanānanda Cidvallī Sanskrit commentary and English translation; coverage of Cidvallī translation not independently proven','https://ci.nii.ac.jp/ncid/BB02052185','Chaukhamba Sanskrit Pratishthan / Chaukhamba Surabharati Prakashan',evidence='Original CiNii university catalogue: “edited & translated by” Dvivedi and Malaviya, with Cidvallī Sanskrit commentary and English translation, xii+152pp.',access='BUY')
# Publisher itself establishes translations, no inference from mere English introductions.
add('M00402','Louise M. Finn',1986,'full or substantial: Kulacūḍāmaṇi Nigama English translation, alongside Vāmakeśvaratantra; compare source recension before full coverage gate','https://www.harrassowitz-verlag.de/title_4083.ahtml','Harrassowitz Verlag',evidence='Publisher explicitly states BOTH tantras translated from original Sanskrit in 417-page English book (ISBN 9783447026581).',access='BUY',source='primary_publisher')
# 2026 independent online translation made from Bagchi and Muktabodha copies.
add('M00003','Adi Suyash',2026,'full or substantial: online English Akulavīratantra translation; site announces linked PDF but exact download address unverified','https://adisuyash.com/akulaviratantra-english-translation/','Adi Suyash (author’s website)',evidence='Author’s article dated 2026-10-18 explicitly says they translated Akulavīratantra using Bagchi and Muktabodha texts. Scope claimed whole text, but PDF not independently inspected; no direct download URL invented.',access='HTML',confidence='medium',source='self_published_direct_translation')
# Genuine Hindi Siddhitrayī translation, including all three Sanskrit root works.
for cid in ('M00502','M00658','M00023','M00660','M00080'):
 add(cid,'Sūrya Prakāśa Vyāsa',1989,'full or substantial: Hindi translation of root Utpaladeva Siddhitrayī (Ajaḍapramātṛsiddhi, Īśvarasiddhi, Sambandhasiddhi), plus Vṛtti where included; align duplicate Muktabodha IDs separately','https://ci.nii.ac.jp/ncid/BA10296960','Chaukhambha Sanskrit Sansthan, Kashi Sanskrit Series 259',language='hi',evidence='CiNii official catalogue lists all three constituent works, and states Hindi translation and “Edited and translated by Surya Prakash Vyas” on added English title page. One collective edition counted once per matching catalog ID.',access='PRINT',source='university_library')
for cid in ('M00502','M00658'):
 add(cid,'David Peter Lawrence',2009,'full: article translation of Ajaḍapramātṛsiddhi and the Harabhaṭṭa Śāstrī Vṛtti, pp. 641–652','https://dlbs.liberal.ntu.edu.tw/en/search/search_detail.jsp?seq=376893','Journal of Indian Philosophy 37(6):627–653, Springer',evidence='University NTU indexed journal abstract explicitly says provides introduction to and translation of Ajaḍapramātṛsiddhi with Vṛtti; contents show “Translation” begins page 641.',access='BORROW',source='university_journal_index')
# Exact source edition title matched to original 1903 Muktabodha printed witness.
add('M00621','Kṛṣṇājī Nārāyaṇa Jośī',1903,'full or substantial: 1903–1904 Sanskrit Prabhuliṅgalīlā printed with Marathi translation; source volume distribution uncollated','https://dsal.uchicago.edu/bibliographic/bmcatalogs/Z7049.I3B85.pdf','Solapur printed edition / British Museum library holdings, 1903–1904',language='mr',evidence='1915 British Museum catalogue explicitly records Prabhulingalīlā Sanskrit text with Marathi translation by Kṛṣṇājī Nārāyaṇa Jośī, 1903–04; Sanskrit Wikisource Muktabodha record M00621 derives from 1903 Solapur print. Individual translated passages not separately collated.',corroboration='https://sa.wikisource.org/wiki/प्रभुलिङ्गलीला',access='PRINT',source='historical_library_catalogue')
# Hindi language publisher storefront, edition existence verified but authorship not independently established.
add('M00064','Pandit Kanhaiyalal Mishra (listed author; translator attribution needs inspection)','n.d.','full or substantial: 516-page Yoginītantra printed with Sanskrit and Hindi translation; exact Hindi translator and Sanskrit recension require verification','https://surplus-factory.myshopify.com/products/yogini-tantra-yoginitantra-sanskrit-text-with-hindi-translation','Khemraj Shri Krishna Das Prakashan',language='hi',evidence='Marketplace bibliographic listing explicitly labels Sanskrit Text with Hindi Translation, 516pp, and names Pandit Kanhaiya Lal Mishra as author; cannot assert he personally translated without title-page inspection.',confidence='medium',access='PRINT',source='book_retail_bibliography')
# Ahirbudhnyasaṃhitā part I of two catalog records; publisher explicitly first 7 chapters only.
add('M00002a','Mitsunori Matsubara',1994,'partial: Ahirbudhnyasaṃhitā chapters 1–7 only, critical annotated English translation; first printed source volume assumed, verify chapter ranges','https://www.mlbd.in/products/pancaratra-samhitas-and-early-vaisnava-theology-mitsunori-matsubara-9788120812215-8120812212','Motilal Banarsidass Publishing House',evidence='Publisher specifies Part Two contains fully annotated English translation of only FIRST SEVEN CHAPTERS; do not propagate to volume 2, M00002b, without source alignment.',access='BUY',source='primary_publisher')
# More editions for already positive root works (do not rewrite primary row).
add('M00153','Gautam Chatterjee',2015,'full or substantial: Sanskrit text with English translation of Tantrasāra','https://ci.nii.ac.jp/ncid/BB21062095','Indian Mind / Indica Books, Abhinava Gupta Tantra series 8',evidence='CiNii university library lists 2015 edited/translated by Gautam Chatterjee, Sanskrit Roman and Devanagari, English translation, pp. 581–584 references.',access='BUY')
for cid in ('M00092','M00093'):
 add(cid,'Gautam Chatterjee',2008,'partial multi-volume Śrītantrāloka Sanskrit/English translation, at least vols. 1–5; cannot assert all 38 āhnikas or exact source half coverage','https://ci.nii.ac.jp/ncid/BB01211228','Indian Mind / Indica Books, Abhinava Gupta Tantra series 1–5',evidence='CiNii records five-volume set begun 2008 explicitly “text with English translation”; mapping each āhnika to M00092 (1–14) vs M00093 (15–38) not independently corroborated, so do not count this edition as full source coverage.',access='BUY',confidence='medium')
add('M00091','Teun Goudriaan',1992,'partial: selected discussion/translation of awakening stages in Svacchandatantra; exact verses not collated','https://list.indology.info/pipermail/indology/2016-September/044180.html','SUNY Press, Tantrism: Studies in Honor of André Padoux, pp. 139–173',evidence='Academic contents list Goudriaan “The stages of awakening in the Svacchanda-Tantra” pp.139–173. Inclusion of complete verse translation not independently verified; supplemental edition evidence only.',access='PRINT',confidence='medium',source='academic_contents_bibliography')
# Strongly justified exclusions: different source language, root vs commentary, citation without translation.
lead('M00239','ASSAMESE_REDACTION_NOT_VERIFIED_SANSKRIT_ROOT','Assam Government 1928 Kamaratna Tantra is explicitly an Assamese text with parallel English translation; Muktabodha M00239 is cataloged Sanskrit Kamaratnatantra. Compare chapters/recension before marking root Sanskrit translation TRUE.', ['https://dhas.assam.gov.in/sites/default/files/swf_utility_folder/departments/dhas_medhassu_in_oid_6/portlet/level_1/files/LIST%20OF%20PUBLICATION-.pdf','https://books.google.com/books/about/Kamaratna_Tantra_Edited_by_Pandit_Hemcha.html?id=tRsHMwEACAAJ'])
lead('M00122','SANSKRIT_ONLY_ENGLISH_INTRODUCTION_NOT_TRANSLATION','Motilal Banarsidass Tantrarājatantra seller explicitly labels Sanskrit Only (English Introduction); previous heuristic English title/intro must not count as a translated root.', ['https://www.motilalbanarsidass.com/collections/tantra/products/tantraraja-tantra'])
lead('M00306','LAGHUSTAVA_LAGHUSTUTI_BĀLĀVIṂŚATI_IDENTITY_UNVERIFIED','2022 Religions article translates complete Bālāviṃśati (20 verses), widely called Laghustuti. Catalog M00306 laghustava records 38 source units. Requires opening first and last Sanskrit verses to verify identity, not automatically TRUE.', ['https://www.mdpi.com/2077-1444/13/7/667'])
lead('M00355','LAGHUSTUTI_COMMENTARY_TRANSLATION_UNPROVEN','2022 Karasiński-Sroka and Sharman translate 20-verse Bālāviṃśati root but do not establish translation of Rāgavānanda commentary cataloged under M00355.', ['https://www.mdpi.com/2077-1444/13/7/667'])
lead('M00615','PRINTED_1905_TITLE_SĀRASANGRAHA_DIFFERS_FROM_CATALOG_SAṄGRAHA','1915 British Museum catalogue identifies a 1905–06 Marathi translation of Anādi-Vīraśaiva-SĀRASANGRAHA, but Muktabodha M00615 is Anādivīraśaiva-SAṄGRAHA. Compare actual Sanskrit incipits before merging.', ['https://dsal.uchicago.edu/bibliographic/bmcatalogs/Z7049.I3B85.pdf'])
lead('M00002b','PART_ONE_TRANSLATION_CANNOT_BE_EXTENDED_TO_VOLUME_TWO','Matsubara 1994 English translates Ahirbudhnyasaṃhitā chapters 1–7 only. M00002b is second volume; do not infer translation of its text.', ['https://www.mlbd.in/products/pancaratra-samhitas-and-early-vaisnava-theology-mitsunori-matsubara-9788120812215-8120812212'])
lead('M00030','SAMPLED_QUOTATIONS_NOT_FULL_ROOT','Dyczkowski A Journey in the World of the Tantras 2004 is cited for individual Kubjikāmatatantra passages, but online automated verse pages are not proof of full root translation or exact identity with generic catalog Kubjikātantra.', ['https://www.wisdomlib.org/hinduism/book/kubjikamatatantra-sanskrit/d/doc900181.html'])
with C.open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
with E.open('w',encoding='utf8') as f:
 for e in eds:f.write(json.dumps(e,ensure_ascii=False,sort_keys=True)+'\n')
with L.open('w',encoding='utf8') as f:
 for e in leads:f.write(json.dumps(e,ensure_ascii=False,sort_keys=True)+'\n')
newpos={r['catalog'] for r in rows if r['has_translation']=='TRUE'}-origpos
print(json.dumps({'new_catalogs':sorted(newpos),'new_work_count':len(newpos),'total_documented_works':len(origpos|newpos),'new_edition_records':len(eds)-143,'total_editions':len(eds),'unresolved_works':499-len(origpos|newpos),'leads':len(leads)},indent=2))
