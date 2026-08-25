# V1 implementation tracker

Last updated: 2026-08-25

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

## Manual directory gates

- [ ] Stable public privacy-policy URL published.
- [ ] Stable public terms-of-service URL published.
- [ ] OpenAI domain/challenge verification completed if requested.
- [ ] Claude connector/domain verification completed if requested.
- [ ] Registered production application ID available before adding `.app.json`.
- [ ] Clean OpenAI directory install proves both required connections.
- [ ] Clean Claude directory install proves both required connections.

Directory gates are intentionally separate from the public GitHub V1 release.
