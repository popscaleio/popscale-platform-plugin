# AGENTS.md

## Scope

This repository is the public distribution source for the Popscale Platform
plugin. Keep changes focused on plugin manifests, marketplace metadata, skills,
tests, and public documentation.

## Non-negotiable boundaries

- Keep `popscale-docs` exactly at `https://docs.popscale.io/mcp` and public,
  unauthenticated, and read-only.
- Keep `popscale-platform` exactly at `https://app.popscale.io/mcp/` and OAuth
  authenticated with company scope derived by the service.
- Never add secrets, tokens, customer identifiers, private URLs, environment
  files, backend implementation, or customer content.
- Never route customer data or product writes through `popscale-docs`.
- Never make draft or review-status docs authoritative for a product mutation.
- Keep `safe-journey-creation` product-only and require confirmation before
  execution or publication.

## Packaging

- Keep Codex and Claude manifests at version parity.
- Keep `.agents/plugins/marketplace.json` and
  `.claude-plugin/marketplace.json` aligned with the shared plugin root.
- Every manifest path must stay inside `plugins/popscale-platform`.
- Do not add `.app.json` until a real registered application mapping exists.
- Update `CHANGELOG.md` and `docs/IMPLEMENTATION_TRACKER.md` with every release.

## Validation

Run before committing:

```bash
python3 -m unittest discover -s plugins/popscale-platform/tests -p 'test_*.py' -v
python3 scripts/validate_release.py
python3 scripts/live_docs_smoke.py
git diff --check
```

Live product OAuth tests are manual and read-only by default. Product writes
require an explicit human confirmation and a dedicated test company.
