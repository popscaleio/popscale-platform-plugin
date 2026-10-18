"""Pure package contracts; no host or OAuth proof is implied."""
import importlib.util,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from build_classification_skills import build_classification_bundle
SPEC=importlib.util.spec_from_file_location('old_public_builder',ROOT/'scripts/build_public_skills.py')
old=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(old)


class ClassificationBundleTests(unittest.TestCase):
    def setup_inputs(self):
        root=ROOT/'plugins/popscale-platform'
        sources={str(p.relative_to(root)):p.read_text() for p in (root/'skills').rglob('*.md')}
        contract=json.loads((ROOT/'contracts/product-tools-v1.json').read_text())
        ext=json.loads((ROOT/'contracts/studies-classification-v1.json').read_text())
        return sources,contract,ext

    def test_new_classification_artifact_carries_all_new_tools_without_changing_default_builder(self):
        sources,contract,ext=self.setup_inputs()
        before=json.dumps(contract,sort_keys=True)
        legacy=json.loads(old.build_bundle(sources,'1.6.8','a'*40,contract))
        new=json.loads(build_classification_bundle(sources,'1.6.8','a'*40,contract,ext))
        self.assertEqual(json.dumps(contract,sort_keys=True),before)
        self.assertTrue(set(ext['operations']).issubset(new['required_tools']))
        self.assertFalse(set(ext['operations'])&set(legacy['required_tools']))
        self.assertFalse(set(ext['excluded'])&set(new['required_tools']))
        self.assertEqual(new['schema_version'],legacy['schema_version'])
        self.assertEqual(new['skill_bundle_sha256'],legacy['skill_bundle_sha256'])
        # Full artifact differs because required-tool contracts differ; consumers
        # must bind source/profile + exact artifact, not cache by skills SHA alone.
        self.assertNotEqual(new['required_tools'],legacy['required_tools'])

    def test_duplicate_or_excluded_operation_cannot_be_promoted_into_profile_tools(self):
        sources,contract,ext=self.setup_inputs()
        for operation in (ext['operations'][0],ext['excluded'][0],'unreviewed_same_length_operation'):
            candidate=dict(ext,operations=ext['operations'][:-1]+[operation])
            with self.subTest(operation=operation),self.assertRaises(ValueError):
                build_classification_bundle(sources,'1.6.8','a'*40,contract,candidate)

    def test_scope_or_review_risk_tampering_does_not_create_a_valid_classification_artifact(self):
        from copy import deepcopy
        sources,contract,ext=self.setup_inputs()
        for key,value in (("required_scopes",["interview:analysis:read"]),("risk","bounded_write")):
            candidate=deepcopy(ext)
            candidate["operation_contracts"]["start_interview_classification"][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):
                build_classification_bundle(sources,'1.6.8','a'*40,contract,candidate)

    def test_profile_revision_bool_and_unknown_package_do_not_validate_as_reviewed_C3(self):
        sources,contract,ext=self.setup_inputs()
        for key,value in (("profile_revision",True),("consent_revision",2),("consent_revision",True)):
            candidate=dict(ext,**{key:value})
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):
                build_classification_bundle(sources,'1.6.8','a'*40,contract,candidate)

    def test_excluded_output_restore_cannot_enter_via_the_base_contract(self):
        from copy import deepcopy
        sources,contract,ext=self.setup_inputs()
        candidate=deepcopy(contract)
        candidate["product_tools"].append("resume_interview_analysis")
        with self.assertRaises(ValueError):
            build_classification_bundle(sources,'1.6.8','a'*40,candidate,ext)

    def test_extra_requirements_change_the_full_artifact_even_when_text_identity_is_equal(self):
        import hashlib
        sources,contract,ext=self.setup_inputs()
        legacy=old.build_bundle(sources,'1.6.8','a'*40,contract)
        classified=build_classification_bundle(sources,'1.6.8','a'*40,contract,ext)
        self.assertNotEqual(hashlib.sha256(legacy).hexdigest(),hashlib.sha256(classified).hexdigest())
        self.assertFalse(set(ext['operations'])&set(json.loads(legacy)['required_tools']))

    def test_missing_reachable_reference_cannot_silently_drop_an_accepted_tool(self):
        sources,contract,ext=self.setup_inputs()
        selected='skills/safe-interview-administration/references/classification-analysis.md'
        self.assertIn(selected,sources)
        missing=dict(sources)
        del missing[selected]
        with self.assertRaises(ValueError):
            build_classification_bundle(missing,'1.6.8','a'*40,contract,ext)
