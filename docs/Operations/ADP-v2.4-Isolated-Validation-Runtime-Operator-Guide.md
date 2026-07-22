# ADP v2.4 Isolated Validation Runtime Operator Guide

## 1. Current Status

```text
GUIDE_STATUS=CANDIDATE_NOT_RUNTIME_AUTHORIZED
RUNTIME_BASELINE_TAG=adp-v2.4-pre-runtime-controls-v2
RUNTIME_ENTRY_GATE=scripts/adp24_isolated_runtime_preflight.sh
PRE_PROMOTION_QUALITY_GATE=HISTORICAL_NOT_RUNTIME
EVIDENCE_WORKSPACE_GIT_IGNORE=REQUIRED
PRIMARY_INSTANCE_CHANGE=NONE
MODEL_SYNC_OPERATION=PROHIBITED
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

## 2. One Current Workflow

1. Verify that `artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/` is ignored by Git.
2. Create one unique evidence workspace under that ignored path.
3. Run `scripts/adp24_isolated_runtime_preflight.sh` and save the transcript as `04-preflight-transcript.txt` in the active evidence workspace. This is the only current Git and runtime-entry gate. Do not run `scripts/adp24_pre_runtime_quality_gate.sh`; it is the historical pre-promotion candidate gate.
4. Export the selected deterministic model from the primary user interface into the active evidence workspace using the required raw filename.
5. Run `scripts/adp24_validate_model_export.py` and retain its outputs in the same evidence workspace.
6. Stop and return evidence for runtime authorization.
7. After separate authorization, run `scripts/adp24_isolated_runtime_apply.sh --execute`.
8. Complete first-run isolated administrator setup in Firefox at `http://127.0.0.1:3001`.
9. Import the sanitized model using Import only.
10. Run `scripts/adp24_isolated_runtime_verify.sh`.
11. Run `scripts/adp24_validation_volume_backup.sh --execute <backup-directory>`.
12. Perform the separately frozen restart-persistence check.
13. Perform the separately frozen non-counted dry run.

## 3. Evidence Workspace

Use one new path matching:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/<UTC-PACKET-ID>/
```

The active workspace is ignored by Git because it may contain restricted raw exports, local screenshots, and runtime transcripts. Do not use Git ignore status as permission to retain secrets. Raw exports remain restricted evidence and shall not be committed.

The later runtime apply step reruns the preflight. The evidence workspace must therefore remain ignored so that evidence capture does not create a dirty-worktree failure.

## 4. Human Evidence Actions

For each Firefox action, save the screenshot using the exact filename from `artifacts/Configuration/ADP-v2.4/runtime-evidence-filename-map.json`.

Do not capture:

- Passwords
- Session cookies
- API keys
- Email addresses unless unavoidable for account evidence
- Browser password-manager prompts
- Unrelated chats or data

## 5. Immediate Stop Conditions

Stop for any baseline-tag mismatch, evidence workspace not ignored by Git, primary-instance degradation, unexpected public binding, model mismatch, secret-bearing export, nonempty model association, wrong volume, failed backup, failed checksum, missing screenshot, wrong filename, or unexpected repository change.

Do not improvise around a stop condition. Preserve evidence and return the consolidated bundle.
