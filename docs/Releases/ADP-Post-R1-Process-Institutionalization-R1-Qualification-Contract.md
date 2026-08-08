# ADP Post-R1 Process Institutionalization R1 Qualification Contract

## Mandatory one-pass control block

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

```text
EXACT_COMMITTED_CANDIDATE_QUALIFICATION=MANDATORY
FULL_REPOSITORY_REGRESSION=MANDATORY
PROCESS_VALIDATOR=MANDATORY
MANDATORY_INVARIANT_VALIDATOR=MANDATORY
TRANSITION_VALIDATOR=MANDATORY
TRUST_ROOT_MIGRATION_PREFLIGHT=MANDATORY
EXCEPTION_ADVERSARIAL_SWEEP=MANDATORY
EXACT_OPERATOR_REHEARSAL=MANDATORY
UNRESOLVED_ASSUMPTIONS=0
```

This record defines the release contract and does not self-declare final PASS. Exact committed-candidate evidence is produced by the operator under `~/Downloads/ADP-Post-R1-Process-Institutionalization-R1-Evidence` and is bound to the final candidate HEAD/tree.

R1 remains closed. The R1 374-cell denominator is not part of this workstream's mutable scope.

## Qualification correction R1

```text
COMMIT_DELTA_VALIDATOR_REQUIRES_COMMITTED_FIXTURE=TRUE
EXACT_COMMITTED_CHANGE_SET_OBSERVED=MANDATORY
PRECOMMIT_EMPTY_DELTA_PASS=NON_AUTHORIZING
```

The exact committed candidate is the first release-authorizing invocation for validators whose scope is derived from Git commit deltas. Supporting precommit syntax checks remain useful but cannot substitute for exact-head change-aware validation.

## Independent review correction contract R1

```text
PROCESS_POLICY_NON_WEAKENING=MANDATORY
CHANGED_HANDOFF_INSTANCE_VALIDATION=MANDATORY
CHANGED_PROCESS_METRICS_INSTANCE_VALIDATION=MANDATORY
COMPLETE_PI_MARKER_ENFORCEMENT=PI-01..PI-16
COMPLETE_PROCESS_METRIC_MARKER_ENFORCEMENT=P01-P14
BOUNDED_REVIEW_RECHECK_COUNT=1
```

This correction is the single bounded independent-review recheck permitted by P13. After the corrected exact head passes local qualification and GitHub required checks, no further open-ended model/review expansion is authorized absent a new material defect under the already-defined criteria.

## Template-instance boundary correction contract R1

```text
PROCESS_METRICS_TEMPLATE_IS_NOT_INSTANCE=TRUE
CANONICAL_TEMPLATE_VALIDATION=STRUCTURAL_MARKERS_ONLY
LIVE_INSTANCE_VALIDATION=CONCRETE_P01_P14_RECORD
HANDOFF_TEMPLATE_AS_LIVE_RECORD=PROHIBITED
P13_REVIEW_REFREEZE_CYCLES=1
```

Qualification must prove the canonical template remains intentionally placeholder-based while changed live records under governed instance roots are fail-closed and handoffs cannot bind the template in place of a completed workstream process-assurance record.

## PR #6 material-review escape correction qualification

```text
PR6_MATERIAL_REVIEW_ESCAPE_CORRECTION=4_OF_4
FINDINGS_REQUIRED_CLOSED=4_OF_4
DEDICATED_PROCESS_TESTS_EXPECTED=42
FULL_REPOSITORY_REGRESSION_EXPECTED=536
TRANSITION_BINDING_SCENARIO=MANDATORY
PROCESS_METRICS_DELETE_SCENARIO=MANDATORY
PROCESS_METRICS_IDENTITY_SCENARIOS=NONEXISTENT_AND_WRONG_TREE
HANDOFF_CONTENT_SCENARIOS=EMPTY_PLACEHOLDER_DUPLICATE
TRUST_ROOT_PATH_SET_EXPANSION=NONE
```

Release-authorizing qualification must occur on the exact committed corrected candidate. The prior 34/34 and 528/528 results remain historical coverage evidence only. Review threads remain unresolved until exact corrected-head evidence proves each finding closed.

## Final transition-validator collision closure qualification R1

```text
TRANSITION_VALIDATOR_COLLISION_ROOT_CAUSES=2
CANONICAL_OWNER_AUTHORIZATION_CARDINALITY=EXACTLY_ONE
LIVE_TRANSITION_RECORD_ASSIGNMENT_KEY_RESERVED_FOR_RECORD_BINDINGS=TRUE
CANONICAL_TEMPLATE_TRANSITION_RECORD_FIELD=EXACTLY_ONE_INTENTIONALLY_EMPTY
DEDICATED_PROCESS_TESTS_EXPECTED=44
FULL_REPOSITORY_REGRESSION_EXPECTED=538
PROCESS_INSTITUTIONALIZATION_VALIDATOR=PASS_REQUIRED
MANDATORY_ASSURANCE_VALIDATOR=PASS_REQUIRED
TRANSITION_METRICS_VALIDATOR=PASS_REQUIRED
EXCEPTION_ADVERSARIAL_SWEEP=35000_OF_35000_PASS_REQUIRED
TRUST_ROOT_MIGRATION_PREFLIGHT=PASS_REQUIRED
TRUST_ROOT_PATH_SET_EXPANSION=NONE
R1_REOPENED=FALSE
```

The intentionally empty transition-record field is a template sentinel, not a live evidence claim. Materialized governed handoffs must replace it with an exact repository metrics-record path; leaving it empty fails closed. Requirement and cardinality statements must use non-record semantic keys so repository-path scanners cannot misclassify governance text as evidence bindings.
