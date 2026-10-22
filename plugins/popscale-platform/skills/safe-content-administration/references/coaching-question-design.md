# Coaching question design

Review proposed and generated Coaching inputs before saving/dispatching, including
Journey items. Adapt to type, audience, purpose and approved sources. This is
quality guidance, not a validator or fixed question count. Apply
[conversation assessment](conversation-assessment.md) for task mode and evidence.

## Participant task

Give each question one primary goal, expressed naturally: identify, explain,
decide, practise or reflect. Separate independent skills into an ordered progression
only where the type supports multiple questions. Preserve knowledge assessment
without coaching hints and sustained-question types without converting them into
quizzes. Otherwise narrow scope or propose another session/type.

Include essential facts and constraints in participant-facing wording; administrative
background may be invisible. Later questions can reuse established context. Put
internal labels, scoring mechanics and model directions in authoring fields;
ordinary subject-matter uses of those words are acceptable. Put answer expectations
in reference answers and assessment guidance in schema-supported inputs such as
`evaluation_input`, `success_behaviours` or `critical_missteps`. These cannot replace
necessary participant instructions and are not generated outputs.

Align answers and points to the asked goal without unasked product lists or later
tasks. Ground facts in approved sources and qualify variable information. Review
dense scenarios, labels, independent tasks and multiple question marks semantically;
length/punctuation alone do not justify rewriting. A decision with its justification
can be one coherent goal; explain retained multipart questions. Choose count/length
from purpose, duration and live limits, not a fixed split.

## Preserve and verify

Read the complete question set and total before revision. Preserve unaffected
questions, answers and points. Splits redistribute existing points unless a score
change was explicitly requested; resolve incompatible point/count limits before saving.

Use structured `reference_facts` (`question`, `answer`, `max_points`) where supported;
`questions_answers` is its legacy mirror. Follow the schema for legacy-only routes.
Read back order, answers, allocations and calculated `obtainable_evaluation_score`.

Establish a supported, authorized regeneration path before any input edit, including
active content. After the final edit regenerate BOTH `agent_prompt` and
`evaluation_instructions` through the platform; never manually edit them. Follow
[generation verification](generation-verification.md): both require fresh, current,
unmodified metadata linked to completed post-edit request steps. Redacted text
cannot be semantically reviewed. Keep missing, stale, edited or unverified pairs
incomplete despite green readiness. Check visible type, questions, answers and totals;
correct mismatches through authorized input edits and regeneration.

See the repository's `docs/evaluation/` coaching-question scenarios.
