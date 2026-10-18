# Compact Studies Analysis and Private Criteria

Require live `studies_analysis_v1`/native/source/own rights, never colleagues'
private data. Legacy scopes are not aliases. Platform assistant is unsupported until separate P3b3
and host verification.

Read `current_user`, `capabilities`, `get_interview_analysis_capabilities`.
Missing means unavailable, not empty; use live limits.
R = `interview:analysis:read`; W = `interview:analysis:write`.

| Operation | Scope | Result |
| --- | --- | --- |
| `get_interview_analysis_capabilities` | R | AnalysisCapabilities |
| `list_interview_analysis_studies` | R | StudyList |
| `get_interview_analysis_study` | R | StudyDetail |
| `create_interview_analysis` | R+W | envelope: AnalysisContext |
| `get_interview_analysis_context` | R | AnalysisContext |
| `prepare_interview_dataset` | R | envelope: PreparedDataset |
| `get_interview_dataset` | R | Dataset |
| `get_interview_dataset_job` | R | DatasetJob |
| `read_interview_dataset_page` | R | DatasetPage |
| `get_interview_dataset_artifact` | R | envelope: ArtifactAccess |
| `save_interview_dataset` | R+W | envelope: Dataset |
| `cancel_interview_dataset_job` | R | envelope: DatasetJob |
| `list_interview_classification_definitions` | R | DefinitionList |
| `get_interview_classification_definition` | R | DefinitionVersion |
| `save_interview_classification_definition` | R+W | envelope: DefinitionVersion |

Six bounded writes always return `{product_action, action_url}`; the domain
result is `product_action.result`. Non-AI/no debit; contexts start zero-mandate. R-only writes change state.

Choose explicit sources/population, canonical UUIDs, strict schemas/returned
cursors; no company/grant/profile/worker authority. Stable `idempotency_key` and transport `command_id`
replay unchanged after uncertainty. Changed intent needs new identities.
Receipt manifest=null: poll fresh dataset/job; action success is not READY.

Preserve full text/quotes/nested authored keys/agent_prompt/attribution and
false/zero/empty versus unknown; never infer identity. Read complete pages/required
file. dataset_file_transport_required forbids paging fallback, transcript
reconstruction, base64/prompt dump or truncation. Smaller selection needs new intent.

Save requested own READY/exact revision to own context: creation+24h temporary,
creation+30d saved; read/replay/refresh never extends/revives. Cancel remaining
build only; completed saved results survive. Inputs are not computed outputs.

## Own private criteria versions

List cursor=null/returned cursors; get exact definition_id/version_id.
Criteria JSON does not require a file adapter. Save requested criteria with stable
`command_id`/`idempotency_key`:

- New family: `definition_id=null`, name, criteria.
- Append: definition_id, current `expected_family_revision`, explicit
  `predecessor_version_id`, name, criteria, nonempty `change_reason`.

Append never overwrites history. `plan_stale`: reread; uncertain acknowledgement
replays unchanged. Save is private draft, `recommended=false`: no quality approval,
classification/purchase/publication/colleague/evidence access.

## Private file delivery and unsupported hosts

Trusted Product-origin authenticated_proxy needs current OAuth plus UUID
access_ref in X-Popscale-Artifact-Access, outside chat/model/tool/URL/scripts.
UUID alone grants nothing. A skill cannot extract the host credential;
no browser/manual-reupload substitute. Verify full canonical UTF-8 JSONL EOF,
SHA-256/bytes/record count in actual runtime before computing. Link/HEAD/receipt
proves no download; no Range. Revoke/source/role loss/expiry/credential
rotation/switch stops access; no handle transfer.

Otherwise transport_unavailable. D08 needs named platform/Codex desktop/macOS
builds and >4MiB/full computation; CLI/package/manual upload proves no host support.

## Consent and scope limits

Explicit profile=studies_analysis_v1; consent 1 retains R10/RW12; consent 2 adds
criteria R/R+W (R12/RW15) only after explicit new consent. Issuance stays on1 until
server activation; no client revision/config selector. refresh, switch
or plugin update never upgrades; New grants inherit no old private handles.
W permits own context/dataset/criteria saving, not classification/publication.
Finances require credits:read plus native rights; null is hidden, not zero.
C3's conditional [classification branch](classification-analysis.md) needs its
own server-selected package. External saved outputs/restore remain unavailable.
