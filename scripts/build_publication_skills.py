#!/usr/bin/env python3
"""Explicit optional C4 asset; C1/C2/C3/default artifacts keep their ceilings."""
from copy import deepcopy
from pathlib import Path
import argparse
import hashlib
import json
from build_public_skills import ROOT, git, build_bundle
from build_classification_skills import build_classification_bundle

PUBLICATION_OPERATIONS = frozenset(['submit_interview_classification_definition', 'publish_interview_classification_definition', 'recommend_interview_classification_definition', 'archive_interview_classification_definition', 'restore_interview_classification_definition'])
EXPECTED = {'schema_version': 'popscale.studies.publication-plugin.v1', 'tool_contract_version': 'popscale.product.actions.v1', 'profile_name': 'studies_analysis_v1', 'profile_revision': 1, 'consent_revision': 4, 'operations': ['submit_interview_classification_definition', 'publish_interview_classification_definition', 'recommend_interview_classification_definition', 'archive_interview_classification_definition', 'restore_interview_classification_definition'], 'operation_contracts': {'submit_interview_classification_definition': {'required_scopes': ['interview:analysis:read', 'interview:analysis:write'], 'request_schema': 'DefinitionLifecycleRequest', 'result_schema': 'DefinitionVersion', 'risk': 'bounded_write'}, 'publish_interview_classification_definition': {'required_scopes': ['interview:analysis:read', 'interview:definitions:publish'], 'request_schema': 'DefinitionLifecycleRequest', 'result_schema': 'DefinitionVersion', 'risk': 'review_required'}, 'recommend_interview_classification_definition': {'required_scopes': ['interview:analysis:read', 'interview:definitions:publish'], 'request_schema': 'DefinitionLifecycleRequest', 'result_schema': 'DefinitionVersion', 'risk': 'review_required'}, 'archive_interview_classification_definition': {'required_scopes': ['interview:analysis:read', 'interview:definitions:publish'], 'request_schema': 'DefinitionLifecycleRequest', 'result_schema': 'DefinitionVersion', 'risk': 'review_required'}, 'restore_interview_classification_definition': {'required_scopes': ['interview:analysis:read', 'interview:definitions:publish'], 'request_schema': 'DefinitionLifecycleRequest', 'result_schema': 'DefinitionVersion', 'risk': 'review_required'}}, 'scope_counts': {'R': 20, 'RW': 27, 'RC': 24, 'RP': 24, 'RWC': 31, 'RWP': 31, 'RCP': 28, 'RWCP': 35}}


def build_publication_bundle(sources, version, commit, base_contract, classification, publication):
    # First validate exact immutable C3, including its scopes and risk contracts.
    build_classification_bundle(sources, version, commit, base_contract, classification)
    if (type(publication) is not dict or publication != EXPECTED
            or type(publication.get("profile_revision")) is not int
            or type(publication.get("consent_revision")) is not int
            or type(publication.get("scope_counts")) is not dict
            or any(type(value) is not int for value in publication["scope_counts"].values())):
        raise ValueError("Exact separately reviewed C4 publication contract is required")
    contract = deepcopy(base_contract)
    contract["product_tools"] = sorted(set(contract["product_tools"]) | set(classification["operations"]) | PUBLICATION_OPERATIONS)
    raw = build_bundle(sources, version, commit, contract)
    if not PUBLICATION_OPERATIONS.issubset(json.loads(raw)["required_tools"]):
        raise ValueError("The complete publication method must be reachable")
    return raw


def build_from_checkout(root=ROOT):
    from build_public_skills import build_from_checkout as base_build
    root = Path(root)
    base = json.loads(base_build(root))
    commit = base["skill_source_commit"]
    sources = {row["path"]: row["content"] for row in base["files"]}
    read = lambda name: json.loads(git(root, "show", f"{commit}:{name}"))
    return build_publication_bundle(sources, base["plugin_version"], commit,
        read("contracts/product-tools-v1.json"), read("contracts/studies-classification-v1.json"),
        read("contracts/studies-publication-v1.json"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    raw = build_from_checkout()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "public-publication-skills.json").write_bytes(raw)
    checksum = hashlib.sha256(raw).hexdigest()
    (args.output_dir / "public-publication-skills.sha256").write_text(checksum + "\n", encoding="ascii")
    print(f"Built separate C4 method asset ({len(raw)} bytes), sha256={checksum}")


if __name__ == "__main__":
    main()
