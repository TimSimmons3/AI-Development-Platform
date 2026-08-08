# SMT Mandatory Transition Metrics and Handoff Skill

## Status and authority

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
HANDOFF_LEVEL_SKILL=MANDATORY
REPOSITORY_CANONICAL_STATUS=CANONICAL_REPO_INTEGRATION_RECORD
TRANSITION_METRICS=MANDATORY
UNKNOWN_IS_NOT_ZERO=MANDATORY
NEXT_LIVE_CHANGE_REQUIRES_TRANSITION_GOVERNANCE=TRUE
```

## Operating rule

At every transition, produce one self-contained handoff package carrying current source-of-truth identities, evidence hashes, closed/open boundaries, defect/CAPA lineage, lessons learned, change-control state, security guardrails, and a complete M01-M28 metrics snapshot. Receiving work must not depend on conversational memory to reconstruct required facts.

## Metrics rule

Use `config/transition-metrics-policy.json` as the machine-readable metric dictionary. Record metrics at workstream start, gates, deviations/failures, release reset, live attempt, closeout, and handoff. `UNKNOWN` is never zero or PASS. External incidents remain separate from internal defects. Trend metrics bind to the prior handoff when one exists.

## Handoff package rule

A handoff is complete only when M26 proves all canonical package components present: main handoff, opening prompt, baseline/recovery identities, source-of-truth matrix, lifecycle/change addendum, QA/testing addendum, consolidated lessons/CAPA, metrics standard, paired metrics JSON/CSV, evidence manifest/checksums, superseded/historical register, security exclusion/redaction register, and package validation report.

## Timing and privacy rule

M21-M23 use event-based duration categories only: `ACTIVE_ENGINEERING`, `ACTIVE_OPERATOR`, `REWORK`, `HOLD_EXTERNAL`, and `HOLD_USER`. Do not capture keystrokes, message bodies, browsing history, raw prompts, credentials, environment dumps, or surveillance telemetry.

## Change/lifecycle rule

Use the canonical lifecycle state machine in the transition policy. A user-visible failure transitions to `RELEASE_RESET_REQUIRED`. Corrections use `CRn`; requirement/scope changes require a new governed revision after owner decision. External incidents preserve the exact candidate unless they expose a genuine internal defect. `CLOSED_AND_FROZEN` work is never reopened in place.

## Stop conditions

Stop with `BLOCKED_WITH_EXACT_REASON` when required metrics/evidence are missing, a handoff is incomplete, an unsafe or stale binding exists, the lifecycle transition is invalid, a live change is proposed before exact-artifact qualification, or the effective protected-publication contract cannot be re-observed before remote publication.

## Final assurance and handoff lineage

Every governed handoff must carry the complete defect/review/CAPA lineage, including qualification escapes, state-oracle coverage, trust-root/bootstrap status, exact base/head/tree identities, applicable-cell denominator, expectation-delta count, exception-surface result, full regression result, and documentation/skill reconciliation status. Do not convert missing evidence to zero or PASS.

M04/M05 and M24/M25 remain historical metrics; they do not by themselves prove assurance completeness. Supplemental assurance KRIs are mandatory when Final Assurance Recovery applies: applicable-state coverage percentage, oracle expectation delta count, unhandled exception count, unresolved material finding count, base-freshness status, and trust-root migration status. Future work must not start under superseded assurance controls.

When reporting assurance-model status, distinguish denominator changes from probe-subcase changes. A same-requirement/same-outcome/same-enforcement-branch subdivision is probe detail and does not change the frozen denominator. Any denominator change must identify the missing authoritative requirement or materially different expected enforcement/release disposition that justifies it.

## Post-R1 process-assurance overlay

```text
POST_R1_PROCESS_INSTITUTIONALIZATION=MANDATORY
PROCESS_ASSURANCE_METRICS=P01-P14
HANDOFF_CANONICAL_TEMPLATE=docs/Templates/SMT-Workstream-Continuation-Control-Template.md
M01_M28_SEMANTICS_UNCHANGED=TRUE
```

Every governed handoff carries P01-P14 in addition to M01-M28 where transition metrics apply. Handoffs must use the canonical 16-section continuation template, preserve defect/CAPA lineage, distinguish accepted risk from unresolved defect, and identify the exact next authorized step. Missing external evidence remains HOLD and may not be normalized to PASS.

## Post-R1 dual handoff binding

```text
TRANSITION_AND_PROCESS_METRICS_BINDINGS=MANDATORY
TRANSITION_METRICS_BINDING_CARDINALITY=EXACTLY_ONE
PROCESS_ASSURANCE_METRICS_BINDING_CARDINALITY=EXACTLY_ONE
```

Every governed post-R1 handoff must bind the existing M01-M28 transition record and the P01-P14 process-assurance record. The canonical template must expose both fields.
