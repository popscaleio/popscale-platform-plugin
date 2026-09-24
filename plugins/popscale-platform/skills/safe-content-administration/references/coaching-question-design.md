# Coaching question design

Apply when authoring, reviewing or revising Coaching inputs, including Journey
items. Adapt to the selected Coaching type, learning purpose, audience and
company's approved sources. This is an input-quality review, not a new platform
validator or a fixed question-count rule.

## Design the participant's task

- Give each participant-facing question one primary reflection or assessment
  goal. Phrase it as the natural utterance the participant should hear, with a
  clear expectation: identify, explain, decide, practise a response or reflect.
- When a brief trains separate skills, use an ordered progression where the
  selected type supports multiple questions. For example, understanding a need
  can precede selecting a relevant response. That is one possible progression,
  not a universal customer/sales sequence or a required number of questions.
- Preserve the selected type's interaction: a knowledge assessment should not
  gain coaching hints, and a type built around one sustained question, objection
  or situation should not become a multi-question quiz. Narrow the task or
  propose a suitable separate session/type if needed, within the user's scope.
- Give only the scenario facts needed to understand the current task. Include
  essential context in participant-facing wording rather than assuming the
  participant sees administrative background fields. Later questions can refer
  to established context and earlier answers without repeating the whole case.
- Use natural language in questions. Keep internal labels such as `Analysis:`,
  `Task:` or `Instructions:`, scoring mechanics and model-facing directions in
  the appropriate authoring fields rather than spoken text. Ordinary use of
  those words in the subject matter is not a defect by itself.
- Keep constraints the participant needs to perform the task in the question.
  Put answer expectations in the reference answer and assessment guidance in
  supported inputs such as `evaluation_input`, `success_behaviours` or
  `critical_missteps`, according to the live schema. These inputs do not replace
  an essential participant instruction and are not generated instruction outputs.
- Align each reference answer and its points with that question's goal. A
  question about understanding a situation should be assessable on that basis,
  without requiring an unasked product list or a later response formulation.
  Keep facts grounded in approved sources and qualify information that may vary.

## Review before saving or dispatching

Review proposed inputs before a write or generation dispatch, and generated
inputs when they become available for review. Flag dense scenario text,
internal labels, multiple independent tasks, or several question marks for
semantic review. Explain the specific ambiguity and propose a focused change;
punctuation or length alone is not grounds for automatic rewriting.

A decision and its justification can form one coherent goal. Keep a multipart
question when the parts need to be answered together and explain why. Choose
question count and length from the skill being practised, session duration and
live schema limits, rather than always splitting into three or four steps.

When revising existing inputs, read the current complete question set and total
score first. For a focused split, preserve unaffected questions, answers and
points. Distribute the original question's points across its replacements so
the total remains unchanged unless a score change was explicitly requested.
If the live point/count limits make that impossible, explain the conflict and
resolve the proposed design before saving; never silently change the total.

## Save inputs, regenerate instructions, verify

Use structured `reference_facts` (`question`, `answer`, `max_points`) when the
live contract supports it. Treat `questions_answers` as its legacy mirror;
follow the live schema for any legacy-only route. Read saved inputs back to
verify the question order, answer alignment, each point allocation and the
server-calculated `obtainable_evaluation_score`. A successful write alone does
not establish that the intended split or total was preserved.

Every change to Coaching generation inputs still requires platform generation
of BOTH `agent_prompt` and `evaluation_instructions` after the final input edit,
as defined in [generation verification](generation-verification.md). Never edit
either output manually. Establish a supported, authorized regeneration path
before changing inputs, including for active content.

Read both newly saved outputs and their linked completed request steps. Verify
that the agent instructions reflect the revised question order and the selected
type, and that evaluation follows the corresponding answers and point totals.
Evaluation need not repeat the question set verbatim. Keep the update incomplete
and stop plugin activation when either output is missing, stale, edited,
unverified or still follows the old inputs, even if server readiness is green.
Do not claim the server itself enforces this semantic review. Route any mismatch
through authorized input correction and platform regeneration, preserving
unrelated content and existing publication approvals.

Read the coaching-question evaluation scenarios in the repository's `docs/evaluation/` directory when
evaluating this guidance in a host.
