---
name: safe-content-administration
description: Find, inspect, create, and granularly edit company-scoped Popscale learning content, including roleplays, coaching sessions, challenges, episodes, flashcards, and existing journeys, with revision checks and safe generation or publication boundaries. Use when a company admin asks to manage existing Popscale content rather than design and execute a new journey plan.
---

# Safe Content Administration

Administer existing company content through `popscale-platform` while keeping the
OAuth-selected company, current server catalog, focused edits, and explicit
confirmation boundaries authoritative.

Read the shared [product action contract](../route-popscale-requests/references/product-actions.md) before any
mutation. Stable command identity and server-side human approval apply alongside
the workflow below; confirmation booleans alone do not approve effects.

## Required Workflow

1. Call `current_user`, then `capabilities`. Require an active effective
   `company_admin` in the intended OAuth-selected company. A Popscale superuser
   acting for a company must still select that company and receive company-admin
   capabilities for the session; global privilege or a company ID in the prompt
   is not authority.
2. Find the target with `search_company_content`. Use
   `list_company_content_references` for company-owned languages, departments,
   models, voices, or tags instead of guessing identifiers.
3. Read current state with `content_detail`. For nested content, call
   `list_content_components` and then `get_content_component` for the specific
   stable-ID row. Preserve pagination and truncation indicators.
4. Before changing an object, record the root `revision`, status, editable
   fields, component type, and exact requested delta. Prefer one focused root or
   component mutation over replacing a collection or unrelated fields.
   Apply the generation-only field rule below before any root write. When local
   Python is available, check proposed `content_update` arguments with the
   packaged checker's `--check-manual-write` mode; otherwise apply the same field
   exclusion directly. Editable fields and override flags do not waive it.
5. Pass the latest root `revision` as `expected_revision` for every protected
   mutation. Refresh after each successful mutation because root revision
   changes. On conflict, re-read and reconcile the user's requested delta; never
   retry blindly.
6. For an active-content edit through a tool whose live schema exposes
   `confirm_active_edit`, present the learner-visible consequence and obtain
   immediate explicit approval before setting `confirm_active_edit=true`.
   Editing approval does not authorize deletion, reordering, archiving,
   unrelated regeneration, reassignment, or publication. For Coaching input
   changes, include mandatory regeneration of both instruction outputs in the
   operation from the start; reuse authorization that already covers it.
7. Before deleting, reordering, replacing department assignments, or archiving,
   inspect `get_content_usage`. Use the dedicated confirmation required by the
   tool and describe any learner or journey impact. If usage details are
   truncated, retry once with `limit` large enough for the returned Journey and
   department counts, capped at the server maximum of 100. If the retry remains
   truncated, report the totals and stop when the decision requires exact
   dependency details. This tool cannot be filtered, offset, or paged.
8. Before generation, call `content_generation_capabilities` and follow the
   returned format/subpart contract. Generation is draft-only, asynchronous,
   and idempotent. Poll the returned request with `generation_request_detail`
   and `generation_request_steps`; do not claim completion early.
   After changing a dependency of a generation-only output, refresh detail and
   freshness, read generation capabilities, and follow the dependency decision
   flow in [tool-workflow.md](references/tool-workflow.md). Queue the supported
   subpart when authorized, or report the status/tool/scope/approval blocker.
   Source edits alone must not be reported as synchronized generated output.
   **Coaching exception to selective regeneration:** whenever Coaching inputs
   change, always regenerate BOTH `agent_prompt` (agent instructions) and
   `evaluation_instructions` through the platform after the source edits. Do
   not select only the output marked stale or reuse an older completed run.
   Verify both new saved outputs before completion or activation. If the pair
   cannot be generated, report the update as blocked/incomplete, never repair
   either instruction manually.
9. Before publication, read current detail and freshness for every generation-only
   output on the root, even if the earlier edit/report concerned another field.
   Stop on an edited protected output; do not rely on readiness to detect it.
   Call `content_activation_readiness`, present every failed or warning check,
   and call `content_activate` only after immediate explicit confirmation with
   `confirm_publish=true` and no unresolved generation-only workflow failure.
10. Report server-returned IDs, revisions, status, change history/freshness,
    generation state, and remaining warnings. Before any generation claim, follow
    [generation-verification.md](references/generation-verification.md): verify
    each requested artifact against its linked completed request step and actual
    saved output. Separate readiness, freshness and provenance; `legacy_unknown`
    never proves generation, and `output_edited` must be reported separately.
    Use the packaged evidence checker when local Python is available, otherwise
    apply the same checks to tool results. Never invent a URL, field,
    component, completion state, or permission.

## Safety Rules

- Treat every result as private to the company returned by `current_user`.
- Never send customer content, generated artifacts, identifiers, or OAuth
  material to `popscale-docs`.
- Never write, patch, translate, clear, or manually repair generation-only
  outputs: Roleplay `evaluation_instructions`; Coaching session
  `evaluation_instructions` and `agent_prompt`; Challenge `evaluation_prompt`.
  Never include these in `content_update` or a root create payload, or use
  `confirm_generated_output_override` for them. Generate them through the
  platform even when `editable_fields` or the schema permits direct writes.
  An explicit manual-rewrite request must be routed to platform generation;
  an unavailable generation path is a blocker, not a manual-text fallback.
- An edited generation-only output, including
  `source_changed_and_output_edited`, is a workflow failure. Report it and stop
  synchronization/publication claims and activation until platform regeneration
  and saved-output verification resolve it. Green readiness cannot clear it.
- Use `content:read` for inspection; focused mutations additionally require
  `content:write`. Supported generation workflows also require
  `generation:read` for voice discovery and asynchronous status/step reads;
  targeted regeneration requires `content:write` and `generation:write`, while
  language generation additionally requires `content:read` and
  `generation:write`. Activation additionally requires `publish:write`.
- Existing grants are not widened automatically. Surface the server's missing
  scopes and ask the user to reconnect or reauthorize instead of requesting a
  bearer token.
- Never add a confirmation field that the live tool schema does not expose.
  `archive_company_content` uses `confirm_archive` and, when required by the
  server, `confirm_learner_impact`; it does not accept `confirm_active_edit`.
- Treat `allowed_fields`, component types, generation capabilities, readiness,
  and validation errors returned by the server as authoritative. Never work
  around them through generic REST calls or guessed fields.
  Server editability is a technical constraint, not permission to override the
  stricter generation-only workflow.
- Do not expose or reconstruct bounded, masked, omitted, or cross-company data.
- `delete_content_component` requires a specific delete confirmation.
  `reorder_content_components` replaces one complete bounded ordering scope;
  verify every stable ID before calling it.
- `set_content_departments` replaces the complete assignment set. Resolve every
  department through the company-scoped reference tool and show the before/after
  set first.
- Targeted generation and language generation apply only to drafts. Card and
  generated-customer operations are append-only where the live capability
  catalog says so.
- Read-only media components are evidence, not editable fields. Use dedicated
  upload-intent tools only when the user separately asks to upload supported
  media and the required media scope is available.

Read [tool-workflow.md](references/tool-workflow.md) for exact tool and scope
selection. Read [content-format-map.md](references/content-format-map.md) when
choosing a root, component, or generation target. Read
[safety-and-fallbacks.md](references/safety-and-fallbacks.md) for stale edits,
active content, bounded results, and partial failures. Read
[evaluation-scenarios.md](references/evaluation-scenarios.md) when validating a
host or changing the Product MCP catalog.

## Product feedback and navigation

When the user wants to report a product problem or idea, use
[safe-product-feedback](../safe-product-feedback/SKILL.md) without copying private
content into a report implicitly. For a requested page destination, follow
[navigation and activity](../route-popscale-requests/references/navigation-and-activity.md).
A navigation proposal does not approve any content change or publication.
