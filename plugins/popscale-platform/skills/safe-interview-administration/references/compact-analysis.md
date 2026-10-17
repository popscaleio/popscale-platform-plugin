# Compact Studies Analysis and Private Criteria

Use only when the live Product MCP exposes the requested operation under an
explicit `studies_analysis_v1` OAuth profile. Current native Studies read rights,
feature, source access and private owner remain authoritative; Company Admin
cannot open a colleague's private data or criteria. Legacy Interview scopes are not
aliases. Platform assistant is unsupported until separate P3b3 support and host
verification; a public skill bundle grants no tools or credentials.

## Discovery and exact operation subset

Call `current_user`, `capabilities`, then
`get_interview_analysis_capabilities`. Missing operations are unavailable, not
empty data. Use returned limits; never hardcode capacity. R below means
`interview:analysis:read`; W means `interview:analysis:write`.

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
result is `product_action.result`. They are non-AI without generation debit;
R-only does not make them read-only. Follow server action state/approval rules.
Context creation has zero purchase mandate; it starts no model or paid work.

1. List/read permitted Study/version/topic metadata; choose the explicit saved
   sources/population for the user's question. Follow strict live schemas,
   canonical UUIDs and returned cursors. Unknown fields are rejected: never
   supply company/grant/profile/worker authority or internal normalized selection.
2. Prepare once with stable domain `idempotency_key` and transport `command_id`.
   Replay identical intent with both identities unchanged after an uncertain
   response; do not create another job. Changed intent needs new identities.
   The prepare action receipt has `manifest=null`: poll fresh dataset/job with
   growing intervals until READY, failure or a required decision. Action success
   alone is not dataset completion.
3. Read complete canonical pages or the required file, preserving text, quotes,
   nested values and attribution. False/zero/empty differ from missing or
   unavailable. Do not strip permitted content/PII or authored keys merely named
   `agent_prompt`; internal authority/prompts stay outside the server projection.
   Do not infer withheld identity or treat insufficient evidence as negative.
4. Respect `dataset_file_transport_required`. No unlimited page fallback,
   transcript reconstruction, base64/prompt dump, truncation or silent smaller
   population. Propose any smaller selection explicitly as a new request.
5. Save only when requested: own live READY dataset, own context and exact
   content revision. Temporary expiry is creation+24h; explicit save is
   creation+30d. Reads/replay/refresh do not extend it or revive closed content.
   Cancel only requested remaining build work; completed saved results survive.
   Saved input is not a saved computed analysis or output upload.

## Own private criteria versions

Use list with `cursor=null`, then only returned cursors; get requires exact
`definition_id` and `version_id`. Criteria JSON does not require a file adapter.
Save only requested criteria with stable `command_id` and `idempotency_key`:
- New family: `definition_id=null`, `name`, `criteria`.
- Append: `definition_id`, current `expected_family_revision`, explicit
  `predecessor_version_id`, `name`, `criteria`, nonempty `change_reason`.

Use live criteria schemas; no extra fields. Append creates an immutable version;
it never overwrites history. On `plan_stale`, reread before proposing revised
intent; uncertain acknowledgement replays unchanged identities. Saved criteria
remain private draft, `recommended=false`; saving provides no quality approval,
classification, purchase, publication, colleague access or evidence access.

## Private file delivery and unsupported hosts

Use the server's `authenticated_proxy` path on the trusted Product MCP origin.
A verified private host adapter sends current OAuth credentials and UUID
`access_ref` in `X-Popscale-Artifact-Access`; the UUID alone grants no access.
Never a bearer in chat, prompt, model/tool arguments, URL/query or saved scripts.
A skill cannot extract the host credential; generic fetch/browser and manual
reupload are not substitutes.

The adapter must install the full canonical UTF-8 JSONL into the actual runtime
and independently match manifest SHA-256, bytes and record count before computing.
A link, HEAD response or action receipt proves no download/computation. No Range
resume is supported. Revocation, source/role loss, expiry or company switch stops
access; refresh does not widen consent or extend retention. Old private handles
cannot be rebound after switch; an old in-flight credential stops after refresh.

Without verified credential-preserving adapter support, report
`transport_unavailable` for file delivery; do not claim Codex desktop support.
D08 requires separate actual platform-agent and Codex desktop/macOS/local-runtime
proof, locked versions, private >4 MiB JSONL and a known full-file computation
without manual upload. CLI/package tests do not pass these host gates.

## Consent and scope limits

Select `profile=studies_analysis_v1` through supported OAuth consent. The server
selects the package: consent 1 retains R10/RW12; consent 2 adds list/get criteria
with R and save with R+W (R12/RW15). New authorization stays on package 1 until
server activation of 2; no client revision/config selector. Use live capabilities.
Missing consent needs explicit reauthorization after activation; refresh, switch
or plugin update never upgrades it. New grants inherit no old private handles.
W permits own context/dataset/criteria saving, not classification/publication.
Classify/publish scopes add no operations here. Finances additionally require
`credits:read` and native finance rights; null means hidden, not zero. New
classification, corrections, budgets, durable computed outputs and external output
return remain unavailable.
