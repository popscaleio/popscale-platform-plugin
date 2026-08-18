#!/usr/bin/env python3
"""Validate the public plugin package without network access."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "popscale-platform"
EXPECTED_VERSION = "1.0.0"
EXPECTED_SERVERS = {
    "popscale-platform": {"type": "http", "url": "https://app.popscale.io/mcp/"},
    "popscale-docs": {"type": "http", "url": "https://docs.popscale.io/mcp"},
}
REQUIRED_FILES = (
    ROOT / ".agents" / "plugins" / "marketplace.json",
    ROOT / ".claude-plugin" / "marketplace.json",
    PLUGIN / ".codex-plugin" / "plugin.json",
    PLUGIN / ".claude-plugin" / "plugin.json",
    PLUGIN / ".mcp.json",
    PLUGIN / "skills" / "route-popscale-requests" / "SKILL.md",
    PLUGIN / "skills" / "safe-journey-creation" / "SKILL.md",
    ROOT / "SECURITY.md",
    ROOT / "LICENSE",
    ROOT / "CHANGELOG.md",
)
FORBIDDEN_NAMES = {".env", ".env.local", "id_rsa", "id_ed25519"}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    for path in REQUIRED_FILES:
        if not path.is_file():
            fail(f"Required file is missing: {path.relative_to(ROOT)}")

    for path in ROOT.rglob("*"):
        if path.is_symlink():
            fail(f"Symlinks are not allowed in the public package: {path.relative_to(ROOT)}")
        if path.is_file() and path.name in FORBIDDEN_NAMES:
            fail(f"Forbidden credential file: {path.relative_to(ROOT)}")

    codex = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
    claude = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
    claude_marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    codex_marketplace = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    versions = {codex["version"], claude["version"], claude_marketplace["version"]}
    if versions != {EXPECTED_VERSION}:
        fail(f"Release versions diverge: {sorted(versions)}")

    mcp = load_json(PLUGIN / ".mcp.json")
    if mcp != {"mcpServers": EXPECTED_SERVERS}:
        fail(".mcp.json does not contain the exact production server contract")
    docs = mcp["mcpServers"]["popscale-docs"]
    if set(docs) != {"type", "url"}:
        fail("The public docs server must not include auth or secret configuration")

    codex_entry = codex_marketplace["plugins"][0]
    if codex_entry["source"] != {"source": "local", "path": "./plugins/popscale-platform"}:
        fail("Codex marketplace source is not the shared plugin root")
    if codex_entry["policy"] != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
        fail("Codex marketplace policy is incomplete")
    if claude_marketplace["plugins"][0]["source"] != "./plugins/popscale-platform":
        fail("Claude marketplace source is not the shared plugin root")

    for manifest in (codex, claude):
        if manifest["name"] != "popscale-platform":
            fail("Host manifest name mismatch")
        if manifest.get("repository") != "https://github.com/popscaleio/popscale-platform-plugin":
            fail("Host manifest repository metadata mismatch")
        if manifest.get("license") != "MIT":
            fail("Host manifest license metadata mismatch")

    if "apps" in codex or (PLUGIN / ".app.json").exists():
        fail("Do not ship a placeholder app mapping before host registration")

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".json", ".yaml", ".yml", ".py"}:
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"Possible secret in {path.relative_to(ROOT)}")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## [{EXPECTED_VERSION}]" not in changelog:
        fail("CHANGELOG.md has no entry for the release version")

    print(f"Validated Popscale Platform plugin {EXPECTED_VERSION}")
    print("Validated 2 host manifests, 2 marketplaces, 2 MCP servers, and 0 secrets")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(f"release validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
