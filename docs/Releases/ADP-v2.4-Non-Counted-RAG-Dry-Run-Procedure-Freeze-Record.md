# ADP v2.4 Non-Counted RAG Dry-Run Procedure-Freeze Record

## 1. Status

```text
FREEZE_RECORD_STATUS=PROCEDURE_FREEZE_DEFINED_EXECUTION_NOT_AUTHORIZED
STARTING_COMMIT=83e0103ab6daa67c822763769e9c685b7d38ac6b
IMPLEMENTATION_BRANCH=adp-v2.4-non-counted-rag-procedure-freeze
PROCEDURE_FREEZE_TAG=adp-v2.4-non-counted-rag-dry-run-procedure-freeze
RUNTIME_MUTATION=NONE
KNOWLEDGE_UPLOAD_AUTHORIZATION=HOLD
NON_COUNTED_RAG_EXECUTION_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

## 2. Decision

The technical runtime baseline and restart-persistence evidence passed. Non-counted RAG execution remains blocked because the repository did not contain a frozen upload, attachment, single-prompt, response-capture, citation-classification, evidence, and stop-condition procedure.

The correction is a direct Git-native procedure-freeze change. It does not use a self-extracting packet or recursive execution wrapper.

## 3. Selected Dry-Run Scope

Only provisional Case C is selected:

```text
PROMPT=State the verification color and review window for AURORA-24-KITE.
EXPECTED_FACTUAL_ANSWER=The verification color for AURORA-24-KITE is amber, and the review window is thirty-six hours.
```

Case C provides the bounded two-fact retrieval needed to observe multi-fact answer behavior. Cases A, B, and D remain unexecuted and provisional for later counted-run design.

## 4. Citation Design

The existing exact-answer validator rejects any inline citation as a factual mismatch. The approved RAG template requests a citation when the context contains a source id, while prior deterministic evidence did not establish one stable inline citation format.

The new non-counted classifier therefore separates:

- Exact factual content
- No inline citation
- Numeric bracket citation, such as `[1]`
- Source-id bracket citation, such as `[AURORA-24-KITE]`

The classification is observational only. The final counted citation policy remains blocked until the single dry run is reviewed.

## 5. Exact Write Set

The procedure-freeze change modifies exactly eight paths:

```text
M  artifacts/Configuration/ADP-v2.4/model-import-reset-evidence-filename-map.json
A  artifacts/Configuration/ADP-v2.4/non-counted-rag-dry-run-contract.json
A  docs/Operations/ADP-v2.4-Isolated-Validation-Non-Counted-RAG-Dry-Run-Procedure.md
M  docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md
A  docs/Releases/ADP-v2.4-Non-Counted-RAG-Dry-Run-Procedure-Freeze-Record.md
A  docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md
A  scripts/adp24_non_counted_rag_procedure_freeze_quality_gate.sh
A  scripts/adp24_validate_non_counted_rag_response.py
```

The source, provisional test cases, approved template, deterministic model record, Compose files, runtime scripts, validation volume, model database, and evidence workspace are not modified.

## 6. Frozen Input Hashes

```text
SOURCE_SHA256=18dc6a195e566da27dd4fe4be525d716a32dd0c753b6f1890c9c2ad7c3e12cfd
TEST_CASES_SHA256=a631a0dfb0823ea7e24179b0f0113f057c79476e8e14e091f2c98a8a554357d9
TEMPLATE_SHA256=def3db3e05b1651aa33b921a03573074d8033ca5d2ce691446638e362ef92d96
MODEL_DISCOVERY_RECORD_SHA256=ed81f8a23aec8676f6a55d8034222ac92487e38f56e0f1a05798482c244a146a
RESTART_BEFORE_SHA256=86626ad992356b49eb9cbe8cf0c6624b09f7b5b6718d017c7a5a197eda23dd67
RESTART_AFTER_SHA256=3acfc43ccccc317259a80ccb0eb23d692327e9e2bf5ad55284cc1261ad68306c
STABLE_STATE_SHA256=ff524630a4c95728017f80cc5728aff5c70796db663ec833653071c7c3a73d60
POST_IMPORT_BACKUP_SHA256=93e615d0e7c0fae2c30b6f7d77b14437f76df76ef3278dfafb2d3e1a57928b12
```

## 7. Evidence Contract

Evidence files 12 through 17 become required for the selected single dry run. Their purposes are bound consistently in the active filename map and the new contract.

No prior dry-run evidence may be reused. Any material change after the Knowledge upload begins voids the non-counted attempt and requires preservation, review, and a separately authorized reset.

## 8. Promotion Requirements

Before Knowledge upload authorization:

1. Apply the transparent patch in a disposable worktree at the exact starting commit.
2. Pass the procedure-freeze quality gate.
3. Review the complete seven-path diff.
4. Commit and push the correction branch.
5. Fast-forward `main` and create the new annotated procedure-freeze tag.
6. Pass a post-promotion read-only gate.
7. Complete the five-pass readiness review under `docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md`.
8. Revalidate evidence collisions, runtime health, model state, primary health, source hashes, contract, and prior restart evidence.

## 9. Authorization Boundary

```text
PROCEDURE_FREEZE_IMPLEMENTATION_STATUS=DEFINED_AND_QUALITY_GATED
FIVE_PASS_READINESS_REVIEW=REQUIRED_BEFORE_EXECUTION
KNOWLEDGE_UPLOAD_AUTHORIZATION=HOLD_PENDING_SEPARATE_AUTHORIZATION
NON_COUNTED_RAG_EXECUTION_AUTHORIZATION=HOLD_PENDING_SEPARATE_AUTHORIZATION
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```
