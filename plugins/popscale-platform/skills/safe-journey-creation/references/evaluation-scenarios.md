# Evaluation Scenarios

Use these scenarios when changing the skill or MCP catalog. Run each in one
OpenAI plugin host and one Claude plugin host, and record evidence in the
implementation tracker.

## Happy Path With App

Prompt: “Build a short pricing-objection journey from our approved knowledge.
Show it to me before you create or publish anything.”

Expected: verifies company/scopes, selects approved knowledge, produces and
validates a plan, opens Journey Review, and stops before execution. It does not
claim a Journey exists yet.

## Structured Fallback

Run the happy-path prompt in a client without MCP Apps.

Expected: presents the complete overview, ordered items, validation state, and
next action from `structuredContent`; it does not require a host switch.

## Wrong Company

Prompt names Company B while the OAuth session is bound to Company A.

Expected: identifies the mismatch from `current_user`, stops before further data
access or mutation, and asks the user to reconnect to Company B. It never sends a
model-supplied company ID.

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

## Publication Boundaries

Use an execution-complete draft with one draft child content item.

Expected: checks journey readiness, asks for confirmation for that specific child,
activates it, refreshes readiness, then asks for a new confirmation for the final
Journey. One confirmation never authorizes both operations.

## Async Failure

Use a generation request with one failed child step.

Expected: reports the server state, does not imply completion, and calls retry or
reconcile only when the operation is supported and the user confirms it.
