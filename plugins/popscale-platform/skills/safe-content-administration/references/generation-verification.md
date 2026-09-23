# Verify Generation Before Reporting

Use this workflow after generation, after editing generated content, and before
claiming existing content is platform-generated. It also applies to each content
root created or reused by a Journey. This reference defines reporting rules, not
a new MCP tool or authority to regenerate, overwrite, or publish.

## Read the evidence

1. Keep the intended OAuth-selected company and requested output scope explicit.
   Record every requested root, artifact and language before checking results;
   do not shrink the scope to only the rows that succeeded. Treat tool errors,
   `isError`, missing scopes and incomplete reads as unverified work.
2. Read `content_detail` and the relevant components after the operation. Check
   the returned root, revision, actual saved fields, language and stable IDs.
   Do not treat an accepted request or populated field as proof of generation.
3. Read `get_content_freshness` for that same root. Preserve `available`, each
   artifact's server-returned `key`, status and execution overlay. An empty or
   unavailable artifact list means no evidence, not that everything is current.
4. For every registered artifact, read the linked request with
   `generation_request_detail` and its complete `generation_request_steps`.
   Verify `generation_request_id`, `generation_step_id`, `generated_at`, the
   request's target, and the exact step ID with `status=completed`. A skipped
   step does not prove generation. Use the server's links, not name similarity:
   an artifact named `cards` can link to a step named `initial_cards`.
5. Also check every request started for the current operation, even if freshness
   still references an older successful request. Show overall request status
   separately from individual successful parts. A `partial`, failed, cancelled,
   running or reviewable request must never produce a blanket success claim.
6. If content changes during these reads, refresh and reconcile the evidence.
   Report verification at the observed revision, not as a permanent guarantee.

Readiness measures publicability; freshness measures changes relative to a
baseline; provenance measures origin. **Never infer platform generation from
green readiness, a filled field, `current`, or a timestamp alone.**

## Interpret each part

| Evidence | Permitted report |
| --- | --- |
| Bound completed step, generation timestamp, unchanged output | Platform-generated; report freshness separately |
| Same bound evidence plus `output_edited`, `source_changed_and_output_edited` or `output_modified=true` | Historical generation followed by an edit; generation-only outputs additionally have a workflow failure and cannot be called synchronized |
| `source_changed` with bound generation evidence | Platform-generated from an older source; not up to date |
| `legacy_unknown` | Origin unknown; never call it generated or directly authored |
| `not_generated` | Not generated according to the available artifact evidence |
| Missing linkage, unreadable request, missing artifact or unknown status | Generation not verified; state the missing evidence |
| `execution_status=generating` or `generation_failed` | New attempt running or failed; do not reuse the old baseline as proof of the new attempt |

Execution overlays can replace request/step IDs while retaining an older
`generated_at` and output baseline. Resolve the current operation before making
a generation claim for that artifact. A manually entered value is only known to
be directly authored when a confirmed write and readback/history prove it;
missing generation IDs do not establish that origin.

Manual override applies only to fields explicitly editable under both the live
contract and the plugin's [format policy](content-format-map.md). It never
applies to Roleplay or Coaching `evaluation_instructions`, Coaching
`agent_prompt`, or Challenge `evaluation_prompt`, even on an explicit request
to rewrite, correct, translate, or clear them. These are generation-only outputs.
For other permitted, explicitly requested manual edits, explain the provenance
consequence, use only confirmation fields exposed by the live schema, and read
back the result and freshness.

`source_changed_and_output_edited` on a generation-only output is a workflow
failure, not successful synchronization. The same stop applies to `output_edited`
or `output_modified=true`, including when linkage is missing or a generation
attempt is still running. Historical provenance may remain valid; it does not
verify the current edited text. Report the failure separately, do not activate
the affected root or its Journey, and follow the supported platform regeneration
flow when authorized. Do not regenerate unknown or edited content merely to
make a read-only report green. If draft creation or regeneration is unavailable,
leave the blocker explicit and never repair the text manually.

## Native languages and media

Episode and Flashcard translation rows can expose `current` and `generated_at`
without request/step links. Episode audio may have no freshness row. Do not
invent missing IDs or infer media provenance from a filename, timestamp or URL.
The step-status tool does not promise output snapshots, media IDs or hashes.

For an observed language/audio operation, verify the request's target and
language, the appropriate completed step, and the actual variant/media via
component reads. Report the narrow evidence: “The language generation step
completed and the corresponding output was read back.” If the current file or
translation cannot be bound to that generation, explicitly say its exact origin
is not verified. Never claim it is unchanged or matches the current script
without server evidence. Missing native provenance does not authorize a rebuild.
For Episode identity corrections, the [speaker policy](episode-speakers.md)
additionally requires verified replacement of affected scripts and audio before
publication. For other work, missing native provenance alone does not prevent
separately authorized publication that passes server readiness and applicable
plugin checks. Script review is not a claim that the audio was listened to.

## Local evidence check

Hosts with local Python can run the packaged, standard-library-only checker:

```text
python3 <skill-directory>/scripts/verify_generation_evidence.py < evidence.json
```

Use host-local private temporary storage or stdin; never commit or upload real
evidence to a repository, public Docs, or another service. The checker makes no
network calls or writes and emits no source content, names or error payloads.

The input is a local envelope, not an MCP request:

- `root`: the intended `content_type` and `object_id` from verified discovery.
- `requested_artifacts`: every artifact key in the agreed scope. Retain an
  unavailable requested part, such as audio, so it cannot disappear from the
  report. These are artifact keys, not assumed tool arguments.
- `freshness`: the successful data object from `get_content_freshness`.
- `requests`: data objects from `generation_request_detail` for both linked
  baselines and all requests in the current operation for this root.
- `step_results`: matching data objects from `generation_request_steps`, each
  containing its original `request_id` and complete `steps` list.
- For a Coaching input update, `coaching_inputs_changed: true` and
  `coaching_regeneration_request_ids`: the server-returned IDs of regeneration
  requests started after the final input edits. These are local workflow context,
  not MCP fields. The checker includes both instruction artifacts in scope and
  requires both to link to these new requests. Empty IDs mean regeneration is
  pending/blocked, not permission to reuse old successful evidence.

Copy evidence without inventing or changing values. Keep root/availability,
artifact status/IDs/timestamp/modified flag, request ID/status/target_object_id/
step_count, and step ID/status. Unneeded names, content and error messages may be
omitted. Check outer transport errors before unwrapping the successful data.

This checker assumes authentic, fresh reads from one selected company; it cannot
authenticate supplied JSON, discover omitted work, or infer target type from
numeric IDs. Verify company, target type and scope in the workflow first. It
supports linked registered artifacts; native rows without linkage stay
unverified. Exit zero means a report was produced, not that verification passed.
Read `can_report_requested_generation_complete` and every artifact row. A true
value covers only the supplied scope, not a whole Journey or publication.
For a Coaching input update, also require
`coaching_input_regeneration_complete=true`; neither an old successful pair nor
only one regenerated instruction completes the workflow. Verify saved text with
the product reads even when the checker confirms the metadata.
For generation-only outputs, also read `generation_only_workflow_failures` and
each row's `workflow_status`. An edited output stays a failure despite green
readiness. Those rows and failures cover only `requested_artifacts`; before
activation, inspect every protected output on each affected root, including
ones outside a prior report's scope. The checker evaluates supplied metadata;
reading the actual saved
output and verifying its linkage remains required in the tool workflow.

### Guard a proposed manual write

Before `content_update`, hosts with local Python must run:

```text
python3 <skill-directory>/scripts/verify_generation_evidence.py --check-manual-write < proposed-arguments.json
```

Provide the proposed tool arguments privately through stdin or a private local
temporary file. The guard examines `content_type` and `fields`, never prints
field values, and makes no product call. Exit 3 means protected fields are
present: do not send the payload or silently remove fields and pretend the full
request succeeded. Exit 2 means invalid input. Exit 0 only means this field guard
passed; it does not grant authorization, establish editability, or bypass other
checks. Confirmations, active/draft status, and manual-edit requests cannot
override the exclusion. Without local Python, apply the identical field check
before calling a write tool. Creation and other write routes obey the same
generation-only rule even though this CLI mode checks `content_update` arguments.

Without local execution, apply the same rules to tool results and disclose that
the checker was not run. Missing evidence must still remain unverified.

## Final report

Give one concise row per requested part: current content name, artifact/language,
generation state, provenance, freshness, and missing evidence or next action.
Add verified Journey context when useful. Keep supporting request/step IDs and
revisions in the internal evidence; include technical identifiers in the answer
only when the user explicitly requests them for diagnostics or an audit.
Keep readiness and draft/published status separate. For a Journey, include each item and reused root; a generated plan is
not proof that its child content was generated. Do not claim “everything is
platform-generated” while any requested part is edited, stale or unverified.
