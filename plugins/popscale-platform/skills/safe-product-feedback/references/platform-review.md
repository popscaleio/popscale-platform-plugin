# Platform review

Optional `feedback:review` requires reauthorization, eligible company-admin status, active superuser account and explicitly assigned `product_feedback.review_platform_feedback` permission. Never infer or default authority.

`platform_feedback_list` filters bounded kind/status pages; `platform_feedback_get` returns detail/immutable `status_history`; `platform_feedback_statistics` aggregates current ratings across companies. Statuses: `received`, `in_review`, `in_development`, `responded`, `parked`, `closed`. Closed need not mean fixed; responded sends nothing.

`platform_feedback_context` needs `feedback_id` and specific `reason` (≤500 characters); every attempt is audited. No consent or expired/deleted session means no context or fallback. First-party: ≤6 messages before anchor/submission, each ≤2,000 characters; no later turns, attachments or private instructions. External: agreed excerpt/reference only, `external_transcript_available:false`.

`update_feedback_status` needs `feedback_id`, fresh `expected_status`, new `status`, optional `note` (≤1,000), stable UUID `command_id`. Show ProductAction preview; await authenticated human approval. On conflict reread and prepare newly reviewed transition. Report only persisted change.
