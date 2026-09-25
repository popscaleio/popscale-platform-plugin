# Content Administration Safety and Fallbacks

## Company and role

The OAuth session selects the company. A prompt-supplied company name or ID is
context, not authority. Stop if `current_user` returns a different company or an
effective role other than active `company_admin`. This applies equally when a
Popscale superuser is acting for a customer company.

For a company mismatch, explain the active company and ask for explicit
confirmation immediately before creating a switch link. Only after confirmation,
call `request_company_switch` with the grant ID from the latest `current_user`
result as `current_grant_id` and `confirm_switch=true`. Never send a target
company or membership identifier. Present the returned `switch_url`; the user
signs in to the same Popscale account, selects the membership, and confirms in
the browser. Then verify the company with `current_user` through the same MCP
connection before resuming. Treat `replay_ignored=true` as a safe no-op, require
new confirmation before replacing an expired or used link, and do not claim
reauthorization or token rotation when `reauthentication_required=false`.

## Stale revisions

On an `expected_revision` conflict:

1. read root detail and the affected component again;
2. compare the refreshed value with the user's requested delta;
3. preserve unrelated concurrent changes;
4. ask again if the target or consequence changed materially; and
5. retry once with the new revision only after the intended delta remains clear.

Never convert a focused edit into a broad replacement to avoid a conflict.

## Active content and destructive boundaries

For an Episode identity/script correction, follow the shared
[speaker policy](episode-speakers.md). Never edit generated source or translated
scripts, even on drafts. Correct Script input (`model_steering`) and request
platform regeneration. Stop before active input edits if that correction cannot
be regenerated and published safely. Draft-only generation is not permission to
demote, clone or reassign an active Episode. Present the input delta and blocker.

Active edits can affect current learners. Show the exact active object and field
delta before requesting `confirm_active_edit`, and send that flag only when the
live tool schema exposes it. Delete, reorder, department replacement, archive,
regeneration, and publication remain separate approvals. Archive calls use
`confirm_archive` and, when the server reports learner impact,
`confirm_learner_impact`; they do not accept `confirm_active_edit`.

Active-edit approval never permits a manual write to a generation-only output.
If source changes require regenerating protected instructions but generation is
draft-only, use an authorized documented draft flow or report the blocker. Do
not use `confirm_generated_output_override`, demote the root, or manually repair
the instructions to work around the restriction. Report any source changes
already saved and that the generated output remains unsynchronized.

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
