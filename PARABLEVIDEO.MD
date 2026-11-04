# PARABLEVIDEO.MD — the full journey, with process notes

*Canonical record of how the parable shorts came to be. Read this before
touching anything in the pipeline. Status: LIVING — song 4 is the proof;
songs 5+ follow the same road.*

## The idea in one line

Sanskrit → literal (exact) → parable (story) → tagged voice (granny) →
one image (freedom snapshot) → vertical short. Each layer feeds the next;
nothing downstream ever flows back.

## The journey (in order, with dates)

1. **Literal skill** (`ipvv/skills/literal/SKILL.md`). Karpathy's
   ASD-STE100 at 80%: short sentences, one idea each, plain words.
   Community roots: `danyuchn/asd-ste100-skill` (structural vs lexical
   split, scan checklist, output discipline) and `prithivrajmu/asd-ste100`
   (80%-by-default, preserve meaning first). Cloned to
   `/root/ste-upstream/` for reference.
2. **First literal pass, Paramarthasara song 1** — mechanical, from L2.
   Owner correction #1: *"doesn't appear literally"* (guhāsu → "caves"
   misleads; the stack is silent on the referent). Fix: resolve every
   image through the stack in tiers — stack says it / stable background
   (heart-caves, visible compound) / keep the bare image.
3. **SANSKRIT FIRST becomes law.** Never render from the gloss alone;
   re-read cite → T1 → L0 → argmap (clearest explanation) → L2 → C1,
   every verse. Sanskrit-first pass caught 9 real errors the L2-first
   draft had smuggled (missing gahanād line, invented placements,
   upgraded moods).
4. **No-metaphor rule.** Literal says what's actually talked about:
   similes and stock illustrations decode to referents; technical terms
   stay; concrete nouns without illustrating function stay. The parable
   lanes carry images; literal carries referents.
5. **Full literal pass, all 105 verses** (`paramarthasara/LITERAL-DRAFT.md`,
   MACHINE_DRAFT). Linted clean with upstream `ste-lint.py`.
6. **C2 voice work.** Stored genz turned out formal, not voice (canonical
   `.genz.json` = translator-hand terse). Real voice found only in
   bhairavastava experiments (`.gen-z.v2`, roadman). Lesson: check what
   the files actually contain before promising a voice.
7. **Roadman v1, all 105** (`paramarthasara/ROADMAN-v1.DRAFT.json`):
   per-verse c2 + rasa + choices with Sanskrit payloads, register audit
   clean (zero banned gen-z markers). House shape = bhairavastava v2.
8. **Allegory/myth split.** Not the same: parable = analogy (loose
   correspondence, point first — Nathan's sheep); myth = coded message
   (decode first — Ezekiel's eagle). Myth uses only the tradition's own
   images at full size; parable may frame with ordinary scenes.
9. **Parable skill** (`ipvv/skills/allegory/SKILL.md`). Community roots:
   `mblode/eli5` (one analogy + its limit), `companion-inc/feynman`
   (separate source from speculation), `rcosteira79` (packaging not
   facts), `guicortei/feynman-technique` (mechanism before name),
   `jwynia/paradox-fables` (embodiment test, no moral inside the story).
   Pedagogy roots: Gospel three-point shape, trap-and-turn, seed;
   exemplar shelf (Prodigal Son, Good Samaritan, Nathan, Zhuangzi's
   butterfly, Growing Seed, Cave).
10. **Plain-words-inside law.** No doctrine terms in the tale — Māyā,
    tanmātra, Sadāśiva never appear; the map holds them. Jesus-vibes:
    concrete nouns, one turn, end on the turn, never explain.
11. **Map the hinge, not every pebble.** Characters as beings, not walking
    allegories. Embodiment test: remove the doctrine — if the story
    still stands, it wasn't in it.
12. **Voices separated from writing.** Parable text is third-person
    narrative, no dialogue tags (granny/kid scripting was a wrong turn).
    Production adds the voice map: GRANNY reads (LOCKED: Granny British,
    owner's ear pick); KID only where the story has a child.
13. **Tagged delivery.** Inline drama tags per damn house guide (max 3,
    one emotion/sentence, pauses do the work), rasa→direction, validated
    on paper (`damn/fish/validate.py`, PASS shippable). Song 4 rendered
    in Granny's voice via worker `/api/read` (free tier), 9 segments
    stitched: `parables/song04-granny-full.mp3` (92s).
14. **One image, final snapshot.** Preset `sleepdraw/lora2-inv.yaml`
    (inverse of lora2: black ink / white paper / 9:16, locked lora files
    untouched). Rule: never the struggle, always the arrival; rasa
    encoded (stillness = white space, luminosity = densest ink, release
    = upward motion). One landscape per parable, no per-beat boards.
15. **Registry** (`PARABLEREGISTRY.md`): 30 works shortest-first,
    Paramarthasara in progress, batch order scripts → confirm →
    image+audio → assembly. Phase 1 = still + slow zoom; Phase 2 =
    inverted etch reveal (not yet built).

## Laws (do not break)

- SANSKRIT FIRST. Whole stack re-read, argmap clearest, gloss never first.
- Literal = no metaphors. Story lanes = images. Never the reverse.
- The arrow runs Sanskrit → exact → story, never story → exact.
- Parable: ordinary words inside, map outside, no moral inside the tale.
- Map the hinge. Characters are beings. Embodiment test every parable.
- Machine proposes, human disposes. MACHINE_DRAFT until promoted.
- No renders without explicit owner yes per call. No secrets in repos.

## Worked reference: song 4 (the proof)

**Parable** (third-person, no doctrine words):
> A spider spun her web between two branches and sat in the middle of it.
> She slept in it, dreamed in it, woke in it — and never once stepped
> outside it. When the wind came — cloud, smoke, dust — she watched her
> threads shake and thought the whole world was shaking. The sky above
> stayed blue all along. She never looked up. One still morning, dew
> settled on every thread, and each drop held its own small sun. The
> spider looked — really looked — and remembered: *I made this.* She
> walked out along her very first thread, into the open air that had
> never gone anywhere. The web stayed, beaded and shining. She did not.

**Map** (hinge): slept/dreamed/woke inside → three states + fourth [34–35];
threads shaking = world shaking → mistaking non-self for self [30–31];
blue sky unlooked-at → untouched [36]; dewdrop suns → stain doesn't
pass [37]; *I made this* → unwrapping [33]; walked out, web stayed →
release, play continues [v32–33].
**Limit**: the garden keeps its webs; only the sitter leaves. Freedom
isn't the end of webs. **Rasa**: karuṇa-śānta — pity the self-tied,
peace the open air.

**Justification, layer by layer:**
- *Rasa (C1)*: karuṇa-śānta, "darkness pitied, unwrapping stillness."
  The parable's arc IS that sentence.
- *L4*: v32 already says "as does the spider" — the parable extends L4's
  own image. v33's "bright play of bound and free" → "The web stayed.
  She did not." v36–37 → blue sky, dewdrop suns. Cadence borrowed from
  L4's clipped parallels.
- *Argmap*: v32 "How net-wrapped?" and v33 "Whose play?" become the two
  motions (tying, walking out).
- *Essence*: all 7 C1 entries mapped, one per picture-beat.

**Delivery** (drama-3 tags, validated PASS): calm/warm/slowly throughout;
low voice for darkness; sad for the taking; hope for unwrapping; long
pauses before "he shone through it all, unveiled" and the close.
Voice: GRANNY (locked).

**Image prompt** (lora2-inv, black on white, vertical):
> Black ink sketch on warm white paper, hand-drawn storybook etching:
> vast open sky filling most of the frame, a small luminous spider
> ascending on a single gossamer thread toward the light above, below it
> an empty beaded web strung between two bare branches, a few dewdrops
> catching light on the threads, fine monochrome grey ink linework,
> dense etched detail on spider and web, wide breathing white space,
> no text, no letters, vertical composition 9:16

## Open threads

- FAL key missing (checked env, vault files, opencode config) — image
  gen blocked until owner provides it. Draft renders via Cloudflare
  Workers AI (flux-1-schnell) meanwhile.
- Fish MCP OAuth: `opencode mcp auth fish-audio` prints the authorize
  URL and listens on 127.0.0.1:19876; needs the browser reachable to
  the box (SSH -L 19876:localhost:19876 if remote). Awaiting owner click.
- Drama-3 needs $5 API credit (402 until topped up). Free tier works now
  (storyteller + worker-granny paths proven).
- KID voice uncast. Poetic lane has zero stored renders (live-only).
  Stored genz is formal-register (mislabeled, see §6).
- Video assembly Phase 2 (inverted etch reveal) unbuilt. Phase 1 = still
  + slow zoom + subtitles + granny VO.

## ASSEMBLY SPEC (the video, locked 2026-11-04)

### Image (finished art, song 4 reference)
- Model: `fal-ai/flux-2-lora-gallery/ballpoint-pen-sketch` (trigger
  `b4llp01nt`, $0.021/MP, seed recorded per image — seed+prompt =
  same image). Cloudflare flux-1-schnell = cheap drafts only.
- Prompt encodes FULL RASA in layers (see song 4 prompt above) and
  passes the review gate: setting = song's set, subject placed where
  the story leaves it, composition reads release.
- L4 density pass: bottom = knotted roots, tangled web, heavy dark
  ink (sorrow's weight); top = clear sparkling freedom (sky as pure
  white). The vertical gradient IS the rasa: karuṇa-śānta from thick
  roots heading toward the sky. Regenerate with denser bottom before
  final.
- BACKGROUND ALWAYS PURE WHITE `#FFFFFF` — not cream, not faded, not
  paper-tinted. Enforced in prompt AND post (levels/gamma check).

### Etch draw (lora2-inv / techdou)
- techdou `generate_whiteboard.py` natively draws BLACK lines on a
  light canvas (`WB_BG`, `BLACK_PIXEL_THRESHOLD=10`) — no inversion
  needed. Set `WB_BG=#FFFFFF` (its default `#F6F1E3` is cream —
  MUST override or it reverts to faded white).
- Duration = audio length (`--duration`, song 4 = 92s).
- DIRECTION IS THE RASA: draw BOTTOM → TOP, ending on the spider.
  techdou currently orders blocks top-down-ish (component sort + NN
  within block) — needs a patch: sort global component draw order by
  y descending (roots first, sky-ward last, spider last of all).
  Vendored MIT, sleepdraw already patches vendor — add
  `WB_BOTTOM_UP=1` env, default off, sleep channels unaffected.
- End: 2-second fade to WHITE in silence — clean loop point (viewers
  re-see the white start seamlessly). Post step: ffmpeg
  `fade=out:color=white:st=<dur-2>:d=2` + audio afade out.
  Not techdou's hold phase (that holds the frame, doesn't fade).

### Shorts layout (NOT plain YouTube full-frame)
- 9:16 total. Image does NOT fill it: art occupies top ~75%
  (1080×1440), bottom ~25% (1080×480) stays PURE WHITE for
  SUBTITLES (granny's lines, timed to audio). The white subtitle
  zone is continuous with the art's sky — one white field.
- YouTube Shorts would overlay captions on art; we don't want that.
  Custom-assembled: image + white zone + burned subtitles → upload
  as-is.

### Print (Prodigi, sell the art)
- `.prodigi.env` at /root is EMPTY (0 bytes) — no creds yet.
- Target: fine art greetings cards. Sizes offered: 4x6"/10x15cm,
  5x5", 5x7"/12.5x18cm (portrait — closest to our vertical), A4.
  File: JPG or PDF, 300dpi optimal. Our 1080×1920 = ~4.5×8in at
  300dpi — 5x7" card fits with white margins (margins are our
  aesthetic). 324gsm Mohawk matte = the better paper for ink art.
- Same art sells as postcard (4x6", 350gsm) too.

### Batch order (unchanged)
ALL scripts → owner confirm → images (with review gate) → audio →
assembly (etch + fades + subtitles) → shorts + card files.

### WHITE-NORMALIZE (mandatory pre-step, proven 2026-11-04)
Source images carry the model's paper tone (ballpoint LoRA renders warm
cream ~243,232,213) and techdou composites it — WB_BG only shows where
source is absent. So before ANY etch: levels pass, snap paper to pure
white: `v>=200 → 255` (ink lives <120, safe band), keep ink curve below.
Verified: corners all (255,255,255), darkest 0, ~89% pure white.
Smoke etch (6s, WB_BG=#FFFFFF, no-hand): natively black-on-white,
no inversion needed; h264 shifts ~255→251 (encode at higher quality /
yuv444 for delivery).
Duration flag is MILLISECONDS (`--duration 92000` for song 4's 92s).

### PRODIGI (docs imported 2026-11-04) — sell the art
- PRIMARY: **fine art postcard 5x7"** = 125x175mm portrait, 324gsm
  Mohawk matte, Giclée, from £1.00, ships worldwide, SKU GLOBAL-POST.
  Alt: fine art postcard 4x6" (10x15cm). Small-print upsell: smooth
  art paper print 5x7"+ from £2.23 (also Giclée).
  NEVER classic postcard (152x109 landscape — crops the art).
- Files: JPG/PNG @ **300dpi** → 5x7" = **1500x2100px**. Current art
  576x1024 (~180dpi ok for line art); regenerate ballpoint at
  1500x2100 (custom size allowed ≤2048) before selling. Bleed auto.
- ⚠ AUTO-CROP trap: default central-crop to product aspect. Our 9:16
  (0.56) is narrower than 5x7" (0.71) → would trim top/bottom (spider
  or web). ALWAYS pre-compose on a white 1500x2100 canvas, art
  centered — margins are our aesthetic anyway.
- Creds: `/root/.prodigi.env` EMPTY — need Prodigi account (Sandbox
  key first); manual order form works for a first sample without code.
- 50% off first sample order (Prodigi policy) — order one before
  selling.

### FRAME LAW (owner, 2026-11-04)
Central panel = the parable's own simple ink art (the story, one image).
Border = THE WORLD L4 DESCRIBES from the Sanskrit — the verse's imagery
rendered as illuminated Splendor Solis border, expounding C1 + all the
rasa: motifs from the song's own words, mood/palette from C1 rasa.
The page itself preaches the text. Reference set:
`sleepdraw/assets/refs-splendor-solis/` (Commons PD, Wellcome +
Harley 3469 + BnF; user-picked plates included).

## P1 SEED — v4: how it was made, and why it is a seal

**Artifact:** `parables/song04-solis-p1v4.png` (published R2).
**Model:** fal `flux-pro/kontext` · ref: user-picked Solis bordered page
(`parables/refs/solis-page.jpg`) · seed 123 · guidance 3.5 · 3:4.

### How it came to be (3 failures first)
v1: pretty + basic — I over-specified structure (roundels, "keep the
border"), Kontext obeyed instructions instead of thinking; border stayed
generic foliage. v2: I *replaced the web with a thread* in the prompt —
the middle zone died, a duplicate spider appeared in the roundel. v3:
correct four-zone brief but roundel-micromanaged; got heavy and fussy.
The owner's correction, which is the actual method: **reference carries
the structure; the prompt carries only the seal — vividly.** The less
you steer, the more the manuscript's own intelligence survives.
v4 prompt in full: *"In the manner of this manuscript page, one vertical
seal: at the bottom, black gnarled roots knotted into a choking tangle;
among those roots a spider web, strung tight and constricted, choked
with tangled threads and old debris, glistening with caught dewdrops
like imprisoned stars; from the web's dark heart one gossamer thread
climbs, and the spider — one only — weaves herself up along it, legs
strung to the line, leaving the knot below; above her the sky opens
into pure gold-white light, and she ascends into it, small and blazing,
free. Roots hold the web. Web holds the thread. Thread holds the light.
Colors: umber and black at the base, lapis and ivory mid-air, burning
gold at the crown. Pity below, peace above. No text, no letters, one
spider total."* Nothing else. No roundels, no border commands, no
template talk.

### The seal exegesis — every zone is a verse
The image reads bottom→top, which is the parable's chronology AND the
song's argument, compressed into one axis (Solis plates stage alchemical
sequence; this one stages it rising):

1. **Black gnarled roots** — v29–31: the unreal orders arising by
   delusion-power; darkness shining in things; body and breath taken
   for self. The choke is literal: roots that knot.
2. **The knotted ball at the center, star inside it** — v32: *"the self
   nets itself — a wonder — as does the spider."* The web is not
   pretty here: it is a wound-dark knot (karuṇa — pity the self-tied).
   And the cold star INSIDE the knot is v33's *own knowing glory* —
   the unwrapping-source was never outside the net. The knot contains
   its own key.
3. **The one gossamer thread climbing out, beaded** — the parable's
   *"she walked out along her very first thread"*, and v33's
   unwrapping by her own knowing. Dew = the verse's own water imagery
   (v36: cloud cannot soil what it touches; the beads stay clean
   climbing).
4. **The spider — one only, legs strung to the line, mid-climb** — the
   enlightened sitter leaving. She is between worlds: below her the
   knot still exists (the web stays — release is not destruction),
   above her only light.
5. **The gold-white burst, crowned by the arch** — v34–35: the fourth
   abode, unveiled, *"past that, the fourth"*; bhāsvarūpa,
   light-formed. The frame's arch = the abode with no canvas from the
   parable's telling — the structure itself becomes the fourth tent.
6. **Clouds and clear sky flanks** — v36–37: cloud, smoke, dust leave
   the sky unstained; one jar's dust does not travel. The world-green
   at the sides continues untouched.

**Rasa as gradient:** C1 gives *karuṇa-śānta — darkness pitied,
unwrapping stillness.* The image encodes it vertically: umber knot and
shadow below (pity — sorrow fully painted, not denied), unwrapping
line in the middle (the turning), burning stillness above (peace —
where nothing is, gold). The vertical gradient IS the sthāyibhāva
movement from karuṇā to śama. L4's couplets become the reading order.

**Why it works as a seal:** nothing in it is decoration. Remove any
zone and a verse goes missing; the reader who knows the text reads the
song at a glance, the reader who doesn't sees the argument before a
word — bondage holding its own key, held in light. That is the whole
translated work in one frame: literal (the zones as facts), argmap
(knot → unwrapping → freedom as inference), C1 (rasa gradient),
L4 (its own imagery), parable (its exact five beats).

# ============ NORTHSTAR (owner's verbatim words, 2026-11-04) ============

> "the prarable and p1 can work together basically encoding the sanskrit
> work into parable and art .. we can save the renders into a quee as
> they take time right p0 is getting all teh parables written and at the
> same time the seals (rereading all the layers ) and the p1 prompt and
> choosing a splender solis base, then using that exact base in the
> construction of our chosen rseal"

Supporting verbatim (same day, standing law):
> "just use solis as reference and implicitly say retain all stylings"
> "the whole text itself drives the seal"
> "for p1 we need to create the logic of the seal using all available
> info and then thinking about like hermetic art alchemical art how
> meaning is encoded in symbols and then basically making it so no
> mistakes can be made"

READ THE FLOW AS: P0 = parables written (Sanskrit-first, all layers).
Simultaneously per parable: seal reread of layers → P1 (seal logic +
double-anchor key + checklist) → choose an UNSPENT Splendor Solis base
(SOLIS-REFS.md stage-match) → render with THAT EXACT BASE via fal
kontext (ref carries style IMPLICITLY; prompt = seal text only) →
owner review gate → save render to the R2 queue (they take time).
Parable and P1 together encode the Sanskrit work into story and art.

# ============ JOURNEY LOG (for the next agent) ============

## Path walked (order matters)
1. literal skill (STE-80) → Paramarthasara full 105-verse literal
   (LITERAL-DRAFT) → roadman v1 105 (ROADMAN-v1.DRAFT) → allegory
   skill (parable/myth/eli5 modes) → parable diction laws → song-by-
   song parables with map/limit/rasa → voice layer (granny locked)
   → tagged drama scripts (validated PASS) → granny audio via worker
   (48.6s spider parable) → image law (final-snapshot, rasa gradient)
   → fal ballpoint ink art → print cut (1500×2100@305dpi, ivory
   margins) → P1 seal method → SOLIS-REFS stage-match book → v4 seal
   (keeper) → technical seal → Solis restyle (rejected as AI-looking)
   → v4 etched at audio length (techdou, bottom-up acts, 48588ms).

## Mistakes (each one is now a law somewhere above)
- Rendered literal from L2 first → missed gahanād (heart-caves).
  LAW: Sanskrit first, whole stack, argmap clearest.
- Metaphors in literal (rock "caves") → resolve tiers (stack says it /
  stable background visible / bare image kept).
- Song-4 pageant parable (9 beats, cast) → tortoise-and-hare bar:
  one essence, ≤2 characters, one image, retellable. The spider
  parable is the keeper.
- Scripted GRANNY/KID tags INTO the parable text → voices are a
  PRODUCTION layer; story text is third-person, clean.
- P1 v1/v2/v3 over-specification (roundels, "keep the border",
  template parts) → produced template AI-look and a lost web.
  LAW: ref carries structure+style; prompt carries ONLY the seal,
  vivid. LESS IS BETTER (owner).
- v2 prompt replaced web with a thread → the middle zone died;
  duplicate spider echoed into roundel. LAWS: all zones connected;
  exactly one subject.
- Two-step "transform into Solis treatment" → looks AI-generated.
  LAW: implicit style retention — one step, reference does styling.
- CF "cheap ref path": our CF catalog has NO ref-accepting model
  (inpaint 400, only flux t2i). Renderer = fal kontext, $0.04/image.
- Print compose sampled a dark edge → black margin bars. LAW:
  fixed PAPER constant + aspect-exact compose (Prodigi crop no-op).
- Worker API 403s bare urllib (CF bot block) → playwright browser
  path for /api/read (free granny voice).
- Background renders killed by tool session cleanup (setsid too) →
  render in FOREGROUND with long timeout (92s/48s etches ≈ 2.4 min).
- Commons bulk download 429'd (110 files) → bounded lists, 3–5s
  delays, never full-catalogue crawls (owner: "u taking way too long").
- Review gate saved the product: owner caught v1 (spider not between
  branches / not going for freedom) and v3 (no web, wrong roundel).
  Never ship an image without checking it against the parable.

## Things that worked (do these again)
- Seeds logged per render (seed+prompt = same image).
- validate.py paper-check before ANY spend ($0 discipline).
- White-normalize pre-step (v≥200→255) for ink art; colour plates
  compose on PAPER constant.
- techdou bottom-up acts patch (WB_BOTTOM_UP + inverted _act_reorder,
  WB_ACTS=4 + breath pauses) — roots first, spider last; verify with
  contact sheets, not vibes.
- Stage-match Solis selection (SOLIS-REFS.md) + spent-log per plate.
- P1 double-anchor rule (symbol must cite verse AND essence) +
  anti-mistake checklist before every render.

# ============ TOP 5 TO-DOS (next agents, in order) ============
1. **P0 batch** — write remaining parables per PARABLEREGISTRY.md
   (songs 5→12, then works): Sanskrit first, all layers, tortoise-hare
   bar, map/limit/rasa. Owner reviews each before any media.
2. **Seal loop per approved parable** — reread layers → P1 file
   (`<work>/P1-<song>-SEAL.md`: zone table, colour cipher, double-
   anchor key, checklist) → choose UNSPENT Solis base by stage-match →
   fal kontext render (base + seal-text ONLY, seed logged) → review
   gate → save to R2 queue (`parables/` + registry render column).
3. **Finish product #1 (song 4)** — etch DONE (`/tmp/parab/etch_v4/`
   34.4MB @48588ms), audio DONE (`parables/song04-spider-granny.mp3`,
   48.6s). REMAINS: assemble 9:16 (art top 1080×1512 + white bottom
   408px), burn subtitles from the 5 segments, 2s fade-to-white in
   silence → publish. Then Prodigi sample (creds: `.prodigi.env` empty).
4. **Queue discipline** — renders take time: scripts+P1 first, media
   after owner confirm (registry batch rule); every render lands in
   R2 `parables/` with seed + P1 path logged in the registry.
5. **Docs discipline** — every mistake/win appends to this JOURNEY
   LOG; never reuse a spent Solis base; renderer is fal kontext
   ($0.04), CF has no ref-model; owner eyes every image.

# ============ SEAL READING APPARATUS (web findings, 2026-11-04) ============

## Adam McLean / alchemywebsite — the method (free pages, use it)
- `emblems_project_introduction.html`: emblem = "a gathering together
  of alchemical symbols into an integrated image"; sense comes from
  **how symbols link in the GEOMETRY of the emblem**, not from
  isolated lookups. Naive reading = projecting preconceptions.
- `symbolic.html` (KEY): **no fixed dictionary** — same symbol means
  different things in different works; symbols must be read (a) as
  part of the whole emblem, (b) by WHAT THEY ARE DOING (giving?
  receiving? rising?), (c) by relation (left/right, top/bottom,
  triangle/square), (d) with the ground/background as content.
- `emblems_project_courses.html` / Foundation Course 24 lessons: the
  curriculum = geometry, oppositions, trees, birds, animals, "how
  NOT to interpret", **"reading an emblem from within itself"** —
  that lesson IS our double-anchor law. McLean's stated method:
  "no importing of external ideas, no projecting modern mentalities"
  — identical to our no-new-doctrine law. Jung = optional lens, NOT
  ours (stay contextual, text-internal).
- Rosarium commentary method: "integrating the symbols into a
  complete pattern rather than analyzing them as separate symbols"
  — our v4 zone-continuity rule, said by him first.

## Plate-by-plate commentaries (for SOLIS-REFS accuracy + P1 depth)
- **Skinner, *Splendor Solis* (Watkins 2019)** — has a whole chapter
  "Commentary on the Text and Plates of Splendor Solis" (plate-by-
  plate exegesis; also Prinke authorship, Godwin translation). PDF
  copies exist (archive.org / rexresearch). THE plate reference.
- **mythcrafts.com plate series** (free): reads central scene AND
  frame symbols (plate 2: deer=soul, bee=soul, butterfly=Great Work,
  peacock=cauda pavonis middle-stage) — **proof that frames were
  read as commentary**, and a ready border-symbol vocabulary for us.
- Sherwood, *Transformation of the Psyche* (Routledge 2015).
- Völlnagel 2011 (BL Journal, free): Harley 3469 production +
  iconography sources.
- Feinstein 2006 (Sixteenth Century J.): framing devices ("ordinary
  horse" as frame-logic) — frame analysis is a real subfield.
- ⚠ Skinner debunks the 22-plates↔22-tarot mapping ("hard to find a
  single good link") — do NOT use tarot in SOLIS-REFS.

## Two gifts for our flow
1. **Treatise 5.1 of Solis itself contains a summary of each plate**
   (so the text explains its image) — historical precedent for P1:
   P1 is our Sanskrit's plate-summary in reverse.
2. **Border symbol vocabulary** (checked, from Solis itself):
   butterfly = transformation; peacock = many-colored middle stage;
   bee/deer = soul; birds = volatile/fixed (tied bird vs flying bird
   = fixed vs volatile!). Our "border = L4's world" now has Solis's
   own approved symbol set to build from — stage-correct, not improvised.

## Added to P1 checklist (relation + geometry pass)
- [ ] Each element's ACTION stated (rising? receiving? holding?) —
      McLean: what symbols DO, not what they are?
- [ ] Positions carry meaning (above/below = above/below IN THE
      VERSE too)? Geometric arrangement checked?
- [ ] Frame/background elements also double-anchored (they're
      commentary — mythcrafts reads them)?
- [ ] No external-projected meanings (Jung/tarot/etc.) — from within
      the text only.

# ============ RATINGS + NEW ANGLES (owner review round 1) ============
Kid-story bar applied: mechanism visible (spider: weaves knots →
weaves to freedom), self-caused, no explaining, retellable. Full
ratings in PARABLEREGISTRY. Verdict: ghatakarpara best (9.4);
paryantapancasika worst (5.8) — bathhouse = invented frame,
ten-fingers = my massage-reading. Re-angles found for worst four:
- paryanta → THE POND THAT WAS NEVER HEATED (rest-makes-weather =
  the emission doctrine as a kid-mechanism: never heated, steams
  anyway; poke it = flat; leave it twice-rested = steam carries
  your own face back = face-to-face).
- isvarasiddhi → THE POT WITH THE THUMB-HANDLE (fitness-proof:
  handle closes on a thumb it never met = maker-proven; kills the
  lecture; reductio folds into "who showed you my thumb?").
- ajadapramatrsiddhi → THE UNWEIGHABLE SCALE (everything weighs,
  the scale can't weigh itself; 'this/its two words' kept; papers→
  no-ledger-civic-strain).
- sivastotravali → THE TWENTY KNOTS OF WHEN (she knots twenty
  whens on her string asking the sky; twenty-first knot the string
  is empty and the feast is on the table — answers s09 engine +
  s17 feast, de-folds s10/13-14/19 into the waiting).
- param-s05 → THE IMPOSSIBLE-ORDER STALL (sky-flower = the stock
  that only impossible shops keep; one-gold under designs).
paryanta full re-draft written to PARY-CANONICAL-SEAL-P1.md (v2).

# ============ OWNER TASTE RULE (round 2 — bind all future P1s) ============
> "surely some cooler ones. the spider is mythic compared to these"

The bar = MYTHIC: the image is a cosmic type performing its own
doctrine (spider weaves the bondage it escapes). BANNED registers:
institutions (census, workshop, steward-office, school, bathhouse),
explaining-figures (travelers who lecture), cleverness-without-myth
(thumb-handles, scales rejected on feel). Required: the image must
perform the teaching WITHOUT anyone in the story understanding it;
ideally kid-verifiable (flame-has-no-shadow class); art must be
COOL (owner judges image-appeal as a criterion).

## Owner verdicts logged
- APPROVED (develop as P1 rewrites): isvarasiddhi = **FOOTPRINT ON
  THE UNWALKED SHORE** ("gorgeous"); ajadapramatrsiddhi = **HALL
  WHERE ONLY FLAMES HAVE NO SHADOW** ("gorgeous, art could be
  incredible"); bodhapancadasika = **GARDEN BLOOMS INTO ITS OWN
  SEAL** ("sounds cool").
- REJECTED: paryanta v2-anti-narcissus angle ("makes no sense") →
  3 new ideas requested.
- DEFERRED by owner: sivastotravali lotus-twentieth-rain re-angle —
  "maybe lets leave it, it's a bit long" → original parable stands.
- Standing loves: spider-mythic standard; ghatakarpara best; kid-
  story retellability; the §1-pattern literal; granny voice; v4
  seal art.

# ============ PROCESS NOTES — how the hits were found (round 2) ============

## The approach-to-hits (use this forever)
1. **Image-first inversion.** Never start from the thesis. List the
   text's own images (the furniture), then ask: which ONE object can
   PERFORM the whole argument? Spider/web (song4), footprint
   (isvara), still-sea (paryanta), garland (krama), garden (bodha),
   print-palm (isva's own p07).
2. **The mechanism test (the spider standard).** The image must DO
   the teaching physically, kid-verifiable, no explanation inside:
   weave→knot→climb-to-freedom; foot fits print → maker proven;
   never-heated stillness → spills stars; flame casts no shadow →
   knower-not-inert. If a child can't re-tell the CAUSE, it fails.
3. **Institution sweep (the round-2 kill-list).** census, workshop,
   bathhouse, school, steward-office, town-argue = lecture-frames.
   Replace with natural/cosmic registers: shore, sea, hall-of-
   flames, garden, lotus, pond. Your verdicts proved it: every
   institution frame rated ≤6.8; every natural frame ≥7.5.
4. **Show-don't-tell law.** Explaining figures (the traveler who
   lectures, the judges) banned. Doctrine shown as BEHAVIOR OF
   THINGS: the door replies by brightening; the print fits; the
   steam carries your face. "The image must perform the teaching
   without anyone in the story understanding it."
5. **Double-anchor audit BEFORE presenting.** After drafting, re-
   verify every beat against THIS work's passages only. Your one
   question ("ensure they still are related to the texts?") caught
   two cross-text leaks (parapraveśikā's proof-retired and ten-
   trumpets smuggled into paryanta ideas A/C). RULE: a great line
   never crosses works.
6. **Self-grade against the benchmark before showing.** Rate vs
   the spider (9.5) honestly — self-rating surfaced paryanta as
   worst at 5.8 BEFORE you had to say it. Fix-first, then present.
7. **Triple-option rule.** When an angle dies, offer THREE distinct
   ones spanning different engines of the text (drum=emission,
   sea=reflection-rest, book=speech) — the pick is then strategic,
   not cosmetic.
8. **Approval-mining → law.** Your verdicts become written taste
   (below) so future work pre-filters: "gorgeous" = mythic register
   + real-world-verifiable + art-potential; "cool" = watch-it-grow/
   self-causing mechanism; "let's leave" = length-honesty beats
   ambition.
9. **Anatomy of a hit (footprint/flame/garden/sea):**
   (a) real-world-verifiable phenomenon (flame-no-shadow, foot-fit),
   (b) mythic register (trace-of-the-unseen, still-sea cosmology),
   (c) the work's own FINAL image promoted to the centre (bodha's
   v15 emblem becomes the garden's fruit; isva's palm-jewel becomes
   the print's palm), (d) closing beat = the text's own closing
   claim worded plainly ("the proof stands", "it conquers").
10. **Your loves, catalogued:** spider-mythic; ghatakarpara-style
    wit+text-true endings ("She has said it"); mechanism-as-story;
    art-appeal as a scoring criterion; kid-retellability; one-sentence
    seals; granny voice; §1-literal; v4's final-snapshot rasa-in-art;
    face-to-face/two-hands-gap imagery. **Your hates:** institutions,
    explaining figures, cleverness-without-myth, cross-text leaks,
    over-specified prompts, dense clause-folding, anyone translating
    essences into abstractions the child can't hold.

# ============ MECHANISM RE-AUDIT (todo 7 — spider standard, all 19) ============
Verdict per parable: does the image PHYSICALLY perform the teaching
(kid-verifiable cause), with no explainer?
PERFORMS (pass): ghatakarpara (pour-rings-nothing-back) ·
bhairavastava (glare-slides, bow-dances, heat-drops) ·
spandasandoha (waves = his throb) · parapravesika (never-heated-
class: proof-down → sprout-up) · kramastotra (cut-at-fullness →
loop) · sambandhasiddhi (logs-apart don't join — demo) ·
anubhavanivedana (notes vanish by becoming) · phrdaya (descent/
return on ONE stair) · bodhavilasa (never-heated well-rope runs) ·
ajada-v2 (flame-no-shadow — kid-testable FACT) · isva-v2 (fit) ·
paryanta-v3 (stillness spills stars) · param-s05/s06/s07/s08/s09/
s10/s11 (mirror-wipes, ford-crossing, file-ends-open, anywhere-
walked, temple-lamps, gem-cut, costume-falls) · bodha-v2 (watch-
it-grow) · bhairavanukarana (cup-drinks → declaration).
WEAK / EXPLAINER-DEPENDENT (candidates for owner review, no re-angle
without his word):
- pancashloki (7.5) — the old traveler EXPLAINS the doctrine (the
  v2 idea on file: "the door replies by getting brighter" kills
  him).
- sivastotravali (6.8) — several clauses are essence-translation,
  not mechanism (owner already deferred re-angle: "let's leave it").
- sambandhasiddhi tail — "every other relation is that knowing
  wearing a face" = abstraction the tail must SHOW (ribbon hanging
  each join is the show; the final sentence tells) — one-line fix
  candidate.
- anuttarastika + paramarthacarca — mirror/glass OVERLAP (both
  perform, but the set's variety ding: one may swap to
  moonlight-that-stayed-after-waking at owner's pleasure).
Mechanism-standard now = law in skill (p1-seal v1.1 note appended
next edit).

# ============ ROUND-3 LAW: THE ONE-LINE TEST (owner) ============
> "wf is shrine-dust? like im reading parables and having to figure
> them out?? think spider.. spun itself in knots then spun itself to
> freedom. beautiful — i shouldnt need to squint."

Rule: one plain sentence states the core after ONE hearing. Seal
names = real-world kid nouns (heat-city ✓ / shrine-dust ✗ /
altar-of-refusals ✗ / heartbeat-under-everything ✓). Layer-terms
become kid-nouns in the telling. Added to p1-seal SKILL; all five
tier-2 parables rewritten plain.

# ============ ROUND-4: NATURE-FIRST (owner's method) ============
> "think about the nature of the thing and make that the rasa — for
> spanda its pulsating throb, so a vibration, or eye of the storm,
> or a creature reborn"

Rule: BEFORE drafting, ask: what is this work's NATURAL
PHENOMENON — the real-world event whose physics already IS the
teaching? (spanda → the storm whose eye was never made; deha →
the hive where the senses bring the pollen; pdva → heat-haze;
rhpa → the morning itself; mpa → the gift that sinks.) The
phenomenon becomes both parable and seal; rasa rides its weather.
One-line + nature-first now = the two gates of every parable.

# ============ ROUND-5: ANIMALS/FOLK-FIRST + TECHNICAL-FIDELITY GUARD ============
> "animals will usually be a good go to also just nature in general,
> folk story type — ensure ur not sacrificing the actual text
> technicals though"

Law: when the nature-first question hits a wall, ask next: which
ANIMAL or folk-event already performs this? (deha → the hive/bees
because the text's flower-feasts ARE pollen-loads; spanda → storm/
eye; krama → garland; etc.) Nature and folk-tale beats > invented
human institutions, ALWAYS.
THE GUARD (equal weight): the animal must ENCODE the technicals,
never evict them. Checklist addition (in p1-seal SKILL): the
TECHNICAL-FIDELITY line — every technical member of the work
(counts, loci, stations, lists, named structures) must appear
plainly in the telling OR be named in the hinge-map. Example that
passes: deha-v2 keeps temple (the doctrine), six pollen-loads (the
six senses), queen-hum (quivering-pith), eight cells (petals) —
the bees did NOT replace the anatomy; they carry it.

# ============ ROUND-6: THE DOORWAY TITLE (owner, on svabodhasiddhi) ============
> "immediately im in from the title.. sun never sets?! incredible
> beautiful im already in awe"

The one-line/title = a DOORWAY, not a summary: name the
impossible natural thing first, flat and plain — the reader's
"wait — where?" supplies the awe, and the doctrine walks in behind
the wonder. Check every title: does it make you step IN? (sun-
never-sets = door; heartbeat-under-everything = summary → rewrite
at review). Awe-before-terminology = the title's whole job.

# ============ EMBEDDING AUDIT — mechanics IN story vs glossed ============
Question asked: does each parable EMBED the text's operating
mechanic, or is it a high-level gloss? Verdict per work (E=embedded
performed / M=mixed / G=gloss-leaning):

E+ (mechanic performed): mpa gifts-sink/self-figure (the model) ·
spandasandoha waves-are-his-throb · isva-v2 fit-proves · pary-v3
stillness-spills · sakt sleep-climb-pour · ptvm fruit-before-tree ·
sivasutra-v3 events-perform-sūtras · samband false-joins-fall ·
phrdaya two-flows-scissor · spanda-v2 churn/unmade-eye · svab
blur→sharp + blade-in-knot · ghatakarpara dhvani-as-halted-rain +
pour-structure · bhairavastava bow-causes-every-zone · parp
proof-retirement · ajada-v2 flame-no-shadow · rpa never-heated-
steam.

M (mixed — gloss-MIDDLES, repairs proposed): kramastotra (beads-
middle = naming not doing; cut/loop carry it) · bodhapancadasika-v2
("knowing this is release: fence and gate one nature" = spoken
doctrine — rest is performed) · bhairavanukarana (boon-hand
cascade = told achievements, not acted) · pdva (outflank = "the
grant stood nowhere but in the flame" narrated-logic) ·
anubhavanivedana (strong, but grace-line "given not gotten"
asserted) · anuttarastika (rope-heap described-in-list).

G (gloss-leaning, on record): pancashloki (the traveler SAYS the
sense-free doctrine — show-don't-tell violation; door-brightens
re-angle already drafted) · siva450 (clause = essence-translation;
owner deferred) · s05-11 sketch-tier (hinge-dense).

## Repair proposals (bless to apply)
- bodha: "Knowing this is release: fence and gate one nature,
  bondage and freedom the same ground." → PERFORM: "He walks out
  through a gap — and finds the gap is where the fence and the
  road were always the same ground." (release as crossing, not
  statement)
- bhuv: the boon-cascade → make each boon an ACT on the scene:
  "the ground-claim in her step, the veil ripped by a breath, the
  rest commanded by a held-up palm" (verbs on stage).
- pdva: "the grant stood nowhere but in the flame" → SHOW: "the
  shadows all nodded — and the nod came from the light: where
  else could it have stood?" (the granting as the flame's own
  gesture).
- anubhavanivedana: "given and not gotten" → fold into the dew-
  image: "the dew was not asked for — it came before asking."
Owner: bless → I apply these four lines in their files.

## Repair correction note: the grant-line offender was AJADA-v2's
flame-hall sentence (not pdva's — pdva never had a grant scene).
Audit row updated mentally: M-list = kram, bodha, bhuv, ajada,
anubhavanivedana, anuttarastika. All four repairs APPLIED to files
2026-11-04.
