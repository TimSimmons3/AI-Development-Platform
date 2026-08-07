# SMT Transition Governance Integration Addendum

## Status

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
TRANSITION_GOVERNANCE_CANONICAL=TRUE
BASELINE_COMMIT=311642c7465a01ada8297f8242b3d6e73033fed6
LIVE_CHANGE_BEFORE_INTEGRATION_QUALIFICATION=HOLD
REMOTE_PUBLICATION_REQUIRES_SEPARATE_AUTHORIZATION=TRUE
```

## Integration model

This addendum supplements the existing high-assurance and mandatory one-pass control chain. It does not replace or weaken owner-only exception control, existing invariant policy, live-attempt limits, external-contract controls, or security/recoverability requirements.

Canonical transition additions are the transition skill, transition standard, transition policy, transition validator, validator tests, structured templates, lifecycle/change-control requirements, and M01-M28 collection rules.

## Precedence

Where controls overlap, the stricter requirement governs. The existing mandatory one-pass invariant remains authoritative for artifact delivery and owner exceptions. Transition governance adds measurement, lifecycle, handoff completeness, and prospective event traceability.

## CI integration

The existing required check name remains `Mandatory assurance invariant gate`. The same workflow runs transition unit tests and a separate transition validation step. No additional GitHub permission is required. No repository ruleset change is required by this integration.

## Historical compatibility

Unchanged historical records remain immutable and are not retroactively rewritten. A historical governed record modified after adoption is validated under current transition requirements when its filename/scope triggers those requirements.

## Publication boundary

Offline qualification does not authorize commit, push, PR creation/merge, ruleset changes, Timeshift creation, or runtime changes. Before remote publication, re-observe effective `main` protection and required-check identity. A mismatch stops publication without automatic repair.

## Final assurance recovery supersession

The earlier statement that changed-path/file-scope design and the existing candidate workflow alone were sufficient is superseded for release authorization. Historical transition identity is sticky across modification, deletion, type change, rename/move, policy-classifier evolution, and reverse-reference discovery. Current validation uses the current policy while historical classification uses the merge-base policy; ordinary policy revisions cannot weaken the R1 semantic contract.

Change discovery uses the shared fail-closed A/M/D/T Git object contract. The existing `Mandatory assurance invariant gate` remains a candidate self-check. A separate `Mandatory assurance trusted gate`, executed from default-branch trusted code with read-only permissions, is the independent future trust anchor after bootstrap adoption. Activating it as a required ruleset check is a separate administrative authorization and is not performed by this recovery.

Any repeated material qualification escape triggers an assurance reset to the state model/oracle rather than another symptom patch.
