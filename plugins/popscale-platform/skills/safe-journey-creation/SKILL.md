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
3. Establish the selected format mix, then complete the shared
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
4. Create or inspect a generation request, start it when requested, and poll
   `generation_request_detail` until it reaches a terminal or reviewable state.
   Do not invent successful completion while work is still queued or running.
5. Open `journey_plan_detail`. Review the overview and every item. Use
   `journey_plan_update_item_input` for specific edits and
   `journey_plan_update_overview` only after the user explicitly confirms the
   overview change.
   Present the plan's `generation_notes` verbatim; they are the generator's
   channel for trade-offs and thin sources. Show the scenario/customer mapping
   for every Roleplay item: `generate_new` creates a scenario, `link_existing`
   reuses an existing scenario (with `customer_id` or a new `customer_seed`),
   and `reuse_scenario` reuses the scenario of an earlier plan item named by
   `reuse_from_client_id` with a new `customer_seed`. Several sections can share
   one scenario with a different customer each; prefer that over near-identical
   scenarios. A `reuse_from_client_id` must point at an earlier Roleplay item,
   never forward or at itself. If the request set `format_mix`, check that the
   plan kept to it; the server treats the mix as advice, so correct drift
   through `journey_plan_update_overview` after confirmation.
   Check material use of the verified company sources. If format mix, sources,
   revisions or configuration change, repeat the affected preflight before
   generating item inputs or executing the plan; an old snapshot is not refreshed
   merely by re-reading current assets.
6. Call `journey_plan_validate_item_input` for every item that will be executed. Resolve all
   validation errors; never bypass server validation.
7. Call `render_journey_review` so App-capable hosts can show the interactive
   Journey Review. If the host cannot render the App, present the returned
   structured overview, item status, validation errors, and next actions in text.
8. Summarize the exact operation and ask for explicit confirmation immediately
   before any execution, activation, or publication call.
9. Only after confirmation, call `journey_plan_execute`. Poll the related request
   with `generation_request_detail` and use `journey_plan_reconcile` only
   when status or server guidance indicates reconciliation is appropriate.
   Read item statuses literally: `waiting_for_scenario` and
   `child_request_created` are not done; `linked` is done;
   `dependency_failed`, `child_request_failed`, `link_failed` and
   `invalid_input` are failures to report with the affected item. On a partial
   result, reconcile and retry the existing step; never create a second plan.
10. When the user asks to publish, first review the whole Journey against the
    public checklist (`/journeys/review-before-activation/`, fetched as the
    routing skill describes): empty sections, placeholder text, unfinished
    scored items, question counts, opening lines, section descriptions,
    passing-score policy, attempt rules within a section, naming and mix.
    Report findings in its three levels with a proposed value each; fix only
    what the user approves, through the content workflow. Then call
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
    steps, saved output and freshness; a completed plan or green Journey
    readiness does not prove child artifact provenance. Use the packaged local
    checker when available, or the same evidence rules without local execution.
    Report draft/published status, each part's provenance and freshness, remaining
    warnings, and a concise audit-friendly summary. A partial result is not a
    completed Journey generation.
    Repeat the preflight's source-use review on saved child exercises; a plausible
    plan does not prove that child outputs used the selected company sources.

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
