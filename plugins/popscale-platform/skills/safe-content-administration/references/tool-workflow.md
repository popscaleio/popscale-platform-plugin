# Content Administration Tool Workflow

Discover the live catalog with `capabilities`. Tool availability, returned
schemas, and authorization remain authoritative over this reference.

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
`expected_revision`. Refresh root detail after success. Active content also
requires `confirm_active_edit=true` after the user approves the exact edit.
Deletion requires `confirm_delete=true`; archive requires
`confirm_archive=true` and may require a separate learner-impact confirmation.

Use component CRUD for a single roleplay customer/question/objection/decision
rule/criterion, episode script variant, flashcard/card translation, or journey
section/item. Use `content_update` for scalar root edits and directly addressable
child edits when no collection operation is needed.

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
   that separate mutation.
6. Refresh `content_detail`, `list_content_components`, and
   `get_content_freshness` after completion before reporting the generated
   result.

An idempotency key replay is safe only for identical input. A conflict means the
key was already used for different work; create a new key rather than mutating
or bypassing the request.

## Activation

`content_activation_readiness` and `content_activate` require `content:read`,
`content:write`, and `publish:write`. Activation is available for roleplays,
coaching sessions, challenges, episodes, and flashcard decks—not Journeys.
Existing Journey publication remains in `safe-journey-creation` through
`journey_activation_readiness` and `journey_activate`.

Present the exact target, current revision/status, readiness checks, and
learner-visible consequence. Obtain immediate confirmation, then call
`content_activate` with `confirm_publish=true`. Refresh detail after success.
