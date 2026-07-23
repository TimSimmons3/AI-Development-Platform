# ADP v2.4 Isolated Validation Runtime Operator Guide

## 1. Current Status

```text
GUIDE_STATUS=NON_COUNTED_RAG_PROCEDURE_DEFINED_EXECUTION_HELD
RUNTIME_CREATION_BASELINE_TAG=adp-v2.4-pre-runtime-controls-v2
MODEL_IMPORT_CORRECTION_TAG=adp-v2.4-model-import-envelope-correction
HISTORICAL_RUNTIME_RESILIENCE_TAG=adp-v2.4-runtime-resilience-controls
RUNTIME_RESILIENCE_CORRECTION_TAG=adp-v2.4-runtime-resilience-controls-v2
NON_COUNTED_RAG_PROCEDURE_FREEZE_TAG=adp-v2.4-non-counted-rag-dry-run-procedure-freeze
RUNTIME_ENTRY_GATE=scripts/adp24_isolated_runtime_preflight.sh
RESTART_PERSISTENCE_SCRIPT=scripts/adp24_validation_restart_persistence.sh
NON_COUNTED_RAG_CONTRACT=artifacts/Configuration/ADP-v2.4/non-counted-rag-dry-run-contract.json
NON_COUNTED_RAG_PROCEDURE=docs/Operations/ADP-v2.4-Isolated-Validation-Non-Counted-RAG-Dry-Run-Procedure.md
FIVE_PASS_READINESS_STANDARD=docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md
EVIDENCE_WORKSPACE_GIT_IGNORE=REQUIRED
PRIMARY_INSTANCE_CHANGE=NONE
MODEL_SYNC_OPERATION=PROHIBITED
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

## 2. Current Controlled Position

The isolated container and volume were created under the runtime-creation baseline. The model-import envelope correction was promoted and the corrected deterministic model was imported exactly once. An accidental post-import toggle was diagnosed and corrected before counted execution. The model is active, has the approved deterministic parameters, and has no Knowledge, tool, skill, function, filter, file, or access-grant association.

The post-import runtime manifest, cold-volume backup, corrected runtime-resilience promotion, and controlled restart-persistence gate passed. The single-case non-counted RAG procedure is defined, but Knowledge upload and dry-run execution remain blocked pending a separate five-pass readiness review and explicit authorization.

Preserve the voided pre-runtime workspace and the active corrected-attempt workspace unchanged except for newly authorized evidence files.

## 3. Corrected Model-Import Workflow

1. Validate the model-import correction tag and controlled reset workspace.
2. Revalidate the retained runtime and original raw export.
3. Generate and independently validate the corrected top-level-array import payload.
4. Import the corrected payload exactly once through Workspace, Models, Import.
5. Do not use Sync.
6. Verify exactly one active deterministic model with temperature 0 and seed 42.
7. Verify no model associations or access grants.
8. Capture the runtime manifest.
9. Create and validate the post-import cold-volume backup.
10. Stop for review.

## 4. Restart-Persistence Workflow

After the corrected runtime-resilience v2 controls are promoted and separately authorized:

1. Confirm the active reset evidence workspace.
2. Confirm `10-restart-before.txt` and `11-restart-after.txt` do not exist.
3. Run `scripts/adp24_validation_restart_persistence.sh --execute`.
4. Allow transient `starting` or `unhealthy` states during the bounded readiness wait.
5. Stop immediately for `exited`, `dead`, timeout, semantic drift, model drift, volume drift, primary-instance degradation, or repository change.
6. Return both evidence hashes and the consolidated gate result.
7. Do not begin the non-counted dry run until the restart-persistence gate is reviewed.

The authoritative procedure is `docs/Operations/ADP-v2.4-Isolated-Validation-Restart-Persistence-Procedure.md`.

## 5. Non-Counted RAG Dry-Run Workflow

After the procedure-freeze commit and annotated tag are promoted, the five-pass readiness review passes, and execution is separately authorized:

1. Confirm the active reset evidence workspace.
2. Confirm evidence files 12 through 17 do not exist.
3. Revalidate the restart evidence, post-import backup, runtime, model, source, cases, template, and contract.
4. Create exactly one isolated validation Knowledge collection named `ADP-v2.4-AURORA-24-KITE-Non-Counted`.
5. Upload exactly one synthetic source file.
6. Start one fresh chat with the deterministic model.
7. Attach the collection at chat level only.
8. Submit provisional Case C exactly once.
9. Capture the exact raw response and source panel.
10. Run the frozen factual-content and citation-shape classifier.
11. Stop regardless of result and return the complete evidence set for review.
12. Do not run Cases A, B, or D and do not retry Case C.

The authoritative contract is `artifacts/Configuration/ADP-v2.4/non-counted-rag-dry-run-contract.json`.

The authoritative procedure is `docs/Operations/ADP-v2.4-Isolated-Validation-Non-Counted-RAG-Dry-Run-Procedure.md`.

## 6. Backup Protection

New backups must be created in a mode-700 directory. The archive and checksum file must be owned by the invoking host user and have mode 600.

The post-import archive created before this hardening remains byte-valid and checksum-valid inside a mode-700 directory. Its historical ownership and mode are evidence and do not invalidate its contents. Do not alter that historical artifact without a separately recorded metadata-normalization action.

## 7. Evidence Workspaces

Voided historical workspace:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/20260722T215656Z/
```

Corrected attempt workspace pattern:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Model-Import-Reset/<UTC-PACKET-ID>/
```

Both workspace roots are ignored by Git because they may contain restricted raw exports, local screenshots, and runtime transcripts. Do not use Git ignore status as permission to retain secrets.

## 8. Human Evidence Actions

For each Firefox action, save the screenshot using the exact filename from the active evidence filename map.

Do not capture passwords, session cookies, API keys, browser password-manager prompts, unrelated chats, or unnecessary email addresses.

For raw text evidence, preserve the exact assistant response without correction, paraphrase, source-panel labels, or added commentary.

## 9. Immediate Stop Conditions

Stop for any repository-baseline mismatch, evidence workspace not ignored by Git, primary-instance degradation, validation-container terminal state, wrong user or administrator count, wrong model count, model parameter drift, nonempty model association, wrong volume, failed backup, failed checksum, missing evidence, wrong filename, semantic restart drift, unexpected repository change, wrong collection, wrong source, premature prompt submission, prompt retry, regeneration, or response editing.

Do not improvise around a stop condition. Preserve evidence and return the consolidated bundle.
