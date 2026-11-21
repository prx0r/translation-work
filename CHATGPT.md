# ChatGPT — start here (translation-work lane)

*You are looking at the translation factory. The thing you can actually USE
lives one repo over. Read this first, then go there.*

## 1. Use the live surface (svread), not this checkout

- Probes + report template: `https://svatantrya.net/CHATGPT-FEEDBACK.md`
  (repo: `prx0r/svread`, same filename). 5 read-only probes with ground truth.
- Claim pages (no JS): `https://svatantrya.net/claim/<work>/<target>/`
- Machine index: `https://svatantrya.net/llms.txt` · `ai-catalog.json`
- This lane's MCP (`translation__*` / `shastra__*`): `https://shastra.svatantrya.net/mcp`
- Federation (scholar evidence, formal traces): `https://mcp.svatantrya.net/mcp`

## 2. If you are reviewing THIS repo

- Live branch is `burn/muktabodha` (this checkout). `master` is ~1,000+ commits
  stale — never audit against it.
- Truth command: `python3 tools/verify_core.py` (per-work, full run times out).
- Gates: `python3 tools/validate_all.py --quick` (manifest-fresh FAILs come and
  go while the burn writes; regen with `python3 tools/manifest.py gen`).
- Acceptance pack (10 MCP read tests + report template): `CHATGPT-TEST.md`.
- Owner decisions (human-only calls): `OWNER-DECISIONS.md`.
- Do NOT call write tools (assemble/promote/seed/burn/recycle) unless explicitly
  authorized. BLOCKED with named `needs[]` is an honest state, not a failure.
