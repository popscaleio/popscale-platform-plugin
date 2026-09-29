# Safety and Fallback Reference

## Authorization

The OAuth session selects the company. A company name or ID in a prompt is
context, not authority. When `current_user` shows a different company than the
user intended, stop before any further product read or write. Explain the
current company and ask for explicit confirmation immediately before creating a
switch link. Only after confirmation, call `request_company_switch` with the
grant ID from the latest `current_user` result as `current_grant_id` and
`confirm_switch=true`. Never pass a target company name, company ID, or
membership ID to the tool.

Present the returned `switch_url`. The user must sign in to the same Popscale
account, select the intended membership, and confirm in the authenticated
browser. Link creation is not proof of a completed switch. Afterwards, retry
`current_user` through the same MCP connection and verify the returned company
before resuming the Journey workflow. If `replay_ignored=true`, refresh
`current_user` and leave the active connection unchanged. If a switch link is
expired or already used, ask again before creating a new one. Do not claim
reauthorization, token rotation, or grant revocation when
`reauthentication_required=false`.

A tool result may include `_meta["mcp/www_authenticate"]`. Treat this as a host
reauthorization signal. Preserve the server's required scope list when explaining
what the user or Popscale admin must enable.

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
