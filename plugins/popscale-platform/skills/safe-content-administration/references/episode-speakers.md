# Episode Speakers and TTS Voices

Apply this policy to standalone Episodes and Episode items in Journeys, including
source inputs, scripts, translations, audio generation and corrections. Keep the
[company asset preflight](company-asset-preflight.md) and live authorization
contract in force; this policy does not add a tool or permission.

## Author inputs; the platform owns scripts

**Never manually author, patch, clear or translate generated Episode scripts.**
This includes root `script` and source/translated variant `script_text`, through
root creation, `content_update`, component creation/update or any other route.
The rule applies to drafts and active content even when a tool exposes writable
fields or the user asks for a small textual correction. Read scripts for
verification; corrections belong in inputs followed by platform regeneration.

The UI's **Script input** maps to `model_steering` in the current contract. Set
speaker anonymity, conversational style, opening/ending and pacing there. Use
`content` for the subject matter when that change is requested. Preserve unrelated
inputs and resolve exact fields through the live contract; do not invent a
`script_input` API parameter or hide a replacement transcript in an input field.
For Journey items, set the corresponding supported Episode input before execution.
Read saved inputs back after authorized edits, then let the platform generate
source script, translations and audio through its supported workflow.

## Anonymous conversation is the default

Use anonymous conversational voices. Start with a welcome and the topic, then
move into a natural exchange. Do not invent host names, job titles, biographies,
personal histories or recurring podcast personas. Warmth, differing viewpoints
and a conversational tone do not require personal identities.

The platform-generated result should have this kind of opening; this is an
illustration of tone, not text for the agent to write into a script field:

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
use a generic anonymity instruction in Script input instead. For example:

> Write a natural dialogue between two anonymous voices. Open with a welcome
> and the topic. Do not give the speakers names, biographies, job titles or
> recurring host identities. Speaker labels are structural and must not be
> spoken. TTS voice choices do not define who is speaking.

When the user explicitly supplies host identities, keep that intent separate
from voice selection in Script input. Do not invent a host-profile
field or API. A user-supplied host name may happen to match a voice name; record
that narrow exception from the user's request, not from the generated output.

## Generate and verify without editing outputs

1. Inspect the current Script input and selected TTS configuration. Put the
   anonymity requirements in `model_steering` through an authorized input edit,
   preserving other instructions. Remove accidental voice-as-person directives
   from that input and read the saved value back before regeneration.
2. Use the supported platform pipeline for script generation, translation and
   audio. Combined operations are allowed by this policy; do not require a new
   pause/review endpoint or an intermediate manual script-edit step. Existing
   company-asset preflight, generation capability and authorization gates still
   apply. Passing Script input rules is not proof that the model followed them.
3. Read actual saved source and target-language scripts without changing them.
   Review full text for invented host introductions, attributes and continuity,
   not just selected TTS names. Structural speaker labels and legitimate names
   in the subject matter are not host identities. If checking voice-name matches,
   use Unicode-aware case-insensitive whole-name matching, not substrings such
   as `Kore` inside `koreanska`. Resolve ambiguous matches in context.
4. If output violates the input, report the mismatch and adjust Script input
   when appropriate, then use authorized platform regeneration for affected
   scripts/translations/audio. Do not replace introductions by hand, translate
   output yourself, or repeatedly retry without a bounded supported recovery.
   If a separate audio job has not started and its script is known to be faulty,
   resolve the generation failure before dispatching that job.
5. Follow [generation verification](generation-verification.md) for every
   requested language. Distinguish input read-back, generated script review,
   successful audio jobs, script-to-audio linkage and actual listening. Do not
   claim audio was heard or matched the current script based only on text reads.

An unintended host identity or a manually changed script remains an unresolved
output issue. Do not claim the requested correction complete or activate the
corrected Episode/Journey while it persists. If generation or verification is
unavailable, report the blocker; it never authorizes direct script edits.
Read-only inspection does not authorize regeneration or publication.

## Correct existing Episodes through inputs and regeneration

Before changing an active Episode's inputs for a correction, establish a
supported, authorized regeneration/publication workflow that keeps affected
scripts, translations and audio consistent. If generation is draft-only and no
safe version/draft flow is exposed, stop before the input change and present the
proposed Script input delta and blocker. Never invent `ensure_content_draft`,
demote the Episode, clone/reassign Journey links or replace media manually.

For an authorized draft correction, change only the necessary inputs, preserve
voice choices and unrelated settings, then let the platform regenerate affected
outputs. Do not promise unchanged wording in generated scripts: an input change
can cause the platform to rewrite more than the unwanted introduction. Recheck
saved results and their revisions, and do not publish a replacement with old or
unverified audio. A repair proposal does not authorize live customer changes.
