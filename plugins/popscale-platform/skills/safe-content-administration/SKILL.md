---
name: safe-content-administration
description: Find, inspect, create, and granularly edit company-scoped Popscale learning content, including roleplays, coaching sessions, challenges, episodes, flashcards, and existing journeys, with revision checks and safe generation or publication boundaries. Use when a company admin asks to manage existing Popscale content rather than design and execute a new journey plan.
---

# Safe Content Administration

Administer existing company content through `popscale-platform` while keeping the
OAuth-selected company, current server catalog, focused edits, and explicit
confirmation boundaries authoritative.

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
5. Pass the latest root `revision` as `expected_revision` for every protected
   mutation. Refresh after each successful mutation because root revision
   changes. On conflict, re-read and reconcile the user's requested delta; never
   retry blindly.
6. For active content, present the learner-visible consequence and obtain
   immediate explicit approval before setting `confirm_active_edit=true`.
   Editing approval does not authorize deletion, reordering, archiving,
   regeneration, reassignment, or publication.
7. Before deleting, reordering, replacing department assignments, or archiving,
   inspect `get_content_usage`. Use the dedicated confirmation required by the
   tool and describe any learner or journey impact.
8. Before generation, call `content_generation_capabilities` and follow the
   returned format/subpart contract. Generation is draft-only, asynchronous,
   and idempotent. Poll the returned request with `generation_request_detail`
   and `generation_request_steps`; do not claim completion early.
9. Before publication, call `content_activation_readiness`, present every failed
   or warning check, and call `content_activate` only after immediate explicit
   confirmation with `confirm_publish=true`.
10. Report server-returned IDs, revisions, status, change history/freshness,
    generation state, and remaining warnings. Never invent a URL, field,
    component, completion state, or permission.

## Safety Rules

- Treat every result as private to the company returned by `current_user`.
- Never send customer content, generated artifacts, identifiers, or OAuth
  material to `popscale-docs`.
- Use `content:read` for inspection; focused mutations additionally require
  `content:write`. Supported generation workflows also require
  `generation:read` for voice discovery and asynchronous status/step reads;
  targeted regeneration requires `content:write` and `generation:write`, while
  language generation additionally requires `content:read` and
  `generation:write`. Activation additionally requires `publish:write`.
- Existing grants are not widened automatically. Surface the server's missing
  scopes and ask the user to reconnect or reauthorize instead of requesting a
  bearer token.
- Treat `allowed_fields`, component types, generation capabilities, readiness,
  and validation errors returned by the server as authoritative. Never work
  around them through generic REST calls or guessed fields.
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
