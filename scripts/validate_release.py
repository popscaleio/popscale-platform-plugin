#!/usr/bin/env python3
"""Validate the public plugin package without network access."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "popscale-platform"
EXPECTED_VERSION = "1.2.0"
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
    PLUGIN / "assets" / "icon.png",
    PLUGIN / "skills" / "route-popscale-requests" / "SKILL.md",
    PLUGIN / "skills" / "company-usage-insights" / "SKILL.md",
    PLUGIN / "skills" / "safe-content-administration" / "SKILL.md",
    PLUGIN / "skills" / "safe-interview-administration" / "SKILL.md",
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


def release_paths() -> list[Path]:
    """Return tracked and non-ignored untracked files that could enter a release."""
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def main(tag: str | None = None) -> int:
    for path in REQUIRED_FILES:
        if not path.is_file():
            fail(f"Required file is missing: {path.relative_to(ROOT)}")

    package_paths = release_paths()
    for path in package_paths:
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
    if tag is not None and tag != f"v{EXPECTED_VERSION}":
        fail(f"Release tag {tag!r} does not match plugin version v{EXPECTED_VERSION}")

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

    interface = codex["interface"]
    if interface.get("brandColor") != "#4B1693":
        fail("Codex manifest brand color mismatch")
    for field in ("composerIcon", "logo"):
        if interface.get(field) != "./assets/icon.png":
            fail(f"Codex manifest {field} must reference the packaged icon")
    icon = PLUGIN / "assets" / "icon.png"
    icon_bytes = icon.read_bytes()
    if icon_bytes[:8] != b"\x89PNG\r\n\x1a\n":
        fail("Packaged icon is not a PNG file")
    dimensions = (
        int.from_bytes(icon_bytes[16:20], "big"),
        int.from_bytes(icon_bytes[20:24], "big"),
    )
    if dimensions != (512, 512):
        fail(f"Packaged icon must be 512x512 pixels, got {dimensions[0]}x{dimensions[1]}")
    if icon_bytes[25] not in {4, 6}:
        fail("Packaged icon must include an alpha channel")

    if "apps" in codex or (PLUGIN / ".app.json").exists():
        fail("Do not ship a placeholder app mapping before host registration")

    for path in package_paths:
        if not path.is_file():
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", help="Require this release tag to match v<manifest version>")
    args = parser.parse_args()
    try:
        raise SystemExit(main(tag=args.tag))
    except (AssertionError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"release validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
