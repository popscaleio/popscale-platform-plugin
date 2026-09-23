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

## Updating and releasing the plugin

Merging a PR into `main` runs package validation; it does **not** create a
release or update installed copies. The release workflow runs only when a
`vX.Y.Z` Git tag is pushed. For example, merging a change while the manifests
still say `1.3.1` leaves the published release at `v1.3.1`.

To publish a new version:

1. Choose the next version and update both plugin manifests
   (`plugins/popscale-platform/.codex-plugin/plugin.json` and
   `plugins/popscale-platform/.claude-plugin/plugin.json`), plus
   `.claude-plugin/marketplace.json`. Keep their versions equal. Update the
   expected version in `scripts/validate_release.py` and the package tests;
   add the release to `CHANGELOG.md` and `docs/IMPLEMENTATION_TRACKER.md`.
2. Run the tests, release validator, live Docs MCP smoke test, and
   `git diff --check` listed in [Development](#development). When new skills
   require backend tools, verify that the intended Product MCP environment
   exposes compatible tools before publishing.
3. Open a PR, review the public/private boundary, and merge only after its
   validation check passes.
4. From the merged `main` commit, create and push an annotated `vX.Y.Z` tag
   matching the manifest version. The tag triggers
   [Publish plugin release](.github/workflows/release.yml), which validates
   again, builds the public skills JSON and checksum and the plugin archive,
   then creates the GitHub release. Check that the workflow and release succeed.
5. Refresh the Git marketplace, reinstall the plugin, and start a new Codex
   task to load updated skills and tools:

   ```bash
   codex plugin marketplace upgrade popscale
   codex plugin add popscale-platform@popscale
   ```

   In Claude Code, refresh the marketplace, reinstall the plugin and run
   `/reload-plugins`. Verify both connections in a clean host. A plugin release
   does not deploy the Popscale backend or frontend.

See the [release runbook](docs/RELEASE.md) for the full checks, artifact rules,
and directory-submission gates.

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
git diff --check
```

No database migrations or application deployment are involved in plugin
releases.
