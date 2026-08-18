# Installation and verification

## Prerequisites

Public documentation has no account prerequisite. Authenticated product use
requires all of the following:

1. The company has the `mcp_access` feature enabled.
2. The user is active and has MCP access enabled.
3. The user's role grants the requested product scopes.
4. The user selects and approves the intended company during OAuth.

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
claude mcp login popscale-platform
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
- **Wrong company:** revoke or clear the product connector authentication, sign
  into Popscale, select the correct company, and authenticate again.
- **App UI does not render:** continue from structured MCP results. UI rendering
  is optional and does not change the product authorization boundary.
