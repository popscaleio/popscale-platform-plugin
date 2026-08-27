# Content Administration Safety and Fallbacks

## Company and role

The OAuth session selects the company. A prompt-supplied company name or ID is
context, not authority. Stop if `current_user` returns a different company or an
effective role other than active `company_admin`. This applies equally when a
Popscale superuser is acting for a customer company.

## Stale revisions

On an `expected_revision` conflict:

1. read root detail and the affected component again;
2. compare the refreshed value with the user's requested delta;
3. preserve unrelated concurrent changes;
4. ask again if the target or consequence changed materially; and
5. retry once with the new revision only after the intended delta remains clear.

Never convert a focused edit into a broad replacement to avoid a conflict.

## Active content and destructive boundaries

Active edits can affect current learners. Show the exact active object and field
delta before requesting `confirm_active_edit`, and send that flag only when the
live tool schema exposes it. Delete, reorder, department replacement, archive,
regeneration, and publication remain separate approvals. Archive calls use
`confirm_archive` and, when the server reports learner impact,
`confirm_learner_impact`; they do not accept `confirm_active_edit`.

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
another company's data. Retry only a retryable failed step with a separate user
approval; do not generate a second request merely because the first is slow.

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
