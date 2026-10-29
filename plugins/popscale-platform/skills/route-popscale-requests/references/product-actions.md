# Product action contract

Read live `capabilities` and tool schemas. Under `popscale.product.actions.v1`,
mutations require a stable UUID `command_id` per exact intent. Reuse it and the
identical payload after transport uncertainty; never create duplicates while
waiting. `product_action_prepare` freezes a proposal without execution.

A mutation can return `product_action`, `review_url`, `next_step` and `action_url`
instead of its native result. Show exact targets, changes, revision, audience,
credit effects and expiry. Present the server-returned `review_url` unchanged:
**Review and approve in Popscale, then return to this conversation.** `action_url`
is a machine API address, never the human review link. If `review_url` is absent
or null, report the missing review route; never guess a URL or request tokens.
Adapt presentation to host support; a rendered chat card is optional.

Human approval must be registered in Popscale for this exact proposal. A chat
“yes”, host tool confirmation or legacy boolean does not approve it. Never
manufacture approval credentials or bypass review, including by demoting active
content to draft. Editing, generation and publication retain separate approvals.

On return, call `product_action_get` for the same action. Follow `next_step`:
`review_in_popscale` waits; `execute_action` permits `product_action_execute` only
with current approved state for review-required actions (or server-permitted
bounded work); `inspect_result` verifies persisted native output and asynchronous
jobs separately; `prepare_new_action` requires fresh review; `none` stops.
Prepared, approved and accepted do not mean completed. After uncertainty, inspect
existing action/result before retrying; preserve originating company, actor and
connection authority.

Check `expires_at` even if an older server still reports `awaiting_approval`.
Expired or superseded proposals cannot authorize execution. First inspect prior
outcome and current revision; retain the complete requested field set and text
when preparing a replacement with a new command and fresh human review. Never
substitute an earlier partial proposal. Payload retention is not approval validity.
Rejected/revoked proposals do not authorize automatic replacements.

`confirm_publish`, `confirm_send`, `confirm_archive` and `confirm_active_edit`
remain schema-specific acknowledgements, not server approval. Company-switch
confirmation remains separate; tool presence grants no authority. Use server
quotes/prices/receipts for generation, retaining the existing payable owner on
retries or included work; never assume free generation or add a debit to repair
status.
