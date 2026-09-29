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

Discover existing work with `generation_requests_list`,
`generation_request_detail` and `generation_request_steps`; reuse its request
ID. Start, retry, cancel and reconcile are state-changing operations. Preflight
before creation and again after source or mix changes. The plan retains its
creation snapshot; changed assets need a new request. Poll until completion,
failure or user review; never retry or reconcile speculatively.

## Journey Review

Apply the shared [Episode speaker policy](../../safe-content-administration/references/episode-speakers.md)
to every Episode item before execution: put anonymous-dialogue requirements in
Script input (`model_steering`) and voice codes only in dedicated configuration.
Platform execution generates scripts, translations and audio; the agent verifies
saved results read-only and never edits scripts. A valid plan or anonymous
steering alone does not prove that the generated result followed the inputs.

1. Read the saved overview with `journey_plan_detail`; present it and wait for
   feedback. For approved changes, `journey_plan_update_overview` replaces the
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

Roleplay overview selectors are mutually exclusive. Verify customer count in
the generated item input:

| `mode` | Fields | Result |
| --- | --- | --- |
| `generate_new` | No overview selector; generated input has `number_of_customers` | New scenario and its customers |
| `link_existing` | `linked_object_id` plus `customer_id` or `customer_seed` | Existing scenario; existing or newly generated customer |
| `reuse_scenario` | `reuse_from_client_id` (an earlier Roleplay item) plus `customer_seed` | Scenario created by that item; one new customer |

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

After execution, use the returned generation request or journey identifiers to
poll status. Item statuses: `waiting_for_scenario` and `child_request_created`
are in progress; `linked` is complete; `dependency_failed`,
`child_request_failed`, `link_failed`, `invalid_input` and
`missing_child_request` are failures for that item. Report current content and
Journey names and status. Use only server-returned URLs and verified completion
state. If the result is only a draft, say so plainly.

Before claiming that child content is platform-generated, follow the shared
[generation verification](../../safe-content-administration/references/generation-verification.md).
Use execution mappings to find each child root and request, then inspect its
saved content, linked steps and artifact freshness. Check reused content too;
plan completion and publication readiness cannot substitute for these reads.
Never treat Journey-level `available=false` freshness as proof of current child
content. Keep successful, edited, unknown and failed parts visible in the final
report; a partial child request must not disappear from the summary.
