#!/usr/bin/env python3
"""Conservative, offline reporting over caller-supplied Product MCP evidence.

No network, credentials, writes, or content output. This is not an authorization
check or a substitute for fresh reads from the selected-company MCP connection.
See ../references/generation-verification.md for the input and trust boundary.
"""

import argparse
import json
import sys


GENERATION_ONLY_OUTPUTS = {
    "roleplay": frozenset({"evaluation_instructions"}),
    "coaching_session": frozenset({"evaluation_instructions", "agent_prompt"}),
    "challenge": frozenset({"evaluation_prompt"}),
    "episode": frozenset({"script"}),
    "episode_script_variant": frozenset({"script_text"}),
}
MANUAL_WRITE_TYPES = frozenset({
    "roleplay", "coaching_session", "challenge", "episode", "flashcard_deck",
    "journey", "roleplay_customer", "roleplay_evaluation_criterion",
    "episode_script_variant", "flashcard_card", "flashcard_translation",
})
PROTECTED_FIELD_NAMES = frozenset().union(*GENERATION_ONLY_OUTPUTS.values())


def check_manual_write(arguments):
    """Check field policy only; never authorize or execute a Product MCP write."""
    _complete_result(arguments)
    content_type = arguments.get("content_type")
    fields = arguments.get("fields")
    if (not isinstance(content_type, str) or content_type not in MANUAL_WRITE_TYPES
            or not isinstance(fields, dict) or not fields
            or any(not isinstance(key, str) or not key for key in fields)):
        raise ValueError("Expected known content type and nonempty fields.")
    # Reject protected names even on a wrong root/child type, not just the
    # normal format mapping. Null, empty, and identical values are writes too.
    blocked = sorted(PROTECTED_FIELD_NAMES.intersection(fields))
    return {
        "passes_generation_only_guard": not blocked,
        "blocked_fields": blocked,
        "next_action": ("use_platform_generation_or_report_blocker" if blocked
                        else "apply_normal_authorization_and_schema_checks"),
    }


def _complete_result(value):
    if not isinstance(value, dict) or any(value.get(key) for key in
                                         ("isError", "truncated", "has_more")):
        raise ValueError("Evidence must be a successful, complete tool result.")
    return value


def _index(rows, key):
    if not isinstance(rows, list):
        raise ValueError("Expected evidence rows.")
    result = {}
    for row in rows:
        _complete_result(row)
        identity = row.get(key)
        if isinstance(identity, bool) or not isinstance(identity, (str, int)) or not identity:
            raise ValueError("Missing evidence identity.")
        if identity in result:
            raise ValueError("Duplicate evidence identity; refresh the reads.")
        result[identity] = row
    return result


def verify(evidence):
    _complete_result(evidence)
    root = _complete_result(evidence.get("root"))
    if not isinstance(root.get("content_type"), str) or type(root.get("object_id")) is not int:
        raise ValueError("Specify the intended content root.")
    freshness = _complete_result(evidence.get("freshness"))
    actual = _complete_result(freshness.get("root"))
    if any(root[key] != actual.get(key) for key in ("content_type", "object_id")):
        raise ValueError("Freshness belongs to a different root.")
    if freshness.get("available") is not True:
        raise ValueError("Artifact evidence is unavailable for this root.")
    keys = evidence.get("requested_artifacts")
    if not isinstance(keys, list) or not keys or any(not isinstance(k, str) or not k for k in keys):
        raise ValueError("List every requested artifact, including unavailable ones.")
    if len(set(keys)) != len(keys):
        raise ValueError("Requested artifacts must be unique.")
    coaching_changed = evidence.get("coaching_inputs_changed", False)
    if type(coaching_changed) is not bool:
        raise ValueError("Coaching input-change context must be boolean.")
    coaching_requests = evidence.get("coaching_regeneration_request_ids", [])
    if (not isinstance(coaching_requests, list)
            or any(type(request_id) is not int or request_id <= 0 for request_id in coaching_requests)
            or len(set(coaching_requests)) != len(coaching_requests)):
        raise ValueError("Expected unique server request IDs.")
    if coaching_changed:
        if root["content_type"] != "coaching_session":
            raise ValueError("Coaching input-change context requires a Coaching root.")
        keys = list(dict.fromkeys(keys + ["agent_prompt", "evaluation_instructions"]))
    artifacts = _index(freshness.get("artifacts"), "key")
    requests = _index(evidence.get("requests", []), "id")
    step_results = _index(evidence.get("step_results", []), "request_id")
    steps = {request_id: _index(result.get("steps"), "id")
             for request_id, result in step_results.items()}
    rows = []
    for key in keys:
        artifact = artifacts.get(key, {})
        request_id = artifact.get("generation_request_id")
        step_id = artifact.get("generation_step_id")
        request = requests.get(request_id, {})
        step = steps.get(request_id, {}).get(step_id, {})
        state = artifact.get("status", "unavailable")
        execution = artifact.get("execution_status")
        generation_only = key in GENERATION_ONLY_OUTPUTS.get(root["content_type"], ())
        edited_output = artifact.get("output_modified") is True or state in (
            "output_edited", "source_changed_and_output_edited")
        provenance, reason = "unverified", "missing_or_incomplete_evidence"
        if execution:
            # A newer attempt may replace IDs while keeping the old timestamp.
            reason = "execution_overlay_requires_refresh"
        elif state in ("legacy_unknown", "not_generated"):
            provenance, reason = state, state
        elif (state in ("current", "source_changed", "output_edited", "source_changed_and_output_edited")
              and type(artifact.get("output_modified")) is bool
              and artifact.get("generated_at")
              and request and step.get("status") == "completed"
              and request.get("target_object_id") == root["object_id"]):
            edited = artifact["output_modified"] or state in (
                "output_edited", "source_changed_and_output_edited")
            provenance = "platform_generated_but_edited" if edited else "platform_generated"
            reason = "bound_completed_step"
        workflow_status = "not_generation_only"
        if generation_only:
            if edited_output:
                workflow_status = "workflow_failure"
            elif provenance == "platform_generated" and state == "current":
                workflow_status = "verified_generation_metadata"
            elif state in ("source_changed", "not_generated"):
                workflow_status = "regeneration_required"
            else:
                workflow_status = "verification_required"
        rows.append({
            "key": key, "provenance": provenance, "freshness": state,
            "execution_status": execution, "reason": reason,
            "generation_request_id": request_id, "generation_step_id": step_id,
            "request_status": request.get("status", "unavailable"),
            "generation_only": generation_only, "workflow_status": workflow_status,
        })
    complete = bool(requests) and all(
        request.get("status") == "completed"
        and request.get("target_object_id") == root["object_id"]
        and type(request.get("step_count")) is int
        and request["step_count"] == len(steps.get(request_id, {}))
        and all(step.get("status") in ("completed", "skipped")
                for step in steps.get(request_id, {}).values())
        for request_id, request in requests.items()
    ) and all(
        row["provenance"] == "platform_generated"
        and row["freshness"] == "current"
        and row["request_status"] == "completed"
        for row in rows
    )
    coaching_complete = None
    if coaching_changed:
        coaching_complete = complete and all(
            row["generation_request_id"] in coaching_requests
            for row in rows if row["key"] in GENERATION_ONLY_OUTPUTS["coaching_session"]
        )
        complete = complete and coaching_complete
    return {
        "root": {key: root[key] for key in ("content_type", "object_id")},
        "artifacts": rows,
        "generation_only_workflow_failures": [
            row["key"] for row in rows if row["workflow_status"] == "workflow_failure"
        ],
        "can_report_requested_generation_complete": complete,
        "coaching_input_regeneration_complete": coaching_complete,
        "readiness": "check_separately",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-manual-write", action="store_true",
                        help="Reject protected fields in proposed root/component create or update arguments.")
    args = parser.parse_args()
    try:
        payload = json.load(sys.stdin)
        result = check_manual_write(payload) if args.check_manual_write else verify(payload)
    except (ValueError, TypeError, KeyError, AttributeError):
        print("Invalid or unavailable evidence; generation is not verified.", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.check_manual_write and not result["passes_generation_only_guard"]:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
