"""Role workflow packaging; synthetic host cases establish separate acceptance."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
PLUGIN = ROOT / "plugins/popscale-platform"
spec = importlib.util.spec_from_file_location("role_assignment_bundle", ROOT / "scripts/build_public_skills.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
REFERENCE = "skills/route-popscale-requests/references/role-assignment.md"
ROLE_TOOLS = {
    "admin_user_list", "admin_user_get", "admin_membership_organization_get",
    "admin_business_role_list", "admin_unit_list", "admin_unit_get",
    "admin_membership_role_units_add", "admin_membership_business_roles_set",
}


class RoleAssignmentBundleTests(unittest.TestCase):
    def setUp(self):
        self.sources = {str(path.relative_to(PLUGIN)): path.read_text(encoding="utf-8")
                        for path in (PLUGIN / "skills").rglob("*.md")}
        self.contract = json.loads((ROOT / "contracts/product-tools-v1.json").read_text())

    def bundle(self):
        return json.loads(builder.build_bundle(self.sources, "1.6.11", "a" * 40, self.contract))

    def test_role_workflow_tools_reach_consumer_compatibility_gate(self):
        body = self.bundle()
        # The builder intersects mentions with the fixture: an omitted name
        # would otherwise silently disappear from a consuming host's gate.
        self.assertTrue(ROLE_TOOLS.issubset(body["required_tools"]))
        for name in ROLE_TOOLS:
            self.assertRegex(self.contract["additive_tool_sources"][name], r"^[0-9a-f]{40}$")
        self.assertEqual(len([path for path in body["instruction_paths"] if path.endswith("/SKILL.md")]), 6)
        self.assertEqual(body["tool_contract_version"], "popscale.product.actions.v1")
        self.assertNotIn("product_action_approve", body["required_tools"])

    def test_routing_packages_role_method_and_shared_approval_dependency(self):
        visited, references = builder.dependency_closure(self.sources, ["skills/route-popscale-requests/SKILL.md"])
        self.assertIn(REFERENCE, references)
        self.assertIn("skills/route-popscale-requests/references/product-actions.md", visited)
        self.assertIn(REFERENCE, self.bundle()["required_reference_paths"])
        self.sources.pop(REFERENCE)
        with self.assertRaisesRegex(ValueError, "Missing Markdown dependency"):
            self.bundle()

    def test_role_evidence_method_is_checksummed_but_host_cases_are_not_runtime_text(self):
        original = self.bundle()
        self.sources[REFERENCE] += "\nAdditional role-source verification.\n"
        updated = self.bundle()
        self.assertNotEqual(original["skill_bundle_sha256"], updated["skill_bundle_sha256"])
        self.assertTrue((ROOT / "docs/evaluation/role-assignment.md").is_file())
        self.assertFalse(any("evaluation/" in path for path in updated["instruction_paths"]))


if __name__ == "__main__":
    unittest.main()
