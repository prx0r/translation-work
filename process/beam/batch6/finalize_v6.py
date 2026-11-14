#!/usr/bin/env python3
"""Validate all cumulative 499 catalog rows, prior batch preservation, checksum and ZIP archive (v6)."""
import csv, json, pathlib, hashlib, zipfile, collections, re
P=pathlib.Path(__file__).resolve().parent
Z=P.parent/(P.name+'.zip')
cols='catalog,title,author,verses,tier,tw_status,known_T,T_why,has_translation,translator,year,scope_full_partial_chapters,access_tier,download_url,publisher,info_url,evidence_notes,researcher,verified_at'.split(',')
def loadcsv(x):
 with x.open(encoding='utf-8-sig',newline='') as f:d=csv.DictReader(f);return d.fieldnames,list(d)
def loadjsonl(x):return [json.loads(s) for s in x.read_text(encoding='utf8').splitlines() if s.strip()]
h,rows=loadcsv(P/'burn_research.csv')
h0,source=loadcsv(P/'burn_research.source-PR18.csv')
h5,prior=loadcsv(P/'burn_research.pre-v6.csv')
assert h==h0==h5==cols
assert len(rows)==len(source)==len(prior)==499
assert all(tuple(a[k] for k in cols[:8])==tuple(b[k] for k in cols[:8]) for a,b in zip(rows,source)),'Original source metadata overwritten'
assert all((a['catalog'],a['title'])==(b['catalog'],b['title']) for a,b in zip(rows,prior))
assert all(a['has_translation'] in ('','TRUE') for a in rows)
assert all(not a['download_url'] or a['access_tier']=='DIRECT' for a in rows)
assert all(not a['info_url'] or re.match('^https://[^ ]+$',a['info_url']) for a in rows)
assert all(not a['has_translation'] or all(a[k] for k in ('translator','scope_full_partial_chapters','info_url','researcher','verified_at')) for a in rows)
priorrows={r['catalog']:r for r in prior if r['has_translation']=='TRUE'}
assert len(priorrows)==126,len(priorrows)
now={r['catalog']:r for r in rows if r['catalog']}
assert all(now[k]==r for k,r in priorrows.items()),'Older 126 positive catalog rows were modified'
eds=loadjsonl(P/'translation_editions.jsonl')
prev_eds=loadjsonl(P/'translation_editions.pre-v6.jsonl')
assert len(prev_eds)==168,len(prev_eds)
assert eds[:len(prev_eds)]==prev_eds,'Older 168 editions overwritten or reordered'
assert len({(e['catalog'],e['translator'],e['year'],e['scope'],e['info_url']) for e in eds})==len(eds)
assert all(e['publication_status']=='published' and e['info_url'].startswith('https://') and e['language'] for e in eds)
assert all(not e['download_url'] or e['access_tier']=='DIRECT' for e in eds)
assert all(e['catalog'] in now and now[e['catalog']]['has_translation']=='TRUE' for e in eds)
counts=collections.Counter(e['catalog'] for e in eds)
pos={r['catalog'] for r in rows if r['has_translation']=='TRUE'}
assert all(counts[x]>=1 for x in pos)
newpos=pos-set(priorrows)
neweds=[e for e in eds if e['researcher']=='ChatGPT manual bibliography research, continuation v6']
assert len(pos)==144 and len(newpos)==18,(len(pos),len(newpos))
assert len(eds)==196 and len(neweds)==28,(len(eds),len(neweds))
leads=loadjsonl(P/'manual_leads_and_exceptions.jsonl');watch=loadjsonl(P/'forthcoming_watch.jsonl')
lead_ids={e['catalog'] for e in leads}|{e['catalog'] for e in watch}
with (P/'catalog_research_status.csv').open('w',encoding='utf8',newline='') as f:
 fields=['catalog','title','audit_status','has_translation','known_T','documented_edition_count','action_needed']; w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader()
 for r in rows:
  cid=r['catalog']
  if not cid:st='MISSING_MERGE_KEY';act='Fix blank original catalog ID; cannot merge on title alone'
  elif r['has_translation']=='TRUE':st='VERIFIED_EXISTENCE';act='Compare scope, recension and source edition; obtain rights and access if needed'
  elif cid in lead_ids:st='RESEARCH_LEAD_REQUIRES_FOLLOWUP';act='Investigate exact textual identity; not a confirmed translated edition'
  else:st='NOT_INDIVIDUALLY_RESEARCHED';act='Bibliographic research incomplete; not an assertion of no translation'
  w.writerow({'catalog':cid,'title':r['title'],'audit_status':st,'has_translation':r['has_translation'],'known_T':r['known_T'],'documented_edition_count':counts[cid],'action_needed':act})
with (P/'research_continuation_2026-11-11.jsonl').open('w',encoding='utf8') as f:
 for e in eds:
  if 'continuation' in e['researcher'].lower():
   d={k:e[k] for k in ('catalog','title','translator','year','language','scope','info_url','corroboration_url','confidence','researcher')}
   f.write(json.dumps(d,ensure_ascii=False,sort_keys=True)+'\n')
report=json.loads((P/'validation_report.json').read_text(encoding='utf8'))
report.update({'previous_v5_work_count':126,'previous_v5_edition_count':168,'individual_works_with_verified_translation':144,'verified_published_edition_records':196,'new_works_in_v6':18,'new_editions_in_v6':28,'new_v6_catalog_ids':sorted(newpos),'continuation_v6_new_published_edition_records':28,'languages_in_edition_records':dict(sorted(collections.Counter(e['language'] for e in eds).items())),'research_lead_or_exception_records':len(leads),'works_with_exception_or_forthcoming_leads':len(lead_ids&set(now)),'unresolved_rows':355,'direct_download_links_count':sum(bool(r['download_url']) for r in rows),'previous_126_positive_rows_unchanged':True,'previous_168_edition_records_unchanged':True,'false_translation_flags_created':0,'zip_integrity':'PASSED'})
report['critical_blockers']=[s for s in report.get('critical_blockers',[]) if 'catalog rows remain unresolved' not in s]+[
 '355 catalog rows remain unresolved; evidence of non-translation is not established by an empty field',
 'Partial translated Śivadharmaśāstra chapters 6, 10 and 11 do not imply full Śivadharmaśāstra translation or match to M00210',
 '1896 Laghu-Yoga-Vāsiṣṭha translates the Sanskrit root, not Vāsiṣṭhacandrikā commentary',
 'Hindi Śaktisaṃgamatantra multi-volume booksets have not been text-collated with all Muktabodha khanda transcripts',
 'Undated editions retained as n.d.; do not infer year from a nearby edition, barcode, or listing updated date',
 'One untranslated-status source row has blank catalog ID (Saundaryalaharī) and cannot be merged safely',
 'Source verse counts may be incomplete; work-level evidence does not imply complete exact witness coverage']
(P/'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
readme=P/'README.md';s=readme.read_text(encoding='utf8')
s=s.replace('## Cumulative continuation summary (2026-11-11, v5)','## Cumulative continuation summary (2026-11-11, v6)')
s=s.replace('**126 of 499 catalog rows**','**144 of 499 catalog rows**').replace('**168 separate published-edition records**','**196 separate published-edition records**').replace('**373 rows remain unresolved**','**355 rows remain unresolved**')
s=s.replace('and `continue_v5.py` record cumulative additions, and `finalize_v5.py`','`continue_v5.py`, and `continue_v6.py` record cumulative additions, and `finalize_v6.py`')
s=s.replace('**168 independently represented published translation records for 126 works**','**196 independently represented published translation records for 144 works**').replace('(126 documented works, 373 unresolved)','(144 documented works, 355 unresolved)')
if '### Continuation v6 discoveries' not in s:
 s=s.replace('## Deliverables','''### Continuation v6 discoveries (new)

- **18 additional catalog records** with independently documented translation existence and **28 further edition records**. Cumulative **144 work records / 196 editions / 355 unresolved**.
- **Śivadharmaśāstra** separately published, annotated English translations of chapters 6 (Bisschop 2018), 11 (Bisschop/Kafle/Lubin 2021), and 10 (Bisschop/Kafle/Kiss 2025, also a commentary translation). These do **not** establish full Śivadharma translation or identity with the distinct Nandiprokta catalog ID.
- **Cidgaganacandrikā**: Agnihotri Śāstrī's **1941 English translation of the first two vimarśas only**, discovered through later specialist commentary review.
- **Laghu-Yoga-Vāsiṣṭha**: K. Narayanaswami Aiyer's **1896/1971 English root translation**. The indexed Muktabodha file includes **Vāsiṣṭhacandrikā commentary not covered by the English translation**.
- Substantial Sanskrit–Hindi translated works: **Śāktapramoda, Dakṣiṇāmūrtisaṃhitā, Kaṅkālamālinītantra, Muṇḍamālātantra part 1 (source-division unresolved), Bṛhannīlatantra, Tārārahasya, Kaulāvalīnirṇaya, Gandharvatantra, Kāmākhyātantra, Kāmadhenutantra, Bṛhattantrasāra, and five-volume Merutantra**.
- **Śaktisaṃgamatantra** three printed khaṇḍas (Kālī/Tārā/Sundarī) each have at least two separate bilingual Hindi-edition series; do not infer that they correspond verse-for-verse to Muktabodha source segments.
- Additional Rādheśyām Chaturvedī five-volume **Tantrāloka Sanskrit–Hindi** edition evidence recorded without overwriting prior Tantrāloka records.
- Preserved snapshot of prior edition in `burn_research.pre-v6.csv` and `translation_editions.pre-v6.jsonl`. Added `continue_v6.py` and `finalize_v6.py` for audit and reproduction. No Github changes made.

## Deliverables''')
readme.write_text(s,encoding='utf8')
notes=P/'PROCESS_NOTES.md';s=notes.read_text(encoding='utf8')
if '## Cumulative continuation v6' not in s:
 s+='''\n## Cumulative continuation v6 (2026-11-11)\n\n**18 further documented works, 28 editions**, cumulative **144/499 translation-evidenced records and 196 edition records; 355 unresolved**. Source hierarchy this pass: UniorPress (Śivadharma ch.10, ch.11), Brill/BnF/JSTOR (ch.6), university libraries and original dated digital copy (Laghu-Yoga-Vāsiṣṭha root only), a specialist scholarly investigation for Cidgaganacandrikā’s 1941 first-two-vimarśa translation, direct Chaukhamba storefront (Dakṣiṇāmūrti, Kaulāvali, Tārārahasya, Kāmākhya, Kāmadhenutantra) and detailed printed Hindī edition listings (Bṛhattantrasāra, Merutantra, Gandharva, Śāktapramoda, Śaktisaṃgama, etc.).\n\nBookstore descriptions verify translation existence but cannot independently settle Sanskrit witness alignment. In particular Muṇḍamālātantra has two Muktabodha source file parts, with the printed translation section division unresolved; only first part conservatively flagged and second part leads. Tārārahasya root is distinct from its independent commentaries. Śivadharma text is distinct from Śivadharmottara and Nandiprokta witness. The 1896 Laghu Yoga Vasistha root translation does NOT translate the bundled Vāsiṣṭhacandrikā commentary. Some date fields remain n.d. when the source does not specify publication year. Follow-up exceptions are recorded separately rather than inventing untranslated flags. All earlier 126 positive work rows, 168 edition records and 499 original metadata rows were validated unchanged.\n'''
 notes.write_text(s,encoding='utf8')
flist=sorted(x for x in P.iterdir() if x.is_file() and x.name!='FILES_MANIFEST.json')
manifest={'created':'2026-11-11','source_pr':18,'source_head':report['source_head_commit'],'cumulative_works_with_translation':len(pos),'edition_records':len(eds),'unresolved':499-len(pos),'files':[{'name':x.name,'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in flist]}
(P/'FILES_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
with zipfile.ZipFile(Z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(P.iterdir()):
  if p.is_file():z.write(p,arcname=P.name+'/'+p.name)
with zipfile.ZipFile(Z) as z:
 assert z.testzip() is None
 assert set(z.namelist())=={P.name+'/'+p.name for p in P.iterdir() if p.is_file()}
 assert all(hashlib.sha256(z.read(P.name+'/'+x['name'])).hexdigest()==x['sha256'] for x in manifest['files'])
assert len(list(csv.DictReader((P/'catalog_research_status.csv').open(encoding='utf8'))))==499
print(json.dumps({'zip':str(Z),'zip_bytes':Z.stat().st_size,'rows':len(rows),'works_with_translation_evidence':len(pos),'new_works':len(newpos),'edition_records':len(eds),'new_editions':len(neweds),'unresolved':499-len(pos),'manual_leads':len(leads),'languages':report['languages_in_edition_records'],'zip_integrity':'PASSED','source_metadata_unchanged':'PASSED','previous_126_rows_unchanged':'PASSED','previous_168_editions_unchanged':'PASSED'},ensure_ascii=False,indent=2))
