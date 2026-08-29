# Privacy, Tenant, and Result Limits

## Company authority

The OAuth grant selects the company. Do not pass, trust, or derive a company ID
from the prompt. A superuser is not a cross-company analytics identity: they
must act through an explicitly selected company membership and receive the
effective company-admin catalog for that session. Cross-company department,
Journey, content, membership, or cursor identifiers must be rejected by the
server and must not be retried in another context.

If `current_user` reports a different company than the user intended, stop all
analytics reads. Explain the active company and ask for explicit confirmation
immediately before creating a switch link. Only after confirmation, call
`request_company_switch` with the latest `current_grant_id` and
`confirm_switch=true`; never send a target company or membership identifier.
Present the returned `switch_url`, wait for the user to select and confirm the
membership in Popscale's authenticated browser, then verify the company with
`current_user` through the same MCP connection. Treat `replay_ignored=true` as a
safe no-op and require a new confirmation before replacing an expired or used
link. Do not claim reauthorization or token rotation when
`reauthentication_required=false`.

## Suppression

Aggregate rows below `minimum_cohort_size` are suppressed. Preserve the flag and
threshold and describe the metric as unavailable. Never:

- reduce the threshold or split filters until a person can be inferred;
- subtract visible groups from a company total;
- combine overlapping date windows, roles, or departments;
- use member or attempt pages to calculate a suppressed aggregate;
- describe missing or suppressed values as zero.

If every relevant group is suppressed, answer that the requested comparison
cannot be made safely and offer a broader, genuinely useful cohort—not a series
of calls designed to reveal it.

## Personal data

Member drilldowns can return stable `membership_id`, display name, role,
department, progress, and safe attempt metrics. They deliberately omit email,
transcripts, reflections, evaluation feedback text, and raw result payloads.
Treat even the included identity and behavior as private company data:

- require an explicit user request for member- or attempt-level detail; an
  aggregate outlier or unexplained group is not consent to drill down;
- show only rows needed for the user's explicit question;
- do not enrich identifiers from public docs or outside sources;
- do not expose hidden fields, reconstruct omitted text, or produce a broad
  people export;
- do not retain or send the results to `popscale-docs`.

## Bounded and unavailable results

Preserve `has_more`, cursors, offsets, effective filters, and availability
notices. The member offset cap, per-page limits, 366-day date maximum, and
20,000-attempt aggregate guard are product boundaries. Narrow by a meaningful
department, role, status, or date range when needed. Do not claim company-wide
completeness from a page, treat a cap as zero remaining rows, or bypass a guard
by stitching detail pages into a private shadow aggregate.

Missing `usage:read` requires OAuth reauthorization. Missing tools or data must
not trigger a fallback to generic REST, UI scraping, a bearer token, the public
Docs MCP, or a different company.
