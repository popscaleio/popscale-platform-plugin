# Study Design Quality

Use this reference when creating a Study or substantially redesigning its
questions. For a focused edit, apply only relevant guidance to the affected
topic; leave unrelated topics and settings intact. Design review alone does
not authorize mutations, publication, invitations, or live test runs.

## Review the design as a whole

Evaluate information quality and respondent experience separately. A useful
analysis does not prove that the respondent was heard, and a technically ready
draft does not prove either outcome.

Start with the Study's purpose, required insights, audience, and promised time.
For each topic, align its main question, must-cover points, conditional probes,
completion criteria, and relevant extraction fields. Completion should describe
what needs to be understood, not merely that a subject was mentioned or a fixed
number of questions was asked. Treat respondent refusal or a request to move
on as a valid reason to stop probing even when information remains missing.

## Choose probes by missing information

| Response | Authoring guidance |
| --- | --- |
| Positive | Explore the reason or a concrete example when understanding success matters to the purpose; otherwise avoid unnecessary probing. |
| Neutral or factual | Clarify only what is needed for the research question. |
| Mixed | Preserve both the positive experience and the improvement need. |
| Negative | Acknowledge the contribution, then explore relevant gaps such as impact or desired change/support. |
| Sensitive or emotional | Use restrained acknowledgment, offer the option not to elaborate, and avoid pressure or unnecessary personal details. |
| Short or ambiguous | Ask for clarification or an example when useful and welcome; a refusal is not ambiguity to overcome. |

Write one thought per main question; put the reason or the comparison in a
probe. "Would you recommend joining?" is one question; "would you recommend
it, do you know someone in a similar role, and why or why not" is three.
Ask one question at a time. Do not prescribe a minimum probe count: a respondent
may already have supplied the example, impact, and desired change in one answer.
Acknowledgment should not impose an emotion, endorse an unsupported conclusion,
or introduce a leading explanation.

For meaningful negative, mixed, or sensitive feedback, provide an opportunity
to add something before changing topic, unless the respondent already asked to
move on or stop. Put that check-in inside the topic, before its completion;
keep the final interview closing as a thank-you rather than another question.
When an experience is relevant to a later topic, reuse what was already said
and ask only about the new aspect. Do not ask for what the invitation already
carries: role or title, team or department, region or market and respondent
type are invite fields and flow into the analysis as segments.

## Preserve respondent choice and research purpose

- Allow the respondent to decline detail, skip a topic, or end the interview.
  Missing required information is not permission to pressure them.
- Align topic count and depth with the time promised in the description and
  intro. If time is an estimate, ask whether the respondent wants to continue
  before exceeding it. Respect a fixed limit and requests to stop. Do not
  silently extend the duration or promise unverified runtime controls.
- Keep interviewing separate from coaching. Do not give unsolicited advice,
  shift responsibility for an organizational problem to the individual, or
  promise follow-up. If advice is requested, a neutral referral to a suitable,
  verified contact may be appropriate; never imply an automatic notification.
- For sensitive Studies, use the actual privacy setup and approved handling
  guidance. Never invent anonymity guarantees, escalation capabilities, or
  contact details. Surface missing handling decisions when they matter to the
  requested Study rather than inventing them.

## Capture useful evidence without forcing answers

Choose extraction fields according to the purpose. Candidates include the
experience or improvement need, a concrete example, frequency, impact, desired
change, desired support, and whether an issue was raised and what happened.
Do not add all fields to every topic. Distinguish a missing or declined answer
from an explicit negative answer; do not infer details the person did not give.

Use the current tool schema and existing field keys. The current authoring
contract provides topic `main_question`, `must_cover`, `probe_examples`,
`completion_criteria`, and `extract_fields`, plus draft `completion_rules`.
Prefer targeted probe/must-cover append/remove and keyed extraction-field
upserts. Read the existing completion rules and supported schema before editing
them; these design recommendations are not new JSON keys or a new product
setting. Do not replace unrelated rules to insert a general policy.

## Synthetic example

Purpose: understand what helps or hinders weekly planning in a fictional tool.

Main question: “How does planning your week in the tool work for you?”

Conditional probe examples:

- If the experience is unclear: “Can you describe an occasion?”
- If a difficulty is mentioned but its impact is missing: “What effect does
  that have on your work?”
- If desired change is missing: “What would make planning easier?”
- If it works well and the reason matters: “What about it helps you?”

Completion criteria example:

> Understand what works or needs improvement. For a difficulty, explore relevant
> impact and desired change that have not already been explained. Acknowledge
> meaningful feedback and offer a chance to add something before changing topic.
> Reuse earlier answers. If the respondent asks to move on or end, respect that
> immediately even when evidence is incomplete.

Adapt this to the purpose rather than copying it to every topic.

## Review and verification evidence

Before handing over a new or redesigned Study, report three separate states:

1. **Design reviewed:** which relevant criteria were checked in the actual draft
   and what gaps remain.
2. **Publish readiness:** the server's current errors and warnings, when that
   check was requested or needed for publication.
3. **Conversation tested:** which synthetic scenarios were actually exercised,
   on what version, and what the interviewer did; otherwise say not tested.

Use the authoring-host and respondent-conversation scenarios in
the host evaluation scenarios in the repository's `docs/evaluation/` directory. A simulated transcript or
offline design review must not be reported as a live product test. Keep live
test setup and mutations within the authorized scope and use a dedicated test
company. An observed failure despite clear design instructions is a product
behavior investigation, not proof that more wording will fix it. Preserve
bounded evidence and report the gap without claiming a runtime change.
