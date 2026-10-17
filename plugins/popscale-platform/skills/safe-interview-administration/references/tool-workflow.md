# Interview Tool Workflow Reference

Live `capabilities` and schemas are authoritative. Compact saved-data analysis
uses [compact-analysis.md](compact-analysis.md), not the administration route.

## Administration discovery and authoring

After `current_user` / `capabilities`, use `list_interview_studies` and
`get_interview_study` for current published state, editable draft and edit tokens.
Authoring requires `interview:read` + `interview:write`:

- `create_interview_study` creates only a requested new Study;
  `ensure_interview_study_draft` idempotently finds/creates its current draft.
- `update_interview_study` changes non-versioned metadata;
  `update_interview_draft` changes versioned content/report language.
- `create_interview_topic`, `update_interview_topic`,
  `delete_interview_topic`, `reorder_interview_topics` make focused topic changes.
- `upsert_interview_localization`, `delete_interview_localization` affect the
  current draft; `generate_interview_localizations` queues asynchronous work.

Use exact latest `expected_updated_at` (topic timestamp for topic edits), then
refresh Study detail after child changes. Study generation through
`generation_request_create(request_type=interview_study)` takes required `name`,
`purpose`, `context`, optional category/respondent/report language,
`desired_duration_minutes` (5–240), and `must_include` (up to 30). Unknown fields
are dropped: read `generation_request_detail` before start. Compact inputs
instead reject unknown fields.

## Publication and distribution

`get_interview_publish_readiness` precedes confirmed `publish_interview_study`:
latest edit token, `confirm_publish=true`, read/write plus `publish:write`.

`list_interview_invites` returns summaries under `interview:read`.
`get_interview_invite`, `create_interview_invite`,
`create_interview_invites_bulk`, `send_interview_invite_email`,
`revoke_interview_invite`, `expire_interview_invite` also need
`interview:distribute`. Sending needs immediate confirmation, `confirm_send=true`
and at most 500 explicit `invite_ids`. Summaries do not authorize link/contact
reconstruction.

## Existing runs and aggregate analyses

`list_interview_runs`, `get_interview_run_review` provide bounded evidence;
page transcript turns only using their returned cursors/limits.
`list_interview_analyses`, `preview_interview_analysis`,
`get_interview_analysis` use `interview:read`.
`generate_interview_analysis`, `retry_interview_analysis`,
`update_interview_run_action_status`, `update_interview_analysis_action_status`
also require `interview:write`. Generation/retry are explicit asynchronous
mutations. Preserve truncation/provenance bounds and omitted identity, filter
values and raw errors. These tools never substitute for a compact dataset.
