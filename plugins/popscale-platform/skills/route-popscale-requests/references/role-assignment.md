# Assign a role on selected units

Use authenticated `popscale-platform` and the shared
[product action contract](product-actions.md). Business roles, responsibility
units, own affiliations and permission sources are separate. Public Docs and
existing aggregate access establish none of them.

## Select and review

1. Check `current_user` and `capabilities` for the intended company, live
   authority and available administration tools. Resolve the exact person with
   `admin_user_list` / `admin_user_get` and retain the returned membership UUID.
   Read `admin_membership_organization_get`, `admin_business_role_list` and
   `admin_unit_list`; use `admin_unit_get` when needed. Follow pagination before
   selecting from catalogs. Ask about ambiguous people, roles or units; never
   guess identifiers or infer responsibility from all of a person's own units.
2. Obtain the explicitly chosen role and nonempty responsibility-unit selection.
   `admin_membership_role_units_add` accepts `membership_id` and nonempty
   `business_roles`, each containing `role_id` and nonempty `unit_ids`, plus the
   stable `command_id`. Follow live bounds. Units must be current own units of
   that person. Missing affiliation requires a separate authorized workflow;
   do not add affiliations, remove old roles/scopes or substitute manual grants.
   This operation adds exact pairs and preserves unrelated roles, earlier scope,
   permission tier, own units and direct permission sources.
3. Inspect the saved preview's `role_assignment_review` version 1. Show the
   named person, selected roles/units, added or retained unit and company
   permission sources, capabilities, descendant effects and relevant policy
   versions. Compare complete sources and per-role counts, separately from
   `effective_access_changes`. Existing direct access can make that net change
   empty while a new role-owned source still requires review. Include company
   sources even when no net permission changes; disclose session invalidation
   and self sign-out. A role with no configured permissions grants none.
4. Present the unchanged server review link and wait for human approval of this
   exact proposal. Chat consent, a confirm boolean and host tool confirmation
   cannot approve it. Read the same action with `product_action_get`, then use
   `product_action_execute` only under its current approved state and `next_step`.
   Preserve command/payload identity on uncertainty. Changed authority, policy,
   scope or an expired proposal follows the shared fresh-review boundary.

## Verify the committed assignment

Action approval or `succeeded` alone is insufficient. Inspect the committed
`result.role_assignment_verification`: version 1, `verified=true`, the selected
membership and every requested role. For each role require
`company_authority_confirmed=true`, `unit_scope_confirmed=true` and
`unit_scope_complete=true`. Its `requested_unit_ids` must match that selection;
persisted `unit_ids` must contain them and preserve earlier scope. Check the
returned `scope_unit_ids`, rather than inferring scopes from capabilities.

Require `permission_sources_complete=true`. Match every expected source from
the approved review to the receipt's role, unit/company scope, capabilities,
descendant policy and effective/accepted template versions. Retained source
identities must match; added sources can have a null preview `source_id` but
must have a committed source identity in the receipt.
Direct grants or aggregate permissions cannot replace role-owned source proof,
including when the net access change is zero. A complete empty source list is
valid only when the reviewed role has no configured sources. Confirmation flags
alone never prove a live company permission binding. Verify the preservation
fields; report missing or inconsistent evidence as unverified, not complete.

This receipt is captured and verified in the native transaction. A fresh
`admin_membership_organization_get` can supplement it when access remains;
it is not required after the approved change invalidates the current connection.
Report assignment and permission effects separately in product language.

## Legacy tool and unavailable capability

`admin_membership_business_roles_set` remains the legacy role-label collection
tool. Its additions do not confirm role-unit scopes or new role permissions;
collection removals may retire earlier role-owned access. Retain its live host
restrictions, including additions-only behavior where enforced. Never use it
as a substitute for full assignment or claim existing access proves completion.
If the full tool or required proof is unavailable, explain that limitation and
offer organization administration; do not bypass it with another tool or browser.
