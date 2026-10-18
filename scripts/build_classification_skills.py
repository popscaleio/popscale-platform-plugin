"""PROPOSAL pure secondary artifact builder; no default bundle/cache replacement."""
from copy import deepcopy
from build_public_skills import build_bundle

CLASSIFICATION_OPERATIONS = frozenset(('prepare_interview_classification_review', 'get_interview_classification_review', 'save_interview_classification_review', 'prepare_interview_classification', 'get_interview_classification_plan', 'start_interview_classification', 'get_interview_classification_job', 'list_interview_classification_jobs', 'read_interview_classification_results', 'cancel_interview_classification_job', 'get_interview_analysis_budget', 'set_interview_analysis_budget', 'get_interview_classification_post_review', 'save_interview_classification_correction', 'list_interview_classification_corrections'))

EXPECTED_CONTRACTS = {'prepare_interview_classification_review': {'required_scopes': ['interview:analysis:read',
                                                                 'interview:classify'],
                                             'risk': 'bounded_write',
                                             'request_schema': 'PrepareQualityPlanRequest',
                                             'result_schema': 'QualityPlan'},
 'get_interview_classification_review': {'required_scopes': ['interview:analysis:read'],
                                         'risk': 'read',
                                         'request_schema': 'QualityPlanIdRequest',
                                         'result_schema': 'QualityPlan'},
 'save_interview_classification_review': {'required_scopes': ['interview:analysis:read',
                                                              'interview:analysis:write'],
                                          'risk': 'review_required',
                                          'request_schema': 'SaveQualityReviewRequest',
                                          'result_schema': 'QualityPlan'},
 'prepare_interview_classification': {'required_scopes': ['interview:analysis:read',
                                                          'interview:classify'],
                                      'risk': 'bounded_write',
                                      'request_schema': 'PrepareClassificationRequest',
                                      'result_schema': 'ClassificationPlan'},
 'get_interview_classification_plan': {'required_scopes': ['interview:analysis:read'],
                                       'risk': 'read',
                                       'request_schema': 'PlanIdRequest',
                                       'result_schema': 'ClassificationPlan'},
 'start_interview_classification': {'required_scopes': ['interview:analysis:read',
                                                        'interview:classify'],
                                    'risk': 'review_required',
                                    'request_schema': 'StartClassificationRequest',
                                    'result_schema': 'ClassificationJob'},
 'get_interview_classification_job': {'required_scopes': ['interview:analysis:read'],
                                      'risk': 'read',
                                      'request_schema': 'JobIdRequest',
                                      'result_schema': 'ClassificationJob'},
 'list_interview_classification_jobs': {'required_scopes': ['interview:analysis:read'],
                                        'risk': 'read',
                                        'request_schema': 'ListRequest',
                                        'result_schema': 'ClassificationJobList'},
 'read_interview_classification_results': {'required_scopes': ['interview:analysis:read'],
                                           'risk': 'read',
                                           'request_schema': 'ReadResultsRequest',
                                           'result_schema': 'ClassificationResultsPage'},
 'cancel_interview_classification_job': {'required_scopes': ['interview:analysis:read',
                                                             'interview:classify'],
                                         'risk': 'bounded_write',
                                         'request_schema': 'CancelClassificationJobRequest',
                                         'result_schema': 'ClassificationJob'},
 'get_interview_analysis_budget': {'required_scopes': ['interview:analysis:read'],
                                   'risk': 'read',
                                   'request_schema': 'AnalysisIdRequest',
                                   'result_schema': 'MissionBudget'},
 'set_interview_analysis_budget': {'required_scopes': ['interview:analysis:read',
                                                       'interview:analysis:write'],
                                   'risk': 'review_required',
                                   'request_schema': 'BudgetMandateRequest',
                                   'result_schema': 'MissionBudget'},
 'get_interview_classification_post_review': {'required_scopes': ['interview:analysis:read'],
                                              'risk': 'read',
                                              'request_schema': 'PostReviewPageRequest',
                                              'result_schema': 'PostReviewPage'},
 'save_interview_classification_correction': {'required_scopes': ['interview:analysis:read',
                                                                  'interview:analysis:write'],
                                              'risk': 'review_required',
                                              'request_schema': 'SaveCorrectionRequest',
                                              'result_schema': 'Correction'},
 'list_interview_classification_corrections': {'required_scopes': ['interview:analysis:read'],
                                               'risk': 'read',
                                               'request_schema': 'C3CorrectionPageRequest',
                                               'result_schema': 'CorrectionPage'}}
EXCLUDED = frozenset(['save_interview_analysis_revision', 'get_interview_analysis_revision', 'resume_interview_analysis', 'prepare_interview_report_edition', 'get_interview_report_edition', 'submit_interview_classification_definition', 'publish_interview_classification_definition', 'recommend_interview_classification_definition', 'archive_interview_classification_definition', 'restore_interview_classification_definition'])


def build_classification_bundle(sources, version, commit, base_contract, extension):
    if (extension.get('schema_version') != 'popscale.studies.classification-plugin.v1'
            or extension.get('tool_contract_version') != base_contract['tool_contract_version']
            or extension.get('profile_name') != 'studies_analysis_v1'
            or type(extension.get('profile_revision')) is not int or extension['profile_revision'] != 1
            or type(extension.get('consent_revision')) is not int or extension['consent_revision'] != 3
            or extension.get('operation_contracts') != EXPECTED_CONTRACTS
            or extension.get('scope_counts') != {'R': 20, 'RW': 26, 'RC': 24, 'RWC': 30}
            or not isinstance(extension.get('excluded'), list) or set(extension['excluded']) != EXCLUDED
            or type(extension.get('operations')) is not list
            or any(type(name) is not str for name in extension['operations'])
            or len(extension['operations']) != len(CLASSIFICATION_OPERATIONS)
            or set(extension['operations']) != CLASSIFICATION_OPERATIONS
            or set(extension['operations']) & set(extension['excluded'])):
        raise ValueError('Exact separately reviewed classification contract is required')
    contract=deepcopy(base_contract)
    if EXCLUDED & set(base_contract['product_tools']):
        raise ValueError('Excluded operations cannot enter through the legacy contract')
    contract['product_tools']=sorted(set(contract['product_tools']) | set(extension['operations']))
    return build_bundle(sources,version,commit,contract)


def build_from_checkout(root=None):
    """Use the same clean committed provenance as the existing release builder."""
    import json
    from pathlib import Path
    from build_public_skills import ROOT, build_from_checkout as base_build, git
    root = ROOT if root is None else Path(root)
    base = json.loads(base_build(root))
    commit = base['skill_source_commit']
    sources = {row['path']: row['content'] for row in base['files']}
    contract = json.loads(git(root, 'show', f'{commit}:contracts/product-tools-v1.json'))
    extension = json.loads(git(root, 'show', f'{commit}:contracts/studies-classification-v1.json'))
    return build_classification_bundle(sources, base['plugin_version'], commit, contract, extension)


def main():
    import argparse
    import hashlib
    from pathlib import Path
    parser = argparse.ArgumentParser(description='Build a separate optional C3 skills artifact from clean committed public sources')
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    raw = build_from_checkout()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'public-classification-skills.json').write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    (args.output_dir / 'public-classification-skills.sha256').write_text(digest + '\n', encoding='ascii')
    print(f'Built separate public-classification-skills.json ({len(raw)} bytes), sha256={digest}')


if __name__ == '__main__':
    main()
