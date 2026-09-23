# V1 implementation tracker

Last updated: 2026-09-23

## Episode Script input correction — unreleased

- [x] Map Script input to `model_steering`; source `script` and translated/source
  `script_text` are generation-only regardless of exposed editability. Correct
  the format map and both standalone/Journey authoring workflows.
- [x] Extend the offline field guard to root/component create/update payloads
  and report edited Episode scripts as workflow failures. Keep input edits and
  unrelated allowed fields under their existing authorization rules.
- [x] Remove the prior mandatory intermediate pre-audio review gate. Use supported
  platform pipelines, including combined generation, and verify outputs read-only.
- [x] Add positive Script input guidance with coherent, developed turns and
  meaningful speaker changes. Keep technical boundaries in the agent workflow;
  adapt examples, structure and pace to each company, purpose and supported
  format. Cover varied briefs, explicit choices and platform-owned pacing fixes.
- [x] Correct the shared speaker scenarios and add draft manual-repair, payload
  bypass and edited-output cases. No backend implementation or customer mutation.
- [x] All 80 package tests pass, including four new Episode policy/guard tests
  plus expanded protected-field cases. Release and both skill validators pass;
  public bundle dependency checks, `git diff --check` and live Docs smoke pass.
- [ ] Live host tool traces and a separately authorized release remain pending.

## Anonymous Episode speakers — unreleased guidance

- [x] Share anonymous-speaker defaults across standalone Episode and Journey
  workflows. Use natural topic-led openings, structural speaker labels and
  separate TTS configuration; no invented or persistent podcast identities.
- [x] Limit named-host exceptions to explicit user-supplied identities. Review
  steering and complete source/translated scripts; distinguish whole-name
  matches from substrings and legitimate subject-matter mentions.
- [x] Superseded the initial intermediate review gate with the Script input
  correction above: platform-owned generation and read-only output verification.
  Preserve existing company preflight/scopes.
- [x] Stop active input corrections without a supported way to regenerate scripts
  and audio together; separate script review, job success, media linkage and
  listening evidence. No customer incident data enters the public package.
- [x] Add shared synthetic host acceptance scenarios for defaults, identity leakage,
  translations, exceptions, missing gates and active/draft corrections.
- [x] All 76 package tests, release validation, both changed skill validators,
  Markdown dependency checks and live public Docs MCP smoke pass. The shared
  policy and scenarios are included in the public skill bundle.
- [ ] Run live Codex/Claude tool-trace scenarios; package checks do not establish
  model behavior or audio quality.
- [ ] Backend support remains separate reported work. No backend code, customer
  mutation, profile feature, manifest bump or plugin release is included.

## Company asset preflight — unreleased guidance

- [x] Journey and standalone generation share one preflight reference, with a
  format requirements matrix, all nine Roleplay customer categories, substantive
  completeness, paginated discovery and saved-value/revision verification.
- [x] Require evidence of actual context inclusion before generation; distinguish
  asset presence and Knowledge hashes from company-source binding. Missing tools,
  material omissions/truncation and stale bindings are explicit blockers.
- [x] Recheck after relevant changes and review source use in both plans and saved
  outputs. Preserve approval/scope boundaries and mandatory paired Coaching
  regeneration; read-only inspection and source preparation remain possible.
- [x] Add shared host evaluation scenarios covering pagination, blank sources,
  missing evidence, changed revisions/mix, conditional configuration, standalone
  retries and actual output review. Public guidance contains no private data.
- [x] All 76 package tests, release validation, both changed skills' frontmatter
  validation, Markdown reference checks and the public Docs MCP smoke pass.
  The shared reference and scenarios are included in the public skill bundle.
- [ ] Run the documented Codex/Claude tool-trace scenarios. Package tests and
  static reference validation do not establish host compliance.
- [ ] Backend enforcement and a supported pre-generation context verification
  surface remain separate implementation work. This guidance deliberately stops
  when live tools cannot prove the required context; it adds no backend capability.
- [ ] Publish separately; no manifest bump, tag or plugin release in this change.

## Live Docs smoke repair

- [x] Replace the retired `/integrations/popscale-mcp/` fixture with the published
  `/integrations/connect-assistant/` guide and its listed resource URI.
- [x] Check exact structured search/page paths, published status and nonempty
  Markdown; reject MCP tool errors explicitly with actionable diagnostics.
- [x] All 76 unit tests pass, including five smoke regressions. Release validation,
  `git diff --check` and the full read-only live Docs MCP smoke pass.
- [x] Preserve public unauthenticated Docs access, tool annotations and protocol
  checks. No endpoint, product mutation, manifest version or release changes.

## Generation-only evaluation outputs — unreleased fix

- [x] Coaching input updates require new platform generation of both instruction
  outputs after the final source edits, even if only one or neither appears
  stale. Known blockers stop new input edits; incomplete pairs block completion
  and activation. The offline checker requires the pair and post-edit request IDs.
- [x] Exclude Roleplay/Coaching `evaluation_instructions`, Coaching `agent_prompt`,
  and Challenge `evaluation_prompt` from manual plugin writes, including explicit
  rewrite requests and schema-provided override confirmation.
- [x] Add dependency regeneration/draft-blocker handling and align the format
  map, tool flow, reporting, safety guidance, and Journey child-content boundary.
- [x] Add an offline field guard to the existing evidence checker, plus explicit
  workflow-failure reporting for edited protected artifacts. This is a host-side
  aid, not a server-enforced write prohibition or a new MCP tool.
- [x] Add synthetic regressions and host scenarios for active and draft content,
  manual rewrite requests, green readiness after editing, and ordinary manual
  fields. No customer data or incident identifiers enter the public package.
- [x] Local validation passes: 64 unit tests (including 17 new behavioral
  regressions), `scripts/validate_release.py`, `quick_validate.py` for both
  changed skills, and `git diff --check`. Review includes pre-activation checks
  for protected outputs outside a prior report's scope.
- [x] The legacy Docs smoke path failure is resolved by the separate repair
  above. This public documentation check is not a generation test.
- [ ] Run clean Codex/Claude tool-trace evaluations in an authorized dedicated
  test company. Automated local tests do not establish live host behavior.
- [ ] Release separately. No manifest version bump, tag, backend change, live
  content repair, or customer mutation is part of this fix.

## Public skill distribution — 1.3.1 candidate

- [x] Deterministic committed-source JSON/checksum builder and tag-release assets.
  Complete recursive Markdown text is included; private host instructions,
  configuration, executables and customer content are outside the artifact.
- [x] Routing, content, Journey and Interview skills link the shared Product
  Actions v1 contract. Existing OAuth/public Docs endpoints remain unchanged.
  Setup/capability metadata reviewed: no additional scopes or host capabilities.
- [x] Compatibility fixture and consumer contract documented, including refresh,
  provenance, cached fallback, immutable conversations and version rollback.
  Backend PR #438 consumes the assets; publication is a separate dependency.
- [x] `python3 -m unittest discover -s plugins/popscale-platform/tests -p
  'test_*.py' -v`: 54 tests pass, including seven bundle regressions covering
  reproducibility, reference closure, content hashes, size/path limits, actual
  committed provenance, dirty inputs and symlinks. `python3
  scripts/validate_release.py` and `git diff --check` pass.
- [x] Live Docs smoke passes after the separate current-guide repair above.
  Clean host evaluations/OAuth smoke remain manual release checks and were not
  run here.
- [ ] Separate approval, merge and public release remain required. No release,
  backend deployment, price/feature activation or maintenance action performed.

## Study design quality — unreleased guidance

- [x] Add a conditional authoring reference to `safe-interview-administration`
  for new Studies and substantial redesigns, preserving focused-edit scope.
- [x] Cover conditional probes, completion by information rather than question
  quotas, transitions, respondent choice, relevant extraction, time expectations,
  and the boundary between interviewing and coaching.
- [x] Add separate authoring-host and respondent-conversation evaluation cases.
  Design review, publish readiness, and observed behavior remain distinct.
- [x] Align with the companion public Studies guide using synthetic examples.
  No customer evidence or runtime implementation is included in the package.
- [x] Package checks pass: 47 unit tests, `scripts/validate_release.py`, skill
  `quick_validate.py`, and `git diff --check`. PyYAML for the skill validator was
  installed in a temporary directory, without a package dependency change.
- [ ] `scripts/live_docs_smoke.py` reaches search but fails its legacy canonical
  path assertion for `/integrations/popscale-mcp/`, as already recorded for the
  1.3.1 candidate below. The script is unchanged; this guidance does not fix the
  existing smoke-test mismatch. No conversation behavior is validated by it.
- [ ] Evaluate in clean Codex and Claude hosts and run authorized synthetic
  conversations in a dedicated test company. These checks are not replaced by
  package validation and are not claimed as completed by this change.
- [ ] Review and release separately; no manifest version change, tag, runtime
  change, backend deployment, or customer Study mutation is included here.

## Generation verification — 1.3.1 candidate

- [x] Shared evidence rules connected to content administration, Journey
  completion and private product-state routing. Readiness, freshness and origin
  are reported separately for every requested artifact.
- [x] Local standard-library evidence checker with synthetic regressions for
  populated ready fields with unknown origin, edited output, partial requests,
  newer failed attempts, missing native linkage and incomplete/mismatched reads.
  It performs no network requests, writes, or product actions.
- [x] Current Product MCP read contracts reviewed. No endpoint, tool, OAuth scope
  or backend change is needed for this conservative reporting improvement.
  Existing native language/audio evidence limitations are explicit.
- [x] Routing and safe-journey-creation updated; manifest capabilities and setup
  reviewed with no new scope/capability requirement. Host manifests and the
  Claude marketplace are aligned at candidate version 1.3.1.
- [x] Validation: `python3 -m unittest discover -s plugins/popscale-platform/tests
  -p 'test_*.py' -v` (47 tests); `python3 scripts/validate_release.py` and
  `git diff --check` pass. A focused independent read review found no actionable
  issues. Python coverage validates the checker/package, not host LLM behavior.
- [ ] `python3 scripts/live_docs_smoke.py` fails at the canonical integration
  path assertion in the search result. The same failure was reproduced with
  the unmodified main script. Initialization and tool listing pass; later page
  and resource assertions were not reached. No Docs code changed here.
- [ ] Clean Codex and Claude evaluations of the new scenarios and read-only
  OAuth smoke tests remain release checks; they were not run in this PR work.
- [ ] Review, merge, tag and publish 1.3.1 separately. This candidate performs no
  backend deployment, migration, maintenance-mode action or customer mutation.

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
  `content:read`, `content:write`, `generation:read`, `generation:write`, and
  `publish:write`.
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
- [x] Title-only analytics resolution uses company-scoped
  `search_company_content` under optional `content:read`; known-ID analytics
  remain `usage:read`-only and never guess prompt-supplied IDs.
- [x] Routing, Codex/Claude metadata, setup/OAuth consent, security model,
  release smoke guidance, and package contracts updated for usage insights.
- [x] `safe-content-administration`, `safe-journey-creation`, and
  `safe-interview-administration` reviewed and intentionally unchanged: the new
  contract is read-only analytics, while `get_content_usage` remains an
  authoring dependency/impact check.
- [x] Usage-insights plugin delivery remains package-only: no MCP App, backend
  deploy, migration, maintenance mode, or plugin release is included in this PR.
- [x] Browser-confirmed company-switch Product MCP downstream impact reviewed
  against the production backend contract for `request_company_switch`.
- [x] Routing, Journey, Interview, content-administration, and usage-insights
  guidance updated to stop reads/writes on a mismatch, require explicit link
  creation confirmation, and verify the selected company on the same connection.
- [x] Setup, installation, security documentation, evaluation scenarios, and
  package contracts cover target-free tool input, stale replay, expired links,
  and preserved OAuth access and refresh tokens.
- [x] Company-switch plugin delivery remains package-only: no MCP endpoint,
  OAuth scope, MCP App mapping, database migration, backend deploy, or
  maintenance-mode action is included in this PR.

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
- [ ] `v1.3.0` company-switch package reviewed, merged, tagged, and published
  after the production switch page is available and clean Codex/Claude host
  smoke tests pass.

## Manual directory gates

- [ ] Stable public privacy-policy URL published.
- [ ] Stable public terms-of-service URL published.
- [ ] OpenAI domain/challenge verification completed if requested.
- [ ] Claude connector/domain verification completed if requested.
- [ ] Registered production application ID available before adding `.app.json`.
- [ ] Clean OpenAI directory install proves both required connections.
- [ ] Clean Claude directory install proves both required connections.

Directory gates are intentionally separate from the public GitHub V1 release.
