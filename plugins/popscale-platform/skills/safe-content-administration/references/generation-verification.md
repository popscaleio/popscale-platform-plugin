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
| Same bound evidence plus `output_edited`, `source_changed_and_output_edited` or `output_modified=true` | Platform-generated, then edited; this alone does not identify who or what edited it |
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

For an explicitly requested manual edit, explain its provenance consequence and
use any override confirmation exposed by the live schema. Do not add unsupported
confirmation fields. Read the result and freshness again. Do not regenerate
unknown or edited content automatically to make a report green.

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
without server evidence. Missing native provenance does not authorize a rebuild
or prevent separately authorized publication that passes server readiness.

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

Without local execution, apply the same rules to tool results and disclose that
the checker was not run. Missing evidence must still remain unverified.

## Final report

Give one concise row per requested part: target/artifact/language, generation
state, provenance, freshness, supporting request/step IDs where present, and
missing evidence or next action. Keep readiness and draft/published status
separate. For a Journey, include each item and reused root; a generated plan is
not proof that its child content was generated. Do not claim “everything is
platform-generated” while any requested part is edited, stale or unverified.
