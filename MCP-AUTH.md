# MCP-AUTH.md — securing the shastra MCP (proposal, 2026-11-15)

*Status: PROPOSAL. Nothing here is enabled. Writes (`promote`, `assemble`,
`onboard`, `burn`, `recycle`, `queue_guard --fix`) are currently reachable by
anyone with the URL; reads are fully open (MCP-ESTATE §7). Traffic is
Cloudflare-proxied, which makes the cheapest fix an edge policy, not code.*

## 1. What we are protecting

| Class | Tools | Consequence if abused |
|---|---|---|
| Read | status, recon, lore, validate, gates, verify_core, health, query/bibliography tools | data exposure; cheap, low risk |
| Write (queue) | swarm_seed, swarm_decide, recycle, queue_guard --fix, review_sweep, beam_review | burns beam quota; corrupts queue |
| Write (canonical) | assemble, promote, onboard, burn, make_readable/--publish | writes `data/`, STATUS/REGISTRY/MANIFEST; a false `promote` fakes "gold" |
| Ops | supervise, swarm_workers | starts/stops workers |

The canonical-write and ops classes are the ones that must never be public.

## 2. Recommendation (do this first — no code)

**Cloudflare Access (Zero Trust) on `shastra.svatantrya.net`.** The tunnel is
already remote-managed by Cloudflare; Access is an edge policy, so the server
and FastMCP stay untouched.

```
1. Zero Trust → Access → Applications → Add application
   - Type: Self-hosted
   - Application domain: shastra.svatantrya.net
   - Session duration: 24h
2. Policy "operators": Action = Allow
   - Include: emails (owner + any ChatGPT service identity) OR Service Auth
3. For machine clients (ChatGPT connector, scripts):
   - Access → Service Auth → create a Service Token
     (CF-Access-Client-Id / CF-Access-Client-Secret)
   - Add a policy: Action = Service Auth, Include = that token
4. Verify:
   curl -s -o /dev/null -w '%{http_code}\n' https://shastra.svatantrya.net/mcp   # 302 to login when unauthenticated = good
```

ChatGPT custom connectors support headers, so the Service Token pair is added
as two request headers on the connector. Browser/manual clients hit the
Cloudflare login. This closes the write surface without a redeploy.

**Keep `mcp.svatantrya.net` (federation, read-only sheaf) open** unless its
tool set grows write capability.

## 3. Defense-in-depth (optional, code-gated OFF by default)

Add a bearer-token check to the HTTP transport only when
`SHASTRA_MCP_TOKEN` is set, so stdio/local agents are unaffected.

```python
# mcp_server.py — sketch; confirm FastMCP 3.4.7 middleware API before wiring
import os

TOKEN = os.environ.get("SHASTRA_MCP_TOKEN")

if TOKEN and "--serve-http" in sys.argv:
    # reject requests without  Authorization: Bearer <TOKEN>
    # FastMCP 3.x: register an ASGI/HTTP middleware that inspects the
    # Authorization header and returns 401 before dispatch.
    ...
```

Rules if implemented:
- Env-gated: absent env ⇒ current behaviour (no breakage).
- `--serve` (stdio) never requires the token.
- Log the rejection count, never the presented secret.
- Rotate via the oracle vault (`agent-vault`), same as the Go keys.

## 4. Network allowlist (belt and braces)

Cloudflare WAF rule on the hostname: allow only expected ASNs/regions or a
Cloudflare mTLS cert where the client supports it. Not a substitute for §2.

## 5. Rollout checklist

- [ ] Create the Access application + "operators" policy (§2.1–2.2)
- [ ] Create Service Token; add to the ChatGPT connector headers (§2.3)
- [ ] Verify 302-when-unauthenticated and 200-with-token (§2.4)
- [ ] Update `MCP-ESTATE.md §7` (drop "none yet") and `MCP.md` §8
- [ ] (Optional) env-gated bearer middleware (§3), tests in `tests/`
- [ ] Add a smoke assertion: unauthenticated write call is rejected

## 6. Owner decisions needed

1. Access allowlist = owner email only, or also a shared service identity?
2. Keep `mcp.svatantrya.net` federation open, or lock it too?
3. Implement §3 now, or edge-only (§2) is sufficient?
