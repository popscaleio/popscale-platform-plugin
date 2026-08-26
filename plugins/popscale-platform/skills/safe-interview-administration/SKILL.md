---
name: safe-interview-administration
description: Inspect and administer company-scoped Popscale interview Studies through the authenticated Product MCP, including precise question edits, respondent-intro localizations, invitations, run evidence, and aggregate analyses. Use when a company admin asks to view, create, edit, publish, distribute, or analyze Popscale interviews.
---

# Safe Interview Administration

Administer Interviews through `popscale-platform` while keeping the OAuth-bound
company, focused server tools, optimistic concurrency, privacy controls, and
human confirmation authoritative.

## Required Workflow

1. Call `current_user`, then `capabilities`. Confirm the authenticated company is
   the intended company, the user is an active `company_admin`, the `interviews`
   feature is available, and the required Interview scopes are granted. Never
   accept a company name or ID from the prompt as authorization.
2. Read current state before changing it. Start with
   `list_interview_studies` or `get_interview_study`; use the returned current
   published snapshot, current editable draft, publish readiness, and edit token.
3. For authoring, create a Study or call `ensure_interview_study_draft`, then use
   the narrowest mutation. Update Study metadata separately from draft content.
   Use the topic tools for one question, probe, must-cover point, or keyed
   extraction-field change instead of replacing unrelated content.
4. Pass the exact latest `updated_at` value as `expected_updated_at` whenever the
   tool requires it. After any topic or localization mutation, refresh Study
   detail before the next edit or publish attempt because child changes advance
   the draft edit token.
5. Use localization tools only on the current draft. Treat generated respondent
   intros as asynchronous work and inspect the returned generation request;
   never claim completion before the server does.
6. Call `get_interview_publish_readiness` before publication. Present the exact
   Study, draft, changed sections, errors, and warnings. Call
   `publish_interview_study` only after immediate explicit confirmation and with
   `confirm_publish=true`.
7. For invitations, list summaries before opening a specific invitation. Access
   respondent links or create, send, revoke, or expire invitations only when the
   `interview:distribute` capability is present. Ask for immediate confirmation
   before sending email or reminders and use `confirm_send=true`. Never expose a
   respondent link or masked contact value beyond the user's requested context.
8. For insights, use bounded run and analysis tools. Page transcript turns,
   preserve truncation indicators, distinguish stored evidence from inference,
   and never attempt to reconstruct hidden identity, metadata filters, or
   omitted provenance.
9. Summarize server-returned IDs, outcomes, remaining warnings, truncation, and
   the next safe action. Do not invent URLs, completion, or publication state.

## Scope Boundaries

- `interview:read`: bounded Study, invite-summary, run, transcript, readiness,
  and analysis reads.
- `interview:write`: Study/draft/topic/localization mutations, localization and
  analysis generation/retry, and recommendation workflow status.
- `interview:distribute`: individual invite/respondent-link access, invitation
  creation, email/reminders, revoke, and expire.
- `publish:write`: additionally required for Interview Study publication.

Existing OAuth grants are not widened automatically. If a required scope is
missing, stop and ask the user to reconnect or reauthorize `popscale-platform`;
do not request or paste a bearer token.

## Safety Rules

- Treat every result as private to the company returned by `current_user`.
- Never send Interview data, respondent data, invitation links, transcripts, or
  analyses to `popscale-docs`.
- Never request, display unnecessarily, persist, or transform OAuth tokens or
  respondent bearer tokens.
- Do not mutate an older, published, discarded, archived, or otherwise
  non-current draft. Refresh current Study detail instead.
- Do not retry a stale edit blindly. Show the conflict, refresh, preserve the
  user's intended focused change, and ask again if the refreshed state changes
  the operation materially.
- Do not combine create, send, publish, revoke, expire, delete, regenerate, or
  retry actions behind one inferred confirmation.
- Respect server limits. Invitation email/reminder batches accept at most 500
  explicit invite IDs; split larger user-approved work into separately reviewed
  batches rather than bypassing validation.
- Treat masked or omitted respondent data as intentionally unavailable. Never
  infer it from labels, evidence, or adjacent results.
- If a tool is unavailable, report the missing capability or scope. Do not use a
  generic REST request, public documentation, or another tenant as a fallback.

Read [tool-workflow.md](references/tool-workflow.md) for exact tool order and
scope mapping. Read [safety-and-fallbacks.md](references/safety-and-fallbacks.md)
for conflicts, PII, asynchronous work, and bounded-result handling. Read
[evaluation-scenarios.md](references/evaluation-scenarios.md) when validating a
host or changing the Product MCP catalog.
