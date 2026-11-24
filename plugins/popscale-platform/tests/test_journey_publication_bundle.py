"""Package compatibility for the exact, server-owned publication workflow.

These checks establish bundle dependencies, not live approval or publication.
Host behavior is covered by the separate synthetic acceptance cases.
"""
import importlib.util
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[3]
PLUGIN = ROOT / "plugins/popscale-platform"
spec = importlib.util.spec_from_file_location("publication_bundle", ROOT / "scripts/build_public_skills.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
PUBLICATION = "skills/safe-journey-creation/references/publication.md"


class JourneyPublicationBundleTests(unittest.TestCase):
    def setUp(self):
        self.sources = {str(path.relative_to(PLUGIN)): path.read_text()
                        for path in (PLUGIN / "skills").rglob("*.md")}
        self.contract = json.loads((ROOT / "contracts/product-tools-v1.json").read_text())

    def bundle(self):
        return json.loads(builder.build_bundle(self.sources, "1.6.10", "a" * 40, self.contract))

    def test_bundle_requires_new_publication_and_keeps_individual_commands(self):
        bundle = self.bundle()
        self.assertEqual(bundle["tool_contract_version"], "popscale.product.actions.v1")
        self.assertTrue({"journey_publish_bundle", "content_activate", "journey_activate",
                         "product_action_get", "product_action_execute"}.issubset(bundle["required_tools"]))
        self.assertNotIn("product_action_approve", bundle["required_tools"])
        source = self.contract["additive_tool_sources"].get("journey_publish_bundle", "")
        self.assertIsNotNone(re.fullmatch(r"[0-9a-f]{40}", source))
        self.assertNotEqual(source, self.contract["source_commit"])

    def test_both_entrypoints_package_the_publication_contract_once(self):
        for entrypoint in ("safe-journey-creation", "route-popscale-requests"):
            with self.subTest(skill=entrypoint):
                paths, _ = builder.dependency_closure(
                    self.sources, [f"skills/{entrypoint}/SKILL.md"])
                self.assertIn(PUBLICATION, paths)
        bundle = self.bundle()
        self.assertEqual(sum(item["path"] == PUBLICATION for item in bundle["files"]), 1)
        self.assertIn(PUBLICATION, bundle["required_reference_paths"])
        self.assertFalse(any("evaluation/" in path for path in bundle["instruction_paths"]))

    def test_missing_publication_reference_cannot_ship(self):
        self.sources.pop(PUBLICATION, None)
        with self.assertRaisesRegex(ValueError, "Missing Markdown dependency"):
            self.bundle()


if __name__ == "__main__":
    unittest.main()
