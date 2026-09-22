# Navigation and actual tool activity

Discover `navigation_resolve` and supported targets through Product MCP. It takes
only `target` and `intent`; company comes from authentication. Use `navigate`
when the user asks to go there, otherwise `offer`. For example:

```json
{"target":{"route_id":"journey.settings","object_type":"journey","object_id":"42"},"intent":"offer"}
```

Route IDs include `journey.detail`, `journey.settings`, `company.settings`,
`studies.list`, `interview_study.detail` and `ai_lab`. Discover other supported
targets rather than guessing paths. Object targets need the matching type and a
positive ID as a string; non-object targets reject object fields. Journey routes
need `journey:read`; Study routes need `interview:read` and the interviews feature;
Company Settings needs `admin:read`; AI Lab needs `generation:read`. Other targets
have their own content, knowledge or credits scopes and features. Handle foreign
objects, missing scope and disabled features as unavailable, never as grounds to
invent a URL or bypass access controls.

A result is a verified proposal, not evidence that a page opened. External MCP
returns `execution:"host_link"`, typed `target`, selected `company_id`, stable
`proposal_id`, null session/run and `replay_policy:"never_auto_execute"`. A
capable host may resolve that target to a trusted product link. Without this
capability, describe the page honestly; do not invent frontend URLs or promise
control of an open Popscale tab. Customer-content links are not navigation tools.

First-party proposals bind to session/run and frozen `source_page_context`.
Frontend maps known routes and verifies current company/session plus its normal
unsaved-change confirmation before leaving. Never execute restored history or
old proposals automatically. Navigation grants no authority to edit, publish or
charge credits at the destination.

Discovery can expose `_meta["popscale/activity"]` with `presentation_key` and
safe fallback `label`. Use these for actual operations if supported by the host;
unknown keys retain a generic safe fallback. Tool descriptions and this metadata
are server-owned; the plugin does not install a second tool catalogue. External
clients control their own progress UI. First-party durable `activity.upserted`
events (running/completed/failed/interrupted) are a separate authenticated
frontend contract, not a public MCP subscription.

Do not expose hidden reasoning, private prompts or raw arguments as progress.
Completion of a job-submission call means the job was ordered; verify its job
status and persisted result before saying generation finished. A failed or
interrupted operation must not be presented as successful.
