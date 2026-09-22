#!/usr/bin/env python3
"""Build a deterministic, text-only public skill release from committed inputs."""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import subprocess
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = "plugins/popscale-platform"
SCHEMA = "popscale.public_skills.v1"
CONTRACT = "popscale.product.actions.v1"
MAX_FILE_BYTES = 256 * 1024
MAX_BUNDLE_BYTES = 1024 * 1024
MAX_INSTRUCTION_CHARS = 200_000
SKILLS = (
    "route-popscale-requests", "safe-content-administration",
    "safe-journey-creation", "safe-interview-administration", "company-usage-insights",
    "safe-product-feedback",
)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def markdown_destinations(text):
    destinations, remaining = [], []
    def take(value):
        value = value.strip()
        if value.startswith("<") and ">" in value:
            destinations.append(value[1:value.index(">")])
        elif value:
            destinations.append(value.split(maxsplit=1)[0])
    for line in text.splitlines():
        definition = re.match(r"^[ \t]{0,3}\[[^\]\n]{1,200}\]:[ \t]*", line)
        if definition:
            take(line[definition.end():])
            continue
        cursor = 0
        while True:
            start = line.find("](", cursor)
            if start < 0:
                break
            end = line.find(")", start + 2)
            if end < 0:
                break
            label_start = line.rfind("[", cursor, start)
            remaining.append(line[cursor:label_start if label_start >= cursor else start])
            take(line[start + 2:end])
            cursor = end + 1
        remaining.append(line[cursor:])
    destinations.extend(token.rstrip(".,;:!")
                        for token in re.split(r'''[\s`<>()[\]"']+''', "\n".join(remaining))
                        if ".md" in token.lower())
    return destinations


def dependency_closure(sources, entrypoints):
    visited, required = set(), set()
    def visit(path):
        if path in visited:
            return
        if path not in sources:
            raise ValueError(f"Missing Markdown dependency: {path}")
        visited.add(path)
        for destination in markdown_destinations(sources[path]):
            parsed = urlsplit(destination)
            if parsed.scheme in ("http", "https") or not unquote(parsed.path).lower().endswith(".md"):
                continue
            target = unquote(parsed.path)
            if (parsed.scheme or parsed.netloc or parsed.query or target.startswith("/")
                    or "\\" in target or any(ord(c) < 32 for c in target)):
                raise ValueError(f"Unsafe Markdown dependency in {path}")
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
            if not resolved.startswith("skills/"):
                raise ValueError(f"Dependency escapes public skills: {path}")
            required.add(resolved)
            visit(resolved)
    for path in entrypoints:
        visit(path)
    return visited, required


def build_bundle(sources, version, commit, contract):
    """Pure builder; CLI supplies only committed public input bytes."""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Source revision must be a full Git commit")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("A stable semantic plugin version is required")
    if contract["tool_contract_version"] != CONTRACT:
        raise ValueError("Unsupported tool contract")
    for path, content in sources.items():
        parts = PurePosixPath(path).parts
        if (not path.startswith("skills/") or "\\" in path or
                any(p in ("", ".", "..") for p in path.split("/")) or
                len(parts) < 3 or parts[1] not in SKILLS or
                not (path.endswith("/SKILL.md") or (len(parts) == 4 and parts[2] == "references" and path.endswith(".md")))):
            raise ValueError(f"Non-public skill text path: {path}")
        if len(content.encode("utf-8")) > MAX_FILE_BYTES:
            raise ValueError(f"Oversized file: {path}")
    entrypoints = [f"skills/{name}/SKILL.md" for name in SKILLS]
    visited, references = dependency_closure(sources, entrypoints)
    # Include only text reachable from a skill entrypoint, never unrelated local files.
    paths = entrypoints + sorted(visited - set(entrypoints))
    if len("\n\n".join(sources[path] for path in paths)) > MAX_INSTRUCTION_CHARS:
        raise ValueError("Instructions exceed the consumer bound")
    known_tools = set(contract["product_tools"])
    if not known_tools or any(not re.fullmatch(r"[a-z][a-z0-9_]{0,159}", name) for name in known_tools):
        raise ValueError("Invalid product tool names")
    mentioned = set(re.findall(r"`([a-z][a-z0-9_]+)`", "\n".join(sources[p] for p in paths)))
    required_tools = sorted(known_tools & mentioned)
    if not {"current_user", "capabilities", "product_action_prepare", "product_action_get", "product_action_execute"}.issubset(required_tools):
        raise ValueError("Missing common product action contract")
    files = [{"path": p, "sha256": hashlib.sha256(sources[p].encode("utf-8")).hexdigest(), "content": sources[p]} for p in sorted(visited)]
    identity = [{"path": f["path"], "sha256": f["sha256"]} for f in files]
    body = {"schema_version": SCHEMA, "plugin_version": version,
            "skill_source_commit": commit, "tool_contract_version": CONTRACT,
            "required_tools": required_tools, "files": files,
            "instruction_paths": paths, "required_reference_paths": sorted(references),
            "skill_bundle_sha256": hashlib.sha256(canonical(identity)).hexdigest()}
    raw = canonical(body) + b"\n"
    if len(raw) > MAX_BUNDLE_BYTES:
        raise ValueError("Bundle exceeds the consumer bound")
    return raw


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)


def build_from_checkout(root=ROOT):
    commit = git(root, "rev-parse", "HEAD").decode().strip()
    # A release's provenance is the exact checkout, not a caller-supplied SHA.
    if git(root, "status", "--porcelain", "--untracked-files=all").strip():
        raise ValueError("Build from a clean committed checkout")
    entries = git(root, "ls-tree", "-r", "-z", commit, "--", f"{PLUGIN}/skills").split(b"\0")
    sources = {}
    for entry in entries:
        if not entry:
            continue
        metadata, encoded_path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        path = encoded_path.decode()
        if mode == "120000":
            raise ValueError("Symlinks cannot be packaged")
        relative = path[len(PLUGIN) + 1:]
        if not relative.endswith(".md"):
            continue
        if mode not in {"100644", "100755"} or kind != "blob":
            raise ValueError("Only regular public text files can be packaged")
        sources[relative] = git(root, "cat-file", "blob", oid).decode("utf-8")
    def read_json(path):
        return json.loads(git(root, "show", f"{commit}:{path}"))
    version = read_json(f"{PLUGIN}/.codex-plugin/plugin.json")["version"]
    contract = read_json("contracts/product-tools-v1.json")
    return build_bundle(sources, version, commit, contract)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    raw = build_from_checkout()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "public-skills.json").write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    (args.output_dir / "public-skills.sha256").write_text(digest + "\n", encoding="ascii")
    print(f"Built public-skills.json ({len(raw)} bytes), sha256={digest}")


if __name__ == "__main__":
    main()
