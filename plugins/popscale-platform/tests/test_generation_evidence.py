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
    def protected_sample(self, content_type, key):
        data = sample()
        data["root"]["content_type"] = content_type
        data["freshness"]["root"]["content_type"] = content_type
        data["requested_artifacts"] = [key]
        data["freshness"]["artifacts"][0]["key"] = key
        return data

    def test_edited_protected_outputs_fail_even_with_green_readiness(self):
        for content_type, key in (("roleplay", "evaluation_instructions"),
                                  ("coaching_session", "evaluation_instructions"),
                                  ("coaching_session", "agent_prompt"),
                                  ("challenge", "evaluation_prompt")):
            for status in ("active", "draft"):
                with self.subTest(content_type=content_type, key=key, status=status):
                    data = self.protected_sample(content_type, key)
                    data["root"]["status"] = status
                    data["readiness"] = {"can_activate": True}
                    data["freshness"]["artifacts"][0].update(
                        status="source_changed_and_output_edited", output_modified=True)
                    report = verifier.verify(data)
                    self.assertEqual(report["generation_only_workflow_failures"], [key])
                    self.assertEqual(report["artifacts"][0]["provenance"],
                                     "platform_generated_but_edited")
                    self.assertFalse(report["can_report_requested_generation_complete"])
                    self.assertEqual(report["readiness"], "check_separately")

    def test_protected_edit_without_links_or_during_retry_is_still_a_failure(self):
        for patch in ({"generation_request_id": None, "generation_step_id": None},
                      {"execution_status": "generating"},
                      {"status": "current", "output_modified": True},
                      {"status": "output_edited", "output_modified": False}):
            with self.subTest(patch=patch):
                data = self.protected_sample("roleplay", "evaluation_instructions")
                data["freshness"]["artifacts"][0].update(
                    status="source_changed_and_output_edited", output_modified=True)
                data["freshness"]["artifacts"][0].update(patch)
                report = verifier.verify(data)
                self.assertEqual(report["generation_only_workflow_failures"],
                                 ["evaluation_instructions"])
                self.assertFalse(report["can_report_requested_generation_complete"])

    def test_source_change_requires_generation_without_inventing_manual_edit(self):
        data = self.protected_sample("roleplay", "evaluation_instructions")
        data["freshness"]["artifacts"][0]["status"] = "source_changed"
        report = verifier.verify(data)
        self.assertEqual(report["generation_only_workflow_failures"], [])
        self.assertEqual(report["artifacts"][0]["workflow_status"], "regeneration_required")
        self.assertEqual(report["artifacts"][0]["provenance"], "platform_generated")
        self.assertFalse(report["can_report_requested_generation_complete"])

    def test_verified_generation_resolves_protected_output_failure(self):
        data = self.protected_sample("roleplay", "evaluation_instructions")
        data["root"]["status"] = "draft"
        report = verifier.verify(data)
        self.assertEqual(report["generation_only_workflow_failures"], [])
        self.assertEqual(report["artifacts"][0]["workflow_status"],
                         "verified_generation_metadata")
        self.assertTrue(report["can_report_requested_generation_complete"])

    def test_editable_output_edit_does_not_become_generation_only_failure(self):
        data = sample()
        data["freshness"]["artifacts"][1].update(status="output_edited", output_modified=True)
        report = verifier.verify(data)
        self.assertEqual(report["generation_only_workflow_failures"], [])
        self.assertEqual(report["artifacts"][1]["workflow_status"], "not_generation_only")
        self.assertFalse(report["can_report_requested_generation_complete"])

    def test_manually_edited_episode_script_is_a_workflow_failure(self):
        data = sample()
        data["freshness"]["artifacts"][0].update(status="output_edited", output_modified=True)
        report = verifier.verify(data)
        self.assertEqual(report["generation_only_workflow_failures"], ["script"])
        self.assertFalse(report["can_report_requested_generation_complete"])

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


class CoachingInputRegenerationTests(unittest.TestCase):
    def sample(self):
        data = sample()
        data["root"]["content_type"] = "coaching_session"
        data["freshness"]["root"]["content_type"] = "coaching_session"
        data["coaching_inputs_changed"] = True
        data["coaching_regeneration_request_ids"] = [10]
        data["requested_artifacts"] = ["agent_prompt", "evaluation_instructions"]
        for row, key in zip(data["freshness"]["artifacts"],
                            ["agent_prompt", "evaluation_instructions", "description"]):
            row["key"] = key
        return data

    def test_both_new_outputs_complete_coaching_input_update(self):
        report = verifier.verify(self.sample())
        self.assertTrue(report["coaching_input_regeneration_complete"])
        self.assertTrue(report["can_report_requested_generation_complete"])

    def test_requesting_only_one_output_cannot_omit_the_other(self):
        data = self.sample()
        data["requested_artifacts"] = ["agent_prompt"]
        data["freshness"]["artifacts"] = data["freshness"]["artifacts"][:1]
        report = verifier.verify(data)
        self.assertEqual([row["key"] for row in report["artifacts"]],
                         ["agent_prompt", "evaluation_instructions"])
        self.assertFalse(report["coaching_input_regeneration_complete"])
        self.assertFalse(report["can_report_requested_generation_complete"])

    def test_current_old_outputs_do_not_replace_new_generation(self):
        for request_ids in ([], [11]):
            with self.subTest(request_ids=request_ids):
                data = self.sample()
                data["coaching_regeneration_request_ids"] = request_ids
                report = verifier.verify(data)
                self.assertTrue(all(row["freshness"] == "current" for row in report["artifacts"]))
                self.assertFalse(report["coaching_input_regeneration_complete"])
                self.assertFalse(report["can_report_requested_generation_complete"])

    def test_only_one_new_instruction_cannot_complete_the_pair(self):
        for old_index in (0, 1):
            with self.subTest(old_index=old_index):
                data = self.sample()
                data["requests"].append({"id": 9, "status": "completed", "target_object_id": 1,
                                         "step_count": 1})
                data["step_results"].append({"request_id": 9, "steps": [{"id": 9, "status": "completed"}]})
                data["freshness"]["artifacts"][old_index].update(
                    generation_request_id=9, generation_step_id=9)
                self.assertFalse(verifier.verify(data)["coaching_input_regeneration_complete"])

    def test_partial_failed_or_skipped_step_leaves_coaching_incomplete(self):
        for status in ("failed", "running", "skipped"):
            with self.subTest(status=status):
                data = self.sample()
                data["step_results"][0]["steps"][1]["status"] = status
                self.assertFalse(verifier.verify(data)["coaching_input_regeneration_complete"])

    def test_coaching_context_is_explicit_and_validated(self):
        for patch in ({"coaching_inputs_changed": "true"},
                      {"coaching_regeneration_request_ids": [True]},
                      {"coaching_regeneration_request_ids": [10, 10]}):
            data = self.sample()
            data.update(patch)
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                verifier.verify(data)
        self.assertIsNone(verifier.verify(sample())["coaching_input_regeneration_complete"])


class ManualWriteGuardTests(unittest.TestCase):
    def test_confirmations_cannot_authorize_protected_output_writes(self):
        for content_type, field in (("roleplay", "evaluation_instructions"),
                                    ("coaching_session", "evaluation_instructions"),
                                    ("coaching_session", "agent_prompt"),
                                    ("challenge", "evaluation_prompt"),
                                    ("episode", "script"),
                                    ("episode_script_variant", "script_text")):
            for status in ("active", "draft"):
                for value in ("Manually rewritten instruction", "", None):
                    with self.subTest(content_type=content_type, status=status, value=value):
                        proposed = {
                            "content_type": content_type, "object_id": 1,
                            "expected_revision": "synthetic-revision",
                            "confirm_active_edit": True,
                            "confirm_generated_output_override": True,
                            "fields": {field: value},
                        }
                        # Status and intent are hostile extra context, not MCP authority.
                        proposed["status"] = status
                        proposed["user_requested_manual_edit"] = True
                        report = verifier.check_manual_write(proposed)
                        self.assertFalse(report["passes_generation_only_guard"])
                        self.assertEqual(report["blocked_fields"], [field])
                        self.assertEqual(report["next_action"],
                                         "use_platform_generation_or_report_blocker")

    def test_protected_field_cannot_hide_in_mixed_payload_or_child_type(self):
        for content_type in ("roleplay", "roleplay_customer", "episode"):
            report = verifier.check_manual_write({
                "content_type": content_type,
                "fields": {"description": "Synthetic description",
                           "evaluation_instructions": "Synthetic override"},
            })
            self.assertFalse(report["passes_generation_only_guard"])
            self.assertEqual(report["blocked_fields"], ["evaluation_instructions"])

    def test_source_and_normally_editable_fields_pass_only_field_policy(self):
        for content_type, fields in (
                ("roleplay", {"success_behaviours": "Ask about the customer's goal"}),
                ("roleplay_customer", {"personality_description": "Hesitant"}),
                ("roleplay_evaluation_criterion", {"max_points": 5}),
                ("coaching_session", {"coaching_context": "Practice planning"}),
                ("episode", {"description": "A synthetic summary"})):
            with self.subTest(content_type=content_type):
                report = verifier.check_manual_write({"content_type": content_type, "fields": fields})
                self.assertTrue(report["passes_generation_only_guard"])
                self.assertEqual(report["next_action"], "apply_normal_authorization_and_schema_checks")

    def test_episode_script_input_is_allowed_but_mixed_script_write_is_blocked(self):
        args = {"content_type": "episode", "fields": {
            "content": "Question techniques", "model_steering": "Use anonymous voices."}}
        self.assertTrue(verifier.check_manual_write(args)["passes_generation_only_guard"])
        args["fields"]["script"] = "Speaker 1: Synthetic replacement"
        report = verifier.check_manual_write(args)
        self.assertFalse(report["passes_generation_only_guard"])
        self.assertEqual(report["blocked_fields"], ["script"])

    def test_episode_root_and_component_create_update_payloads_cannot_write_script(self):
        for field, extra in (("script", {}), ("script_text", {"component_type": "episode_script_variant"})):
            for value in (None, "", "Speaker 1: Synthetic output"):
                for ids in ({}, {"object_id": 1, "component_id": 2, "expected_revision": "r1"}):
                    args = {"content_type": "episode", "fields": {field: value}, **extra, **ids}
                    with self.subTest(args=args):
                        self.assertFalse(verifier.check_manual_write(args)["passes_generation_only_guard"])

    def test_cli_blocks_episode_component_script_without_echoing_content(self):
        args = {"content_type": "episode", "component_type": "episode_script_variant",
                "fields": {"script_text": "SYNTHETIC_PRIVATE_SCRIPT"}}
        result = subprocess.run([sys.executable, str(SCRIPT), "--check-manual-write"],
                                input=json.dumps(args), capture_output=True, text=True)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["blocked_fields"], ["script_text"])
        self.assertNotIn("SYNTHETIC_PRIVATE_SCRIPT", result.stdout + result.stderr)

    def test_invalid_write_input_fails_closed(self):
        for arguments in ({}, {"content_type": "unknown", "fields": {"name": "x"}},
                          {"content_type": "roleplay", "fields": {}},
                          {"content_type": "roleplay", "fields": []}):
            with self.subTest(arguments=arguments), self.assertRaises(ValueError):
                verifier.check_manual_write(arguments)

    def test_cli_blocks_manual_request_without_echoing_output_text(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--check-manual-write"],
            input=json.dumps({"content_type": "roleplay",
                              "confirm_generated_output_override": True,
                              "fields": {"evaluation_instructions": "SYNTHETIC_PRIVATE_CONTENT"}}),
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 3)
        self.assertFalse(json.loads(result.stdout)["passes_generation_only_guard"])
        self.assertNotIn("SYNTHETIC_PRIVATE_CONTENT", result.stdout + result.stderr)

    def test_cli_permitted_field_and_invalid_input_exit_codes(self):
        for payload, code in ((json.dumps({"content_type": "episode", "fields": {"description": "x"}}), 0),
                              ('{"private":"SYNTHETIC_SECRET",', 2)):
            with self.subTest(code=code):
                result = subprocess.run([sys.executable, str(SCRIPT), "--check-manual-write"],
                                        input=payload, capture_output=True, text=True)
                self.assertEqual(result.returncode, code)
                self.assertNotIn("SYNTHETIC_SECRET", result.stdout + result.stderr)
