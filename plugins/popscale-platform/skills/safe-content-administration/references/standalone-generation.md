# Standalone Coaching and Flashcards

For a new generated exercise, use `generation_request_create`, read normalized
inputs, then `generation_request_start` on its persisted ID. Do not first create
an empty root. Manual draft authoring and existing-root regeneration are separate
operations. Apply the shared preflight and product-action approval contract.

## Request shape

Keep `request_type`, `input_payload` and stable `idempotency_key` at the top
level; exercise inputs belong inside `input_payload`. Follow live schemas and
validation, not root `fields` or Journey item payloads.

| Type | Creation inputs |
| --- | --- |
| `coaching_session` | `name`, `coaching_session_type`, `session_description`, `coaching_context`, nonempty eligible `knowledge_asset_ids`; use structured `reference_facts` with `question`, `answer`, `max_points`, and requested `output_language` |
| `flashcard_deck` | `name`, company numeric `source_language`, `source_text` or eligible `knowledge_asset_ids`, explicit requested `number_of_cards`; `target_languages` are company language IDs |

Apply Coaching [question design](coaching-question-design.md), keeping assessment
answers out of learner-visible descriptions. Verify normalized count, language
and sources before starting. Correct identified argument errors once; repeated
opaque rejection is a contract blocker, not permission to guess another route.

## Follow the accepted job

Preserve request, command and idempotency identities across uncertain responses,
reloads and turns. Read the job before any separately authorized retry/cancellation;
unclear progress never authorizes replacement. `queued`/`running` means work remains. `needs_review`
is terminal generation awaiting review: verify every requested step and saved
target, then report a delivered draft with review outstanding. A skipped required
part, partial failure or missing target prevents that claim. Refresh persisted
state before a final pending claim; progress percentages alone prove nothing.
Use [generation verification](generation-verification.md) for artifact evidence.
If the host turn ends first, say what remains and offer to check the saved job
again; do not promise automatic continuation or expose raw job IDs.
