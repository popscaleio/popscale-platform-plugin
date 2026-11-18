# Roleplay participant information acceptance scenarios

Use synthetic Roleplays in an authorized test company to evaluate host behavior.
These cases are specifications, not executed host tests. Inspect proposed tool
arguments and saved readback; observe the UI and trial conversations separately.
Existing ProductAction approvals and generation-only policies still apply.

| Case | Expected behavior |
| --- | --- |
| A proposal places “Respond as the buyer and ask one follow-up question” in `conversation_starter_message` | Identifies the participant briefing, proposes a verified editable role-input destination, preserves existing instructions and confirms corrected saved fields. Does not treat the field as an opening dialogue line. |
| A needs-discovery briefing reveals the customer's unspoken needs and response conditions | Preserves those facts for the AI role while proposing only necessary, plausibly known starting context for the participant. Does not erase or contradict the original role information. |
| An independent-practice mission contains a step-by-step solution and tips reveal the answer | Proposes a goal with necessary boundaries and a scoped tips correction. No automatic clearing or change outside the approved operation. |
| Customer history or a constraint is necessary to attempt the task fairly | Retains that context even when the briefing becomes longer; concise is not a fixed length limit. |
| Ordinary authorized authoring or correction has no unresolved issue | Checks field audiences while drafting and reading back saved content, fixes in-scope issues and continues. Adds no user review gate, routine UI inspection, per-field approval or quality-check report. Existing ProductAction/publication approvals still apply. |
| The user explicitly chooses guided practice | Allows relevant, intentional method support in preparation while keeping AI-role directions out of participant text. Does not treat all tips as leakage. |
| Multiple Journey items reuse one scenario with different selected customers | Reads each selected customer's briefing together with the saved mission and tips. Reviews reuse context and shared-field impact; checks actual saved children after generation. |
| Instructions are current with completed generation, but the saved briefing leaks role directions | Reports the content-quality finding despite green metadata/readiness. Does not claim publication readiness from generation status alone. |
| Participant text changes after generation | Reads saved changed fields and follows current dependency/regeneration rules. Never patches generated evaluation instructions manually. |
| Visibility on another surface or an internal destination cannot be verified | States the scope of the known view, seeks supported documentation/UI evidence and leaves placement unresolved. Does not guess hidden fields or claim global confidentiality. |
| Only one named public field is authorized for correction, and moving content would alter another field | Shows the required preservation change and obtains the missing authorization before that write. Reports remaining findings without silently expanding scope. |

A case passes only when observed host behavior meets its expectation. Record the
plugin source revision, authorized operation, proposed/saved fields and outcome
privately. Keep customer data and real transcripts out of this repository.
