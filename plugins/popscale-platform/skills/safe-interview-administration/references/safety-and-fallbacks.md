# Interview Safety and Fallback Reference

## Authorization and company scope

The OAuth-selected company is authority, never a prompt company ID. On mismatch,
stop reads/writes. Follow the routing skill's company-switch boundary: explicit
confirmation, `request_company_switch(current_grant_id, confirm_switch=true)`,
then authenticated browser selection/confirmation and fresh `current_user` on
the same MCP connection. No target identifiers in tool inputs. Respect
`replay_ignored=true`; replacing expired/used links needs new confirmation.
Do not claim token rotation when `reauthentication_required=false`.

Unavailable tools or `_meta["mcp/www_authenticate"]` challenges require the
stated feature/right or reauthorization, never raw bearer material. Broad
administration requires Company Admin and its dedicated scopes; compact analysis
uses [compact-analysis.md](compact-analysis.md) and separate current rights.
One capability check suffices; generic tools/UI/public Docs are not bypasses.

## Administration conflicts and privacy

Only mutate the returned current editable draft. Pass current timestamps;
refresh after child edits. On `edit_conflict`, use `current_updated_at`, preserve
others' changes and ask again if the intended effect materially changes. Never
recover a missing old draft by guessing IDs.

Invitation summaries omit contacts and reusable links; detail/distribution need
their own rights. Preserve masking/anonymous identity boundaries and never infer
identity from adjacent evidence. Repeat links only for the requested task.
Transcripts/analyses are private; keep attribution and send nothing to public
Docs. Compact rich saved data has its own strict projection, not a new PII
content filter or a promise that every permitted value is anonymized.

## Bounded asynchronous work

Preserve legacy truncation/provenance markers; bounded pages are not exhaustive.
For localization/aggregate generation inspect durable jobs and persisted output.
Retry only a server-designated retryable failure after the user requests or
confirms it. Unknown Study-generation input fields can be dropped; read back
before start. Compact inputs reject extras and dataset retries keep identity.

Confirmation is action-specific: create/edit/generate/delete/revoke/expire/
retry/send/publish are separate. Immediately confirm exact email/reminder or
publication consequences. Server ProductAction approval remains authoritative.
A compact file descriptor or completed action does not prove file installation,
full-data computation or completed background work.
