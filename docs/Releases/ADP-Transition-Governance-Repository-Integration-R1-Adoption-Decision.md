# ADP Transition Governance Repository Integration R1 Adoption Decision

## Control block

```text
ONE_PASS_WORKING_DELIVERABLE=MANDATORY
EXACT_DISTRIBUTED_ARTIFACT_REHEARSAL=MANDATORY
EXACT_OPERATOR_WORKFLOW_REHEARSAL=MANDATORY
ACTUAL_TARGET_STATE_FIXTURE=MANDATORY
SUCCESS_PATH_END_TO_END=MANDATORY
FAILURE_AND_PRESERVE_STATE_PATHS=MANDATORY
INDEPENDENT_REQUIREMENTS_REVIEW=MANDATORY
UNRESOLVED_ASSUMPTIONS_BEFORE_DELIVERY=0
USER_VISIBLE_REPLACEMENT_PACKAGE_TARGET=0
PATCH_AND_RETRY_CYCLE=PROHIBITED
PRODUCTION_AS_TEST_ENVIRONMENT=PROHIBITED
EXCEPTION_AUTHORITY=PROJECT_OWNER_ONLY
EXCEPTION_STATUS=NOT_GRANTED
```

## Change record

```text
CHANGE_RECORD_BASELINE=311642c7465a01ada8297f8242b3d6e73033fed6
CHANGE_RECORD_SCOPE=TRANSITION_GOVERNANCE_REPOSITORY_INTEGRATION_R1_OFFLINE
CHANGE_RECORD_EXCLUSIONS=REMOTE_GITHUB_PUBLICATION_RULESET_CHANGE_TIMESHIFT_RUNTIME_MUTATION
AUTHORIZED_CHANGED_RESOURCES=DOCUMENTED_OFFLINE_PAYLOAD_PATHS_ONLY
DEPENDENCIES=PYTHON_3_STANDARD_LIBRARY_GIT_BASH
EXTERNAL_CONTRACTS=NONE_FOR_OFFLINE_VALIDATOR
SECURITY_IMPACT=NO_NEW_TOKEN_SCOPE_NO_RUNTIME_OR_FIREWALL_CHANGE
MUTATION_PRESERVE_BOUNDARIES=ISOLATED_OFFLINE_BRANCH_ONLY_NO_REMOTE_WRITE
TEST_MATRIX=35_DESIGN_NEGATIVE_CASES_PLUS_EXISTING_REPOSITORY_REGRESSION
EVIDENCE_PLAN=DETERMINISTIC_PACKAGE_MANIFEST_TEST_REPORT_AND_CLEAN_FIXTURE_REHEARSAL
RECOVERY_PLAN=DISCARD_OFFLINE_BRANCH_OR_RECLONE_FROM_VERIFIED_311642C_BUNDLE
METRICS_PLAN=M01_M28_START_GATE_CLOSEOUT_AND_HANDOFF_COLLECTION
OWNER_AUTHORIZATION=OFFLINE_IMPLEMENTATION_AND_QUALIFICATION_ONLY_2026_08_07
OWNER_AUTHORIZATION_EXPIRATION=NOT_APPLICABLE_OFFLINE_SCOPE
```

## Decision

Adopt transition metrics and handoff performance as a separate canonical module rather than merging M01-M28 semantics into the existing mandatory invariant/owner-exception validator.

## Rationale

The existing one-pass control chain is already qualified and security-sensitive. A separate policy/validator limits regression blast radius while the existing mandatory workflow remains the single required-check identity. The transition module adds measurement, lifecycle, deviation, test metadata, handoff completeness, timing, rework, and trend controls without duplicating artifact-delivery or exception semantics.

## Rejected alternatives

- Copy the R2 handoff addenda wholesale into parallel standards: rejected for duplication and precedence risk.
- Add M01-M28 logic to `validate_mandatory_assurance_invariants.py`: rejected for unnecessary coupling to owner-exception enforcement.
- Create a second required GitHub workflow/check: rejected because the existing mandatory workflow can host a separate validation step without a ruleset change.

## Publication status

This decision is qualified for offline implementation only. Canonical remote adoption remains pending a separately authorized publication gate.

## Final Assurance Recovery R1 decision amendment

The modular transition validator/policy architecture remains adopted as the preferred separation of concerns. The earlier conclusion that the existing candidate workflow should remain the sole required-check architecture is superseded by the independently reviewed trust-root design. A base/default-branch trusted read-only gate is required as the future independent trust anchor; its first adoption is a bootstrap migration and cannot self-protect.

Canonical merge readiness is HOLD until Final Assurance Recovery closes all 108 applicable state-oracle cells with zero expectation delta, zero unhandled exceptions, exact-base committed-candidate qualification, process CAPA/document reconciliation, and zero unresolved material findings. Ruleset activation and merge remain separately authorized actions.
