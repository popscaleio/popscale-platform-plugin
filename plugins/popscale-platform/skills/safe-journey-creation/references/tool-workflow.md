# Tool Workflow Reference

## Readiness

| Order | Tool | Purpose | Required scope |
| --- | --- | --- | --- |
| 1 | `current_user` | Verify identity, role, selected company, and granted scopes | Authenticated MCP session |
| 2 | `capabilities` | Discover allowed Popscale capabilities for this session | Authenticated MCP session |
| 3 | `company_assets_list`, `company_asset_detail` | Inspect required assets, category coverage, saved values and revisions for the selected format mix | `content:read` |
| 4 | `list_company_content_references` | Resolve languages, models and applicable voices; separately verify actual configuration | `content:read` |
| 5 | `knowledge_agent_context_manifest` | Inspect the stored Knowledge manifest and source hash; it does not prove company-asset inclusion | `knowledge:read` |
| 6 | `knowledge_assets_list` | Select approved, active, generation-eligible assets | `knowledge:read` |
| 7 | `knowledge_generation_context` | Read the approved Knowledge context; reading may diagnose gaps before generation is allowed | `knowledge:read` |

If the required capability or scope is absent, stop before the affected action.
Run the shared [company asset preflight](../../safe-content-administration/references/company-asset-preflight.md)
before generation: server requirements stop, recommended inputs warn. The
plan's captured company context (`generation_metadata.company_context`) shows
what the generator actually consumed; read it at plan review.

## Plan and Generation

Reuse requests via `generation_requests_list`, `generation_request_detail` and
`generation_request_steps`. Start, retry, cancel and reconcile change state.
Preflight before creation and after source/mix changes; changed assets need a
new request. Saved overview without an active item-input step means
`overview_review` where available; `item_inputs` means its step is pending,
queued or running. Never retry speculatively.

## Journey Review

Apply the shared [Episode speaker policy](../../safe-content-administration/references/episode-speakers.md)
to every Episode item before execution: put format-appropriate anonymous speaker
requirements in Script input (`model_steering`) and voice codes only in dedicated
configuration.
Platform execution generates scripts, translations and audio; the agent verifies
saved results read-only and never edits scripts. A valid plan or anonymous
steering alone does not prove that the generated result followed the inputs.
For a plan that may produce audio Episodes with Next Generation enabled, include the structured
plan brief and locales. After `journey_plan_get_item_inputs`, inspect each
Episode's distinct brief, then propose and, after approval, validate corrections before
execution. Explicit Original or video uses Original; no manual Episode drafts.

1. Read `journey_plan_detail`; show the proposal immediately, then wait. Count
   one item per customer encounter and show scenario → item → selected customer;
   clarify conflicting totals or mix. For approved changes,
   `journey_plan_update_overview` replaces the
   complete overview. Re-read and obtain acceptance on the same plan.
2. Only then call `journey_plan_generate_item_inputs`. Poll, then read the
   results with `journey_plan_get_item_inputs`.
3. Validate every item with `journey_plan_validate_item_input`; summarize the
   inputs, offer item detail/edits and wait. Apply approved focused changes via
   `journey_plan_update_item_input`, re-read and revalidate.
4. `render_journey_review` offers the App review; use structured text otherwise.
5. Call `journey_plan_execute` only after the second review and an explicit
   “create Journey” confirmation. These conversational stops add no backend
   approval state.

Each Roleplay item selects one customer. Scenario customer count does not count
Journey items. Overview selectors are mutually exclusive:

| `mode` | Fields | Result |
| --- | --- | --- |
| `generate_new` | No overview selector; verify generated `input_payload.number_of_customers: 1` for this pattern | New scenario; first customer |
| `link_existing` | `linked_object_id` plus `customer_id` or `customer_seed` | Existing scenario; existing/new customer |
| `reuse_scenario` | `reuse_from_client_id` (an earlier Roleplay item) plus `customer_seed` | New customer in reused scenario |

## Publication

1. Reconcile until the plan reports `journey_draft_ready`.
2. Call `journey_activation_readiness` and inspect every linked content row.
3. For each draft row with `can_activate=true`, present the exact content target,
   ask for specific confirmation, then call `content_activate` with
   `confirm_publish=true`. This call requires `content:read`, `content:write`,
   and `publish:write`; an older grant may need reauthorization.
4. Refresh `journey_activation_readiness`. Do not continue while an item is
   missing, invalid, draft, inactive, or still generating.
5. Present the current Journey title, enough verified context to identify it,
   and the activation consequence. Ask for a new
   final confirmation, then call `journey_activate` with `confirm_publish=true`.

Content activation and journey activation are separate safety boundaries. A user
approval for one does not authorize the other.

Never infer that an App button bypasses the MCP tool. App actions call the same
server tools and therefore use the same OAuth scopes, tenant checks, serializers,
auditing, and error handling.

## Completion

Poll the returned request/Journey. `waiting_for_scenario` and
`child_request_created` are pending; `linked` is complete;
`dependency_failed`, `child_request_failed`, `link_failed`, `invalid_input` and
`missing_child_request` are item failures. Report names and status using only
verified server URLs. Call a draft a draft.

Read `journey_structure_get` after execution. For shared Roleplay encounters,
verify two saved items with the same `scenario_id` and different `customer_id`
values; a scenario containing both customers alone does not meet the brief.

Before claiming generated content, follow [generation verification](../../safe-content-administration/references/generation-verification.md):
use execution mappings to inspect each child's saved content, request steps
and freshness, including reused content. Plan completion, readiness and
Journey-level `available=false` freshness prove none of these. Report
successful, edited, unknown and failed parts, including partial requests.
