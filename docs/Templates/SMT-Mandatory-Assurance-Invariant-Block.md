# SMT Mandatory Assurance Invariant Block

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

Copy the block above exactly once into every future governed Markdown record. Do not change key names, values, spacing, or exception status unless a valid owner-approved exception record exists.

## Required handoff evidence fields

| Field | Requirement |
|---|---|
| Final artifact identity | Exact file name, size, SHA-256, and manifest SHA-256 |
| Exact launcher rehearsal | Final packaged launcher and clean-extraction evidence |
| Exact operator workflow | Exact command, shell, working directory, arguments, stdin, prompts, and expected outputs |
| Target-state fixture | Checksum-bound actual target capture or approved equivalent |
| Success-path evidence | End-to-end final state and recovery proof |
| Failure-path evidence | Material failure and preserve-state proof |
| Independent review | Reviewer method and independently derived expectations |
| Assumptions | Explicit count; must be zero before delivery |
| Prior iterations | User-visible package/failure count and release-reset status |
| Exception | `NOT_GRANTED`, or a path to a valid owner-approved exception record |

## Exception record field names

An exception record uses these field names: exception status, approved by, GitHub login, approved UTC, approval-text SHA-256, control IDs, scope, rationale, residual risk, compensating controls, expiration UTC, artifact manifest path, and artifact SHA-256 set. The mandatory one-pass standard defines the canonical approval-basis hash preimage, artifact-manifest identity ordering, and trusted-time validity rules; the machine-readable policy defines required values and formats.
