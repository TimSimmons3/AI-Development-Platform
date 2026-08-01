# ADP v2.5 High-Assurance Standards Adoption Decision

## 1. Decision identity

```text
DECISION_ID=ADP-DEC-2026-08-01-HA-001
DECISION_STATUS=APPROVED_FOR_LOCAL_DOCUMENTATION_IMPLEMENTATION
EFFECTIVE_ADOPTION_STATUS=PENDING_VALIDATION_COMMIT_PUSH_AND_INDEPENDENT_VERIFICATION
BASELINE_COMMIT=12cfc9f41f10b95464f7a1848ab000319fff5d6b
```

## 2. Decision

ADP will adopt the repository-integrated SMT high-assurance skill, global preflight checklist, live-change and external-API validation standard, integration guide, and the complete mandatory ADP v2.4 assurance delta.

No future ADP live-change package may be authorized until adoption acceptance criteria are verified or a separately governed exception is approved.

## 3. Repository architecture adjudication

The following ADP architecture is authoritative:

- `docs/ADP-Engineering-Log.md` is the canonical running record.
- Detailed plans, decisions, corrections, validation records, and closeout records remain under `docs/Releases`.
- Standards remain under `docs/Standards`.
- Repo-integrated skills remain under `skills`.
- The integration guide belongs under `docs/Integration`.

ADP does not currently use a root changelog, global document hierarchy, global decision register, or release-plan template. Creating those structures solely for this adoption would duplicate governance and create scope creep.

This decision record satisfies the required adoption-decision function without creating a new global register. Future release plans and handoffs must reference the canonical assurance files directly.

## 4. Rationale

ADP v2.4 demonstrated that package-level validation alone did not prevent defects in Git tree construction, signing flow, external-contract interpretation, evidence sealing, snapshot parsing, or release communication.

The August 1 closeout handoff therefore made the v2.4 assurance delta mandatory before any future live-change package. Integrating the controls now reduces the risk of repeated pre-mutation failures, invalid live-readiness claims, duplicate platform objects, hidden failure evidence, or incorrect preserve-state decisions.

## 5. Alternatives rejected

### Defer adoption until Candidate-v7 promotion

Rejected because live-change authorization is explicitly on HOLD until adoption.

### Create a root changelog and global governance registers

Rejected because ADP already has an established engineering log and release-record architecture. Duplicate structures would conflict with prior repository-architecture adjudication.

### Substitute existing ADP validation standards

Rejected because the existing ADP standards do not contain the complete mandatory v2.4 controls and are not proven equivalents of the SMT assurance records.

## 6. Authorization boundary

Approved:

- local creation of the seven new documentation files;
- local append to the engineering log;
- local validation and independent review.

Not approved:

- commit;
- push;
- tag;
- Timeshift snapshot;
- runtime or platform change;
- Candidate-v7 promotion;
- counted RAG execution;
- any ADP v2.4 witness, registry, receipt, or ruleset change.

## 7. Effectiveness criteria

The decision becomes effective adoption only after:

```text
EXACT_CHANGED_PATHS=PASS
CONTENT_AND_TRACEABILITY=PASS
INDEPENDENT_REVIEW=PASS
COMMIT=PASS
PUSH=PASS
REMOTE_STATE_VERIFIED=PASS
RECOVERABILITY=PASS
```
