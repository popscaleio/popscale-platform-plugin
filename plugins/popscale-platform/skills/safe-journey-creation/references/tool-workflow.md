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

Follow the main skill's two saved review gates. For Episode items, apply the
shared [speaker policy](../../safe-content-administration/references/episode-speakers.md)
and inspect each saved brief before execution. `render_journey_review` is
optional; structured text works. Only an explicit instruction after the second
review authorizes `journey_plan_execute` on the accepted plan.

Each Roleplay item selects one customer. Scenario customer count does not count
Journey items. Overview selectors are mutually exclusive:

| `mode` | Fields | Result |
| --- | --- | --- |
| `generate_new` | No overview selector; verify generated `input_payload.number_of_customers: 1` for this pattern | New scenario; first customer |
| `link_existing` | `linked_object_id` plus `customer_id` or `customer_seed` | Existing scenario; existing/new customer |
| `reuse_scenario` | `reuse_from_client_id` (an earlier Roleplay item) plus `customer_seed` | New customer in reused scenario |

For seeded reuse, `customer_id` is assigned during execution. A linked
pre-execution selector with no summary errors is ready for review. The item
input validation tool rejects selectors because they have no generated payload;
a tool argument error does not establish invalid content.

## Publication

Follow the main skill's publication step: verify `journey_activation_readiness`,
confirm and activate each child, refresh readiness, then separately confirm the
Journey. Activation uses `confirm_publish=true`; `content_activate` needs
`content:read`, `content:write` and `publish:write`.
App controls use the same server authorization.

## Completion

`waiting_for_scenario` and `child_request_created` are pending; `linked` is
complete. `dependency_failed`, `child_request_failed`, `link_failed`,
`invalid_input` and `missing_child_request` are failures. Read
`journey_structure_get` after execution; shared Roleplay encounters need
separate items with one scenario and distinct customers. Follow
[generation verification](../../safe-content-administration/references/generation-verification.md)
for each child; plan completion alone proves no child artifact provenance.
