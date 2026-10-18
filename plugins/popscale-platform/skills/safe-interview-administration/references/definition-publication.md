# Conditional C4 Definition Publication

Require actual C4 discovery, company/read rights and exact version.
Keep original-grant handles; C1/C2/C3 never expand.

`submit_interview_classification_definition`: bounded R+W shares safe criteria
only, never private evidence/drafts/counts. Submission is not publication.

With R+`interview:definitions:publish` and current native publish permission,
`publish_interview_classification_definition`, `recommend_interview_classification_definition`,
`archive_interview_classification_definition`, `restore_interview_classification_definition`
require REVIEW_REQUIRED initiating-human approval of the exact server preview.
Classify grants no publish authority.

Valid `awaiting_approval` envelopes (compatibility HTTP409; named MCP
`isError=false`) retain action_id/command_id/idempotency_key/body/grant.
After human approval, repeat the same named request. Generic execute reports
`approval_required` before approval. Recover with `product_action_get` before
uncertain retries; fresh preview/approval is for actual stale/conflicting intent.
Never self-approve or replace a pending action.

One recommendation per family; older published versions remain selectable.
Archive blocks new acceptance, preserves accepted work/prices/deadlines.
Restore revives no approvals/recommendations. Safe cards grant no private-source
access; no AI/debit, external output restore or organization MCP.
