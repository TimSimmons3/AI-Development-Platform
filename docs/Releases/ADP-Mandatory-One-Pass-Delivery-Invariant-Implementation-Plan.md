# ADP Mandatory One-Pass Delivery Invariant Implementation Plan

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

## 2. Objective

Make first-pass working delivery, exact distributed-artifact rehearsal, exact operator-workflow rehearsal, owner-only exceptions, and release-reset behavior mandatory and machine-checkable for future ADP governance and execution records.

## 3. Scope

Create:

- a mandatory one-pass delivery skill;
- a formal owner-exception standard;
- an integration addendum;
- a reusable handoff invariant template;
- a machine-readable policy;
- an invariant validator and tests;
- an owner-exception approval validator and tests;
- a GitHub Actions gate that runs the complete test suite;
- CODEOWNERS ownership entries;
- an adoption decision and exception-directory guidance.

Historical evidence is not rewritten. No runtime, model, Docker, firewall, candidate, registry, witness, Timeshift, or production configuration change is included.

## 4. Design controls

- One machine-readable policy is the source of truth for required invariant keys and values.
- The invariant validator checks only new or modified governed Markdown.
- Every required assignment must appear exactly once.
- An approved exception must cite a regular Markdown record under `docs/Exceptions/`.
- Exception records require exact project-owner identity and non-placeholder, format-valid fields.
- An exception-bearing pull request requires exactly one current authorization comment authored by `TimSimmons3`.
- The owner comment is bound to the PR number, current head SHA, and complete sorted exception-record path set.
- Any new commit invalidates the prior approval automatically.
- Direct-push exception changes fail the workflow.
- Normal no-exception changes require the mandatory CI gate but no impossible self-review.
- Full prevention remains blocked until an active `main` ruleset requires pull requests and the workflow, has no ordinary bypass, requires resolved conversations, and blocks force pushes and deletion.

## 5. Validation plan

- strict JSON duplicate-key parsing;
- governed-path and filename-keyword tests;
- valid invariant block success;
- missing and duplicate assignment failures;
- missing, malformed, placeholder, and wrong-owner exception failures;
- exact owner-comment success;
- wrong-owner, wrong-PR, stale-head, wrong-exception-set, duplicate-comment, and whitespace-drift failures;
- paginated GitHub comment-response handling;
- symlink, outside-path, invalid UTF-8, CR, and trailing-whitespace failures;
- exact workflow syntax review;
- complete unit-test execution in GitHub Actions;
- validator execution against every new governed Markdown file;
- changed-path, file hash, and branch diff reconciliation;
- independent review before merge.

## 6. Acceptance criteria

```text
NEW_SKILL_PRESENT=PASS
OWNER_EXCEPTION_STANDARD_PRESENT=PASS
INTEGRATION_ADDENDUM_PRESENT=PASS
HANDOFF_TEMPLATE_PRESENT=PASS
POLICY_JSON_VALID=PASS
INVARIANT_VALIDATOR_TESTS=PASS
OWNER_APPROVAL_VALIDATOR_TESTS=PASS
NEW_GOVERNANCE_MARKDOWN_VALIDATION=PASS
WORKFLOW_PRESENT=PASS
WORKFLOW_TEST_EXECUTION=PASS
CODEOWNERS_PRESENT=PASS
ADOPTION_DECISION_PRESENT=PASS
BRANCH_RULESET_REQUIRED_ACTION=RECORDED
RUNTIME_MUTATION=FALSE
```
