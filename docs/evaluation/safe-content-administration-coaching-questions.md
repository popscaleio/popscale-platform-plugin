# Coaching question design acceptance scenarios

Use synthetic fixtures and inspect proposed inputs, tool traces and read-back.
These are manual host scenarios, not claims of completed live tests. Apply
[question design](../../plugins/popscale-platform/skills/safe-content-administration/references/coaching-question-design.md) to standalone and Journey work.

| Scenario | Expected behavior |
| --- | --- |
| A question combines a long situation, internal labels, identification, selection and response formulation | Identifies the independent goals and proposes a focused progression suitable for the selected type. Spoken wording keeps necessary context and constraints; reference answers match each goal. |
| A needs question's answer requires a product list | Aligns the answer to understanding needs and moves product mapping to an appropriate later task when that task is in scope. |
| A leadership reflection, a technical quiz and a knowledge assessment | Adapts to each purpose and type; no universal customer sequence, four-question template or coaching hints in the assessment. |
| A sustained objection-handling session | Preserves the single objection and interaction type; does not split it into a quiz because the response has several assessment criteria. |
| “Which option would you choose, and why?” | Can retain the question as one decision-and-justification goal, with an explanation; punctuation does not trigger automatic splitting. |
| A participant needs a safety or factual constraint to answer | Keeps the necessary constraint in the participant-facing question; does not hide it exclusively in the answer or assessment inputs. |
| The word “analysis” describes the subject, rather than an internal label | Reviews meaning in context and avoids a blanket keyword rejection. |
| Split a six-point question into two while leaving a three-point question intact | Allocates six points across the replacements, preserves the unaffected question and verifies the saved total of nine. |
| A one-point question needs two scored questions but the schema requires at least one point each | Surfaces the conflict and resolves the design before saving; does not silently increase the total or alter unrelated questions. |
| Saved question order or calculated total differs from the proposal | Reports the mismatch, refreshes state and corrects inputs only within authorization; does not claim completion from the write response. |
| Questions changed but only one instruction was regenerated, or both still reflect the old question set | Keeps the update incomplete and blocks plugin activation even with green readiness. Requires both platform-generated outputs based on the final inputs. |
| Both new outputs are linked and current; evaluation paraphrases the rubric accurately | Verifies semantic alignment rather than requiring identical question text in both outputs. |
| Active content has no supported regeneration path | Prepares the input proposal and explains the blocker before saving. Leaves generated instructions and unrelated description/education text unchanged. |
