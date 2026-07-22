# ADP v2.4 Isolated Validation Runtime Evidence Schema

## 1. Workspaces

Initial pre-runtime evidence workspace:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/<UTC-PACKET-ID>/
```

Controlled model-import reset workspace:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Model-Import-Reset/<UTC-PACKET-ID>/
```

Use one new active workspace for each controlled attempt. Do not overwrite or continue writing execution evidence into a voided workspace.

The model-import envelope amendment permits one narrowly bounded cross-workspace reference: the corrected validator may read the unchanged raw native export from the voided pre-runtime workspace only after its recorded SHA-256 is revalidated. All corrected outputs and subsequent evidence shall be written to the new reset workspace.

## 2. Evidence Classes

- Terminal transcripts
- JSON reports
- Checksums
- Runtime manifests
- Browser screenshots
- Volume backup metadata
- Raw and normalized non-counted responses
- Stop and void records
- Cross-workspace reference records authorized by an approved amendment

## 3. Integrity Rules

- One purpose per filename.
- No overwrite.
- Raw model export remains restricted and outside Git.
- Sanitized import payload may enter Git only after review and a separate promotion gate.
- Raw responses are immutable.
- Normalized responses are separate files.
- Every archive has an internal manifest and external SHA-256.
- Every manual action identifies application, object, expected result, evidence filename, and stop condition.
- A voided screenshot remains in its original workspace and is not reused as successful evidence.
- Corrected model-import evidence uses the dedicated reset filename map.
- Cross-workspace reuse is prohibited unless a governing amendment identifies the exact source artifact, checksum, reason, and allowed purpose.

## 4. Status Fields

```text
PACKET_STATUS=PASS|FAIL|INCONCLUSIVE
PRIMARY_INSTANCE_STATUS=PASS|FAIL
MODEL_EXPORT_VALIDATION=PASS|FAIL
MODEL_IMPORT_PAYLOAD_VALIDATION=PASS|FAIL
MODEL_IMPORT_VALIDATION=PASS|FAIL
VOLUME_BACKUP_STATUS=PASS|FAIL
RESTART_PERSISTENCE_STATUS=PASS|FAIL
NON_COUNTED_DRY_RUN_STATUS=PASS|FAIL|INCONCLUSIVE
RUNTIME_AUTHORIZATION=HOLD|PASS
COUNTED_EXECUTION_AUTHORIZATION=HOLD|PASS
```

A packet is not a full pass when a required field is missing.
