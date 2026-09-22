# Product action contract

Read the live `capabilities` and tool schemas before a mutation. Under
`popscale.product.actions.v1`, mutation tools require a stable UUID `command_id`
for one exact intent. Reuse it only for the identical payload after a transport
retry; a changed target, input or scope is a new intent. Never generate another
command merely because a previous submission has not returned its result.

An effect can return a `product_action` preview and `action_url` instead of the
native result. `product_action_prepare` can prepare a supported operation without
executing it. Explain the preview, including exact targets, scope, revision,
audience, expected credit charge and material effects. Let the human approve in
the authenticated review UI. A natural-language yes or a tool's legacy
confirmation boolean does not grant this approval. Never claim to approve as the
user, manufacture approval credentials or bypass the review with another tool.

Use `product_action_get` to read current action state. Only after the server says
the review action is approved may `product_action_execute` execute it. Bounded
actions which the server explicitly permits without review still require the
user's requested scope and the skill's confirmation rules. A prepared or
accepted action is not a completed effect: inspect the returned native result
and, for asynchronous work, the returned job/request until terminal status and
persisted output are verified. Do not blindly retry an uncertain submission.

Existing fields such as `confirm_publish`, `confirm_send`, `confirm_archive` and
`confirm_active_edit` still express operation-specific acknowledgements when the
live schema requires them; they do not replace server-side human approval.
Company and actor authority, current revisions, scopes and enabled capabilities
remain service-enforced. A tool's presence in a skill or bundle does not grant
permission to use it. The browser-confirmed `request_company_switch` workflow
retains its separate `current_grant_id` and `confirm_switch=true` contract.

Use server-returned quotes, prices and accepted order receipts for generation.
Do not assume images or other generated content are free, infer a price from a
public skill, or start extra generation to resolve a missing configuration.
Retries and included work must retain the server's existing operation owner;
never create another payable operation merely to repair a status display.
