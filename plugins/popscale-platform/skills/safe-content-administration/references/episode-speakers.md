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

Use anonymous voices by default. For a conversational Episode without a more
specific opening brief, give the listener a relevant reason to engage with the
topic through an observation, situation or question. A brief welcome may lead
into that opening. Adapt the structure to the requested purpose and supported
format. Do not invent host names, job titles, biographies, personal histories
or recurring podcast personas. Warmth, differing viewpoints and a conversational
tone do not require personal identities.

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
use the positive conversation guidance below in Script input.

When the user explicitly supplies host identities, keep that intent separate
from voice selection in Script input. Do not invent a host-profile
field or API. A user-supplied host name may happen to match a voice name; record
that narrow exception from the user's request, not from the generated output.

## Write positive Script input instructions

Use general principles that work across companies, subjects and Episode
purposes. Adapt them to the supplied brief, approved content, audience, source
language, company Tone of Voice, duration and supported format. Keep specific
industries, customer situations, learning promises and calls to action tied to
the actual request and sources. Preserve existing relevant instructions and
explicit user choices; apply defaults only where the brief leaves room.

Describe the desired result in positive language. Keep technical voice/output
boundaries in this agent workflow. The following Swedish guidance illustrates
an adaptable Script input brief, not a fixed script or mandatory structure;
write the actual brief in the configured source language:

> Utforma avsnittet utifrån dess syfte, innehåll och målgrupp. Anpassa språk,
> ton, struktur och tempo till företagets Tone of Voice och avsnittets sammanhang.
>
> Använd anonyma röster och låt innehållet stå i centrum. Ge lyssnaren en tydlig
> ingång till ämnet genom en relevant observation, situation eller fråga som
> väcker nyfikenhet och passar avsnittets syfte och format.
>
> I samtal med två röster, låt dem bidra på olika sätt. Den ena kan ställa en
> fråga eller pröva ett perspektiv, medan den andra förklarar eller nyanserar.
> Låt funktionerna växla naturligt när det för resonemanget framåt.
>
> Ge tankar och resonemang utrymme att utvecklas sammanhängande. I samtal,
> låt rösterna komplettera varandra och ta vid när de tillför något relevant,
> till exempel en fråga, ett perspektiv eller en fördjupning. Anpassa replikernas
> längd och talarbyten efter innehållet och det önskade tempot. Låt reaktioner
> anknyta till det som just sagts och utveckla dess betydelse för lyssnaren.
>
> Förankra faktapåståenden i det godkända underlaget och tydliggör vad som gäller
> under särskilda förutsättningar. Använd relevanta förklaringar, exempel eller
> reflektioner för att göra innehållet begripligt och meningsfullt.
>
> Avrunda med en insikt, reflektion eller tillämpning som passar avsnittets syfte
> och ger lyssnaren något värdefullt att ta med sig.

For a conversational opening, “Hej och välkommen! I dag ska vi prata om
[ämnet]” is one possible welcome, not required wording or a complete opening
brief: connect it to why this subject matters to the listener. A summary,
reflection or practical next step can suit some endings; choose one only when
it serves the brief. Questions, examples and everyday situations are optional
ways to develop the subject, not required ingredients in every Episode.

Apply speaker-change guidance within the supported format actually selected;
it does not introduce a new speaker-count option. Aim for developed thoughts
and meaningful speaker changes without imposing a sentence quota, a switch
after each point, or the same calm or energetic pace on every Episode.

## Conversational Episode quality

For a two-speaker conversational Episode, tailor Script input to the intended
listening experience, not only topic and tone. Words such as “warm, clear and
calm” need concrete guidance on the opening, voice contributions and development.
Apply these principles to the brief without requiring one dramaturgy:

- Give the opening relevance or curiosity through an appropriate observation,
  question or situation. A restrained factual introduction can serve a policy
  update; engagement does not require a dramatic hook or a customer case.
- Give the anonymous voices complementary conversational functions: asking,
  testing an idea, explaining, qualifying or applying it. Functions may alternate;
  they are not host identities, invented expertise or permanent personality roles.
  Different contributions do not require fabricated disagreement.
- Let each contribution develop the subject, connect ideas or clarify why a fact
  matters. Choose examples, reflection or application where they help. A factual
  list can be useful, but should serve understanding rather than substitute for
  the requested conversation.
- Use natural reactions and varied turn lengths while giving thoughts room to
  develop. Meaningful speaker changes matter more than frequency. Respect a
  request for fewer changes, a calm reflection or a concise formal style.
- Make transitions and endings add a connection, synthesis or useful perspective.
  Repeated agreement fillers or recaps are review signals when they dominate;
  an occasional “exactly” or a useful summary is not a defect.
- Match energy to the audience and Tone of Voice. Ground claims in approved
  sources and bound facts that vary with time, location or agreement. Illustrative
  situations must remain clearly hypothetical, without invented company claims.

Keep these as positive instructions in the actual Script input. Preserve explicit
style choices and supported formats; do not impose rapid short turns, a fixed
questioner/expert pairing, high energy, a sales scenario or a recap on all Episodes.
For other supported formats, apply only the relevant principles.

### Review the saved script

Read the complete saved source script against the brief, and review translated
scripts where available. Use these questions as semantic checks, not keyword
counts or a guarantee of audience enjoyment:

| Check | What to assess |
| --- | --- |
| Opening | Does the opening give this audience a reason to follow the subject, in the requested style? |
| Voice contributions | Do the voices add complementary functions or perspectives without invented identities? |
| Development | Do facts build understanding through suitable explanation, examples or reflection? |
| Rhythm | Do turn lengths and speaker changes support coherent thoughts and the requested pace? |
| Relevance and repetition | Do sections and the ending add value, with reactions that do more than repeat agreement? |
| Grounding | Are claims supported and variable information appropriately bounded? |
| Anonymity | Are speaker identities and technical voice configuration kept separate, subject to explicit user-supplied identities? |

Report material mismatches with concrete evidence from the saved text. Distinguish
script quality review from successful jobs, publish readiness and actual listening.
Text review cannot establish prosody, pronunciation, audio pace or listener response.

## Generate and verify without editing outputs

1. Inspect the current Script input and selected TTS configuration. Put the
   anonymity and applicable listening-experience guidance in `model_steering`
   through an authorized input edit, preserving other instructions. Remove
   accidental voice-as-person directives from that input and read the saved
   value back before regeneration.
2. Prefer generating and reviewing the source script before audio and target
   languages when live capabilities expose a complete, authorized staged path
   for this target and status. Inspect `content_generation_capabilities` and the
   returned subpart/dependency contract. For an eligible draft, that can mean
   platform generation of `script` with its `source_script_variant`, followed
   by saved-script review, then `source_audio` and the supported language flow.
   Use only exposed subparts and verify the current source variant before audio.
   Keep the review bound to that saved version; subsequent input or script
   generation changes require a fresh review before dependent dispatch.
   Review target scripts before their audio when that separation is also supported.
   A granular draft regeneration tool does not imply that new Episode or Journey
   creation can pause between stages; assess the actual operation being requested.
   Combined generation remains valid when staging is unavailable or the user's
   brief prioritizes speed. Review the saved outputs afterwards and describe any
   unreviewed audio generation honestly. Do not add an endpoint, pause gate or
   extra user approval merely for text review; existing preflight, scope and
   generation authorization requirements still apply.
3. Read actual saved source and target-language scripts without changing them.
   Review full text for invented host introductions, attributes and continuity,
   not just selected TTS names. Structural speaker labels and legitimate names
   in the subject matter are not host identities. If checking voice-name matches,
   use Unicode-aware case-insensitive whole-name matching, not substrings such
   as `Kore` inside `koreanska`. Resolve ambiguous matches in context.
   Apply the saved-script quality checks above in the requested style; good
   steering and job completion alone do not prove that the output follows it.
4. For a material quality or input mismatch, explain it, make a focused positive
   Script input correction when authorized, and regenerate through the platform.
   Hold any not-yet-dispatched audio/language work that would reuse the faulty
   source until the correction is reviewed. If a combined job already generated
   audio, report that fact and establish an authorized way to regenerate affected
   outputs together. Never patch, merge turns or translate scripts manually.
   Keep correction to one focused regeneration-and-review attempt within the
   authorized scope and cost. If it still misses the brief, present the remaining
   issue and proposed next step before further paid retries. A quality review
   neither authorizes generation nor justifies endless polishing.
   Do not claim the requested quality correction complete while a material
   mismatch remains; retain the separate technical job status and evidence.
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
