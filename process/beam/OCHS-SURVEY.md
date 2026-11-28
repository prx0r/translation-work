# OCHS deep dive — what we can use and build on (2026-11-11)

## Usable now

1. **Metadata schema (63 cols).** Their manuscript sheet
   (`muktabodha-demo-meta.xlsx` in `ulyngs/ochs-database-import-demos`)
   models per-item: tradition(s), translation(s), dating, provenance,
   secondary literature, license, excerpts. Our research matrix now
   carries `dating_text/provenance_ms/secondary_literature/ochs_db_hit`
   to align. Their per-item curation >> our keyword guesses.
2. **Muktabodha import demos** (same repo: meta-extract + text-CSV
   .qmds). Validates our census parser (same front-matter headers);
   their text-CSV shape is a candidate interchange with our
   passages.jsonl (compare before inventing).
3. **Text-mining lecture code** (`ulyngs/ochs_text_mining`: GRETIL
   import/clean, frequency/co-occurrence/parallel analysis, dashboard
   prep in R). No R on our box — port the *analyses* to Python:
   school term-frequency profiles, parallel-passage detection
   (Dyczkowski-quote hunting), verse-length stats. Directly serves
   the "shared speciality terms" burn grouping.
4. **Taxonomy authority.** Sanderson "Śaiva Literature" streams +
   KSTS Trika threefold already adopted as burn schools v2.
5. **Netra coordination signal.** Flood/Wernicke-Olesen/Khatiwoda full
   Netra translation in prep (Routledge). Our Netra burn should track,
   not race, theirs — different base (M00038 vs NAK MS 1-285).

## Needs a browser (researcher lane)

- Manuscript DB contents (R flexdashboard; CSV download per view).
- Lakshmanjoo course/book catalog; OCHS course materials.

## Partnership (owner call, not machine)

- Team: Wernicke-Olesen (Netra/Śākta), Khatiwoda (manuscripts),
  Lyngs (methods, 102 repos, open-source everything), Flood (director).
- They explicitly want computational collaborators; we have the only
  running free-tier translation burn. Natural trade: our burn output
  + methods for their editions/manuscripts/scholarship review.
- Contact surface: ochs.org.uk Śākta programme pages; no cold-scrape.

## Watch, don't duplicate

- Sanderson multi-vol Tantrāloka edition+translation (in prep).
- Sutton Mokṣadharma translation (Hindu Studies Press).
- Mirador IIIF tests (needs manuscript images we don't hold).
