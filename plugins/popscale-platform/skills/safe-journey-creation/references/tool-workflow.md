# Tool Workflow Reference

## Readiness

| Order | Tool | Purpose | Required scope |
| --- | --- | --- | --- |
| 1 | `current_user` | Verify identity, role, selected company, and granted scopes | Authenticated MCP session |
| 2 | `capabilities` | Discover allowed Popscale capabilities for this session | Authenticated MCP session |
| 3 | `knowledge_agent_context_manifest` | Inspect the stored company context snapshot and source hash | `knowledge:read` |
| 4 | `knowledge_assets_list` | Select approved, generation-eligible assets | `knowledge:read` |
| 5 | `knowledge_generation_context` | Build the approved context used for this generation | `knowledge:read` |

If the required capability or scope is absent, stop before the affected action.

## Plan and Generation

Use `generation_request_create` only when a suitable request does not already
exist. Use `generation_requests_list`, `generation_request_detail`, and
`generation_request_steps` to discover and understand existing work before
starting or retrying it. `generation_request_start`, `generation_step_retry`,
`generation_request_cancel`, and `journey_plan_reconcile` are explicit
state-changing operations.

The workflow is asynchronous. Poll status at a reasonable cadence and stop when
the request is completed, failed, canceled, or awaiting user action. Do not call
retry or reconcile speculatively.

## Journey Review

1. `journey_plan_detail` returns the plan overview, items, readiness, and known
   validation state.
2. `journey_plan_update_overview` changes the plan-level overview. Confirm the
   proposed replacement before calling it.
3. `journey_plan_update_item_input` applies one focused item input change.
4. `journey_plan_validate_item_input` validates one item against Popscale's server contract.
5. `render_journey_review` returns the same review state and links the standard
   Journey Review MCP App through resource metadata.
6. `journey_plan_execute` turns an entirely valid plan into downstream journey
   work. It requires an immediately preceding explicit user confirmation.

## Publication

1. Reconcile until the plan reports `journey_draft_ready`.
2. Call `journey_activation_readiness` and inspect every linked content row.
3. For each draft row with `can_activate=true`, present the exact content target,
   ask for specific confirmation, then call `content_activate` with
   `confirm_publish=true`.
4. Refresh `journey_activation_readiness`. Do not continue while an item is
   missing, invalid, draft, inactive, or still generating.
5. Present the exact journey ID/title and activation consequence. Ask for a new
   final confirmation, then call `journey_activate` with `confirm_publish=true`.

Content activation and journey activation are separate safety boundaries. A user
approval for one does not authorize the other.

Never infer that an App button bypasses the MCP tool. App actions call the same
server tools and therefore use the same OAuth scopes, tenant checks, serializers,
auditing, and error handling.

## Completion

After execution, use the returned generation request or journey identifiers to
poll status. Report server-returned IDs and status, not model-generated URLs or
guessed completion state. If the result is only a draft, say so plainly.
