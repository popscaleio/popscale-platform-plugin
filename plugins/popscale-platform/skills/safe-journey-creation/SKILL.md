---
name: safe-journey-creation
description: Create or revise a Popscale learning journey from approved company knowledge with tenant checks, item validation, scoped user authorization, and platform-required approvals. Use when a company admin asks to build, generate, review, validate, execute, or publish a Popscale journey.
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
   counts and Roleplay customer count. State the understood name, split, language,
   draft intent and next action briefly; ask only about consequential gaps. For
   `generation_request_create(request_type=journey_plan)`, put
   `name`, `journey_brief`, nonempty `learning_goals` (a list of goal strings),
   nonempty `knowledge_asset_ids`, `desired_item_count`,
   `section_item_counts` when specified, `format_mix`, `constraints`,
   `output_language` and company `source_language` ID inside `input_payload`.
   Section counts sum to the item total. `format_mix` lists unique types;
   `constraints` is prose.
   Count Roleplay encounters; clarify conflicting totals. Run
   [company asset preflight](../safe-content-administration/references/company-asset-preflight.md)
   before generation. Server requirements block; recommended gaps warn. Inspect
   captured context; omitted/truncated required facts block affected items.
   Select Knowledge by eligibility, relevance and metadata. Do not default to
   test/demo assets when suitable real sources exist; ask if intent is unclear.
   A changed plan-level source set needs a new request because its Knowledge
   snapshot is frozen. Carry forward approved title, goals, language, section
   split, formats, durations and constraints unless the user changes them.
   A Challenge is a practical task with a written response, not a question quiz.
   For a requested knowledge check, explain supported question-based options
   such as Coaching or Flashcards and confirm any format substitution.
   For plans that may include audio Episodes, read
   `content_generation_capabilities.episode.creation`.
   When the audio default is `next_generation`, include a company-scoped
   `episode_next_generation_brief`, `episode_source_locale` and
   `episode_target_locales` in the request. Each item gets its own outcome and
   duration. Resolve missing brief inputs before creation; never make manual
   Episode drafts. Explicit Original and video follow the Original path.
   Apply [speaker and voice rules](../safe-content-administration/references/episode-speakers.md)
   to Episode briefs, Script `model_steering` and output review: anonymous by
   default, TTS names in configuration, selected format preserved. Stage only
   where supported; never manually edit scripts or invent gates.
   For Roleplay/Coaching items, apply shared
   [conversation assessment](../safe-content-administration/references/conversation-assessment.md)
   to briefs, item inputs and saved children before activation, including
   participant information.
   For Coaching items, apply shared
   [question design](../safe-content-administration/references/coaching-question-design.md)
   to the generation brief and review generated item inputs before execution.
   Preserve the selected type, aligned answers and intended total score.
   Fetch `/journeys/plan/` before writing outcome-based planning fields. Apply
   shared defaults to minor cadence, level or style gaps; ask only about material
   choices or purpose/audience/behavior that cannot be inferred.
4. Reuse the request and fresh preflight under creation intent. Batch reads.
   On rejection, inspect `error_field`/schema and correct before retrying.
   Poll `generation_request_detail` with growing intervals; read steps for
   unclear/failed phases. Reserve reads for both saved quality checks. Without
   an active item-input step, `overview_review` awaits the next supported action,
   not necessarily another chat yes. Honor requested/platform stops and unresolved
   decisions. Update in the user's language on changed state or needed input;
   omit repeated receipts, poll narration, tool names and private-thinking claims.
5. Read saved `journey_plan_detail`: title, goals, language, ordered sections/items,
   counts/formats, purposes and `generation_notes`. Present it as a proposal,
   not created content; use names with codes/IDs in technical detail. Map each
   Roleplay scenario → item → selected customer. `reuse_scenario` with an
   earlier `reuse_from_client_id` and `customer_seed` creates a new customer
   during execution; no `customer_id` is expected beforehand. Existing
   customers need separate `link_existing` items with distinct `customer_id`
   values. Reject forward or self references. Compare saved
   `journey_title`, language, section counts, formats, per-item minutes and
   total duration to the last approved brief, including after source-driven
   recreation. `format_mix` is advice. Correct drift to already approved,
   server-valid values with `journey_plan_update_overview`, then re-read before
   review; do not invent fixed platform estimates. Stop on conflicting totals.
   A Next Generation Episode item estimated above 10 minutes cannot fit the
   brief's 600-second limit. Propose shortening it or splitting it into
   multiple Episodes in the overview before generating item inputs.
   Verify plan-level `knowledge_asset_ids` and its frozen snapshot separately
   from each new Roleplay's `source_knowledge_asset_ids` subset (empty means
   parent selection); reused Roleplays retain their pins. Removing an item pin
   does not remove a plan source. For a requested source removal, verify the
   whole effect, explain the locked snapshot and agree on recreation. Repeat
   affected preflight after format, source, revision or configuration changes.
   Honor requested review stops; unresolved material decisions block dependents.
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
   Use `render_journey_review` when available, otherwise text. Check each saved
   input's purpose, learner task, language, sources and validation. Check each
   Episode's `next_generation_brief` outcome, duration, format, company bindings
   and locales. Correct in-scope issues with `journey_plan_update_item_input`;
   re-read and validate. Surface unresolved errors/selections or brief/question/
   score decisions. These are inputs, not generated content.
8. Recap execution against the authorized scope. Reuse clear creation intent;
   respect planning-only requests, requested checkpoints and platform approvals.
   Ask about unresolved material changes; validation supplies no authorization.
9. Call `journey_plan_execute` under that intent and platform approvals. Poll
   `generation_request_detail`; reconcile only on status/server guidance.
   `waiting_for_scenario`/`child_request_created` are pending; `linked` is done.
   Report `dependency_failed`, `child_request_failed`, `link_failed`, `invalid_input`
   per item. Continue supported independent child jobs under the shared local-
   blocker rule; never bypass whole-plan validation, drop items or duplicate jobs.
   Retry supported existing steps under the shared contract. Verify saved structure:
   shared Roleplay encounters
   need one scenario and distinct customers. Require `journey_draft_ready` and
   every requested saved link for completion. Give short pending status and
   supported navigation/Open controls; keep IDs in technical detail.
10. When the user asks to publish, first review the whole Journey against the
    public checklist (`/journeys/review-before-activation/`, fetched through
    routing): structure, text, scoring, attempts, naming and format mix.
    Correct in-scope issues through the content workflow without per-finding
    questions. Group unresolved or out-of-scope decisions for the user. A created Journey
    with enrollment history needs that workflow's complete-structure
    ProductAction review for section/item changes. Then call
    `journey_activation_readiness`. Activate
    each ready draft child through `content_activate` under the publication
    instruction when its scope includes those children; obtain any missing intent
    together and retain each platform-required approval. A scenario shared by several items is activated once, after
    every customer generation that targets it has reached `linked`; a new
    customer cannot be generated against an active scenario. Before child or Journey activation, read current child detail
    and freshness for all generation-only outputs, including on reused active
    roots. Stop if any is edited or that check is unavailable. Refresh readiness,
    and require both newly generated instruction outputs after Coaching input
    changes, as defined in the shared generation verification workflow. Then
    present the final Journey target and call `journey_activate` under the same
    publication intent if unchanged, following its own platform approval.
11. Follow [generation verification](../safe-content-administration/references/generation-verification.md)
    for every requested/reused root: child steps, visible output and freshness;
    protected Roleplay/Coaching instructions have metadata only. Use the local
    checker when available, otherwise its evidence rules. Green plan/readiness
    proves no child provenance. Check saved children's source use, participant
    information and language, including English/acronyms in Swedish fields.
    Correct within scope; leave unresolved material drift in draft. Report
    publication, provenance, freshness and remaining work separately.

## Bounded continuation handoff

Budget calls for preflight and both quality checks; poll with growing intervals
(normally at most six reads per turn). UI activity counts are not tool-call
counts; snapshots do not resume an agent turn or renew its tool budget. Before
cutoff, hand off a brief checkpoint:
observed linked/pending/failed counts, time, saved request/plan/Journey/child
IDs and next read, keeping IDs internal. Resume only on host continuation;
honor requested/platform review stops. Job inspection needs no new consent.
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
- Reuse explicit creation intent for draft execution. Publication, distribution,
  cancellation, archive and broader overwrites require matching intent, which may
  be part of the same instruction; retain platform approval for each effect.
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
- Wrong company: follow routing and `request_company_switch`. Use latest
  `current_grant_id`, `confirm_switch=true` and explicit switch intent; no target
  identifier. Verify `current_user` on the same connection after browser approval.
- Stale knowledge context: refresh it only when the user wants that operation;
  otherwise explain that generated content may not reflect current knowledge.
- Validation failure: correct within scope and revalidate. Continue independent
  preparation; whole-plan execution waits for all required items. Ask about material changes.
- Async failure: inspect the existing job; retry/reconcile only when supported,
  within authorized scope/cost and permitted by the current platform approval.
- Host lacks MCP Apps: continue with the same tools and structured results. App
  support is never a prerequisite for completing the safe workflow.

Read [tool-workflow.md](references/tool-workflow.md) when selecting exact tool
order or required scopes. Read
[safety-and-fallbacks.md](references/safety-and-fallbacks.md) when authorization,
validation, async execution, or host capability differs from the happy path.
