# SMT Mandatory Transition Metrics and Handoff Performance Standard

## Authority and status

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
TRANSITION_METRICS=MANDATORY
HANDOFF_METRICS_BASELINE=MANDATORY
GATE_METRICS_DELTA=MANDATORY
UNKNOWN_IS_NOT_ZERO=MANDATORY
METRICS_EVIDENCE_TRACEABILITY=MANDATORY
REPOSITORY_CANONICAL_STATUS=CANONICAL_REPO_INTEGRATION_RECORD
```

## Canonical machine-readable authority

`config/transition-metrics-policy.json` defines the exact M01-M28 names, formulas, targets, units, data-quality states, lifecycle states, timing categories, handoff components, and change-record fields. `scripts/validate_transition_metrics.py` fails closed on invalid structured records and required Markdown link/control fields.

## Core KPI/KRI definitions

| ID | Metric | Definition / formula | Target |
|---|---|---|---|
| M01 | First-pass delivery rate | First user-visible artifacts completing intended path without replacement / user-visible artifacts delivered | 100% |
| M02 | User-visible replacement count | Runnable corrected/replacement packages issued after release | 0 |
| M03 | User-visible failure count | Failures after delivery, including pre-mutation failures | 0 |
| M04 | Defect escape count | Internal defects first detected after user-visible release/checkpoint | 0 |
| M05 | Pre-release detection rate | Internal defects caught before user delivery / internal defects found | 100% |
| M06 | Plan adherence | Planned gates completed as designed / gates executed, with deviations separately counted | >=95%, target 100% |
| M07 | Unapproved deviation count | Deviations without owner/change-control disposition | 0 |
| M08 | Scope adherence | Actual changed resources within authorized scope / actual changed resources | 100% |
| M09 | Unauthorized mutation count | Mutations beyond authorization boundary | 0 |
| M10 | Exact artifact rehearsal | Exact distributed artifact + exact operator workflow proven | PASS |
| M11 | Production validator parity | Release rehearsal uses production policy/validator byte-identically | PASS |
| M12 | Target-state fidelity | Actual topology or bound equivalent fixture covers known conditions | PASS |
| M13 | Failure-path coverage | Material preserve-state failure paths rehearsed / planned paths | 100% |
| M14 | Independent review coverage | Release-authorizing controls independently derived and verified | 100% |
| M15 | Deterministic rebuild | Byte-identical rebuild when determinism claimed | PASS |
| M16 | Evidence completeness | Required evidence artifacts present/valid / required artifacts | 100% |
| M17 | Recoverability proof | Recovery point + bundle/archive verify + clean restore/clone proof | PASS |
| M18 | Security guardrail violations | Secret exposure, bypass, force push, unauthorized cleanup, firewall/runtime weakening, etc. | 0 |
| M19 | Owner exception count | Approved exceptions in period | 0 preferred; every exception exact/bound |
| M20 | External blocker events | Service/dependency incidents that block planned gate | Track; separate from internal defects |
| M21 | External blocker hold time | Time blocked by external service | Track |
| M22 | Active engineering/operator time | Measured active work, excluding external/user hold | Track |
| M23 | Rework ratio | Active rework time / total active work time | Downward trend |
| M24 | Test iteration count | Qualification runs by test layer and result | Track; minimize repeats |
| M25 | Repeat-defect rate | Defects violating an already-recorded lesson/control / total defects | 0 |

M25 numeric records must carry `numerator` equal to the repeated-defect count and `denominator` equal to the total defect count; both are validated against the bound defect ledger before the percentage is accepted.
| M26 | Handoff completeness | Required handoff sections/evidence/metrics present / required | 100% |
| M27 | Metrics data quality | Metrics with evidence and defined collection method / required metrics | 100% |
| M28 | Runtime/security baseline drift | Unauthorized changes to protected runtime/security state | 0 |

## Data-quality rule

Allowed states are `MEASURED`, `DERIVED`, `UNKNOWN`, and `NOT_APPLICABLE`. `UNKNOWN` and `NOT_APPLICABLE` require a reason and null value. Measured/derived values require collection method and evidence. Denominator-zero ratio metrics are `NOT_APPLICABLE` unless the canonical policy explicitly defines another behavior; they are never converted to artificial 100 percent.

M27 is derived from M01-M26 and M28 to avoid self-reference. A metric counts as data-quality complete when measured/derived evidence and collection method exist, or when policy-supported `NOT_APPLICABLE` is explicitly justified. `UNKNOWN` lowers M27.

## Timing calculations

- M21 = sum of `HOLD_EXTERNAL` seconds.
- M22 = sum of `ACTIVE_ENGINEERING`, `ACTIVE_OPERATOR`, and `REWORK` seconds; both external and user hold are excluded.
- M23 = `REWORK` seconds / M22 active seconds. If M22 is zero, M23 is `NOT_APPLICABLE` or `UNKNOWN`.
- Timing intervals may not overlap under policy R1.

## Test and defect calculations

M24 is a distribution of qualification runs by test layer and result. Each run carries test ID, requirement ID, production function/path, fixture provenance, expected-result source, actual result, mutation boundary, cleanup/preserve behavior, evidence artifact, and release-authorizing flag.

M25 counts a defect as repeated only when its record links to the prior lesson/control it violates. With zero defects, M25 is `NOT_APPLICABLE` rather than an invented percentage.

## Handoff completeness

A `HANDOFF` snapshot must include every component listed by policy in canonical order, each `PRESENT` with path and SHA-256. M26 must equal 100 percent. JSON is canonical; CSV is a deterministic projection and is cross-validated row-for-row.

## Lifecycle and deviation governance

Use only policy lifecycle transitions. `RELEASE_RESET_REQUIRED` may return only to read-only planning or design qualification. Every deviation requires unique identity, UTC timestamp, category, planned/observed condition, impact, mutation status, evidence reference, owner disposition, and permanent-control decision.

## Collection cadence

Record a full snapshot at workstream start, closeout, and handoff. Record gate/event data at every gate, deviation/failure, release reset, live attempt, and material external blocker. Do not reconstruct avoidable metrics from memory after the fact.

## Security/privacy

Metrics records may not contain raw tokens, credentials, unnecessary PII, runtime dumps, raw prompts, or surveillance telemetry. Evidence uses repository-relative paths with optional SHA-256 binding or non-secret external artifact/incident identities.

## Supplemental assurance KRIs

M04/M05 track user-visible replacement and material failure history; M24/M25 track test iterations and repeated control defects. They must not be interpreted as proof that the qualification model was complete. When a state-oracle assurance reset applies, add the following non-substitutive KRIs to release/handoff evidence: applicable oracle-cell coverage percent, independent-versus-implementation expectation delta count, unhandled exception surface count, undispositioned Git-state class count, unresolved material finding count, exact-base freshness, and trust-root migration/bootstrap status.

Do not invent success values. Unknown remains UNKNOWN; a blocked review remains HOLD. A material post-publication qualification escape increments the defect/CAPA lineage even when the technical correction is later successful.

## Post-R1 process assurance metrics

```text
PROCESS_ASSURANCE_METRICS=P01-P14
M01_M28_SEMANTICS_UNCHANGED=TRUE
PROCESS_METRICS_POLICY=config/adp-process-institutionalization-policy.json
```

P01-P14 measure assurance-process effectiveness and are carried by future governed handoffs. They supplement, but do not alter, M01-M28 transition metric semantics. UNKNOWN is not zero. Accepted risk is tracked explicitly and may not be represented as PASS.
