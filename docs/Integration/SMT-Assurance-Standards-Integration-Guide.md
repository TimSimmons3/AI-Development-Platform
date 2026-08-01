# SMT Assurance Standards Integration Guide

## 1. Canonical files

The ADP repository must retain these canonical assurance records:

```text
skills/smt-high-assurance-engineering-delivery/SKILL.md
docs/Standards/SMT-Global-Code-and-Artifact-Preflight-Checklist.md
docs/Standards/SMT-Live-Change-and-External-API-Validation-Standard.md
docs/Integration/SMT-Assurance-Standards-Integration-Guide.md
```

Every new release plan, major-section handoff, code-generation request, package, and live-change gate must reference the first three files.

Every new-chat handoff must include:

```text
APPLY_HIGH_ASSURANCE_SKILL=TRUE
APPLY_GLOBAL_PREFLIGHT_CHECKLIST=TRUE
APPLY_LIVE_CHANGE_STANDARD=TRUE
LIVE_ATTEMPT_BUDGET=1
USER_VISIBLE_REPLACEMENT_PACKAGE_TARGET=0
```

## 2. ADP repository architecture resolution

ADP uses:

```text
docs/ADP-Engineering-Log.md
```

as its canonical running record. Detailed plans, decisions, corrections, validation records, and closeout records belong under `docs/Releases`.

ADP does not currently use a root `CHANGELOG.md`, a global document-hierarchy file, a global decision register, or a release-plan template. Do not create duplicate governance structures solely to satisfy a generic adoption checklist.

For ADP:

- update `docs/ADP-Engineering-Log.md`;
- create a release plan under `docs/Releases`;
- create a narrowly scoped adoption decision record under `docs/Releases`;
- create and maintain the assurance delta traceability matrix under `docs/Standards`;
- place the integration guide under `docs/Integration`;
- require future plans and handoffs to reference the canonical assurance records.

## 3. Integration procedure

The documentation-only adoption change must:

1. verify the clean authorized repository baseline;
2. verify source hashes and provenance;
3. install the three canonical assurance records;
4. install this integration guide;
5. integrate the complete ADP v2.4 mandatory delta;
6. create the v2.5 integration plan;
7. create the adoption decision record;
8. create the requirement traceability matrix;
9. append the implementation record to the engineering log;
10. validate exact changed paths, links, headings, ASCII, hashes, and working-tree state;
11. perform independent review before commit and push;
12. publish closeout only after remote state and recoverability are verified.

Do not combine this adoption with Candidate-v7 promotion, counted RAG execution, witness control changes, registry changes, runtime changes, or Timeshift creation.

## 4. Validation and revision policy

The initial source package provides the authoritative July 29 assurance baseline. The August 1 ADP v2.4 handoff provides the mandatory delta.

The adopted files must preserve baseline intent while adding every mandatory v2.4 control. Implementation or review defects use corrected revisions, not new product versions. A new conceptual version is warranted only when architecture or external contract changes materially.

## 5. Skill limitation

These records are repository-integrated governance controls. They do not alter ChatGPT system instructions or built-in product skills. Compliance becomes durable when the files are committed, referenced by project governance, and applied in each future workstream.

## 6. Adoption acceptance criteria

```text
SKILL_FILE_COMMITTED=PASS
PREFLIGHT_STANDARD_COMMITTED=PASS
LIVE_CHANGE_STANDARD_COMMITTED=PASS
INTEGRATION_GUIDE_COMMITTED=PASS
V2_4_DELTA_TRACEABILITY=PASS
ADOPTION_DECISION_RECORDED=PASS
ENGINEERING_LOG_UPDATED=PASS
RELEASE_AND_HANDOFF_REFERENCE_RULE=PASS
LINK_AND_HASH_VALIDATION=PASS
INDEPENDENT_REVIEW=PASS
REMOTE_STATE_VERIFIED=PASS
RECOVERABILITY_VERIFIED=PASS
```

No future ADP live-change package may be authorized until these criteria pass or an explicit separately governed exception is approved.
