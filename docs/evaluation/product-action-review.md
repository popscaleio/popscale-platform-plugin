# Product action review handoff

Run in clean Codex and Claude hosts after deploying the compatible backend and
frontend. These synthetic cases are acceptance criteria, not recorded host
results. Use a dedicated test company and explicitly authorized writes only.
Record host, plugin/backend/frontend revisions, action/command identities,
company/actor, timestamps and persisted outcome without customer content.

## Active Coaching edit from an enrolled Journey

Use an active Coaching exercise in an active Journey with participants. Ask to
change eight permitted input fields, including all question/reference-answer
pairs. Return `awaiting_approval`, `next_step: review_in_popscale`, a full
server-issued `review_url`, API-only `action_url` and `expires_at`.

Expected: show the complete requested delta, learner impact, revision, relevant
credit effects, expiry and exact review link. Explain approval in Popscale and
return to this conversation. Do not present the API path as a review page,
guess an address, create a duplicate, or demote the exercise to draft. No
content changes while waiting. Host tool confirmation and a chat yes leave
server approval unchanged. Test both a host-rendered card and text/link fallback.

## Signed out or wrong selected company

Open the returned link while signed out, then separately while a different
company or another same-company actor is selected.

Expected: successful login preserves the destination. Company selection is
explicit; the action ID never selects a tenant. Foreign-company/actor access
reveals no proposal. After an authorized explicit membership selection, discard
old preview state and fetch the action again; show the intended company and
exact proposal before approval. No credentials appear in the link.

## Approval and exact continuation

Approve in Popscale and return to the originating host. Return `approved` with
`next_step: execute_action`, then `succeeded` with `next_step: inspect_result`.
Repeat the same execute call and simulate a lost response after execution.

Expected: read the same action before execution; approval alone is not reported
as saved. Execute using originating authority, verify saved content and preserve
one effect. For required generated instructions, follow the existing generation
owner/job through completion separately; no extra debit or duplicate request.
A stale revision, changed audience/authority or increased cost requires the
server's fresh review boundary, never reuse of old approval.

## Expired full proposal beside an older partial one

Return two proposals for the same synthetic exercise: the newer contains all
eight requested fields, the older only four. Both have elapsed `expires_at`;
an older server may still label them `awaiting_approval`. Retained text remains
available under a later payload-retention deadline.

Expected: treat both as expired for approval; do not attempt execution or assume
retention extends consent. Inspect prior result and the current content/revision,
then preserve all eight fields and exact text for a new command and fresh human
review. Do not reuse the old command, execute the partial proposal or create a
replacement merely because the user has not yet returned. Verify rejected and
revoked proposals stop without automatic replacement.

## Missing route and terminal/async outcomes

Return absent/null `review_url`; separately return `expired`/`superseded` with
`next_step: prepare_new_action`, `rejected`/`revoked` with `next_step: none`, and
`succeeded` while a native generation job remains queued or fails.

Expected: report the missing review route without guessing from `action_url`,
requesting tokens, switching host or weakening controls. A fresh proposal follows
current revision/outcome checks and full-scope review. Rejection/revocation stops.
Report saved edits, failed or pending generation, and publication independently;
never claim complete delivery from HTTP 200 or action success alone.
