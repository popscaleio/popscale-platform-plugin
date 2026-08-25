# Interview Safety and Fallback Reference

## Authorization and company scope

The OAuth session selects the company. A prompt-supplied company name or ID is
context, not authority. If `current_user` returns another company, stop before
further reads or writes and ask the user to reconnect to the intended company.

If a capability is unavailable or a result supplies an
`_meta["mcp/www_authenticate"]` challenge, preserve the required scopes in the
explanation and ask the user to reconnect or reauthorize. Never ask for a raw
access token or respondent link token.

## Optimistic concurrency

Study, draft, and topic edits use server-returned timestamps as edit tokens. On
an `edit_conflict`, refresh Study detail and compare the current focused field
with the user's requested change. Do not replay an old full object or overwrite
unrelated concurrent edits. Ask for renewed confirmation if the refreshed state
changes the consequence of the operation.

Only the current editable draft returned by Study detail may be mutated. Treat a
not-found response for an older draft as a safety boundary, not a reason to
guess another version ID.

## Respondent privacy

List results intentionally omit contact PII and reusable links. Detail and
delivery results may contain only masked values, while anonymous respondents
return no identity or segmentation fragments. Preserve masking, do not combine
adjacent evidence to identify a respondent, and do not repeat a respondent link
unless the user explicitly needs it for the current distribution task.

Transcripts and analyses are sensitive company data. Summarize only the portion
needed for the user's request, retain evidence attribution, and never send this
content to the public Docs MCP.

## Bounded and asynchronous results

Study history, runs, transcript turns, findings, evidence, recommendations, and
provenance are bounded. Report truncation and page intentionally when more data
is needed; never claim a bounded response is exhaustive.

Localization and analysis generation may return durable asynchronous work.
Report queued/running states accurately and use supported status reads. Retry
only a server-designated retryable failure and only after the user requests or
confirms that separate action.

## Confirmation boundaries

Ask for confirmation immediately before sending email/reminders or publishing a
Study, after presenting the exact target and consequences. Creation, editing,
generation, deletion, revoke, expire, retry, send, and publish are separate
actions. Approval for one does not authorize another.
