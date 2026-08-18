# Safety and Fallback Reference

## Authorization

The OAuth session selects the company. A company name or ID in a prompt is
context, not authority. When `current_user` shows a different company than the
user intended, stop and reconnect rather than attempting cross-company lookup.

A tool result may include `_meta["mcp/www_authenticate"]`. Treat this as a host
reauthorization signal. Preserve the server's required scope list when explaining
what the user or Popscale admin must enable.

## Explicit Confirmation

Ask for confirmation at the final boundary, after presenting the exact target and
consequences. A confirmation for editing a draft does not also authorize publish,
activation, cancellation, regeneration, archive, or execution. If the target or
proposed change materially changes after confirmation, ask again.

## Validation

Show validation failures beside the affected journey item. Propose the smallest
correction, obtain approval for a content-changing edit, apply it with the focused
update tool, and validate again. Never mark an item valid in the conversation
without a successful server result.

## MCP App Capability

The Journey Review App is progressive enhancement. If `render_journey_review`
returns structured content but no view appears, summarize:

- request and plan status;
- overview;
- every item title/type/status;
- readiness and validation errors;
- the exact next safe actions.

Then continue with ordinary MCP tools. Do not ask the user to switch hosts merely
to complete the core flow.

## Async and Partial Failure

Queued or running work is not failure. Poll using the status tool. On a terminal
failure, report the server error without exposing tokens, hidden prompts, or
another tenant's data. Retry only a retryable operation and reconcile only when
the workflow is inconsistent or server guidance says it is needed.
