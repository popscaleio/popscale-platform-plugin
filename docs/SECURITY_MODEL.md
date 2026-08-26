# Security model

## Assets protected

- customer content and approved company knowledge;
- Interview Studies, questions, respondent-intro localizations, invitation
  links, respondent contact data, transcripts, evidence, and analyses;
- journey plans, generation jobs, and publication actions;
- Popscale OAuth access and refresh tokens;
- company membership, role, and feature state;
- the integrity and status of public documentation.

## Boundaries

### Public documentation server

`https://docs.popscale.io/mcp` is unauthenticated and read-only. Its packaged
configuration contains no headers, token, secret, or environment value. It
exposes published documentation only and cannot access customer records.

### Product server

`https://app.popscale.io/mcp/` requires Popscale OAuth. Authorization and company
isolation are enforced by the service, not by the skill. Clients do not provide
a company ID to override the authenticated company scope.

### Host and plugin

Codex and Claude decide when to call available tools. The routing skill reduces
cross-boundary mistakes but is not a security control. Every product tool must
still reject unauthorized scopes, roles, memberships, and companies server-side.

## Required controls

- PKCE and exact redirect binding for OAuth authorization-code flows.
- No static customer credential in the repository or MCP configuration.
- Product grants remain company-scoped and revocable.
- Write and publication flows require explicit human confirmation where defined
  by the safe journey workflow.
- Interview scopes remain separated: `interview:read` for bounded reads,
  `interview:write` for authoring and analysis mutations, and
  `interview:distribute` for respondent links and invitation operations. Study
  publication additionally requires `publish:write`.
- Existing grants are never silently widened; users reauthorize before newly
  requested Interview scopes become available.
- Docs marked `draft` or `review` are labeled and not used as verified mutation
  authority.
- Customer identifiers, content, credentials, and OAuth material never go to
  the public docs server.

## Threats and mitigations

| Threat | Mitigation |
| --- | --- |
| Public docs receive customer data | Routing skill prohibition; separate server; no product capability |
| Docs are treated as authorization | Skill boundary plus server-side product authorization |
| Cross-company product access | Company derived from authenticated membership; server-side isolation tests |
| Respondent link or PII disclosed by a broad read | Focused detail tool requires `interview:distribute`; list results omit links and raw contact data |
| Stale or broad Interview edit overwrites concurrent work | Current-draft requirement, focused mutation tools, and optimistic concurrency tokens |
| OAuth callback substitution | Exact callback binding with narrowly scoped loopback-port compatibility |
| Unreviewed write or publish | Safe journey workflow and explicit confirmation |
| Secret committed to plugin | Public-repo validation, review, and no secret-bearing config fields |
| Host lacks MCP App rendering | Structured result fallback; authorization remains unchanged |

## Review requirements

Any change to server URLs, OAuth metadata, scopes, routing rules, write behavior,
or host packaging requires a focused security review. Test with a second company
whenever a product-service change could affect tenant isolation. This public
repository itself has no database and introduces no migrations.
