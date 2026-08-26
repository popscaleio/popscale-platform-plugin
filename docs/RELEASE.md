# Release runbook

## Release scope

Plugin releases publish manifests, marketplaces, skills, tests, and public docs.
They do not deploy the Popscale backend, frontend, Docs MCP, DNS, or database and
therefore do not trigger application maintenance mode.

## Prepare

1. Start from `main` and create a branch.
2. Update both host manifest versions and the Claude marketplace version.
3. Update `CHANGELOG.md` and `docs/IMPLEMENTATION_TRACKER.md`.
4. Preserve both exact MCP URLs and the public/private routing boundary.
5. Confirm no backend code, customer data, environment file, or secret is added.

## Validate

```bash
python3 -m unittest discover -s plugins/popscale-platform/tests -p 'test_*.py' -v
python3 scripts/validate_release.py
python3 scripts/live_docs_smoke.py
git diff --check
```

Then perform read-only OAuth smoke tests in clean Codex and Claude installations:

- docs search and page retrieval without authentication;
- `current_user` and `capabilities` against the intended Popscale company;
- bounded `search_company_content` plus one `content_detail` read without any
  mutation, generation, or publication;
- host restart and credential persistence;
- no write or mutation unless separately approved in a dedicated test company.

## Publish

1. Open a PR and require the package validation check.
2. Review the complete diff and the security boundary.
3. Merge to `main` only when checks and review are green.
4. Create a signed or annotated `vX.Y.Z` tag and GitHub release.
5. Attach the generated Claude plugin archive from the release workflow.
6. Test installation from the public GitHub marketplace in a clean host.

## Directory submission gates

GitHub marketplace distribution and universal directory submission are separate.
Before submitting to a host directory:

- publish stable privacy-policy and terms-of-service URLs; do not use guessed or
  404 URLs in the manifest;
- complete any host domain ownership or challenge verification for
  `app.popscale.io` and `docs.popscale.io`;
- register the production MCP application with the host and add `.app.json`
  only when a real stable application ID exists;
- verify the submission flow provisions the primary product MCP and the public
  docs dependency, or document the separate docs connector fallback;
- run a clean directory install rather than relying on a local marketplace;
- complete Claude and OpenAI submissions independently because approvals do not
  transfer between directories.

These gates do not block public GitHub V1 distribution.

## Rollback

If a release package is incorrect, publish a corrected patch release and mark
the faulty GitHub release as superseded. Do not repoint MCP URLs to staging and
do not weaken OAuth or tenant boundaries as a rollback mechanism. Server-side
incidents follow the owning service's deployment runbook, not this repository.
