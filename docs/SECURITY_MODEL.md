# Security model

## Assets protected

- customer content and approved company knowledge;
- Interview Studies, questions, respondent-intro localizations, invitation
  links, respondent contact data, transcripts, evidence, and analyses;
- journey plans, generation jobs, and publication actions;
- roleplays, coaching sessions, challenges, episodes, flashcards, existing
  Journey components, media metadata, change history, and freshness state;
- Journey participation, completion, mastery, content outcome aggregates,
  member identities/progress, attempt metrics, and organization dimensions;
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
  requested Interview or content scopes become available.
- Content scopes remain separated: `content:read` for bounded inspection,
  `content:write` for focused mutations, `generation:write` for targeted
  generation, and `publish:write` for activation. Protected mutations use
  `expected_revision`; active edits additionally require
  `confirm_active_edit`.
- Company usage analytics require the dedicated read-only `usage:read` scope.
  The OAuth-selected company is authoritative; prompt-supplied company IDs do
  not change it. Small cohorts remain suppressed and member/attempt drilldowns
  stay bounded and PII-minimized.
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
| Stale or broad content edit overwrites a root or sibling collection | Stable-ID component tools, allowlisted fields, root `expected_revision`, and refresh after every mutation |
| Active content changes current learner behavior without review | Explicit active-edit confirmation plus separate delete, reorder, archive, generation, and publication boundaries |
| Cross-company reference ID is injected into content or generation | OAuth-selected company plus server validation of departments, languages, models, voices, assets, roots, and components |
| Cross-company analytics identifier or prompt company is supplied | OAuth-selected company plus server validation of Journeys, content, departments, memberships, and cursors |
| A small cohort is inferred from multiple analytics calls | Server suppression plus skill prohibition on threshold reduction, overlapping filters, subtraction, or detail-page reconstruction |
| Member drilldown exposes unnecessary PII | Explicit bounded drilldown; stable membership ID and safe display name only; no email, transcript, reflection, feedback text, or raw result payload |
| Historical score is presented as an immutable snapshot | Preserve `score_contract` and `historical_score_notice`; distinguish current thresholds/configuration and legacy Episode fallbacks |
| OAuth callback substitution | Exact callback binding with narrowly scoped loopback-port compatibility |
| Unreviewed write or publish | Safe journey workflow and explicit confirmation |
| Secret committed to plugin | Public-repo validation, review, and no secret-bearing config fields |
| Host lacks MCP App rendering | Structured result fallback; authorization remains unchanged |

## Review requirements

Any change to server URLs, OAuth metadata, scopes, routing rules, write behavior,
or host packaging requires a focused security review. Test with a second company
whenever a product-service change could affect tenant isolation. This public
repository itself has no database and introduces no migrations.
