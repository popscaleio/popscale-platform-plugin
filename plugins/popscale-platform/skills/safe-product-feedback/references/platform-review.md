# Authorized platform feedback review

Discover optional `feedback:review`; existing connections must explicitly
reauthorize to add it. Never request it for every user by default. Review requires
an eligible company admin who is an active superuser AND has explicitly assigned
`product_feedback.review_platform_feedback` permission, directly or by group.
Company-admin access or automatic superuser permission bypass is insufficient.
Do not impersonate, switch company or silently broaden scopes after denial.

Use `platform_feedback_list` with deliberate kind/status filters and bounded
pagination (`limit` up to 100, `offset` up to 10,000; `results`, `next_offset`).
Use `platform_feedback_get` with `feedback_id` for detail and `status_history`.
`platform_feedback_statistics` returns aggregate current saved ratings across
companies. These privileged tools differ from actor-private feedback reads.

Statuses are `received`, `in_review`, `in_development`, `responded`, `parked`,
`closed`. Interpret unhandled work deliberately across relevant statuses; closed
does not necessarily mean fixed. There is no unrestricted conversation search.

Context is a separate purposeful call to `platform_feedback_context` with
`feedback_id` and a nonempty `reason` of at most 500 characters. Every attempt is
audited. Respect absent consent, expired/deleted conversations and denied access;
never retrieve private sessions via another endpoint as a fallback.

First-party shared context contains at most six messages up to the anchor or
submission boundary, each truncated to 2,000 characters. No later turns,
attachments or private runtime instructions are available. External context is
only the stored agreed excerpt/reference with
`external_transcript_available:false`, not a full or independently verified
transcript.

For `update_feedback_status`, read the fresh status and prepare `feedback_id`,
`expected_status`, new `status`, optional `note` up to 1,000 characters and a
stable UUID `command_id`. Show the transition and note through the authenticated
ProductAction human approval flow before execution. Status history is immutable.
On conflict, reread and prepare a newly reviewed transition; never replay
automatically against a changed status. Setting responded sends no email,
notification or external message. Report only the confirmed persisted transition.
