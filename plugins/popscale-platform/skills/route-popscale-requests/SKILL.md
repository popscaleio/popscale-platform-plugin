---
name: route-popscale-requests
description: Route Popscale questions to the public read-only documentation MCP or the authenticated company-scoped product MCP without crossing their security boundary. Use when a user asks how Popscale works, requests public setup or product guidance, mixes documentation questions with customer data or actions, or is ambiguous about whether they want general information versus an authenticated Popscale operation.
---

# Route Popscale Requests

Keep public documentation retrieval separate from authenticated product data and
actions. This skill supplies routing policy only; it does not duplicate Popscale
documentation or MCP tool descriptions.

Read the shared [product action contract](references/product-actions.md) before any
mutation. Stable command identity and server-side human approval apply alongside
the workflow below; confirmation booleans alone do not approve effects.

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
   question edits, invitations, respondent links, run review, or analysis. Use
   `safe-content-administration` to find, create, inspect, or granularly edit
   existing roleplays, coaching sessions, challenges, episodes, flashcards, or
   Journey sections/items, and for their supported regeneration, language, or
   activation workflows. Use `company-usage-insights` for company-scoped
   Journey participation, completion, mastery, content outcomes, and bounded
   member or attempt drilldown.
5. Before authoring new or rewritten input for an exercise, a Knowledge
   document, a Journey brief or a Study, fetch the matching writing guide from
   `popscale-docs` with `get_pages` and shape the input by it:
   `/content/writing-good-input/` for any exercise,
   `/content/questions-that-work/` for questions and reference answers,
   `/content/what-can-be-assessed/` for evaluation criteria,
   `/content/one-situation-many-customers/` for Roleplays,
   `/knowledge/write-a-knowledge-document/` for Knowledge,
   `/journeys/plan/` for a Journey brief, `/studies/` for a Study. The guides
   describe what good input contains, not how the platform processes it. Ask
   the user for what the guide says is missing before creating anything. Never
   put company facts into the docs query; fetch the guide, then author on the
   product side.
6. For a mixed request, answer the public portion from `popscale-docs`, clearly
   separate it from the authenticated portion, and obtain product state only
   from `popscale-platform`.
7. If `current_user` returns a different company than the user intended, stop
   product reads and writes and follow the company-switch boundary below. Do not
   route the mismatch through public Docs or treat reconnect as the default.

## Discovery and Polling Discipline

- Search content with a short keyword or a tag, not the full title. If nothing
  matches, try one variant, then list with a status or type filter. Do not
  repeat the same search.
- A tool that `capabilities` marks `available: false` is not callable. Say
  which feature or scope is missing, once. Do not search for the tool again,
  substitute a generic tool, or drive a browser to work around it.
- While a generation request is running, poll with a growing interval and
  report only when the status changes. Do not narrate every read.

## Company Switch Boundary

1. Use the grant ID from the latest `current_user` result. Explain the current
   company and ask for explicit confirmation immediately before creating a
   short-lived switch link.
2. Only after confirmation, call `request_company_switch` with
   `current_grant_id` and `confirm_switch=true`. Never pass a target company
   name, company ID, or membership ID to the tool.
3. Present the returned `switch_url`. The user signs in to the same Popscale
   account, selects the intended membership in the authenticated browser, and
   confirms there. Creating the link alone does not switch the company.
4. After browser confirmation, call `current_user` again through the same MCP
   connection and verify the returned company before resuming product work.
5. If the result has `replay_ignored=true`, refresh `current_user`; the current
   connection remains active. If a link expired or was already used, obtain new
   confirmation before creating another. Do not claim reauthorization, token
   rotation, or grant revocation when the server returns
   `reauthentication_required=false`.

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
- Keep `safe-content-administration` authoritative for company content
  authoring. Use `safe-journey-creation` for a new Journey plan or its
  execution/publication, but use the content workflow for a focused edit to an
  already created Journey section or item.
- Questions about whether an artifact was generated, edited or is current are
  private product-state reads. Route them to `safe-content-administration` and
  its generation-verification workflow; public docs are not provenance evidence.
- Keep `company-usage-insights` authoritative for private usage analytics.
  `get_content_usage` is a dependency/impact check before content mutation;
  learner outcomes and attempts use the dedicated usage-insights workflow.
  Never send aggregates, member identities, or attempt data to `popscale-docs`.
- Keep company switching on `popscale-platform`. The target membership is chosen
  only in Popscale's authenticated browser flow; prompt-supplied target
  identifiers are never tool inputs or authorization.
- If `popscale-docs` is unavailable, use the public artifacts at
  `https://docs.popscale.io/llms.txt`, `/llms-full.txt`, `/docs-index.json`, or a
  returned `/markdown/...` URL only for public reading. Do not fall back to the
  product MCP for public documentation search.

Read [evaluation-scenarios.md](references/evaluation-scenarios.md) when
validating routing behavior in a host.
