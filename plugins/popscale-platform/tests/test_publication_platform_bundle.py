"""Pure optional asset contracts; neither OAuth nor host capability evidence."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from build_public_skills import build_bundle
from build_classification_skills import build_classification_bundle
from build_publication_skills import build_publication_bundle, PUBLICATION_OPERATIONS
from build_platform_classification_skills import (build_platform_classification_bundle,
    DOMAIN_OPERATIONS, CONTROL_TOOLS, ENTRYPOINT)


class PublicationPlatformBundleTests(unittest.TestCase):
    def inputs(self):
        plugin = ROOT / "plugins/popscale-platform"
        sources = {str(path.relative_to(plugin)): path.read_text(encoding="utf-8")
                   for path in (plugin / "skills").rglob("*.md")}
        read = lambda name: json.loads((ROOT / "contracts" / name).read_text())
        return sources, read("product-tools-v1.json"), read("studies-classification-v1.json"), read("studies-publication-v1.json"), read("studies-platform-classification-v1.json")

    def test_optional_c4_adds_exact_five_without_mutating_default_or_c3_tools(self):
        sources, base, classification, publication, platform = self.inputs()
        old = json.loads(build_bundle(sources, "1.7.0", "a" * 40, base))
        c3 = json.loads(build_classification_bundle(sources, "1.7.0", "a" * 40, base, classification))
        c4 = json.loads(build_publication_bundle(sources, "1.7.0", "a" * 40, base, classification, publication))
        self.assertEqual(set(c4["required_tools"]) - set(c3["required_tools"]), PUBLICATION_OPERATIONS)
        self.assertFalse(PUBLICATION_OPERATIONS & set(old["required_tools"]))
        self.assertFalse(PUBLICATION_OPERATIONS & set(c3["required_tools"]))
        self.assertEqual(c3["skill_bundle_sha256"], c4["skill_bundle_sha256"])
        self.assertNotEqual(hashlib.sha256(build_classification_bundle(sources,"1.7.0","a"*40,base,classification)).hexdigest(),
                            hashlib.sha256(build_publication_bundle(sources,"1.7.0","a"*40,base,classification,publication)).hexdigest())
        self.assertNotIn(ENTRYPOINT, old["instruction_paths"])

    def test_c4_scope_risk_closed_shape_and_revision_cannot_be_caller_modified(self):
        sources, base, c3, c4, platform = self.inputs()
        mutations = [c4 | {"consent_revision": 3}, c4 | {"profile_revision": True}, c4 | {"extra": True}, c4 | {"scope_counts":c4["scope_counts"] | {"R":20.0}}]
        changed = deepcopy(c4); changed["operation_contracts"]["publish_interview_classification_definition"]["risk"] = "bounded_write"; mutations.append(changed)
        changed = deepcopy(c4); changed["operation_contracts"]["publish_interview_classification_definition"]["required_scopes"] = ["interview:analysis:read", "interview:classify"]; mutations.append(changed)
        changed = deepcopy(c4); changed["scope_counts"]["RWCP"] = 36; mutations.append(changed)
        for mutation in mutations:
            with self.subTest(keys=sorted(mutation)), self.assertRaises(ValueError):
                build_publication_bundle(sources,"1.7.0","a"*40,base,c3,mutation)

    def test_platform_asset_has_exact36_complete_public_method_and_no_other_workflows(self):
        sources, base, c3, c4, platform = self.inputs()
        raw = build_platform_classification_bundle(sources,"1.7.0","a"*40,platform)
        body = json.loads(raw)
        self.assertEqual(set(body["required_tools"]), DOMAIN_OPERATIONS | CONTROL_TOOLS)
        self.assertEqual(len(body["required_tools"]),36)
        self.assertEqual(len(DOMAIN_OPERATIONS),31)
        self.assertEqual(body["instruction_paths"],[ENTRYPOINT])
        self.assertNotIn("request_company_switch",body["required_tools"])
        self.assertFalse(PUBLICATION_OPERATIONS & set(body["required_tools"]))
        self.assertNotIn("save_interview_classification_definition",body["required_tools"])
        identity=[{"path":row["path"],"sha256":row["sha256"]} for row in body["files"]]
        from build_public_skills import canonical
        self.assertEqual(body["skill_bundle_sha256"],hashlib.sha256(canonical(identity)).hexdigest())
        self.assertEqual(raw,build_platform_classification_bundle(dict(reversed(list(sources.items()))),"1.7.0","a"*40,platform))

    def test_platform_protocol_tools_missing_method_and_dependency_fail_closed(self):
        sources, base, c3, c4, platform = self.inputs()
        for mutation in (platform | {"protocol_revision":"studies.provider-execution.v1"},
                         platform | {"operation_ids":platform["operation_ids"][:12]},
                         platform | {"control_tools":platform["control_tools"]+["request_company_switch"]},
                         platform | {"extra":True}):
            with self.subTest(mutation=sorted(mutation)),self.assertRaises(ValueError):
                build_platform_classification_bundle(sources,"1.7.0","a"*40,mutation)
        for text in (sources[ENTRYPOINT].replace("`save_interview_analysis_revision`","save revision"),
                     sources[ENTRYPOINT]+"\nRead [missing](missing.md)."):
            with self.assertRaises(ValueError):
                build_platform_classification_bundle(sources | {ENTRYPOINT:text},"1.7.0","a"*40,platform)

    def test_platform_is_not_an_oauth_or_private_config_asset_and_text_change_binds_new_sha(self):
        sources, base, c3, c4, platform = self.inputs()
        raw=build_platform_classification_bundle(sources,"1.7.0","a"*40,platform)
        changed=build_platform_classification_bundle(sources | {ENTRYPOINT:sources[ENTRYPOINT]+"\nAnother public method note.\n"},"1.7.0","a"*40,platform)
        self.assertNotEqual(hashlib.sha256(raw).hexdigest(),hashlib.sha256(changed).hexdigest())
        self.assertFalse({"consent_revision","allowed_tools","host_instructions","private_sha256"} & set(json.loads(raw)))
        with self.assertRaises(ValueError):build_platform_classification_bundle(sources,"1.7.0","not-a-commit",platform)

    def test_platform_paths_match_existing_consumer_without_encoded_or_oversized_names(self):
        sources, base, c3, c4, platform = self.inputs()
        prefix = ENTRYPOINT.rsplit('/', 1)[0] + '/'
        for name, link in (("bad%2fname.md", "bad%252fname.md"),
                           ("bad?name.md", "bad%3Fname.md"),
                           ("bad#name.md", "bad%23name.md"),
                           ("bad:name.md", "bad%3Aname.md"),
                           ("x" * 480 + ".md", "x" * 480 + ".md")):
            selected = sources | {prefix + name: "Public method reference.",
                ENTRYPOINT: sources[ENTRYPOINT] + "\nRead [extra](" + link + ").\n"}
            with self.subTest(name=name), self.assertRaises(ValueError):
                build_platform_classification_bundle(selected, "1.8.0", "a" * 40, platform)
