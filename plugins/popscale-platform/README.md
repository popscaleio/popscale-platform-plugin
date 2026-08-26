# Popscale Platform Plugin

The Popscale Platform plugin gives Codex and Claude two deliberately separate
remote MCP connections:

| Server | Endpoint | Access | Purpose |
| --- | --- | --- | --- |
| `popscale-docs` | `https://docs.popscale.io/mcp` | Public, no authentication, read-only | Search and retrieve indexed public documentation |
| `popscale-platform` | `https://app.popscale.io/mcp/` | Popscale OAuth, company-scoped | Read customer data and perform authorized product actions |

The product server lets a company administrator find, create, and granularly
edit roleplays, coaching sessions, challenges, episodes, flashcards, and
existing Journey sections/items; trigger supported format-specific generation;
inspect and precisely edit Interview Studies; and create validated learning
journeys. It also compares company-scoped Journey participation and learning
outcomes with privacy-safe aggregates and bounded member or attempt drilldown.
Active edits, generation, publishing, and invitation delivery keep their
dedicated scopes, revision checks, and confirmation gates. The docs server
contains no product actions or customer data.

## What is in the package

- `.codex-plugin/plugin.json`: OpenAI/Codex distribution metadata; explicitly
  points to the shared MCP configuration and skills directory.
- `.claude-plugin/plugin.json`: Claude plugin identity and cache version; Claude
  discovers `.mcp.json` and `skills/` from the same plugin root.
- `.mcp.json`: both production remote-MCP connections.
- `assets/icon.png`: packaged Popscale symbol used by Codex plugin surfaces.
- `skills/route-popscale-requests/`: portable routing policy for public
  documentation versus authenticated product work.
- `skills/safe-interview-administration/`: company-scoped Interview authoring,
  distribution, evidence, and analysis workflow.
- `skills/safe-content-administration/`: company-scoped content discovery,
  stable-ID component editing, generation, history/freshness, and activation.
- `skills/company-usage-insights/`: read-only Journey participation and
  format-aware content outcomes with suppression and bounded drilldown.
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
- Route Interview Study reads, precise question edits, invitations, respondent
  links, transcripts, and analyses through `safe-interview-administration` and
  `popscale-platform`. Never send that data to the Docs MCP.
- Route existing company content discovery, focused root/component edits,
  targeted regeneration, languages, and activation through
  `safe-content-administration` and `popscale-platform`. Use
  `safe-journey-creation` for designing/executing a new Journey plan, not for a
  one-field edit to an existing Journey item.
- Route company, department, or role comparisons of Journey completion/mastery
  and content outcomes through `company-usage-insights` and
  `popscale-platform`. Keep suppressed aggregates, names, membership IDs, and
  attempt data away from the Docs MCP. Use `get_content_usage` only for
  dependency/impact review before a content mutation, not learner statistics.
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

Interview administration additionally requires the company `interviews` feature
and one or more dedicated scopes: `interview:read`, `interview:write`, and
`interview:distribute`. Study publication also requires `publish:write`.
Existing grants are not widened automatically; reconnect and review the new
consent scopes before using these tools.

Company-content inspection requires `content:read`; focused edits additionally
require `content:write`. Targeted regeneration also requires
`generation:write`, and activation additionally requires `publish:write`.
Existing grants are not silently widened after these scopes become available.
Reconnect and review consent before using a missing capability. Protected
mutations use the latest root `revision` as `expected_revision`; active edits
also require an explicit `confirm_active_edit` boundary.

Company usage and Journey insights require the dedicated read-only
`usage:read` scope. Existing grants must be reauthorized before it is available.
Aggregates can suppress small cohorts; member and attempt drilldowns remain
private company data even though email, transcripts, reflections, feedback
text, and raw result payloads are omitted.

The staging product endpoint is `https://staging.popscale.io/mcp/`; it is not
packaged and must only be used for testing.

## Documentation ownership

Public docs are maintained in the separate `popscale-docs` repository through
its normal branch-and-PR workflow. This plugin only reads the deployed index. Do
not add a docs write tool or update docs through the product MCP.

Public architecture, installation, security, release, and implementation status
are maintained in this repository's `docs/` directory.
