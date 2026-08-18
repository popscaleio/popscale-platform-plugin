# Popscale Platform Plugin

The Popscale Platform plugin gives Codex and Claude two deliberately separate
remote MCP connections:

| Server | Endpoint | Access | Purpose |
| --- | --- | --- | --- |
| `popscale-docs` | `https://docs.popscale.io/mcp` | Public, no authentication, read-only | Search and retrieve indexed public documentation |
| `popscale-platform` | `https://app.popscale.io/mcp/` | Popscale OAuth, company-scoped | Read customer data and perform authorized product actions |

The product server lets a company administrator create a learning-journey plan
from approved knowledge, validate every generated item, review the plan in the
Journey Review MCP App, and explicitly execute or publish it. The docs server
contains no product actions or customer data.

## What is in the package

- `.codex-plugin/plugin.json`: OpenAI/Codex distribution metadata; explicitly
  points to the shared MCP configuration and skills directory.
- `.claude-plugin/plugin.json`: Claude plugin identity and cache version; Claude
  discovers `.mcp.json` and `skills/` from the same plugin root.
- `.mcp.json`: both production remote-MCP connections.
- `skills/route-popscale-requests/`: portable routing policy for public
  documentation versus authenticated product work.
- `skills/safe-journey-creation/`: authenticated journey workflow used by both
  hosts.
- `SETUP.md`: installation, authentication, verification, and troubleshooting.

The repository-level `.claude-plugin/marketplace.json` and
`.agents/plugins/marketplace.json` expose the same package as
`popscale-platform@popscale` in Claude and Codex.

Repository/local marketplace installs in Codex and Claude load this shared
package and therefore receive both MCP servers. OpenAI's public submission form
accepts one primary MCP server URL, while an uploaded skill may declare extra MCP
dependencies that make their tools available. The intended public submission
uses Popscale Platform as the primary URL and the routing skill's `popscale-docs`
dependency. A clean directory install must prove both connections are present;
if the portal does not retain that dependency, publish/connect Popscale Docs
separately before claiming the dual-server workflow.

The MCP servers and MCP App are hosted by Popscale. This package contains no
customer credential, token, tenant identifier, or embedded API implementation.

## Routing and trust boundary

- Send general product, setup, and public documentation questions to
  `popscale-docs`. Start with `get_docs_overview` or `search_docs`, then use
  `get_pages` for returned canonical paths.
- Respect page metadata. Describe `draft` as draft and unverified, and `review`
  as under review; neither is confirmed product behavior.
- Send customer records, selected-company state, approved knowledge, and all
  actions to `popscale-platform`. It requires OAuth and derives company scope
  from the authenticated session.
- Never send customer data or credentials to the public server, and never treat
  public docs as authorization or approved company knowledge for a write.
- The Journey Review App is an optional presentation layer. Hosts without App
  support receive the same structured results and can complete the product flow
  with ordinary authenticated tool calls.

## Customer prerequisites

Public documentation requires only network access to `https://docs.popscale.io`.
Authenticated product work additionally requires:

1. The customer's company has the `mcp_access` feature enabled.
2. The user is an active `company_admin` and has MCP access enabled.
3. The user completes Popscale OAuth and selects the intended company.

The staging product endpoint is `https://staging.popscale.io/mcp/`; it is not
packaged and must only be used for testing.

## Documentation ownership

Public docs are maintained in the separate `popscale-docs` repository through
its normal branch-and-PR workflow. This plugin only reads the deployed index. Do
not add a docs write tool or update docs through the product MCP.

Public architecture, installation, security, release, and implementation status
are maintained in this repository's `docs/` directory.
