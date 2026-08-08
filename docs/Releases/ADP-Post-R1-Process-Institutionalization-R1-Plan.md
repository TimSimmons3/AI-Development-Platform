# ADP Post-R1 Process Institutionalization R1 Plan

## Mandatory one-pass control block

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

```text
WORKSTREAM=ADP_POST_R1_PROCESS_INSTITUTIONALIZATION_R1
BASE_MAIN=e599880ad7d1359efaf48c818b561275c069382e
BASE_TREE=533199b8332304b34501cddac3e1965005b11b45
R1_REOPENED=FALSE
R1_FROZEN_DENOMINATOR=374
CONTROL_MATRIX=16_OF_16
PROCESS_METRICS=14_OF_14
MANDATORY_HANDOFF_SECTIONS=16_OF_16
```

CHANGE_RECORD_BASELINE=e599880ad7d1359efaf48c818b561275c069382e
CHANGE_RECORD_SCOPE=Institutionalize the approved 16-control post-R1 process matrix across handoffs skills standards machine policy QA validation testing workflow enforcement CODEOWNERS trust-root CAPA release gates metrics and recoverability.
CHANGE_RECORD_EXCLUSIONS=No R1 reopen no 374-cell denominator change no runtime or service mutation no ruleset weakening no direct unreviewed main change no Timeshift no cleanup and no unrelated change.
AUTHORIZED_CHANGED_RESOURCES=The exact 23 paths frozen by the implementation operator and no others.
DEPENDENCIES=Python3 Git existing ADP mandatory invariant transition metrics and assurance trust-root validators GitHub feature-branch publication and existing required check identity.
EXTERNAL_CONTRACTS=Git repository object model GitHub pull-request workflow and trust-root owner-approval contract.
SECURITY_IMPACT=Strengthens fail-closed process assurance and does not alter runtime service or data-plane behavior.
MUTATION_PRESERVE_BOUNDARIES=Repository content only on a separate governed feature branch; main runtime services rulesets Timeshift and unrelated state are preserved.
TEST_MATRIX=Process-validator positive negative boundary tests full repository regression mandatory invariant validation transition validation trust-root migration preflight and existing exception adversarial sweep.
EVIDENCE_PLAN=Exact committed head tree diff validator reports regression logs source archive trust-root path digest and GitHub required-check evidence.
RECOVERY_PLAN=Feature branch remains separable from main until reviewed merge; exact baseline and candidate identities plus source archive are retained.
METRICS_PLAN=Measure and hand off P01-P14 as the process-assurance family while preserving M01-M28 semantics.
OWNER_AUTHORIZATION=Project-owner authorization dated 2026-08-08 for ADP Post-R1 Process Institutionalization R1.
OWNER_AUTHORIZATION_EXPIRATION=Valid only for this bounded workstream through final administrative closeout unless revoked.

## Objective

Institutionalize the R1 lessons across skills, standards, handoffs, machine policy, QA, validation, testing, workflow enforcement, CODEOWNERS, trust-root governance, metrics, CAPA, release gates, and recoverability without reopening R1.

## Implementation scope

One governed branch and pull request. No direct unreviewed main change, ruleset weakening, force/history rewrite, Timeshift, runtime/service mutation, cleanup, or unrelated change.

## Acceptance gates

- 16/16 controls represented in the canonical standard and machine policy.
- P01-P14 defined and available to every future handoff.
- 16/16 handoff sections machine-checked.
- Three canonical skills updated.
- Core standards and RTM updated.
- Candidate and trusted workflows integrate the institutionalization validator.
- CODEOWNERS and trust-root manifest cover the new controls.
- Positive, negative, and boundary tests pass.
- Full repository regression passes on the exact committed candidate.
- Existing exception/adversarial qualification passes.
- Exact operator/package evidence is retained.
- User-visible replacement-package count remains zero.

## Qualification defect disposition - 2026-08-08

The first local operator stopped after the exact committed candidate full regression. Two related defects were identified before remote publication:

- `IMPLEMENTATION_DEFECT`: the appended one-pass skill subsection repeated `USER_VISIBLE_REPLACEMENT_PACKAGE_TARGET=0`, while the canonical invariant validator requires every mandatory assignment exactly once.
- `REVIEW_TEST_DEFECT`: the operator labeled precommit change-aware validators PASS while the 23 changes were uncommitted. Those validators derive scope from committed Git deltas, so the precommit invocation observed an empty change set and could not qualify the new governed Markdown.

Remediation: remove only the duplicate appended assignment; preserve the canonical invariant; require committed candidate fixtures for all Git-delta-based validation; add a machine-enforced marker and regression; rerun complete exact-head qualification before publication.

No remote branch publication, PR creation, main change, runtime/service mutation, ruleset change, Timeshift creation, or R1 reopen occurred before this correction.

Interim process-assurance metric disposition for this escape:

```text
P07_LATE_MATERIAL_FINDINGS_AFTER_IMPLEMENTATION_START=1
P08_POST_PUBLICATION_MATERIAL_ESCAPE_COUNT=0
P09_USER_VISIBLE_REPLACEMENT_PACKAGE_COUNT=1
P10_UNRESOLVED_ASSUMPTIONS_AT_CORRECTION_GATE=0
P11_OPERATOR_RERUN_DUE_TO_PACKAGE_DEFECT=1
P13_REVIEW_REFREEZE_CYCLES=0
```

P01-P06, P12, and P14 are finalized at workstream closeout from the complete evidence set; they are not silently defaulted to zero.

## Independent review material finding - 2026-08-08

The single bounded independent review of draft PR #6 found one material enforcement gap before ready-for-review or merge:

- `DESIGN_DEFECT`: the process validator verified canonical institutionalization artifacts were present but did not validate future changed workstream handoff/process-metrics instances.
- `REVIEW_TEST_DEFECT`: the dedicated tests did not prove middle PI controls, middle P metrics, policy non-weakening, or changed handoff/P01-P14 instance enforcement.
- `TRUST_BOUNDARY_DEFECT`: future trusted code consumed a candidate-controlled process policy without comparing it to the trusted merge-base policy.

Remediation is bounded to the existing institutionalization model: add merge-base policy non-weakening, changed-instance handoff/P01-P14 validation, complete PI/P marker enforcement, and positive/negative/boundary tests. No new controls, metrics, denominator, Codex review, or R1 reopen is introduced.

```text
P07_LATE_MATERIAL_FINDINGS_AFTER_IMPLEMENTATION_START=2
P08_POST_PUBLICATION_MATERIAL_ESCAPE_COUNT=0
P09_USER_VISIBLE_REPLACEMENT_PACKAGE_COUNT=2
P10_UNRESOLVED_ASSUMPTIONS_AT_REVIEW_CORRECTION_GATE=0
P11_OPERATOR_RERUN_DUE_TO_PACKAGE_DEFECT=1
P13_REVIEW_REFREEZE_CYCLES=1
```

## Template-instance boundary qualification defect - 2026-08-08

The independent-review correction commit passed 31/31 dedicated tests and 525/525 full repository regression, then stopped before publication when the process validator classified the canonical P01-P14 template as a live metrics instance.

Classification:
- `IMPLEMENTATION_DEFECT`: live-instance discovery treated any changed JSON carrying the process-metrics record type as a completed live record, including the canonical placeholder template.
- `REVIEW_TEST_DEFECT`: the prior suite did not contain a boundary test proving the template is excluded from live-instance classification.

Remediation: define governed process-metrics instance roots; prohibit handoffs from binding the canonical template as a live record; validate template structure separately from concrete instance semantics; add positive/negative/boundary tests.

```text
P07_LATE_MATERIAL_FINDINGS_AFTER_IMPLEMENTATION_START=3
P08_POST_PUBLICATION_MATERIAL_ESCAPE_COUNT=0
P09_USER_VISIBLE_REPLACEMENT_PACKAGE_COUNT=3
P10_UNRESOLVED_ASSUMPTIONS_AT_TEMPLATE_BOUNDARY_GATE=0
P11_OPERATOR_RERUN_DUE_TO_PACKAGE_DEFECT=2
P13_REVIEW_REFREEZE_CYCLES=1
```

This completes the already-authorized single bounded review correction and is not a second independent review/refreeze cycle.
