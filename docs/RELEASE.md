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

Host evaluation scenarios for each skill are in `docs/evaluation/`; they are
acceptance criteria for the host runs below and are excluded from the runtime
bundle on purpose.

Then perform read-only OAuth smoke tests in clean Codex and Claude installations:

- docs search and page retrieval without authentication;
- `current_user` and `capabilities` against the intended Popscale company;
- bounded `search_company_content` plus one `content_detail` read without any
  mutation, generation, or publication;
- one sufficiently large department-grouped Journey aggregate through
  `company-usage-insights`, preserving suppression and without member drilldown;
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

## Public skill assets

The `1.3.1` candidate adds `public-skills.json` and `public-skills.sha256` beside
the existing archive. Build them from a clean, committed checkout with:

```bash
python3 scripts/build_public_skills.py --output-dir dist
```

The tag workflow runs the same builder after the unchanged validation gates.
The CLI derives `skill_source_commit` from HEAD and reads public skill bytes from
that commit's Git objects. It refuses dirty or untracked input and symlinks.
Assets are deterministic for one commit: no timestamps, host paths, environment
values or credentials are included. `dist/` is ignored and is never source.

The JSON `schema_version` is `popscale.public_skills.v1`. It contains:

- `plugin_version`, equal to the release tag without its `v` prefix;
- the exact `skill_source_commit` and `tool_contract_version`;
- `required_tools`, the supported Product MCP tool names referenced by the
  bundled methods, including the shared product-action contract;
- UTF-8 `files` with relative `skills/...` paths, SHA-256 and verbatim `content`;
- `instruction_paths`, the six skill entrypoints in declared order followed by
  their sorted recursive Markdown dependencies, and `required_reference_paths`;
- `skill_bundle_sha256`, SHA-256 of the path-sorted `{path, sha256}` array encoded
  as Python `json.dumps(..., sort_keys=True, separators=(',', ':'))` UTF-8.

The companion asset is the SHA-256 of the exact JSON bytes followed by one LF.
The bundle is at most 1 MiB, each file at most 256 KiB, and the compiled text
joined by two newlines at most 200,000 characters. Markdown references are
resolved relative to their source, including cross-skill references; missing,
escaping or unsafe local dependencies fail the build. Only reachable SKILL and
reference Markdown text is included. Local Python helpers remain optional
plugin development/host assets and are never executed by the bundle consumer.

`contracts/product-tools-v1.json` is a public name-only compatibility fixture
reviewed against the Product MCP contract. When a skill starts requiring a new
tool, update the fixture and its compatibility version when behavior changes.
The bundle describes requirements, not authority: a consuming host independently
restricts tools, authentication, company scope and approvals. Public Docs tools
are separate from the Product MCP requirement list. Host-specific routing and
private instructions belong to the consuming host, never to these assets.

A runtime consumer may discover new published, stable compatible releases,
verify both checksums and dependency closure, and cache them without deploying
the backend. It must trust the fixed repository/release origin, reject
incompatible contracts, retain its last verified compatible package on refresh
failure, and keep accepted conversations pinned to their exact verified source.
Checksums detect corruption; they do not replace trusted release ownership.
Marking a release superseded alone does not revoke an already pinned runtime
snapshot: consumers need an explicit version pin/blocklist for rollback.

Publication remains a separate approval after merge. The `1.3.1` skill contract
now requires the Product Actions v1 API; deploy that compatible backend before
publishing this plugin candidate. Coordinate with backend PR #438's consumer,
which can only fetch these assets after a separately authorized release. A
private assistant prompt or runtime configuration must never be added here.

## Feedback and navigation candidate — 1.5.0

Before publication, deploy compatible feedback/navigation tools, permissions and
schema, then verify target-environment discovery. The Product Actions v1 envelope
and bundle schema are unchanged; required_tools now includes the new capabilities.
Run synthetic feedback/navigation evaluations in clean Codex and Claude hosts.
Read-only OAuth checks do not prove submissions or approvals work. Any live write
needs separate explicit confirmation and a dedicated test company.

New first-party sessions use the verified current profile/cache; existing sessions
retain their immutable accepted instructions and delegation. Start a new session
to pick up this workflow. Preserve compatibility/checksum/dependency gates and
never load arbitrary branch assets to bypass release verification. Record exact
commit, validation commands/results and artifact hashes in the PR. Publishing,
frontend integration, clean-host checks and backend deployment remain separate
release gates; a packaged skill is not proof of end-to-end behavior.
