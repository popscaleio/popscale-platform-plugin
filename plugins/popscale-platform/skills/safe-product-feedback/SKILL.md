---
name: safe-product-feedback
description: Submit Popscale bugs, ideas and improvements, read own feedback, or review platform feedback with explicit authority.
---

# Safe Product Feedback

Use authenticated `popscale-platform`; check `current_user`, `capabilities` and company. Never send context to Docs or evade denial; missing tools do not mean an empty queue. Read [ProductAction](../route-popscale-requests/references/product-actions.md) before writes, [platform review](references/platform-review.md) for privileged work and [navigation/activity](../route-popscale-requests/references/navigation-and-activity.md) for destinations/progress.

Classify `general`, `bug`, `improvement` or `idea`. Get title (≤200 characters), text (≤5,000) and attempted/expected/observed bug behavior when known. Clarify vague reports. `submit_feedback` requires optional `admin:write`, `kind`, `title`, `text`, `share_context:false` and stable UUID `command_id`. Server derives company/actor/source/status and first-party conversation IDs. On uncertain response inspect `product_action_get` and retry exact arguments/ID; never duplicate.

External MCP may supply agreed `external_excerpt` (≤4,000 characters) and opaque `client_reference` (≤500). Nonempty excerpts require `share_context:true` and authenticated approval of the preview showing exact excerpt/reference and sharing scope. Remove unrelated data/secrets; never harvest chats or pass first-party IDs. First-party context also needs consent. Backend cannot fetch external transcripts.

Execute review previews only after server-confirmed human approval; verbal yes is insufficient. Say submitted only when effect returns `feedback` and `created`, with ID/status. Preview or completed tool call is insufficient.

Optional `admin:read`: `list_feedback`, `get_feedback`, `feedback_statistics` for this actor/company. Lists filter `kind`/`status`, `limit` ≤100, `offset` ≤10,000 and return `results`/`next_offset`; detail uses `feedback_id` without context/reviewer notes. Statistics are caller's current up/down ratings. Frontend owns thumbs/follow-up; no external-host rating tool exists.
