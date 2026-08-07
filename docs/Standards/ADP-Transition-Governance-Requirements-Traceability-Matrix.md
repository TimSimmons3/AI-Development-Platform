# ADP Transition Governance Requirements Traceability Matrix

## Control block

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

## Scope

Baseline: `311642c7465a01ada8297f8242b3d6e73033fed6`. Source: final ADP v2.4 R2 handoff package plus independently qualified R1-CR1 design.

| Requirement | Implemented control | Qualification method |
|---|---|---|
| M01-M28 canonical definitions | `config/transition-metrics-policy.json` | policy/order/schema tests |
| Unknown is not zero | transition validator data-quality rules | negative tests |
| Start/gate/closeout/handoff collection | snapshot/event schema | valid-record tests |
| Lifecycle state machine | policy allowed transitions | valid/invalid transition tests |
| Deviation fields | event validator | missing-field tests |
| CRn/external incident/freeze rules | transition standard + event validator | external/frozen negative tests |
| M21-M23 timing | interval ledger/calculation | overlap/hold/rework tests |
| M24 iterations | structured test run metadata | distribution/missing-metadata tests |
| M25 repeats | defect ledger + prior-control link | repeat-link negative test |
| M26 handoff completeness | 14-component policy set | missing-component and JSON/CSV tests |
| M27 data quality | validator-derived percentage | UNKNOWN/data-quality tests |
| Prior handoff trend | prior-handoff binding | missing-binding test |
| Change record minimum | Markdown assignment validator | missing-field test |
| Handoff/closeout/gate metrics link | Markdown assignment validator | missing-link test |
| Historical compatibility | changed-path/file-scope design | regression tests |
| Existing invariant chain | unchanged validator/policy + same workflow | full repo unit tests |
| Security/privacy | safe path/reference and no live API | path/symlink tests + source review |
| Protected publication boundary | addendum/plan | manual pre-publication gate |

## Final assurance state/equivalence traceability

The coarse requirement rows above remain historical summary evidence. Release authorization is now traced through `config/adp-transition-governance-final-assurance-state-oracle-r1.json` and `docs/Standards/ADP-Transition-Governance-Final-Assurance-State-Oracle-R1.md`, which enumerate 108 independent cells across Git change discovery, mandatory invariants, transition policy, governance identity, reference graph, parser/schema, workflow trust root, and reporting/process controls.

Finding 17 is explicitly represented by `GIT-11` (regular file -> symlink type change) and is controlled by ARC-01/ARC-02. Every oracle cell maps to one or more ARC-01..ARC-13 controls and must produce a qualification disposition; applicable coverage must be 100% and independent-versus-implementation expectation delta must be zero before release.
