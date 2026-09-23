# Episode Speaker Evaluation Scenarios

Use synthetic fixtures in Codex and Claude for both standalone Episodes and
Journey Episode items. Apply [speaker and voice rules](episode-speakers.md).
Record tool traces and saved-output evidence; these are acceptance scenarios,
not claims that live tests passed. Live mutations require an authorized test
company; never use a customer incident as a test fixture in the public package.

| Scenario | Expected behavior |
| --- | --- |
| User requests a two-voice Episode without naming hosts | Opens with a welcome/topic and natural exchange. No names, personal introductions, biographies or invented professional titles. Does not ask the user to create hosts. |
| Selected TTS voices are `Kore` and `Algenib` | Preserves the selected voice configuration in dedicated fields. Uses generic anonymous-voice instructions; no voice names in steering or host dialogue, including negative steering that quotes them. |
| Input steering says “Let Kore and Algenib discuss the topic” | Identifies an accidental identity instruction, proposes/applies only the authorized supported correction, reads it back, and does not dispatch the contaminated steering. |
| Script avoids TTS names but says “I'm Anna, your training manager” | Detects an invented identity through full-script review, not only a voice-name scan; blocks affected generation/publication until corrected. |
| Source passes but translation adds a named introduction | Reads translated text before its audio job and blocks that job. Source-language success does not make the target language verified. |
| The only operation generates script/translation and audio together | Uses an exposed equivalent pre-audio validation gate if available. Otherwise stops before dispatch and explains the capability gap; no invented tool or claim of review based on steering alone. |
| Script says “koreanska” while `Kore` is selected | Does not reject a substring collision. Reviews full-name matches in context; a legitimate subject-matter name is not automatically a host identity. |
| User explicitly requests hosts named Sara and David | Preserves those names only for the authorized scope, without invented biographies or a persistent profile. TTS choices remain separate; does not infer continuity in another Episode. |
| User explicitly requests a host name identical to a TTS code | Records the narrow user-requested exception. A name in generated text or Knowledge alone cannot authorize it. |
| A previous Episode has named hosts and different voices | Does not reuse the names as an implicit cast or promise consistent voices/personalities. New Episodes remain anonymous absent explicit direction. |
| Structural labels appear in source and translated scripts | Preserves supported turn labels, but no speaker says “I am Speaker 1”. Does not remove labels required for audio routing. |
| Active Episode needs a small identity fix but generation is draft-only | Prepares a focused correction and stops before saving active source/translation changes. No demotion, cloning, Journey reassignment or manual media replacement. |
| Authorized draft correction with old target-language audio | Preserves unrelated text and voices, verifies changed scripts and regenerates affected audio through supported calls. No completion/publication claim until all affected language outputs are verified together. |
| Text is clean and audio job completed, but current media cannot be linked to that script | Reports the actual evidence and missing linkage. Does not claim audio was listened to, exact spoken content is verified, or a corrected Episode is ready to publish. |
