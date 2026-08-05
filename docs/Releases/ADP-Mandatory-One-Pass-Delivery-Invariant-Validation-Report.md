# ADP Mandatory One-Pass Delivery Invariant Validation Report

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

## 2. Validation scope

The validation covered the mandatory skill, owner-exception standard, integration addendum, handoff template, machine-readable policy, invariant validator, owner-approval validator, both test suites, GitHub workflow, CODEOWNERS ownership map, implementation plan, adoption decision, validation record, and exception-directory guidance.

Exact changed paths and content identity are derived from the final immutable Git tree, the pull-request comparison, and the CI validation result. No separately committed intermediate hash manifest is used because sequential branch commits would make it drift-prone before finalization.

## 3. Results

```text
PYTHON_AST_AND_BYTECODE=PASS
STRICT_POLICY_JSON=PASS
WORKFLOW_YAML_PARSE=PASS
INVARIANT_VALIDATOR_TESTS=26_OF_26_PASS
OWNER_APPROVAL_VALIDATOR_TESTS=18_OF_18_PASS
TOTAL_FUNCTIONAL_TESTS=44_OF_44_PASS
EXACT_CHANGED_FILE_WORKFLOW=PASS
EXACT_NEGATIVE_WORKFLOW=PASS
NEW_GOVERNANCE_MARKDOWN_VALIDATION=PASS
INDEPENDENT_REVIEW_EXECUTION=PASS
TRAILING_WHITESPACE=PASS
CR_CHARACTER_SCAN=PASS
SYMLINK_AND_OUTSIDE_PATH_NEGATIVE_TESTS=PASS
OWNER_ONLY_EXCEPTION_RECORD_TESTS=PASS
OWNER_COMMENT_BINDING_TESTS=PASS
RUNTIME_MUTATION=FALSE
```

## 4. Exact workflow rehearsal

An isolated Git repository was initialized with a baseline commit. The exact invariant-validator command used by the workflow was executed against the changed governed-file set using a real Git comparison base. All governed files passed. A new handoff with one mandatory invariant line removed was committed and the same changed-file workflow failed with the expected canonical-block and control-specific violations.

The owner-approval validator was exercised through its actual CLI with strict JSON input and output files. Tests proved:

- no exception requires no owner comment;
- one exact current owner comment passes;
- paginated GitHub `--slurp` comment shape passes;
- wrong owner, wrong PR number, stale head SHA, wrong exception set, added whitespace, and duplicate exact comments fail;
- malformed counts, duplicate exception paths, unsorted exception paths, invalid head SHA, malformed comment structures, and failed invariant reports fail closed.

The GitHub workflow runs both test suites before changed-governance validation. For exception-bearing PRs it retrieves repository comments through the GitHub API and executes the production owner-approval validator. Merge is prohibited unless the workflow passes on the exact final PR head.

## 5. Independent review

A separate requirements-based review independently checked:

- the canonical block appears exactly once and in policy-defined order in every governed Markdown file;
- owner-only exception and release-reset requirements appear in the skill and standard;
- every future handoff is required to copy the block exactly;
- the exception approval is bound to owner identity, PR number, current head SHA, and exact exception-record set;
- a new commit invalidates prior approval;
- no-exception changes do not require an impossible self-review;
- exception direct pushes fail;
- branch-ruleset limitations are stated accurately;
- CODEOWNERS remains an ownership map without becoming a sole-owner merge deadlock.

## 6. Residual enforcement hold

```text
REPOSITORY_POLICY_CONTENT=READY
DETECTIVE_CI_GATE=READY
FULL_PREVENTATIVE_ENFORCEMENT=HOLD_PENDING_ACTIVE_MAIN_RULESET
```

The active `main` ruleset must require pull requests and the `Mandatory assurance invariant gate`, have no ordinary bypass actor, require resolved review conversations, and block force pushes and branch deletion.

A required approval count and required CODEOWNER approval must not be enabled while `TimSimmons3` is the sole repository operator and PR author, because the author cannot approve their own pull request. Owner exception approval is enforced by the exact bound comment and CI validator instead.

## 7. Release disposition

```text
PARTIAL_WORK_COMPLETED_AND_NOT_RELEASED
```

The governance implementation is validated for a controlled branch and draft pull request. Merge and full enforcement remain blocked pending active repository ruleset verification and a passing workflow on the exact final head.
