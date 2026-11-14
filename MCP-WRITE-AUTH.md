# Shastra MCP write authorization

The Shastra HTTP MCP server keeps its read tools public and gates mutations at
the FastMCP tool-call middleware layer. The implementation targets the
repository's pinned `fastmcp==3.4.7` API.

The public read allowlist is in `mcp_server.py`. Every other known tool must be
in `OWNER_WRITE_TOOLS`, and then requires both:

- `SHASTRA_ENABLE_WRITES=1`
- an exact `Authorization: Bearer <token>` header, where the configured
  `SHASTRA_WRITE_BEARER` is at least 32 bytes

The bearer scheme is case-insensitive; the credential comparison uses
`hmac.compare_digest`. Unknown or future tools are denied even when a bearer is
present. A write call without an HTTP request (including unauthenticated stdio
calls) is denied. Mutations stay disabled when either environment variable is
unset, misconfigured, or too short. Do not enable them until the ChatGPT
connector is configured to send a dedicated owner credential over HTTPS.

Set credentials through the service's protected secret mechanism, not source
files or shell history. The request header is the supported authorization
channel; never pass the bearer as a tool argument. Reads remain available while
writes are disabled.

This layer does not mint translation PASS records, publish, or push. Promotion
remains disabled inside the MCP tool until a separate owner-approval mechanism
is implemented.
