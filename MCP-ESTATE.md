# MCP-ESTATE.md — the whole agent surface (MCP servers + REST), durable & public

*Last verified: 2026-11-12. Everything below is served by enabled systemd units
behind one Cloudflare named tunnel; it survives reboots. ChatGPT connects to any
of these as a custom connector.*

---

## 1. The four public endpoints

| Endpoint | Kind | Backend (systemd) | Local port | Tools / routes |
|---|---|---|---|---|
| **https://mcp.svatantrya.net/mcp** | MCP (Streamable HTTP) | `tw-mcp.service` | 8930 | **25** — translation/shastra + full bibliography |
| **https://book.svatantrya.net/mcp** | MCP (Streamable HTTP) | `bookfactory-mcp.service` | 8950 | **22** — book factory |
| **https://video.svatantrya.net/mcp** | MCP (Streamable HTTP) | `videofactory-mcp.service` | 8951 | **18** — video factory |
| **https://patala.svatantrya.net** | REST (read-only) | `openpatala-api.service` | 8802 | **46** `/v1/*` + `/health` + `/openapi.json` |

In ChatGPT: **Settings → Connectors → Add custom connector →** paste each MCP
URL. Tools appear namespaced per server (`shastra__*`, `bookfactory__*`,
`video__*`). The REST endpoint is plain HTTP/JSON for any client.

---

## 2. Serving chain (one tunnel, many hostnames)

```
ChatGPT / agents ──HTTPS──▶ *.svatantrya.net   (Cloudflare, proxied)
                                  │  CNAME → 2131eb3e-….cfargotunnel.com
                                  ▼
              svatantrya-tunnel.service  (cloudflared, named tunnel 2131eb3e)
                                  │  ingress (REMOTE-managed config):
                                  │    mcp.svatantrya.net   → 127.0.0.1:8930
                                  │    book.svatantrya.net  → 127.0.0.1:8950
                                  │    video.svatantrya.net → 127.0.0.1:8951
                                  │    patala.svatantrya.net→ 127.0.0.1:8802
                                  │    pow.systems / proofdesk / longhaul → …
                                  ▼
   tw-mcp / bookfactory-mcp / videofactory-mcp / openpatala-api   (systemd)
```

**Important:** tunnel `2131eb3e` uses a **remotely-managed (dashboard) config**.
Editing `/root/.cloudflared/config.yml` does nothing at runtime — update ingress
through the Cloudflare API instead (§6). The local `config.yml` is a fallback
only.

---

## 3. Units (all enabled at boot, Restart=always)

| Unit | Command | Notes |
|---|---|---|
| `tw-mcp.service` | `mcp_server.py --serve-http --port 8930` | translation/shastra |
| `bookfactory-mcp.service` | `bf_mcp/server.py --serve-http --port 8950` | book factory |
| `videofactory-mcp.service` | `vf_mcp_server.py --serve-http --port 8951` | `VF_MCP_ALLOW_WRITE=0` (gated writes) |
| `openpatala-api.service` | `uvicorn patala.api:app --port 8802` | Postgres-backed REST |
| `svatantrya-tunnel.service` | `cloudflared tunnel --config … run` | the site tunnel |

Check/repair:
```bash
systemctl status tw-mcp bookfactory-mcp videofactory-mcp openpatala-api svatantrya-tunnel
systemctl restart tw-mcp            # after editing mcp_server.py
journalctl -u svatantrya-tunnel -n 30   # tunnel connection + loaded config
```

---

## 4. Tool catalogs

### 4.1 `mcp.svatantrya.net` — shastra / translation (25)
Bibliography base layer: `bibliography`, `priority`, `schema`, `stats`, `works`,
`editions`, `links`, `availability`.
Translation loop: `status`, `recon`, `lore`, `concepts`, `skill`,
`swarm_seed`, `swarm_review`, `swarm_decide`, `assemble`, `promote`, `validate`,
`gates`, `swarm_status`, `swarm_workers`, `supervise`, `review_sweep`,
`beam_review`.
Full detail: `translation-work/BIBLIOGRAPHY.md` + `MCP.md`.

### 4.2 `book.svatantrya.net` — book factory (22)
Read: `factory_overview`, `list_lanes`, `check_lane`, `next_actions`,
`read_thesis`, `list_specs`, `read_template`, `read_entries`, `read_book`,
`read_decisions`, `read_docs`, `read_file`, `list_dir`, `inspect_verse`,
`read_rule_boxes`.
Write (gated by factory.py's own rules): `decide`, `new_book`, `stage`,
`audio_plan`, `epub`, `package`, `quote_preview`.
Source: `/root/bookfactory/bf_mcp/server.py`; CLI: `/root/bookfactory/factory.py`.

### 4.3 `video.svatantrya.net` — video factory (18)
Read/gate: `vf_projects`, `vf_status`, `vf_units`, `vf_unit`, `vf_issues`,
`vf_gate`, `vf_logs`, `vf_finals`, `vf_skills`, `vf_skill`, `vf_triage`,
`vf_skill_propose`, `vf_check`, `vf_tests`.
Gated (refuse unless `VF_MCP_ALLOW_WRITE=1`; publish is human-only): `vf_launch`,
`vf_queue`, `vf_publish`, `vf_pack`.
Source: `/root/videofactory/vf_mcp_server.py`.

### 4.4 `patala.svatantrya.net` — OpenPatala REST (46)
Identity: `/v1/resolve`, `/v1/works`, `/v1/works/{id}`, `/v1/works/{id}/completeness`,
`/v1/graph/{id}`, `/v1/bundle/{id}`.
Translations: `/v1/translations`, `/v1/works/{id}/translations`,
`/v1/translation-availability`, `/v1/passages/{id}/translations`,
`/v1/frontier/translations`.
Text: `/v1/passages`, `/v1/passages/{id}/alignments`, `/v1/editions`,
`/v1/etexts/{id}/content`, `/v1/witnesses`, `/v1/surrogates`,
`/v1/etexts`, `/v1/observations`, `/v1/assertions`.
Meta: `/v1/stats`, `/v1/traditions`, `/v1/people`, `/v1/institutions`,
`/v1/providers/*`, `/v1/search`, `/v1/autocomplete`, `/v1/changes`,
`/v1/snapshots`, `/health`.
Live counts (2026-11-12): 2051 works · 596 editions · 451 translations · 743 availability.

---

## 5. Using it in the work

**Translation priority → translation:**
```
shastra.priority → shastra.bibliography{editions/links} → shastra.recon
   → shastra.swarm_seed → [beam drafts] → swarm_review → swarm_decide
   → assemble → validate → promote → gates
```
Bind outputs to canonical ids with `GET patala.svatantrya.net/v1/resolve?q=…`
then `/v1/works/{id}/translations` to avoid re-translating.

**Book production:** `bookfactory.list_lanes` → `read_thesis`/`read_decisions`
→ `new_book`/`decide`/`stage`/`audio_plan`/`epub`/`package` (all gated by the
factory; PDF build is last).

**Video production:** `vf_projects` → `vf_status`/`vf_units`/`vf_triage` →
`vf_gate`/`vf_check`; renders/publish stay on-box (gated).

---

## 6. Add another MCP server (recipe)

1. **Serve it over HTTP** — FastMCP: `mcp.run(transport="http", host="127.0.0.1", port=PORT, path="/mcp")`.
2. **systemd unit** — `Type=simple`, `Restart=always`, `WantedBy=multi-user.target`;
   `systemctl enable --now <unit>`.
3. **Tunnel ingress (remote config)** — PUT the full ingress list:
```bash
set -a; . /root/.r2-env; set +a
ACC=954612afb5a97bb15dddcdc70176813d
TID=2131eb3e-f087-44c2-bde5-fdc32d9f98bb
curl -sS -X PUT "https://api.cloudflare.com/client/v4/accounts/$ACC/cfd_tunnel/$TID/configurations" \
  -H "Authorization: Bearer $CF_API_TOKEN" -H 'Content-Type: application/json' \
  --data '{"config":{"ingress":[ /* …keep existing… */ {"service":"http://127.0.0.1:PORT","hostname":"NEW.svatantrya.net"}, {"service":"http_status:404"}]}}'
```
4. **DNS** — CNAME `NEW.svatantrya.net → 2131eb3e-f087-44c2-bde5-fdc32d9f98bb.cfargotunnel.com` (proxied), via
   `POST /zones/{zone}/dns_records` (zone id `21941f4dbedd8922caa1293bf996afaf`).
5. **Verify** — `initialize → tools/list` over `https://NEW.svatantrya.net/mcp` (HTTP 200).

---

## 7. Auth, safety, caveats

- **Auth:** none yet (open MCP reads; write tools are gated by the factories).
  Before wide sharing: Cloudflare Access or a bearer token on the hostnames.
- **No auto-publish/sign/ship:** `promote` is machine-proposed; video publish/launch
  refuse over MCP unless `VF_MCP_ALLOW_WRITE=1` (deliberately). Human disposes.
- **WAF:** Cloudflare edge-filters the bare `Python-urllib` default UA (403).
  ChatGPT, `requests`, `httpx`, node-fetch, okhttp, Go, Java all pass. Set any
  non-default `User-Agent` if using stdlib.
- **Data:** the translation MCP reads the final Muktabodha baseline (2026-11-12);
  the REST reads the openpatala Postgres graph (`dbname=openpatala`).

---

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| public `/mcp` 404 | ingress missing in **remote** tunnel config | §6 step 3 (not the local yml) |
| public 403 for a script | `Python-urllib` UA filtered | set a UA |
| 502/timeout | tunnel down or origin port not listening | `systemctl status svatantrya-tunnel <mcp-unit>` |
| tools list missing a server | unit crashed | `journalctl -u <unit> -n 50` |
| REST 500 | Postgres down | `systemctl status postgresql openpatala-api` |
