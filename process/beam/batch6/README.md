# Muktabodha translation-existence research: PR #18 handoff

Evidence slice dated **2026-11-11**; repo `prx0r/translation-work`, PR #18, head `5b102c18b785e689bdacc949db7cc299d7019e89`.

## Cumulative continuation summary (2026-11-11, v6)

- **144 of 499 catalog rows** now have documented existing translation evidence (up from 35 in first package).
- **196 separate published-edition records** (up from 42), with translation language, scope, publisher, landing URL, corroboration and source caveats.
- **355 rows remain unresolved**. Leave these blank: no comprehensive negative search has been performed.
- The original 499-row / 19-field merge schema is preserved; no baseline metadata was rewritten.
- `continue_v2.py`, `continue_v3.py`, `continue_v4.py`, `continue_v5.py`, and `continue_v6.py` record cumulative additions, and `finalize_v6.py` regenerates this package and validates the current files. The import should still be manually reviewed for work identity and completeness.
- `forthcoming_watch.jsonl` is separate: scheduled books are not falsely counted as published.
- Early high-value discoveries included a 20-Upaniṣad English collection, Kṣemarāja Spandanirṇaya, Bhāskara Śivasūtravārttika, complete English Paramārthasāra with Yogarāja, French coverage of all four Mṛgendra pādas across two editions, and a Hindi commentary to Stutikusumāñjali.

### Continuation v4 discoveries

- **30 new catalog IDs** flagged with published translation evidence, **32 new edition entries**, including sources in English, Hindi, French, and Russian (plus three language-undetermined Agama editions).
- The 84000 Mañjuśrīmūlakalpa translation cites the very three-volume Sanskrit source from which the three Muktabodha IDs arise; those print-volume chapter boundaries still need crosswalks.
- Fremantle's Guhyasamājatantra doctoral thesis: **chapters I–XVII only**, not an automatic translation of Uttaratantra (XVIII), despite its own abstract using "entirety".
- Sources also document Kāmikāgama Pūrvapāda/Uttarapāda English parts, Sarvajñānottara, Gorakṣayogaśāstra Russian, Sanskrit/Sadyojyoti treatises in French, Kaula texts, and the Mātṛkābhedatantra.
- **Not proof of 113 fully translated works**: multiple rows are only excerpt/section translations, and some are duplicate IDs for one root text; `translation_editions.jsonl` carries exact evidence and notes.

### Continuation v5 discoveries (new)

- **13 additional catalog IDs**, **25 edition records**, making **126 translation-evidenced catalog rows / 168 edition records**; 373 unverified rows remain.
- Pandey’s *Bhāskarī* vol. 3 is explicitly a translation of Abhinavagupta’s **Īśvarapratyabhijñāvimarśinī** (1954, reissued 1998 and 2021), not merely an English introduction to the Sanskrit commentary.
- Two *Kāmakalāvilāsa* Muktabodha IDs each map to bibliographically proven English translations: Avalon (1922, 1961) and Dvivedī/Mālavīya (2004). They are **duplicate root identifiers, not independent compositions**.
- Utpaladeva’s three *Siddhitrayī* works have a **1989 Hindi translation** by Sūrya Prakāśa Vyāsa, and Lawrence (2009) independently translates **Ajaḍapramātṛsiddhi** plus Harabhaṭṭa’s Vṛtti.
- **Kulacūḍāmaṇi Nigama** (Finn 1986), **Akulavīratantra** (Adi Suyash, Oct 2026), **Ahirbudhnyasaṃhitā ch. 1–7** (Matsubara 1994), **Yoginītantra Hindi** (undated) and **Prabhuliṅgalīlā Marathi** (1903–04) are added with explicit scope and provenance limits.
- Additional editions for Tantrasāra and Tantrāloka recorded separately without changing prior positive catalog entries.
- **Excluded false matches**: *Tantrarājatantra* Sanskrit-only with English introduction; *Kāmaratnatantra* 1928 Assamese version not automatically same as Muktabodha Sanskrit; Bālāviṃśati / Laghustava correspondence pending text collation.
- Preserve the immutable previous-version snapshots `burn_research.pre-v5.csv` and `translation_editions.pre-v5.jsonl` to audit the cumulative changes.

### Continuation v6 discoveries (new)

- **18 additional catalog records** with independently documented translation existence and **28 further edition records**. Cumulative **144 work records / 196 editions / 355 unresolved**.
- **Śivadharmaśāstra** separately published, annotated English translations of chapters 6 (Bisschop 2018), 11 (Bisschop/Kafle/Lubin 2021), and 10 (Bisschop/Kafle/Kiss 2025, also a commentary translation). These do **not** establish full Śivadharma translation or identity with the distinct Nandiprokta catalog ID.
- **Cidgaganacandrikā**: Agnihotri Śāstrī's **1941 English translation of the first two vimarśas only**, discovered through later specialist commentary review.
- **Laghu-Yoga-Vāsiṣṭha**: K. Narayanaswami Aiyer's **1896/1971 English root translation**. The indexed Muktabodha file includes **Vāsiṣṭhacandrikā commentary not covered by the English translation**.
- Substantial Sanskrit–Hindi translated works: **Śāktapramoda, Dakṣiṇāmūrtisaṃhitā, Kaṅkālamālinītantra, Muṇḍamālātantra part 1 (source-division unresolved), Bṛhannīlatantra, Tārārahasya, Kaulāvalīnirṇaya, Gandharvatantra, Kāmākhyātantra, Kāmadhenutantra, Bṛhattantrasāra, and five-volume Merutantra**.
- **Śaktisaṃgamatantra** three printed khaṇḍas (Kālī/Tārā/Sundarī) each have at least two separate bilingual Hindi-edition series; do not infer that they correspond verse-for-verse to Muktabodha source segments.
- Additional Rādheśyām Chaturvedī five-volume **Tantrāloka Sanskrit–Hindi** edition evidence recorded without overwriting prior Tantrāloka records.
- Preserved snapshot of prior edition in `burn_research.pre-v6.csv` and `translation_editions.pre-v6.jsonl`. Added `continue_v6.py` and `finalize_v6.py` for audit and reproduction. No Github changes made.

## Deliverables

- `burn_research.csv`: **same 19 columns, same 499 rows, same order** as PR #18 input. Preserves all 8 upstream metadata columns exactly. Research additions appear only in existing output columns. Merge on `catalog`.
- `burn_research.source-PR18.csv`: immutable comparison input exported using the same normalized CSV format.
- `translation_editions.jsonl`: **196 independently represented published translation records for 144 works**, including English, Hindi, French, and Italian; this prevents losing multiple editions when squeezing work-level research into one CSV row.
- `catalog_research_status.csv`: all 499 records marked `VERIFIED_EXISTENCE`, `RESEARCH_LEAD_REQUIRES_FOLLOWUP`, `NOT_INDIVIDUALLY_RESEARCHED`, or `MISSING_MERGE_KEY`.
- `manual_leads_and_exceptions.jsonl`: investigated leads that are NOT verified translations of the exact Muktabodha work. The primary CSV leaves `has_translation` blank for those unless a separate verified translation already exists.
- `source_census_warnings.jsonl`: suspicious verse-unit counts and chapter indexing risks.
- `validation_report.json`: counts and structural/claim checks.

## Critical limitations

**This is NOT a completed 499-work exhaustive bibliographic census (144 documented works, 355 unresolved).** It is a verified, safely mergeable research batch plus all untouched rows for the remainder. The user requested all 499; bibliographic verification of every work (including Indian print catalogues, European sources, Shodhganga theses and article translations) was NOT completed in this interaction. The unresolved field values are intentionally blank, NEVER fabricated `FALSE`. `verified_at` for exception-only rows denotes *review of a research lead*, not a comprehensive negative.

- The existing `access_tier` schema lacks `ONLINE_HTML`. Where a fully translated work is freely readable as HTML but there is no verified downloadable file, `access_tier` and `download_url` are blank, `info_url` contains the webpage, and `evidence_notes` explains it. `translation_editions.jsonl` uses `access_mode: ONLINE_HTML`. Do NOT mislabel an HTML page as a PDF/direct download.
- `PRINT` is used where a record of an out-of-print / holding-only publication is verified; `BUY` where active sales/publisher availability are reasonably supported. A marketplace listing is not proof of copyright permission for third-party downloadable scans.
- Translation status `TRUE` denotes corroborated **translation existence**, not a claim that the *entire Muktabodha etext* was covered. See `scope_full_partial_chapters`, `confidence`, `evidence` for exact limits. For works with only root-text translations, commentary coverage must be inspected separately.
- `known_T` and `T_why` left **unchanged** as required for deterministic merge, although they contain known false matches such as Pauṣkara Saṃhitā to Śivasūtravimarśinī and Saṃnyāsa Upaniṣads to Haṭhayogapradīpikā. These are upstream ranker tasks, not safe to silently rewrite inside a research-only CSV.
- One input row, `saundaryalaharī`, has a **blank `catalog` merge key**; fix against Muktabodha first. No fake ID assigned.
- `M00092`/`M00093`: Italian full Tantrāloka (Gnoli), English chapters 1 and 29 separately, French chapters 1–5 separately. Dyczkowski volumes II–XI were listed forthcoming by publisher as of research date. Distinguish complete draft from obtainable published book.
- `M00211` Śivadharmottara translation of chapter 2 by De Simini; do not mark full.
- `M00126` Kriyākramadyotikā *dīkṣāvidhi* thesis translation, not full.
- `M00082` Śivasaṃhitā and `M00632` Dattātreyatantra have implausible upstream 1–2 verse counts; reconfirm source identity before scaling translation worker prioritisation.

## Next-agent merging recipe

1. Confirm branch SHA and take a fresh working copy; avoid replacing newer manual research.
2. Parse `burn_research.csv` with `utf-8`, CSV rules (quote-sensitive), 499 rows expected.
3. Merge by exact `catalog`; quarantine the blank catalog row for manual resolution.
4. For each verified `TRUE` row, map the **separate editions** in `translation_editions.jsonl` into Openpatala `translations`, with `scope`, `language`, `publication_status`, `confidence`, `info_url` and matching canonical work ID.
5. Reconfirm ambiguous work identities/recensions before public exposure; partial translations cannot satisfy a work-level `FULL English` gate.
6. Keep unresolved rows unknown, NOT `FALSE` and NOT counted as untranslated.
7. Re-run source census for 1/2-verse anomalies, particularly major tantric or haṭhayogic works.
8. Keep ongoing publication watch for Netratantra Flood and Tantrāloka II–XI.

## Source hierarchy

Official publishers (IFP/EFEO, MLBD, OUP, Tattva, Adelphi, YogaVidya, Indica), library holdings (Wellcome, Library of Congress, BnF, CiNii), and clearly documented open web translations (Mahānaya) were preferred. All cataloged results and secondary corroboration URLs are recorded. Searches were manual targeted verification, not a claimed all-works automated census.
