# SMT Mandatory One-Pass Delivery Skill

## 1. Status and authority

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

This skill is a mandatory supplement to the SMT High-Assurance Engineering Delivery Skill. It applies to every future ADP and Send Manna Too LLC handoff, plan, gate, runbook, implementation request, package, transaction, authorization, closeout, and execution-authorizing Markdown record.

This skill supersedes any prior language that allowed an unspecified written exception. Only the project owner, Tim Simmons, may approve an exception. No assistant, developer, reviewer, operator, automation, model, or repository administrator may self-approve, infer, broaden, or renew an exception.

## 2. Non-waivable operating rule

A deliverable may be presented as ready only when the exact user-delivered artifact and the exact operator workflow have completed the complete intended path successfully in a clean rehearsal environment that faithfully represents the target state.

The following are not substitutes:

- component tests;
- isolated function tests;
- development-directory execution;
- a synthetic success path that bypasses the final launcher;
- a command that differs from the command given to the user;
- a fixture that omits known target-state conditions;
- a reviewer who reuses implementation assumptions;
- a successful preflight that never proves the complete transaction.

## 3. Mandatory release evidence

Before user-visible delivery, retain evidence for:

1. the exact final package hash and manifest hash;
2. clean extraction of the exact final package;
3. execution of the exact distributed launcher;
4. execution of the exact user command, including shell, working directory, arguments, quoting, stdin, permissions, and prompts;
5. the actual target-state fixture or a checksum-bound target-state capture;
6. the complete success path through final state and recovery evidence;
7. every material failure and preserve-state path;
8. independent requirements-derived review;
9. zero unresolved assumptions, dependencies, path ambiguities, or authorization-contract mismatches;
10. reconciliation of outputs, counts, paths, modes, hashes, source removal, archive state, and remote state.

## 4. Release reset rule

Any user-visible failure before completion is a release-process failure, even when no mutation occurred. After the first user-visible failure:

- withdraw the package family;
- prohibit automatic corrected-package delivery;
- preserve evidence and reconcile actual state;
- perform a formal root-cause and test-gap review;
- redesign from requirements when the defect is systemic;
- require a new independent review that exercises the exact distributed artifact and operator workflow;
- obtain new package-bound authorization before any later mutation.

A corrected revision is not authorized merely because the mutation budget was preserved.

## 5. Owner-only exception control

An exception is valid only when all of the following exist before delivery:

- a Markdown exception record under `docs/Exceptions/`;
- exact controls being waived;
- exact scope and named artifacts;
- artifact SHA-256 set;
- rationale, residual risk, and compensating controls;
- UTC approval and expiration timestamps;
- SHA-256 of the owner's exact approval text;
- project-owner identity `Tim Simmons` and GitHub login `TimSimmons3`;
- exactly one current owner authorization comment when the change is processed through GitHub.

The exact comment form is:

```text
APPROVE SMT MANDATORY ASSURANCE EXCEPTION PR=<PR_NUMBER> HEAD=<CURRENT_HEAD_SHA> EXCEPTIONS=<SORTED_COMMA_SEPARATED_EXCEPTION_PATHS>
```

The comment must be authored by `TimSimmons3` and match the PR number, current head SHA, and complete sorted exception-record set exactly. A new commit invalidates the approval. Wrong-owner, stale-head, duplicate, incomplete, expanded, or whitespace-altered comments fail closed.

GitHub PR review approval is not used for this owner-exception control because PR authors cannot approve their own pull requests. The exact bound owner comment provides the required auditable approval without weakening branch protection or requiring a bypass.

Words such as “proceed,” “continue,” “approved,” or general authorization do not waive this skill. An exception cannot be implied from urgency, prior practice, rollback success, or the absence of mutation.

## 6. Handoff rule

Every future handoff must:

- include the complete invariant block exactly once;
- state whether an owner exception exists;
- cite any approved exception record;
- list exact final artifact and operator-workflow rehearsal evidence;
- identify unresolved assumptions as zero or stop the handoff;
- prohibit downstream work when the invariant block is absent or altered.

## 7. Machine enforcement

The repository invariant validator, owner-approval validator, test suite, and GitHub workflow are authoritative enforcement aids. They validate changed governance Markdown against the machine-readable policy, reject missing or altered invariant lines, reject malformed exception records, and require an exact current owner authorization comment for approved exceptions.

The protected `main` branch must require pull requests and the `Mandatory assurance invariant gate`, prohibit ordinary bypass, require resolved review conversations, and block force pushes and deletion. CODEOWNERS remains the authoritative ownership map but is not a required approval gate while the project owner is the sole repository operator and PR author.

Machine enforcement does not modify ChatGPT system instructions. It makes project compliance durable through repository content, automated gates, and required status checks.

## 8. Prohibited practices

- claiming “validated” when only components or simulations passed;
- delivering a package that has not executed through its final distributed launcher;
- changing operator instructions after package qualification without rerunning the exact workflow;
- using the target host as a test harness;
- issuing multiple corrected packages in response to sequential symptoms;
- treating a pre-mutation stop as permission to continue iterating with the user;
- allowing an exception without the project owner's exact written approval record and bound GitHub authorization comment;
- weakening, omitting, or rewording the invariant block to avoid the validator.
