---
name: route-popscale-requests
description: Route Popscale questions to the public read-only documentation MCP or the authenticated company-scoped product MCP without crossing their security boundary. Use when a user asks how Popscale works, requests public setup or product guidance, mixes documentation questions with customer data or actions, or is ambiguous about whether they want general information versus an authenticated Popscale operation.
---

# Route Popscale Requests

Keep public documentation retrieval separate from authenticated product data and
actions. This skill supplies routing policy only; it does not duplicate Popscale
documentation or MCP tool descriptions.

## Route the Request

1. Classify each part of the request:
   - General product concepts, public setup, public integration guidance, or
     documentation lookup: use `popscale-docs`.
   - Customer records, selected-company state, approved company knowledge, or
     any product action: use `popscale-platform` and its OAuth session.
2. For a broad public question, call `get_docs_overview`. For a focused question,
   call `search_docs`, then call `get_pages` only with canonical paths returned
   by the overview or search result.
3. Read the returned `status`, `owner`, and `last_reviewed` metadata before
   answering. Label `draft` content as draft and unverified, and label `review`
   content as under review. Do not present either as confirmed product behavior.
4. For an authenticated action, follow the relevant product workflow. Use
   `safe-journey-creation` for journey creation, execution, or publication. Use
   `safe-interview-administration` for Interview Study authoring, precise
   question edits, invitations, respondent links, run review, or analysis.
5. For a mixed request, answer the public portion from `popscale-docs`, clearly
   separate it from the authenticated portion, and obtain product state only
   from `popscale-platform`.

## Boundary Rules

- Never send customer identifiers, customer content, credentials, or OAuth
  material to `popscale-docs`.
- Never use `popscale-docs` for a write, as proof of authorization, or as the
  source of approved company knowledge for a product mutation.
- Never infer missing behavior from a draft, editorial TODO, empty result, or
  unavailable page. State the limitation and, when appropriate, verify actual
  customer state through the authenticated product server.
- Keep `safe-journey-creation` authoritative for its authenticated workflow;
  public documentation does not weaken its company, validation, or confirmation
  checks.
- Keep `safe-interview-administration` authoritative for Interview workflows;
  never send Study content, respondent data, invitation links, transcripts, or
  analyses to the public documentation server.
- If `popscale-docs` is unavailable, use the public artifacts at
  `https://docs.popscale.io/llms.txt`, `/llms-full.txt`, `/docs-index.json`, or a
  returned `/markdown/...` URL only for public reading. Do not fall back to the
  product MCP for public documentation search.

Read [evaluation-scenarios.md](references/evaluation-scenarios.md) when
validating routing behavior in a host.
