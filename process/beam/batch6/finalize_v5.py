#!/usr/bin/env python3
"""Idempotent v5 validation, manifest, and ZIP build from cumulative work data."""
import csv,json,pathlib,hashlib,zipfile,collections,re
P=pathlib.Path(__file__).resolve().parent
ZIP=P.parent/(P.name+'.zip')
cols='catalog,title,author,verses,tier,tw_status,known_T,T_why,has_translation,translator,year,scope_full_partial_chapters,access_tier,download_url,publisher,info_url,evidence_notes,researcher,verified_at'.split(',')
def csvrows(path):
 with path.open(encoding='utf-8-sig',newline='') as f:
  d=csv.DictReader(f);return d.fieldnames,list(d)
def jsonls(path):return [json.loads(s) for s in path.read_text(encoding='utf8').splitlines() if s.strip()]
h,rows=csvrows(P/'burn_research.csv')
h0,original=csvrows(P/'burn_research.source-PR18.csv')
h4,prevrows=csvrows(P/'burn_research.pre-v5.csv')
assert h==h0==h4==cols
assert len(rows)==len(original)==len(prevrows)==499
assert all(tuple(r[k] for k in cols[:8])==tuple(o[k] for k in cols[:8]) for r,o in zip(rows,original))
assert all((r['catalog'],r['title'])==(p['catalog'],p['title']) for r,p in zip(rows,prevrows))
assert all(r['has_translation'] in ('','TRUE') for r in rows)
assert all(not r['download_url'] or r['access_tier']=='DIRECT' for r in rows)
assert all(not r['info_url'] or re.match(r'^https://[^ ]+$',r['info_url']) for r in rows)
assert all(not r['has_translation'] or all(r[k] for k in ('translator','scope_full_partial_chapters','info_url','researcher','verified_at')) for r in rows)
prepos={r['catalog'] for r in prevrows if r['has_translation']=='TRUE'}
assert len(prepos)==113
current={r['catalog']:r for r in rows if r['catalog']}
assert all(current[cid]=={r['catalog']:r for r in prevrows}[cid] for cid in prepos),'Existing 113 work rows were modified'
eds=jsonls(P/'translation_editions.jsonl');before=jsonls(P/'translation_editions.pre-v5.jsonl')
assert len(before)==143
assert eds[:143]==before,'Preexisting 143 edition records modified or reordered'
assert all(e['publication_status']=='published' for e in eds)
assert len({(e['catalog'],e['translator'],e['year'],e['scope'],e['info_url']) for e in eds})==len(eds),'Duplicate editions'
counts=collections.Counter(e['catalog'] for e in eds)
allids={r['catalog'] for r in rows if r['catalog']}
assert all(e['catalog'] in allids for e in eds)
assert all(e['info_url'].startswith('https://') and e['language'] for e in eds)
assert all(not e['download_url'] or e['access_tier']=='DIRECT' for e in eds)
assert all(current[cid]['has_translation']=='TRUE' for cid in counts)
assert all(counts[r['catalog']]>=1 for r in rows if r['has_translation']=='TRUE')
pos={r['catalog'] for r in rows if r['has_translation']=='TRUE'}
newpos=pos-prepos
v5='ChatGPT manual bibliography research, continuation v5'
neweds=[e for e in eds if e['researcher']==v5]
assert len(pos)==126 and len(newpos)==13,(len(pos),len(newpos))
assert len(eds)==168 and len(neweds)==25,(len(eds),len(neweds))
leads=jsonls(P/'manual_leads_and_exceptions.jsonl');watch=jsonls(P/'forthcoming_watch.jsonl')
leadids={e['catalog'] for e in leads}|{e['catalog'] for e in watch}
with (P/'catalog_research_status.csv').open('w',encoding='utf8',newline='') as f:
 fields=['catalog','title','audit_status','has_translation','known_T','documented_edition_count','action_needed'];w=csv.DictWriter(f,fields,lineterminator='\n');w.writeheader()
 for r in rows:
  cid=r['catalog']
  if not cid: st='MISSING_MERGE_KEY';act='Resolve original Muktabodha catalog ID; cannot merge by title'
  elif r['has_translation']=='TRUE':st='VERIFIED_EXISTENCE';act='Compare available translation scope to original Sanskrit recension; collect access rights'
  elif cid in leadids:st='RESEARCH_LEAD_REQUIRES_FOLLOWUP';act='Investigate manuscript and edition identity; translation of exact root not confirmed'
  else:st='NOT_INDIVIDUALLY_RESEARCHED';act='Per-work bibliography research pending, not asserted untranslated'
  w.writerow({'catalog':cid,'title':r['title'],'audit_status':st,'has_translation':r['has_translation'],'known_T':r['known_T'],'documented_edition_count':counts[cid],'action_needed':act})
with (P/'research_continuation_2026-11-11.jsonl').open('w',encoding='utf8') as f:
 for e in eds:
  if 'continuation' in e['researcher'].lower():
   d={k:e[k] for k in ('catalog','title','translator','year','language','scope','info_url','corroboration_url','confidence','researcher')}
   f.write(json.dumps(d,ensure_ascii=False,sort_keys=True)+'\n')
oldreport=json.loads((P/'validation_report.json').read_text(encoding='utf8'))
report=dict(oldreport)
report.update({'previous_v4_work_count':113,'previous_v4_edition_count':143,'individual_works_with_verified_translation':len(pos),'verified_published_edition_records':len(eds),'new_works_in_v5':len(newpos),'new_editions_in_v5':len(neweds),'new_v5_catalog_ids':sorted(newpos),'continuation_v5_new_published_edition_records':len(neweds),'languages_in_edition_records':dict(sorted(collections.Counter(e['language'] for e in eds).items())),'research_lead_or_exception_records':len(leads),'works_with_exception_or_forthcoming_leads':len(leadids&allids),'unresolved_rows':len(rows)-len(pos),'direct_download_links_count':sum(bool(r['download_url']) for r in rows),'previous_113_positive_rows_unchanged':True,'previous_143_edition_records_unchanged':True,'false_translation_flags_created':0})
report['critical_blockers']=[b for b in report.get('critical_blockers',[]) if '386' not in b and '499-work' not in b]+[
 '373 catalog rows remain unresolved, not proved untranslated; this is not a 499-work exhaustive census',
 'One blank catalog ID for Saundaryalaharī still cannot merge by catalog',
 '2022 Bālāviṃśati translation not assigned to Laghustava or commentary: textual crosswalk needed',
 'Assamese-language Kamaratna Tantra 1928 not assumed identical to Muktabodha Sanskrit Kamaratnatantra',
 'Some volumes, duplicate catalog IDs and recensions require chapter and verse alignment',
 'No direct download URLs guessed; public HTML is represented in edition JSONL']
(P/'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
readme=P/'README.md';s=readme.read_text(encoding='utf8')
s=s.replace('## Cumulative continuation summary (2026-11-11, v4)','## Cumulative continuation summary (2026-11-11, v5)')
s=s.replace('**113 of 499 catalog rows**','**126 of 499 catalog rows**').replace('**143 separate published-edition records**','**168 separate published-edition records**').replace('**386 rows remain unresolved**','**373 rows remain unresolved**')
s=s.replace('`continue_v3.py`, and `continue_v4.py`','`continue_v3.py`, `continue_v4.py`, and `continue_v5.py`').replace('`finalize_v4.py` regenerates','`finalize_v5.py` regenerates')
s=s.replace('**143 independently represented published translation records for 113 works**','**168 independently represented published translation records for 126 works**').replace('(113 documented works, 386 unresolved)','(126 documented works, 373 unresolved)')
s=s.replace('## Deliverables','''### Continuation v5 discoveries (new)

- **13 additional catalog IDs**, **25 edition records**, making **126 translation-evidenced catalog rows / 168 edition records**; 373 unverified rows remain.
- Pandey’s *Bhāskarī* vol. 3 is explicitly a translation of Abhinavagupta’s **Īśvarapratyabhijñāvimarśinī** (1954, reissued 1998 and 2021), not merely an English introduction to the Sanskrit commentary.
- Two *Kāmakalāvilāsa* Muktabodha IDs each map to bibliographically proven English translations: Avalon (1922, 1961) and Dvivedī/Mālavīya (2004). They are **duplicate root identifiers, not independent compositions**.
- Utpaladeva’s three *Siddhitrayī* works have a **1989 Hindi translation** by Sūrya Prakāśa Vyāsa, and Lawrence (2009) independently translates **Ajaḍapramātṛsiddhi** plus Harabhaṭṭa’s Vṛtti.
- **Kulacūḍāmaṇi Nigama** (Finn 1986), **Akulavīratantra** (Adi Suyash, Oct 2026), **Ahirbudhnyasaṃhitā ch. 1–7** (Matsubara 1994), **Yoginītantra Hindi** (undated) and **Prabhuliṅgalīlā Marathi** (1903–04) are added with explicit scope and provenance limits.
- Additional editions for Tantrasāra and Tantrāloka recorded separately without changing prior positive catalog entries.
- **Excluded false matches**: *Tantrarājatantra* Sanskrit-only with English introduction; *Kāmaratnatantra* 1928 Assamese version not automatically same as Muktabodha Sanskrit; Bālāviṃśati / Laghustava correspondence pending text collation.
- Preserve the immutable previous-version snapshots `burn_research.pre-v5.csv` and `translation_editions.pre-v5.jsonl` to audit the cumulative changes.

## Deliverables''')
readme.write_text(s,encoding='utf8')
notes=P/'PROCESS_NOTES.md';s=notes.read_text(encoding='utf8')
if '## Cumulative continuation v5' not in s:
 s+='''\n## Cumulative continuation v5 (2026-11-11)\n\n**13 newly documented catalog rows and 25 new translation edition entries**, cumulative **126/499 work rows** and **168 edition records**, with **373 unresolved**. Strong source anchors: CiNii (Pandey 1954/1998, Avalon 1922/1961, Dwivedī/Mālavīya 2004, 1989 Siddhitrayī), Harrassowitz (Finn 1986), Springer/NTU (Lawrence 2009), MLBD publisher (Matsubara's Ahirbudhnya ch.1–7), British Museum (Prabhuliṅgalīlā Marathi), direct author site (Akulavīratantra, 2026), and a weaker bookseller-only Hindi Yoginītantra record.\n\nSeparate published reprints are represented as separate editions, not separate translated Sanskrit works. Two Kāmakalāvilāsa IDs, two Ajadapramātṛsiddhi IDs and two Īśvarasiddhi IDs are duplicate/variant catalog records pending source collation. The 1989 Hindi Siddhitrayī volume maps to three root works, not to a single invented collection ID. Marketplace-only source for Yoginītantra has *medium* confidence and unknown translator responsibility. No public direct PDF URL was invented for Adi Suyash 2026 despite the download-label on the web page. The Bālāviṃśati 2022 scholarly full translation is a lead only because the source Sanskrit witness has not been collated with laghustava / laghustuti root and commentary records. This is proof of translation *existence*, often only partial, not of complete Sanskrit-witness alignment.\n\nThe original 499 rows and all eight metadata columns remain byte-equivalent under CSV parsing. Earlier 113 positive rows and earlier 143 edition records were copied and checked unchanged. No GitHub mutation was performed.\n'''
 notes.write_text(s,encoding='utf8')
files=sorted(x for x in P.iterdir() if x.is_file() and x.name!='FILES_MANIFEST.json')
manifest={'created':'2026-11-11','source_pr':18,'source_head':report.get('source_head_commit'),'cumulative_works_with_translation':len(pos),'edition_records':len(eds),'unresolved':len(rows)-len(pos),'files':[{'name':x.name,'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in files]}
(P/'FILES_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for x in sorted(P.iterdir()):
  if x.is_file():z.write(x,arcname=P.name+'/'+x.name)
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None
 assert set(z.namelist())=={P.name+'/'+p.name for p in P.iterdir() if p.is_file()}
 assert all(hashlib.sha256(z.read(P.name+'/'+x['name'])).hexdigest()==x['sha256'] for x in manifest['files'])
assert len(list(csv.DictReader((P/'catalog_research_status.csv').open())))==499
print(json.dumps({'zip':str(ZIP),'bytes':ZIP.stat().st_size,'works':len(pos),'new_works':len(newpos),'edition_records':len(eds),'new_editions':len(neweds),'unresolved':len(rows)-len(pos),'leads':len(leads),'languages':report['languages_in_edition_records'],'zip_integrity':'PASSED','baseline_preserved':'PASSED','earlier_113_rows_unchanged':'PASSED','earlier_143_editions_unchanged':'PASSED'},ensure_ascii=False,indent=2))
