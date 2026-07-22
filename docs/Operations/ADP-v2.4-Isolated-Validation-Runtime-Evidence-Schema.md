# ADP v2.4 Isolated Validation Runtime Evidence Schema

## 1. Workspace

Use one new active workspace:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/<UTC-PACKET-ID>/
```

Do not reuse a prior or voided workspace.

## 2. Evidence Classes

- Terminal transcripts
- JSON reports
- Checksums
- Runtime manifests
- Browser screenshots
- Volume backup metadata
- Raw and normalized non-counted responses
- Stop and void records

## 3. Integrity Rules

- One purpose per filename.
- No overwrite.
- Raw model export remains restricted and outside Git.
- Sanitized import payload may enter Git only after review and a separate promotion gate.
- Raw responses are immutable.
- Normalized responses are separate files.
- Every archive has an internal manifest and external SHA-256.
- Every manual action identifies application, object, expected result, evidence filename, and stop condition.

## 4. Status Fields

```text
PACKET_STATUS=PASS|FAIL|INCONCLUSIVE
PRIMARY_INSTANCE_STATUS=PASS|FAIL
MODEL_EXPORT_VALIDATION=PASS|FAIL
MODEL_IMPORT_VALIDATION=PASS|FAIL
VOLUME_BACKUP_STATUS=PASS|FAIL
RESTART_PERSISTENCE_STATUS=PASS|FAIL
NON_COUNTED_DRY_RUN_STATUS=PASS|FAIL|INCONCLUSIVE
RUNTIME_AUTHORIZATION=HOLD|PASS
COUNTED_EXECUTION_AUTHORIZATION=HOLD|PASS
```

A packet is not a full pass when a required field is missing.
