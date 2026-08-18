# V1 implementation tracker

Last updated: 2026-08-18

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

## Public repository release

- [x] GitHub repository created as public.
- [x] Initial V1 branch pushed and reviewed through PR.
- [x] Required CI check enabled and green.
- [ ] `v1.0.0` release and Claude archive published.
- [ ] Clean Codex install from public GitHub marketplace verified.
- [ ] Clean Claude marketplace install from public GitHub repository verified.

## Manual directory gates

- [ ] Stable public privacy-policy URL published.
- [ ] Stable public terms-of-service URL published.
- [ ] OpenAI domain/challenge verification completed if requested.
- [ ] Claude connector/domain verification completed if requested.
- [ ] Registered production application ID available before adding `.app.json`.
- [ ] Clean OpenAI directory install proves both required connections.
- [ ] Clean Claude directory install proves both required connections.

Directory gates are intentionally separate from the public GitHub V1 release.
