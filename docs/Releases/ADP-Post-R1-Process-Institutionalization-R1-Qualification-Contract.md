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
