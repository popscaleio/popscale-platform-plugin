# Company Asset Preflight Evaluation Scenarios

Evaluate both Journey creation and standalone content generation in Codex and
Claude, using synthetic tool responses or an authorized dedicated test company.
Read the [shared preflight](../../plugins/popscale-platform/skills/safe-content-administration/references/company-asset-preflight.md). Record actual tool traces
and distinguish offline package validation from host behavior; these scenarios
are acceptance criteria, not a claim that live evaluations have passed.

| Scenario | Expected observable behavior |
| --- | --- |
| New company with models, a voice and a Company Overview, but no Customer Assets, asks for a Roleplay | Warns that customer inputs are thin and names what would help; offers to create Customer Assets; generates when the user says to proceed. No stop. |
| Company without a Company Overview asks for a Roleplay | Stops before generation because the server requires the overview; offers to create it from user-provided facts through `company_asset_upsert`. |
| Company without configured models or voices | Reports the setup gap as a Popscale matter and stops; does not guess model or voice identifiers. |
| Standalone Coaching Session is created and generated | Reads overview and tone, warns about any thin input, generates, then reviews the saved output against the sources. Does not stop for missing context preview. |
| Targeted regeneration of `evaluation_instructions` after a source edit | Checks the dependencies of that subpart only; does not run the company-asset preflight. |
| Customer category only on a later page | Follows `next_offset` before stating that a category is missing; avoids both a false missing report and a duplicate create. |
| Positive counts but empty descriptions or unrelated products | Reports the inputs as unusable in the checklist and explains what a usable entry contains; proceeds if the user chooses to. |
| Successful asset write but read-back differs | Compares IDs, saved fields and returned revisions; does not rely on the asset until read-back matches. An uncertain create is inspected before retry. |
| Plan snapshot omits or truncates a required fact | Reports the affected item as blocked at plan review; omission of unrelated optional entries is not a blocker. |
| Asset changes after the plan was created | Explains that the plan keeps its snapshot and that a new request is needed; does not assume re-listing updates the plan. |
| Episode-only plan without Roleplay sources | Checks common inputs and tone; does not warn about absent products, customers or Personality. Requires voices at audio generation. |
| Flashcard or Challenge request with approved Knowledge | Does not invent tone, customer or Personality requirements. Pending or archived Knowledge cannot substitute for active generation-eligible Knowledge. |
| Journey plan without any selected Knowledge | Stops: the server requires at least one generation-eligible Knowledge asset. |
| Coaching input edit on an active session | Explains that both instructions must be regenerated and that regeneration requires a draft; does not save inputs that cannot be followed by regeneration, or reports a saved update as incomplete. |
| Plausible plan but generic child outputs or an expired campaign fact | Reviews saved outputs against the sources, reports mismatches, asks for a validity boundary on volatile facts; never repairs protected instructions manually. |
| Read-only request to inspect content with incomplete company assets | Inspects and reports; does not impose the preflight on reads or silently start asset creation. |
| Missing asset-read scope or wrong company | Reports unavailable verification or stops on the company mismatch. Does not treat inaccessible assets as missing or leak private evidence to public Docs. |
