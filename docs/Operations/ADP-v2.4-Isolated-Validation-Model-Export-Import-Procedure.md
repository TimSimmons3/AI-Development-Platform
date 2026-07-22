# ADP v2.4 Isolated Validation Model Export and Import Procedure

## 1. Boundary

```text
MODEL_SOURCE=PRIMARY_OPEN_WEBUI_SINGLE_MODEL_EXPORT
MODEL_TARGET=ISOLATED_VALIDATION_INSTANCE
IMPORT_METHOD=ADDITIVE_IMPORT_ONLY
MODEL_SYNC_OPERATION=PROHIBITED
API_KEY_USE=NOT_REQUIRED
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
SANITIZED_IMPORT_SHA256=<sha256>
```

Any failure stops the workflow. Do not manually edit a failing export into compliance.

## 4. Import Into Isolated Instance

Application: Firefox connected to `http://127.0.0.1:3001`.

Prerequisites:

- Isolated container healthy.
- Isolated administrator account established.
- Sanitized import payload validated and checksummed.
- Primary instance still healthy.

Steps:

1. Open Workspace.
2. Open Models.
3. Choose Import.
4. Select the sanitized import JSON.
5. Confirm exactly one model is added or updated.
6. Do not use Sync.
7. Do not attach Knowledge, tools, skills, functions, or filters.
8. Capture the required screenshots from the evidence filename map.

## 5. Post-Import Verification

Verify through read-only inspection that:

- Model id is exact.
- Base model is `llama3.2:3b`.
- Temperature is `0`.
- Seed is `42`.
- Model is active.
- System prompt is absent.
- Model-level Knowledge, tools, skills, functions, and filters are absent.

A capability flag does not prove that a capability is attached or enabled for a chat. Per-chat controls remain mandatory.
