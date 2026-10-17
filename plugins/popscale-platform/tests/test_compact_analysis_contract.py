"""Public compact workflow contracts; these tests make no host-support claim."""
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
PLUGIN = ROOT / "plugins/popscale-platform"
REFERENCE = "skills/safe-interview-administration/references/compact-analysis.md"
SPEC = importlib.util.spec_from_file_location("compact_bundle_builder", ROOT / "scripts/build_public_skills.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)

# Reviewed P3b2 subset. W is independently required only for own context/save.
OPERATIONS = {
    "get_interview_analysis_capabilities": ("R", "AnalysisCapabilities"),
    "list_interview_analysis_studies": ("R", "StudyList"),
    "get_interview_analysis_study": ("R", "StudyDetail"),
    "create_interview_analysis": ("R+W", "envelope: AnalysisContext"),
    "get_interview_analysis_context": ("R", "AnalysisContext"),
    "prepare_interview_dataset": ("R", "envelope: PreparedDataset"),
    "get_interview_dataset": ("R", "Dataset"),
    "get_interview_dataset_job": ("R", "DatasetJob"),
    "read_interview_dataset_page": ("R", "DatasetPage"),
    "get_interview_dataset_artifact": ("R", "envelope: ArtifactAccess"),
    "save_interview_dataset": ("R+W", "envelope: Dataset"),
    "cancel_interview_dataset_job": ("R", "envelope: DatasetJob"),
}


def sources():
    return {str(path.relative_to(PLUGIN)): path.read_text(encoding="utf-8")
            for path in (PLUGIN / "skills").rglob("*.md")}


def build(content=None):
    contract = json.loads((ROOT / "contracts/product-tools-v1.json").read_text())
    return json.loads(builder.build_bundle(
        sources() if content is None else content, "1.6.8", "a" * 40, contract))


class CompactAnalysisContractTests(unittest.TestCase):
    def test_exact_operation_matrix_preserves_effects_and_minimal_write_scopes(self):
        text = (PLUGIN / REFERENCE).read_text()
        rows = re.findall(r"^\| `([a-z_]+)` \| (R(?:\+W)?) \| ([^|]+) \|$", text, re.M)
        self.assertEqual(len(rows), 12)
        self.assertEqual({name: (scope, result.strip()) for name, scope, result in rows}, OPERATIONS)
        actions = {name for name, (_, result) in OPERATIONS.items() if result.startswith("envelope:")}
        self.assertEqual(len(actions), 5)
        self.assertEqual(actions - {"create_interview_analysis", "save_interview_dataset"}, {
            "prepare_interview_dataset", "get_interview_dataset_artifact", "cancel_interview_dataset_job"})
        contract = json.loads((ROOT / "contracts/product-tools-v1.json").read_text())
        self.assertEqual(len(contract["product_tools"]), len(set(contract["product_tools"])))
        self.assertTrue(set(OPERATIONS).issubset(contract["product_tools"]))
        self.assertEqual(contract["tool_contract_version"], "popscale.product.actions.v1")

    def test_all_twelve_tools_and_reference_reach_the_real_runtime_bundle(self):
        bundle = build()
        self.assertIn(REFERENCE, bundle["instruction_paths"])
        self.assertIn(REFERENCE, bundle["required_reference_paths"])
        self.assertTrue(set(OPERATIONS).issubset(bundle["required_tools"]))
        self.assertNotIn("start_interview_classification", bundle["required_tools"])
        self.assertFalse(any("docs/evaluation/" in path for path in bundle["instruction_paths"]))
        self.assertEqual(bundle["schema_version"], "popscale.public_skills.v1")

    def test_compact_reference_is_required_and_its_change_invalidates_bundle_identity(self):
        content = sources()
        original = build(content)
        content[REFERENCE] += "\nAdditional host evidence remains separately required.\n"
        self.assertNotEqual(original["skill_bundle_sha256"], build(content)["skill_bundle_sha256"])
        del content[REFERENCE]
        with self.assertRaisesRegex(ValueError, "Missing Markdown dependency"):
            build(content)

    def test_compact_selection_precedes_admin_gate_and_preserves_host_boundary(self):
        skill = (PLUGIN / "skills/safe-interview-administration/SKILL.md").read_text()
        compact = (PLUGIN / REFERENCE).read_text()
        self.assertLess(skill.index("compact-analysis.md"), skill.index("require active `company_admin`"))
        self.assertIn("does not require Company Admin", skill)
        self.assertIn("Platform assistant is unsupported until separate P3b3", compact)
        self.assertIn("transport_unavailable", compact)
        self.assertIn("never a bearer in", (ROOT / "docs/evaluation/safe-interview-administration.md").read_text())
        self.assertIn("A skill cannot extract the host credential", compact)
        self.assertIn("Five bounded writes always return `{product_action, action_url}`", compact)
        self.assertIn("result is `product_action.result`", compact)
        self.assertIn("`idempotency_key` and transport `command_id`", compact)


if __name__ == "__main__":
    unittest.main()
