# ADP v2.4 Isolated Validation Runtime Operator Guide

## 1. Current Status

```text
GUIDE_STATUS=NON_COUNTED_RAG_COMPLETE_FAILED_RESULT_PRESERVED_CANDIDATE_V7_C2_FINAL_FREEZE_COMPLETE
RUNTIME_CREATION_BASELINE_TAG=adp-v2.4-pre-runtime-controls-v2
MODEL_IMPORT_CORRECTION_TAG=adp-v2.4-model-import-envelope-correction
HISTORICAL_RUNTIME_RESILIENCE_TAG=adp-v2.4-runtime-resilience-controls
RUNTIME_RESILIENCE_CORRECTION_TAG=adp-v2.4-runtime-resilience-controls-v2
NON_COUNTED_RAG_PROCEDURE_FREEZE_TAG=adp-v2.4-non-counted-rag-dry-run-procedure-freeze
NON_COUNTED_RAG_RESULT=FAIL_PRESERVED_NO_RETRY
NON_COUNTED_RAG_RERUN_AUTHORIZATION=PROHIBITED
COUNTED_DESIGN_CANDIDATE=V7_C2_FINAL_FREEZE_COMMITTED_PENDING_EXTERNAL_EXECUTION_AUTHORIZATION
COUNTED_DESIGN_CONTRACT=artifacts/Configuration/ADP-v2.4/counted-rag-qualification-design-candidate-v7.json
COUNTED_BINDING_MANIFEST=artifacts/Configuration/ADP-v2.4/counted-rag-governing-bindings-v7.json
FIVE_PASS_READINESS_STANDARD=docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md
PRIMARY_INSTANCE_CHANGE=NONE
MODEL_SYNC_OPERATION=PROHIBITED
NON_COUNTED_REMEDIATION_REHEARSAL_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

## 2. Current Controlled Position

The isolated validation runtime, deterministic model, restart evidence, post-import backup, and non-counted evidence set are preserved. The single authorized non-counted Case C run completed once. Its factual retrieval passed, its required answer format failed, and its frozen classifier reported failure. The run is historical evidence and must not be retried, regenerated, edited, or reused as execution evidence for a replacement procedure.

Counted-design candidates v1 through v5 were rejected before commit and are superseded. Candidate v6 failed the required post-application independent full-diff review and is preserved only as superseded historical evidence. Candidate v7 C1 was independently reviewed and committed as signed commit `12fec97f9ef858c9aae5d844973b38d0f2cd1753`. Candidate v7 C2 is the final repository freeze. It does not authorize Knowledge upload, model mutation, a remediation rehearsal, a push, registry creation, or counted execution.

## 3. Historical Model-Import and Restart State

1. The corrected deterministic model was imported exactly once through the Open WebUI import operation.
2. Sync remains prohibited.
3. The approved model remains `llama-32-3b-rag-deterministic-test`, based on `llama3.2:3b`, with temperature `0` and seed `42`.
4. Model-level Knowledge, tools, skills, functions, filters, files, and access grants must remain absent.
5. Restart evidence 10 and 11 and the post-import backup remain immutable historical evidence.

## 4. Historical Non-Counted RAG Result

The authoritative historical procedure and contract remain unchanged:

```text
docs/Operations/ADP-v2.4-Isolated-Validation-Non-Counted-RAG-Dry-Run-Procedure.md
artifacts/Configuration/ADP-v2.4/non-counted-rag-dry-run-contract.json
```

The run used provisional Case C exactly once. Evidence files 12 through 17 are immutable. The result is:

```text
FACTUAL_RETRIEVAL_RESULT=PASS
ANSWER_FORMAT_ADHERENCE=FAIL
FROZEN_CLASSIFIER_RESULT=FAIL_PRESERVED
NON_COUNTED_RAG_DRY_RUN_RESULT=FAIL_PRESERVED_NO_RETRY
```

Do not follow the pre-execution steps in the historical procedure again. They are retained to show what governed the completed run, not to authorize another run.

## 5. Counted-Design Remediation Workflow

1. Work only from the clean disposable remediation worktree at the approved parent commit.
2. Treat candidates v1 through v5 as `SUPERSEDED_DO_NOT_COMMIT_DO_NOT_REAPPLY`.
3. Validate Candidate v7 C1 against the exact 68-path application manifest, Package v12 canonical trust bindings, and the frozen design-parent commit.
4. Require the response validator to separate factual truth, format, citation, source-panel, and unsupported-addition dimensions.
5. Require the binding validator to verify repository dependencies and to block execution until the final promotion commit and all external evidence bindings are frozen.
6. Run the complete fixture matrix, binding self-tests, output-collision tests, and full-diff independent review.
7. Stop for any defect. A material correction supersedes the candidate and requires a clean reset and new package.
8. Do not authorize a remediation rehearsal or counted execution from a design-candidate result.

## 6. Binding and Evidence Rules

Candidate v7 C2 preserves the reviewed C1 implementation and adds only the six frozen final-freeze paths. Design validation checks the 68-path C1 state, Package v12, and the signed workspace authorization. Promotion and execution validation must additionally bind the exact C1 or C2 commit and tree, governing records, immutable evidence, signer namespace, single-use authorization registry, and protected remote witness state.

A response validator may not run in execution context without a binding report that matches the exact contract and binding-manifest hashes and reports `EXECUTION_BINDING_VALIDATION=PASS`.

## 7. Evidence Workspaces

Voided historical workspace:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/20260722T215656Z/
```

Completed corrected-attempt workspace:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Model-Import-Reset/20260722T234427Z/
```

The completed workspace is historical and immutable. Any separately authorized remediation rehearsal requires a new evidence workspace, a new procedure version, new filenames, and a new five-pass readiness record.

## 8. Human Evidence Protection

Do not capture passwords, session cookies, API keys, browser password-manager prompts, unrelated chats, or unnecessary personal information. Preserve exact raw evidence without correction or paraphrase.

## 9. Immediate Stop Conditions

Stop for any baseline mismatch, stale status, changed historical evidence, failed hash, unexpected path, output collision, masked failure, model or access drift, primary-instance degradation, unsupported validator claim, fixture gap, self-matching audit logic, incomplete semantic traceability, unresolved material residual risk, or security exposure.

Do not improvise around a stop condition. Preserve the failed state as non-authorizing historical evidence and return to Pass 1 after a clean reset.

## 10. Candidate v7 C2 final-freeze state

```text
CANDIDATE_V7_STATE=C2_FINAL_FREEZE_COMMITTED_PENDING_EXTERNAL_EXECUTION_AUTHORIZATION
DESIGN_PARENT_COMMIT=b934c7bd84bfbc35563f3681712c4d5bd8478196
C1_PATH_COUNT=68
C2_PATH_COUNT=6
PACKAGE_V12_CANONICAL_TRUST_BINDING=REQUIRED
C1_COMMIT=12fec97f9ef858c9aae5d844973b38d0f2cd1753
C1_TREE=760a0da5f425a706b0e1e8cd3be3f0f6c0d5f6d4
C2_PATH_COUNT=6
C2_C1_REVIEW=docs/Releases/ADP-v2.4-Counted-Design-Candidate-v7-C1-Independent-Full-Diff-Review.md
C2_PROCEDURE_FREEZE=docs/Releases/ADP-v2.4-Counted-RAG-Candidate-v7-Final-Procedure-Freeze-Record.md
C2_ARTIFACT_MANIFEST=docs/Releases/ADP-v2.4-Counted-RAG-Candidate-v7-Final-Artifact-Manifest.md
GIT_PUSH_AUTHORIZATION=HOLD
C2_FINAL_FREEZE=COMPLETE_LOCAL_SIGNED_COMMIT
AUTHORIZATION_REGISTRY_CREATION=HOLD_PENDING_SIGNED_EXECUTION_AUTHORIZATION
RUNTIME_MUTATION=NONE
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

The Candidate v7 worktree remains isolated from `main`. C2 authorizes no runtime, Knowledge, model, collection, evidence-workspace, push, registry, or counted-execution action.
