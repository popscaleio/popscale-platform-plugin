# Episode Speakers and TTS Voices

Apply this policy to standalone Episodes and Episode items in Journeys, including
source inputs, scripts, translations, audio generation and corrections. Keep the
[company asset preflight](company-asset-preflight.md) and live authorization
contract in force; this policy does not add a tool or permission.

## Anonymous conversation is the default

Use anonymous conversational voices. Start with a welcome and the topic, then
move into a natural exchange. Do not invent host names, job titles, biographies,
personal histories or recurring podcast personas. Warmth, differing viewpoints
and a conversational tone do not require personal identities.

For example, a Swedish opening may be:

> Speaker 1: Hej och välkomna! I dag ska vi prata om hur man ställer bra frågor.
>
> Speaker 2: Ja! Det är intressant, för en liten förändring i frågan kan ge ett
> mycket tydligare svar.

`Speaker 1` and `Speaker 2` are structural turn labels for the two-speaker
format, not spoken introductions. Do not write “I am Speaker 1”, “I'm your
training manager”, or “As I told you in our last episode” to manufacture an
identity or continuity. Preserve legitimate names, quotations and roles in the
subject matter; they do not automatically identify a host.

Do not ask the user to name the hosts as a routine setup step. Only depart from
anonymity when the user explicitly requests participant-facing host identities;
preserve only the identities and attributes they actually supplied. A name in
Knowledge, an old generated script, a TTS catalog or a previous Episode is not
such an instruction. Do not invent missing names or backgrounds.

There is no persistent podcast-profile feature in this workflow. Do not create
or promise a recurring cast, infer a stable persona from a voice, or claim the
same host/voice will persist across Episodes or languages. An explicit name for
one Episode does not create a stored profile for future Episodes.

## Keep voice selection separate from content

TTS voice names, display names and codes are technical configuration. Resolve
them through the supported catalog and put them only in the live tool's
dedicated voice fields, such as `speaker_1_voice_name` and
`speaker_2_voice_name` when exposed. Preserve the authorized voice selections;
removing an accidental host identity does not require changing the voices.

Never transfer those names into `model_steering`, Journey item instructions,
dialogue, titles, descriptions or education text as speaker identities. Even a
negative instruction quoting the voice codes can contaminate content prompts;
use a generic anonymity instruction instead. For example:

> Write a natural dialogue between two anonymous voices. Open with a welcome
> and the topic. Do not give the speakers names, biographies, job titles or
> recurring host identities. Speaker labels are structural and must not be
> spoken. TTS voice choices do not define who is speaking.

When the user explicitly supplies host identities, keep that intent separate
from voice selection in supported content fields. Do not invent a host-profile
field or API. A user-supplied host name may happen to match a voice name; record
that narrow exception from the user's request, not from the generated output.

## Review before dispatch and after generation

1. Before script generation or Journey item execution, inspect steering and
   Episode inputs. Remove unintended identity instructions through an authorized,
   supported edit and read them back. Do not send technical voice names into
   content steering to assign personalities.
2. Read the actual saved source script and each target-language script. Review
   the full text for host introductions, invented attributes and cross-episode
   continuity, not just occurrences of the selected voice names. Translation
   must preserve anonymity and structural labels without introducing identities.
3. Before each audio job, inspect the exact script/language revision it will
   consume. Check selected voice codes and display names using Unicode-aware,
   case-insensitive whole-name matching with punctuation/word boundaries, not
   naive substrings. For example, `Kore` inside Swedish `koreanska` is not a
   host-name match. Inspect context: a legitimate subject-matter mention is not
   an introduction. Ambiguous full-name matches remain a blocker until resolved;
   a user-authorized host-name exception applies only to that intended identity.
4. Keep source and translation checks ahead of audio dispatch. When a tool can
   generate translation and audio together, use a supported staged flow to read
   back the translated script before its audio job. For any automatic pipeline,
   proceed only if the live contract provides an equivalent pre-audio validation
   gate. If neither path exists, report the capability blocker before dispatch;
   do not launch a combined job and claim that a prompt instruction guarantees
   validation. Never guess a pause, review flag or audio-only endpoint.
5. After generation, read back saved scripts and media, and follow
   [generation verification](generation-verification.md). Verify every requested
   language and the audio job's actual input binding where exposed. Distinguish
   script review, successful job execution, script-to-audio linkage and listening
   to the audio. Text inspection alone does not prove what was heard.

A confirmed unintended host identity blocks the affected generation/publication
until corrected and verified. This is a plugin review rule, not a claim that the
backend already enforces it. Do not report a completed or synchronized Episode
while translations or audio still represent the old script.

## Correct existing Episodes without splitting script and audio

Before saving an active Episode's script or translation correction, verify that
the live tools provide a supported, authorized way to update the affected text,
regenerate its audio in every affected language, verify the results and publish
the replacement together. If generation is draft-only and no safe version/draft
flow is exposed, stop before the active text edit and present the proposed delta
and blocker. Do not invent `ensure_content_draft`, demote the Episode, clone or
reassign Journey links, replace media manually, or leave new text paired with
old audio as a workaround.

For an authorized draft correction, preserve unrelated content and voice choices,
read back steering and scripts, check translations again, and regenerate the
affected audio through supported operations. Apply the revision checks again if
text changes during the workflow. Do not activate the corrected Episode or its
Journey until the affected text/audio revisions are verified together. A repair
proposal does not authorize live changes to a reported customer incident.
