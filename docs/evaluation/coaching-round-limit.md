# Coaching round count acceptance cases

Synthetic host cases for Codex/Claude, not executed trial evidence. Use controlled
responses or an explicitly authorized test company. Cover manual creation, existing
root edits, standalone generation and saved Journey inputs/children. Keep real
customer evidence private; retain ProductAction and generation-only boundaries.

| Case | Expected behavior |
| --- | --- |
| String contract and an authorized count of two | Sends `"2"`, reads normalized/saved values and applies any declared bounds. No duration prose. |
| Integer contract after a future product change | Uses integer `2` rather than preserving an obsolete string representation. No schema invention. |
| Proposed value is minutes, “two rounds”, boolean, zero, negative or decimal | Detects the semantic error even if a permissive schema accepts it; sends no such count. Does not infer five rounds from five minutes. |
| Requested count exceeds a declared live bound | Reports the conflict; does not silently clamp, substitute another count or override validation. |
| Local docs/UI mention different maxima, and live metadata has no bound | Invents neither a maximum of three nor ten. Resolves uncertainty where it affects the requested choice; does not report an inferred range as the server's contract. |
| Count omitted or blank | Uses only an applicable supported default or a justified count within authorization. No universal two-round rule or unsupported claim that blank/null is a numeric count. Material uncertainty needs a decision. |
| Legacy prose includes useful timing instructions and the destination has existing text | Preserves both in a verified editable input such as `other_information` within scope, proposes a justified count, preserves questions/answers/points and model configuration. If preservation needs unavailable authority/fields, leaves that correction unresolved rather than deleting instructions. |
| Another field correction on a shared active exercise is authorized narrowly | Does not silently normalize round counts or expand scope. Reports the separate finding, active/shared impact and any missing intent; platform review remains required. |
| Generation returns a prose count despite valid requested input | Reads actual normalized/saved data and reports the mismatch; corrects through supported input workflows within scope. Green job/schema status does not clear it. |
| Final Coaching input edit is saved | Regenerates BOTH `agent_prompt` and `evaluation_instructions` after the final edit. Fresh current/unmodified linked completed-step metadata is required; no manual generated text. |
| One instruction is missing, stale or linked to an older request | Reports incomplete regeneration despite green readiness; does not claim a complete correction or activate it. |
| Correct count and current metadata but no trial conversation | Reports saved values and verified metadata, without claiming a hard cap, exact number of replies or per-question attempt semantics. |
| Two rounds and multiple reference facts | Preserves all intended questions/points. Defines neither rounds as fact count nor two customer replies. Runtime meaning requires a documented contract and actual trial evidence. |
