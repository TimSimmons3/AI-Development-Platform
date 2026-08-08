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
- An exception-bearing pull request requires exactly one current authorization comment authored by `TimSimmons3`.
- The comment must match the machine-generated form exactly and bind the PR number, current head SHA, and complete sorted exception-record path set.
- Any new commit changes the head SHA and invalidates the prior authorization automatically.
- The pull-request author may post the authorization comment; GitHub does not allow authors to approve their own pull requests, so PR review approval is not used as the owner-exception control.
- Expired, placeholder, inherited, post-execution, open-ended, stale-head, wrong-owner, duplicate, or whitespace-altered approvals are invalid.
- Each exception uses a separate Markdown file and the exact fields defined by the machine-readable policy.
- Each exception names exactly one canonical artifact manifest under `docs/Exceptions/Artifacts/`; repository artifacts are byte-hash verified and external artifact/incident identities remain explicitly identity-to-digest bound.
- The approval-text SHA-256 is computed from the fixed non-circular authorization-basis field sequence defined by the mandatory one-pass standard; it does not hash the candidate head or itself.
- Approval and expiration are checked against trusted GitHub server timestamps during live qualification. Equality at expiration is invalid.

The exact comment form is:

```text
APPROVE SMT MANDATORY ASSURANCE EXCEPTION PR=<PR_NUMBER> HEAD=<CURRENT_HEAD_SHA> EXCEPTIONS=<SORTED_COMMA_SEPARATED_EXCEPTION_PATHS>
```

No exception is currently approved.
