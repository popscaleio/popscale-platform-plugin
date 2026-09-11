#!/usr/bin/env python3
"""Conservative, offline reporting over caller-supplied Product MCP evidence.

No network, credentials, writes, or content output. This is not an authorization
check or a substitute for fresh reads from the selected-company MCP connection.
See ../references/generation-verification.md for the input and trust boundary.
"""

import json
import sys


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
        rows.append({
            "key": key, "provenance": provenance, "freshness": state,
            "execution_status": execution, "reason": reason,
            "generation_request_id": request_id, "generation_step_id": step_id,
            "request_status": request.get("status", "unavailable"),
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
    return {
        "root": {key: root[key] for key in ("content_type", "object_id")},
        "artifacts": rows,
        "can_report_requested_generation_complete": complete,
        "readiness": "check_separately",
    }


def main():
    try:
        result = verify(json.load(sys.stdin))
    except (ValueError, TypeError, KeyError, AttributeError):
        print("Invalid or unavailable evidence; generation is not verified.", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
