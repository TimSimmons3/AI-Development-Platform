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

Approved exceptions must be stored under `docs/Exceptions/` and require a current `TimSimmons3` approval on the exact PR head commit. General project authorization is not an exception approval.

## 6. Repository protection requirement

Full preventative enforcement requires branch protection or a repository ruleset that:

1. requires pull requests before merging to `main`;
2. requires the `Mandatory assurance invariant gate` status check;
3. requires code-owner review for canonical policy, skill, validator, workflow, and exception records;
4. dismisses stale approvals when new commits are pushed;
5. prohibits bypass except by the project owner for a separately recorded emergency exception.

Until those repository settings are enabled, the workflow detects violations but cannot prevent an administrator from direct-pushing around it. This limitation must remain a recorded HOLD, not be described as fully enforced.
