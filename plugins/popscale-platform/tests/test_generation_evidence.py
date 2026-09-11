"""Synthetic tool snapshots: no customer content or live product operations."""

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = (Path(__file__).resolve().parents[1] / "skills" /
          "safe-content-administration" / "scripts" / "verify_generation_evidence.py")
spec = importlib.util.spec_from_file_location("generation_evidence", SCRIPT)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


def sample():
    return {
        "root": {"content_type": "episode", "object_id": 1},
        "requested_artifacts": ["script", "description", "education_text"],
        "freshness": {
            "available": True,
            "root": {"content_type": "episode", "object_id": 1},
            "artifacts": [
                {"key": key, "status": "current", "output_modified": False,
                 "generated_at": "2026-01-01T12:00:00Z",
                 "generation_request_id": 10, "generation_step_id": index}
                for index, key in enumerate(["script", "description", "education_text"], 1)
            ],
        },
        "requests": [{"id": 10, "status": "completed", "target_object_id": 1, "step_count": 3}],
        "step_results": [{"request_id": 10, "steps": [
            {"id": index, "step_key": key, "status": "completed"}
            for index, key in enumerate(["script", "description", "education_text"], 1)
        ]}],
    }


class GenerationEvidenceTests(unittest.TestCase):
    def test_completed_bound_steps_verify_each_requested_artifact(self):
        report = verifier.verify(sample())
        self.assertTrue(report["can_report_requested_generation_complete"])
        self.assertEqual([row["provenance"] for row in report["artifacts"]],
                         ["platform_generated"] * 3)

    def test_filled_ready_episode_does_not_prove_unknown_description_or_education(self):
        data = sample()
        data["readiness"] = {"can_activate": True}
        for row in data["freshness"]["artifacts"][1:]:
            row.update(status="legacy_unknown", generated_at=None,
                       generation_request_id=None, generation_step_id=None)
        report = verifier.verify(data)
        self.assertFalse(report["can_report_requested_generation_complete"])
        self.assertEqual([r["provenance"] for r in report["artifacts"]],
                         ["platform_generated", "legacy_unknown", "legacy_unknown"])

    def test_manual_edit_is_not_reported_as_unchanged_generation(self):
        for content_type in ("roleplay", "coaching_session", "challenge", "episode", "flashcard_deck"):
            with self.subTest(content_type=content_type):
                data = sample()
                data["root"]["content_type"] = content_type
                data["freshness"]["root"]["content_type"] = content_type
                data["freshness"]["artifacts"][0].update(status="output_edited", output_modified=True)
                report = verifier.verify(data)
                self.assertEqual(report["artifacts"][0]["provenance"], "platform_generated_but_edited")
                self.assertFalse(report["can_report_requested_generation_complete"])

    def test_partial_request_preserves_successful_parts_without_blanket_success(self):
        data = sample()
        data["requests"][0]["status"] = "partial"
        data["step_results"][0]["steps"][2]["status"] = "failed"
        report = verifier.verify(data)
        self.assertEqual(report["artifacts"][0]["provenance"], "platform_generated")
        self.assertEqual(report["artifacts"][2]["provenance"], "unverified")
        self.assertFalse(report["can_report_requested_generation_complete"])

    def test_failed_or_running_overlay_does_not_reuse_old_baseline_timestamp(self):
        for status in ("generation_failed", "generating"):
            with self.subTest(status=status):
                data = sample()
                data["freshness"]["artifacts"][0]["execution_status"] = status
                report = verifier.verify(data)
                self.assertEqual(report["artifacts"][0]["provenance"], "unverified")
                self.assertEqual(report["artifacts"][0]["execution_status"], status)
                self.assertFalse(report["can_report_requested_generation_complete"])

    def test_current_or_timestamp_alone_does_not_prove_generation(self):
        for field in ("generation_request_id", "generation_step_id", "generated_at"):
            data = sample()
            data["freshness"]["artifacts"][0][field] = None
            self.assertEqual(verifier.verify(data)["artifacts"][0]["provenance"], "unverified")

    def test_step_from_another_request_is_not_evidence(self):
        data = sample()
        data["step_results"][0]["request_id"] = 20
        self.assertFalse(verifier.verify(data)["can_report_requested_generation_complete"])

    def test_request_for_another_target_cannot_verify_the_artifact(self):
        data = sample()
        data["requests"][0]["target_object_id"] = 2
        self.assertEqual(verifier.verify(data)["artifacts"][0]["provenance"], "unverified")

    def test_old_provenance_does_not_hide_failed_current_operation(self):
        data = sample()
        data["requests"].append({"id": 11, "status": "failed", "target_object_id": 1, "step_count": 1})
        data["step_results"].append({"request_id": 11, "steps": [{"id": 4, "status": "failed"}]})
        report = verifier.verify(data)
        self.assertEqual(report["artifacts"][0]["provenance"], "platform_generated")
        self.assertFalse(report["can_report_requested_generation_complete"])

    def test_missing_step_rows_cannot_be_reported_complete(self):
        data = sample()
        data["requested_artifacts"] = ["script"]
        data["step_results"][0]["steps"] = data["step_results"][0]["steps"][:1]
        self.assertFalse(verifier.verify(data)["can_report_requested_generation_complete"])

    def test_inconsistent_new_request_does_not_hide_a_failed_step(self):
        data = sample()
        data["requests"].append({"id": 11, "status": "completed", "target_object_id": 1, "step_count": 1})
        data["step_results"].append({"request_id": 11, "steps": [{"id": 4, "status": "failed"}]})
        self.assertFalse(verifier.verify(data)["can_report_requested_generation_complete"])

    def test_completed_request_does_not_upgrade_skipped_artifact(self):
        data = sample()
        data["step_results"][0]["steps"][0]["status"] = "skipped"
        self.assertFalse(verifier.verify(data)["can_report_requested_generation_complete"])

    def test_cards_binding_uses_step_id_not_guessed_step_name(self):
        data = sample()
        data["requested_artifacts"] = ["cards"]
        data["freshness"]["artifacts"][0]["key"] = "cards"
        data["step_results"][0]["steps"][0]["step_key"] = "initial_cards"
        self.assertTrue(verifier.verify(data)["can_report_requested_generation_complete"])

    def test_wrong_root_rejects_snapshot(self):
        data = sample()
        data["freshness"]["root"]["object_id"] = 2
        with self.assertRaises(ValueError):
            verifier.verify(data)

    def test_missing_requested_artifact_is_not_silently_omitted(self):
        data = sample()
        data["requested_artifacts"].append("audio")
        report = verifier.verify(data)
        self.assertEqual(report["artifacts"][-1]["provenance"], "unverified")
        self.assertFalse(report["can_report_requested_generation_complete"])

    def test_native_translation_without_ids_remains_unverified(self):
        data = sample()
        data["requested_artifacts"] = ["translation:7"]
        data["freshness"]["artifacts"] = [{
            "key": "translation:7", "status": "current", "output_modified": False,
            "generated_at": "2026-01-01T12:00:00Z", "generation_request_id": None,
            "generation_step_id": None,
        }]
        self.assertEqual(verifier.verify(data)["artifacts"][0]["provenance"], "unverified")

    def test_source_change_keeps_origin_separate_from_currentness(self):
        data = sample()
        data["freshness"]["artifacts"][0]["status"] = "source_changed"
        report = verifier.verify(data)
        self.assertEqual(report["artifacts"][0]["provenance"], "platform_generated")
        self.assertEqual(report["artifacts"][0]["freshness"], "source_changed")
        self.assertFalse(report["can_report_requested_generation_complete"])

    def test_duplicate_evidence_and_empty_scope_fail_closed(self):
        for key in ("requested_artifacts", "requests", "step_results"):
            data = sample()
            data[key].append(copy.deepcopy(data[key][0]))
            with self.subTest(key=key), self.assertRaises(ValueError):
                verifier.verify(data)
        data = sample()
        data["requested_artifacts"] = []
        with self.assertRaises(ValueError):
            verifier.verify(data)

    def test_unavailable_or_truncated_evidence_cannot_be_complete(self):
        for patch in ({"available": False}, {"truncated": True}, {"has_more": True}):
            data = sample()
            data["freshness"].update(patch)
            with self.assertRaises(ValueError):
                verifier.verify(data)

    def test_cli_never_echoes_customer_payload_on_invalid_input(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], input='{"private": "SYNTHETIC_SECRET",',
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("SYNTHETIC_SECRET", result.stdout + result.stderr)

    def test_cli_outputs_only_evidence_summary(self):
        data = sample()
        data["requests"][0]["input_payload"] = {"text": "SYNTHETIC_PRIVATE_CONTENT"}
        result = subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps(data),
                                capture_output=True, text=True, check=True)
        self.assertTrue(json.loads(result.stdout)["can_report_requested_generation_complete"])
        self.assertNotIn("SYNTHETIC_PRIVATE_CONTENT", result.stdout)
