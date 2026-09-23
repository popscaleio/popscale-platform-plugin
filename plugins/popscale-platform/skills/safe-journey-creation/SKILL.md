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
   approved, active, generation-eligible Knowledge. Verify substantive source
   content, saved revisions and inclusion in the actual generation context;
   missing or unverifiable required inputs stop generation. Knowledge context
   reads may diagnose gaps but do not replace this gate.
   For Episode items, apply the shared
   [speaker and voice rules](../safe-content-administration/references/episode-speakers.md)
   to planning, item inputs and execution. Default to anonymous, topic-led
   dialogue; TTS names are configuration, never inferred host identities.
   Do not invent recurring podcast profiles. Require a supported script review
   or equivalent validation gate before audio generation, including translations.
4. Create or inspect a generation request, start it when requested, and poll
   `generation_request_detail` until it reaches a terminal or reviewable state.
   Do not invent successful completion while work is still queued or running.
5. Open `journey_plan_detail`. Review the overview and every item. Use
   `journey_plan_update_item_input` for specific edits and
   `journey_plan_update_overview` only after the user explicitly confirms the
   overview change.
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
10. When the user asks to publish, call `journey_activation_readiness`. Activate
    each ready draft child through `content_activate` only after a specific
    confirmation. Before child or Journey activation, read current child detail
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
- Child-content corrections follow `safe-content-administration` and its
  generation-only field policy. Never repair protected evaluation outputs or
  Coaching `agent_prompt` manually. An edited generation-only artifact is a
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
