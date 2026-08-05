# ADP Mandatory One-Pass Delivery Invariant Adoption Decision

## 1. Governing invariant

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

## 2. Decision

ADP adopts the SMT Mandatory One-Pass Delivery Skill and the SMT Mandatory One-Pass Delivery and Owner Exception Control Standard as non-optional project governance.

Only Tim Simmons may approve an exception. Approval must be exact, written, time-bounded, artifact-bound, and recorded before delivery. General instructions to proceed do not waive the invariant.

## 3. Rationale

Repeated user-visible package corrections demonstrated that component tests, synthetic success paths, and partial launcher rehearsals can produce unsupported readiness claims. The corrective action is a governance and enforcement redesign, not another package-level patch.

## 4. Effective scope

The invariant applies to all future and newly modified ADP:

- handoffs;
- skills and standards;
- release and implementation plans;
- package and transaction instructions;
- authorization and gate records;
- runbooks, decision records, and closeouts;
- other execution-authorizing Markdown identified by the machine-readable policy.

Historical evidence remains unchanged unless independently amended for another approved reason.

## 5. Enforcement decision

The repository will use a policy JSON, validator, workflow, and CODEOWNERS file. The required GitHub branch-protection configuration is a mandatory administrative action. Until it is enabled, enforcement is detective rather than fully preventative and must not be represented as complete.

## 6. Exception boundary

No current exception is approved. Any future exception requires a record under `docs/Exceptions/` and current approval by `TimSimmons3` on the exact PR head commit.

## 7. Implementation boundary

This adoption is documentation, policy, validation-code, and CI configuration only. It authorizes no runtime, infrastructure, model, repository-main merge, or live platform mutation beyond publishing the controlled branch and pull request.
