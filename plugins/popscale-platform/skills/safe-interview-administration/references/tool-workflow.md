# Interview Tool Workflow Reference

Discover the live catalog with `capabilities`. The names below describe the
current Product MCP contract; server results and authorization remain
authoritative.

## Identity and discovery

| Order | Tool | Purpose | Required scope |
| --- | --- | --- | --- |
| 1 | `current_user` | Verify identity, selected company, role, and granted scopes | Authenticated MCP session |
| 2 | `capabilities` | Verify the Interviews feature and available operations | Authenticated MCP session |
| 3 | `list_interview_studies` | Find a bounded Study summary | `interview:read` |
| 4 | `get_interview_study` | Read current published state, current draft, edit tokens, and readiness | `interview:read` |

## Authoring

Use `create_interview_study` only for a new Study. Use
`ensure_interview_study_draft` to idempotently reuse or create the current draft.

- `update_interview_study` changes non-versioned Study metadata.
- `update_interview_draft` changes versioned purpose, description, intro,
  closing, completion rules, action areas, change summary, or report language.
- `create_interview_topic`, `update_interview_topic`,
  `delete_interview_topic`, and `reorder_interview_topics` make focused question
  changes. Prefer append/remove/upsert operations for probes, must-cover points,
  and extraction fields when the user did not ask to replace the whole list.
- `upsert_interview_localization` and `delete_interview_localization` manage one
  normalized locale. `generate_interview_localizations` queues durable
  respondent-intro generation.

These mutations require `interview:read` and `interview:write`. Use the latest
returned `updated_at` as `expected_updated_at` where required, and refresh Study
detail after every child mutation.

## Publication

1. Call `get_interview_publish_readiness` with `interview:read`.
2. Present errors, warnings, changed sections, and the exact draft target.
3. Obtain immediate explicit confirmation.
4. Call `publish_interview_study` with `confirm_publish=true`, the current edit
   token, `interview:read`, `interview:write`, and `publish:write`.

Publication is separate from editing or generating content. Earlier approval to
edit does not authorize publication.

## Invitations

| Tool | Purpose | Required scope |
| --- | --- | --- |
| `list_interview_invites` | Read PII-minimized Study invitation summaries | `interview:read` |
| `get_interview_invite` | Read one masked detail and reusable respondent link | `interview:read` + `interview:distribute` |
| `create_interview_invite` | Create one invitation | `interview:read` + `interview:distribute` |
| `create_interview_invites_bulk` | Create a validated invitation batch | `interview:read` + `interview:distribute` |
| `send_interview_invite_email` | Send invitations or reminders after confirmation | `interview:read` + `interview:distribute` |
| `revoke_interview_invite` | Revoke one invitation | `interview:read` + `interview:distribute` |
| `expire_interview_invite` | Expire one invitation | `interview:read` + `interview:distribute` |

`send_interview_invite_email` requires `confirm_send=true` and at most 500
explicit `invite_ids`. Do not treat list output as a source of raw respondent
contact data or reusable links.

## Runs and analyses

- `list_interview_runs` and `get_interview_run_review` provide bounded,
  evidence-first run data. Page transcript turns using the returned cursor and
  limits rather than requesting or concatenating an unbounded transcript.
- `list_interview_analyses`, `preview_interview_analysis`, and
  `get_interview_analysis` are reads under `interview:read`.
- `generate_interview_analysis`, `retry_interview_analysis`,
  `update_interview_run_action_status`, and
  `update_interview_analysis_action_status` also require `interview:write`.

Analysis generation and retry are explicit asynchronous mutations. Preserve
truncation markers and the global provenance limits in summaries. Hidden
metadata filter values, raw processing errors, and omitted respondent identity
are not recoverable fields.
