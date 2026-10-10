# Channel permissions and recovery

## Live authority

Check `current_user`, `capabilities` and the selected company. Use only tools
marked `available: true` or currently allowed by the host. Role labels, templates,
scopes and installation are not authority; missing tools are not empty data.
CompanyAdmin keeps established access; other active human memberships
need explicit channel permissions. Support checks remain server-owned.

| Channel            | Activation         | Docs group          | Operations group          |
| ------------------ | ------------------ | ------------------- | ------------------------- |
| External MCP       | `mcp.external.use` | `mcp.external.docs` | `mcp.external.operations` |
| Built-in assistant | `assistant.use`    | `assistant.docs`    | `assistant.operations`    |

Each group requires that channel's activation permission. External access also
requires `mcp_access`, `mcp_access_enabled` and OAuth consent. Built-in access needs
`admin_assistant`; its access is independent of the external switch.
An operations group never grants ordinary system powers.

## Documentation and native authority

Documentation-only Product MCP consent requests optional `docs:read`, not every
advertised scope. Compatible CompanyAdmin `admin:read` can still read docs; the
alias is one-way. `docs:read` never grants admin company data, Studies, people
reads or generic ProductAction preparation/execution. Do not require operational
tools to answer public questions; do not broaden permissions to recover docs.

The separate public `popscale-docs` server requires no channel permission,
template or OAuth. External hosts use it for public guidance, never customer
content, identifiers, tokens or denied product work. Built-in hosts use exposed
server-owned docs tools: do not invent a public connection,
browser, plugin installation or OAuth workflow. Retain draft/review status.

| Work                                                                                          | Native authority, plus channel/group, features and operation consent |
| --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Studies inspection/analysis                                                                   | `studies.read` or `studies.edit`                                     |
| Study editing, invitations, publication, recommendation updates                               | `studies.edit`                                                       |
| People inspection                                                                             | `people.read` within the currently permitted units                   |
| Journey/content authoring, usage insights, settings, catalogs, credits, access administration | Established CompanyAdmin/domain restrictions                         |

A Study reader's analysis `interview:write` consent grants no editing/invitation
access. Analysis retains price, receipt and approval rules: not a free read.
People consent `admin:read` opens only permitted people tools, never another
unit/company or `status=removed/all`. Do not join stale department labels.

## Recovery

`available: false` does not identify its cause by itself; do not invent a missing
permission. Follow the evidence:

| Evidence                                                           | Action                                                                                                            |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| Channel/group/native denial, including 403 or JSON-RPC -32003      | Stop; authorized administrator reviews access. Reconnecting cannot grant authority.                               |
| Missing required OAuth scopes or explicit authentication challenge | External reauthorization for required scopes, after server-side authority is available. Never request raw tokens. |
| Disabled company feature                                           | Ask its authorized feature owner.                                                                                 |
| Tool excluded by the host profile, or cause unknown                | Report the limitation; do not assume reconnect fixes it.                                                          |

External OAuth reconnect is not an assistant recovery step. For wrong-company
external sessions follow the [company-switch workflow](../SKILL.md#company-switch-boundary)
instead of reconnecting. Built-in users select the company in the portal and
start a new conversation; never offer external switch tools.

## Revocation and uncertain effects

After revocation, stop affected reads/effects; do not replay an old preview,
approval or successful result as authority. Keep the accepted `command_id` and
action/job identity. Read `product_action_get` only if it is still allowed;
otherwise report the outcome as unknown. Never issue a new command, reconnect,
scrape UI or use generic REST to bypass revocation. Only explicit stale-preparation
rejection plus restored authority permits refreshed state and a newly reviewed
intent; old approval cannot be reused. Plugin updates grant no rights or consent.
Built-in sessions retain pinned snapshots; new sessions adopt verified published
compatible bundles, never branch assets or private host instructions.
