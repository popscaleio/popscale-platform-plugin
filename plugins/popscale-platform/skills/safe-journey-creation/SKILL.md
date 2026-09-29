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
   counts and Roleplay customer count. Confirm the brief and next action in one
   or two plain-language sentences, including name, split, language and draft
   intent. For
   `generation_request_create(request_type=journey_plan)`, put
   `name`, `desired_item_count`, `format_mix`, `journey_brief`, `constraints`,
   `output_language` and company `source_language` ID inside `input_payload`.
   `format_mix` lists unique types, not counts; `constraints` is plain text.
   Put exact counts and section allocation in the brief or constraints.
   Two customers in one Roleplay count as one item; verify its generated
   `input_payload.number_of_customers: 2` before execution. Then complete the shared
   [company asset preflight](../safe-content-administration/references/company-asset-preflight.md)
   before generating an overview, item inputs or child exercises. It requires
   `content:read` for company assets/configuration and `knowledge:read` for
   approved, active, generation-eligible Knowledge. Stop only on server
   requirements: configured models and voice, a Company Overview when the mix
   includes Roleplays, and at least one selected generation-eligible Knowledge
   asset. Thin recommended inputs are a warning with an offer to fill them; the
   user decides whether to generate anyway. Read the plan's captured company
   context at review and treat omitted or truncated required facts as blockers
   for the affected items.
   For Episode items, apply the shared
   [speaker and voice rules](../safe-content-administration/references/episode-speakers.md)
   to planning, item inputs and execution. Default to anonymous, topic-led
   dialogue; TTS names are configuration, never inferred host identities.
   Do not invent recurring podcast profiles. Put the rules in the item's
   supported Script input (`model_steering`) and let platform generation produce
   scripts, translations and audio. Include tailored conversational-quality
   guidance and review saved outputs. Prefer script review before audio only
   when the actual Journey operation supports staging; otherwise review after
   supported combined generation. Never edit generated Episode scripts or
   require an unsupported intermediate review gate.
   For Coaching items, apply shared
   [question design](../safe-content-administration/references/coaching-question-design.md)
   to the generation brief and review generated item inputs before execution.
   Preserve the selected type, aligned answers and intended total score.
   Before filling `journey_brief`, `learning_goals`, `desired_item_count`,
   `difficulty` and `format_mix`, fetch the Journey planning guide
   (`/journeys/plan/`) as described in the routing skill's "Before authoring"
   step, and ask the user for whichever of its seven questions the request
   leaves open (why now, for whom, what they should be able to do, duration and
   cadence, level, mix, constraints). A brief written as topics produces a
   list; a brief written as behaviors produces a program.
4. Create or inspect a request, start it when requested, and poll
   `generation_request_detail` within a bounded window. Use the handoff below
   if time or tool budget ends; never claim completion while it runs.
5. After overview generation, read `journey_plan_detail`. Present the saved
   title, requested goals and language, ordered sections/items, counts/formats,
   and each item's short summary and purpose. Call this a proposed plan: no
   Journey or child content exists yet. Show the plan's `generation_notes` and each
   Roleplay's scenario/customer mapping: `generate_new` creates a scenario,
   `link_existing` selects an existing scenario and `customer_id` or new
   `customer_seed`; `reuse_scenario` uses an earlier `reuse_from_client_id` and
   new `customer_seed`. Prefer scenario reuse over duplicates; never reference
   a later item or itself. Compare saved
   `journey_title`, language, section counts and format totals to the brief;
   `format_mix` is advice. Show exact drift and proposed corrections.
   Check material use of the verified company sources. If format mix, sources,
   revisions or configuration change, repeat the affected preflight before
   generating item inputs or executing the plan; an old snapshot is not refreshed
   merely by re-reading current assets. The parent Knowledge snapshot informs
   planning; each new Roleplay item's `source_knowledge_asset_ids` selects its
   child subset (empty means the full parent selection). Inspect that subset
   before execution. An existing or reused Roleplay keeps its own saved pins;
   do not silently replace them with the plan's assets.
   Ask what the user wants to adjust and wait. For confirmed changes, call
   `journey_plan_update_overview` with the complete corrected `overview` on the
   same request; re-read and present the revised plan. Continue only after the
   user accepts the saved overview.
6. Call `journey_plan_generate_item_inputs` on that request, poll until the
   inputs are ready, then read `journey_plan_get_item_inputs`. Do not execute
   the plan at this stage.
7. Validate every item with `journey_plan_validate_item_input`; report errors.
   Call `render_journey_review` when available; otherwise show its structured
   review state in text. Summarize each saved input's purpose, learner task,
   language, sources and validation state. These are generation inputs, not
   generated child content. Offer item-level detail and ask what to review or
   adjust; wait for the user's answer. For approved edits, call
   `journey_plan_update_item_input` on the existing plan; re-read, validate and
   show the revised item, then wait again. Neither a valid plan nor “no changes”
   authorizes execution.
8. After this second review, an explicit “create Journey” instruction for the
   current plan is the execution confirmation. Recap the exact operation before
   calling the tool; ask again if the plan changed since that go-ahead.
   Activation and publication each need separate confirmation.
9. Only after that confirmation, call `journey_plan_execute`. Poll the related
   request with `generation_request_detail` and use `journey_plan_reconcile` only
   when status or server guidance indicates reconciliation is appropriate.
   Read item statuses literally: `waiting_for_scenario` and
   `child_request_created` are not done; `linked` is done;
   `dependency_failed`, `child_request_failed`, `link_failed` and
   `invalid_input` are failures to report with the affected item. On a partial
   result, reconcile only when status or server guidance calls for it; retry
   only the supported existing step under the product action contract. Never
   create a second plan or child request.
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
    requested language. Flag drift despite green steps or freshness;
    keep the Journey in draft for review and use supported correction workflows.
    Report draft/published status, provenance, freshness, warnings and a concise
    audit-friendly summary. A partial result is not completed generation.
    Repeat the preflight's source-use review on saved child exercises; a plausible
    plan does not prove that child outputs used the selected company sources.

## Bounded continuation handoff

Poll with growing intervals (normally at most six reads per turn). Give brief
plain-language milestones and the next step. At a cutoff, report observed
linked/pending/failed counts with observation time; keep request, plan, Journey
and child IDs in the handoff, not the main answer unless needed for clarity.
Explain that the same operation will continue without duplicate jobs. Resume
with `generation_request_detail`, then `journey_plan_detail` and child status as
needed; refresh before repeating earlier counts. Reconcile only when refreshed
state or server guidance calls for it under the product action contract. Never
recreate a request, plan, Journey or child job due to a cutoff. Mark artifact
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
