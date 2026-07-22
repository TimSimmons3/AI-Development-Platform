# ADP v2.4 Isolated Validation Runtime Operator Guide

## 1. Current Status

```text
GUIDE_STATUS=MODEL_IMPORT_CORRECTION_CANDIDATE_NOT_PROMOTED
RUNTIME_CREATION_BASELINE_TAG=adp-v2.4-pre-runtime-controls-v2
MODEL_IMPORT_CORRECTION_TAG=adp-v2.4-model-import-envelope-correction
RUNTIME_ENTRY_GATE=scripts/adp24_isolated_runtime_preflight.sh
PRE_PROMOTION_QUALITY_GATE=HISTORICAL_NOT_RUNTIME
EVIDENCE_WORKSPACE_GIT_IGNORE=REQUIRED
PRIMARY_INSTANCE_CHANGE=NONE
MODEL_SYNC_OPERATION=PROHIBITED
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

## 2. Current Controlled Position

The isolated container and volume were created under the runtime-creation baseline and are currently retained in an administrator-only state. The first model-import attempt is void because the prior sanitized payload used an incompatible wrapper object. The target model count was verified as zero after the failed attempt.

Do not reuse the voided pre-runtime workspace as the active corrected-attempt workspace. Preserve it unchanged.

## 3. Corrected Model-Import Workflow

1. Promote the model-import envelope correction and create the annotated correction tag.
2. Create one unique evidence workspace under `artifacts/Evidence/ADP-v2.4-Isolated-Validation-Model-Import-Reset/`.
3. Create the controlled reset reference record using the exact filename from `artifacts/Configuration/ADP-v2.4/model-import-reset-evidence-filename-map.json`.
4. Revalidate the retained runtime: healthy container, healthy primary instance, one isolated user, one isolated administrator, zero target models, valid pristine backup, and clean repository.
5. Revalidate the prior raw export SHA-256.
6. Run the corrected `scripts/adp24_validate_model_export.py` and write new report and sanitized import outputs into the reset workspace.
7. Run `scripts/adp24_validate_model_import_payload.py` against the corrected sanitized import.
8. Stop and return the new hashes for import authorization.
9. After separate authorization, open Workspace, open Models, and choose Import.
10. Select the corrected sanitized import file in the file picker.
11. Capture the selected file in the file picker before clicking Open.
12. Click Open. The v0.10.2 import begins immediately; there is no later confirmation button.
13. Confirm exactly one deterministic model appears.
14. Do not use Sync.
15. Run read-only post-import verification.
16. Capture the runtime manifest and post-import volume backup.
17. Perform the separately frozen restart-persistence check.
18. Perform the separately frozen non-counted dry run.

## 4. Evidence Workspaces

Voided historical workspace:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/20260722T215656Z/
```

Corrected attempt workspace pattern:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Model-Import-Reset/<UTC-PACKET-ID>/
```

Both workspace roots are ignored by Git because they may contain restricted raw exports, local screenshots, and runtime transcripts. Do not use Git ignore status as permission to retain secrets.

The prior raw export may be read from the voided workspace only for the exact corrected-sanitizer purpose authorized by the model-import envelope amendment and only after SHA-256 revalidation.

## 5. Human Evidence Actions

For each Firefox action, save the screenshot using the exact filename from the active evidence filename map.

Do not capture:

- Passwords
- Session cookies
- API keys
- Email addresses unless unavoidable for account evidence
- Browser password-manager prompts
- Unrelated chats or data

## 6. Immediate Stop Conditions

Stop for any repository-baseline mismatch, evidence workspace not ignored by Git, primary-instance degradation, validation-container degradation, wrong user or administrator count, nonzero target model count before corrected import, raw-export checksum mismatch, import payload not a top-level array, model mismatch, secret-bearing export, nonempty model association, wrong volume, failed backup, failed checksum, missing screenshot, wrong filename, or unexpected repository change.

Do not improvise around a stop condition. Preserve evidence and return the consolidated bundle.
