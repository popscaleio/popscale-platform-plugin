# Content Format Map

Use `content_generation_capabilities`, `content_detail`, and returned
`component_types` as the live contract. This map helps select the correct tool;
it does not authorize unsupported fields or operations.

| Root type | Granular components | Targeted generation subparts |
| --- | --- | --- |
| `roleplay` | customers; customer questions, objections, and decision rules; evaluation criteria | `setup`, `customers`, `description`, `education_text`, `coaching_focus`, `evaluation_criteria`, `evaluation_instructions` |
| `coaching_session` | Root fields only | `description`, `education_text`, `agent_prompt`, `evaluation_instructions` |
| `challenge` | Root fields only | `description`, `education_text`, `evaluation_prompt` |
| `episode` | Script variants; media rows are readable but not component-editable | `script`, `source_script_variant`, `description`, `education_text`, `source_audio` |
| `flashcard_deck` | Cards, translations, and deck languages | `cards`, `description` |
| `journey` | Sections and items | No targeted content regeneration; use Journey planning/generation tools for a new plan |

## Format-specific decisions

### Roleplays

- Use `roleplay_customer` for one persona,
  `roleplay_customer_question` for one question,
  `roleplay_customer_objection` for one objection,
  `roleplay_customer_decision_rule` for one decision rule, and
  `roleplay_evaluation_criterion` for one scoring criterion. Do not replace a
  customer's nested lists to make a one-row edit.
- Customer and evaluation-criterion changes may update calculated root totals;
  refresh the root revision before the next call.
- Generated customers are append-only when the live capabilities say
  `add_generated_customers`; do not interpret regeneration as replacement.

### Coaching sessions and challenges

- These formats expose focused root fields rather than nested component CRUD.
- Change only fields returned as editable. Model, voice, and department IDs
  must come from company-scoped references.

### Episodes

- Edit one language script through `episode_script_variant`. Treat
  `episode_media` rows as read-only evidence unless the user separately requests
  a supported upload-intent flow.
- Regenerating `script` also synchronizes the source script variant.
- Use `content_language_generate` for a target-language script and optional
  audio. `overwrite=true` replaces existing generated language output and needs
  explicit explanation before the call.

### Flashcards

- Use `flashcard_card` for one card, `flashcard_translation` for one card in one
  language, and `flashcard_language` for deck-language state. Source-card edits
  can mark translations stale; inspect freshness afterward.
- Generated cards are append-only when the live capability reports
  `append_generated_cards`. Do not promise replacement or a fixed final count.
- Use `content_language_generate` to generate or refresh a deck language.
  Refreshing existing translations requires `overwrite=true`.

### Existing journeys

- Use `journey_section` and `journey_item` to make granular edits to an already
  created Journey. Reordering replaces the complete section or item ordering
  within the selected bounded parent scope.
- Use `safe-journey-creation` for creating, validating, executing, or publishing
  a Journey plan. Existing-Journey component editing does not bypass that
  workflow's publication boundary.
