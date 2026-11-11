#!/usr/bin/env python3
"""Regenerate cumulative PR18 audit/status/manifest/ZIP from the existing 499-row CSV.
Safe to re-run: source CSV and translation editions are not rewritten. Validate all
structural invariants before packaging. No network requests and no GitHub writes.
"""
from __future__ import annotations
import csv,json,pathlib,collections,hashlib,zipfile,re
P=pathlib.Path(__file__).resolve().parent
ZIP=P.parent/(P.name+'.zip')
headers=['catalog','title','author','verses','tier','tw_status','known_T','T_why','has_translation','translator','year','scope_full_partial_chapters','access_tier','download_url','publisher','info_url','evidence_notes','researcher','verified_at']
meta_cols=headers[:8]
def csvrows(path):
 with path.open(encoding='utf-8-sig',newline='') as f:
  d=csv.DictReader(f);cols=list(d.fieldnames);rows=list(d)
 return cols,rows
h,rows=csvrows(P/'burn_research.csv')
h0,source=csvrows(P/'burn_research.source-PR18.csv')
assert h==h0==headers,(h,h0)
assert len(rows)==len(source)==499,(len(rows),len(source))
assert all([r[k] for k in meta_cols]==[s[k] for k in meta_cols] for r,s in zip(rows,source))
assert all(r['has_translation'] in ('TRUE','') for r in rows)
assert all(not r['download_url'] or r['access_tier']=='DIRECT' for r in rows)
assert all((not r['info_url']) or re.match(r'^https://[^\s]+$',r['info_url']) for r in rows)
assert all((not r['has_translation']) or (r['translator'] and r['scope_full_partial_chapters'] and r['info_url'] and r['researcher'] and r['verified_at']) for r in rows)
eds=[json.loads(x) for x in (P/'translation_editions.jsonl').read_text(encoding='utf8').splitlines() if x.strip()]
assert all(e['publication_status']=='published' for e in eds)
assert len({(x['catalog'],x['translator'],x['year'],x['scope'],x['info_url']) for x in eds})==len(eds)
allids={r['catalog'] for r in rows if r['catalog']}
assert all(e['catalog'] in allids for e in eds)
bycat=collections.Counter(e['catalog'] for e in eds)
positives=[r for r in rows if r['has_translation']=='TRUE']
assert all(bycat[r['catalog']]>=1 for r in positives)
assert all(r['has_translation']=='TRUE' for r in rows if bycat[r['catalog']])

leads_path=P/'manual_leads_and_exceptions.jsonl'
leads=[json.loads(s) for s in leads_path.read_text(encoding='utf8').splitlines() if s.strip()]
newleads=[
 ('M00014','STUDY_NOT_TRANSLATION','S. Mahalakshmi Cidgaganacandrikā study discusses Sanskrit but is not an attested direct translation.', ['https://www.wisdomlib.org/hinduism/book/cidgaganacandrika-study']),
 ('M00122','ENGLISH_INTRO_ONLY','Publisher Tantrarāja Tantra retail text is in Sanskrit with English introduction; does not establish English translation of the tantra.', ['https://www.motilalbanarsidass.com/collections/tantra/products/tantraraja-tantra']),
 ('M00233','CATALOG_CONFLICT','Īśānaśivagurudevapaddhati bookseller claims English translation, while OpenLibrary lists Sanskrit with English introduction. Do not set TRUE without direct inspection.', ['https://openlibrary.org/books/OL13175874M/Isanasivagurudevapaddhati_of_Isanasivagurudeva_-_2_Vols.']),
 ('M00211','RECENSION_COLLATION_REQUIRED','2016 Hindi Śivadharmottarapurāṇa edition recorded separately; manuscript/printed root recension must be compared to M00211.', ['https://ci.nii.ac.jp/ncid/BB29732577']),
 ('M00330','EDITION_UNIT_COLLATION_REQUIRED','Bhagavad Gītā source is 1168 units, not the usual approximately 700 verses; confirming English root translation does not validate text-alignment completeness.', ['https://www.easwaran.org/store/the-bhagavad-gita/']),
 ('M00244','EDITION_UNIT_COLLATION_REQUIRED','Bhagavad Gītā source row is 341 units, not the usual approximately 700 verses; may be composite/partial, check source before canonical matching.', ['https://www.easwaran.org/store/the-bhagavad-gita/']),
 ('M00163','AUTHOR_METADATA_MISMATCH','Spandanirṇaya is Kṣemarāja commentary, but PR #18 author field attributes Kallaṭa, author of root kārikā; correction belongs to identity layer.', ['https://www.motilalbanarsidass.com/products/spanda-karikas-the-divine-creative-pulsation']),
 ('M00041','LANGUAGE_NOT_CONFIRMED','The 1994 Kamalā Dvivedī Paramārthasāra Google Books record does not explicitly state English language. Its edition record is conservative low confidence and must not be used as an English count.', ['https://books.google.com/books/about/Param%C4%81rthas%C4%81ra.html?id=wR2_zwEACAAJ']),
 ('M00123','SELECTED_VERSE_NOT_GLOBAL_TRANSLATION','Wisdomlib verse pages refer to Harshananda translation in The Pāñcarātra Āgamas: An Introduction. No verified full Jayākhyasaṃhitā coverage; remains unknown.', ['https://www.wisdomlib.org/hinduism/book/jayakhya-samhita-sanskrit/d/doc1059191.html']),
 ('M00319','ARTICLE_PDF_PERMISSION_UNCHECKED','2026 Brahmayāmala ch.46 scholarly PDF is a lead; no unverified direct download_url inserted, article year and copyright to reconfirm.', ['https://orca.cardiff.ac.uk/id/eprint/184619/1/693aeb3de31ce.pdf'])]
existingkeys={(x.get('catalog'),x.get('status')) for x in leads}
for cid,status,note,urls in newleads:
 if (cid,status) not in existingkeys:
  leads.append(dict(catalog=cid,title=next((r['title'] for r in rows if r['catalog']==cid),''),status=status,note=note,links=urls))
with leads_path.open('w',encoding='utf8') as f:
 for x in leads: f.write(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n')
leadids={x['catalog'] for x in leads}
watch=[json.loads(x) for x in (P/'forthcoming_watch.jsonl').read_text(encoding='utf8').splitlines() if x.strip()]
for x in watch:leadids.add(x['catalog'])

statusfile=P/'catalog_research_status.csv'
with statusfile.open('w',encoding='utf8',newline='') as f:
 cols=['catalog','title','audit_status','has_translation','known_T','documented_edition_count','action_needed']
 w=csv.DictWriter(f,fieldnames=cols,lineterminator='\n');w.writeheader()
 for r in rows:
  cid=r['catalog'];positive=r['has_translation']=='TRUE';n=bycat[cid]
  if not cid: st='MISSING_MERGE_KEY';nextstep='Resolve original catalog ID against Muktabodha; do not merge by title'
  elif positive: st='VERIFIED_EXISTENCE'; nextstep='Review exact edition, scope, recension; import all linked edition records'
  elif cid in leadids: st='RESEARCH_LEAD_REQUIRES_FOLLOWUP';nextstep='Review exceptions/forthcoming watch; no verified existing translation established'
  else: st='NOT_INDIVIDUALLY_RESEARCHED';nextstep='Manual per-work bibliography search pending; no absence claim'
  w.writerow(dict(catalog=cid,title=r['title'],audit_status=st,has_translation=r['has_translation'],known_T=r['known_T'],documented_edition_count=n,action_needed=nextstep))

langs=dict(sorted(collections.Counter(e['language'] for e in eds).items()))
first_pass=42
v2_added=sum(e['researcher']=='ChatGPT manual bibliography research, continuation v2' for e in eds)
v3_added=sum(e['researcher']=='ChatGPT bibliography continuation v3 (verified published records)' for e in eds)
assert first_pass+v2_added+v3_added==len(eds)
report=dict(source_repo='https://github.com/prx0r/translation-work/pull/18',source_branch='burn/muktabodha',source_head_commit='5b102c18b785e689bdacc949db7cc299d7019e89',date='2026-11-11',original_catalog_rows=499,final_catalog_rows=len(rows),original_headers=headers,final_headers=h,all_baseline_columns_unchanged=True,row_order_preserved=True,
 individual_works_with_verified_translation=len(positives),verified_published_edition_records=len(eds),
 previous_batch_works=35,previous_batch_edition_records=first_pass,
 continuation_v2_new_published_edition_records=v2_added,continuation_v3_new_published_edition_records=v3_added,
 new_work_records_since_first_package=len(positives)-35,
 languages_in_edition_records=langs,research_lead_or_exception_records=len(leads),
 works_with_exception_or_forthcoming_leads=len({r['catalog'] for r in rows if r['catalog'] in leadids}),
 unresolved_rows=sum(r['has_translation']!='TRUE' for r in rows),blank_catalog_ids=[r['title'] for r in rows if not r['catalog']],false_translation_flags_created=0,
 direct_download_links_count=sum(bool(r['download_url']) for r in rows),
 evidence_model='TRANSLATION_EXISTENCE is not FULL translated corpus alignment; note scope and confidence',
 download_url_rule='Only verified direct author/publisher/institution files; avoid third-party potentially copyrighted scans',
 critical_blockers=['One blank original catalog ID (saundaryalaharī) cannot merge by catalog','Upstream verse counts include block counts and source-recension ambiguities','Known_T/T_why original fields are unmodified and can be false positives','416 unresolved records remain; no absence assertions','No 499-work exhaustive survey completed.'])
(P/'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

readme=P/'README.md'
s=readme.read_text(encoding='utf8')
s=s.replace('**42 independently represented published translation records for 35 works**','**111 independently represented published translation records for 83 works**')
s=s.replace('**This is NOT a completed 499-work exhaustive bibliographic census.**','**This is NOT a completed 499-work exhaustive bibliographic census (83 verified works, 416 unresolved).**')
intro='''## Cumulative continuation summary (2026-11-11, v3)\n\n- **83 of 499 catalog rows** now have documented existing translation evidence (up from 35 in first package).\n- **111 separate published-edition records** (up from 42), with translation language, scope, publisher, landing URL, corroboration and source caveats.\n- **416 rows remain unresolved**. Leave these blank: no comprehensive negative search has been performed.\n- The original 499-row / 19-field merge schema is preserved; no baseline metadata was rewritten.\n- `continue_v2.py` and `continue_v3.py` record cumulative additions, and `finalize_cumulative.py` regenerates this package and validates the current files. The import should still be manually reviewed for work identity and completeness.\n- `forthcoming_watch.jsonl` is separate: scheduled books are not falsely counted as published.\n- New high-value discoveries include a 20-Upaniṣad English collection, Kṣemarāja Spandanirṇaya, Bhāskara Śivasūtravārttika, complete English Paramārthasāra with Yogarāja, French coverage of all four Mṛgendra pādas across two editions, and a Hindi commentary to Stutikusumāñjali.\n\n'''
if '## Cumulative continuation summary' not in s:
 s=s.replace('## Deliverables',intro+'## Deliverables')
readme.write_text(s,encoding='utf8')

notes=P/'PROCESS_NOTES.md';s=notes.read_text(encoding='utf8')
more='''\n## Cumulative continuation v2 and v3 (2026-11-11)\n\n**V2:** 51 new edition records / 37 new catalog IDs. Major corpus clusters: Adyar's 20 Yoga Upaniṣads in a single publisher-declared English translation; additional historical K. Narayanasvami Aiyar versions of 11; Āgamaprāmāṇya; Sadyojyoti Paramokṣanirāsakārikā; Brahmayāmala published English selected chapters (Hatley, Kiss); Pauṣkarasaṃhitā; Śrīvidyārṇava Hindi; Mālinīvijayavārttika I.1–399; root-only Yoga-Vāsiṣṭha; Śivāgrayogin and Mahānaya. All URLs retained per edition.\n\n**V3:** 18 new edition records / 11 new catalog IDs. Publisher/library corroboration: complete Kṣemarāja Spandanirṇaya (Jaideva Singh, 1980); Ṣaṭtriṃśattattvasandoha (Debabrata Sen Sharma, 1977); Bhāskara Śivasūtravārttika (Dyczkowski 1992); Mṛgendrāgama French vidyā/yoga (Hulin 1980) and kriyā/caryā (Brunner-Lachaux 1985); Paramārthasāra including Yogarāja commentary (Sen Sharma 2007, Routledge 2011); Sāmbapañcāśikā Hindi bhāṣāṭīkā; Stutikusumāñjali Hindi exegesis; Bhagavad Gītā two additional Muktabodha IDs, source unit alignment unresolved; Lalitāsahasranāma and Bhāskararāya; Lallāvākyāni 1920.\n\n**Conservative exceptions:** Do not equate commentary or root-only translation with a complete edition; some retailer listings show English introductions, not translations (Tantrarājatantra, Īśānaśivagurudevapaddhati). All edition links are informational; direct downloadable files remain blank unless verified with rights. The Netra Tantra Flood/Wernicke-Olesen projected 2026-12-21 publication is `forthcoming_watch.jsonl` only.\n\nNo comprehensive individual bibliographic search for all 499 completed. Current **unresolved = 416**. `known_T` upstream columns remain untouched.\n'''
if '## Cumulative continuation v2 and v3' not in s:s+=more
notes.write_text(s,encoding='utf8')

batch=(P/'research_continuation_2026-11-11.jsonl')
with batch.open('w',encoding='utf8') as f:
 for e in eds:
  if e['researcher'] in ('ChatGPT manual bibliography research, continuation v2','ChatGPT bibliography continuation v3 (verified published records)'):
   f.write(json.dumps({'catalog':e['catalog'],'title':e['title'],'translator':e['translator'],'scope':e['scope'],'info_url':e['info_url'],'corroboration_url':e['corroboration_url'],'confidence':e['confidence'],'researcher':e['researcher']},ensure_ascii=False,sort_keys=True)+'\n')

# Verify all outputs then manifest; manifest hashes all other contents.
files=sorted(x for x in P.iterdir() if x.is_file() and x.name!='FILES_MANIFEST.json')
manifest={'created':'2026-11-11','source_pr':18,'source_head':report['source_head_commit'],'cumulative_works_with_translation':len(positives),'edition_records':len(eds),
 'files':[{'name':x.name,'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in files]}
(P/'FILES_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for x in sorted(P.iterdir()):
  if x.is_file():z.write(x,arcname=P.name+'/'+x.name)
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(list(P.iterdir()))
 assert z.read(P.name+'/burn_research.csv')==(P/'burn_research.csv').read_bytes()
print(json.dumps({'zip_path':str(ZIP),'zip_bytes':ZIP.stat().st_size,'rows':len(rows),'positives':len(positives),'edition_records':len(eds),'new_works':len(positives)-35,'unresolved':len(rows)-len(positives),'leads':len(leads),'languages':langs,'all_validation_pass':True},ensure_ascii=False,indent=2))
