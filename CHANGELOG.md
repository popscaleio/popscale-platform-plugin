# Changelog

All notable changes to the Popscale Platform plugin are documented here.

## [Unreleased]

### Changed

- Make the company-asset preflight proportional. Only server requirements stop
  generation: configured models and voice, a Company Overview for Roleplays, and
  selected generation-eligible Knowledge for Journey plans. Recommended inputs
  produce a warning and an offer to fill them; the user decides whether to
  generate anyway. The preflight applies to new exercises and Journey plans, not
  to targeted regeneration or language generation. Context-inclusion evidence is
  read from the plan snapshot where it exists; standalone generation is reviewed
  against the sources afterwards instead of being stopped for lack of a preview.

### Fixed

- Correct Episode authoring to use Script input (`model_steering`) exclusively
  for speaker/style rules. Source and translated scripts are generation-only;
  block manual root/component script writes and route corrections through
  platform regeneration. Remove the agent-imposed intermediate audio review
  gate; verify saved outputs read-only after supported platform generation.
- Use positive Episode Script input guidance adaptable to each company, purpose,
  audience and supported format. Keep openings and endings flexible, develop
  coherent thoughts and use meaningful speaker changes at the requested pace.
- Default Episodes to anonymous, topic-led conversations without invented host
  names, biographies or recurring podcast personas. Keep TTS choices separate
  from content; review source and translated scripts before audio, and stop
  active script corrections without a supported safe text/audio replacement flow.
- Require a shared company-asset preflight for Journey and standalone learning
  generation: substantive format-specific inputs, paginated discovery, exact
  read-back and evidence that verified sources reach the generation context.
  Missing or unverifiable required inputs block dispatch; source/configuration
  changes invalidate the prior check. Review source use in plans and saved
  exercises separately, while preserving mandatory paired Coaching generation.
- Point the live Docs MCP smoke test at the published assistant connection
  guide, and verify structured search/page results, published Markdown and tool
  errors instead of matching text anywhere in a response.
- Coaching input updates always regenerate both agent and evaluation
  instructions through the platform, regardless of per-output freshness.
  Completion requires both outputs to link to new post-edit generation requests.
- Classify Roleplay/Coaching evaluation instructions, Coaching agent prompts,
  and Challenge evaluation prompts as generation-only outputs. Technical
  editability and override flags no longer authorize manual plugin writes.
- Require a supported, authorized regeneration path after dependency changes,
  with explicit draft/status blockers and linked-step/saved-output verification.
- Treat edited protected outputs as workflow failures independent of readiness.
  Add an offline manual-write field guard and synthetic regression coverage;
  correct conflicting host scenarios, including active Coaching prompt edits.

### Changed

- Add purpose-led Study design guidance for conditional probes, meaningful
  completion criteria, respondent choice, focused extraction, and realistic
  interview duration without fixed question quotas.
- Separate design review, server publish readiness, and observed conversation
  quality. Add authoring-host and respondent-conversation evaluation scenarios;
  preserve narrow edits and existing product authorization boundaries.
- This is a guidance update, not an interviewer runtime change or a new Study
  setting. Live host and conversation evaluations remain separate release work.

## [1.3.1] - Unreleased

### Added

- Deterministic text-only public skill release assets with file hashes, complete
  Markdown dependencies, source provenance and Product Actions v1 requirements.
- Shared mutation guidance for stable UUID command identity, authenticated human
  approval, asynchronous result verification and server-owned generation prices.
- Bundle consumers can refresh compatible published skills independently of a
  backend deployment; private instructions and host adapters remain external.

### Fixed

- Require artifact-level generation evidence in content and Journey reporting;
  distinguish publishability, freshness, unknown origin and edited output.
- Preserve partial failures and current-operation errors even when older
  generated content remains present. Native media or translations without
  reliable linkage remain explicitly unverified.
- Add an offline evidence checker and synthetic regression tests. No new MCP
  tools, OAuth scopes, backend deployment or automatic remediation are added.

## [1.3.0] - 2026-08-29

### Added

- Added a browser-confirmed company-switch workflow using
  `request_company_switch`, the latest `current_grant_id`, and explicit
  confirmation before a short-lived switch link is created.
- Added Codex and Claude evaluation scenarios for successful switching,
  declined confirmation, stale-grant replay, and expired or used links.

### Changed

- Replaced wrong-company reconnect guidance across routing, Journey, Interview,
  content-administration, usage-insights, setup, and installation documentation
  with same-connection company verification through `current_user`.
- Kept reconnect and OAuth reauthorization guidance for actual authentication
  challenges or missing scopes rather than ordinary membership switching.

### Security

- Documented that the MCP tool never accepts a target company or membership
  identifier; eligible membership selection and final confirmation happen only
  in Popscale's authenticated browser flow.
- Added package contracts for explicit switch-link confirmation, replay-safe
  grant binding, same-connection verification, and non-rotation behavior.

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
- Added OAuth guidance for `content:read`, `content:write`, `generation:read`,
  `generation:write`, and `publish:write` without silently widening existing
  grants or queuing asynchronous generation that cannot be monitored.
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
- Documented that title-based analytics discovery uses
  `search_company_content` with optional `content:read`, while known-ID
  analytics remain available through `usage:read` alone.

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
