# HANDOFF — manual translation research (for ChatGPT with browsing)

*You get: `burn_research.csv` (499 rows) + `RESEARCH-BRIEF.md` (method).
Do the parts below marked NOT CHECKED. Everything marked CHECKED is
done — verify-don't-redo (spot-check 1 in 20 if you doubt it).*

## ✅ CHECKED — do not redo (evidence on file)

| Lane | Coverage | Result location |
|---|---|---|
| OpenLibrary edition search | 492 census + 1,493 openpatala works | `deepfind*.jsonl` → `confirmed` counts |
| archive.org advancedsearch (+DLI) | same | same rows, `archive.org` source |
| Wisdomlib book pages | same | same rows |
| Magee PDFs (shivashakti /texts,/netra,/bibby) | full index scraped | `curated_hits.jsonl` (14 hits) |
| Dyczkowski scripture index (36) | full index scraped | `curated_hits.jsonl` (15 hits) |
| Wallis blog sitemap (349 URLs, VB series) | full sitemap matched | `curated_hits.jsonl` (21 hits) |
| Pradīpaka Trika index (titles) | index read (deep links pending) | FAMOUS estimates in ranker |
| Majors web research | TA (Dyczkowski 11v ✓), IPK (Torella ✓), IPVV (Pandey 1954 ✓), Kularnava (Pandit/Rai ✓), Netra/Svacchanda (Singh partial ✓), Gītā (dozens ✓) | `prioritize_mukta.py` FAMOUS + matrix rows |
| bibliographySeed.ts (58 records) | parsed + 14 verified pairs merged | openpatala `translations` table (43 rows) + matrix |
| Our own translations | audit-complete works flagged | CSV `tw_status` |

## ❌ NOT CHECKED — this is your job

1. **Print catalogs** — Motilal/Indica/SUNY/DK Printworld/Exotic India/
   Vedams backlists for each work (rows with `known_T=0` first).
2. **Hindi layer** — `<title> hindi anuvad OR hindi tika` (counts as translation).
3. **Theses** — Shodhganga + `thesis translation` queries (chapter-level counts).
4. **Journal articles** — JIP/IIJ/JAOS pieces with translations inside.
5. **Non-English European** — German/French/Italian/Russian (beyond the sampled majors).
6. **Oral/living-teacher** — Lakshmanjoo audio/courses, Wallis courses, OCHS seminars (note, don't overclaim).
7. **Forthcoming watch** — Flood Netra, Sanderson TA (FALSE + `in-prep` note).
8. **JS-walled catalogs** — Lakshmanjooacademy books, Viśvāsa mirror, SanskritDocuments (needs your browser).

## 📥 Return

Filled CSV, same columns. Priority: `burn_order` ascending
(`ranked_burn.json` — ask for it if you want the order).
Merge key: `catalog`. Rules: verified-links-only TRUE, partials with
chapters, logged negatives, researcher+date every row.
