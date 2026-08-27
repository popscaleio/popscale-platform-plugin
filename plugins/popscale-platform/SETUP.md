---
name: setup
description: Install and verify the public Popscale Docs MCP and the authenticated Popscale Platform MCP in OpenAI or Claude hosts.
---

# Set Up Popscale Platform

The plugin packages both remote HTTP MCP servers from its root `.mcp.json`:

```text
popscale-docs     https://docs.popscale.io/mcp      No auth; public read-only docs
popscale-platform https://app.popscale.io/mcp/      OAuth; company-scoped product
```

Keep the product URL's trailing slash and keep the docs URL without one. Do not
add headers, environment variables, API keys, or bearer tokens to the docs
server. Do not ask a customer to create or paste a product bearer token.

## Install the package

For Codex, install the public repository marketplace:

```bash
codex plugin marketplace add popscaleio/popscale-platform-plugin
codex plugin add popscale-platform@popscale
```

The Codex manifest points to `./.mcp.json` and `./skills/`, so one plugin install
supplies both servers and the routing, Interview-administration,
content-administration, company-usage-insights, and Journey skills. Start a new
task after installation.

That one-install contract applies to repository/local marketplace distribution.
OpenAI's public submission form accepts one primary MCP server URL, and uploaded
skills may declare additional MCP dependencies. The intended public package
submits **Popscale Platform** as its primary URL and keeps **Popscale Docs** in
the routing skill dependency metadata. Validate a clean directory install before
release. If OpenAI does not provision the dependency, connect a separate
**Popscale Docs** entry as the documented fallback; never claim the routing
workflow unless both servers are present.

For Claude Code, add and install the public repository marketplace from an
interactive session:

```text
/plugin marketplace add popscaleio/popscale-platform-plugin
/plugin install popscale-platform@popscale
/reload-plugins
/mcp
```

Claude discovers `.mcp.json` and `skills/` at the plugin root. Run
`/reload-plugins` or restart Claude Code after an update so changed MCP
connections are reloaded.

Claude.ai, Desktop, and Cowork users can add the GitHub marketplace and install
the complete package from **Customize → Plugins**. For connector-only testing,
add each endpoint as its own custom connector; never label the public docs
connector as the authenticated product connector.

## Authenticate product access

The first `popscale-platform` use opens Popscale authorization:

1. Sign in to Popscale in the browser.
2. Select the intended company and approve the requested scopes.
3. After redirecting to the host, call `current_user` and `capabilities`.
4. Confirm the returned company is the company the user intended to use.
5. If authorization is unavailable, ask a Popscale company admin to enable the
   company feature and the user's MCP access.

Interview administration uses the dedicated `interview:read`,
`interview:write`, and `interview:distribute` scopes. Publishing an Interview
Study also requires `publish:write`. Existing OAuth grants are not silently
widened after a plugin or server update. Reconnect `popscale-platform`, review
the consent page, and approve only the scopes needed for the requested work. A
read-only user can list PII-safe invitation summaries, but individual respondent
links require both `interview:read` and `interview:distribute`.

Granular company-content reads use `content:read`. Creating or editing roots and
stable-ID components additionally requires `content:write`; supported
generation requires `generation:read` for voice/status reads and
`generation:write` to queue work; activation requires `publish:write`. Existing
grants are not silently widened for these scopes either. Protected content
mutations pass the latest root revision as `expected_revision`. Active
field/component edits require `confirm_active_edit` only when exposed by the
live schema; archive uses its separate archive and learner-impact confirmations.

Company usage and Journey insights require the dedicated read-only
`usage:read` scope. Existing grants are not silently widened for it. Reconnect
`popscale-platform` and approve that scope before comparing Journey completion,
content outcomes, or bounded member/attempt detail. Small-cohort suppression is
authoritative and must not be reconstructed through narrower filters. Analytics
tools accept stable IDs; title resolution through `search_company_content`
additionally requires `content:read`. With a usage-only grant, provide an ID or
link already returned by the Product MCP rather than guessing.

`popscale-docs` must work without this flow and must never receive the product
OAuth session or customer data.

## Verify both servers

1. Ask for a public docs overview. Confirm the host uses `popscale-docs` without
   opening OAuth.
2. Search for “Popscale MCP plugin,” retrieve the returned canonical page with
   `get_pages`, and confirm the response includes document `status` metadata.
3. Ask which company is connected. Confirm the host uses `popscale-platform`,
   opens OAuth when needed, and returns the intended company.
4. Ask a mixed question such as “Explain journeys, then list ours.” Confirm the
   host clearly separates the public explanation from the authenticated lookup.
5. In a company with Interviews enabled, ask to list Interview Studies. Confirm
   the host uses `safe-interview-administration` and `popscale-platform`, makes
   no mutation, and exposes no respondent link or raw contact data.
6. Ask to search company content and inspect one returned object and its
   freshness without mutation. Confirm the host uses
   `safe-content-administration`, reports bounded results and the current root
   revision, and stays in the OAuth-selected company.
7. Ask to compare Journey completion by department without member drilldown.
   Confirm the host uses `company-usage-insights`, requires `usage:read`, and
   preserves any suppressed groups.

## Troubleshoot

- If neither server appears, reinstall/reload the plugin and verify the shared
  `.mcp.json` contains both named entries.
- If docs prompts open OAuth, confirm they route to `popscale-docs` and that its
  configuration contains only `type` and `url`.
- If a docs page is missing, run `get_docs_overview` or `search_docs` before
  `get_pages`; do not invent or guess a path.
- If product tools return an authorization challenge, reconnect
  `popscale-platform`; do not copy its credentials to `popscale-docs`.
- If Interview tools or respondent-link access are missing after an update,
  reconnect `popscale-platform` and review the dedicated Interview scopes. Do
  not paste a bearer token or treat `interview:read` as distribution authority.
- If content search, focused editing, generation, or activation is unavailable,
  reconnect `popscale-platform` and review `content:read`, `content:write`,
  `generation:read`, `generation:write`, and `publish:write` as appropriate. Do
  not broaden a grant beyond the requested operation or queue generation that
  the grant cannot monitor.
- If usage insights are unavailable, reconnect `popscale-platform` and approve
  `usage:read`. Do not use a write scope, public Docs, generic REST, or member
  enumeration to substitute for the missing analytics capability. For a
  title-only request, approve optional `content:read` or provide a Product
  MCP-returned ID/link.
- If the MCP App does not render, continue from the product server's structured
  result. App support is not required for safe product actions.

Public docs are maintained in the separate `popscale-docs` repository through a
branch and PR. This plugin has no documentation write tool. To disconnect product
access completely, remove the product connector in the host and revoke the
corresponding connected MCP session in Popscale.
