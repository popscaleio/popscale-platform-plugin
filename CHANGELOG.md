# Changelog

All notable changes to the Popscale Platform plugin are documented here.

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
