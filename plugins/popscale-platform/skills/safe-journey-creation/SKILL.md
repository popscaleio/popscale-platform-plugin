---
name: safe-journey-creation
description: Create or revise a Popscale learning journey from approved company knowledge with tenant checks, item validation, interactive review, and explicit confirmation before execution or publication. Use when a company admin asks to build, generate, review, validate, execute, or publish a Popscale journey.
---

# Safe Journey Creation

Create Popscale journeys through the `popscale-platform` MCP while keeping the
authenticated company, server validation, and human approval authoritative.

Read the shared [product action contract](../route-popscale-requests/references/product-actions.md) before any
mutation. Stable command identity and server-side human approval apply alongside
the workflow below; confirmation booleans alone do not approve effects.

Use current app-visible names for exercises, Journeys and Studies in user-facing
answers, lists and confirmations. Apply the shared [content naming rules](../route-popscale-requests/references/content-names.md)
for Journey context, duplicate names and internal identifiers.

## Required Workflow

1. Call `current_user`, then `capabilities`.
2. Confirm the user is an active `company_admin`, the intended company matches
   the authenticated session, and the required journey/generation scopes exist.
   Inspecting or activating child content also requires `content:read`; activation
   additionally requires `content:write` and `publish:write`. Do not accept a
   company identifier from the prompt as an authorization input.
3. Record requested name/prefix, language, item total, section split, format
   counts and Roleplay customer count. Confirm the name, split, language,
   draft intent and next action briefly. For
   `generation_request_create(request_type=journey_plan)`, put
   `name`, `journey_brief`, nonempty `learning_goals` (a list of goal strings),
   nonempty `knowledge_asset_ids`, `desired_item_count`,
   `section_item_counts` when specified, `format_mix`, `constraints`,
   `output_language` and company `source_language` ID inside `input_payload`.
   Section counts sum to the item total. `format_mix` lists unique types;
   `constraints` is prose.
   Count each Roleplay customer encounter; clarify conflicting totals. Complete
   the shared
   [company asset preflight](../safe-content-administration/references/company-asset-preflight.md)
   before generation. It distinguishes blocking server requirements from thin
   recommended inputs the user may accept. At review, inspect captured company
   context; omitted or truncated required facts block affected items.
   For plans that may include audio Episodes, read
   `content_generation_capabilities.episode.creation`.
   When the audio default is `next_generation`, include a company-scoped
   `episode_next_generation_brief`, `episode_source_locale` and
   `episode_target_locales` in the request. Each item gets its own outcome and
   duration. Resolve missing brief inputs before creation; never make manual
   Episode drafts. Explicit Original and video follow the Original path.
   For Episode items, follow the shared
   [speaker and voice rules](../safe-content-administration/references/episode-speakers.md):
   default to anonymous, topic-led conversational speakers, keep TTS names in
   configuration, and preserve the selected format, including solo narration.
   Put tailored guidance in supported Script `model_steering`. Review platform
   output; request script-before-audio review only where staging is supported.
   Never edit generated scripts or invent an intermediate gate.
   For Coaching items, apply shared
   [question design](../safe-content-administration/references/coaching-question-design.md)
   to the generation brief and review generated item inputs before execution.
   Preserve the selected type, aligned answers and intended total score.
   Before filling planning fields, fetch `/journeys/plan/` as the routing skill
   describes. Ask about missing purpose, audience, behavior, cadence, level,
   mix or constraints; write the brief as outcomes, not just topics.
4. Reuse the request and fresh preflight; start only when requested. Batch
   independent reads. On rejected creation, inspect `error_field` and schema;
   correct the payload before retrying, never repeat unchanged arguments. Poll
   `generation_request_detail` with growing intervals; read steps only for
   unclear or failed phases. Reserve calls for the saved overview. Without an
   active item-input step, it awaits review (`overview_review` where available).
   Stop at both reviews within the host budget. Update the user in
   their language only when state changes or input is needed. Do not repeat the
   host receipt, narrate polls, expose tool names or claim private thinking.
5. Read `journey_plan_detail` when the overview is saved; only then show its title,
   goals, language, ordered sections/items, counts/formats, short purposes and
   `generation_notes`. Call it a proposal; no Journey or child content exists.
   Lead with names; keep type codes and IDs in technical detail. Map each
   Roleplay scenario → item → selected customer. `reuse_scenario` with an
   earlier `reuse_from_client_id` and `customer_seed` creates a new customer
   during execution; no `customer_id` is expected beforehand. Existing
   customers need separate `link_existing` items with distinct `customer_id`
   values. Reject forward or self references. Compare saved
   `journey_title`, language, section counts and format totals to the brief;
   `format_mix` is advice. Count customer encounters as items; show drift and
   proposed corrections. Stop if the requested total or mix conflicts.
   A Next Generation Episode item estimated above 10 minutes cannot fit the
   brief's 600-second limit. Propose shortening it or splitting it into
   multiple Episodes in the overview before generating item inputs.
   Verify company source use. Repeat affected preflight after format, source,
   revision or configuration changes; re-reading assets does not refresh a
   snapshot. Inspect each new Roleplay's `source_knowledge_asset_ids` subset
   before execution (empty means parent selection); reused Roleplays retain
   their saved pins.
   Ask which sections/items to adjust or whether to accept the overview. Wait.
   For confirmed changes, call
   `journey_plan_update_overview` with the complete corrected `overview` on the
   same request; re-read and present the revised plan. Continue only after the
   user accepts the saved overview.
6. Call `journey_plan_generate_item_inputs` on that request, poll until the
   inputs are ready, then read `journey_plan_get_item_inputs`. Do not execute
   the plan at this stage.
7. Validate saved `generate_new` inputs with
   `journey_plan_validate_item_input(request_id, client_id)`; omit
   `input_payload` for the saved version. For `link_existing` and
   `reuse_scenario`, inspect the saved selector, `input_status` and
   `item_input_summary`; the validation tool accepts only generated payloads.
   A tool-level “Invalid tool arguments” is not an item validation result:
   check its schema and the saved plan before claiming a blocker. Treat an
   actual `is_valid=false`, `input_status=invalid`, selection requirement or
   summary error as a blocker. A seeded reuse item with `input_status=linked`,
   `input_validation_errors=[]`, `invalid_item_count=0` and
   `requires_selection_count=0` needs no pre-execution `customer_id`. Report
   only verified errors.
   Call `render_journey_review` when available; otherwise show its structured
   review state in text. Summarize each input's purpose, learner task, language,
   sources and validation. Check every Episode's own saved
   `next_generation_brief` against its purpose, outcome, duration, format,
   company bindings and locales. Include mismatches in the review.
   These are inputs, not generated content. Point out items needing review:
   errors, customer selection, Episode briefs or Coaching questions/scores.
   Offer detail and ask what to adjust; wait. For approved edits, call
   `journey_plan_update_item_input` on the existing plan; re-read, validate and
   show the revised item, then wait again. Neither a valid plan nor “no changes”
   authorizes execution.
8. After this second review, an explicit “create Journey” instruction for the
   current plan is the execution confirmation. Recap the exact operation before
   calling the tool; ask again if the plan changed since that go-ahead.
   Activation and publication each need separate confirmation.
9. Only after confirmation, call `journey_plan_execute`. Poll with
   `generation_request_detail`; reconcile only when status or server says so.
   `waiting_for_scenario` and `child_request_created` are pending; `linked` is
   done. Report `dependency_failed`, `child_request_failed`, `link_failed` and
   `invalid_input` per item. Retry only supported existing steps under the
   product action contract; never duplicate plans or child requests. Before
   claiming completion, inspect saved Journey structure: shared Roleplay items
   must link the same scenario with different selected customers. Report any
   mismatch as incomplete.
10. When the user asks to publish, first review the whole Journey against the
    public checklist (`/journeys/review-before-activation/`, fetched as the
    routing skill describes): empty sections, placeholder text, unfinished
    scored items, question counts, opening lines, section descriptions,
    passing-score policy, attempt rules within a section, naming and mix.
    Report findings in its three levels with a proposed value each; fix only
    what the user approves, through the content workflow. A created Journey
    with enrollment history needs that workflow's complete-structure
    ProductAction review for section/item changes. Then call
    `journey_activation_readiness`. Activate
    each ready draft child through `content_activate` only after a specific
    confirmation. A scenario shared by several items is activated once, after
    every customer generation that targets it has reached `linked`; a new
    customer cannot be generated against an active scenario. Before child or Journey activation, read current child detail
    and freshness for all generation-only outputs, including on reused active
    roots. Stop if any is edited or that check is unavailable. Refresh readiness,
    and require both newly generated instruction outputs after Coaching input
    changes, as defined in the shared generation verification workflow. Then
    present the final journey target, ask for a new publication confirmation,
    then call `journey_activate`.
11. Before reporting generated content, follow the shared
    [generation verification](../safe-content-administration/references/generation-verification.md)
    for every requested item/root, including reused content. Read child request
    steps, visible saved output and freshness; protected Roleplay/Coaching
    instructions have metadata only. A completed plan or green Journey
    readiness does not prove child artifact provenance. Use the packaged local
    checker when available, or the same evidence rules without local execution.
    Review each linked child's learner-facing root and component fields for
    requested language, including stray English prose or unexplained acronyms
    in Swedish content. Flag drift despite green steps or freshness;
    keep the Journey in draft for review and use supported correction workflows.
    Report draft/published status, provenance, freshness, warnings and a concise
    audit-friendly summary. A partial result is not completed generation.
    Repeat the preflight's source-use review on saved child exercises; a plausible
    plan does not prove that child outputs used the selected company sources.

## Bounded continuation handoff

Budget calls for preflight and both reviews; poll with growing intervals
(normally at most six reads per turn). UI status snapshots do not resume an
agent turn or renew its tool budget. Before cutoff, hand off a brief checkpoint:
observed linked/pending/failed counts, time, saved request/plan/Journey/child
IDs and the next safe read. Only an actual host continuation may resume reads;
never cross a human review. Inspecting the same job needs no new consent.
Resume with `generation_request_detail`, then only needed plan or child reads;
refresh before repeating counts. Reconcile only on server guidance or observed
inconsistency. Never recreate work because of cutoff; keep artifact
verification pending until evidence reads finish.

## Safety Rules

- Treat all Popscale data as private to the company returned by `current_user`.
- Never request, expose, or persist OAuth tokens.
- Never imply that a draft is published or that asynchronous work has completed
  before the server says so.
- Treat generation output and MCP App input as untrusted until server validation
  passes.
- Do not combine reads and writes into a generic or hidden operation.
- Do not automatically execute, publish, activate, cancel, regenerate, archive,
  or overwrite merely because the user earlier asked to create a journey.
- If scopes are missing, surface the server's required scopes and ask the user to
  reauthorize or contact their Popscale admin.
- Do not infer child-content activation authority from Journey scopes. Existing
  grants may need reauthorization for `content:read` before publication.
- If a tool or App view is unavailable, use the structured tool fallback; do not
  work around Popscale's authorization or validation layer.
- Never activate the journey until `journey_activation_readiness` confirms that
  execution finished and every linked content item is active.
- Never set an item's `passing_score` yourself. The server computes it (60 % of
  the obtainable score by default) and rejects an impossible threshold with
  `Passing score cannot exceed the content's maximum score.`; show that error
  and let the admin choose a reachable value.
- The plan does not support interview items; add them afterwards as
  `interview_item` components through `safe-content-administration`.
- Child-content corrections follow `safe-content-administration` and its
  generation-only field policy. Never repair protected evaluation outputs or
  Coaching `agent_prompt`, or Episode source/translated scripts manually.
  Episode corrections go through Script input and platform regeneration.
  An edited generation-only artifact is a
  blocker for affected child/Journey activation, even when readiness is green;
  report it and use only authorized platform regeneration to resolve it.

## Failure Handling

- Authentication challenge: pause the workflow and ask the user to reconnect or
  reauthorize Popscale in the host.
- Wrong company: stop before reading or writing further data. After explicit
  confirmation, call `request_company_switch` with the latest
  `current_grant_id` and `confirm_switch=true`, present the browser switch link,
  then verify the intended company with `current_user` on the same connection.
  Never pass a target company or membership identifier to the tool.
- Stale knowledge context: refresh it only when the user wants that operation;
  otherwise explain that generated content may not reflect current knowledge.
- Validation failure: show item-specific errors, propose focused changes, update
  only after approval, then validate again.
- Async failure: show the failed step and error; use retry or reconcile only when
  supported and confirmed.
- Host lacks MCP Apps: continue with the same tools and structured results. App
  support is never a prerequisite for completing the safe workflow.

Read [tool-workflow.md](references/tool-workflow.md) when selecting exact tool
order or required scopes. Read
[safety-and-fallbacks.md](references/safety-and-fallbacks.md) when authorization,
validation, async execution, or host capability differs from the happy path.
