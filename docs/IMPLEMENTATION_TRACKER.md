# V1 implementation tracker

Last updated: 2026-08-26

## Complete

- [x] Separate public Docs MCP and authenticated Platform MCP.
- [x] Exact production endpoint packaging for both servers.
- [x] Codex and Claude manifests share one plugin root.
- [x] Codex and Claude marketplace metadata included.
- [x] Minimal routing skill chosen and documented; no duplicated docs content.
- [x] Safe journey skill remains product-only.
- [x] Docs status metadata is respected by routing policy.
- [x] Customer installation, verification, and troubleshooting documented.
- [x] Package contract and release validation implemented.
- [x] Live Docs MCP initialize, tools, search, pages, and resources smoke covered.
- [x] Production OAuth verified manually in Codex against company Popscale.
- [x] Production custom-connector flow verified manually in Claude Cowork.
- [x] Migration review: no database or migration changes.
- [x] Deployment review: repository publication does not trigger maintenance.
- [x] Official Popscale logo packaged and covered by manifest contract tests.
- [x] Interview Admin Product MCP downstream impact reviewed against the
  stabilized backend contract.
- [x] Portable Interview administration skill added for current-state reads,
  focused edits, invitation safety, and bounded insights.
- [x] Routing, capability metadata, setup/OAuth consent guidance, evaluation
  scenarios, and package contract tests updated for Interview scopes.
- [x] `safe-journey-creation` reviewed and intentionally unchanged because the
  Journey tool and safety contract did not change.
- [x] Interview plugin delivery remains package-only: no MCP App, backend deploy,
  database migration, or maintenance mode action is included.
- [x] Granular Company Content Product MCP downstream impact reviewed against
  the backend contract deployed to staging at `44735b3`.
- [x] Portable `safe-content-administration` skill added for bounded discovery,
  root/component CRUD, usage/history/freshness, targeted regeneration, language
  generation, and explicit activation.
- [x] Roleplay customers/questions/objections/decision rules/criteria, Episode
  script/media state, Flashcard cards/translations/languages, and existing
  Journey sections/items mapped to stable-ID workflows and eval scenarios.
- [x] Routing, capability metadata, setup/OAuth consent guidance, security
  model, release validation, and package contract tests updated for
  `content:read`, `content:write`, `generation:write`, and `publish:write`.
- [x] `safe-journey-creation` updated only for the new `content:read` requirement
  on child-content activation. Journey plan/execution, MCP App, and final Journey
  publication remain unchanged; existing-Journey component edits route to
  `safe-content-administration`.
- [x] `safe-interview-administration` reviewed and intentionally unchanged
  because the Interview contract did not change in this backend slice.
- [x] Content plugin delivery remains package-only: no MCP App, backend deploy,
  database migration, maintenance mode, or plugin release is included in this
  PR.
- [x] Company Usage and Journey Insights downstream impact reviewed against the
  backend contract deployed green to staging at `d5c90e0`.
- [x] Portable `company-usage-insights` skill added for `get_journey_insights`,
  `list_journey_members`, `get_member_journey`, `get_content_outcomes`, and
  `list_content_attempts` through `usage:read`.
- [x] Aggregate-first department/role comparisons, bounded member/attempt
  drilldown, small-cohort suppression, tenant authority, PII minimization,
  pagination/window/row guards, and current versus historical metric semantics
  documented and covered by evaluation scenarios.
- [x] Routing, Codex/Claude metadata, setup/OAuth consent, security model,
  release smoke guidance, and package contracts updated for usage insights.
- [x] `safe-content-administration`, `safe-journey-creation`, and
  `safe-interview-administration` reviewed and intentionally unchanged: the new
  contract is read-only analytics, while `get_content_usage` remains an
  authoring dependency/impact check.
- [x] Usage-insights plugin delivery remains package-only: no MCP App, backend
  deploy, migration, maintenance mode, or plugin release is included in this PR.

## Public repository release

- [x] GitHub repository created as public.
- [x] Initial V1 branch pushed and reviewed through PR.
- [x] Required CI check enabled and green.
- [x] `v1.0.0` release and Claude archive published.
- [x] Clean Codex install from public GitHub marketplace verified.
- [x] Clean Claude marketplace install from public GitHub repository verified.
- [ ] `v1.0.1` logo patch and archive published.
- [ ] `v1.1.0` Interview administration package reviewed, merged, tagged, and
  published after the backend contract is deployed and host smoke tests pass.
- [ ] `v1.2.0` granular company-content and usage-insights package reviewed,
  merged, tagged, and published after production backend availability and clean
  host smoke tests.

## Manual directory gates

- [ ] Stable public privacy-policy URL published.
- [ ] Stable public terms-of-service URL published.
- [ ] OpenAI domain/challenge verification completed if requested.
- [ ] Claude connector/domain verification completed if requested.
- [ ] Registered production application ID available before adding `.app.json`.
- [ ] Clean OpenAI directory install proves both required connections.
- [ ] Clean Claude directory install proves both required connections.

Directory gates are intentionally separate from the public GitHub V1 release.
