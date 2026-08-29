import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parents[1]
EXPECTED_VERSION = "1.3.0"
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
EXPECTED_INTERVIEW_TOOLS = (
    "list_interview_studies",
    "get_interview_study",
    "ensure_interview_study_draft",
    "create_interview_study",
    "update_interview_study",
    "update_interview_draft",
    "create_interview_topic",
    "update_interview_topic",
    "delete_interview_topic",
    "reorder_interview_topics",
    "upsert_interview_localization",
    "delete_interview_localization",
    "generate_interview_localizations",
    "get_interview_publish_readiness",
    "publish_interview_study",
    "list_interview_invites",
    "get_interview_invite",
    "create_interview_invite",
    "create_interview_invites_bulk",
    "send_interview_invite_email",
    "revoke_interview_invite",
    "expire_interview_invite",
    "list_interview_runs",
    "get_interview_run_review",
    "list_interview_analyses",
    "preview_interview_analysis",
    "generate_interview_analysis",
    "get_interview_analysis",
    "retry_interview_analysis",
    "update_interview_run_action_status",
    "update_interview_analysis_action_status",
)
EXPECTED_CONTENT_TOOLS = (
    "search_company_content",
    "create_company_content",
    "list_company_content_references",
    "list_content_components",
    "get_content_component",
    "create_content_component",
    "update_content_component",
    "delete_content_component",
    "reorder_content_components",
    "set_content_departments",
    "archive_company_content",
    "get_content_usage",
    "list_content_history",
    "get_content_freshness",
    "content_detail",
    "content_update",
    "content_generation_capabilities",
    "content_language_generate",
    "content_regenerate_subparts",
    "content_activation_readiness",
    "content_activate",
)
EXPECTED_USAGE_TOOLS = (
    "get_journey_insights",
    "list_journey_members",
    "get_member_journey",
    "get_content_outcomes",
    "list_content_attempts",
)


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
            "safe-interview-administration",
            "safe-content-administration",
            "company-usage-insights",
            "request_company_switch",
            "current_grant_id",
            "confirm_switch=true",
        ):
            self.assertIn(required, skill)
        self.assertNotIn("[TODO:", skill)
        self.assertIn('value: "popscale-docs"', metadata)
        self.assertIn('url: "https://docs.popscale.io/mcp"', metadata)
        self.assertIn('value: "popscale-platform"', metadata)
        self.assertIn('url: "https://app.popscale.io/mcp/"', metadata)

    def test_company_switch_guidance_matches_product_contract(self):
        switch_paths = (
            PLUGIN_ROOT / "skills" / "route-popscale-requests" / "SKILL.md",
            PLUGIN_ROOT
            / "skills"
            / "safe-journey-creation"
            / "references"
            / "safety-and-fallbacks.md",
            PLUGIN_ROOT
            / "skills"
            / "safe-interview-administration"
            / "references"
            / "safety-and-fallbacks.md",
            PLUGIN_ROOT
            / "skills"
            / "safe-content-administration"
            / "references"
            / "safety-and-fallbacks.md",
            PLUGIN_ROOT
            / "skills"
            / "company-usage-insights"
            / "references"
            / "privacy-and-limits.md",
            PLUGIN_ROOT / "SETUP.md",
            REPO_ROOT / "docs" / "INSTALLATION.md",
            REPO_ROOT / "docs" / "SECURITY_MODEL.md",
        )
        guidance = "\n".join(
            path.read_text(encoding="utf-8") for path in switch_paths
        )
        for required in (
            "request_company_switch",
            "current_grant_id",
            "confirm_switch=true",
            "switch_url",
            "current_user",
            "same MCP connection",
            "replay_ignored=true",
            "reauthentication_required=false",
        ):
            self.assertIn(required, guidance)
        self.assertNotIn("reconnect to Company B", guidance)
        self.assertNotIn("reconnect/select Company B", guidance)

    def test_company_switch_evaluations_cover_confirmation_and_safe_replay(self):
        evaluations = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                PLUGIN_ROOT
                / "skills"
                / "route-popscale-requests"
                / "references"
                / "evaluation-scenarios.md",
                PLUGIN_ROOT
                / "skills"
                / "safe-journey-creation"
                / "references"
                / "evaluation-scenarios.md",
            )
        )
        for required in (
            "Authenticated Company Switch",
            "Declined or Stale Company Switch",
            "Declined, Replayed, or Expired Company Switch",
            "explicit confirmation",
            "confirm_switch=true",
            "replay_ignored=true",
            "expired or used link",
        ):
            self.assertIn(required, evaluations)

    def test_usage_skill_covers_tools_privacy_bounds_and_metric_contract(self):
        skill_root = PLUGIN_ROOT / "skills" / "company-usage-insights"
        skill = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        metadata = (skill_root / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        workflow = (skill_root / "references" / "tool-workflow.md").read_text(
            encoding="utf-8"
        )
        metrics = (skill_root / "references" / "metric-semantics.md").read_text(
            encoding="utf-8"
        )
        privacy = (skill_root / "references" / "privacy-and-limits.md").read_text(
            encoding="utf-8"
        )
        evaluations = (
            skill_root / "references" / "evaluation-scenarios.md"
        ).read_text(encoding="utf-8")

        for required in (
            "current_user",
            "capabilities",
            "usage:read",
            "OAuth-selected company",
            "suppressed",
            "score_contract",
            "historical_score_notice",
            "get_content_usage",
            "search_company_content",
            "server-returned ID/link",
            "366-day",
            "20,000",
        ):
            self.assertIn(required, skill)
        for required_tool in EXPECTED_USAGE_TOOLS:
            self.assertIn(required_tool, workflow)
        for required_semantic in (
            "current-state view",
            "current stored values",
            "removed or inactive customer-human memberships",
            "support and service identities",
            "Roleplay and Coaching history",
            "Flashcard sessions",
            "Legacy attempts",
            "Challenge pass/no-pass",
        ):
            self.assertIn(required_semantic, metrics)
        for required_boundary in (
            "Never:",
            "subtract visible groups",
            "email",
            "20,000-attempt",
            "different company",
        ):
            self.assertIn(required_boundary, privacy)
        for required_scenario in (
            "Department Journey Completion",
            "Department-manager Roleplay Outcomes",
            "Explicit Member Drilldown",
            "Missing Usage Scope",
            "Title-only Resolution With Usage-only Grant",
            "Wrong Company or Prompt-supplied Company ID",
            "Suppressed Small Cohort",
            "Bounded Window, Pagination, and Row Guard",
            "Historical Roleplay and Coaching Scores",
            "Flashcard and Legacy Episode History",
            "Current Organization Dimensions",
        ):
            self.assertIn(required_scenario, evaluations)
        self.assertNotIn("popscale-docs", metadata)
        self.assertIn('value: "popscale-platform"', metadata)
        self.assertIn('url: "https://app.popscale.io/mcp/"', metadata)
        self.assertIn("only when the user explicitly asks", skill)
        self.assertIn("is not consent", skill)
        self.assertIn("is not consent to drill down", privacy)

    def test_manifest_advertises_company_usage_insights(self):
        codex = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
        claude = load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")
        marketplace = load_json(REPO_ROOT / ".claude-plugin" / "marketplace.json")
        for manifest in (codex, claude, marketplace["plugins"][0]):
            self.assertIn("learning-analytics", manifest["keywords"])
            self.assertIn("journey-insights", manifest["keywords"])
            self.assertIn("usage", manifest["description"].lower())
        self.assertTrue(
            any("outcomes" in prompt.lower() for prompt in codex["interface"]["defaultPrompt"])
        )

    def test_content_skill_covers_granular_tools_formats_and_safety_contract(self):
        skill_root = PLUGIN_ROOT / "skills" / "safe-content-administration"
        skill = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        metadata = (skill_root / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        workflow = (skill_root / "references" / "tool-workflow.md").read_text(
            encoding="utf-8"
        )
        formats = (skill_root / "references" / "content-format-map.md").read_text(
            encoding="utf-8"
        )
        evaluations = (
            skill_root / "references" / "evaluation-scenarios.md"
        ).read_text(encoding="utf-8")

        for required in (
            "current_user",
            "capabilities",
            "expected_revision",
            "confirm_active_edit=true",
            "confirm_publish=true",
            "content:read",
            "content:write",
            "generation:read",
            "generation:write",
            "publish:write",
            "Never send customer content",
        ):
            self.assertIn(required, skill)
        for required_tool in EXPECTED_CONTENT_TOOLS:
            self.assertIn(required_tool, workflow)
        for required_format in (
            "`roleplay`",
            "`coaching_session`",
            "`challenge`",
            "`episode`",
            "`flashcard_deck`",
            "`journey`",
            "roleplay_customer_question",
            "episode_script_variant",
            "flashcard_translation",
            "journey_item",
        ):
            self.assertIn(required_format, formats)
        for required_scenario in (
            "One roleplay question",
            "Stale edit conflict",
            "Active content confirmation",
            "Active Content Archive",
            "Truncated Dependency Usage",
            "Episode language and audio",
            "Existing Journey item",
            "Wrong company and superuser acting context",
            "Publication boundary",
        ):
            self.assertIn(required_scenario, evaluations)
        self.assertNotIn("popscale-docs", metadata)
        self.assertIn('value: "popscale-platform"', metadata)
        self.assertIn('url: "https://app.popscale.io/mcp/"', metadata)
        self.assertIn("does not accept `confirm_active_edit`", skill)
        self.assertIn("does not send `confirm_active_edit`", evaluations)
        self.assertIn("server maximum of 100", skill)
        self.assertIn("If the retry remains", skill)
        self.assertIn("if the retry is still truncated", workflow)
        self.assertIn("retries once with a sufficient `limit` capped at 100", evaluations)
        self.assertIn("exposes no such inputs", evaluations)

    def test_manifest_advertises_company_content_administration(self):
        codex = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
        claude = load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")
        marketplace = load_json(REPO_ROOT / ".claude-plugin" / "marketplace.json")
        for manifest in (codex, claude, marketplace["plugins"][0]):
            self.assertIn("content-authoring", manifest["keywords"])
            self.assertIn("roleplays", manifest["keywords"])
            self.assertIn("episodes", manifest["keywords"])
            self.assertIn("flashcards", manifest["keywords"])
            self.assertIn("content", manifest["description"].lower())
        self.assertTrue(
            any("roleplay" in prompt.lower() for prompt in codex["interface"]["defaultPrompt"])
        )

    def test_interview_skill_is_product_only_and_preserves_safety_contract(self):
        skill_root = PLUGIN_ROOT / "skills" / "safe-interview-administration"
        skill = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        metadata = (skill_root / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        workflow = (skill_root / "references" / "tool-workflow.md").read_text(
            encoding="utf-8"
        )
        evaluations = (
            skill_root / "references" / "evaluation-scenarios.md"
        ).read_text(encoding="utf-8")

        for required in (
            "current_user",
            "capabilities",
            "expected_updated_at",
            "confirm_publish=true",
            "confirm_send=true",
            "interview:read",
            "interview:write",
            "interview:distribute",
            "publish:write",
            "500",
            "Never send Interview data",
        ):
            self.assertIn(required, skill)
        for required_tool in EXPECTED_INTERVIEW_TOOLS:
            self.assertIn(required_tool, workflow)
        for required_scenario in (
            "Stale edit conflict",
            "Read-only grant and respondent link",
            "Oversized delivery batch",
            "Publish boundary",
            "Bounded evidence review",
            "Wrong company",
        ):
            self.assertIn(required_scenario, evaluations)
        self.assertNotIn("popscale-docs", metadata)
        self.assertIn('value: "popscale-platform"', metadata)
        self.assertIn('url: "https://app.popscale.io/mcp/"', metadata)

    def test_manifest_advertises_interview_admin_capability(self):
        codex = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
        claude = load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")
        marketplace = load_json(REPO_ROOT / ".claude-plugin" / "marketplace.json")
        self.assertIn("interviews", codex["keywords"])
        self.assertIn("interviews", claude["keywords"])
        self.assertIn("interviews", marketplace["plugins"][0]["keywords"])
        self.assertIn("interview", codex["description"].lower())
        self.assertIn("interview", claude["description"].lower())
        self.assertTrue(
            any("interview" in prompt.lower() for prompt in codex["interface"]["defaultPrompt"])
        )

    def test_interview_oauth_guidance_requires_reauthorization_and_scopes(self):
        docs = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                REPO_ROOT / "docs" / "INSTALLATION.md",
                REPO_ROOT / "docs" / "SECURITY_MODEL.md",
                PLUGIN_ROOT / "README.md",
                PLUGIN_ROOT / "SETUP.md",
            )
        )
        for required in (
            "interview:read",
            "interview:write",
            "interview:distribute",
            "publish:write",
        ):
            self.assertIn(required, docs)
        self.assertIn("not silently", docs)
        self.assertIn("respondent", docs.lower())

    def test_content_oauth_guidance_requires_granular_scopes(self):
        docs = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                REPO_ROOT / "docs" / "INSTALLATION.md",
                REPO_ROOT / "docs" / "SECURITY_MODEL.md",
                PLUGIN_ROOT / "README.md",
                PLUGIN_ROOT / "SETUP.md",
            )
        )
        for required in (
            "content:read",
            "content:write",
            "generation:read",
            "generation:write",
            "publish:write",
        ):
            self.assertIn(required, docs)
        self.assertIn("not silently", docs)
        self.assertIn("expected_revision", docs)
        self.assertIn("confirm_active_edit", docs)

    def test_usage_oauth_guidance_requires_scope_and_privacy_boundaries(self):
        docs = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                REPO_ROOT / "docs" / "INSTALLATION.md",
                REPO_ROOT / "docs" / "SECURITY_MODEL.md",
                PLUGIN_ROOT / "README.md",
                PLUGIN_ROOT / "SETUP.md",
            )
        )
        self.assertIn("usage:read", docs)
        self.assertIn("not silently", docs)
        self.assertIn("small-cohort", docs.lower())
        self.assertIn("membership", docs.lower())
        self.assertIn("transcript", docs.lower())

    def test_safe_journey_skill_remains_product_only(self):
        safe_root = PLUGIN_ROOT / "skills" / "safe-journey-creation"
        safe_skill = (safe_root / "SKILL.md").read_text(encoding="utf-8")
        safe_metadata = (safe_root / "agents" / "openai.yaml").read_text(encoding="utf-8")
        workflow = (safe_root / "references" / "tool-workflow.md").read_text(
            encoding="utf-8"
        )
        evaluations = (
            safe_root / "references" / "evaluation-scenarios.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("popscale-docs", safe_skill)
        self.assertNotIn("popscale-docs", safe_metadata)
        self.assertIn('value: "popscale-platform"', safe_metadata)
        self.assertIn("content:read", safe_skill)
        for required_scope in ("content:read", "content:write", "publish:write"):
            self.assertIn(required_scope, workflow)
        self.assertIn("Missing Child-content Read Scope", evaluations)
        self.assertIn("request_company_switch", safe_skill)
        self.assertIn("confirm_switch=true", safe_skill)

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
