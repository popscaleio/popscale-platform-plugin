---
name: safe-interview-administration
description: Inspect authorized company-scoped Popscale interview Studies, saved-data datasets and private criteria versions, or administer Studies with the separate administration rights. Use for Studies analysis, precise question edits, respondent-intro localizations, invitations, run evidence, or aggregate analyses.
---

# Safe Interview Administration

Use `popscale-platform` for the direct Product MCP connection. When the user
selects a separately authorized own-grant Studies adapter, use that one actually
configured named server for all private contexts, datasets, criteria, actions and
file installation; never transfer handles between it and the direct connection.
Company, current rights, strict schemas, revisions and server approval remain
authoritative. Before mutations read the shared
[product action contract](../route-popscale-requests/references/product-actions.md).
Use app-visible names and the shared
[content naming rules](../route-popscale-requests/references/content-names.md).

## Choose the workflow

Call `current_user`, then `capabilities`; verify the intended company, active
membership, `interviews` feature and actual available operations. Never accept a
prompt company ID as authority. `available: false` is a boundary: report missing
`required_features` or `required_scopes` once, then stop that operation. Do not
search again, substitute generic REST or use a browser workaround.

For saved-data analysis or private criteria, use [compact-analysis.md](references/compact-analysis.md)
only with the explicit analysis profile and its current native rights. This
branch does not require Company Admin or authorize administration. Missing tools
mean unavailable, not an empty dataset. For explicitly available C3 classification,
follow [classification-analysis.md](references/classification-analysis.md).
Platform support needs a new accepted runtime/source/file proof, never old assistant12.

For broad administration below, require active `company_admin` and the specific
Interview scopes. Keep this branch separate from compact data/criteria.

## Administration workflow

1. Read `list_interview_studies` / `get_interview_study` before changing anything.
   Catalog `active` does not prove publication: check the published version and
   say “saved, not published” when absent. Explain badges only when relevant;
   never archive to reconcile labels or expose `current_published` routinely.
2. Create only a requested new Study; otherwise use
   `ensure_interview_study_draft`. Apply the narrowest metadata, topic or
   localization mutation to the current editable draft. Preserve unrelated
   fields; prefer append/remove/upsert over replacement. For new/substantial
   designs fetch `/studies/` from public Docs without company facts and read
   [study-design-quality.md](references/study-design-quality.md). A focused edit
   does not authorize redesign.
3. Use server enums: `interview_category` is `customer_research`,
   `employee_research` (staff), `win_loss`, `product_feedback`, `market_research`,
   `sales_discovery` or `other`; `default_respondent_type` is `customer`,
   `prospect`, `employee`, `partner` or `other`; `report_language` is `sv-SE`,
   `nb-NO`, `da-DK`, `fi-FI` or `en`. `target_insight_areas` uses
   `research_summary`, `sales_training`, `marketing_insights`,
   `product_feedback`, `customer_experience`, `operations`, `coaching`.
   On generic argument rejection inspect the schema; do not guess repeatedly.
   Study generation uses `must_include` (up to 30), not `questions`; read the
   normalized request back before starting because unknown generation fields
   are silently dropped. This behavior does not apply to strict compact inputs.
4. Pass exact latest `expected_updated_at`: a topic's own timestamp, not the
   draft's. After child edits refresh Study detail because its token advances.
   On `edit_conflict`, refresh using `current_updated_at`, preserve concurrent
   changes and review any materially changed effect before retrying.
5. Localizations affect only the current draft. Inspect asynchronous generation
   until persisted completion. Before publishing, read
   `get_interview_publish_readiness`, show target/changes/errors/warnings and
   obtain immediate confirmation for `publish_interview_study` with
   `confirm_publish=true`. Readiness does not establish conversation quality.
6. List invitation summaries first. Respondent links/distribution need
   `interview:distribute`. Before email/reminders obtain immediate confirmation
   and use `confirm_send=true`, at most 500 explicit IDs per separately reviewed
   batch. Do not expose contacts/links beyond the requested distribution task.
7. Existing run/aggregate analysis uses bounded legacy tools in
   [tool-workflow.md](references/tool-workflow.md). Preserve truncation,
   attribution and unavailable data; never reconstruct hidden identity or
   filters. Verify saved changes and asynchronous output before completion.

## Administration scopes and safety

`interview:read` covers bounded reads; `interview:write` adds authoring and
analysis mutations; `interview:distribute` adds respondent-link/invitation
operations. Publication additionally requires `publish:write`. Existing grants
are not silently widened: reauthorize needed scopes, never paste a bearer token.
These scopes do not alias the compact profile.

Never send Interview data, respondent links, transcripts or analyses to
`popscale-docs`. Keep company/source/owner boundaries; preserve masked data.
Do not combine create/send/publish/revoke/expire/delete/regenerate/retry behind
one confirmation. For company switch, privacy, conflicts and asynchronous
failures read [safety-and-fallbacks.md](references/safety-and-fallbacks.md).
Host evaluation scenarios live in the repository's `docs/evaluation/` directory;
package checks do not establish host or respondent-conversation behavior.
