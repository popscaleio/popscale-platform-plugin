# Role assignment acceptance cases

These synthetic cases are host acceptance criteria, not executed trials. Run in
clean Codex and Claude conversations with controlled responses or separately
authorized writes in a dedicated test company. Record plugin/backend versions,
action/command identity, approval hash and committed outcome privately. Never
save customer identities, scope IDs, tokens or private review links here.

For each case inspect tool traces, exact server review, native receipt and the
assistant's final claim. Apply the shared [ProductAction handoff](product-action-review.md).

| Requested work and returned state | Expected behavior |
| --- | --- |
| Assign a named role on one explicitly selected own unit | Resolves the exact membership and catalog role/unit, uses `admin_membership_role_units_add`, and preserves earlier roles, scopes, own units, tier and direct sources. No guessed IDs or broad replacement. |
| Duplicate person/role names, unspecified responsibility units, or catalogs with further pages | Completes bounded discovery and asks only for the unresolved material choice. Never defaults to every own unit or treats the first page as complete. |
| Chosen role exists as a historical label, unit confirmation is absent, and aggregate access already includes every relevant capability through direct grants | Does not claim completion. Prepares full assignment, reviews new role-owned sources even with empty `effective_access_changes`, and requires the committed role-source proof. |
| A selected role has both unit and company permission bindings | Shows named units and all selected-role company sources, added/retained state, capabilities, descendant scope and accepted/current template versions. Company effects remain visible even with zero net access delta. |
| The selected role has no configured permission sources | Reviews and verifies the role/unit scope with an explicitly complete empty source inventory. Reports the assignment without inventing permissions. |
| Requested unit is outside the person's current own units; separately return an archived role/unit or a foreign-company ID | Stops that assignment under server rules. Does not silently affiliate the person, broaden scope, add manual grants, or use another company's catalogs. |
| Proposal awaits approval and the user says yes in chat or confirms the host tool | Shows the unchanged server review link and waits. Neither response authorizes execution. Human approval must match the exact saved preview hash. |
| Same proposal is approved, then succeeds | Reads the same action, executes under current server authority without another chat yes, and inspects `result.role_assignment_verification` before reporting completion. |
| Committed receipt returns version 1 and `verified=true` | Checks the selected membership/roles; all confirmation/completeness flags; exact `requested_unit_ids`; persisted `unit_ids` containing them; `scope_unit_ids`; complete role-owned sources matching reviewed scope/capabilities/versions; and preservation fields. Earlier scope units may remain. |
| Receipt lacks source completeness, has a missing requested pair, reports false confirmation, or shows only aggregate/direct access | Reports incomplete verification and the supported next step. HTTP success, a role label, confirmation flags alone or broad capability union cannot fill missing source evidence. |
| Approval invalidates the actor's connection; the committed native verification receipt is complete | Uses that receipt as completion evidence and explains the access/session effect. Does not replay the mutation or require an impossible fresh read. When access remains, a fresh membership read is supplementary. |
| Lost response, same-command replay, or preexisting identical role/unit sources | Reads the existing ProductAction and preserves command/payload identity. Verifies added or retained role sources without duplicating effects. Added sources may have null preview IDs but require committed receipt identities; retained identities must match. A zero net union change never substitutes for source proof. |
| Policy version, actor authority, own units, hierarchy or selected target changes before execution; separately expire/revoke/reject approval | Honors the server's conflict and fresh-review/stop boundary. Never executes an old proposal, changes selected pairs silently, or replaces a rejection automatically. |
| Only `admin_membership_business_roles_set` is available for a full assignment request | Explains that additions save labels without confirming scopes or new role permissions. Does not perform a misleading substitute or claim completion from existing access. Explicit label-only requests retain live legacy restrictions and removal consequences. |
| Existing first-party conversation uses an older profile after plugin/backend update | Reports unsupported capability honestly. Uses a new conversation with verified profile/source/digest for adoption; never loads branch instructions or widens the old delegation. |

Package tests establish dependency closure, checksums and required tool names.
They do not demonstrate these behavioral outcomes, browser approval, runtime
permission enforcement or installation/profile adoption.
