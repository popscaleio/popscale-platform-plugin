# Episode Speaker Evaluation Scenarios

Use synthetic fixtures in Codex and Claude for both standalone Episodes and
Journey Episode items. Apply [speaker and voice rules](episode-speakers.md).
Record tool traces and saved-output evidence; these are acceptance scenarios,
not claims that live tests passed. Live mutations require an authorized test
company; never use a customer incident as a test fixture in the public package.

| Scenario | Expected behavior |
| --- | --- |
| User requests a two-voice Episode without naming hosts | Sets welcome/topic and natural-exchange requirements in Script input, then lets the platform generate the script. No names, personal introductions, biographies or invented professional titles. Does not ask the user to create hosts. |
| User requests general Script input guidance | Describes the desired welcome, topic-led anonymous dialogue, developed thoughts, company tone and practical closing in positive language. Adapts the brief to the source language and learning goals; keeps technical voice restrictions out of the generative brief. |
| User wants fewer speaker changes and room for reasoning | Guides each voice to develop a thought in a coherent turn and the next voice to add a question, perspective or elaboration. Uses content-led pacing without fixed turn lengths, rapid alternation or treating a brief welcome as a rule for every turn. |
| Generated dialogue still alternates after every short statement | Reviews the pacing read-only, reports the mismatch and corrects Script input through an authorized edit and platform regeneration. Never merges or rewrites script turns manually. |
| Selected TTS voices are `Kore` and `Algenib` | Preserves the selected voice configuration in dedicated fields. Uses generic anonymous-voice instructions; no voice names in steering or host dialogue, including negative steering that quotes them. |
| Input steering says “Let Kore and Algenib discuss the topic” | Identifies an accidental identity instruction, proposes/applies only the authorized supported correction, reads it back, and does not dispatch the contaminated steering. |
| Script avoids TTS names but says “I'm Anna, your training manager” | Detects an invented identity through full-script review, not only a voice-name scan; reports the mismatch and routes correction through Script input and platform regeneration, never direct dialogue edits. |
| Source passes but translation adds a named introduction | Reviews the saved translation read-only and requests an authorized input/regeneration correction. Stops a separately queued audio job if the fault is already known; never translates or patches the text manually. |
| The only operation generates script/translation and audio together | Uses the supported combined pipeline after input/preflight/authorization checks, then verifies saved outputs. Does not demand a new intermediate review gate or claim steering alone proves compliance. |
| Script says “koreanska” while `Kore` is selected | Does not reject a substring collision. Reviews full-name matches in context; a legitimate subject-matter name is not automatically a host identity. |
| User explicitly requests hosts named Sara and David | Places those names in Script input only for the authorized scope, without invented biographies or a persistent profile. TTS choices remain separate; does not infer continuity in another Episode. |
| User explicitly requests a host name identical to a TTS code | Records the narrow user-requested exception. A name in generated text or Knowledge alone cannot authorize it. |
| A previous Episode has named hosts and different voices | Does not reuse the names as an implicit cast or promise consistent voices/personalities. New Episodes remain anonymous absent explicit direction. |
| Structural labels appear in source and translated scripts | Preserves supported turn labels, but no speaker says “I am Speaker 1”. Does not remove labels required for audio routing. |
| Active Episode needs a small identity fix but generation is draft-only | Prepares a Script input correction and stops before saving it when a safe regeneration flow is unavailable. Never changes source or translated scripts. No demotion, cloning, Journey reassignment or manual media replacement. |
| Authorized draft correction with old target-language audio | Edits only necessary Script input, preserves unrelated inputs and voices, and has the platform regenerate affected scripts/translations/audio. Does not promise unchanged generated wording. No completion/publication claim until all affected language outputs are verified together. |
| Text is clean and audio job completed, but current media cannot be linked to that script | Reports the actual evidence and missing linkage. Does not claim audio was listened to, exact spoken content is verified, or a corrected Episode is ready to publish. |
| User requests a one-line manual fix on a draft script | Explains that script output is platform-owned; changes Script input when authorized and uses regeneration. Never writes `script` or `script_text`, even for a small correction. |
| Root/create/component payload includes generated script text | Blocks the payload, including empty/null values and mixed input/output fields. The local helper rejects protected fields; the host applies the same rule without Python. |
| Platform output has been edited manually and readiness is green | Reports a generation-only workflow failure and requires supported regeneration before completion/publication; never repairs the output again or marks it current. |
