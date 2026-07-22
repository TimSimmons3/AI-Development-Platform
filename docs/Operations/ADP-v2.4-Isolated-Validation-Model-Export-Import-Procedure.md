# ADP v2.4 Isolated Validation Model Export and Import Procedure

## 1. Boundary

```text
MODEL_SOURCE=PRIMARY_OPEN_WEBUI_SINGLE_MODEL_EXPORT
MODEL_TARGET=ISOLATED_VALIDATION_INSTANCE
IMPORT_METHOD=ADDITIVE_IMPORT_ONLY
MODEL_SYNC_OPERATION=PROHIBITED
API_KEY_USE=NOT_REQUIRED
OPEN_WEBUI_IMPORT_ROOT=TOP_LEVEL_ARRAY
```

## 2. Export From Primary Open WebUI

Application: Firefox connected to `http://127.0.0.1:3000`.

1. Open Workspace.
2. Open Models.
3. Locate `Llama 3.2 3B RAG Deterministic Test`.
4. Open the selected model menu.
5. Choose Export for that model only.
6. Save the native JSON export in Downloads.
7. Do not export all models.
8. Do not capture passwords, cookies, tokens, or API keys.

Required raw-evidence filename:

```text
01-primary-deterministic-model-export-raw.json
```

The raw export is restricted evidence and shall not be committed.

## 3. Validate and Sanitize

Run:

```text
python3 scripts/adp24_validate_model_export.py \
  --input <raw-export.json> \
  --sanitized-output <sanitized-import.json> \
  --report-output <validation-report.json>
```

Required outputs:

```text
MODEL_EXPORT_VALIDATION=PASS
MODEL_COUNT=1
MODEL_ID=llama-32-3b-rag-deterministic-test
BASE_MODEL=llama3.2:3b
TEMPERATURE=0
SEED=42
MODEL_ASSOCIATIONS=ABSENT
SANITIZED_IMPORT_ROOT=TOP_LEVEL_ARRAY
SANITIZED_IMPORT_MODEL_COUNT=1
SANITIZED_IMPORT_SHA256=<sha256>
```

The sanitized import artifact shall be a top-level JSON array containing exactly one model object. A wrapper object such as `{"models":[...]}` is not compatible with the Open WebUI v0.10.2 Workspace Models import handler and is prohibited.

Validate the generated artifact independently:

```text
python3 scripts/adp24_validate_model_import_payload.py \
  --input <sanitized-import.json>
```

Any failure stops the workflow. Do not manually edit a failing export or sanitized import into compliance.

## 4. Controlled Reset After the Voided Import Attempt

The import attempt in evidence workspace:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/20260722T215656Z/
```

is void at the model-import boundary because the prior sanitizer generated an incompatible wrapper object. Preserve that workspace unchanged as non-counted historical evidence.

A corrected import attempt shall use one new workspace matching:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Model-Import-Reset/<UTC-PACKET-ID>/
```

The existing initialized isolated runtime may be retained only when all of the following are revalidated before the corrected import:

- Validation container is healthy.
- Primary instance is healthy.
- Isolated user count is exactly one.
- Isolated administrator count is exactly one.
- Target deterministic model count is zero.
- The pristine pre-administrator backup checksum remains valid.
- Repository worktree is clean.
- The prior raw export SHA-256 is exactly `dc5f11638c994e7204b7a8e2b0920bd7f8ccf324253260ac65dd7efcf99269fa`.

This amendment explicitly permits the corrected validator to read the unchanged, checksum-validated raw export from the voided workspace. No other setup or execution evidence may be reused. New validator outputs, screenshots, verification, manifest, backup, restart, and non-counted evidence shall be created in the new reset workspace.

The existing `08-model-import-selection.png`, if present, remains immutable evidence of the failed selection attempt. Do not overwrite, rename, or reuse it.

## 5. Import Into Isolated Instance

Application: Firefox connected to `http://127.0.0.1:3001`.

Prerequisites:

- Isolated container healthy.
- Isolated administrator account established.
- Corrected sanitized import payload validated and checksummed.
- Primary instance still healthy.
- New reset evidence workspace active.
- Target model count confirmed as zero.

Steps:

1. Open Workspace.
2. Open Models.
3. Choose Import.
4. In the file picker, select the corrected sanitized import JSON.
5. Before clicking Open, capture the file-picker selection screenshot using the reset evidence map.
6. Click Open. In Open WebUI v0.10.2, file selection triggers the import immediately; there is no separate confirmation button.
7. Confirm exactly one model is added.
8. Do not use Sync.
9. Do not attach Knowledge, tools, skills, functions, or filters.
10. Capture the completed Models page using the reset evidence map.

## 6. Post-Import Verification

Verify through read-only inspection that:

- Model id is exact.
- Base model is `llama3.2:3b`.
- Temperature is `0`.
- Seed is `42`.
- Model is active.
- System prompt is absent.
- Model-level Knowledge, tools, skills, functions, and filters are absent.
- Exactly one target model record exists.

A capability flag does not prove that a capability is attached or enabled for a chat. Per-chat controls remain mandatory.
