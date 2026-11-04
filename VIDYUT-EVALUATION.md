# Optional Vidyut evaluation

`tools/vidyut_candidates.py` is a read-only experiment against one canonical
source span. It uses the optional `vidyut==0.4.0` Python wheel for transliteration
and, only when supplied a compatible meter file, an experimental meter candidate.
Nothing is written to T1, L0, L4, Git ledgers or the site. Review source coverage
and all outputs independently before using them.

Example after installing the optional package in an isolated environment:

```sh
python3 tools/vidyut_candidates.py --work paramarthasara --target param-p01-v01 --scheme iast
python3 tools/vidyut_candidates.py --work paramarthasara --target param-p01-v01 --scheme iast --meters /path/to/your/meters.tsv
```

The output records the source-file hash, locator, excerpt, input scheme, Vidyut
version, and meter-file hash if used. It does not prove that the referenced span
is complete or philologically correct. Ghaṭakarpara is explicitly withheld until
its source alignment is repaired. The meter classifier is experimental; `null` or
a partial match is not an identification of the metre.

Vidyut code is MIT-licensed; linguistic models, dictionaries and meter datasets
have independent provenance and rights. Supply data only when you have rights to
use it; do not commit or redistribute it merely because the code is open source.
The Chedaka segmenter needs a separately acquired model and lexical data and is
not integrated in this initial experiment. No linguistic data is vendored here.

Evaluation here: upstream source inspected at `2a802d0b6cfba5839f0a62cec174da1e58771ef8`;
the installed PyPI wheel is a separate release, version `0.4.0` (Linux x86-64
wheel SHA-256 `844d213d283218708e4aa5723d656e270a0b639e6ab9af3af96c62b760868b1f`).
Those identifiers do not imply that the wheel was built from that source commit.
A local Paramārthasāra passage was transliterated, and a locally supplied meter
file returned no named match. That result is not a philological assessment.
