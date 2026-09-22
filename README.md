# Popscale Platform Plugin

The official Popscale plugin for Codex, Claude Code, Claude Desktop, and Claude
Cowork. One install provides public Popscale documentation and authenticated,
company-scoped Interview, granular learning-content, Journey, and privacy-safe
usage-insights workflows while keeping those trust boundaries separate.

## Included connections

| Server | Endpoint | Authentication | Purpose |
| --- | --- | --- | --- |
| `popscale-docs` | `https://docs.popscale.io/mcp` | None | Public, read-only documentation |
| `popscale-platform` | `https://app.popscale.io/mcp/` | Popscale OAuth | Company-scoped product data and actions |

The docs server never receives customer data, credentials, or product OAuth.
The product server derives company scope from the authenticated Popscale
session. Public documentation with `draft` or `review` status is not treated as
verified product behavior.

## Install in Codex

```bash
codex plugin marketplace add popscaleio/popscale-platform-plugin
codex plugin add popscale-platform@popscale
```

Start a new Codex task after installation. Authenticate `popscale-platform`
when prompted; `popscale-docs` must work without authentication.

## Install in Claude Code

Inside Claude Code:

```text
/plugin marketplace add popscaleio/popscale-platform-plugin
/plugin install popscale-platform@popscale
/reload-plugins
```

Run `/mcp` to verify both servers and authenticate `popscale-platform`.

## Install in Claude Cowork

Open **Cowork → Customize → Plugins**. Add the GitHub marketplace
`popscaleio/popscale-platform-plugin`, install **Popscale Platform**, and enable
its connectors in the task. If an organization policy does not yet allow the
marketplace, an Owner can add the two endpoints as custom web connectors under
Organization settings instead.

Cowork connects to remote MCP servers from Anthropic's cloud. Both packaged
endpoints are public HTTPS services; only the product endpoint requires OAuth.

## Verify a clean install

1. Ask the plugin to search public docs for `Popscale MCP plugin` and retrieve
   the canonical page. It must use `popscale-docs` without opening OAuth and
   report the page status.
2. Ask it to call only `current_user` and `capabilities`. It must use
   `popscale-platform`, authenticate when needed, and report the intended
   company and role.
3. If the test company has Interviews enabled, ask it to list Interview Studies
   without making changes. It must use `popscale-platform` and expose no
   respondent link or raw contact data.
4. Ask it to search company content and read one returned object's status,
   revision, editable fields, and freshness without making changes. It must use
   `safe-content-administration` and remain inside the OAuth-selected company.
5. Ask it to compare Journey completion by department without member drilldown.
   It must use `company-usage-insights`, preserve suppressed cohorts, and make
   no write.
6. Restart the host and repeat the product read test. It should reuse the saved
   OAuth session.
7. Do not test writes in a customer company. Use a dedicated test company and
   explicit human confirmation for mutation or publication tests.

See [installation](docs/INSTALLATION.md), the
[security model](docs/SECURITY_MODEL.md), and the
[release runbook](docs/RELEASE.md) for complete guidance.

## Repository layout

```text
.agents/plugins/marketplace.json       Codex marketplace
.claude-plugin/marketplace.json        Claude marketplace
plugins/popscale-platform/             Shared plugin package
  .codex-plugin/plugin.json            Codex manifest
  .claude-plugin/plugin.json           Claude manifest
  .mcp.json                            Both remote MCP servers
  assets/icon.png                      Packaged Popscale symbol
  skills/                              Portable routing, Interview, content, usage, and Journey workflows
```

This repository contains distribution metadata and agent workflows only. The
MCP services and Popscale application are maintained in separate repositories.
Public documentation is maintained through PRs in the separate
`popscale-docs` repository; this plugin contains no documentation write tool.

## Development

```bash
python3 -m unittest discover -s plugins/popscale-platform/tests -p 'test_*.py' -v
python3 scripts/validate_release.py
python3 scripts/live_docs_smoke.py
```

No database migrations or application deployment are involved in plugin
releases.

## Product feedback and page navigation

The `safe-product-feedback` workflow submits bugs, ideas and improvements and
reads the caller's own feedback with optional `admin:write` / `admin:read` scopes.
Conversation sharing is explicit, bounded and reviewed through authenticated
ProductAction approval. External chat history cannot be retrieved later.

Platform review requires optional `feedback:review`, an eligible company admin,
active superuser status and explicitly assigned review permission. Existing
connections must reauthorize for this scope; it is not a default for all users.
A missing tool or denied request does not mean there are no reports.

Navigation returns verified typed destinations. A capable host resolves them to
trusted links; otherwise the assistant describes the page without claiming it
opened. Host progress UI varies; a completed submission tool does not mean its
background job is finished. Compatible backend discovery must precede publication
of version 1.4.0; first-party sessions must be restarted to pick up new profiles.
