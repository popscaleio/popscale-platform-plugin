# Interview Safety and Fallback Reference

## Authorization and company scope

Apply [channel policy](../../route-popscale-requests/references/channel-permissions.md) to company switching.

The company needs `interviews` enabled. Study delegation follows live operation
availability; an unavailable capability alone does not imply missing consent.
Never ask for raw access or respondent tokens.

## Silently dropped generation fields

The Study generation input drops unknown fields without error. A request
created with `questions` instead of `must_include` succeeds with an empty
requirement list. Read the request back and show the normalized input before
starting; cancel and recreate if a requirement is missing.

## Optimistic concurrency

Study, draft, and topic edits use server-returned timestamps as edit tokens; a
topic's token is its own `updated_at`, not the draft's. On an `edit_conflict`,
use the returned `current_updated_at`, refresh Study detail and compare the
current focused field with the user's requested change. Do not replay an old full object or overwrite
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
