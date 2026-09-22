# Content Administration Tool Workflow

Discover the live catalog with `capabilities`. Tool availability, returned
schemas, and authorization remain authoritative over this reference.
The plugin's generation-only exclusions are stricter than technical editability;
an editable field or override flag does not authorize bypassing them.

## Identity and discovery

| Tool | Purpose | Required scope |
| --- | --- | --- |
| `current_user` | Verify effective role and OAuth-selected company | Authenticated MCP session |
| `capabilities` | Discover enabled tools and missing scopes | Authenticated MCP session |
| `search_company_content` | Search bounded summaries across supported root formats | `content:read` |
| `list_company_content_references` | Resolve company languages, departments, models, voices, or tags | `content:read` |
| `content_detail` | Read one root or directly addressable child plus editable fields and root revision | `content:read` |
| `list_content_components` | Page stable-ID components under one root | `content:read` |
| `get_content_component` | Read one component in its company-scoped root | `content:read` |
| `get_content_usage` | Read bounded journey and department usage | `content:read` |
| `list_content_history` | Page bounded MCP/admin change summaries | `content:read` |
| `get_content_freshness` | Inspect generated artifact freshness and regeneration hints | `content:read` |

Search results are summaries. Read detail before a mutation and preserve
`has_more`, offsets, cursors, truncation, and unavailable-history indicators.
`get_content_usage` is bounded but not pageable or filterable. When the default
result is truncated, retry once with `limit` equal to the larger returned
Journey/department count, capped at the server maximum of 100. Preserve totals
and truncation flags; if the retry is still truncated, stop when exact details
are required. Do not invent offset, cursor, or filter arguments.

## Focused authoring

| Tool | Mutation boundary | Required scope |
| --- | --- | --- |
| `create_company_content` | Create one draft root using allowlisted fields | `content:read`, `content:write` |
| `content_update` | Update allowlisted fields on one root or directly addressable child | `content:read`, `content:write` |
| `create_content_component` | Add one stable-ID component without replacing siblings | `content:read`, `content:write` |
| `update_content_component` | Update one component | `content:read`, `content:write` |
| `delete_content_component` | Delete one component after usage/revision checks | `content:read`, `content:write` |
| `reorder_content_components` | Replace one complete bounded sibling ordering | `content:read`, `content:write` |
| `set_content_departments` | Replace the complete company department assignment set | `content:read`, `content:write` |
| `archive_company_content` | Move supported content to its non-destructive inactive/archive state | `content:read`, `content:write` |

Every protected mutation uses the latest root `revision` as
`expected_revision`. Refresh root detail after success. Active-content edits
require `confirm_active_edit=true` only on tools whose live schema exposes that
field, after the user approves the exact edit. Deletion requires
`confirm_delete=true`. `archive_company_content` does not accept
`confirm_active_edit`; it requires `confirm_archive=true` and may require
`confirm_learner_impact=true` after a separate learner-impact confirmation.

Use component CRUD for a single roleplay customer/question/objection/decision
rule/criterion, episode script variant, flashcard/card translation, or journey
section/item. Use `content_update` for scalar root edits and directly addressable
child edits when no collection operation is needed.
Exclude all generation-only outputs in [content-format-map.md](content-format-map.md)
from manual payloads, including creation. Use the local `--check-manual-write`
guard described in [generation-verification.md](generation-verification.md) when
available before `content_update`; a failed guard prevents the call.

## Dependency changes and generation-only outputs

For Coaching input changes, the required output scope is always BOTH
`agent_prompt` and `evaluation_instructions`, regardless of per-artifact freshness
or dependency hints. Include the pair in the input-update operation and its
required authorization from the outset; do not ask again when already covered.
If the user explicitly forbids regeneration, explain the conflict and stop
before making a new input edit rather than completing a source-only update.
If generation is already known to be unavailable for the target, resolve the
draft/capability blocker before starting new Coaching input edits. Report any
inputs already saved as an incomplete update.

1. Identify whether the requested source/component changes affect a protected
   output using current detail, freshness, dependency hints, and capabilities.
   Examples include customer, criteria/points, goals, or coaching-source edits.
   Before an active edit, include any known regeneration limitation in the
   learner-impact review so source changes are not presented as a complete fix.
2. After source mutations, refresh root detail/revision and
   `get_content_freshness`. If a generation-only output is affected, call
   `content_generation_capabilities` and choose only supported subparts.
3. If generation is supported for the current status and authorized, queue
   `content_regenerate_subparts` for the affected outputs. If authorization or
   the required monitoring/write scopes are missing, report that specific
   blocker before dispatch. For other formats, a source-only edit or “keep
   everything else” request does not silently authorize extra generation.
   Coaching input updates always include the required pair; preserve unrelated
   fields and do not expand the refresh to description or education text.
4. If generation requires a draft, use only a documented draft workflow exposed
   by the available product tools and authorized for this target. If none is
   available, stop and explain that a draft workflow or additional platform
   support is required. Do not invent a draft endpoint, demote active content,
   clone/reassign it, or use an override as a substitute.
5. Follow the returned request with `generation_request_detail` and
   `generation_request_steps`. Verify each affected artifact against its linked
   completed step and actual saved result, then read freshness again. If source
   or output changed in the meantime, reconcile rather than claiming success.
   For Coaching, bind BOTH outputs to the regeneration request(s) started after
   the final input edits. Do not substitute a pre-edit successful request or
   accept only one completed instruction. Record `coaching_inputs_changed=true`
   and `coaching_regeneration_request_ids` in the local checker envelope, keeping
   these host-side fields out of MCP arguments.
6. Report source changes actually saved, generation completed/pending/blocked,
   and readiness, freshness, and provenance separately. Stop activation and
   synchronized-output claims on an edited generation-only artifact even if
   readiness is green. Do not disable an already active object without authority.

Never use `content_update` on the generation-only output itself, including when
generation is unavailable, fails, or the user explicitly asks for manual text.

## Generation

1. Call `content_generation_capabilities` with `content:read` immediately before
   choosing a format, subpart, or granular generation operation.
2. Confirm the target is a draft and present the exact generated subparts.
3. For targeted regeneration, call `content_regenerate_subparts` with a stable
   idempotency key. It requires `content:write` and `generation:write`.
4. For Episode or Flashcard language generation, resolve the language through
   `list_company_content_references`, then call `content_language_generate` with
   `content:read`, `content:write`, and `generation:write`. Use
   `gemini_tts_voices_list` when Episode audio voice names are needed.
5. Poll `generation_request_detail` and `generation_request_steps`. Retry or
   cancel only when the server reports a supported state and the user approves
   that separate mutation. Voice discovery and both polling tools require
   `generation:read`; do not queue work under a grant that cannot monitor it.
6. Refresh `content_detail`, `list_content_components`, and
   `get_content_freshness` after completion. Follow
   [generation-verification.md](generation-verification.md) before reporting:
   check each requested artifact, linked completed step, saved output and any
   current failed/running attempt. Readiness does not prove generator origin.

An idempotency key replay is safe only for identical input. A conflict means the
key was already used for different work; create a new key rather than mutating
or bypassing the request.

## Activation

`content_activation_readiness` and `content_activate` require `content:read`,
`content:write`, and `publish:write`. Activation is available for roleplays,
coaching sessions, challenges, episodes, and flashcard decks—not Journeys.
Existing Journey publication remains in `safe-journey-creation` through
`journey_activation_readiness` and `journey_activate`.

Read current detail and freshness for all generation-only outputs on the target
before activation, including outputs outside the earlier edit/report scope.
An edited protected artifact blocks activation even when server readiness is
green. A scoped evidence report does not establish readiness for the whole root.
After Coaching input changes, pending or unverified regeneration of either
instruction also blocks activation, even if neither output is marked edited.
If the required freshness read is unavailable, report the verification blocker
rather than assuming there is no failure.

Present the exact target, current revision/status, readiness checks, unresolved
generation-only failures, and learner-visible consequence. Once no such failure
remains, obtain immediate confirmation, then call
`content_activate` with `confirm_publish=true`. Refresh detail after success.
