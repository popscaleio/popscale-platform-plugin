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

Use current app-visible names for exercises, Journeys and Studies in user-facing
answers, lists and confirmations. Apply the shared [content naming rules](../route-popscale-requests/references/content-names.md)
for Journey context, duplicate names and internal identifiers.

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
   stable-ID row. Preserve pagination and truncation indicators. For enrolled
   Journeys, read the complete structure with `journey_structure_get`.
   For Coaching input authoring or review, apply
   [question design](references/coaching-question-design.md): one primary goal,
   type-appropriate progression, aligned answers and preserved total score.
   Before authoring new or rewritten input, fetch the matching writing guide
   from `popscale-docs` as described in the routing skill's "Before authoring"
   step (`/content/writing-good-input/` and the format-specific guides) and ask
   for what it says is missing. The guide shapes the input; the platform owns
   the generation.
4. Before changing an object, record the root `revision`, status, editable
   fields, component type, and exact requested delta. Prefer one focused root or
   component mutation over replacing a collection or unrelated fields.
   For customer behavior changes, check related rules and outcomes for
   contradictions using the Roleplay guidance in
   [content-format-map.md](references/content-format-map.md).
   Exclude the generation-only outputs (Safety Rules) from every create and
   update payload, including component payloads; use the packaged checker's
   `--check-manual-write` mode when local Python is available.
5. Pass the latest root `revision` as `expected_revision` for every protected
   mutation. Refresh after each successful mutation because root revision
   changes. For enrolled Journey sections/items, follow
   [content-format-map.md](references/content-format-map.md). On conflict,
   re-read and reconcile the
   user's requested delta; never retry blindly.
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
8. Before creating a new exercise, run the shared
   [company asset preflight](references/company-asset-preflight.md) for the target
   format: stop only on what the server requires, warn about thin recommended
   inputs and offer to fill them, then generate when the user decides. The
   preflight does not apply to targeted regeneration or language generation;
   those check only the selected subpart's dependencies. For new generated
   Coaching/Flashcards, read [standalone generation](references/standalone-generation.md)
   for payload shape and follow-through. Call
   `content_generation_capabilities` and follow the returned format/subpart
   contract. Create a new Episode through `generation_request_create`, never
   `create_company_content`; use the company-reported audio mode and the
   structured Next Generation brief and locales when that mode is enabled.
   An explicit request for Original remains available. For existing-root
   regeneration, follow the intent, replacement/append consent, language and
   dependency rules in [tool-workflow.md](references/tool-workflow.md), preserving
   IDs and Journey links. Read detail/freshness and capabilities first;
   never queue extra subparts or claim synchronization from source edits alone.
   Choose from intent, never from what is available. Changed criteria mean
   `evaluation_criteria`, which replaces the whole criteria list; explain and confirm it.
   **Coaching exception:** any Coaching input change regenerates BOTH
   `agent_prompt` and `evaluation_instructions` afterwards, never only the one
   marked stale and never an older run. If the pair cannot be generated, report
   the update as incomplete.
   For Episodes, apply [speaker and voice rules](references/episode-speakers.md)
   to Script input (`model_steering`), listening guidance, review and supported
   combined generation.
   Stop active input corrections when safe regeneration is unavailable.
9. Before publication, review the root against the public checklists: fetch
   `/journeys/review-before-activation/` and `/content/language-in-exercises/`
   from `popscale-docs` (see the routing skill's "Before authoring" step) and
   read every learner-facing field with them. Report findings in the
   checklist's three levels (stops activation, breaks a rule, cosmetic) with a
   proposed value per finding; change nothing without a yes per finding, and
   never touch generation-only outputs. Then read detail and freshness for
   every generation-only output on the root; an edited one blocks activation
   regardless of readiness.
   Call `content_activation_readiness`, present every failed or warning check,
   and call `content_activate` only after immediate explicit confirmation with
   `confirm_publish=true`.
10. Follow [generation-verification.md](references/generation-verification.md)
    before generation claims, using the evidence checker when available. Read
    visible saved output and source use; verify redacted instructions through
    metadata only. Report content names, draft/publication status, generation,
    freshness, provenance and concrete remaining review needs separately.
    Never invent links, fields, completion, permissions or hidden output text.

## Safety Rules

- Treat every result as private to the company returned by `current_user`.
- Never send customer content, generated artifacts, identifiers, or OAuth
  material to `popscale-docs`.
- **Generation-only outputs** are Roleplay `evaluation_instructions`; Coaching
  `evaluation_instructions` and `agent_prompt`; Challenge `evaluation_prompt`;
  Episode `script` and variant `script_text`. Never write, patch, translate,
  clear or repair them through any tool, payload or override flag, even when
  the schema permits it or the user asks for manual text; route the change
  through source inputs and platform generation, and treat an unavailable
  generation path as a blocker. An edited one (freshness `output_edited` or
  `source_changed_and_output_edited`) is a workflow failure that stops
  synchronization claims and activation until regeneration and saved-output
  verification resolve it; green readiness cannot clear it.
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
- Do not expose or reconstruct bounded, masked, omitted, or cross-company data.
- `delete_content_component` requires a specific delete confirmation.
  `reorder_content_components` replaces one complete bounded ordering scope;
  verify every stable ID before calling it.
- `set_content_departments` replaces the complete assignment set. Resolve every
  department through the company-scoped reference tool and show the before/after
  set first.
- Targeted regeneration and language generation can update active content when
  the live catalog permits it. Check each requested subpart and status; active
  multi-step work can show intermediate output. Card and generated-customer
  operations are append-only where the live catalog says so.
- Roleplay customers are added one at a time with
  `create_content_component` (`roleplay_customer`) after the scenario exists.
  Always state `number_of_customers` explicitly when creating a Roleplay,
  normally `1`; the server default is `5`, and a high value is not a way to get
  variety.
- For a Coaching session of type `assessment`, `session_description`,
  `coaching_context` and other learner-visible fields must not contain
  questions, answers or reference material; those belong in `reference_facts`.
  The server generates the description and education text from limited input;
  do not rewrite them with answers.
- Read-only media components are evidence, not editable fields. Use dedicated
  upload-intent tools only when the user separately asks to upload supported
  media and the required media scope is available.

Read [tool-workflow.md](references/tool-workflow.md) for exact tool and scope
selection. Read [content-format-map.md](references/content-format-map.md) when
choosing a root, component, or generation target. Read
[safety-and-fallbacks.md](references/safety-and-fallbacks.md) for stale edits,
active content, bounded results, and partial failures. Read
the host evaluation scenarios in the repository's `docs/evaluation/` directory when validating a
host or changing the Product MCP catalog.
