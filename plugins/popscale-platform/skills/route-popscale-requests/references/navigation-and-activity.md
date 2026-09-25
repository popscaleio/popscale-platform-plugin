# Navigation and activity

Discover `navigation_resolve`. Pass typed `target` and `intent`: `navigate` only when asked, else `offer`. Object routes require matching type/positive string ID; non-object routes reject objects. `journey.detail/settings` need `journey:read`; `studies.list`/`interview_study.detail` need `interview:read` and interviews enabled; `company.settings` needs `admin:read`; `ai_lab` needs `generation:read`. Never guess URLs or bypass denied/foreign targets.

Proposal does not open a page. External `execution:"host_link"` permits trusted host links; otherwise describe the target. First-party frontend checks session/run, company and unsaved changes. `replay_policy:"never_auto_execute"` forbids restored navigation. Proposal grants no edit/publish authority.

Discovery `_meta["popscale/activity"]` provides `presentation_key` and safe fallback `label` for actual operations; unknown keys use generic labels. First-party `activity.upserted` is a separate frontend contract. Never expose private reasoning/prompts/raw arguments. Submission completion does not finish background work; verify terminal status/output.
