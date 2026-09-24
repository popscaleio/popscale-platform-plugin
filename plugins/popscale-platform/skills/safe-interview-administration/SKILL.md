---
name: safe-interview-administration
description: Inspect and administer company-scoped Popscale interview Studies through the authenticated Product MCP, including precise question edits, respondent-intro localizations, invitations, run evidence, and aggregate analyses. Use when a company admin asks to view, create, edit, publish, distribute, or analyze Popscale interviews.
---

# Safe Interview Administration

Administer Interviews through `popscale-platform` while keeping the OAuth-bound
company, focused server tools, optimistic concurrency, privacy controls, and
human confirmation authoritative.

Read the shared [product action contract](../route-popscale-requests/references/product-actions.md) before any
mutation. Stable command identity and server-side human approval apply alongside
the workflow below; confirmation booleans alone do not approve effects.

Use current app-visible names for exercises, Journeys and Studies in user-facing
answers, lists and confirmations. Apply the shared [content naming rules](../route-popscale-requests/references/content-names.md)
for Journey context, duplicate names and internal identifiers.

## Required Workflow

1. Call `current_user`, then `capabilities`. Confirm the authenticated company is
   the intended company, the user is an active `company_admin`, the `interviews`
   feature is available, and the required Interview scopes are granted. Never
   accept a company name or ID from the prompt as authorization.
   `capabilities` lists every tool, including ones that cannot be called; the
   `available` flag decides. `available: false` with a missing
   `required_features` entry means Studies is not enabled for this company and
   Popscale enables it; a missing `required_scopes` entry means the grant needs
   widening. Say so once and stop; do not search for the tool again, use a
   generic tool instead, or drive a browser around it.
2. Read current state before changing it. Start with
   `list_interview_studies` or `get_interview_study`; use the returned current
   published snapshot, current editable draft, publish readiness, and edit token.
3. For authoring, create a Study or call `ensure_interview_study_draft`, then use
   the narrowest mutation. Update Study metadata separately from draft content.
   Use the topic tools for one question, probe, must-cover point, or keyed
   extraction-field change instead of replacing unrelated content.
   For new Studies or substantial redesigns, fetch `/studies/` from
   `popscale-docs` for what a good Study contains, read
   [study-design-quality.md](references/study-design-quality.md) and review
   conditional probes, completion criteria, respondent choice, and extraction
   needs before considering the design finished. Apply it only to the affected
   topic for a focused edit; do not expand the user's requested scope.
   The Study schema accepts free strings for four fields but the server owns
   the values: `interview_category` is one of `customer_research`,
   `employee_research` (use this for staff studies), `win_loss`,
   `product_feedback`, `market_research`, `sales_discovery`, `other`;
   `default_respondent_type` is `customer`, `prospect`, `employee`, `partner`
   or `other`; `report_language` is `sv-SE`, `nb-NO`, `da-DK`, `fi-FI` or `en`
   (never a bare `sv`); `target_insight_areas` are `research_summary`,
   `sales_training`, `marketing_insights`, `product_feedback`,
   `customer_experience`, `operations`, `coaching`. A wrong value returns a
   generic `Invalid tool arguments.`; do not guess a second time.
   When generating a Study through `generation_request_create` with
   `request_type: interview_study`, the question requirements go in
   `must_include` (at most 30 entries); the server silently drops unknown
   fields such as `questions`. Read the request back with
   `generation_request_detail` and show the normalized input before
   `generation_request_start`.
4. Pass the exact latest `updated_at` value as `expected_updated_at` whenever the
   tool requires it. For `update_interview_topic` that is the topic's own
   `updated_at`, not the draft's; an `edit_conflict` returns
   `current_updated_at`, which is the value to use next. After any topic or localization mutation, refresh Study
   detail before the next edit or publish attempt because child changes advance
   the draft edit token.
5. Use localization tools only on the current draft. Treat generated respondent
   intros as asynchronous work and inspect the returned generation request;
   never claim completion before the server does.
6. Call `get_interview_publish_readiness` before publication. Present the exact
   Study, draft, changed sections, errors, and warnings. Call
   `publish_interview_study` only after immediate explicit confirmation and with
   `confirm_publish=true`.
   Report publish readiness separately from design review and observed
   conversation quality; readiness does not prove interviewer behavior.
7. For invitations, list summaries before opening a specific invitation. Access
   respondent links or create, send, revoke, or expire invitations only when the
   `interview:distribute` capability is present. Ask for immediate confirmation
   before sending email or reminders and use `confirm_send=true`. Never expose a
   respondent link or masked contact value beyond the user's requested context.
8. For insights, use bounded run and analysis tools. Page transcript turns,
   preserve truncation indicators, distinguish stored evidence from inference,
   and never attempt to reconstruct hidden identity, metadata filters, or
   omitted provenance.
9. Report only what you verified. After every mutation, check that the result
   is not an error, read the object back, and confirm the change is present
   before saying it is done. Never report a batch as complete because the
   calls were sent, and never parse an unstructured error text as if it were
   a result. Then summarize Study names, outcomes, remaining warnings,
   truncation, and the next safe action. Do not invent URLs, completion, or
   publication state.

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
- If a tool is unavailable (`available: false`), report the missing feature or
  scope once. Do not search for it again, use a generic REST request, public
  documentation, a browser, or another tenant as a fallback.

Read [tool-workflow.md](references/tool-workflow.md) for exact tool order and
scope mapping. Read [safety-and-fallbacks.md](references/safety-and-fallbacks.md)
for conflicts, PII, asynchronous work, and bounded-result handling. Read
the host evaluation scenarios in the repository's `docs/evaluation/` directory when validating a
host, changing the Product MCP catalog, or evaluating Study design guidance.
