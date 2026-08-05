# Owner-Approved Exception Records

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

This directory stores the only valid project-owner exception records for the mandatory one-pass delivery invariant.

## Rules

- Only Tim Simmons may approve an exception.
- Every exception must be approved before delivery or execution.
- Every exception is limited to named controls, scope, artifacts, hashes, and expiration.
- General instructions, urgency, prior approvals, and preserved mutation budgets do not qualify.
- An exception-bearing pull request requires a current approval from `TimSimmons3` on the exact head commit.
- Expired, placeholder, inherited, post-execution, or open-ended exceptions are invalid.
- Each exception uses a separate Markdown file and the exact fields defined by the machine-readable policy.

No exception is currently approved.
