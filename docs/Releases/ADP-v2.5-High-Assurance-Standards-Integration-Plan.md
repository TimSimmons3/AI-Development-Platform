# ADP v2.5 High-Assurance Standards Integration Plan

## 1. Status

```text
WORKSTREAM=ADP_v2_5_HIGH_ASSURANCE_STANDARDS_INTEGRATION
WORKSTREAM_CLASS=DOCUMENTATION_AND_GOVERNANCE_ONLY
PLAN_STATUS=APPROVED_FOR_LOCAL_DOCUMENTATION_IMPLEMENTATION
BASELINE_COMMIT=12cfc9f41f10b95464f7a1848ab000319fff5d6b
TIMEZONE=America/Chicago
DATA_CURRENCY=2026-08-01
LOCAL_REPOSITORY=~/Labs/AI-Development-Platform
REMOTE_REPOSITORY=git@github.com:TimSimmons3/AI-Development-Platform.git
```

## 2. Objective

Integrate the authoritative July 29 assurance baseline and the mandatory August 1 ADP v2.4 assurance delta into the ADP repository before any future live-change package is authorized.

## 3. Authorized scope

The local documentation implementation may change exactly these repository paths:

```text
docs/ADP-Engineering-Log.md
docs/Integration/SMT-Assurance-Standards-Integration-Guide.md
docs/Releases/ADP-v2.5-High-Assurance-Standards-Adoption-Decision.md
docs/Releases/ADP-v2.5-High-Assurance-Standards-Integration-Plan.md
docs/Standards/SMT-Global-Code-and-Artifact-Preflight-Checklist.md
docs/Standards/SMT-Live-Change-and-External-API-Validation-Standard.md
docs/Standards/SMT-v2.4-Assurance-Delta-Traceability-Matrix.md
skills/smt-high-assurance-engineering-delivery/SKILL.md
```

The documentation installer must not commit, push, tag, create a snapshot, or change runtime state.

## 4. Explicit exclusions

This workstream excludes:

- Candidate-v7 promotion;
- counted RAG execution;
- Epoch-1 or Epoch-2 witness changes;
- authorization-registry or lock changes;
- ruleset changes;
- Open WebUI, Ollama, model, corpus, Docker, firewall, or network changes;
- Timeshift creation;
- root changelog creation;
- creation of a global document hierarchy, decision register, or release template solely for this adoption.

## 5. Source inventory

The July 29 baseline is bound to the validated assurance archive and its package manifest. The August 1 delta is bound to the final handoff.

| Source identity | Provenance and role | Source date (America/Chicago) | Size bytes | SHA-256 |
|---|---|---|---:|---|
| `ADP-v2.4-Phase2-Handoff-and-Assurance-MDs.zip` | Validated outer archive containing the authoritative July 29 assurance baseline; ZIP CRC and package validation passed | `2026-07-29T17:09:00-05:00` | `46685` | `485615f3227aebf7febe361eb7556783360fc5213be119f305326473888ec845` |
| `ADP-v2.4-Phase2-New-Chat-Handoff-Package/skills/smt-high-assurance-engineering-delivery/SKILL.md` | Archive member; canonical skill baseline; standalone copy hash-matched during read-only inventory | `2026-07-29T17:09:00-05:00` | `9435` | `41f981f19aaa79884a2b1d9677281c6ce0a2ed8f00df3580062b9a90a159daad` |
| `ADP-v2.4-Phase2-New-Chat-Handoff-Package/docs/Standards/SMT-Global-Code-and-Artifact-Preflight-Checklist.md` | Archive member; canonical preflight-checklist baseline | `2026-07-29T17:09:00-05:00` | `3754` | `308df182d0d0049ee6e6d2d72b48e85e7f57249d09b46edd5f8ca9a6c339cb50` |
| `ADP-v2.4-Phase2-New-Chat-Handoff-Package/docs/Standards/SMT-Live-Change-and-External-API-Validation-Standard.md` | Archive member; canonical live-change-standard baseline | `2026-07-29T17:09:00-05:00` | `3360` | `6809704a1d5f4b107406f08ef8cb30444893f7e40e1d1eef1b96d5d13495d42d` |
| `ADP-v2.4-Phase2-New-Chat-Handoff-Package/docs/Integration/SMT-Assurance-Standards-Integration-Guide.md` | Archive member; integration baseline; standalone copy hash-matched during read-only inventory | `2026-07-29T17:09:00-05:00` | `1878` | `f29940d282484c7c501631c0630e2fd32d7f3397515c7ec28cd79bdb04ab590d` |
| `ADP-v2.4-Final-New-Chat-Handoff-R1.md` | User-provided authoritative final handoff; two local copies were byte-identical | `2026-08-01T07:42:00-05:00` | `26409` | `1e23b23f71575bab1ed36df8a9d6078e994c3ed649af2474aa2914b2c7cfa9cd` |

## 6. Dependency inventory

Required host capabilities:

```text
python3
git
sha256sum
unzip
```

No network, external API, package installation, elevated privilege, or runtime service dependency is required for local documentation implementation.

## 7. External-contract inventory

```text
EXTERNAL_CONTRACT_INVENTORY=NOT_APPLICABLE
RATIONALE=LOCAL_DOCUMENTATION_ONLY_NO_EXTERNAL_API_OR_PLATFORM_MUTATION
```

Git remote state remains read-only until a later separately validated commit-and-push gate.

## 8. Mutation and preserve-state boundaries

The first mutation is creation of the first new canonical assurance file in the local working tree.

Before mutation require:

- branch `main`;
- exact baseline commit;
- clean working tree;
- expected origin URL;
- all seven new target paths absent;
- engineering log present;
- package manifest and payload hashes valid.

On a pre-mutation mismatch, stop without mutation.

After the first mutation, do not automatically rollback. Preserve the exact local state and report. Git remains the recovery mechanism because the starting tree is clean and no commit or push occurs.

## 9. Validation plan

Required local validation:

- Python AST and compile validation;
- package ZIP CRC, safe path, duplicate, symlink, mode, manifest, and hash validation;
- clean extraction;
- exact target-path set;
- one H1 per Markdown file;
- ASCII and LF line endings;
- required assurance tokens and all 18 delta identifiers;
- link and path existence;
- engineering-log marker exactly once;
- no unexpected repository path changes;
- no commit, push, tag, snapshot, or runtime mutation.

## 10. Independent review plan

The independent review must:

- derive the expected eight changed paths separately;
- verify the baseline and delta sources independently;
- verify all 18 requirements against the revised skill, checklist, live-change standard, and traceability matrix;
- inspect `git diff --check`;
- inspect the full staged candidate diff before any commit;
- verify no unrelated ADP v2.4 evidence or controls changed;
- verify local-only implementation and absence of remote mutation.

## 11. Iteration budget

```text
USER_VISIBLE_REPLACEMENT_PACKAGES_TARGET=0
LOCAL_MUTATION_ATTEMPTS_PER_GATE_MAX=1
AUTOMATIC_PATCH_AND_RETRY=PROHIBITED
REMOTE_MUTATION_ATTEMPTS=0
```

A pre-mutation HOLD does not consume the local mutation attempt. A post-mutation defect requires preserve-state adjudication and independent review.

## 12. Gate status at plan approval

```text
INTENT_DEFINED=PASS
AUTHORITY_CONFIRMED=PASS_LOCAL_DOCUMENTATION_ONLY
SOURCE_INVENTORY=PASS
DEPENDENCY_INVENTORY=PASS
EXTERNAL_CONTRACT_INVENTORY=NOT_APPLICABLE
DESIGN_REVIEW=PASS
MUTATION_BOUNDARY=PASS
PRESERVE_STATE_BOUNDARY=PASS
FAILURE_DISPOSITION_MATRIX=PASS
TEST_PLAN=PASS
INDEPENDENT_REVIEW_PLAN=PASS
IMPLEMENTATION_AUTHORIZATION=PASS_LOCAL_DOCUMENTATION_ONLY
COMMIT_AUTHORIZATION=HOLD
PUSH_AUTHORIZATION=HOLD
LIVE_CHANGE_AUTHORIZATION=HOLD
```
