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

The repository will use a policy JSON, invariant validator, owner-approval validator, full unit-test suite, GitHub Actions workflow, and CODEOWNERS ownership map.

The active `main` ruleset must require pull requests and the `Mandatory assurance invariant gate`, prohibit ordinary bypass, require resolved review conversations, and block force pushes and deletion.

The ruleset will not require an approval count or required CODEOWNER approval while the project owner is the sole repository operator and PR author. GitHub does not permit an author to approve their own PR. Requiring that review would create a deadlock or force a bypass.

## 6. Exception boundary

No current exception is approved. A future exception requires:

1. a valid record under `docs/Exceptions/`;
2. exactly one current authorization comment authored by `TimSimmons3`;
3. exact binding to the PR number, current head SHA, and sorted exception-record path set;
4. a passing `Mandatory assurance invariant gate` result.

A new commit invalidates the prior exception approval automatically. General comments, stale approvals, duplicates, or altered whitespace are invalid.

## 7. Implementation boundary

This adoption is documentation, policy, validation-code, test, and CI configuration only. It authorizes no runtime, infrastructure, model, repository-main merge, or live platform mutation beyond publishing the controlled branch and pull request.
