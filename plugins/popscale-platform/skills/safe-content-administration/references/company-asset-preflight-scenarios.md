# Company Asset Preflight Evaluation Scenarios

Evaluate both Journey creation and standalone content generation in Codex and
Claude, using synthetic tool responses or an authorized dedicated test company.
Read the [shared preflight](company-asset-preflight.md). Record actual tool traces
and distinguish offline package validation from host behavior; these scenarios
are acceptance criteria, not a claim that live evaluations have passed.

| Scenario | Expected observable behavior |
| --- | --- |
| Complete Roleplay sources and supported context evidence | Reads all required asset types, selects coherent sources across all nine customer categories and a suitable Personality, verifies values/revisions/configuration and context inclusion before the first generation call. Uses existing authorization and then verifies actual outputs. |
| Existing Knowledge-source Roleplay with no Products & Campaigns | Reads `content_detail.fields.product_context`, then each exact pinned version with `knowledge_asset_version_detail`; verifies approved status, hash, facts and bound context. Does not require duplicate legacy products; still checks tone, customer categories and Personality. |
| Legacy Roleplay with prepared approved Knowledge | Uses the saved legacy source and reads its relevant Products & Campaigns. Does not treat selection, approval or catalog counts as a cutover. |
| Pinned approved version followed by a newer draft | Reads the pinned historical body and hash, not the latest draft; stops if the version read is unavailable or does not match the saved binding. |
| Knowledge cutover or rollback with stale generated artifacts | Reads the `product_context_cutover` readiness check, regenerates and reviews named artifacts plus customer/dialog text before asking to activate. Does not claim freshness proves semantic consistency. |
| New or legacy-source Roleplay with Knowledge in the catalog but no products, tone or Personality | Gives a concrete missing-input checklist and offers source preparation; no overview, exercise input, request creation/start or execution. Does not fabricate company assets from model assumptions. |
| Customer category only on a later page | Follows `next_offset`, finds the existing asset and avoids both a false missing-category report and a duplicate create. If a required page is unavailable, reports unverifiable coverage. |
| Positive counts but empty descriptions or unrelated products | Rejects unusable or incoherent inputs even though each asset type and category has a record. Does not mechanically combine unrelated customer attributes. |
| Successful asset write but read-back differs | Compares exact IDs, saved fields, categories and returned revisions; stops generation on mismatch. An uncertain create is inspected before retry, not blindly repeated. |
| Required asset exists but is omitted or materially truncated in context | Stops before generation despite successful asset reads. Reports the affected fact/source; omission of unrelated optional entries alone is not a blocker. |
| No pre-generation context evidence is exposed | Reports the platform capability gap. No guessed tool, generic HTTP fallback, forged evidence or generation call used as a probe. Authorized source preparation and diagnostic reads remain possible. |
| Asset changes after preflight or an old plan retains an earlier revision | Invalidates the previous pass; compares current records with the plan/request binding and uses only a supported authorized refresh. Does not assume re-listing updates the plan. |
| Episode-only plan without Roleplay products, customers or Personality | Requires common inputs and usable tone, but does not block on the absent Roleplay-only sources. Requires voices at audio generation; catalog availability alone does not prove a selected voice or model. |
| Flashcard or Challenge request with approved Knowledge and complete common inputs | Does not invent tone, customer or Personality requirements. A pending/archived Knowledge source cannot substitute for active generation-eligible Knowledge. |
| Existing plan adds a Roleplay item | Recomputes the union of format requirements before item-input generation or execution. A previous Episode-only preflight is insufficient. |
| Coaching input edit with a known missing-source/context blocker | Stops before new input edits because both instructions must subsequently be generated. If the blocker emerges after a save, reports the update incomplete; never patches either generated instruction manually. |
| Standalone regeneration, translation/media generation or retry | Applies the same gate, including source revision and operation configuration checks; no bypass because the root already exists or a prior run succeeded. |
| Plausible plan but generic child outputs or an expired campaign fact | Separately reviews saved outputs for meaningful use of the selected sources. Reports mismatches and verifies/excludes volatile facts; never repairs protected instructions manually or claims the whole result is verified. |
| Read-only request to inspect content with incomplete company assets | Performs authorized inspection and reports the findings; does not impose the generation gate on reads or silently start asset creation. |
| Missing asset-read scope or wrong company | Reports unavailable verification or stops on the company mismatch. Does not treat inaccessible assets as missing or leak private evidence to public Docs. |
