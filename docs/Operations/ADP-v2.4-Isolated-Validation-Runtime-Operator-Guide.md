# ADP v2.4 Isolated Validation Runtime Operator Guide

## 1. Current Status

```text
GUIDE_STATUS=CANDIDATE_NOT_RUNTIME_AUTHORIZED
PRIMARY_INSTANCE_CHANGE=NONE
MODEL_SYNC_OPERATION=PROHIBITED
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

## 2. One Current Workflow

1. Run `scripts/adp24_isolated_runtime_preflight.sh`.
2. Export the selected deterministic model from the primary user interface.
3. Run `scripts/adp24_validate_model_export.py` and retain its outputs.
4. Stop and return evidence for runtime authorization.
5. After separate authorization, run `scripts/adp24_isolated_runtime_apply.sh --execute`.
6. Complete first-run isolated administrator setup in Firefox at `http://127.0.0.1:3001`.
7. Import the sanitized model using Import only.
8. Run `scripts/adp24_isolated_runtime_verify.sh`.
9. Run `scripts/adp24_validation_volume_backup.sh --execute <backup-directory>`.
10. Perform the separately frozen restart-persistence check.
11. Perform the separately frozen non-counted dry run.

## 3. Human Evidence Actions

For each Firefox action, save the screenshot using the exact filename from `artifacts/Configuration/ADP-v2.4/runtime-evidence-filename-map.json`.

Do not capture:

- Passwords
- Session cookies
- API keys
- Email addresses unless unavoidable for account evidence
- Browser password-manager prompts
- Unrelated chats or data

## 4. Immediate Stop Conditions

Stop for any primary-instance degradation, unexpected public binding, model mismatch, secret-bearing export, nonempty model association, wrong volume, failed backup, failed checksum, missing screenshot, wrong filename, or unexpected repository change.

Do not improvise around a stop condition. Preserve evidence and return the consolidated bundle.
