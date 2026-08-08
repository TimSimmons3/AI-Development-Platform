# SMT Workstream Continuation Control Template

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
POST_R1_PROCESS_INSTITUTIONALIZATION=MANDATORY
PROCESS_ASSURANCE_METRICS_RECORD=<REQUIRED_REPOSITORY_OR_PACKAGE_PATH>
R1_REOPENED=FALSE
```

Use this template for every governed handoff/new-chat continuation. Replace placeholders with exact evidence; do not omit sections.

## 1. Exact Identity and Authority

<REQUIRED>

## 2. Workstream Phase and Current Gate

<REQUIRED>

## 3. Authorized and Prohibited Actions

<REQUIRED>

## 4. Source of Truth and Requirements Inventory

<REQUIRED>

## 5. Dependency and External Contract Inventory

<REQUIRED>

## 6. Frozen Model and Convergence Rule

<REQUIRED>

## 7. Defect CAPA and Review Lineage

<REQUIRED>

## 8. Scenario-Faithful Probe and Evidence Map

<REQUIRED>

## 9. Live and External Evidence Boundary

<REQUIRED>

## 10. GitHub Protection and Required Check State

<REQUIRED>

## 11. Trust Root and CODEOWNERS State

<REQUIRED>

## 12. Process Assurance Metrics P01-P14

<REQUIRED>

## 13. Artifact Package and Operator Evidence

<REQUIRED>

## 14. Recoverability Evidence

<REQUIRED>

## 15. Risks Accepted Risk Deferred Follow-on and Lessons

<REQUIRED>

## 16. Exact Next Authorized Step and Stop Rule

<REQUIRED>

## Handoff acceptance

```text
HANDOFF_SECTIONS=16_OF_16
AUTHORITATIVE_IDENTITIES=EXACT
UNRESOLVED_ASSUMPTIONS=0
NEXT_AUTHORIZED_STEP=EXPLICIT
IMPLICIT_CONTINUATION=PROHIBITED
```
