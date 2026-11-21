#!/usr/bin/env python3
"""Cumulative second-pass bibliography additions; does not erase earlier PR #18 research.
Run once against the 2026-11-11 research package. All additions keyed by catalog+source URL+scope+translator.
Only bibliographic assertions grounded in listed external pages are promoted to has_translation=TRUE.
"""
from __future__ import annotations
import csv, json, pathlib, datetime, collections
P=pathlib.Path(__file__).resolve().parent
DATE='2026-11-11'
RESEARCHER='ChatGPT manual bibliography research, continuation v2'
basepath=P/'burn_research.csv'; editionspath=P/'translation_editions.jsonl'
with basepath.open('r',encoding='utf-8-sig',newline='') as f:
 rd=csv.DictReader(f); columns=rd.fieldnames; rows=list(rd)
idx={r['catalog']:r for r in rows if r['catalog']}
existing=[json.loads(line) for line in editionspath.read_text(encoding='utf8').splitlines() if line.strip()]
new=[]
def add(catalog,translator,year,scope,tier,url,publisher,language='en',evidence='',corroboration='',status='published',confidence='high',source_type='publisher',download_url=''):
 assert catalog in idx,catalog
 assert url.startswith('https://')
 assert tier in ('BUY','BORROW','PRINT','DIRECT','NONE')
 assert not download_url or tier=='DIRECT'
 new.append(dict(catalog=catalog,title=idx[catalog]['title'],translator=translator,year=str(year),scope=scope,
    access_tier=tier,access_mode=tier,download_url=download_url,publisher=publisher,info_url=url,
    corroboration_url=corroboration,language=language,evidence=evidence,publication_status=status,
    verification_status='BIBLIOGRAPHICALLY_VERIFIED' if status=='published' else 'PUBLICATION_FORTHCOMING',
    source_type=source_type,confidence=confidence,researcher=RESEARCHER,verified_at=DATE))

# Official publisher states English translation *of each* of these 20 Yoga Upanisads.
adyar='https://www.ts-adyar.org/book/yoga-upanisad-s-translation'
ntulib='https://dlbs.liberal.ntu.edu.tw/DLMBS/en/search/search_detail.jsp?seq=653963'
yoga={
'M00102':'Advayataraka','M00103':'Amrtabindu','M00104':'Amrtanada',
'M00108':'Ksurika','M00114':'Tejobindu','M00297':'Trisikhibrahmana',
'M00296':'Darsana','M00106':'Dhyanabindu','M00111':'Nadabindu',
'M00112':'Pasupatabrahma','M00105':'Brahmavidya','M00110':'Mandalabrahmana',
'M00109':'Mahavakya','M00300':'Yogakundali','M00299':'Yogacudamani',
'M00302':'Yogatattva','M00301':'Yogasikha','M00298':'Varaha',
'M00113':'Sandilya','M00107':'Hamsa'}
for cat,short in yoga.items():
 add(cat,'T. R. Srinivasa Ayyangar',1938,'full:individual Yoga Upaniṣad in 20-text collection',
     'BUY',adyar,'Adyar Library and Research Centre (Adyar Library Series 20)','en',
     evidence=f"Publisher's twenty-title contents explicitly includes {short} Upanisad, English translation with commentarial guidance; 1938 1st edition confirmed by NTU library; current Adyar stock listing is a later edition.",
     corroboration=ntulib,source_type='publisher_and_library')

# 1914 accessible public-domain edition covering nine Yoga Upanishads + two Vedanta Upanishads.
ayiar='https://original.sacred-texts.com/hin/tmu/index.htm'
contents='https://original.sacred-texts.com/hin/tmu/tmu01.htm'
for cat in ['M00103','M00114','M00113','M00302','M00106','M00107','M00104','M00298','M00110','M00111','M00300']:
 add(cat,'K. Narayanasvami Aiyar',1914,'full:individual Upaniṣad in Thirty Minor Upanishads',
     'PRINT',ayiar,'Vasanṭā Press (Madras), public-domain text mirrored online','en',
     evidence='Book contents explicitly lists the individual translated Upaniṣad; free-to-read HTML online, not a verified direct PDF/ZIP for the strict DIRECT tier.',
     corroboration=contents,source_type='historical_public_domain_edition')

add('M00001','J. A. B. van Buitenen',1971,'full:Āgamaprāmāṇya Sanskrit text and English translation','PRINT',
 'https://rmrl.in/en/onlinecat/62679/yamuna%27s-agama-pramanyam%2C-or%2C-treatise-on-the-validity-of-pancaratra',
 'Rāmānuja Research Society, Madras','en',
 evidence='RMRL library record explicitly says Sanskrit text and English translation, 1971, 297pp.',
 corroboration='https://vishvasa.github.io/rAmAnujIyam/tattvam/yAmunaH/Agama-prAmANyam/buitenen/',source_type='library')
add('M00008','Alex Watson; Dominic Goodall; S. L. P. Anjaneya Sarma',2013,
 'full:Sadyojyotiḥ Paramokṣanirāsakārikā (59 verses) with Rāmakaṇṭha commentary',
 'BUY','https://ifpindia.org/bookstore/ci122/',
 'Institut Français de Pondichéry / École française d’Extrême-Orient','en',
 evidence='Publisher explicitly says critical edition and annotated English translation of 59-verse treatise plus the commentary; Muktabodha reported units 104, requires source census.',
 corroboration='https://www.tantric-studies.uni-hamburg.de/research/publications/paramoksanirasakarikavrtti.html',source_type='publisher')
add('M00158','Jürgen Hanneder',1998,'partial:first kāṇḍa, verses 1–399 only',
 'BUY','https://brill.com/flyer/title/24058?pdfGenerator=headless_chrome&print=pdf',
 'Egbert Forsten (1998); Brill electronic edition (2023)','en',
 evidence='Publisher and GRETIL editorial header identify precisely I.1–399; remaining passages not translated by this edition. Publication originally 1998, PDF reissued 2023.',
 corroboration='https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_abhinavagupta-mAlinIzlokavArttika.htm',source_type='publisher')
add('M00319','Shaman Hatley',2018,'partial:chapters 1,2,39,40,83',
 'BUY','https://www.ifpindia.org/bookstore/ci133/',
 'Institut Français de Pondichéry / EFEO / University of Hamburg','en',
 evidence='IFP publisher explicitly lists five chapters critically edited and translated; volume I.',source_type='publisher')
add('M00319','Csaba Kiss',2015,'partial:chapters 3,21,45',
 'BUY','https://ifpindia.org/bookstore/ci130/',
 'Institut Français de Pondichéry / EFEO / University of Hamburg','en',
 evidence='IFP publisher explicitly lists three chapters edited and translated; volume II, reprinted 2024.',
 corroboration='https://publications.efeo.fr/en/livres/829_the-brahmay-malatantra-or-picumata-vol-2',source_type='publisher')
add('M00319','Shaman Hatley',2026,'partial:chapter 46',
 'PRINT','https://orca.cardiff.ac.uk/id/eprint/184619/1/693aeb3de31ce.pdf',
 'Asian Literature and Translation (article)','en',
 evidence='University-hosted journal paper identifies critical edition and translation of chapter 46; journal publication status to confirm; direct PDF exists but not independently checked for file permissions.',
 source_type='journal',confidence='medium')
add('M00259','P. P. Apte', '1991–2006','full:chapters 1–43 in two volumes',
 'BUY','https://www.exoticindiaart.com/book/details/pauskara-samhita-in-two-volumes-rare-book-sanskrit-text-with-english-translation-idl172/',
 'Rashtriya Sanskrit Vidyapeetha, Tirupati','en',
 evidence='1991 first volume and 2006 second volume through chapter 43 confirmed in National Sanskrit University publication catalog; seller explicitly English translation.',
 corroboration='https://nsktu.ac.in/storage/2023/03/OUR-PUBLICATION-_-18.03.22.pdf',source_type='publisher_and_university')
add('M00010','Rohan A. Dunuwila',1985,'partial:part 1 of Tattvaprakāśikā, with Aghoraśiva commentary',
 'PRINT','https://openlibrary.org/books/OL2691254M/S%CC%81aiva_Siddha%CC%84nta_theology',
 'Motilal Banarsidass','en',
 evidence='Book catalogue explicitly states English translation of first part of Bhoja Tattvaprakāśikā, not full work; title variant Tattvaprakāśa/Tattvaprakāśikā must be checked against Sanskrit.',
 corroboration='https://ci.nii.ac.jp/ncid/BA03819322',source_type='library',confidence='medium')
add('M00010','Pierre-Sylvain Filliozat',1971,'partial or full scope not established: French version of Bhoja Tattvaprakāśa',
 'PRINT','https://digitalcollections.ifpindia.org/s/manuscripts/item/398697',
 'Journal Asiatique, 1971, pp. 247 ff.','fr',
 evidence='IFP manuscript catalog explicitly cites French translation in Journal Asiatique 1971 fascicle II. Translation scope not collated; article: Le Tattvaprakāśa du roi Bhoja et les commentaires.',
 corroboration='https://real-j.mtak.hu/24225/2/316_846_II_2.pdf',source_type='journal',confidence='medium')
add('M00075','S. S. Suryanarayana Sastri',1982,'full:Śaivaparibhāṣā Sanskrit with English translation',
 'PRINT','https://ci.nii.ac.jp/ncid/BA24594606',
 'University of Madras, Madras University Philosophical Series 35','en',
 evidence='Library explicitly identifies translator, 1982, Sanskrit text with English translation; M00075 title Śaivasiddhāntaparibhāṣā vs printed Śaivaparibhāṣā and author match must be reconfirmed.',
 corroboration='https://books.google.com/books?id=9IDXAAAAMAAJ',source_type='library',confidence='medium')
add('M00098','S. Subrahmanya Sastri',1934,'full:Varivasyārahasya including Prakāśa commentary',
 'BUY','https://ts-adyar.org/book/varivasyarahasya-bhaskararaya-makhin',
 'Adyar Library and Research Centre, Adyar Library Series 28','en',
 evidence='Official publisher explicitly describes English translation with author commentary; 1934 first edition verified by 1968 library catalog.',
 corroboration='https://ci.nii.ac.jp/ncid/BA02089177?l=en',source_type='publisher_and_library')
add('M00217','Kapildev Narayan',2015,'full or near-full:five-volume Sanskrit text with Hindi translation; section alignment unverified',
 'BUY','https://chaukhambabooks.co.in/product/Sri-Vidyarnava-Tantram-of-Sri-Vidyaranya-Sanskrit-Text-With-Hindi-Translation-and-Explanation-Set-of-5-Volumes-8XiUa',
 'Chaukhamba Surbharati Prakashan','hi',
 evidence='Publisher lists five volumes, ISBN 9789380326467, 2,209 pp, Sanskrit with Hindi translation; print dates vary across listings (2012/2015/2023), here 2015 publisher product.',
 corroboration='https://www.exoticindiaart.com/book/details/sri-vidyarnava-tantram-of-sri-vidyaranya-sanskrit-text-with-hindi-translation-and-explanation-set-of-5-volumes-nza081/',source_type='publisher')
add('M00034','Mahānaya editorial translator (uncredited)', 'n.d.','substantial online translation of Trivandrum recension; full extent not independently collated',
 'PRINT','https://mahanaya.org/en/scriptures/mahanayaprakasah/',
 'Mahānaya online scripture translation','en',
 evidence='Web page entitled Mahānayaprakāśaḥ, Trivandrum, Anonymous, presents interlinear English gloss/translation through multiple ullāsa-s; counterpart M00033 is Śitikaṇṭha/KSTS and MUST NOT be conflated.',
 corroboration='https://vishvasa.github.io/AgamaH_shaivaH/sampradAyaH/kaulaH_shAktaH/sampradAyaH/uttarAmnAyaH_kAlI-kulam_kramaH/mukta-bodha-mUlam/',
 source_type='online_parallel_text',confidence='medium')
add('M00091','Radheshyam Chaturvedi (Hindi commentary: Jñānavatī)',2004,
 'full:Hindi commentary on 15 chapters, not confirmed literal translation of every Sanskrit verse',
 'PRINT','https://ci.nii.ac.jp/ncid/BA76560312',
 'Chowkhamba Vidyabhawan / Chowkhamba Krishnadas Academy','hi',
 evidence='University catalog: two volumes chapters 1–6 and 7–15, Sanskrit root and Jñānavatī Hindi bhāṣya; handoff explicitly counts vernacular ṭīkā; DO NOT label full direct root translation.',
 corroboration='https://www.sanatanarahasya.com/lineages/tantra-texts/svacchanda-tantra/',source_type='library',confidence='medium')
# Main Yoga Vasiṣṭha root translated, but source files explicitly include Sanskrit Tātparyaprakāśa: no evidence that commentary is rendered.
for cat in ['M00335','M00336','M00337','M00338','M00339','M00345']:
 add(cat,'Vihari-Lala Mitra', '1891–1899',
     'partial:Yoga-Vāsiṣṭha root translated; attached Tātparyaprakāśa commentary NOT translated',
     'PRINT','https://www.wisdomlib.org/hinduism/book/yoga-vasistha-english',
     'Calcutta 1891 original; reprint versions (public domain)','en',
     evidence='Online full English rendering spans Yoga-Vāsiṣṭha root, six books; the specified Muktabodha item additionally has Tātparyaprakāśa commentary which Mitra does not translate. Mark component/recension mismatch; source volume division remains unverified.',
     corroboration='https://www.wisdomlib.org/hinduism/book/yoga-vasistha-english/d/doc117956.html',source_type='historical_public_domain_edition',confidence='medium')

# Forthcoming is evidence, but NOT a positive translation flag until publication verified after scheduled date.
forthcoming={
 'catalog':'M00038','title':idx['M00038']['title'],'translator':'Gavin Flood; Bjarne Wernicke-Olesen',
 'year':'2026-12-21 (scheduled)','scope':'partial:chapters 1–8, publication forthcoming as of 2026-11-11',
 'access_tier':'NONE','access_mode':'NONE','download_url':'','publisher':'Routledge',
 'info_url':'https://www.routledge.com/Tantra-in-Medieval-India-and-Nepal-An-annotated-edition-and-translation-of-The-Teaching-of-the-Lord-of-Immortality-the-Netra-Tantra-Chapters-1-8/Flood-Wernicke-Olesen/p/book/9780367709600',
 'corroboration_url':'https://www.routledge.com/Routledge-Studies-in-Tantric-Traditions/book-series/RSTT',
 'language':'en','evidence':'Publisher and series listing explicitly mark forthcoming; scheduled December 21 2026, after research date. MUST NOT set has_translation TRUE until publication actually released.',
 'publication_status':'forthcoming','verification_status':'PUBLICATION_FORTHCOMING','source_type':'publisher',
 'confidence':'high','researcher':RESEARCHER,'verified_at':DATE}
# Add only unique verifiable edition key; retain historical first-pass records.
def key(d):return (d.get('catalog'),d.get('translator'),d.get('year'),d.get('scope'),d.get('info_url'))
existingkeys={key(d) for d in existing}
new_uniq=[x for x in new if key(x) not in existingkeys]
assert len({key(e) for e in new})==len(new),'Duplicate within v2 proposed additions'
with editionspath.open('a',encoding='utf8') as f:
 for x in new_uniq:
  f.write(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n')
watch_file=P/'forthcoming_watch.jsonl'
watch_records=[json.loads(s) for s in watch_file.read_text(encoding='utf8').splitlines() if s.strip()] if watch_file.exists() else []
if not any(x.get('catalog')==forthcoming['catalog'] and x.get('info_url')==forthcoming['info_url'] for x in watch_records):
 with watch_file.open('a',encoding='utf8') as f: f.write(json.dumps(forthcoming,ensure_ascii=False,sort_keys=True)+'\n')
# Only ever fill positive verified evidence. No FALSE for missing translations.
bycat=collections.defaultdict(list)
for x in existing+new_uniq:
 if x['publication_status']=='published':bycat[x['catalog']].append(x)
newly_enriched=[]
for row in rows:
 cat=row['catalog']; pairs=bycat.get(cat,[])
 if not pairs or row['has_translation']=='TRUE': continue
 # First primary record listed in batch (preferred recent direct publisher listing).
 p=pairs[0]
 row.update(has_translation='TRUE',translator=p['translator'],year=p['year'],
   scope_full_partial_chapters=p['scope'],access_tier=p['access_tier'],
   download_url=p['download_url'],publisher=p['publisher'],info_url=p['info_url'],
   evidence_notes=p['evidence']+' [All additional editions in translation_editions.jsonl]',
   researcher=RESEARCHER,verified_at=DATE)
 newly_enriched.append(cat)
assert len(rows)==499
assert list(rows[0])==columns
with basepath.open('w',encoding='utf-8',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=columns,lineterminator='\n');wr.writeheader();wr.writerows(rows)
# All editions rather than one per work are retained.
all_eds=existing+new_uniq
print(json.dumps({'new_edition_records':len(new_uniq),'newly_verified_works':len(newly_enriched),'new_catalog_ids':newly_enriched,
 'cumulative_positive_rows':sum(x['has_translation']=='TRUE' for x in rows),'cumulative_published_editions':len([x for x in all_eds if x['publication_status']=='published']),'records_total':len(all_eds)},ensure_ascii=False,indent=2))
