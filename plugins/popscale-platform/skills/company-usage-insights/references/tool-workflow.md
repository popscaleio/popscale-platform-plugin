# Company Usage Insights Tool Workflow

Discover the live catalog with `capabilities`. Returned schemas, authorization,
privacy metadata, and server validation remain authoritative over this guide.

## Identity and aggregate selection

| Tool | Use | Important inputs |
| --- | --- | --- |
| `current_user` | Verify the effective role and OAuth-selected company | Authenticated session |
| `capabilities` | Verify tool availability and `usage:read` | Authenticated session |
| `search_company_content` | Resolve a title to a company-scoped stable ID when needed | Optional `content:read`; offer scoped reauthorization if absent |
| `get_journey_insights` | Compare current Journey participation, completion, and mastery | `journey_id`; `group_by`; optional `department_ids`, `roles`, `minimum_cohort_size` |
| `get_content_outcomes` | Compare attempt outcomes for one content root | `content_type`, `object_id`; optional group/filter/date/cohort inputs |

Use `group_by=company` for an overall answer, `department` for department
comparisons, and `role` for `company_admin`, `department_admin`, or `employee`
comparisons. Department IDs must come from the authenticated company. The
minimum cohort defaults to 3 and can be 2 through 20; never lower or reshape it
to reveal a suppressed result.

Resolve IDs as described in the skill entrypoint; `usage:read` alone cannot
search the catalog. Reuse resolved names without extra presentation permissions.

Supported content outcome types are `roleplay`, `coaching_session`, `episode`,
`challenge`, and `flashcard_deck`. The default date window is the last 90
company-local calendar days and the maximum is 366 days. Always report the
server-returned effective window and timezone.

## Bounded drilldown

| Tool | Use | Bound |
| --- | --- | --- |
| `list_journey_members` | Page current enrolled-member progress after an explicit drilldown request | `limit` at most 100; `offset` at most 1000 |
| `get_member_journey` | Read one returned membership's sections, next action, and attempt timeline | `attempt_limit` at most 50; page with `before_attempt_id` |
| `list_content_attempts` | Page attempts behind one content aggregate | `limit` at most 100; page with `before_attempt_id` |

`list_journey_members` can filter by department, role, or Journey status and can
order by name, department, status, completion, mastery, or last activity. Use
only the ordering needed for the question. Do not page through an entire company
when a group aggregate answers it.

`list_content_attempts` can use the same department, role, and date filters as
the aggregate and may request `evaluated_only=true`. Keep the filters aligned
when explaining which attempts support an aggregate. A 20,000-row aggregate
guard is a request to narrow filters or dates, not permission to reconstruct the
same aggregate from every detail page.

All tools are read-only. No confirmation flag or write scope belongs in this
workflow. UI activity/loading rows do not measure provider tool-call counts;
do not infer backend latency or call volume from them.
