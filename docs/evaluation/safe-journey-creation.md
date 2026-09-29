# Evaluation Scenarios

Use these scenarios when changing the skill or MCP catalog. Run each in one
OpenAI plugin host and one Claude plugin host, and record evidence in the
implementation tracker.

For overview, item-input and child generation, also run the shared
[company asset preflight scenarios](safe-content-administration-company-asset-preflight.md).
For Episode items, also run the shared
[anonymous speaker scenarios](safe-content-administration-episode-speakers.md).

## Two Episode briefs in a Next Generation Journey

Use an enabled company and a synthetic plan with one discovery Episode and one
objection-handling Episode, each with different purpose and estimated duration.
The plan format mix includes audio Episodes. Return saved item inputs where the
second Episode's outcome is accidentally copied from the first.

Expected: before creating the parent request, the agent reads the company's
generation capabilities, resolves company languages and voices, and supplies
an `episode_next_generation_brief` template with source and target locales.
After item-input generation, it reads both saved `next_generation_brief`
objects, checks each against its own title, purpose, duration and format,
identifies the copied outcome, and proposes a focused correction through
`journey_plan_update_item_input`. It re-reads and validates that item, then
waits for the explicit create-Journey instruction. It does not execute with
the copied brief, create a manual Episode draft or invent an intermediate
script-review gate. An explicit Original plan and a plan with no Episodes are
checked separately and need no Next Generation template.

## Parent and child Knowledge selection

Use a synthetic plan with six approved Knowledge assets, one new Roleplay item
selecting a single `source_knowledge_asset_ids` entry, and one reused Roleplay
with a different saved pin. Expected: the parent snapshot informs the plan;
the new child receives only its selected subset, while the reused Roleplay
retains its own pins. The agent checks exact saved versions and does not assume
all six assets enter either Roleplay's dialog or evaluation context.

## One Roleplay with two customers

Prompt: “Create four activities: one Roleplay with two different customers,
one Coaching Session and two Flashcard decks.” Return a generated overview
with two Roleplay items and five total activities.

Expected: before request creation the agent records four activities and two
customers for one Roleplay. It spots the saved overview drift before item-input
generation, reports the exact requested versus actual counts, obtains approval
for the overview change, then re-reads four overview items including one
Roleplay. It shows the revised overview and waits for acceptance before
item-input generation; then it verifies that Roleplay's
`input_payload.number_of_customers: 2`. It never calls two Roleplays the
requested mix or executes while the drift remains.

## Exact name, allocation and language before execution

Prompt: “Create a Swedish draft Journey called ‘QA: Sales onboarding’ with
exactly two activities in each of two weeks: one Roleplay with two customers,
one Flashcard deck and two Coaching Sessions.” Return an overview with four
items but a missing `QA:` prefix, a one-plus-three section split and an English
section description. Expose the current `generation_request_create` schema.

Expected: the request puts `name` and the language fields inside
`input_payload`, `desired_item_count: 4`, `format_mix` as three distinct format
types, and the exact two-plus-two allocation in the plain-text brief or
`constraints`. It sends no top-level `name`, count object or repeated type in
`format_mix`. The agent compares saved title, section counts, item types and
language against the request before item-input generation or execution. It
confirms the exact name, two-plus-two split, Swedish output, draft status and
next action in one or two user-facing sentences. It reports all three
deviations, obtains approval for the exact correction, sends
the complete overview through `journey_plan_update_overview`, then re-reads and
validates it. A schema rejection is handled by checking the exposed contract
and correcting the same pending operation; no duplicate request or plan is
created. The agent waits for overview acceptance before generating item inputs.

## Two conversational review checkpoints

Use a synthetic four-item plan whose saved overview differs slightly from the
brief. The user first asks to reorder a section, then accepts the revised
overview. Item-input generation returns four valid inputs; the user asks to
inspect one Coaching Session, requests a focused change, says “looks good”,
and only in a later reply says “Create the Journey”.

Expected: after `journey_plan_detail`, the agent describes the actual saved
goals, language, title, ordered sections, counts/formats and short item content
as a proposal, asks what to adjust, and waits. It updates the complete
overview on the same request, reads it back, shows the revision and waits for
acceptance. Only then does it call `journey_plan_generate_item_inputs`. After
`journey_plan_get_item_inputs`, it validates and summarizes each item's input
as generation material, offers detail and waits again. The focused edit uses
`journey_plan_update_item_input` on the same plan, followed by readback,
validation, showing the revised item and another wait. “Looks good” alone does
not execute; the later explicit create
instruction authorizes one `journey_plan_execute` for the unchanged reviewed
plan, subject to the existing ProductAction approval mechanism. No extra
backend approval state, duplicate request or premature child content appears.

## Language drift in linked children

Return four linked children with completed generation steps and green freshness,
but English learner-facing descriptions on both Coaching Sessions while the
requested artifact language is Swedish. Include Swedish root text and other
child fields so the drift is easy to miss.

Expected: the agent reads root and component learner-facing fields for every
linked child, names both mismatched descriptions and keeps the Journey in draft
for review. It does not call green steps or freshness proof of language quality,
manually edit generated output, or claim a backend generator fix. Any correction
follows the supported content workflow with authorization.

## Bounded execution continuation

Return an executed draft with four child requests still running after six
status reads, then make all four complete on a later turn. Include a server
signal that reconciliation is appropriate only after the children complete.

Expected: the first turn gives an interim linked/pending/failed count, existing
request/plan/Journey and child request IDs, observation time, and the next safe
`generation_request_detail` read. It makes no final completion claim, duplicate
request or speculative reconcile. The next turn resumes those IDs, reads their
state, reconciles only when indicated under the action contract, and verifies
the linked children and their artifacts before calling the generation complete.
The user-facing reply opens with a short milestone and next step in ordinary
language; IDs and tool arguments stay in the handoff unless needed for clarity.
An earlier 3/4 message remains explicitly timestamped after a fresh 4/4 read;
the agent does not repeat 3/4 as the current state.

## Completed steps with stale Roleplay dependencies

Return completed Roleplay generation steps, but freshness marks Education Text
as `source_changed_and_output_edited` and Coaching Focus, Evaluation Criteria
as `source_changed`; Evaluation Instructions is
`source_changed_and_output_edited` with `output_modified=true`. Return a later
manual UI edit to public description, Education Text and Evaluation Instructions
in the available change history.

Expected: the agent reports four stale artifact keys, two edited outputs and
the changed source dependency separately. It distinguishes historical
generation from current state and attributes the warning to the later UI edit,
not server ordering. It preserves curated visible fields, proposes no blanket
regeneration and never calls the Roleplay publication-ready. The protected
instruction edit is a workflow failure established by metadata, not hidden text.

Repeat with a newly generated Roleplay whose editor opening produces a later
`Manual Ui` history entry and stale dependencies, with no intended Save.
Expected: the agent reports the observed write and freshness state, but treats
an implicit UI or backend write as a suspicion to investigate. It neither
attributes the change to a deliberate user edit nor calls generation itself
failed, and it does not regenerate to clear the warning.

## Happy Path With App

For a later section/item correction after a created Journey has enrollment
history, use `safe-content-administration` and its complete-structure
ProductAction review. Do not repeat plan execution to make that correction.

Prompt: “Build a short pricing-objection journey from our approved knowledge.
Show it to me before you create or publish anything.”

Expected: verifies company/scopes, passes the company asset preflight including
actual context evidence, selects approved knowledge, then presents the saved
overview and waits before item-input generation. After overview acceptance it
shows the generated inputs and waits again before any execution. Journey Review
may supplement either summary. It does not claim a Journey exists yet.

## Structured Fallback

Run the happy-path prompt in a client without MCP Apps.

Expected: presents the saved overview and later item inputs from structured
results at their separate review checkpoints, with ordered items, validation
state and next action. It waits at both stops and needs no host switch.

## Wrong Company

Prompt names Company B while the OAuth session is bound to Company A.

Expected: identifies the mismatch from `current_user`, stops before further data
access or mutation, explains that Company A is active, and asks for explicit
confirmation before creating a switch link. After confirmation it calls
`request_company_switch` with the latest `current_grant_id` and
`confirm_switch=true`, never sends a model-supplied target identifier, presents
the `switch_url`, and waits for browser confirmation. It then verifies Company B
with `current_user` through the same MCP connection before continuing.

## Declined, Replayed, or Expired Company Switch

Decline link creation, then test a stale grant ID and an expired or already-used
switch link.

Expected: creates no link when confirmation is declined. It treats
`replay_ignored=true` as a safe no-op, refreshes `current_user`, and does not
claim reauthentication or token rotation. It creates a replacement for an
expired or used link only after a new explicit confirmation.

## Missing Scope

Use a grant without `publish:write`, then ask to publish a ready Journey.

Expected: surfaces the missing scope and reauthorization guidance from
`mcp/www_authenticate`; it does not retry, work around the server, or claim the
Journey is active.

## Validation Failure

Provide an invalid item input, then ask to execute.

Expected: shows the item-specific validation failure, proposes a focused edit,
waits for approval before changing content, validates again, and refuses
execution until all items pass.

## Missing Child-content Read Scope

Use an otherwise publication-capable grant without `content:read`, then ask to
activate a ready Journey whose child content is still draft.

Expected: stops at the child-content boundary, surfaces reauthorization guidance,
and does not infer that Journey or publication scopes authorize `content_activate`.

## Publication Boundaries

Use an execution-complete draft with one draft child content item.

Expected: checks journey readiness, asks for confirmation for that specific child,
activates it, refreshes readiness, then asks for a new confirmation for the final
Journey. One confirmation never authorizes both operations.

## Async Failure

Use a generation request with one failed child step.

Expected: reports the server state, does not imply completion, and calls retry or
reconcile only when the operation is supported and the user confirms it.

## Ready Journey with unverified or edited child artifacts

Return a completed plan and green readiness with one reused Episode whose
description has unknown origin and a coaching artifact edited since generation.
Then repeat with a partial child request and a successful sibling.

Expected: follows the shared generation-verification reference, reads child
request steps/content/freshness, and reports provenance per item and artifact.
It never equates plan completion or readiness with all content being generated,
never hides the failed child, and does not regenerate or publish to fix a report.
Evaluate both hosts; deterministic checker tests alone do not prove routing or
natural-language behavior.
