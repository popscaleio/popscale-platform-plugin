# User-facing content names

Refer to exercises, Journeys and Studies by their current app-visible name or
title, as returned by the authenticated Product MCP. Use this convention in
progress updates, search results, review tables, approval questions, outcome
reports and error explanations.

- Lead with the exercise name. Add the format and verified Journey title when
  they help the user locate it: `Roleplay “Hantera invändningar” i Journey
  “Tryggare kundmöten”`. These names are illustrative, not product data.
- Use the returned title as written, even when answering in another language.
  This presentation rule does not rename stored content.
- Add a Journey relationship only when current product results establish it.
  An exercise can be standalone or reused in several Journeys; describe the
  relevant verified relationship without implying a unique owner. If membership
  is unknown, use the exercise name alone.
- For duplicate names, use available visible context such as Journey, section,
  format, language or draft/published status. Present numbered choices when
  helpful, retaining each choice's exact server-returned ID internally. Choice
  numbers are local to that list. Resolve ambiguity before a target-specific
  action; a repeated title or list position is not a stable tool identifier.
- If a result contains only an ID, first reuse a verified name already mapped
  to that target in the current context, or read its detail through an available,
  authorized product tool. If the name remains unavailable, explain that plainly
  and use the available format/context. Ask for a visible distinguishing detail
  when needed; keep unresolved targets unresolved. Respect existing scopes,
  pagination and privacy limits when resolving names.
- Keep object/component IDs, request/step IDs and revision tokens in tool calls
  and internal evidence. Preserve exact ID mappings, concurrency checks and
  generation provenance. The user-facing summary describes the named content,
  outcome and any unresolved issue in plain language.
- Include technical identifiers when the user explicitly requests IDs or a
  technical diagnostic/audit export, within existing access and privacy limits.
  Label them alongside the known content names. For navigation, use an app link
  returned by the product tools when available; keep its destination unchanged.

For example, a verified result can be summarized as:
“Jag har uppdaterat ‘Hantera invändningar’ i Journey ‘Tryggare kundmöten’.
Övningen är fortfarande ett utkast.” Preserve any generation or publication
warnings that apply to the operation.

Read [content-names-scenarios.md](content-names-scenarios.md) when validating
these rules in a host.
