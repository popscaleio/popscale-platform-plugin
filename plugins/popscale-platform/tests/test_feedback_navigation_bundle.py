"""Release integration checks; behavioral cases require separate host evaluation."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
PLUGIN = ROOT / "plugins/popscale-platform"
spec = importlib.util.spec_from_file_location("feedback_bundle", ROOT / "scripts/build_public_skills.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
NEW_TOOLS = {
    "submit_feedback", "list_feedback", "get_feedback", "feedback_statistics",
    "platform_feedback_list", "platform_feedback_get", "platform_feedback_context",
    "platform_feedback_statistics", "update_feedback_status", "navigation_resolve",
}


class FeedbackNavigationBundleTests(unittest.TestCase):
    def setUp(self):
        self.sources = {str(p.relative_to(PLUGIN)): p.read_text()
                        for p in (PLUGIN / "skills").rglob("*.md")}
        self.contract = json.loads((ROOT / "contracts/product-tools-v1.json").read_text())

    def bundle(self):
        return json.loads(builder.build_bundle(self.sources, "1.5.0", "a" * 40, self.contract))

    def test_all_new_tools_reach_consumer_requirements(self):
        body = self.bundle()
        self.assertTrue(NEW_TOOLS.issubset(body["required_tools"]))
        self.assertEqual(len([p for p in body["instruction_paths"] if p.endswith("/SKILL.md")]), 6)
        # New tools retain the same mutation envelope; compatibility is also
        # gated by the consumer checking every required tool.
        self.assertEqual(body["tool_contract_version"], "popscale.product.actions.v1")

    def test_mode_references_are_packaged_and_evaluations_are_external(self):
        paths = self.bundle()["required_reference_paths"]
        self.assertTrue((ROOT / "docs/evaluation/safe-product-feedback.md").is_file())
        self.assertFalse(any("evaluation" in path for path in self.bundle()["instruction_paths"]))
        for path in (
            "skills/safe-product-feedback/references/platform-review.md",
            "skills/route-popscale-requests/references/navigation-and-activity.md",
            "skills/route-popscale-requests/references/product-actions.md",
        ):
            self.assertIn(path, paths)
            original = self.sources.pop(path)
            with self.assertRaisesRegex(ValueError, "Missing Markdown dependency"):
                self.bundle()
            self.sources[path] = original

    def test_relevant_workflows_reach_feedback_and_navigation_without_host_metadata(self):
        for name in ("route-popscale-requests", "safe-product-feedback"):
            visited, _ = builder.dependency_closure(self.sources, [f"skills/{name}/SKILL.md"])
            self.assertIn("skills/safe-product-feedback/SKILL.md", visited)
            self.assertIn("skills/route-popscale-requests/references/navigation-and-activity.md", visited)
            self.assertFalse(any("/agents/" in path for path in visited))

    def test_review_scope_not_added_to_connection_defaults(self):
        config = json.loads((PLUGIN / ".mcp.json").read_text())
        self.assertEqual(config["mcpServers"]["popscale-platform"],
                         {"type": "http", "url": "https://app.popscale.io/mcp/"})
        metadata = (PLUGIN / "skills/safe-product-feedback/agents/openai.yaml").read_text()
        self.assertNotIn("feedback:review", metadata)
        self.assertNotIn("popscale-docs", metadata)


if __name__ == "__main__":
    unittest.main()
