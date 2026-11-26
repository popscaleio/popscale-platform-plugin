# Journey publication

Use `journey_publish_bundle` for a whole draft Journey only when live capabilities
permit it and its schema matches. V1 supports at most 20 current Journey items,
including duplicates, with ready Coaching/Roleplay roots. Unsupported types block.

Send `journey_id`, stable `command_id` and `include_new_assignments` (default
false). Never supply company scope. AUTO requires explicit assignment inclusion
even with zero candidates or paused rules. Obtain missing intent; never change
saved enrollment/rules or set inclusion merely to pass validation. Paused
allocation still blocks; the bundle never unpauses it. If legacy settings would
reassign removed/excluded participants outside the reviewed audience, stop for
separate explicit allocation review.

Review company, Journey, deduplicated roots, versions, audience, readiness and
cost effects in `journey_publication_review` v1. Empty selectors do not imply
global learner access. Publication includes no generation/debit. Check every
root's current detail/freshness, including active ones: `legacy_unknown`,
`output_edited`, `stale`, `generating` or unavailable proof blocks. Pending
customer generation/linking must finish first.

Only authenticated Popscale approves/applies; MCP cannot approve. Draft
activations, Journey activation last and the receipt commit together. Active
roots are retained. Outside changes require fresh review; this command's expected
status transitions do not.

After uncertainty inspect the same action or retry its identical command.
Rollback preserves original statuses; no new allocation intent. Never duplicate
objects/jobs. Require `journey_publication_verification` v1 bound to the exact
`preview_hash`, reviewed identities/revisions and active final statuses.
Missing/mismatched proof is unverified. Report assignments separately:
`not_requested`, `queued` or `applied`; queued is not delivered.

Standalone publication/verified older deployments retain `content_activate`,
`journey_activate` and their own approvals/`confirm_publish=true`. Activate ready
children, then check `journey_activation_readiness` before the Journey. Never
fall back after bundle permission, readiness, freshness or unsupported-type
rejection.
