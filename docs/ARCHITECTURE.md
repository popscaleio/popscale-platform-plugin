# Architecture

## Package shape

Popscale Platform is one plugin with two remote MCP servers and two portable
skills. Codex and Claude use host-specific manifests but share the same plugin
root, MCP configuration, and skill source.

```text
Host marketplace
  └─ Popscale Platform plugin
       ├─ route-popscale-requests
       ├─ safe-journey-creation
       ├─ popscale-docs (public and read-only)
       └─ popscale-platform (OAuth and company-scoped)
```

The plugin does not proxy either server and contains no API implementation.

## Trust boundary

| Request | Server | Authority |
| --- | --- | --- |
| Public concepts, setup, or documentation | `popscale-docs` | Published docs plus status metadata |
| Customer state and approved company knowledge | `popscale-platform` | Authenticated company session |
| Product mutation or publication | `popscale-platform` | Server authorization plus human confirmation |

The public server cannot prove authorization and cannot be the source of
approved company knowledge. The product server is not used as a fallback search
engine for public documentation.

## Skill decision

Tool descriptions alone do not reliably resolve mixed requests such as
"explain journeys, then list ours." V1 therefore includes one small routing
skill. It contains policy and workflow only:

1. Public questions use `get_docs_overview` or `search_docs`, then `get_pages`.
2. Customer data and actions use `popscale-platform`.
3. Customer data and credentials never go to the docs server.
4. `draft` and `review` documentation is labeled and not presented as verified
   product behavior.

The skill deliberately does not copy documentation or tool schemas. The
existing `safe-journey-creation` skill remains authoritative for authenticated
journey workflows and does not import public docs as mutation authority.

## MCP App

The product MCP can return structured results and an optional Journey Review UI
resource. Hosts without MCP App rendering continue with structured tool results.
The public repository does not include an `.app.json` placeholder. That file is
added only after a real host application registration supplies a stable mapping.

## Source ownership

- This repository owns public plugin packaging, skills, tests, and release docs.
- The Popscale application repository owns product MCP behavior and OAuth.
- The `popscale-docs` repository owns public documentation and its read-only MCP.

Changes cross repository boundaries through reviewed releases; this plugin does
not write documentation or deploy either server.
