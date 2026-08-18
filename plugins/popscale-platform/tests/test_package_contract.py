import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parents[1]
EXPECTED_VERSION = "1.0.1"
EXPECTED_SERVERS = {
    "popscale-platform": {
        "type": "http",
        "url": "https://app.popscale.io/mcp/",
    },
    "popscale-docs": {
        "type": "http",
        "url": "https://docs.popscale.io/mcp",
    },
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class PluginPackageContractTests(unittest.TestCase):
    def test_shared_mcp_config_has_exact_public_and_product_servers(self):
        config = load_json(PLUGIN_ROOT / ".mcp.json")
        self.assertEqual(config, {"mcpServers": EXPECTED_SERVERS})

    def test_docs_server_has_no_auth_or_secret_configuration(self):
        docs = load_json(PLUGIN_ROOT / ".mcp.json")["mcpServers"]["popscale-docs"]
        self.assertEqual(set(docs), {"type", "url"})
        serialized = json.dumps(docs).lower()
        for forbidden in ("auth", "token", "secret", "header", "env"):
            self.assertNotIn(forbidden, serialized)

    def test_host_manifest_and_marketplace_versions_are_aligned(self):
        codex = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
        claude = load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")
        claude_marketplace = load_json(REPO_ROOT / ".claude-plugin" / "marketplace.json")
        self.assertEqual(
            {codex["version"], claude["version"], claude_marketplace["version"]},
            {EXPECTED_VERSION},
        )

    def test_both_marketplaces_resolve_the_same_plugin_root(self):
        codex_marketplace = load_json(REPO_ROOT / ".agents" / "plugins" / "marketplace.json")
        claude_marketplace = load_json(REPO_ROOT / ".claude-plugin" / "marketplace.json")
        codex_entry = codex_marketplace["plugins"][0]
        claude_entry = claude_marketplace["plugins"][0]
        self.assertEqual(codex_marketplace["name"], "popscale")
        self.assertEqual(claude_marketplace["name"], "popscale")
        self.assertEqual(codex_entry["name"], "popscale-platform")
        self.assertEqual(claude_entry["name"], "popscale-platform")
        self.assertEqual(codex_entry["source"]["path"], "./plugins/popscale-platform")
        self.assertEqual(claude_entry["source"], "./plugins/popscale-platform")
        self.assertEqual(
            codex_entry["policy"],
            {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        )

    def test_codex_manifest_discovers_shared_servers_and_skills(self):
        codex = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
        self.assertEqual(codex["mcpServers"], "./.mcp.json")
        self.assertEqual(codex["skills"], "./skills/")
        self.assertEqual(codex["repository"], "https://github.com/popscaleio/popscale-platform-plugin")
        self.assertEqual(codex["license"], "MIT")
        self.assertLessEqual(len(codex["interface"]["defaultPrompt"]), 3)
        for prompt in codex["interface"]["defaultPrompt"]:
            self.assertLessEqual(len(prompt), 128)

    def test_codex_manifest_packages_popscale_logo(self):
        codex = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
        interface = codex["interface"]
        self.assertEqual(interface["brandColor"], "#4B1693")
        self.assertEqual(interface["composerIcon"], "./assets/icon.png")
        self.assertEqual(interface["logo"], "./assets/icon.png")

        icon = PLUGIN_ROOT / "assets" / "icon.png"
        self.assertTrue(icon.is_file())
        self.assertGreater(icon.stat().st_size, 1024)
        icon_bytes = icon.read_bytes()
        self.assertEqual(icon_bytes[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(
            (
                int.from_bytes(icon_bytes[16:20], "big"),
                int.from_bytes(icon_bytes[20:24], "big"),
            ),
            (512, 512),
        )
        self.assertIn(icon_bytes[25], {4, 6})

    def test_claude_manifest_has_public_release_metadata(self):
        claude = load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")
        self.assertEqual(claude["repository"], "https://github.com/popscaleio/popscale-platform-plugin")
        self.assertEqual(claude["license"], "MIT")
        self.assertTrue((PLUGIN_ROOT / ".mcp.json").is_file())
        self.assertTrue((PLUGIN_ROOT / "skills").is_dir())

    def test_routing_skill_enforces_public_private_boundary(self):
        skill_root = PLUGIN_ROOT / "skills" / "route-popscale-requests"
        skill = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        metadata = (skill_root / "agents" / "openai.yaml").read_text(encoding="utf-8")
        for required in (
            "get_docs_overview",
            "search_docs",
            "get_pages",
            "status",
            "draft",
            "review",
            "Never send customer",
            "Never use `popscale-docs` for a write",
            "safe-journey-creation",
        ):
            self.assertIn(required, skill)
        self.assertNotIn("[TODO:", skill)
        self.assertIn('value: "popscale-docs"', metadata)
        self.assertIn('url: "https://docs.popscale.io/mcp"', metadata)
        self.assertIn('value: "popscale-platform"', metadata)
        self.assertIn('url: "https://app.popscale.io/mcp/"', metadata)

    def test_safe_journey_skill_remains_product_only(self):
        safe_root = PLUGIN_ROOT / "skills" / "safe-journey-creation"
        safe_skill = (safe_root / "SKILL.md").read_text(encoding="utf-8")
        safe_metadata = (safe_root / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertNotIn("popscale-docs", safe_skill)
        self.assertNotIn("popscale-docs", safe_metadata)
        self.assertIn('value: "popscale-platform"', safe_metadata)

    def test_public_docs_name_endpoints_auth_and_maintenance_boundary(self):
        docs = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                REPO_ROOT / "README.md",
                REPO_ROOT / "docs" / "INSTALLATION.md",
                REPO_ROOT / "docs" / "RELEASE.md",
                PLUGIN_ROOT / "README.md",
                PLUGIN_ROOT / "SETUP.md",
            )
        )
        self.assertIn("https://docs.popscale.io/mcp", docs)
        self.assertIn("https://app.popscale.io/mcp/", docs)
        self.assertIn("read-only", docs)
        self.assertIn("OAuth", docs)
        lowered_docs = docs.lower()
        self.assertIn("maintenance mode", lowered_docs)
        self.assertIn("no database", lowered_docs)

    def test_release_workflow_binds_tag_to_manifest_version(self):
        workflow = (REPO_ROOT / ".github" / "workflows" / "release.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn('validate_release.py --tag "$GITHUB_REF_NAME"', workflow)

    def test_claude_shell_login_uses_plugin_server_namespace(self):
        installation = (REPO_ROOT / "docs" / "INSTALLATION.md").read_text(encoding="utf-8")
        self.assertIn(
            "claude mcp login plugin:popscale-platform:popscale-platform",
            installation,
        )

    def test_safe_journey_discovers_existing_generation_requests(self):
        workflow = (
            PLUGIN_ROOT
            / "skills"
            / "safe-journey-creation"
            / "references"
            / "tool-workflow.md"
        ).read_text(encoding="utf-8")
        self.assertIn("generation_requests_list", workflow)
        self.assertEqual(workflow.count("`generation_request_detail`"), 1)

    def test_no_placeholder_app_mapping_is_shipped(self):
        self.assertFalse((PLUGIN_ROOT / ".app.json").exists())
        codex = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
        self.assertNotIn("apps", codex)


if __name__ == "__main__":
    unittest.main()
