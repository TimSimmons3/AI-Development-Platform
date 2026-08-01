# SMT ADP v2.4 Assurance Delta Traceability Matrix

## 1. Purpose

Map every mandatory ADP v2.4 assurance requirement to the revised canonical skill, preflight checklist, and live-change standard.

## 2. Source boundary

```text
BASELINE_SOURCE_DATE=2026-07-29
MANDATORY_DELTA_SOURCE_DATE=2026-08-01
BASELINE_COMMIT=12cfc9f41f10b95464f7a1848ab000319fff5d6b
REQUIREMENT_COUNT=18
```

## 3. Traceability

| ID | Mandatory requirement | Skill | Checklist | Live-change standard | Status |
|---|---|---|---|---|---|
| 9.1 | Validation claim levels | Skill 13.1 | Checklist 9.1 | Live 11 | Integrated |
| 9.2 | Production and test call-path parity | Skill 13.2 | Checklist 9.1 | Live 12 | Integrated |
| 9.3 | Exact launcher and prompt rehearsal | Skill 13.2 | Checklist 9.2 | Live 13 | Integrated |
| 9.4 | Agent-only signing | Skill 13.3 | Checklist 9.2 | Live 14 | Integrated |
| 9.5 | Namespace-specific SSH signing | Skill 13.3 | Checklist 9.2 | Live 15 | Integrated |
| 9.6 | Parent tree and diff controls | Skill 13.4 | Checklist 9.3 | Live 16 | Integrated |
| 9.7 | API contract and permission matrix | Skill 13.5 | Checklist 9.3 | Live 17 | Integrated |
| 9.8 | Final pre-mutation recheck | Skill 13.6 | Checklist 9.4 | Live 18 | Integrated |
| 9.9 | Collection-wide evidence identity | Skill 13.7 | Checklist 9.4 | Live 19 | Integrated |
| 9.10 | Raw evidence and semantic projection | Skill 13.7 | Checklist 9.4 | Live 20 | Integrated |
| 9.11 | Timestamp semantics | Skill 13.7 | Checklist 9.4 | Live 20 | Integrated |
| 9.12 | Failure evidence sealer | Skill 13.8 | Checklist 9.5 | Live 21 | Integrated |
| 9.13 | Visible failure preservation | Skill 13.8 | Checklist 9.5 | Live 22 | Integrated |
| 9.14 | Schema and hash dependency graph | Skill 13.9 | Checklist 9.5 | Live 23 | Integrated |
| 9.15 | Deterministic tests | Skill 13.9 | Checklist 9.5 | Live 23 | Integrated |
| 9.16 | Timeshift and tabular parser rule | Skill 13.10 | Checklist 9.5 | Live 23 | Integrated |
| 9.17 | Communication truthfulness | Skill 13.11 | Checklist 9.6 | Live 24 | Integrated |
| 9.18 | Live-iteration governance | Skill 13.11 | Checklist 9.6 | Live 24 | Integrated |

## 4. Cross-cutting adoption controls

The integration guide resolves ADP repository architecture, required references, adoption procedure, and acceptance criteria.

The v2.5 integration plan records scope, exclusions, source and dependency inventories, mutation boundaries, test matrix, independent-review plan, and authorization status.

The adoption decision records the governance decision and explicitly prohibits live-change authorization until validated adoption is complete.

## 5. Validation rule

A requirement is integrated only when:

1. the normative rule exists in the skill or live-change standard;
2. the operational check exists in the preflight checklist;
3. this matrix identifies the exact controlling sections;
4. independent review confirms semantic coverage rather than keyword presence.

```text
TRACEABILITY_STATUS=COMPLETE_PENDING_REPOSITORY_VALIDATION
LIVE_CHANGE_AUTHORIZATION=HOLD
```
