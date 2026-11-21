#!/usr/bin/env python3
"""Cumulative Muktabodha PR #18 translation bibliography, manual evidence batch v6.
Append published evidence only. New positives may be partial or root-only, not complete witness coverage.
"""
import csv,json,pathlib,shutil,collections
P=pathlib.Path(__file__).resolve().parent
C=P/'burn_research.csv'; E=P/'translation_editions.jsonl'; L=P/'manual_leads_and_exceptions.jsonl'
for now,old in ((C,P/'burn_research.pre-v6.csv'),(E,P/'translation_editions.pre-v6.jsonl')):
 if not old.exists():shutil.copyfile(now,old)
with C.open(encoding='utf8',newline='') as f:d=csv.DictReader(f); fields=d.fieldnames; rows=list(d)
eds=[json.loads(s) for s in E.read_text(encoding='utf8').splitlines() if s.strip()]
leads=[json.loads(s) for s in L.read_text(encoding='utf8').splitlines() if s.strip()]
byid={r['catalog']:r for r in rows if r['catalog']}
prior={r['catalog'] for r in rows if r['has_translation']=='TRUE'}
prior_eds=len(eds)
keys={(e['catalog'],e['translator'],e['year'],e['scope'],e['info_url']) for e in eds}
RESEARCHER='ChatGPT manual bibliography research, continuation v6'
def add(cid,translator,year,scope,url,publisher,language='en',evidence='',corroboration='',access='BUY',confidence='high',source='primary_publisher',download=''):
 assert cid in byid,cid
 assert url.startswith('https://'),url
 r=byid[cid]; k=(cid,translator,str(year),scope,url)
 if k in keys: return
 keys.add(k)
 e={'access_mode':'ONLINE_HTML' if access=='HTML' else ('ONLINE_PDF' if access=='PDF' else access),
 'access_tier':'DIRECT' if download else ('' if access in ('HTML','PDF') else access),
 'catalog':cid,'confidence':confidence,'corroboration_url':corroboration,'download_url':download,
 'evidence':evidence,'info_url':url,'language':language,'publication_status':'published',
 'publisher':publisher,'researcher':RESEARCHER,'scope':scope,'source_type':source,
 'title':r['title'],'translator':translator,'verification_status':'BIBLIOGRAPHICALLY_VERIFIED',
 'verified_at':'2026-11-11','year':str(year)}
 eds.append(e)
 if r['has_translation']!='TRUE':
  assert all(not r[x] for x in ('translator','year','scope_full_partial_chapters','info_url')),cid
  r.update(has_translation='TRUE',translator=translator,year=str(year),scope_full_partial_chapters=scope,
   access_tier=e['access_tier'],download_url=download,publisher=publisher,info_url=url,
   evidence_notes=evidence+' [For further editions and scope details consult translation_editions.jsonl.]',
   researcher=RESEARCHER,verified_at='2026-11-11')
def lead(cid,status,note,urls):
 assert cid in byid,cid
 if any(x.get('catalog')==cid and x.get('status')==status for x in leads):return
 leads.append({'catalog':cid,'title':byid[cid]['title'],'status':status,'note':note,'links':urls})

# Śivadharmaśāstra text: THREE individually verified translated chapters, not the Nandiprokta recension.
add('M00209','Peter C. Bisschop',2018,'partial: chapter 6 Śāntyadhyāya / The Chapter on Appeasement only, pp.147–188; other chapters not translated in this edition',
 'https://www.jstor.org/content/oa_chapter_monograph/10.1163/j.ctv2gjwspz.6','Brill, Universal Śaivism (Gonda Indological Studies 18)',
 evidence='Open JSTOR explicitly identifies book chapter as “The Chapter on Appeasement: Translation”, pp.147–188; BnF confirms 2018 Brill book edits and translates exactly Śivadharmaśāstra ch.6.',
 corroboration='https://catalogue.bnf.fr/ark:/12148/cb45728577p',access='HTML',source='scholarly_edition',confidence='high')
add('M00209','Peter C. Bisschop, Nirajan Kafle and Timothy Lubin',2021,'partial: Śivadharmaśāstra chapter 11 Śivāśramādhyāya only; critical edition and annotated English translation',
 'https://www.fedoabooks.unina.it/index.php/fedoapress/en/catalog/book/305','UniorPress, Studies on the History of Śaivism 1',
 evidence='University press monograph states a critical edition and annotated English translation of the eleventh chapter of the Śivadharmaśāstra, with DOI 10.6093/978-88-6719-215-1.',access='HTML',source='university_publisher')
add('M00209','Peter C. Bisschop, Nirajan Kafle and Csaba Kiss',2025,'partial: Śivadharmaśāstra chapter 10 only; ALSO English translation of a Sanskrit commentary to that chapter',
 'https://www.fedoabooks.unina.it/index.php/fedoapress/en/catalog/book/612','UniorPress, Studies on the History of Śaivism 3',
 evidence='UniorPress confirms Sanskrit edition and English translation of chapter ten plus an edition/translation of its anonymous commentary; University of Naples repository dates February 2025.',
 corroboration='https://www.fedoa.unina.it/15335/',access='HTML',source='university_publisher')
# Historical genuine partial translation independently cited by later scholarly study.
add('M00014','Agnihotri Śāstrī',1941,'partial: FIRST TWO vimarśas of Cidgaganacandrikā translated into English; Divyacakorikā Sanskrit commentary included, translation of all commentary not established',
 'https://www.wisdomlib.org/hinduism/book/cidgaganacandrika-study/d/doc628945.html',
 'Śrī Śāradā Printing Press, Amalapuram (Divyacakorikā)',
 evidence='Scholarly Cidgaganacandrikā study explicitly states Agnihotri Śāstrī (1941) gave English translation “for the first two vimarśas only”; no claim that later sections were translated.',access='PRINT',confidence='medium',source='scholarly_secondary_bibliography')
# A translated root but an un-translated commentary inside the Muktabodha combined title.
add('M00351','K. Narayanaswami Aiyer',1896,'root only: free English translation of Abhinanda’s Laghu-Yoga-Vāsiṣṭha; NOT English translation of Vāsiṣṭhacandrikā commentary included in Muktabodha witness',
 'https://tamildigitallibrary.in/Articles/%E0%AE%A8%E0%AF%82%E0%AE%B2%E0%AF%8D-48065-A%20translation%20of%20Yoga-Va%CC%82sishta-Laghu%20%28the%20smaller%29',
 'Thomson & Co., Madras',evidence='Tamil Digital Library 1896 original printed edition and Adyar Library reprint preface specifically name Narayanaswami Aiyer as English translator. Translates Sanskrit ROOT, NOT Vāsiṣṭhacandrikā.',
 corroboration='https://ge.nii.ac.jp/ncid/BA01598674',access='HTML',source='digital_library')
add('M00351','K. Narayanaswami Aiyer',1971,'root only: second edition / revised reprint of 1896 English Laghu-Yoga-Vāsiṣṭha; commentary Vāsiṣṭhacandrikā untranslated',
 'https://ge.nii.ac.jp/ncid/BA01598674','The Adyar Library and Research Centre, General Series 3',
 evidence='CiNii union catalogue identifies 1971 edition as English translation, 2nd edition and explicitly dates original 1896. Commentary identity not assumed.',access='PRINT',source='university_library')
# Hindi editions: printed source actually says Sanskrit TEXT + Hindi TRANSLATION, not merely Hindi introduction.
add('M00054','Bhīm Singh Biṣṭa',2025,'full or substantial: Sanskrit Śāktapramoda with Hindi translation/explanation; exact root verses and sections not collated',
 'https://bharatiyavidya.com/product/shakta-pramoda/','D.P.B. Publications, Delhi',language='hi',
 evidence='Bookstore bibliography lists 2025 Śākta Pramoda, Bhīm Singh Biṣṭa, 913 pages, bilingual Sanskrit and Hindi; separate bibliographic retail listing explicitly advertises Sanskrit-Hindi text.',confidence='medium',source='publisher_retail_bibliography')
add('M00625','Rādheśyām Chaturvedī',2014,'full or substantial: Sanskrit Dakṣiṇāmūrtisaṃhitā with Hindi translation; 270 pages; no recension collation',
 'https://chaukhambabooks.co.in/product/Sri-Dakshinamurti-Samhita--gOdvq','Chaukhamba Surbharati Prakashan',language='hi',
 evidence='Chaukhamba publisher explicitly lists publishing date 2014, 270 pp, Sanskrit text with Hindi translation and author/translator Rādheśyām Chaturvedī.',source='primary_publisher')
add('M00026','Pradīp Kumār Rāy',2010,'full or substantial: Kaṅkālamālinītantra with Sanskrit text and Hindi translation, exact 535-verse witness alignment uncollated',
 'https://www.exoticindiaart.com/book/details/kankal-malini-tantra-haa392/','Prācyaprakāśan, Vārāṇasī',language='hi',
 evidence='Detailed bookseller record labels 2010 edition Sanskrit Text with Hindi Translation, Pradip Kumar Rai, 106 pp; independent Bharatiya Vidya inventory lists same editor and year, 89 pp (pagination discordance flagged).',
 corroboration='https://bharatiyavidya.com/product/kankal-malini-tantram/',source='publisher_retail_bibliography')
add('M00026','S. N. Khandelwāl',1993,'full or substantial: independently published Kaṅkālamālinītantra Sanskrit with Hindi translation, 90 pp; text witness collation pending',
 'https://bharatiyavidya.com/product/kankal-malini-tantra/','Bhāratīya Vidyā Saṃsthān, Vārāṇasī',language='hi',
 evidence='Seller describes 1993 first edition, 90 pp Sanskrit and Hindi and explicitly names S. N. Khandelwal as translator; separate from Pradīp Rai 2010 edition.',source='publisher_retail_bibliography')
add('M00537','Pradīp Kumār Rāy',2010,'partial or source division uncertain: 2010 printed Hindi Muṇḍamālātantra; confirm which chapters correspond to Muktabodha part 1 versus part 2 before asserting full translation',
 'https://www.exoticindiaart.com/book/details/mundamala-tantra-haa394/','Prācyaprakāśan, Vārāṇasī',language='hi',
 evidence='2010 Sanskrit text with Hindi translation, Pradip Kumar Rai, 232 pp. Catalog M00537 and M00538 split source in two; printing chapter mapping not available. Assign to part1 cautiously and do not propagate to part2.',confidence='medium',source='publisher_retail_bibliography')
add('M00116','Swāmī Śatrughna Dās',2016,'full or substantial: Bṛhannīlatantra Sanskrit with Hindi translation; 608pp; source transcribed verses=27 may be excerpt',
 'https://www.exoticindiaart.com/book/details/brihad-nila-tantram-tantric-method-of-worshipping-goddess-kali-and-tara-nzj749/','Śrī Madhusūdan Prakāśan, Uttarakhand',language='hi',
 evidence='Bookseller identifies bilingual Sanskrit Text with Hindi Translation, translator attributed Swami Shatrughna Das, 2016 608 pages. The Muktabodha CSV lists 27 units; cannot infer equivalence to full 608pp edition.',source='publisher_retail_bibliography')
add('M00095','Aśok Kumār Gaur Śāstrī',2010,'full or substantial: Tārārahasya root Sanskrit text with Hindi translation (NOT Tārārahasyavṛtti commentaries)',
 'https://chaukhambabooks.co.in/product/Tara-Rahasya---0fdft','Chaukhamba Surbharati Prakashan',language='hi',
 evidence='Chaukhamba publisher lists 2010, 480 pages, Sanskrit Text with Hindi Translation, Aśok Kumār Gaur Śāstrī. This is not evidence for distinct M00323/M00096 commentaries.',source='primary_publisher')
add('M00231','Rām Rañjan Mālavīya',2005,'full or substantial: Kaulāvalīnirṇaya root Sanskrit with Hindi translation; 2005 edition',
 'https://chaukhambabooks.co.in/product/Kaulavali-Nirnaya--Belongs-to-Kaula-Sampradaya--qIVeD','Chaukhamba Sanskrit Series Office',language='hi',
 evidence='Publisher explicitly specifies Sanskrit Text with Hindi Translation, Rām Rañjan Mālavīya, 2005 and ISBN 9788170801719.',source='primary_publisher')
for cid,khanda in [('M00128','Kālīkhaṇḍa'),('M00119','Tārākhaṇḍa'),('M00129','Sundarīkhaṇḍa')]:
 add(cid,'Sudhākar Mālavīya and Cittarañjan Mālavīya',2023,
  f'full or substantial: Śaktisaṃgamatantra {khanda} in four-volume Sanskrit-Hindi translated/commented set; exact Muktabodha segment witness not collated',
  'https://www.exoticindiaart.com/book/details/shakti-sangam-tantram-set-of-4-volumes-mzf630/',
  'Chowkhamba Sanskrit Series Office, 4-volume Śaktisaṃgamatantra (ISBN 9788170803959)',language='hi',
  evidence=f'2023 bookseller identifies 4 volumes, Sanskrit Text with Hindi Translation, editors Sudhakar/Chittaranjan Malaviya; publisher description identifies each of four khanda incl. {khanda}.',
  corroboration='https://bharatiyavidya.com/product/shakti-sangam-tantram-set-of-4-vols/',source='publisher_retail_bibliography')
 add(cid,'Rādheśyām Chaturvedī and Śaśiśekhar Chaturvedī',2021,
  f'full or substantial: Śaktisaṃgamatantra {khanda}, Sanskrit with Jñānavatī Hindi commentary/translation, separate four-volume edition',
  'https://www.ibpbooks.com/sri-saktisangama-tantram-with-jnanavati-hindi-commentary-part-1-kali-khanda-part-2-tara-khanda-part-3-sundari-khanda-part-4-chinnamasta-khanda/p/53760',
  'Chaukhamba/Indian Books and Periodicals, four-volume Jñānavatī Hindi Commentary set',language='hi',
  evidence=f'Bookseller explicitly names four khanda including {khanda}, editors Acharya Radheshyam and Dr Shashi Shekhar Chaturvedi, Sanskrit+Hindi, 2021; commentary not assumed literal line-by-line.',
  confidence='medium',source='publisher_retail_bibliography')
add('M00646','Rādheśyām Chaturvedī',2024,'full or substantial: Gandharvatantra Sanskrit with Hindi translation and Jñānavatī Hindi commentary',
 'https://www.exoticindiaart.com/book/details/gandharva-tantram-with-jnanawati-hindi-commentary-nza180/',
 'Chowkhamba Sanskrit Series Office',language='hi',
 evidence='2024 bookseller identifies Gandharva Tantram (with Jnanawati Hindi Commentary), Prof. Radheshyam Chaturvedi, Sanskrit Text with Hindi Translation, 625pp, ISBN 9788170803089.',source='publisher_retail_bibliography')
add('M00132','Rādheśyām Chaturvedī',2014,'full or substantial: Kāmākhyātantra Sanskrit text with Hindi translation; 112 pp',
 'https://www.chaukhambabooks.co.in/product/Kamakhya-Tantram--57Fov',
 'Chaukhamba Surbharati Prakashan',language='hi',
 evidence='Publisher lists Sanskrit Text with Hindi Translation, Acharya Radhe Shyam Chaturvedi, publishing date 2014, 112 pp.',source='primary_publisher')
add('M00132','S. N. Khandelwāl','n.d.','full or substantial: second Kāmākhyātantra Sanskrit with Hindi translation; 172 pp; publication date not listed',
 'https://www.exoticindiaart.com/book/details/kamakhya-tantram-nzz039/','Chowkhamba Sanskrit Series Office',language='hi',
 evidence='Separate 172-page edition ISBN 9788170804826, bibliographic language explicitly Sanskrit Text with Hindi Translation, named S.N. Khandelwal; no date provided, do not infer 2014.',source='publisher_retail_bibliography')
add('M00133','Sudhākar Mālavīya and Annapūrṇā Mālavīya','n.d.','full or substantial: Kāmadhenutantra with Ānandā Hindi translation, 240pp, ISBN 9788170805441',
 'https://chaukhamba.co.in/index.php?product_id=5388&route=product%2Fproduct','Chowkhamba Sanskrit Series Office',language='hi',
 evidence='Publisher explicitly identifies Sanskrit Text with Hindi Translation (Ānandā), translators Sudhakar and Annapurna Malaviya, 240pp, ISBN 9788170805441. No date shown by primary publisher.',source='primary_publisher')
add('M00013','Kapil Dev Nārāyaṇ',2011,'full or substantial: Bṛhattantrasāra Sanskrit text with Hindi translation in two volumes, 1,274 pp',
 'https://www.exoticindiaart.com/book/details/brihat-tantra-sara-set-of-2-volumes-nza079/',
 'Chaukhamba Surbharati Prakashan',language='hi',
 evidence='2011 2-volume Sanskrit Text with Hindi Translation explicitly documented, 1274pp, ISBN 9789380326825; DO NOT confuse with separate 1985 Sanskrit edition having only a Hindi preface.',source='publisher_retail_bibliography')
add('M00195','Kapil Dev Nārāyaṇ',2021,'full or substantial: Merutantra Sanskrit text with Hindi translation in five volumes, 2,182 pages',
 'https://www.exoticindiaart.com/book/details/meru-tantram-set-of-5-volumes-pzz693/',
 'Chaukhamba Surbharati Prakashan',language='hi',
 evidence='2021 five-volume Meru Tantram, Sanskrit Text with Hindi Translation, Kapil Dev Narayan, 2182pp, ISBN 9789389665154; source witness crosswalk pending.',source='publisher_retail_bibliography')

# New additions for previously documented source texts (do NOT change their primary CSV rows).
for cid in ('M00092','M00093'):
 add(cid,'Rādheśyām Chaturvedī','n.d.',
  'partial/coverage TBD: Sanskrit and Hindi translation of Tantrāloka in five volumes; publisher volumes chapter ranges not established for Muktabodha split records',
  'https://www.exoticindiaart.com/book-author/radheshyam/',
  'Chaukhamba (Tantrāloka, 5 volumes)',language='hi',
  evidence='Publisher’s catalog describes Tantrāloka “saṃskṛta evam hindī anuvāda (pāñc khaṇḍoṃ meṃ)” by Rādheśyām Chaturvedī. No year or exact āhnika ranges independently supplied.',confidence='medium',source='publisher_retail_bibliography')
# Negative/ambiguous research MUST not turn into negative absence statements or a false positive.
lead('M00210','SIVADHARMA_RECENSION_ALIGNMENT_REQUIRED','2021, 2025, 2018 chapters translate Śivadharmaśāstra, not necessarily the distinct catalog entry named Śivadharma Nandiprokta. Verify Sanskrit incipits before copying M00209 claims.',
 ['https://www.fedoabooks.unina.it/index.php/fedoapress/en/catalog/book/305','https://www.fedoabooks.unina.it/index.php/fedoapress/en/catalog/book/612'])
lead('M00538','MUNDAMALA_PART_2_SOURCE_COLLATION_REQUIRED','Pradip Kumar Rai 2010 Hindi printed Mundamala Tantra does not specify which part corresponds to Muktabodha second part M00538; do not infer translation of M00538.',
 ['https://www.exoticindiaart.com/book/details/mundamala-tantra-haa394/'])
lead('M00096','TARARAHASYA_COMMENTARY_NOT_AUTOMATIC','2010 Hindi Tārārahasya root translation does NOT demonstrate a translation of distinct Tārārahasyavṛttikā commentary M00096.',
 ['https://chaukhambabooks.co.in/product/Tara-Rahasya---0fdft'])
lead('m00323','TARARAHASYA_VRTTI_SOURCE_ID_AND_COMMENTARY_NOT_AUTOMATIC','2010 Hindi Tārārahasya root edition cannot prove translation of commentary M00323; note this catalog ID is lowercase m in source.',
 ['https://chaukhambabooks.co.in/product/Tara-Rahasya---0fdft'])
lead('M00029','KRAMADIPIKA_DIFFERENT_AUTHOR','Modern printed Hindi Kramadipika often Keśavakāśmīri, while catalog M00029 attributes work to Rāsikamohana; do not merge by title alone.',
 ['https://www.exoticindiaart.com/'])
lead('M00342','SADHANAMALA_PUBLISHER_ENGLISH_INTRO_NOT_FULL_TRANSLATION','1925–28 Sādhanamālā Sanskrit critical edition has an English introduction, which is not a complete English translation; separate excerpts from iconography literature need sādhanā-number mapping.',
 ['https://ci.nii.ac.jp/ncid/BA63304590'])
lead('M00343','SADHANAMALA_VOLUME_TWO_ENGLISH_INTRO_NOT_TRANSLATION','1925–28 Sanskrit Sādhanamālā Vol.2 has English introductory matter but the Sanskrit sādhanās are not thereby translated. Do not mark TRUE based on preface.',
 ['https://ci.nii.ac.jp/ncid/BA63304590'])
lead('M00038','NETRATANTRA_FORTHCOMING_NOT_PUBLISHED','Flood and Wernicke-Olesen forthcoming Routledge text/translation chapters 1–8 bears 2027 copyright and prepublication listings; check actual release, do not count as published in 2026-11.',
 ['https://www.routledge.com/Tantra-in-Medieval-India-and-Nepal-An-annotated-edition-and-translation-of-The-Teaching-of-the-Lord-of-Immortality-the-Netra-Tantra-Chapters-1-8/Flood-Wernicke-Olesen/p/book/9780367709600'])
with C.open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
with E.open('w',encoding='utf8') as f:
 for e in eds:f.write(json.dumps(e,ensure_ascii=False,sort_keys=True)+'\n')
with L.open('w',encoding='utf8') as f:
 for e in leads:f.write(json.dumps(e,ensure_ascii=False,sort_keys=True)+'\n')
newpos={r['catalog'] for r in rows if r['has_translation']=='TRUE'}-prior
print(json.dumps({'new_works':len(newpos),'new_catalogs':sorted(newpos),'total_works':len(prior|newpos),'new_editions':len(eds)-prior_eds,'total_editions':len(eds),'unresolved':499-len(prior|newpos),'manual_leads':len(leads)},ensure_ascii=False,indent=2))
