# RESEARCH BRIEF — translation-existence research for 499 Muktabodha works

*Give this file + `burn_research.csv` to the researcher (ChatGPT with
browsing, or a human). It explains what we want, what we already have,
the method, and the exact output format.*

## 1. What we are looking for (per work, one row each)

For each of the 499 Sanskrit texts: **every existing translation** —
WHO translated it, WHEN, WHAT scope, and HOW to get it:

| Column | Fill with |
|---|---|
| `has_translation` | TRUE/FALSE (FALSE needs evidence of searching, not guessing) |
| `translator` | Name(s), e.g. "Dyczkowski", "Pandit", "Singh" |
| `year` | Publication year (or "in progress" + expected) |
| `scope_full_partial_chapters` | `full` / `partial:ch1-4` / `selected` / `oral-teachings` |
| `access_tier` | **DIRECT > BORROW > BUY > PRINT > NONE** (see §2) |
| `download_url` | Direct file link if DIRECT (PDF/zip, test it loads) |
| `publisher` | Who sells/publishes it if BUY (Motilal, SUNY, Indica, Routledge…) |
| `info_url` | Landing/catalog page if no download (publisher page, WorldCat, archive.org item) |
| `evidence_notes` | One line: what you checked + what you found |

## 2. Access tiers (the format question, answered)

- **DIRECT** — open file: `download_url` filled (archive.org download,
  author PDF, open-access publisher). This is the prize.
- **BORROW** — archive.org lending / Open Library borrowable:
  `info_url` = item page, note `borrowable` in evidence.
- **BUY** — in print, no open copy: `publisher` + `info_url` (publisher
  page or Vedams/Exotic India listing). No pirated links, ever.
- **PRINT** — exists but unbuyable/unscanned: full citation in
  `evidence_notes`, no link required.
- **NONE** — searched and found nothing (list the layers checked).

Language scope: English first, then Hindi (ṭīkā/anuvāda counts),
then German/French/Italian. Sanskrit commentaries are NOT translations
(note them separately in evidence_notes, don't mark TRUE for them).

## 3. What openpatala already has (so you don't redo it)

- **Identity layer (done):** all 499 ingested — Postgres
  `dbname=openpatala` tables `works` (ids `mukta-Mxxxxx`), `editions`,
  `etexts`, `passages` growing per onboarded work. Query:
  `psycopg2.connect(dbname='openpatala',user='patala',password='patala',
  host='127.0.0.1')`. MCP: `openpatala__resolve/search/get_bundle`
  (server at `/root/openpatala/patala/mcp_server.py`, 5 tools).
- **Machine-found evidence (done, in the CSV's `known_T`/`T_why`):**
  OpenLibrary + archive.org + Wisdomlib hits for all 499; curated
  index scrapes (Magee PDFs, Dyczkowski 36, Wallis VB series,
  Pradīpaka titles); web research on majors (Dyczkowski 11-vol TA,
  Torella, Pandey 1954, Singh selected-vol, OCHS pipeline).
  Rows with `known_T > 0` already have leads — verify and expand,
  don't start from zero.
- **Our own translations (skip re-research):** rows with `tw_status`
  containing `complete` are machine-translated here already.
- **Known gaps you must cover manually:** print catalogs (Motilal,
  Indica, SUNY backlists), Hindi ṭīkās, Shodhganga theses, journal
  articles with translations inside, Lakshmanjoo audio/courses,
  OCHS pipeline (Flood Netra, Sanderson TA — both unpublished).

## 4. Method + honesty rules

1. Work `burn_order` ascending (shortest untranslated first — CSV is
   pre-sorted by priority in `ranked_burn.json`, ask for it if needed).
2. ~10 min/work cap.conform: WorldCat → Google Books UI → archive
   advancedsearch → Hindi query → thesis search → publisher catalogs.
3. `has_english TRUE` ONLY on a verified translation (file loads, or
   publisher page confirms). DOI/landing page alone = FALSE.
4. Partial = chapter list mandatory (`partial:VII-VIII`).
5. Forthcoming (Flood, Sanderson) = FALSE + note `in-prep`.
6. Every row gets `researcher` + `verified_at` + ≥1 URL or a logged
   negative ("checked WC/GB/archive/Hindi/thesis — nothing").

## 5. Return format

The filled CSV (same columns, no renames). We merge on `catalog`.
Questions about scope: untranslated-obscure wins over famous-duplicates.
