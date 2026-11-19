# Standalone Coaching and Flashcards

Create generated exercises with `generation_request_create`, inspect normalized
inputs, then `generation_request_start` on that persisted ID; no empty root first.
Manual drafts/regeneration are separate. Apply shared preflight/ProductAction rules.

## Request shape

Keep `request_type`, `input_payload`, stable `idempotency_key` at top level;
exercise inputs inside `input_payload`. Follow live schemas, not root `fields`
or Journey payloads.

| Type | Creation inputs |
| --- | --- |
| `coaching_session` | `name`, `coaching_session_type`, `session_description`, `coaching_context`, nonempty eligible `knowledge_asset_ids`; use structured `reference_facts` with `question`, `answer`, `max_points`, and requested `output_language` |
| `flashcard_deck` | `name`, company numeric `source_language`, `source_text` or eligible `knowledge_asset_ids`, explicit requested `number_of_cards`; `target_languages` are company language IDs |

Apply Coaching [question design](coaching-question-design.md), including numeric
`round_limit` and learner/assessment separation. Verify normalized count, language
and sources before start. Correct argument errors once; repeated opaque rejection
blocks that operation, not permission to guess another route.

## Follow the accepted job

Preserve request/command/idempotency identities across uncertainty, reloads and
turns. Inspect before authorized retry/cancellation; never replace unclear work.
`queued`/`running` is pending. `needs_review` is terminal generation awaiting review:
verify every requested step and saved target before reporting a delivered draft.
Skipped required parts, partial failure or missing targets prevent that claim.
Refresh before final pending reports; percentages prove no completion. Follow
[generation verification](generation-verification.md). At cutoff, state remaining
work and offer a saved-job check; promise no automatic continuation or raw IDs.
