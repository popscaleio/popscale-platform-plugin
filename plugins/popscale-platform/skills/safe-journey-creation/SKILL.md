---
name: safe-journey-creation
description: Create or revise a Popscale learning journey from approved company knowledge with tenant checks, item validation, interactive review, and explicit confirmation before execution or publication. Use when a company admin asks to build, generate, review, validate, execute, or publish a Popscale journey.
---

# Safe Journey Creation

Create Popscale journeys through the `popscale-platform` MCP while keeping the
authenticated company, server validation, and human approval authoritative.

## Required Workflow

1. Call `current_user`, then `capabilities`.
2. Confirm the user is an active `company_admin`, the intended company matches
   the authenticated session, and the required journey/generation scopes exist.
   Inspecting or activating child content also requires `content:read`; activation
   additionally requires `content:write` and `publish:write`. Do not accept a
   company identifier from the prompt as an authorization input.
3. Inspect `knowledge_agent_context_manifest`, then use `knowledge_assets_list`
   and `knowledge_generation_context` for the approved, generation-eligible
   knowledge selected for this journey. If the stored manifest or selected
   context is missing or stale, explain the gap before generating.
4. Create or inspect a generation request, start it when requested, and poll
   `generation_request_detail` until it reaches a terminal or reviewable state.
   Do not invent successful completion while work is still queued or running.
5. Open `journey_plan_detail`. Review the overview and every item. Use
   `journey_plan_update_item_input` for specific edits and
   `journey_plan_update_overview` only after the user explicitly confirms the
   overview change.
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
    confirmation. Refresh readiness, present the final journey target, ask for a
    new publication confirmation, then call `journey_activate`.
11. Report the created draft/published object, remaining warnings, and a concise
    audit-friendly summary of actions taken.

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

## Failure Handling

- Authentication challenge: pause the workflow and ask the user to reconnect or
  reauthorize Popscale in the host.
- Wrong company: stop before reading or writing further data and reconnect using
  the intended company.
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
