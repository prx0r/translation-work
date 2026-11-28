# SPECIAL WORKS — non-standard objects (class: SPECIAL)

*These works cannot go through the verse pipeline. Each gets its own
intake, its own gate, and its own site presentation. DO NOT SEED.*

## 1. Kalpavṛkṣa (M00051) — Sāhib Kaul, 17th c. — CLASS: SPECIAL/LATTICE

**What it is.** A **carmen cancellatum**: a crossword-like visual poem
originally displayed on a **cloth ~1.5 m square** with a chessboard layout.
Red lines formed by **rubricated letters** run in all directions and form
the "intexts". **Three cloths survive** (Oriental Research Library,
Srinagar). It is **the largest carmen cancellatum in world literature**,
using **~30 languages** for its intexts (mostly South Asian, plus Persian
and Arabic). Its declared purpose: to show that Advaita Vedānta, Śaiva
non-dualism and "supreme non-dualism" are one conclusion.

**Why our e-text is not enough.** M00051 is a *flattened* transcription
(135 KB, 247 verse markers, from ms 1353, Śāradā, condition "bad"). The
geometry — the argument — is absent. Burning it would produce a
confident-looking translation of a work whose structure we deleted.

**Approach (own pipeline):**
1. `kalpavrksa.cell.json` — the grid as data:
   `{x, y, glyph, language, source_ref, role: base|intext, line_dir}`
2. Cloth ingest: rectified image → cell grid → calf each rubricated line.
   **The line is the unit, not the verse.**
3. Intext graph: `edges[]` typed by language + source text; this is what
   makes the 30-language claim queryable.
4. Translate **per cell**, provenance mandatory; unresolved source =
   AMBIGUOUS cell, never a guess.
5. Renderer: output must show the lattice (SVG/ASCII matrix). A linear
   translation of a carmen cancellatum is a false object.
6. Gate: no translation claim until (a) Hanneder 2021 collated and (b) at
   least one cloth reconstructed.

**Public sources (verified 2026-11-11):**
- Muktabodha e-text (our base): `muktalib7.com/.../kalpavRkSa-M00051-DEV.txt` (public, CC BY-NC 4.0)
- **Hanneder, *Sāhib Kaula's Tree of Languages*** (Indica et Tibetica 60, 2021) — first edition + study: publisher page `iet-verlag.de/ser_iet60.html`; €32 print / **€23.99 eBook (BoD)**
- Project summary (free): `kasaharaksa.de/storage/pdf/KSH-Summary-en-long.pdf`
- ORL Srinagar Sanskrit manuscript **catalogue** (free): archive.org `jk-orl-srinagar-sanskrit`
- Possible scans of Śāradā mss: **eGangotri** (egangotri.org, Sharada collection; ORL 6000+ collection)
- Berlin language-list ms: Sammlung Janert (Staatsbibliothek zu Berlin) — request access

**Site entry (special):** a dedicated page, not a work page — "The Cloth":
object photography, the lattice rendered as a grid, per-line languages, and
the non-duality thesis. Frame as an **artefact** (largest carmen
cancellatum), not as a translated text.

## 2. Other non-standard objects in the corpus

| Work | Issue | Handling |
|---|---|---|
| Devīnāmavilāsa (M00166) | reworks Bhavānīsahasranāma; ch.3 paraphrases Pratyabhijñāhṛdaya | normal verse pipeline, but **intertext links mandatory** in argmaps |
| M00501 | one file bundles Haṭhapradīpikā + Ācārasāratantra + Samayācāra | split before onboarding |
| M00576 / M00544 | one file bundles 4 texts each | split before onboarding |
| M00043 | bundles Parātriśikātātparyadīpikā + Śāktavijñāna | split before onboarding |
| 90 zero-verse works | prose | prose chunker (separate pipeline) |
| 232 extract-fail files | variant verse markers (`||4/18 (48)||` etc.) | parser extension, not translation work |

## Rule

A work classified SPECIAL may be **described, catalogued and exhibited**
without being "translated". It may not be marked machine-translated, and it
never enters the burn queue.
