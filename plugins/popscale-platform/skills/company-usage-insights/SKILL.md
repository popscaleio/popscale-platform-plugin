---
name: company-usage-insights
description: Analyze company-scoped Popscale Journey participation and learning-content outcomes with privacy-safe aggregates and bounded member or attempt drilldown. Use when a company admin asks about completion, mastery, usage, scores, outcomes, departments, roles, learners, or attempts; do not use it to edit content or create and publish a Journey.
---

# Company Usage Insights

Answer learning-usage questions through `popscale-platform`. Keep the
OAuth-selected company, live capability catalog, privacy metadata, metric
definitions, and server bounds authoritative.

## Required Workflow

1. Call `current_user`, then `capabilities`. Require an active effective
   `company_admin` in the intended OAuth-selected company and `usage:read`.
   A superuser acting for a company still needs that explicit company context;
   a company ID or name in the prompt is never authorization.
2. Resolve the Journey or content object from authenticated product state. Use
   a stable ID/link already returned in the current Product MCP context. For a
   title-only request, call `search_company_content` only when `content:read` is
   granted; otherwise ask the user for a server-returned ID/link or offer scoped
   reauthorization for name resolution. Never guess an ID or send the title,
   identifier, or result to `popscale-docs`.
3. Start with the smallest aggregate that answers the question:
   `get_journey_insights` for current Journey participation/completion/mastery,
   or `get_content_outcomes` for Roleplay, Coaching Session, Episode,
   Challenge, or Flashcard outcomes in a bounded date window.
4. Use `group_by=department` or `group_by=role` only when the comparison calls
   for it. Apply company-validated department and role filters before adding
   detail; do not infer an organization snapshot at the time of an attempt.
   Journey cohorts use active customer-human memberships, while historical
   content windows can retain attempts from removed or inactive customer-human
   memberships. Both exclude support and service identities.
5. Preserve every `suppressed`, `minimum_cohort_size`, count, metric-definition,
   timezone, notice, and availability field. Never reconstruct a suppressed
   value by changing filters, subtracting groups, combining calls, or using
   member-level results.
6. Drill down only when the user explicitly asks for member- or attempt-level
   detail. An aggregate result, outlier, or group that appears to need
   explanation is not consent to disclose people or attempts. Use
   `list_journey_members` before `get_member_journey`, and
   `list_content_attempts` behind a content aggregate. Names and stable
   membership IDs are private personal data even though email, transcripts,
   reflections, feedback text, and raw result payloads are omitted.
7. Respect offsets, attempt cursors, `has_more`, the 366-day maximum content
   window, and the 20,000-row aggregate guard. Narrow the question instead of
   claiming completeness beyond a server bound.
8. State whether the answer is current state or historical attempts. Surface
   `score_contract` and `historical_score_notice` next to affected historical
   Roleplay, Coaching, Flashcard, or legacy Episode results; never describe
   those values as immutable snapshots.
9. Report the filters, denominator, membership-lifecycle cohort, time
   window/timezone, suppression, and historical limitations needed to interpret
   the answer. Do not perform a mutation, request a write scope, or imply that
   analytics authorized one.

## Boundaries

- `usage:read` is a dedicated read-only scope. Existing grants are not silently
  widened; ask the user to reconnect or reauthorize when it is missing.
- The five analytics tools require only `usage:read`, but title-based catalog
  resolution uses `search_company_content` and therefore also requires
  `content:read`. Do not silently broaden the grant when an ID is already known.
- `get_content_usage` belongs to `safe-content-administration`: it reviews
  Journey/department dependencies before a content mutation. It is not the
  source for learner outcomes or attempt statistics.
- `safe-journey-creation` owns new Journey planning, execution, and publication.
  This skill reads Journey usage but never creates, edits, generates, or
  publishes anything.
- Do not export, enumerate, or expose member-level data beyond the user's
  requested, company-scoped drilldown. Do not turn safe identifiers into email
  addresses or join them with outside data.
- Treat missing, unavailable, omitted, or suppressed data as unknown—not zero.
- Never fall back to the public Docs MCP, generic HTTP, copied bearer tokens,
  admin UI scraping, or another company when a tool, scope, or result is
  unavailable.

Read [tool-workflow.md](references/tool-workflow.md) when choosing tools,
filters, or pagination. Read
[metric-semantics.md](references/metric-semantics.md) when interpreting Journey
or format-specific outcomes. Read
[privacy-and-limits.md](references/privacy-and-limits.md) for suppression, PII,
historical, and bounded-result decisions. Read
[evaluation-scenarios.md](references/evaluation-scenarios.md) when validating a
host or changing the Product MCP analytics catalog.
