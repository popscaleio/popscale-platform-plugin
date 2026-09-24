# Content naming acceptance scenarios

Use synthetic product results in host evaluations. Inspect both user-facing
text and tool arguments: readable names must retain precise internal targeting.
These scenarios are manual checks, not evidence of completed live host testing.

| Scenario | Expected behavior |
| --- | --- |
| A named exercise has a verified Journey relationship | Names the exercise and, when useful, the Journey in updates, confirmation and result; tool calls retain the returned IDs. |
| The same title occurs in two Journeys | Offers the two Journey names as context; after selection, acts on the matching internal ID. |
| Same title and Journey, different language or section | Uses those visible distinctions. If still ambiguous, asks for a distinguishing detail and makes no target-specific write. |
| A numbered list is followed by a refreshed result in a different order | Preserves the selected object's ID mapping; does not interpret the old choice using the new list order. |
| An exercise is reused in several Journeys | Describes verified relevant memberships without inventing a single owning Journey. |
| Journey membership is missing or truncated | Uses the known exercise title; preserves any impact-review blocker caused by incomplete dependencies. |
| Results contain an ID but no title | Resolves through permitted current context/detail, or explains that the name is unavailable; does not invent a title or require a hidden ID from the user. |
| Analytics target is known but discovery scope is absent | Uses available names/context, retains scope limits, and reports the requested aggregate without broadening access solely for presentation. |
| Analytics target is unresolved and discovery scope is absent | Offers scoped reauthorization or a supported app-link lookup; does not guess the target or ask the user to find an invisible ID. |
| Generation is partly complete | Names each affected exercise and output, preserves failure/freshness information and internal request evidence; does not dump request IDs into the routine summary. |
| User explicitly requests a technical audit with IDs | Includes permitted IDs alongside known names and verified evidence; privacy restrictions still apply. |
| A Study is renamed before the next confirmation | Uses its current returned title while retaining the exact Study target and current edit token. |
