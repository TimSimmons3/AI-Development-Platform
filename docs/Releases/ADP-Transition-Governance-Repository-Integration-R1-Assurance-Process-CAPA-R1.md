# ADP Transition Governance Repository Integration R1
## Assurance Process Corrective and Preventive Action (CAPA) R1


### Mandatory one-pass control block

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

### 1. Status

```text
DATA_CURRENCY=2026-08-07T15:46:00-05:00
WORKSTREAM=ADP_TRANSITION_GOVERNANCE_REPOSITORY_INTEGRATION_R1
CAPA_CLASS=DESIGN_MODEL_AND_REVIEW_QUALIFICATION_PROCESS
ONE_PASS_OBJECTIVE=NOT_MET
PROCESS_CORRECTIVE_ACTION_REQUIRED=TRUE
LIVE_MUTATION_AUTHORIZED=FALSE
```

### 2. Problem statement

PR #5 experienced repeated material review findings after candidate publication despite increasingly large release-authorizing qualification programs. Seventeen validated Codex findings accumulated; eight are P1. Findings 15, 16, and 17 are especially probative because each exposed a new dimension of the same broad governance/discovery problem after a prior stage had been described as comprehensive.

The technical fixes through CR6-R2 remain valid for the behaviors they cover. The process failure is that the qualification model did not establish that every applicable externally observable state had been enumerated and challenged before publication.

### 3. Evidence of quality-system failure

| Stage | Focused tests | Full repository | Subsequent material escape |
|---|---:|---:|---|
| Initial offline candidate | 39 | 83 | Initial offline integration qualification. |
| CR1 | 47 | 91 | Findings 1-4. |
| CR2 | 63 | 107 | Findings 5-7. |
| CR3 | 70 | 114 | Findings 8-9. |
| CR4 | 93 | 137 | Findings 10-11; 3,000-case randomized fail-closed sweep. |
| CR5 | 117 | 161 | Findings 12-14; repository dependency/cardinality/parser expansion. |
| CR6 | 129 | 173 | Finding 15; 18-case governance-continuity matrix and 1,000 de-governance sweep. |
| CR6-R2 | 155 | 199 | Finding 16; 24-case policy-version matrix, 1,000 de-governance and 5,000 policy-mutation sweep. |

CR6-R2 also passed a 24/24 policy-version matrix, 1,000 historical de-governance attempts, 5,000 policy mutations, 12 preserve-state cases, and 34 independent distribution controls. Finding 17 still escaped because Git status `T` was outside the selected state model.

Conclusion: **passing tests are necessary but not sufficient when the state-space oracle is incomplete**.

### 4. Root causes

#### RC-1 - Requirements/state-space incompleteness
The test plan was derived from named requirements and known defect classes, but not from a complete cross-product of externally observable Git, filesystem, governance, parser, policy, and dependency states.

#### RC-2 - Independent oracle insufficiently independent at the model layer
Review execution was separate, but the reviewed dimensions were too often seeded by the implementation/test plan. The reviewer challenged expected results inside a selected space rather than independently proving the space itself was complete.

#### RC-3 - Readiness inferred from test volume
Increasing test counts and adversarial-case counts created confidence without a coverage denominator based on applicable semantic states.

#### RC-4 - Post-publication reviewer used as discovery
Fresh Codex review repeatedly found the next material boundary after publication. Final independent review therefore operated as an exploratory discovery gate rather than a confirmation gate.

#### RC-5 - Git external contract not fully modeled
`git diff --name-status` status classes were not enumerated as an external contract. `ACMRD` omitted `T`, permitting type changes to bypass validation.

#### RC-6 - Review-administration write boundary not technically allowlisted
A wrong GitHub write action created `__never__`. Authorization language existed, but tooling selection was not constrained by an explicit metadata-only API allowlist.

#### RC-7 - Qualification labels exceeded proven scope
"Comprehensive", "one-pass closure", and "zero unresolved assumptions" were used after the selected test matrix passed. They did not distinguish "zero unresolved assumptions inside the selected model" from "complete model independently proven".

### 5. Corrections already completed

- Findings 1-16 have implementation and regression evidence and resolved review threads.
- Unauthorized `__never__` commit was preserved and normally remediated without force push/history rewrite.
- Main remained frozen at `311642c7465a01ada8297f8242b3d6e73033fed6`.
- CR6-R2 exact-head CI run #29 passed.
- Current finding 17 remains open; no merge occurred.

These corrections do not close this CAPA.

### 6. Corrective action required before another executable

1. Freeze current live state.
2. Reconstruct requirements and externally observable state model outside production code.
3. Create an independent expected-results oracle from standards/contracts.
4. Reconcile oracle vs implementation expectations before coding.
5. Close every applicable state cell.
6. Implement one consolidated correction for all discovered gaps.
7. Commit exact candidate before `base...HEAD` validation.
8. Use byte-identical production validators and exact operator workflow.
9. Run complete real-Git state generation, parser/schema equivalence classes, reverse-reference and policy-version interactions, exception-surface tests, full regression, and preserve-state tests.
10. Perform independent pre-publication adversarial review of frozen candidate.
11. Release only one user-visible executable candidate.
12. Any material post-publication finding triggers CAPA re-evaluation; no automatic CR chain.

### 7. Preventive controls

The following controls become mandatory for future ADP tasks/waves:

```text
STATE_MODEL_BEFORE_IMPLEMENTATION=MANDATORY
APPLICABLE_STATE_CELL_DISPOSITION=100_PERCENT
INDEPENDENT_ORACLE_BEFORE_IMPLEMENTATION_EXPECTATIONS=MANDATORY
INDEPENDENT_VS_IMPLEMENTATION_DELTA=0
PREPUBLICATION_ADVERSARIAL_REVIEW=MANDATORY
POST_PUBLICATION_MATERIAL_DEFECT_TARGET=0
TEST_COUNT_AS_SOLE_READINESS_KPI=PROHIBITED
UNDISPOSITIONED_EXTERNAL_CONTRACT_STATE=0
UNEXPECTED_GIT_STATUS=FAIL_CLOSED
REVIEW_ADMINISTRATION_REPOSITORY_CONTENT_API=PROHIBITED
REPEATED_MATERIAL_ESCAPE_TRIGGERS_ASSURANCE_RESET=TRUE
```

### 8. Documentation/skill institutionalization

This CAPA is not complete until every artifact marked UPDATE REQUIRED or NEW REQUIRED in the documentation/skill update manifest has been updated, independently reviewed, committed, and verified on the protected branch.

The affected scope includes the high-assurance skill, mandatory one-pass skill/standard, live-change standard, preflight checklist, integration guides/addenda, transition skill/standard, workstream plan/decision/qualification/traceability, engineering log, and new CAPA/recovery/closeout records.

### 9. Effectiveness criteria

CAPA effectiveness is proven only when:

```text
APPLICABLE_REQUIREMENT_STATE_CELLS_COVERED=100_PERCENT
INDEPENDENT_VS_IMPLEMENTATION_EXPECTATION_DELTA=0
UNHANDLED_EXCEPTION_SURFACES=0
UNDISPOSITIONED_GIT_STATE_CLASSES=0
UNRESOLVED_ADVERSARIAL_FINDINGS=0
PRODUCTION_PATH_SUBSTITUTIONS_OR_MOCKS=0
USER_VISIBLE_REPLACEMENT_PACKAGE_COUNT_FOR_FINAL_RECOVERY=0
POST_PUBLICATION_MATERIAL_DEFECT_COUNT_FOR_FINAL_RECOVERY=0
SKILL_STANDARD_UPDATE_RECONCILIATION=PASS
FINAL_HANDOFF_COMPLETENESS=100_PERCENT
```

### 10. Residual risk

Until these criteria are met, PR #5 is not merge-ready and the assurance system must be treated as under corrective action. The existing baseline remains protected because `main` is unchanged and the feature branch is isolated.

### Pre-publication recovery qualification finding FAR-QF-01

The first exact committed-candidate trust-root rehearsal failed closed because the bootstrap migration record had been derived only from the recovery working-tree delta. That omitted the already-present CR6-R2 change to `.github/workflows/mandatory-assurance-invariant-gate.yml` relative to exact base `311642c7465a01ada8297f8242b3d6e73033fed6`. The migration set is now derived from the complete base-to-candidate Git delta, including inherited candidate changes. No artifact was released and no remote mutation occurred. The corrected consolidated candidate must repeat every release-authorizing qualification family from the exact new committed identity.

### Pre-publication recovery qualification finding FAR-QF-02

The first production-path mandatory `--base-ref` run failed closed because the new bounded-resource policy shape was incorrectly required to exist in the historical base policy. Exact base `311642c7465a01ada8297f8242b3d6e73033fed6` predates that field. The compatibility contract now permits the field to be absent only in the historical base and requires the current candidate to bootstrap the exact canonical R1 resource limits; once present, the limits are immutable under ordinary work. No release or remote mutation occurred. Full exact-candidate qualification restarts after the amended consolidated commit.

### Pre-publication recovery qualification finding FAR-QF-03

The first full-regression rerun after FAR-QF-02 failed before test execution because the newly added legacy-base resource-limit regression was inserted with invalid Python indentation and an incorrect module alias. This was a test implementation defect; production `--base-ref` validators had already passed, but the full-suite release gate correctly remained closed. The test is corrected and the exact candidate is re-frozen and fully requalified. No artifact or remote mutation occurred.

### Pre-publication recovery qualification finding FAR-QF-04

Adversarial trust-root review found that `.github/CODEOWNERS` and the mandatory, transition, and owner-approval validator test files were not yet included in the R1 trust manifest. Candidate versions of those tests are not executed by the current base-trusted workflow, so this was not a current self-approval path; however, after bootstrap merge they become default-branch trusted regression inputs and therefore must not be weakenable by a later ordinary PR. The trust manifest and bootstrap migration set now protect those paths. No publication or remote mutation occurred.

### Pre-publication recovery qualification finding FAR-QF-05

Ownership-map reconciliation found four R1 trust-root paths protected by the migration validator but not yet explicitly mapped to the project owner in `CODEOWNERS`: the high-assurance skill, live-change standard, owner-approval validator, and owner-approval regression test. The owner map now covers every manifest trust-root path, and a regression enforces that correspondence. This finding was closed before publication and caused no remote or production mutation.

### 11. Offline recovery effectiveness disposition

The consolidated Final Assurance Recovery R1 candidate closes the technical class demonstrated by finding 17 and incorporates FAR-QF-01 through FAR-QF-05, all of which were discovered and corrected before publication. Offline effectiveness requires the final committed candidate to repeat all exact `--base-ref`, full-regression, frozen 374-cell requirements-governed oracle, exception-surface, trusted-bootstrap, preserve-state, exact-artifact/operator, documentation-reconciliation, and adversarial-review gates after this closeout update. The external final qualification report is the authoritative record of those post-commit results.

CAPA remains **publication HOLD** until separately authorized remote publication proves the default-branch trusted gate in GitHub, any required-check/ruleset activation is separately authorized and verified, fresh exact-head remote review has zero unresolved material findings, and a separate owner merge authorization is issued. This HOLD is not a technical failure of the offline recovery candidate.
