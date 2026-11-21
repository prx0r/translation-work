# Metadata inventories — Muktabodha headers vs OCHS schema (2026-11-11)

## 1. Muktabodha e-text header (between `####` blocks; census-parsed across 499)

| Field | Present in | Notes |
|---|---|---|
| Catalog number | 499/499 | M/E/I series; M = main library |
| Uniform title | 499/499 | IAST, primary identity key |
| Description | 499/499 | free text (Dyczkowski blurbs in 14) |
| Notes / Publication year / city / country | 499/499 | year often empty; country mostly India |
| Revision 0 | 406/499 | transcription revision log |
| Manuscript | 254/499 | BHU/NGMCP/IFP ms IDs — provenance! |
| Internet publisher | 250/499 | Muktabodha |
| Publisher | 249/499 | e.g. Varanasi Tantrika Text Series |
| Author | 191/499 | rest unattributed in header |
| Editor | 181/499 | |
| Main title | 141/499 | |
| Commentator | 109/499 | vṛtti/vivṛti authors (never mūla) |
| Secondary title | 103/499 | |
| Alternate name | 55/499 | alias identity |
| Main title / Subject / Extent / script / archive.org links | rare (≤4) | long-tail ad-hoc fields |

License line (all): CC BY-NC 4.0. NO tradition field anywhere —
traditions come ONLY from the library's browse pages
(`muktabodha-traditions-verbatim.md`).

## 2. OCHS schema (`muktabodha-demo-meta.xlsx`, 63 cols, from ulyngs/ochs-database-import-demos)

Internal catalogue id, Reference image, Add to website, Name
(transliteration/indic/translation), Alternative names, Author,
Language, Language (other), Script, Script (other), Patron of
manuscript, Scribe of manuscript, Sponsor for digitised manuscript,
Provenance category (+other/note), Current location of physical
manuscript, External catalogue ids, External meta data, License,
Multi-text manuscript, Dating of original text (+UTC), Date of
copying (+UTC), Place of production, Publisher, Material (+other),
Length/Height (cm), Condition, Binding hole(s), Folios/pages, Lines
per folio/page, Foliation/pagination, Number of volumes, Tradition(s)
& subject(s) (+other), Transliteration, Translation(s), Cataloguer(s),
Excerpt (Beginning/End/Sub-colophons/Colophon), Relevant secondary
literature, Illustrations, Remarks, Photos available?, Text available?,
PDF/TXT source(s), Internal notes, Note on storage location(s),
Text on Googlesheets, Description, Title (transliteration),
Manuscript, Publication city/country/year, Revision, Secondary title,
Uniform title, NA.

Overlap with Muktabodha headers: title/author/manuscript/publisher/
year/revision — OCHS adds tradition(s), translation(s), dating,
provenance, secondary literature (the four we aligned into the
research matrix as `traditions_authority/dating_text/provenance_ms/
secondary_literature`).

CSV export endpoint `muktabodha-digital-library.org/metadata/
download/csv` is Cloudflare-Turnstile walled (browser-only).
