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
| `company_assets_list`, `company_asset_detail` | Inspect paginated company assets and read back exact saved values/revisions | `content:read` |
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
rule/criterion, flashcard/card translation, or journey
section/item. Use `content_update` for scalar root edits and directly addressable
child edits when no collection operation is needed.
Episode script variants are read-only to the agent even when component CRUD
exposes writable fields. Change Script input (`model_steering`) and use platform
generation for source scripts and translations; never patch generated text.
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
A known regeneration blocker (for example an active session) counts here; do
not save new Coaching inputs while the mandatory pair cannot follow.

Pick the subpart from the intent. The table is the contract for existing roots;
the live capabilities decide whether the subpart is supported for the current
status.

| The user wants to | Subpart | Effect on saved content | On an existing Roleplay |
| --- | --- | --- | --- |
| Change how a Roleplay is judged (weighting, tone of feedback, a rule) | `evaluation_instructions` | Rewrites the instruction only | Run after the source edit; no extra confirmation |
| Change Coaching inputs of any kind | `agent_prompt` + `evaluation_instructions` | Rewrites both instructions | Always the pair; see the Coaching rule above |
| Change the scoring criteria themselves | `evaluation_criteria` | Deletes every criterion and creates a new list; totals change | Describe the replacement and obtain a yes first |
| Change the situation, goal or setting of a Roleplay | `setup` | Rewrites scenario fields the user did not name | Describe what is rewritten and obtain a yes first |
| Add customers to a Roleplay | `customers` | Appends; existing customers and Journey links remain | State how many are added and obtain a yes first |
| Refresh learner-facing text after a source change | `description`, `education_text` | Rewrites those texts only | No extra confirmation |
| Change an Episode's content or speaker rules | `script` (then audio) | Regenerates script, marks translations stale | Edit `content` / `model_steering` first |

Never queue several subparts because you are unsure which one applies; ask.
`evaluation_criteria` and `setup` are the two that discard work the admin may
have done by hand, which is why they require a described, confirmed change.

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
4. Draft and active roots can regenerate in place when the selected subpart is
   supported. A live `available: false` result still blocks the call; do not
   demote, clone or reassign content to work around it. For Roleplays, read the
   saved combined Knowledge selection before regeneration. Explicit
   `knowledge_asset_ids` must match those saved IDs; the server freezes their
   approved pinned versions, even if a newer draft version exists. Change the
   saved selection separately, with revision and active-edit checks, if that is
   the user's intent. Do not substitute all assets from a Journey plan.
5. Follow the returned request with `generation_request_detail` and
   `generation_request_steps`. Verify each affected artifact against its linked
   completed step, then read freshness again. Read visible saved results, but
   use metadata only for redacted Roleplay/Coaching instruction outputs. If a
   source changes during active generation, the stale step fails without saving
   it; refresh and reconcile before a separately authorized retry.
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

## Review before activation

The public checklist `/journeys/review-before-activation/` and the language
guide `/content/language-in-exercises/` are the review criteria for
learner-facing text and Journey structure. Server readiness checks structure
and thresholds; the checklist covers what readiness cannot see (placeholder
text, question counts, opening lines, dashes, jargon). Report, propose, wait
for approval per finding, then edit through the focused tools.

## Generation

For Episodes, apply [speaker and voice rules](episode-speakers.md) in Script input
before dispatch. Platform generation owns scripts, translations and audio. Use
the supported pipeline, including combined operations; inspect saved outputs
read-only afterward. Do not require an invented intermediate review gate or
repair a generated script manually.

The [company asset preflight](company-asset-preflight.md) applies when a new
exercise is created, not to targeted regeneration, language/media work or
retries on an existing root. For those, check the dependencies of the selected
subpart and verify the saved output afterwards.

1. Call `content_generation_capabilities` with `content:read` immediately before
   choosing a format, subpart, or granular generation operation.
2. Confirm the current draft/active status and supported subparts. Present the
   active learner impact, Roleplay Knowledge binding when relevant, and exact
   generated subparts.
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
   check each requested artifact, linked completed step, readable saved output
   and any current failed/running attempt. Protected instruction text is omitted
   by MCP; use its server metadata. Readiness does not prove generator origin.

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
