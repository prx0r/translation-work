# WHERE-WE-ARE — 2026-11-14 (read this first if you're picking this up)

*One-page orientation for any agent landing in `/root/translation-work`.
Machine-proposed throughout. Nothing here is human-signed. The law is
`skills/crystal-ipvv/SKILL.md` + `skills/largetext/SKILL.md`; this file is
just the map so you're not lost.*

## The goal (owner, 2026-11-14)

> **Get the whole thing onto ChatGPT as MCP connectors / plugins.**

Translation quality is the product; the *distribution* target is the MCP
estate (below). Both keep running: the autonomy loop drafts; the MCP serves
it to ChatGPT.

## Two eras, in order

1. **Trika era — DONE.** `REGISTRY.json` = 95/95 gold (Tantraloka 37/37,
   Tantrasara 22/22, Gita 18/18, MVV, SSV, Tattvasandoha mūla, stotras,
   prakaraṇas). Machine-proposed, human review pending. This registry does
   **not** include Muktabodha burn works.
2. **Muktabodha burn era — ACTIVE.** The swarm is chewing through the
   Muktabodha corpus shortest-first (see `process/beam/ranked_burn.json`).
   Burn works are tracked in their **own** `STATUS.json`, not `REGISTRY.json`.

## The MCP estate (the ChatGPT surface) — state 2026-11-14

| Endpoint | Tools | State | ChatGPT-ready? |
|---|---|---|---|
| `https://shastra.svatantrya.net/mcp` | **31** | live, HTTP 200 | ✅ paste as connector |
| `https://book.svatantrya.net/mcp` | 22 | live, HTTP 200 | ✅ paste as connector |
| `https://video.svatantrya.net/mcp` | 18 | **401 Cloudflare Access** | ⚠️ needs bypass/OAuth (§MCP-ESTATE 7) |
| `https://patala.svatantrya.net` (REST) | 46 routes | live, 200 | ✅ plain REST |

Local: `http://127.0.0.1:8930/mcp` (tw-mcp), `…:8950/mcp` (book),
`…:8951/mcp` (video), `…:8802` (patala REST).

Systemd units (all `active`, boot-enabled): `tw-mcp`, `bookfactory-mcp`,
`videofactory-mcp`, `openpatala-api`, `svatantrya-tunnel`, `tal-campaign`.
Full detail: `MCP-ESTATE.md`. Tool manual: `MCP.md`. Base layer:
`BIBLIOGRAPHY.md`.

**To connect in ChatGPT:** Settings → Connectors → Add custom connector →
paste the URL. `shastra__*` and `bookfactory__*` tools appear namespaced.
The only gap is `video` (Access-gated).

## The autonomy loop (who is drafting right now)

`systemd tal-campaign` → `tools/harness.sh` is the **single** supervisor
(health-gates 429s with a 30-min pause; staggers workers w1→w2→w3, cap 3).
**Never start `continue.sh`/`ralph.sh`/`watchdog.sh` by hand alongside it.**
Workers draft into `process/beam/runs/`; `tal_stage`/`tw-assemble` assemble;
`ralph` commits + pushes `burn/muktabodha` on green.

Check it:
```bash
systemctl is-active tal-campaign tw-mcp
python3 tools/beam_swarm.py status          # or shastra.swarm_status
tail -n 30 process/beam/harness.log
```

## Current queue + progress (2026-11-14 ~04:45 UTC)

- Queue: `tal_triple` pending 6835 / done 2936 / failed 808 / superseded 716 /
  claimed 3; `tal_gloss` done 3351; `tal_cm` done 1941; `tal_am` done 502;
  `tal_brief` approved 96.
- Workers alive: 3 (holding `mukta-m00124` p43/p48/p49 triples).
- Gates: `validate_all --quick` 0 failures; `check.py` **CANONICAL 0 failures**
  (after this session's disposition fix — see below).

### Burn fronts (assembled / built)
| front | songs built | gold | notes |
|---|---|---|---|
| `kularnavatantra` | 77/83 | 76 | 6 songs unbuilt (p11,p49,p62,p64,p69,p77) blocked by failed-at-max triples; 1 blocked song `kul-p39` (ALIGN_NODISP v967) |
| `mukta-m00027` (kjn) | 26 | 25 | 1 blocked song |
| `svacchandatantra` | 18 | 0 | all 18 need assessor (T1 non-source token / paren truncation — BUGS #12) |
| `netratantra` | 5 | 0 | all 5 need assessor (same re-intake class) |
| `mukta-m00124` (kāmikāgama) | building | — | 5140 v / 206 songs, pass-1 bulk wave, very early (~24 t1) |

## What changed THIS session (2026-11-14)

1. **`check.py` NOT CANONICAL (3 failures) → CANONICAL 0 failures.**
   `proof-s01/s02/s03` were `BLOCKED` on `ALIGN_NODISP` (sivastotravali
   vv17/18/20, s02v20, s03v10/14/17/18). Verified by hand: **sandhi-only**
   decomposition differences (T1 splits sandhi, source is joined; word order
   identical, same words — e.g. `-aḥ>-o`, `-aḥa>o'`, `ā>aa`, `iti>ity`,
   `kah api>ko'pi`, `t>d/c/n`, `ś>s/cch`). Recorded honest per-verse
   dispositions in `tools/proof-disp.json` (same standard as existing
   s04/s05). All three now PASS.
2. **Fixed a stale-brief bug in `mcp_server.py`.** `_lore_path()` only knew the
   Tantraloka `tal-aNN.md` convention, so every burn front (`mukta-m00124`,
   `kularnavatantra`, …) returned `brief: null` **even though the brief exists
   on disk**. Now resolves `lore/<work>.md` first, then `tal-aNN.md`; the
   `lore` tool also lists all `*.md` briefs. `recon`/`status` now report the
   real brief path.
3. **Tool-count truth:** live server = **31** tools. Docs said 25/29/19;
   reconciled `MCP.md`, `MCP-ESTATE.md`, `AGENTS.md`. Also added the four
   missing names (`recycle`, `queue_guard`, `progress`, `watchdog`) to the
   `TOOLS` list so `--list` matches the live surface.
4. **MCP estate verified live** (this session): shastra 200, book 200,
   patala REST 200, video 401 (Access-gated — documented).
5. **No queue surgery needed:** `queue_guard` clean (0 dup / 0 overlap).
   `recycle_failed --dry` = 355 candidates → 0 halved (their ranges are
   already covered by live pending work), so **not applied**.

## Honest blockers (not machine-doable here)

- **`video` MCP is Cloudflare-Access-gated (401).** Needs an Access
  bypass/service-token policy for `/mcp`, or the OAuth flow. Owner decision.
- **`kul-p39`, kjn blocked song, `svacchandatantra` (18), `netratantra` (5):**
  content/intake class — need assessor hand-fix or re-intake (BUGS #12), not
  auto-retry. Never vote-promote (mistakes #20).
- **6 unbuilt kularnava songs** are blocked by failed-at-max triples; retest
  protocol (`beam_swarm.py retest <id>`) or hand-draft, per assessor.
- **Trika human review** + first-verse L4 voice verdicts remain owner actions.

## If you're the next agent — start here

```bash
cd /root/translation-work
python3 check.py | tail -3                 # expect CANONICAL: 0 failures
shastra.progress (or tools/watchdog_progress.py)   # health line
shastra.swarm_status                       # queue
shastra.recon {work}                       # before ANY seeding
shastra.lore {work}                        # brief must exist before seeding
```
Never push canon by hand; the loop pushes `burn/muktabodha` on green. This
branch/PR is a **snapshot for other agents**, not a canon release.
