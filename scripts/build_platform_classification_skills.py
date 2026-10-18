#!/usr/bin/env python3
"""Separate exact-36 public method asset; never replaces public-skills.json."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import re
from build_public_skills import (ROOT, PLUGIN, SCHEMA, CONTRACT, SKILLS, MAX_FILE_BYTES,
    MAX_BUNDLE_BYTES, MAX_INSTRUCTION_CHARS, canonical, dependency_closure, git)

DOMAIN_OPERATIONS = frozenset(['cancel_interview_classification_job', 'cancel_interview_dataset_job', 'create_interview_analysis', 'get_interview_analysis_budget', 'get_interview_analysis_capabilities', 'get_interview_analysis_context', 'get_interview_analysis_revision', 'get_interview_analysis_study', 'get_interview_classification_definition', 'get_interview_classification_job', 'get_interview_classification_plan', 'get_interview_classification_post_review', 'get_interview_classification_review', 'get_interview_dataset', 'get_interview_dataset_artifact', 'get_interview_dataset_job', 'list_interview_analysis_studies', 'list_interview_classification_corrections', 'list_interview_classification_definitions', 'list_interview_classification_jobs', 'prepare_interview_classification', 'prepare_interview_classification_review', 'prepare_interview_dataset', 'read_interview_classification_results', 'read_interview_dataset_page', 'save_interview_analysis_revision', 'save_interview_classification_correction', 'save_interview_classification_review', 'save_interview_dataset', 'set_interview_analysis_budget', 'start_interview_classification'])
CONTROL_TOOLS = frozenset(['capabilities', 'current_user', 'product_action_execute', 'product_action_get', 'product_action_prepare'])
ENTRYPOINT = "skills/safe-interview-administration/references/platform-classification-analysis.md"
EXPECTED = {'schema_version': 'popscale.studies.platform-classification-plugin.v1', 'tool_contract_version': 'popscale.product.actions.v1', 'profile': 'studies_classification_runtime_v1', 'protocol_revision': 'studies.classification-runtime.v1', 'operation_ids': ['cancel_interview_classification_job', 'cancel_interview_dataset_job', 'create_interview_analysis', 'get_interview_analysis_budget', 'get_interview_analysis_capabilities', 'get_interview_analysis_context', 'get_interview_analysis_revision', 'get_interview_analysis_study', 'get_interview_classification_definition', 'get_interview_classification_job', 'get_interview_classification_plan', 'get_interview_classification_post_review', 'get_interview_classification_review', 'get_interview_dataset', 'get_interview_dataset_artifact', 'get_interview_dataset_job', 'list_interview_analysis_studies', 'list_interview_classification_corrections', 'list_interview_classification_definitions', 'list_interview_classification_jobs', 'prepare_interview_classification', 'prepare_interview_classification_review', 'prepare_interview_dataset', 'read_interview_classification_results', 'read_interview_dataset_page', 'save_interview_analysis_revision', 'save_interview_classification_correction', 'save_interview_classification_review', 'save_interview_dataset', 'set_interview_analysis_budget', 'start_interview_classification'], 'control_tools': ['capabilities', 'current_user', 'product_action_execute', 'product_action_get', 'product_action_prepare'], 'entrypoint': 'skills/safe-interview-administration/references/platform-classification-analysis.md'}


def build_platform_classification_bundle(sources, version, commit, extension):
    if (type(extension) is not dict or extension != EXPECTED
            or type(extension.get("operation_ids")) is not list
            or type(extension.get("control_tools")) is not list):
        raise ValueError("Exact separately reviewed 31+5 platform contract is required")
    if (type(version) is not str or re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version) is None
            or type(commit) is not str or re.fullmatch(r"[0-9a-f]{40}", commit) is None):
        raise ValueError("Committed stable public provenance is required")
    visited, references = dependency_closure(sources, [ENTRYPOINT])
    if len(visited) > 256:
        raise ValueError("Too many public method files")
    paths = [ENTRYPOINT] + sorted(visited - {ENTRYPOINT})
    for name in paths:
        parts = PurePosixPath(name).parts
        text = sources[name]
        if (not name.startswith("skills/") or "\\" in name or len(name) > 512
                or any(char in name for char in ("%", "?", "#", ":"))
                or any(ord(char) < 32 for char in name)
                or any(part in ("", ".", "..") for part in name.split("/"))
                or len(parts) != 4 or parts[1] not in SKILLS or parts[2] != "references"
                or not name.endswith(".md") or type(text) is not str
                or len(text.encode("utf-8")) > MAX_FILE_BYTES):
            raise ValueError("Only bounded public method references are eligible")
    instructions = "\n\n".join(sources[name] for name in paths)
    if not instructions.strip() or len(instructions) > MAX_INSTRUCTION_CHARS:
        raise ValueError("Public instructions exceed the consumer bound")
    tools = DOMAIN_OPERATIONS | CONTROL_TOOLS
    mentioned = set(re.findall(r"`([a-z][a-z0-9_]+)`", instructions))
    if not tools.issubset(mentioned) or len(tools) != 36:
        raise ValueError("Every exact platform tool must have a public method")
    files = [{"path": name, "sha256": hashlib.sha256(sources[name].encode("utf-8")).hexdigest(),
              "content": sources[name]} for name in sorted(visited)]
    identity = [{"path": row["path"], "sha256": row["sha256"]} for row in files]
    body = {"schema_version": SCHEMA, "plugin_version": version, "skill_source_commit": commit,
            "tool_contract_version": CONTRACT, "required_tools": sorted(tools), "files": files,
            "instruction_paths": paths, "required_reference_paths": sorted(references),
            "skill_bundle_sha256": hashlib.sha256(canonical(identity)).hexdigest()}
    raw = canonical(body) + b"\n"
    if len(raw) > MAX_BUNDLE_BYTES:
        raise ValueError("Public method asset exceeds the consumer bound")
    return raw


def build_from_checkout(root=ROOT):
    root = Path(root)
    commit = git(root, "rev-parse", "HEAD").decode().strip()
    if git(root, "status", "--porcelain", "--untracked-files=all").strip():
        raise ValueError("Build from a clean committed checkout")
    sources = {}
    entries = git(root, "ls-tree", "-r", "-z", commit, "--", f"{PLUGIN}/skills").split(b"\0")
    for entry in entries:
        if not entry:
            continue
        metadata, encoded_path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        relative = encoded_path.decode()[len(PLUGIN) + 1:]
        if mode == "120000":
            raise ValueError("Symlinks cannot be packaged")
        if not relative.endswith(".md"):
            continue
        if mode not in {"100644", "100755"} or kind != "blob":
            raise ValueError("Only committed public Markdown is eligible")
        sources[relative] = git(root, "cat-file", "blob", oid).decode("utf-8")
    version = json.loads(git(root, "show", f"{commit}:{PLUGIN}/.codex-plugin/plugin.json"))["version"]
    extension = json.loads(git(root, "show", f"{commit}:contracts/studies-platform-classification-v1.json"))
    return build_platform_classification_bundle(sources, version, commit, extension)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    raw = build_from_checkout()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "public-platform-classification-skills.json").write_bytes(raw)
    checksum = hashlib.sha256(raw).hexdigest()
    (args.output_dir / "public-platform-classification-skills.sha256").write_text(checksum + "\n", encoding="ascii")
    print(f"Built separate exact-36 method asset ({len(raw)} bytes), sha256={checksum}")


if __name__ == "__main__":
    main()
