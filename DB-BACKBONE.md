# DB-BACKBONE — translation-work reads the portable openpatala box DB

*2026-11-06. Status: WIRED (read-only). translation-work owns its files;
the box DB is the identity spine. Nothing here writes to the DB — ever.
Loaders live in trika-x (`formal-trika/tools/{openpatala_seed,openpatala_ingest,work_inventory}.py --db`); this repo only reads.*

## Where the truth lives

- **Box dump (portable):** `s3://patala/openpatala/box-2026-11-06/` —
  `openpatala-box-2026-11-06.dump` (115 KB, sha256 `57d54032…ff16ec`,
  PG15-readable) + `manifest.json` (contents, SHAs, rev pins). Restored here
  as database `openpatala_box` (544 works / 909 passages / 87 editions /
  87 etexts). Recipe: `createdb openpatala_box && pg_restore --no-owner
  -d openpatala_box <dump>`.
- **Code/tools (pushed):** `prx0r/trika-x` (seed/ingest/inventory loaders,
  `bridge --db`, BACKBONE doc), `prx0r/svread` (`source-map.json`, 87 works).
  `prx0r/openpatala` itself: read-only reference (migrations, seeds).
- **Local live DB `openpatala` is NOT this box** (1399 works / 0 passages —
  another track's shape). Do not touch it. Use `openpatala_box`.

## How translation-work reads it

`tools/dbread.py` (SELECT only; DSN `$OPENPATALA_DSN`, default
`postgresql://patala:patala@localhost:5432/openpatala_box`):

```bash
python3 tools/dbread.py works [--q foo]   # search works
python3 tools/dbread.py work <db-id>       # work + editions + etexts + passage count
python3 tools/dbread.py passages <db-id>   # citation_value list (spans to translate)
python3 tools/dbread.py coverage <tw-dir>  # DB passages vs local data files (0 missing = covered)
python3 tools/dbread.py ids <tw-dir>       # provenance triple for bundle stamping
```

Locator dialects differ and are normalized inside: DB `chunkA-…` →
`chunk-a-…` (via `ipvv/chunk-song-map.json`), `tsa01-p01` → `tsa-a01`,
`tal-a15-p01` → `tal-a15`. DB passages are finer-grained than songs for
tsa/tal (ahnika song covers its pNN rows); ipvv is 1:1 (49/49 verified).

## Bundle-time provenance (BACKBONE §5.3, to wire)

`zenodo_publish.py` provenance.json gains `openpatala_work_id`,
`edition_id`, `ledger_sha256` — look up via `dbread.py ids <work>` at bundle
time. svread `source-map.json` still shows `openpatala_work_id: UNRESOLVED`
for translation-work works: resolving it is `dbread ids` output, not a
source-map edit (map stays candidate until owner says otherwise).

## Open questions (owner)

1. **assertions: manifest says 1532, restored DB has 1512** (−20). Restored
   clean, no pg_restore errors. Either manifest counted pre-delete rows or
   the dump trails the manifest. Do NOT "fix" by writing rows.
2. **`translations` table is empty (0 rows).** Nobody writes translation
   records to the DB today. If the endgame wants DB-side translation status,
   that needs an owner decision + a trika-x loader — out of this repo's lane.
3. Witnesses UNPINNED box-wide (table empty). Resolver hard-enforces.
