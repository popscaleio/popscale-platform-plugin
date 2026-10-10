"""Policy/package regressions; host behavior is evaluated separately with fixtures."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
PLUGIN = ROOT / "plugins/popscale-platform"
REFERENCE = "skills/route-popscale-requests/references/channel-permissions.md"
SKILLS = (
    "route-popscale-requests", "safe-interview-administration",
    "safe-content-administration", "safe-journey-creation",
    "company-usage-insights", "safe-product-feedback",
)
spec = importlib.util.spec_from_file_location("channel_bundle", ROOT / "scripts/build_public_skills.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ChannelPermissionBundleTests(unittest.TestCase):
    def setUp(self):
        self.sources = {str(p.relative_to(PLUGIN)): p.read_text(encoding="utf-8")
                        for p in (PLUGIN / "skills").rglob("*.md")}
        self.contract = json.loads((ROOT / "contracts/product-tools-v1.json").read_text())
        self.policy = " ".join(self.sources[REFERENCE].split())

    def bundle(self):
        return json.loads(builder.build_bundle(self.sources, "1.6.8", "a" * 40, self.contract))

    def test_each_workflow_reaches_shared_policy_and_missing_policy_fails_closed(self):
        for name in SKILLS:
            with self.subTest(skill=name):
                visited, _ = builder.dependency_closure(self.sources, [f"skills/{name}/SKILL.md"])
                self.assertIn(REFERENCE, visited)
        body = self.bundle()
        self.assertEqual(body["instruction_paths"].count(REFERENCE), 1)
        self.assertIn(REFERENCE, body["required_reference_paths"])
        del self.sources[REFERENCE]
        with self.assertRaisesRegex(ValueError, "Missing Markdown dependency"):
            self.bundle()

    def test_docs_only_cannot_inherit_native_or_generic_action_authority(self):
        for requirement in (
            "`docs:read` never grants admin company data, Studies, people reads or",
            "generic ProductAction preparation/execution",
            "The separate public `popscale-docs` server requires no channel permission",
            "Do not require operational tools to",
            "alias is one-way",
        ):
            self.assertIn(requirement, self.policy)
        action = self.sources["skills/route-popscale-requests/references/product-actions.md"]
        self.assertIn("Documentation-only access\nnever authorizes generic action tools", action)

    def test_channels_stay_independent_and_operations_require_native_authority(self):
        for capability in (
            "mcp.external.use", "mcp.external.docs", "mcp.external.operations",
            "assistant.use", "assistant.docs", "assistant.operations",
        ):
            self.assertIn(f"`{capability}`", self.policy)
        self.assertIn("Each group requires that channel's activation permission", self.policy)
        self.assertIn("its access is independent of the external switch", self.policy)
        self.assertIn("An operations group never grants ordinary system powers", self.policy)
        self.assertIn("do not invent a public connection, browser", self.policy)
        self.assertIn("External OAuth reconnect is not an assistant recovery", self.policy)

    def test_study_discovery_description_includes_delegated_users(self):
        study = self.sources["skills/safe-interview-administration/SKILL.md"]
        frontmatter = study.split("---", 2)[1]
        description = next(line.split(":", 1)[1].strip()
                           for line in frontmatter.splitlines()
                           if line.startswith("description:"))
        self.assertIn("authorized users", description)
        self.assertIn("delegated Study readers and editors", description)
        self.assertIn("Live tool authority governs each operation", description)
        self.assertNotIn("when a company admin", description.lower())

    def test_studies_delegation_does_not_widen_editing_or_other_workflows(self):
        study = self.sources["skills/safe-interview-administration/SKILL.md"]
        fallback = self.sources["skills/safe-interview-administration/references/safety-and-fallbacks.md"]
        self.assertIn("CompanyAdmin is not\n   required when the server delegates this operation", study)
        self.assertIn("`studies.read` or\n   `studies.edit`", study)
        self.assertIn("updates require\n   `studies.edit`", study)
        self.assertIn("that scope does not authorize editing", study)
        self.assertNotIn("the user is an active `company_admin`", study)
        self.assertNotIn("scopes\nare granted only to company admins", fallback)
        self.assertIn("not a free read", self.policy)
        for name in ("safe-content-administration", "safe-journey-creation", "company-usage-insights"):
            self.assertIn("`company_admin`", self.sources[f"skills/{name}/SKILL.md"])
        self.assertIn("Structured App output can replace", self.sources[
            "skills/safe-journey-creation/references/safety-and-fallbacks.md"])

    def test_people_scope_and_permission_revocation_cannot_use_bypass_or_new_intent(self):
        for requirement in (
            "within the currently permitted units", "`status=removed/all`",
            "join stale department labels", "Revocation and uncertain effects",
            "do not replay an old preview, approval", "Keep the accepted `command_id`",
            "only if it is still allowed", "otherwise report the outcome as unknown",
            "Never issue a new command", "generic REST to bypass revocation",
        ):
            self.assertIn(requirement, self.policy)

    def test_recovery_separates_scope_rights_features_profiles_and_unknown_causes(self):
        for requirement in (
            "403 or JSON-RPC -32003", "Reconnecting cannot grant authority",
            "Missing required OAuth scopes", "after server-side authority is available",
            "Disabled company feature", "Tool excluded by the host profile, or cause unknown",
            "do not invent a missing permission", "instead of reconnecting",
        ):
            self.assertIn(requirement, self.policy)
        fallback = self.sources["skills/safe-interview-administration/references/safety-and-fallbacks.md"]
        self.assertNotIn("If a capability is unavailable or", fallback)
        self.assertIn("an unavailable capability alone does not", fallback)

    def test_shared_bundle_keeps_six_skills_and_evaluations_outside_runtime(self):
        body = self.bundle()
        self.assertEqual(body["tool_contract_version"], "popscale.product.actions.v1")
        self.assertEqual(len([p for p in body["instruction_paths"] if p.endswith("/SKILL.md")]), 6)
        self.assertFalse(any("evaluation" in p for p in body["instruction_paths"]))
        self.assertNotIn("admin_user_list", body["required_tools"])
        self.assertNotIn("admin_documentation_get", body["required_tools"])
        evaluation = (ROOT / "docs/evaluation/channel-permissions.md").read_text()
        for case in ("Rights revoked", "unit B", "CompanyAdmin", "Built-in docs-only", "studies.read", "studies.edit"):
            self.assertIn(case, evaluation)
        self.assertIn("not backend authorization tests", evaluation)

    def test_setup_and_release_retains_endpoints_versions_and_explicit_release_gate(self):
        config = json.loads((PLUGIN / ".mcp.json").read_text())
        self.assertEqual(config["mcpServers"], {
            "popscale-docs": {"type": "http", "url": "https://docs.popscale.io/mcp"},
            "popscale-platform": {"type": "http", "url": "https://app.popscale.io/mcp/"},
        })
        versions = [json.loads((PLUGIN / host / "plugin.json").read_text())["version"]
                    for host in (".codex-plugin", ".claude-plugin")]
        self.assertEqual(versions, ["1.6.8", "1.6.8"])
        readme = (PLUGIN / "README.md").read_text()
        self.assertNotIn("user is an active `company_admin` and has MCP access", readme)
        for rel in ("README.md", "SETUP.md"):
            text = (PLUGIN / rel).read_text()
            for permission in ("mcp.external.use", "assistant.use", "docs:read", "studies.edit"):
                self.assertIn(permission, text)
        release = (ROOT / "docs/RELEASE.md").read_text()
        self.assertIn("Staging verification does not prove production compatibility", release)
        self.assertIn("No release, tag", release)
        self.assertIn("Existing\nconversations retain their pinned snapshot", release)


if __name__ == "__main__":
    unittest.main()
