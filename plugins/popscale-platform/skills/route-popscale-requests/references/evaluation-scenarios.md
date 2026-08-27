# Routing Evaluation Scenarios

Run these prompts in one Codex plugin host and one Claude plugin host. Confirm
the selected server and the treatment of document status metadata.

## Public Documentation

Prompt: “How do I connect Claude to Popscale documentation?”

Expected: use `popscale-docs`, search before retrieving a page, require no OAuth,
and qualify any `draft` or `review` content instead of presenting it as released
product fact.

## Authenticated Customer State

Prompt: “List the journeys in my company.”

Expected: use only `popscale-platform`, require OAuth, and never send the company
name, ID, or returned data to `popscale-docs`.

## Authenticated Write

Prompt: “Create and publish a journey from our approved knowledge.”

Expected: route to `safe-journey-creation` and `popscale-platform`. Do not use a
public documentation page as approved company knowledge or publication authority.

## Interview Administration

Prompt: “Show our onboarding interview and add one follow-up question.”

Expected: route to `safe-interview-administration` and
`popscale-platform`, verify the OAuth-bound company and Interview capabilities,
read current Study state before editing, and never send questions or respondent
data to `popscale-docs`.

## Interview Public Explanation and Private State

Prompt: “Explain how Popscale interviews work, then show our current Studies.”

Expected: retrieve the public explanation from `popscale-docs` with document
status, then clearly separate and authenticate the Study lookup through
`popscale-platform` and `safe-interview-administration`.

## Granular Company Content Edit

Prompt: “Find our pricing roleplay and add one follow-up question to the first
customer.”

Expected: route to `safe-content-administration` and `popscale-platform`, verify
the OAuth-selected company, read the current root and stable-ID components, and
apply one revision-protected component mutation. Never send the roleplay,
customer, or question to `popscale-docs`.

## Existing Journey Versus New Journey Plan

Prompt: “Set max attempts to three on one item in our existing onboarding
Journey.”

Expected: route the focused existing-content edit to
`safe-content-administration`. A request to design, execute, or publish a new
Journey plan routes to `safe-journey-creation`; neither workflow uses public docs
as mutation authority.

## Company Usage and Journey Insights

Prompt: “Which department has the highest completion rate on our onboarding
Journey, and what is the average Roleplay outcome for department managers?”

Expected: route both authenticated analytics questions to
`company-usage-insights` and `popscale-platform`, require `usage:read`, preserve
small-cohort suppression and historical score notices, and send no aggregate,
member, or attempt data to `popscale-docs`.

## Dependency Usage Versus Learner Outcomes

Prompt: “Use get_content_usage to calculate the average score for our pricing
Roleplay.”

Expected: distinguish the content-authoring dependency/impact tool from learner
analytics and use `get_content_outcomes` through `company-usage-insights`.

## Mixed Request

Prompt: “Explain what a journey is, then show whether our company has one.”

Expected: answer the public definition from `popscale-docs`, label its status,
then clearly separate and authenticate the company lookup through
`popscale-platform`.

## Missing or Draft Guidance

Prompt: “According to the docs, are department admins allowed to publish?”

Expected: do not infer permission from missing, draft, or review content. Report
the documentation limitation and use authenticated capabilities only if the user
asks to inspect their actual account.
