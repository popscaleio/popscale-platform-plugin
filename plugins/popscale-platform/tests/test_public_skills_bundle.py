import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("build_public_skills", ROOT / "scripts/build_public_skills.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
PLUGIN = ROOT / "plugins/popscale-platform"


def sources():
    return {str(path.relative_to(PLUGIN)): path.read_text(encoding="utf-8")
            for path in (PLUGIN / "skills").rglob("*.md")}


def contract():
    return json.loads((ROOT / "contracts/product-tools-v1.json").read_text())


class PublicSkillsBundleTests(unittest.TestCase):
    def build(self, content=None):
        return builder.build_bundle(content if content is not None else sources(), "1.3.1", "a" * 40, contract())

    def test_real_bundle_is_deterministic_text_only_and_self_consistent(self):
        original = sources()
        raw = self.build(original)
        self.assertEqual(raw, self.build(dict(reversed(list(original.items())))))
        body = json.loads(raw)
        self.assertEqual(body["schema_version"], "popscale.public_skills.v1")
        self.assertLessEqual(len(raw), builder.MAX_BUNDLE_BYTES)
        identities = []
        for entry in body["files"]:
            self.assertTrue(entry["path"].endswith(".md"))
            self.assertNotIn("/agents/", entry["path"])
            self.assertNotIn("/scripts/", entry["path"])
            self.assertEqual(entry["content"], original[entry["path"]])
            self.assertEqual(entry["sha256"], hashlib.sha256(entry["content"].encode()).hexdigest())
            identities.append({"path": entry["path"], "sha256": entry["sha256"]})
        self.assertEqual(body["skill_bundle_sha256"], hashlib.sha256(builder.canonical(identities)).hexdigest())
        self.assertEqual(set(body["instruction_paths"]), {f["path"] for f in body["files"]})
        self.assertTrue(set(body["required_reference_paths"]).issubset(body["instruction_paths"]))
        for tool in ("current_user", "product_action_prepare", "product_action_get", "product_action_execute", "request_company_switch"):
            self.assertIn(tool, body["required_tools"])
        for docs_tool in ("get_docs_overview", "search_docs", "get_pages"):
            self.assertNotIn(docs_tool, body["required_tools"])

    def test_transitive_reference_change_changes_identity(self):
        original = sources()
        before = json.loads(self.build(original))
        original["skills/safe-content-administration/references/generation-verification.md"] += "\nAdditional verified guidance.\n"
        after = json.loads(self.build(original))
        self.assertNotEqual(before["skill_bundle_sha256"], after["skill_bundle_sha256"])

    def test_missing_transitive_reference_fails(self):
        content = sources()
        del content["skills/safe-content-administration/references/generation-verification.md"]
        with self.assertRaisesRegex(ValueError, "Missing Markdown dependency"):
            self.build(content)

    def test_reference_definitions_bare_paths_and_encoded_escapes(self):
        entry = "skills/route-popscale-requests/SKILL.md"
        target = "skills/route-popscale-requests/references/extra.md"
        for link in ("[extra]: references/extra.md", "Read `references/extra.md`."):
            content = sources()
            content[entry] += "\n" + link
            content[target] = "See [nested](nested.md)."
            with self.assertRaisesRegex(ValueError, "Missing Markdown dependency"):
                self.build(content)
            content["skills/route-popscale-requests/references/nested.md"] = "Nested guidance."
            body = json.loads(self.build(content))
            self.assertIn(target, body["required_reference_paths"])
        for link in ("../../%2e%2e/private.md", "/private.md", "file:///private.md", "references/a.md?secret=1"):
            content = sources()
            content[entry] += f"\n[bad]({link})"
            with self.assertRaises(ValueError):
                self.build(content)

    def test_unreachable_text_excluded_and_private_paths_rejected(self):
        content = sources()
        content["skills/route-popscale-requests/references/unlinked.md"] = "Not an instruction."
        body = json.loads(self.build(content))
        self.assertNotIn("Not an instruction.", [f["content"] for f in body["files"]])
        for path in ("private/instructions.md", "skills/route-popscale-requests/host-adapter.md", "skills/../private/SKILL.md"):
            with self.assertRaisesRegex(ValueError, "Non-public skill text"):
                self.build({**sources(), path: "Do not publish"})

    def test_bounds_and_bad_provenance_fail(self):
        with self.assertRaisesRegex(ValueError, "full Git commit"):
            builder.build_bundle(sources(), "1.3.1", "latest", contract())
        for limit in ("MAX_FILE_BYTES", "MAX_BUNDLE_BYTES", "MAX_INSTRUCTION_CHARS"):
            with patch.object(builder, limit, 10), self.assertRaises(ValueError):
                self.build()

    def test_committed_checkout_provenance_and_dirty_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(PLUGIN, root / "plugins/popscale-platform")
            shutil.copytree(ROOT / "contracts", root / "contracts")
            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.DEVNULL).decode().strip()
            git("init")
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "fixture")
            body = json.loads(builder.build_from_checkout(root))
            self.assertEqual(body["skill_source_commit"], git("rev-parse", "HEAD"))
            changed = root / "plugins/popscale-platform/skills/route-popscale-requests/SKILL.md"
            changed.write_text(changed.read_text() + "\nDirty.\n")
            with self.assertRaisesRegex(ValueError, "clean committed"):
                builder.build_from_checkout(root)
            git("checkout", "--", str(changed.relative_to(root)))
            changed.unlink()
            changed.symlink_to("../../.mcp.json")
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "symlink")
            with self.assertRaisesRegex(ValueError, "Symlinks"):
                builder.build_from_checkout(root)


if __name__ == "__main__":
    unittest.main()
