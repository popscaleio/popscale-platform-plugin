# Safety and Fallback Reference

## Authorization

Apply [channel policy](../../route-popscale-requests/references/channel-permissions.md) to company switching.

Journey authoring still requires CompanyAdmin. Structured App output can replace
an unavailable view only when the underlying operation remains authorized.

## Explicit Confirmation

Ask for confirmation at the final boundary, after presenting the exact target and
consequences. A confirmation for editing a draft does not also authorize publish,
activation, cancellation, regeneration, archive, or execution. If the target or
proposed change materially changes after confirmation, ask again.

## Validation

Show saved validation failures beside the affected item. Validate generated
payloads with the item-input tool; use saved selector status and summary for
linked or reused items. A tool invocation error proves neither validity nor
invalidity. Obtain approval for a focused edit, then re-read and revalidate.

## MCP App Capability

The Journey Review App is progressive enhancement. If `render_journey_review`
returns structured content but no view appears, summarize:

- request and plan status;
- overview;
- item title/purpose/status and Roleplay scenario → item → selected customer;
- readiness and validation errors;
- the exact next safe actions.

Label this a plan until execution creates a draft Journey. Lead with names and
short content, not raw type codes or IDs. Continue with ordinary MCP tools; do
not ask the user to switch hosts.

## Invalid Scenario or Customer Selection

A `reuse_from_client_id` that points forward, at itself, or at a non-Roleplay
item, a `customer_id` from another scenario or company, or a new customer
against an already active scenario is rejected by the server. Show the error
and fix the selector in the overview; do not create a new plan.
If two items reuse one scenario but select the same customer, show the mismatch
and stop before claiming that two distinct encounters were created.

## Waiting Dependencies and Failed Sources

`waiting_for_scenario` means the source item has not reached `linked`. If the
source fails, dependent items become `dependency_failed`. Reconcile and retry
the existing step; a second plan produces duplicates.

## Async and Partial Failure

Queued or running work is not failure. Poll using the status tool. On a terminal
failure, report the server error without exposing tokens, hidden prompts, or
another tenant's data. Retry only a retryable operation and reconcile only when
the workflow is inconsistent or server guidance says it is needed.
