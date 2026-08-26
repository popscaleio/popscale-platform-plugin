# Changelog

All notable changes to the Popscale Platform plugin are documented here.

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
