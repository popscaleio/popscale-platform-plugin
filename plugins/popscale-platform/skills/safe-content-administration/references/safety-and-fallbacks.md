# Content Administration Safety and Fallbacks

## Company and role

The OAuth session selects the company. A prompt-supplied company name or ID is
context, not authority. Stop if `current_user` returns a different company or an
effective role other than active `company_admin`. This applies equally when a
Popscale superuser is acting for a customer company.

For a company mismatch, follow the
[company-switch workflow](../../route-popscale-requests/SKILL.md#company-switch-boundary).

## Stale revisions

On an `expected_revision` conflict:

1. read root detail and the affected component again;
2. compare the refreshed value with the user's requested delta;
3. preserve unrelated concurrent changes;
4. ask again if the target or consequence changed materially; and
5. retry once with the new revision only after the intended delta remains clear.

Never convert a focused edit into a broad replacement to avoid a conflict.

## Active content and destructive boundaries

For Episode corrections, follow [speaker policy](episode-speakers.md): edit
Script input, never generated scripts. Establish safe regeneration before active
input edits; no demotion, cloning or reassignment workaround. Show blockers.

Disclose active learner impact; use `confirm_active_edit` only where exposed.
Delete, reorder, reassignment, archive, generation and publication need covering
intent and platform approvals, not repeated chat questions. Archive uses
`confirm_archive` and server-required `confirm_learner_impact`, never
`confirm_active_edit`.

For affected protected outputs, check capabilities/freshness and regenerate through
the platform. No `confirm_generated_output_override` or manual repair. Report
saved inputs separately from pending regeneration.

For Coaching input changes, both `agent_prompt` and `evaluation_instructions`
must be regenerated through the platform. Include this required pair in the
operation up front. If a known status/scope/tool restriction prevents it, stop
before new input edits; if discovered after saving inputs, report the update as
incomplete. Never skip one output because freshness appears current, or manually
patch either output after a partial or failed generation.

Before delete, reorder, reassignment, or archive, inspect bounded usage. If
usage is truncated, do not infer that unseen dependencies are absent. Retry
once with `limit` equal to the larger returned Journey/department count, capped
at the server maximum of 100. If the retry remains truncated, report the totals
and truncation flags and stop when the decision requires exact dependency
details. `get_content_usage` has no filters, offset, or cursor; do not invent
unsupported narrowing or pagination arguments.

## Async generation and partial failure

Queued or running is not complete. Poll the returned generation request at a
reasonable cadence. On terminal failure, report the failed step and safe server
error without exposing hidden prompts, knowledge snapshots, credentials, or
another company's data. Retry only supported failed steps within authorized
scope/cost and platform approval; ask about new costs or missing retry intent.
Do not generate a second request merely because the first is slow.

Refresh content and freshness after success. A successful request can still
leave warnings, stale translations, or unpublished draft content.

## Bounded and unavailable data

Preserve `has_more`, `next_before_id`, offsets, truncation, and `available=false`.
Do not concatenate beyond server bounds, reconstruct omitted history, or treat
an unavailable history/freshness surface as empty proof.

## Missing tool or scope

Respect `_meta["mcp/www_authenticate"]` and the server's missing scope list.
Ask the user to reconnect or reauthorize `popscale-platform`. Do not use the
public Docs MCP, generic HTTP, copied tokens, admin UI scraping, or a different
tenant as a fallback.
