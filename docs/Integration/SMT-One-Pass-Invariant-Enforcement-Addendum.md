# SMT One-Pass Invariant Enforcement Addendum

## 1. Mandatory invariant

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

This addendum is effective for all future ADP handoffs, release plans, decision records, implementation records, package instructions, transaction records, authorization records, runbooks, standards, templates, skills, and closeouts.

## 2. Canonical additions

The canonical assurance set now includes:

```text
skills/smt-mandatory-one-pass-delivery/SKILL.md
docs/Standards/SMT-Mandatory-One-Pass-Delivery-and-Owner-Exception-Control-Standard.md
docs/Integration/SMT-One-Pass-Invariant-Enforcement-Addendum.md
docs/Templates/SMT-Mandatory-Assurance-Invariant-Block.md
config/mandatory-assurance-invariant-policy.json
scripts/validate_mandatory_assurance_invariants.py
scripts/validate_owner_exception_approval.py
.github/workflows/mandatory-assurance-invariant-gate.yml
.github/CODEOWNERS
```

These records supplement the existing high-assurance skill, preflight checklist, live-change standard, and integration guide. Where exception or iteration language conflicts, the stricter owner-only one-pass requirement controls.

## 3. Future handoff minimum block

Every future handoff must copy the invariant block exactly and must additionally state:

- exact final package and manifest hashes, when applicable;
- exact operator command rehearsal result;
- actual target-state fixture identity;
- success-path and failure-path evidence identities;
- independent reviewer and review method;
- unresolved assumptions count;
- owner exception record or explicit absence;
- prior user-visible failure count for the workstream;
- release-reset status.

A handoff missing any required element is `BLOCKED_WITH_EXACT_REASON` and cannot authorize implementation or execution.

## 4. Historical records

Historical evidence and closeouts are not rewritten. A new decision record documents this adoption. Any historical governed Markdown file modified after adoption must satisfy the current invariant validator.

## 5. Exception processing

Approved exceptions must be stored under `docs/Exceptions/`. An exception-bearing PR requires exactly one current comment authored by `TimSimmons3` in this form:

```text
APPROVE SMT MANDATORY ASSURANCE EXCEPTION PR=<PR_NUMBER> HEAD=<CURRENT_HEAD_SHA> EXCEPTIONS=<SORTED_COMMA_SEPARATED_EXCEPTION_PATHS>
```

The workflow binds the approval to the exact PR number, current head SHA, and exact sorted exception-record set. Any new commit invalidates the approval. General project authorization, PR authorship, or an administrator role is not an exception approval.

## 6. Repository protection requirement

Full preventative enforcement requires an active branch ruleset targeting `main` that:

1. requires pull requests before merging;
2. requires the `Mandatory assurance invariant gate` status check;
3. has no ordinary bypass actor;
4. requires all review conversations to be resolved;
5. blocks force pushes;
6. blocks branch deletion.

A required approval count or required CODEOWNER approval is not enabled while the repository has one owner and that owner authors the pull request. GitHub does not permit authors to approve their own PRs. CODEOWNERS remains the authoritative ownership map and notification source. Approved exceptions are instead controlled by the exact owner comment and CI verification above.

Until the repository ruleset is enabled, the workflow detects violations but cannot prevent an administrator from direct-pushing around it. This limitation must remain a recorded HOLD, not be described as fully enforced.

## 7. State-oracle and trust-root enforcement extension

The mandatory invariant gate is necessary but not sufficient for release authorization. Final Assurance Recovery adds a requirements-derived 108-cell state oracle, shared Git A/M/D/T object contract, policy anti-self-weakening, assurance trust-root manifest, and a base/default-branch trusted read-only workflow. The candidate self-check remains supporting evidence; the trusted gate is the independent enforcement path after bootstrap adoption.

Handoffs must include CAPA/state-matrix coverage, exact base/head/tree, expectation delta, exception-surface result, and documentation reconciliation. Future work under superseded assurance controls is prohibited.
