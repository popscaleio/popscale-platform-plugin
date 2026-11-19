# Coaching question design

Review proposed/generated Coaching inputs before save/dispatch, including Journeys.
Adapt to type, audience, purpose and approved sources; no fixed question count.
Apply [conversation assessment](conversation-assessment.md) for task/evidence.

## Participant task

Each spoken question needs one primary goal. Sequence independent skills only where the type supports multiple
questions. Preserve knowledge assessment without hints and sustained-question
types without converting them into quizzes; otherwise narrow scope or propose
another session/type. Include necessary facts/constraints in participant wording;
admin background may be invisible. Reuse established context in later questions.
Keep internal labels, scoring/model directions in authoring fields, except normal
subject-matter uses. Put answer expectations in reference answers and guidance
in supported `evaluation_input`, `success_behaviours` or `critical_missteps`;
these cannot replace essential participant instructions or generated outputs.
Align answers/points with the asked goal, without unasked product lists/later tasks.
Ground/qualify facts. Review dense scenarios, labels, tasks and punctuation
semantically; length alone warrants no rewrite.
Decision/justification can be one goal; explain retained multipart questions. Choose count/length from purpose, duration and live limits.

## Round count

`round_limit` is a positive whole-number count, not minutes, instructions,
`reference_facts` count, score or dialogue-turn count. Use the live representation
and declared range; a string schema needs e.g. `"2"`, not `"two rounds"`.
Reject proposed prose, booleans, decimals, zero/negative or out-of-range counts.
Do not invent a maximum/default from conflicting sources, or universal two-round
policy. Resolve consequential uncertainty; a bare string schema proves no range.
Never convert minutes to rounds. Use editable `other_information` or another
verified input for timing/conduct, preserving existing text and scope.

Apply across manual/standalone creation, Journeys and edits. Read normalized/saved
values; schema/generation success is insufficient.
For legacy prose, preserve instructions and unrelated fields/points,
choose a justified count within authorization and regenerate both instructions.
Do not assume whether a round means a whole retry, per-question attempt or reply;
saved count/current metadata proves no hard runtime cap. Disclose unverified behavior.

## Preserve and verify

Read the complete question set/total before revision; preserve unaffected entries.
Splits redistribute original points unless score changes were requested; resolve
incompatible count/point limits before saving. Use structured `reference_facts`
(`question`, `answer`, `max_points`) where supported; `questions_answers` is its
legacy mirror, with schema-defined legacy-only routes. Read back order, answers,
allocations, selected type and calculated `obtainable_evaluation_score`.

Establish authorized regeneration before input edits, including active content.
After final edits generate BOTH `agent_prompt` and `evaluation_instructions` through
the platform, never manually. Follow [generation verification](generation-verification.md):
fresh/current/unmodified metadata linked to completed post-edit steps for both.
Redacted text cannot be reviewed. Missing/stale/edited/unverified pairs stay
incomplete despite readiness; correct visible mismatches through authorized inputs
and regeneration. See repository `docs/evaluation/` scenarios.
