# Changelog

All notable changes to the Popscale Platform plugin are documented here.

## [1.2.0] - 2026-08-26

### Added

- Added the portable `safe-content-administration` skill for bounded company
  content discovery, stable-ID root/component authoring, usage/history/freshness
  review, targeted regeneration, Episode/Flashcard language generation, and
  explicit activation.
- Added format maps and host evaluation scenarios for roleplays, coaching
  sessions, challenges, episodes, flashcards, and existing Journey sections and
  items, including active edits, stale revisions, wrong-company context, and
  publication boundaries.
- Added OAuth guidance for `content:read`, `content:write`,
  `generation:write`, and `publish:write` without silently widening existing
  grants.
- Added the portable `company-usage-insights` skill for privacy-safe Journey
  participation and content-outcome aggregates plus bounded member/attempt
  drilldown through the dedicated `usage:read` scope.
- Added analytics evaluation scenarios for department and role comparisons,
  small-cohort suppression, company isolation, pagination/date/row bounds, and
  historical Roleplay, Coaching, Flashcard, and Episode score limitations.

### Changed

- Expanded Codex and Claude package metadata and routing to distinguish
  granular edits to existing company content from Interview administration and
  new Journey-plan creation/execution.
- Updated `safe-journey-creation` only where its child-content activation step
  now requires `content:read` alongside write and publication scopes.
- Updated package contracts to require the complete granular content tool
  workflow, the five usage-insights tools, and all five portable skills.
- Expanded routing and package metadata to distinguish learner outcomes from
  `get_content_usage` dependency review and from Journey authoring/publication.

### Security

- Documented OAuth-selected company authority for company admins and superusers
  acting as company admins, root `expected_revision` checks, explicit active
  edit confirmation, stable-ID component mutations, bounded dependency review,
  and separate generation/publication confirmations.
- Documented authoritative small-cohort suppression, PII-minimized drilldown,
  bounded analytics, current organization dimensions, and historical score
  notices that must not be reconstructed or presented as immutable snapshots.

## [1.1.0] - 2026-08-25

### Added

- Added the portable `safe-interview-administration` skill for company-scoped
  Interview Study authoring, precise question edits, invitation workflows,
  bounded evidence review, and aggregate analyses.
- Added Interview routing and host evaluation scenarios, including stale-edit,
  respondent-link scope, delivery confirmation, batch-limit, publication, PII,
  and bounded-result cases.
- Added setup and OAuth consent guidance for `interview:read`,
  `interview:write`, `interview:distribute`, and Interview publication's
  additional `publish:write` requirement.

### Changed

- Expanded Codex and Claude package metadata to advertise Interview
  administration alongside existing Journey workflows.
- Updated public/private routing guidance so Interview data always stays on the
  authenticated Product MCP.

### Security

- Documented that existing grants are not silently widened, reusable respondent
  links require `interview:distribute`, current-draft edits use optimistic
  concurrency, and bounded or masked results must not be reconstructed.

## [1.0.1] - 2026-08-18

### Added

- Packaged the official Popscale symbol inside the plugin archive.
- Added Codex composer icon, logo, and brand-color metadata.
- Added release validation that rejects missing or invalid logo assets.

## [1.0.0] - 2026-08-18

### Added

- Public V1 marketplace distribution for Codex and Claude.
- Separate `popscale-docs` and `popscale-platform` remote MCP connections.
- Portable routing skill that protects the public/private data boundary and
  respects documentation status metadata.
- Safe journey creation workflow with review and explicit publication gates.
- Package contract tests, release validation, and live public Docs MCP smoke.
- Installation guidance for Codex, Claude Code, and Claude Cowork.

### Security

- The public documentation server has no auth, secret, header, or environment
  configuration.
- Customer data and product actions remain restricted to the OAuth-protected,
  company-scoped product server.
