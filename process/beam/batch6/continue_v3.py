#!/usr/bin/env python3
"""Incremental bibliographical continuation, 2026-11-11; append-only edition records.
Only fills a previously empty work-level translation cell; never overwrites previous
confirmed evidence. Preserves 499-row PR #18 schema and all original metadata.
"""
from __future__ import annotations
import csv,json,pathlib,collections
P=pathlib.Path(__file__).resolve().parent
DATE='2026-11-11'; WHO='ChatGPT bibliography continuation v3 (verified published records)'
with (P/'burn_research.csv').open(encoding='utf8',newline='') as f:
 reader=csv.DictReader(f); headers=reader.fieldnames; rows=list(reader)
idx={r['catalog']:r for r in rows if r['catalog']}
path=P/'translation_editions.jsonl'
eds=[json.loads(s) for s in path.read_text(encoding='utf8').splitlines() if s.strip()]
keys={(x['catalog'],x['translator'],x['year'],x['scope'],x['info_url']) for x in eds}
new=[]
def add(id,tr,year,scope,url,pub,lang='en',ev='',cor='',tier='BUY',source='publisher',confidence='high'):
 assert id in idx,id
 assert url.startswith('https://')
 assert tier in ('BUY','PRINT','BORROW','DIRECT','NONE'),tier
 d=dict(catalog=id,title=idx[id]['title'],translator=tr,year=str(year),scope=scope,access_tier=tier,access_mode=tier,
   download_url='',publisher=pub,info_url=url,corroboration_url=cor,language=lang,evidence=ev,
   publication_status='published',verification_status='BIBLIOGRAPHICALLY_VERIFIED',source_type=source,
   confidence=confidence,researcher=WHO,verified_at=DATE)
 key=(d['catalog'],d['translator'],d['year'],d['scope'],d['info_url'])
 if key not in keys: new.append(d);keys.add(key)

add('M00163','Jaideva Singh',1980,'full:Kṣemarāja Spandanirṇaya commentary on Spandakārikā',
 'https://www.motilalbanarsidass.com/products/spanda-karikas-the-divine-creative-pulsation',
 'Motilal Banarsidass',ev='Publisher explicitly states complete English translation of Kṣemarāja commentary, not merely Spandakārikā; original 1980 edition corroborated by Wellcome.',
 cor='https://wellcomecollection.org/works/manv6j64',source='publisher_and_library')
add('M00163','Jaideva Singh',1991,'full:Spandakārikā with Kṣemarāja Spandanirṇaya commentary, revised SUNY edition',
 'https://books.google.com/books/about/The_Yoga_of_Vibration_and_Divine_Pulsati.html?id=0OV8OOgviHMC',
 'SUNY Press',ev='SUNY edition explicitly identifies translation of both root kārikās and Spandanirṇaya, reissue of Singh translation.',source='library')
add('M00151','Debabrata Sen Sharma',1977,'full:Amṛtānandanātha Ṣaṭtriṃśattattvasandoha with Ānanda Kavi commentary',
 'https://ci.nii.ac.jp/ncid/BA23449124?l=en','B. N. Chakravarty University, Sanskrit Series 3',
 ev='Japanese university union catalog explicit: English translation of text AND commentary, 1977 preface, 43 pages.',source='university_library')
add('M00083','Mark S. G. Dyczkowski',1992,'full:Bhāskara Śivasūtravārttika commentary (with Śivasūtra root)',
 'https://mitpressbookstore.mit.edu/book/9780791412640','SUNY Press',
 ev='Publisher and MARC contained-work listing explicitly identify English Bhāskara Vārttika. Muktabodha author field Vasugupta applies to root and should be corrected separately after checking commentary author.',
 cor='https://libcat.weber.edu/bib/898434',source='publisher_and_university')
add('M00037','Michel Hulin',1980,'partial:vidyā/jñāna + yoga pādas, with Nārāyaṇakaṇṭha and Aghoraśiva commentaries',
 'https://ifpindia.org/bookstore/pifi63/','Institut Français de Pondichéry','fr',
 ev='Publisher explicitly states French translation of vidyāpāda (doctrine) and yogapāda with the commentaries, 1980.',source='publisher')
add('M00037','Hélène Brunner-Lachaux',1985,'partial:kriyā + caryā pādas, with Nārāyaṇakaṇṭha commentary',
 'https://ifpindia.org/bookstore/pifi69/','Institut Français de Pondichéry','fr',
 ev='Publisher explicitly states French translation of ritual and conduct sections; complements Michel Hulin 1980 doctrine+yoga volume. Together cover four pādas; commentary coverage differs.',
 cor='https://catalogue.bnf.fr/ark:/12148/cb34977797r',source='publisher_and_library')
add('M00041','Debabrata Sen Sharma',2007,'full:Abhinavagupta Paramārthasāra + Yogarāja commentary',
 'https://openlibrary.org/works/OL44858284W/Param%C4%81rthas%C4%81ra_of_Abhinavagupta',
 'Muktabodha Indological Research Institute','en',
 ev='Library record explicitly identifies Sanskrit verses, full English translation and Yogarāja commentary in English; same Muktabodha publisher.',source='library')
add('M00041','Lyne Bansat-Boudon; Kamaleshadatta Tripathi',2011,'full:Abhinavagupta Paramārthasāra + Yogarāja commentary, critically revised Sanskrit',
 'https://www.routledge.com/An-Introduction-to-Tantric-Philosophy-The-Paramarthasara-of-Abhinavagupta/Bansat-Boudon-Tripathi/p/book/9780415346696',
 'Routledge','en',ev='Publisher explicitly describes first annotated English translation of root + commentary alongside critical Sanskrit edition.',source='publisher')
add('M00041','Kamalā Dvivedī',1994,'full or selected? scope unverified; Paramārthasāra translated publication',
 'https://books.google.com/books/about/Param%C4%81rthas%C4%81ra.html?id=wR2_zwEACAAJ',
 'Motilal Banarsidass','und',ev='Google Books identifies Kamalā Dvivedī as translator; translation language/scope not specified in this record, do NOT count as English; separately flag for review.',source='library',confidence='low')
add('M00076','Swami Lakshman Joo',2009,'full:Śrī Sāmbapañcāśikā with Kṣemarāja commentary, Hindi bhāṣāṭīkā',
 'https://www.vivaswan.pl/hi/sambapancasika','Īśvara Āśrama Trust, Srinagar','hi',
 ev='Specialist bibliography explicitly names Hindi translation and Kṣemarāja exegesis, 2009; scope of whole hymn inferred from published full-commentary title.',source='specialist_bibliography')
add('M00076','Bettina Bäumer',2006,'partial or full: English translation/study of Sāmbapañcāśikā poem; exact verse range requires checking',
 'https://www.vedamsbooks.com/books/pasyanti_trika_saivism_of_kashmir_themes_and_practices',
 'Tamil Arts Academy, Sahrdaya studies / reprinted in Paśyantī','en',
 ev='Book description explicitly promises translation and study of the hymn. Original 2006 article; no claim of every verse until collated.',
 cor='https://www.vivaswan.pl/hi/sambapancasika',source='bibliography_and_book',confidence='medium')
add('M00260','Premvallabh Tripathi (Hindi Premamakaranda commentary)',1938,
 'full:Stutikusumāñjali root text with Hindi Premamakaranda explanation (not literal verse translation verified)',
 'https://openlibrary.org/books/OL1254759M/The_Stuti_kusumanjali_of_Shri_Jagad-dhar_Bhatta',
 'Sanskrit Book Depot, Benares','hi',
 ev='Open Library explicitly identifies 803-page Hindi commentary to Jagaddhara Stutikusumāñjali; handoff includes vernacular ṭīkā, root verse-by-verse literal scope not checked.',
 cor='https://search.worldcat.org/title/The-Stuti-kusumanjali-of-Shri-Jagad-dhar-Bhatta/oclc/31409766',source='library')
for cat in ('M00244','M00330'):
 add(cat,'Eknath Easwaran',1985,
 'full:Bhagavadgītā standard 18-chapter root text; Muktabodha row unit counts/recension NOT aligned',
 'https://www.easwaran.org/store/the-bhagavad-gita/',
 'Nilgiri Press','en',
 ev='Publisher confirms full English Bhagavad Gita; this catalog ID is another version/unit count and actual Sanskrit recension has not been collated with Easwaran. Treat root-work existence, not exact-edition alignment.',
 cor='https://books.google.com/books/about/The_Bhagavad_Gita.html?id=HW3XAAAAMAAJ',confidence='medium',source='publisher_and_library')
add('M00057','R. Ananthakrishna Sastry',1988,
 'full:Lalitāsahasranāma thousand names + Bhāskararāya commentary',
 'https://www.ts-adyar.org/book/lalitasahasranama-eng-translation',
 'Adyar Library and Research Centre','en',
 ev='Publisher explicitly confirms English translation of Bhāskararāya exegesis; 1988 reprint in university catalog; first print earlier.',
 cor='https://ci.nii.ac.jp/ncid/BA13933470',source='publisher_and_library')
add('M00032','George A. Grierson; Lionel D. Barnett',1920,
 'full:the collected Lallā-vākyāni as edited in 1920, edition-specific selection',
 'https://ci.nii.ac.jp/ncid/BA33750316?l=en','Royal Asiatic Society (Asiatic Society Monographs 17)','en',
 ev='University union catalog identifies Kashmir-language text with English translation, 1920; edition-specific verse count may differ from Muktabodha etext.',
 cor='https://books.google.com/books/about/Lall%C4%81_v%C4%81ky%C4%81ni.html?id=T5AFwAEACAAJ',source='university_library')
add('M00032','Sir Richard Carnac Temple',1924,
 'full or selected:verse English poetic adaptation of Lallāvākyāni; extent requires collation',
 'https://ikashmir.net/lalded2/bibliography.html','Cambridge University Press','en',
 ev='Dedicated contemporary review lists The Word of Lalla the Prophetess (1924), a verse adaptation from Grierson/Barnett edition; needs source count comparison.',
 cor='https://www.cambridge.org/core/journals/journal-of-the-royal-asiatic-society/article/abs/lallavakyani-or-the-sayings-of-lal-ded-by-sirgeorge-grierson-and-drlionel-d-barnett-pp-viii-225/DFAECD13A91118B6694F81C3DB72FED7',source='scholarly_bibliography',confidence='medium')
add('M00211','Mohanbodhinī Hindi commentator (as credited in edition)',2016,
 'full or substantial:Śivadharmottarapurāṇa Sanskrit with Hindi translation and commentary; textual recension needs comparison',
 'https://ci.nii.ac.jp/ncid/BB29732577','Chaukhamba Sanskrit Series Office, Varanasi','hi',
 ev='Japanese university catalog explicitly says Sanskrit with Hindi translation, first 2016 edition, 279 pages; exact Śivadharmottara recension versus M00211 not yet collated.',source='university_library',confidence='medium')

assert len({(e["catalog"],e["translator"],e["year"],e["scope"],e["info_url"]) for e in new}) == len(new)
with path.open('a',encoding='utf8') as f:
 for e in new:f.write(json.dumps(e,ensure_ascii=False,sort_keys=True)+'\n')
bycat=collections.defaultdict(list)
for e in eds+new:
 if e['publication_status']=='published': bycat[e['catalog']].append(e)
ids=[]
for r in rows:
 if r['has_translation']=='TRUE' or not bycat.get(r['catalog']):continue
 # Prioritize the earliest research record as the representative work-level translation.
 e=bycat[r['catalog']][0]
 r.update(has_translation='TRUE',translator=e['translator'],year=e['year'],scope_full_partial_chapters=e['scope'],
    access_tier=e['access_tier'],download_url=e['download_url'],publisher=e['publisher'],info_url=e['info_url'],
    evidence_notes=e['evidence']+' [See translation_editions.jsonl for others and caveats]',researcher=WHO,verified_at=DATE)
 ids.append(r['catalog'])
assert len(rows)==499 and list(rows[0])==headers
with (P/'burn_research.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=headers,lineterminator='\n');w.writeheader();w.writerows(rows)
print(json.dumps({'v3_new_works':len(ids),'v3_catalogs':ids,'v3_added_editions':len(new),'cumulative_positives':sum(r['has_translation']=='TRUE' for r in rows),'cumulative_editions':len(eds)+len(new)},ensure_ascii=False,indent=2))
