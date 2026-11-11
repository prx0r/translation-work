# Manual translation search (for what machines can't reach)

*Packs: `manual_research_packs.json` (top-30 burn works, 6 queries each).
Budget ~10 min/work. A clean negative ("searched X, found nothing") IS
evidence — record it with date + queries run.*

## Order per work (~10 min)

1. **WorldCat** (worldcat.org search, query `worldcat`): any book record?
   Note OCLC number + library holdings count (holdings ≈ existence proof).
2. **Google Books UI** (books.google.com, NOT the API — our quota is
   burned): snippet/full view? Record link.
3. **Archive advancedsearch**: `<title> AND (translation OR translated)`.
4. **Hindi layer**: `<title> hindi anuvad OR hindi tika` — Hindi ṭīkās
   count as translations for most readers; record publisher if found.
5. **Theses**: Shodhganga search + `thesis translation` web query.
   Theses routinely translate chapters — chapter-level counts.
6. **Motilal/Exotic India catalogs**: in-print Indian editions.

## Recording (into research matrix row)

`translations[]` entries need: what (translator/year/scope) + where
(publisher/series) + link (verified loads) OR negative note
("checked WorldCat/GB/archive/Hindi/thesis 2026-11-11 — nothing").
`has_english: true` ONLY on a verified full/partial translation.
Partial = note chapters covered (like Singh's selected-chapters vol).

## Stop rules

- Stop at first verified FULL translation + one corroborating source.
- Cap 10 min/work; obscure paddhati/stotra texts will mostly be clean
  negatives — that's the expected result, not failure.
- Never mark from a DOI/landing page alone (pilot rule).
