# Installation and verification

## Prerequisites

Public documentation has no account prerequisite. Authenticated product use
requires all of the following:

1. The company has the `mcp_access` feature enabled.
2. The user is active and has MCP access enabled.
3. The user's role grants the requested product scopes.
4. The user selects and approves the intended company during OAuth.

Interview administration also requires the company `interviews` feature and the
dedicated scopes appropriate to the task: `interview:read`, `interview:write`,
and `interview:distribute`. Publishing a Study additionally requires
`publish:write`. Existing grants are not automatically widened when these tools
become available.

Granular content inspection requires `content:read`; root/component mutation
additionally requires `content:write`; supported generation workflows require
`generation:read` for voice/status reads and `generation:write` to queue work;
and activation requires `publish:write`. Existing grants are not silently
widened. Content mutations use the current root `expected_revision`; active
field/component edits require explicit `confirm_active_edit` only when the live
tool schema exposes it. Archive instead uses its dedicated archive and optional
learner-impact confirmations.

Company usage and Journey insights require the dedicated read-only
`usage:read` scope. Existing grants are not silently widened when it becomes
available. Aggregates can suppress cohorts below a server-returned threshold;
that suppression must not be reconstructed through narrower filters or member
enumeration. The analytics tools accept stable IDs; resolving a title through
`search_company_content` additionally requires `content:read`. With a
`usage:read`-only grant, provide a Product MCP-returned ID/link instead of
guessing or silently widening consent.

Never paste a bearer token or add a static authorization header. Popscale uses
OAuth and stores the resulting host credential through the host's secure flow.

## Codex

```bash
codex plugin marketplace add popscaleio/popscale-platform-plugin
codex plugin add popscale-platform@popscale
codex plugin list
```

Start a new task after installation. If the product server needs authentication:

```bash
codex mcp login popscale-platform
```

Confirm the consent page names the intended company and the resource
`https://app.popscale.io/mcp/` before approving.

## Claude Code

Inside an interactive Claude Code session:

```text
/plugin marketplace add popscaleio/popscale-platform-plugin
/plugin install popscale-platform@popscale
/reload-plugins
/mcp
```

Authenticate `popscale-platform` from `/mcp`, or from the shell:

```bash
claude mcp login plugin:popscale-platform:popscale-platform
```

Claude Code may use an ephemeral loopback callback. The callback's scheme,
hostname, path, query, and fragment must remain unchanged through the Popscale
login and company-selection flow. Only the ephemeral port may vary where the
registered loopback policy permits it.

## Claude Cowork and Claude Desktop

1. Open **Cowork → Customize → Plugins**.
2. In Personal plugins, select **+ → Add marketplace**.
3. Add the GitHub repository `popscaleio/popscale-platform-plugin`.
4. Install **Popscale Platform**.
5. Enable the plugin connectors for the Cowork task.
6. Connect `popscale-platform`, select the intended company, review the scopes,
   and approve.

On Team and Enterprise plans, an Owner may need to approve the marketplace or
add the remote endpoints under Organization settings. Connector-only testing can
use two custom web connectors with the exact URLs from `.mcp.json`.

Cowork calls remote connectors from Anthropic's cloud rather than the local
computer. Local or VPN-only endpoints are not supported by this package.

## Read-only acceptance test

Run these prompts in a clean task or conversation.

### Public docs

```text
Use only popscale-docs. Search public Popscale documentation for
"Popscale MCP plugin", fetch the relevant canonical page, and report its status
metadata. Do not access or include customer data.
```

Expected: no OAuth, a canonical integration page, and explicit status metadata.

### Product identity and capabilities

```text
Use only popscale-platform. Call current_user and capabilities only. Do not call
any mutation or write tool. Report the authenticated company, role, MCP resource,
and whether both calls succeeded.
```

Expected: the company selected during OAuth and resource
`https://app.popscale.io/mcp/`.

### Interview read and consent

In a dedicated test company with Interviews enabled:

```text
Use only popscale-platform and safe-interview-administration. List Interview
Studies without making changes. Do not open an individual invitation or expose
respondent links or contact data.
```

Expected: the OAuth-bound company, bounded Study summaries, and no mutation or
respondent-link material. If `interview:read` was not granted, reconnect the
product connector and review the requested consent scopes. Accessing one
respondent link also requires `interview:distribute`.

### Company content read and consent

In a dedicated test company with representative content:

```text
Use only popscale-platform and safe-content-administration. Search company
content, then read one returned roleplay or episode and its freshness. Do not
make changes, generate content, open media upload URLs, or publish anything.
```

Expected: bounded company-scoped summaries, the current root revision and
editable/component metadata, and no mutation. If `content:read` was not granted,
reconnect and review consent. A later focused edit requires `content:write`;
generation and publication retain their additional scopes and confirmations.

### Company usage read and consent

In a dedicated test company with a Journey assigned across multiple sufficiently
large departments:

```text
Use only popscale-platform and company-usage-insights. Compare current Journey
completion by department. Do not list members or attempts and do not make any
change. Preserve every suppressed group and state the denominator.
```

Expected: bounded company-scoped aggregates, the effective company and current
metric definition, no mutation, and no reconstruction of suppressed cohorts. If
`usage:read` was not granted, reconnect and review consent. A later explicit
member drilldown can return names and stable membership IDs, but not email,
transcripts, reflections, feedback text, or raw result payloads.

### Persistence

Close the host, start a new task, and repeat the product read test. The stored
session should be reused without a new login unless it was revoked or expired.

## Troubleshooting

- **Neither server appears:** update the marketplace, reinstall the plugin, and
  verify the host loaded `.mcp.json` from the plugin root.
- **Docs opens OAuth:** remove any duplicate manual docs connector and confirm
  the packaged docs entry contains only `type` and `url`.
- **Repeated anonymous JSON errors:** verify the host opened the interactive
  Popscale authorization route and preserved its original `redirect_uri`.
- **Callback page cannot connect:** follow the host instruction to paste the
  complete callback URL; do not rewrite `localhost` to `127.0.0.1` or vice versa.
- **Wrong company:** stop product reads and writes, explicitly confirm link
  creation, then call `request_company_switch` with `current_grant_id` from the
  latest `current_user` result and `confirm_switch=true`. Open the returned
  `switch_url`, select and confirm the intended membership in Popscale, then
  verify it with `current_user` through the same MCP connection. Never pass the
  target company to the tool. If `replay_ignored=true`, refresh `current_user`;
  if the link expired or was used, confirm again before creating another.
- **Interview tools or links are unavailable:** reconnect the product connector
  and review `interview:read`, `interview:write`, and
  `interview:distribute`. Do not manually paste tokens or assume a read scope
  authorizes respondent-link access.
- **Content tools are unavailable:** reconnect the product connector and review
  `content:read`, `content:write`, `generation:read`, `generation:write`, and
  `publish:write` for the requested operation. Do not paste tokens, guess a
  company ID, queue generation that cannot be monitored, or treat a read grant
  as mutation authority.
- **Usage insights are unavailable:** reconnect the product connector and
  approve `usage:read`. Do not substitute Journey/content write scopes, public
  Docs, generic REST, UI scraping, or broad member enumeration. If only
  title-based discovery fails, provide a Product MCP-returned ID/link or approve
  optional `content:read` for `search_company_content`.
- **App UI does not render:** continue from structured MCP results. UI rendering
  is optional and does not change the product authorization boundary.
