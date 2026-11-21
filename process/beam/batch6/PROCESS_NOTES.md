# Search and method notes

Research date: 2026-11-11. PR #18 instructions reviewed (`HANDOFF-CHATGPT.md`, `RESEARCH-BRIEF.md`, `MANUAL-SEARCH.md`, `NEXT-PLAN.md`).

## Lanes actually investigated

- First-party publisher catalogues: Motilal Banarsidass, Indica Books, Institut français de Pondichéry/EFEO, Tattva Heritage, Routledge (forthcoming), Adelphi, Oxford University Press, YogaVidya.com, De Gruyter/Brill (Lakṣmītantra), Sri Satguru (Śāradātilaka).
- Bibliographic institutions: Wellcome, Library of Congress, Bibliothèque nationale de France, CiNii, University of California thesis catalogues, JSTOR/SUNY, Google Books, NDLI/IGNCA.
- Hindi translation test: Dattātreyatantra, 1995 Rañjana/Rudradeva Tripāṭhī, corroborated by Wellcome.
- PhD thesis test: Wayne Surdam (1984), annotated Dīkṣāvidhi from Kriyākramadyotikā.
- Italian test: Gnoli (1972, revised 1999) Tantrāloka; French test: Silburn/Padoux (1998) chapters 1–5 and Padoux (1994) Yoginīhṛdaya.
- Online HTML fulltexts: Mahānaya Mahārthamañjarī, Vātūlanāthasūtrāṇi, Bodhapañcadaśikā, Bhairavastava; public-domain Mahānirvāṇatantra and Nāṭyaśāstra root translation.
- Forthcoming watch: Dyczkowski Tantrāloka Volumes II–XI; Netratantra Flood/Wernicke-Olesen.

## Lanes NOT completed globally

Even translated works with duplicated IDs (Lakṣmītantra) require source recensional matching; Shodhganga across all 499; Hindi per-work queries across all 499; exhaustive 2026 publishers' backlists; German/Russian across each work; journal articles with individual verse or chapter translation; oral/teacher recordings and paywalled courses; JS-walled catalogs; confirmation of all source-versification and manuscript variants. No automated full enumeration claims.

## Negative evidence rule

Zero rows marked `FALSE` in this batch. Negative search results require per-work evidence of enough distinct searched sources; absence of a search result or a short etext does not prove no translation. All unprocessed rows are intentionally unknown.

## Transcription and scope errors detected

- Mālinīvijayottaratantra (Vasudeva) publisher scope 1–4, 7, 12–17 differs from secondary indexes claiming 7–11 and 11–17. Prefer first-party publisher, flag for collation.
- Tantrāloka source row '15 thru 38' conflicts with conventional 37 āhnikas; do not overwrite source count blindly.
- M00330 Bhagavadgītā may contain particular commentary; canonical Bhagavadgītā translation cannot automatically validate whole item.
- M00261 ṣaṭcakranirṇaya ≠ ṣaṭcakranirūpaṇa without independent match.
- M00667 Śivasūtravṛtti ≠ Kṣemarāja Vimarśinī automatically; keep unverified.
- `saundaryalaharī` has blank catalog; requires repair from source owner.

## Reproducibility

Source URLs are in `translation_editions.jsonl` and `manual_leads_and_exceptions.jsonl`. Rows newly enriched are the ones with `has_translation=TRUE`. This pack is traceable against the normalized source CSV. External link persistence and paywall availability can change after research date.

## Cumulative continuation v2 and v3 (2026-11-11)

**V2:** 51 new edition records / 37 new catalog IDs. Major corpus clusters: Adyar's 20 Yoga Upaniṣads in a single publisher-declared English translation; additional historical K. Narayanasvami Aiyar versions of 11; Āgamaprāmāṇya; Sadyojyoti Paramokṣanirāsakārikā; Brahmayāmala published English selected chapters (Hatley, Kiss); Pauṣkarasaṃhitā; Śrīvidyārṇava Hindi; Mālinīvijayavārttika I.1–399; root-only Yoga-Vāsiṣṭha; Śivāgrayogin and Mahānaya. All URLs retained per edition.

**V3:** 18 new edition records / 11 new catalog IDs. Publisher/library corroboration: complete Kṣemarāja Spandanirṇaya (Jaideva Singh, 1980); Ṣaṭtriṃśattattvasandoha (Debabrata Sen Sharma, 1977); Bhāskara Śivasūtravārttika (Dyczkowski 1992); Mṛgendrāgama French vidyā/yoga (Hulin 1980) and kriyā/caryā (Brunner-Lachaux 1985); Paramārthasāra including Yogarāja commentary (Sen Sharma 2007, Routledge 2011); Sāmbapañcāśikā Hindi bhāṣāṭīkā; Stutikusumāñjali Hindi exegesis; Bhagavad Gītā two additional Muktabodha IDs, source unit alignment unresolved; Lalitāsahasranāma and Bhāskararāya; Lallāvākyāni 1920.

**Conservative exceptions:** Do not equate commentary or root-only translation with a complete edition; some retailer listings show English introductions, not translations (Tantrarājatantra, Īśānaśivagurudevapaddhati). All edition links are informational; direct downloadable files remain blank unless verified with rights. The Netra Tantra Flood/Wernicke-Olesen projected 2026-12-21 publication is `forthcoming_watch.jsonl` only.

No comprehensive individual bibliographic search for all 499 completed. Current **unresolved = 416**. `known_T` upstream columns remain untouched.

## Cumulative continuation v4 (2026-11-11)

**30 newly documented catalog rows and 32 new bibliographic edition records**, cumulative 113/499 work rows, 143 edition records, 386 unresolved. Clusters: Buddhist tantras (Mañjuśrīmūlakalpa three source volumes; Guhyasamājatantra 1–17); Hindi and English published Śaiva āgama portions; 1980s–1990s French translations of Sadyojyoti treatises; Karpūrādistotra 1922 and 2012 English; 2026 Vijñānabhairava with Ānandabhaṭṭa commentary; Yogacintāmaṇi āsanas only; Russian Gorakṣayogaśāstra; 2011 Mātṛkābhedatantra.

**Counterexamples excluded:** Nareśvaraparīkṣāprakāśa excerpts are not proof that root Nareśvaraparīkṣā was directly translated; Sādhanamālā selected sādhana translation cannot be projected onto both printed volumes; Ratnatrayaparīkṣā commentary excerpt not proof of full root; no negative claims. Language 'und' for three Agama records pending source language verification; edition labels are deliberately conservative. The publisher-specific URL and bibliographic corroboration for each is preserved in JSONL, and all 83 pre-existing positive CSV rows match the previous package byte-for-byte after CSV parsing.

No GitHub write or background task. The same 499-row, 19-column PR #18 CSV is used.

## Cumulative continuation v5 (2026-11-11)

**13 newly documented catalog rows and 25 new translation edition entries**, cumulative **126/499 work rows** and **168 edition records**, with **373 unresolved**. Strong source anchors: CiNii (Pandey 1954/1998, Avalon 1922/1961, Dwivedī/Mālavīya 2004, 1989 Siddhitrayī), Harrassowitz (Finn 1986), Springer/NTU (Lawrence 2009), MLBD publisher (Matsubara's Ahirbudhnya ch.1–7), British Museum (Prabhuliṅgalīlā Marathi), direct author site (Akulavīratantra, 2026), and a weaker bookseller-only Hindi Yoginītantra record.

Separate published reprints are represented as separate editions, not separate translated Sanskrit works. Two Kāmakalāvilāsa IDs, two Ajadapramātṛsiddhi IDs and two Īśvarasiddhi IDs are duplicate/variant catalog records pending source collation. The 1989 Hindi Siddhitrayī volume maps to three root works, not to a single invented collection ID. Marketplace-only source for Yoginītantra has *medium* confidence and unknown translator responsibility. No public direct PDF URL was invented for Adi Suyash 2026 despite the download-label on the web page. The Bālāviṃśati 2022 scholarly full translation is a lead only because the source Sanskrit witness has not been collated with laghustava / laghustuti root and commentary records. This is proof of translation *existence*, often only partial, not of complete Sanskrit-witness alignment.

The original 499 rows and all eight metadata columns remain byte-equivalent under CSV parsing. Earlier 113 positive rows and earlier 143 edition records were copied and checked unchanged. No GitHub mutation was performed.

## Cumulative continuation v6 (2026-11-11)

**18 further documented works, 28 editions**, cumulative **144/499 translation-evidenced records and 196 edition records; 355 unresolved**. Source hierarchy this pass: UniorPress (Śivadharma ch.10, ch.11), Brill/BnF/JSTOR (ch.6), university libraries and original dated digital copy (Laghu-Yoga-Vāsiṣṭha root only), a specialist scholarly investigation for Cidgaganacandrikā’s 1941 first-two-vimarśa translation, direct Chaukhamba storefront (Dakṣiṇāmūrti, Kaulāvali, Tārārahasya, Kāmākhya, Kāmadhenutantra) and detailed printed Hindī edition listings (Bṛhattantrasāra, Merutantra, Gandharva, Śāktapramoda, Śaktisaṃgama, etc.).

Bookstore descriptions verify translation existence but cannot independently settle Sanskrit witness alignment. In particular Muṇḍamālātantra has two Muktabodha source file parts, with the printed translation section division unresolved; only first part conservatively flagged and second part leads. Tārārahasya root is distinct from its independent commentaries. Śivadharma text is distinct from Śivadharmottara and Nandiprokta witness. The 1896 Laghu Yoga Vasistha root translation does NOT translate the bundled Vāsiṣṭhacandrikā commentary. Some date fields remain n.d. when the source does not specify publication year. Follow-up exceptions are recorded separately rather than inventing untranslated flags. All earlier 126 positive work rows, 168 edition records and 499 original metadata rows were validated unchanged.
