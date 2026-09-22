---
name: safe-product-feedback
description: Submit Popscale bugs, ideas and improvements, inspect the caller's feedback and ratings, or perform explicitly authorized platform feedback review. Use for product feedback and its status; not for learner scores, interview analysis or general content editing.
---

# Safe Product Feedback

Use only authenticated `popscale-platform`. Never send feedback, identifiers or
conversation excerpts to public Docs. Discover current tools, `current_user` and
`capabilities`; verify the intended company before reading or submitting. Missing
tools or denied access mean unavailable capability, not an empty feedback queue.
Do not switch company or broaden access to work around a denial.

Read the shared [product action contract](../route-popscale-requests/references/product-actions.md)
before submission or status changes. Read [platform review](references/platform-review.md)
only for privileged review. Navigation and tool progress follow
[navigation and activity](../route-popscale-requests/references/navigation-and-activity.md).

## Submit a report

1. Classify as `general`, `bug`, `improvement` or `idea`. Collect a concise title
   (at most 200 characters) and text (at most 5,000). For a bug, include attempted
   action, expected and observed behavior when available. Ask one useful
   clarification if the report is otherwise meaningless; submit clear reports
   without an unnecessary questionnaire.
2. Use `submit_feedback` with `kind`, `title`, `text`, `share_context:false`
   unless sharing was explicitly requested, and a stable UUID `command_id`.
   This requires optional `admin:write`. Company, actor, source and initial status
   are server-derived; never supply them.
3. Keep the same command ID and exact arguments after a lost response. Resolve
   an existing action with `product_action_get`; do not create another report
   because the first result is uncertain. Changed arguments are a new intent.
4. If a review preview is returned, show its exact effect and authenticated
   approval link. Only execute through `product_action_execute` after the server
   reports approval. A verbal yes, role claim or `confirmed:true` is not an
   approval credential. Plain bounded feedback may complete without review.
5. Say submitted only after the action result contains `feedback` and `created`.
   Report its returned ID/status; `created:false` can mean the existing report
   was recovered. A preview, accepted request or tool-progress completion alone
   is not submission evidence.

## Share only agreed context

An external client can optionally send `external_excerpt` (at most 4,000
characters) and `client_reference` (at most 500). A nonempty excerpt requires
`share_context:true` and human approval of the preview. Show the actual bounded
excerpt/reference and sharing scope before approval. Remove unrelated customer
information and secrets. Never silently collect the entire host conversation.
If the user declines sharing, omit the excerpt and submit only the report with
`share_context:false`; do not manufacture an empty approval.

First-party session/message/run references come from trusted server context;
external tool arguments cannot select those IDs. Even a server-derived reference
does not imply consent to share. A client reference is an opaque pointer, not a
guaranteed URL or permission to open it. Backend cannot fetch external chat
history later; never promise support access to the full conversation.

## Read the caller's feedback

Optional `admin:read` allows `list_feedback`, `get_feedback` and
`feedback_statistics`. Lists accept `kind`, `status`, `limit` up to 100 and
`offset` up to 10,000; follow `results` and `next_offset`. Detail takes
`feedback_id`. These reads are private to the current human in the selected
company, not company-wide support searches; detail excludes conversation text
and reviewer notes.

Statistics count this caller's current saved up/down ratings, not all users'
satisfaction or inferred message ratings. Frontend owns thumbs, rating changes
and follow-up questions. No tool in this workflow rates arbitrary external-host
assistant messages.

Use [evaluation scenarios](references/evaluation-scenarios.md) for host validation.
