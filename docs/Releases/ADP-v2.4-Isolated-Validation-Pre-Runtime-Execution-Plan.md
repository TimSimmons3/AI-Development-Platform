# ADP v2.4 Isolated Validation Pre-Runtime Execution Plan

## 1. Status

```text
PLAN_STATUS=FROZEN_REPOSITORY_CANDIDATE
AUTHORITATIVE_BASELINE=079f30d909114aca450207c37c84ac471b9db828
PRIMARY_INSTANCE_CHANGE=NONE
RUNTIME_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

## 2. Objective

Prepare one controlled pre-runtime package for the isolated Open WebUI validation instance without starting a container, creating a volume, importing a model, or changing the primary instance.

## 3. Governing Boundaries

- Primary Open WebUI remains unchanged on `127.0.0.1:3000`.
- Validation Open WebUI is reserved for `127.0.0.1:3001`.
- Validation data uses only the `open-webui-validation` volume.
- Existing Ollama and UFW settings remain unchanged.
- Real, sensitive, confidential, regulated, client, or production data is prohibited.
- Model synchronization is prohibited.
- Model restoration uses import only.
- No counted run may start from this package.

## 4. Native Model Portability Method

The authoritative source is the native Open WebUI export for the single model named `Llama 3.2 3B RAG Deterministic Test`.

The operator shall export the selected model through the primary Open WebUI user interface. The raw export remains restricted evidence and is not committed. The validator shall:

1. Require exactly one model.
2. Require model id `llama-32-3b-rag-deterministic-test`.
3. Require base model `llama3.2:3b`.
4. Require temperature `0` and seed `42`.
5. Require no system prompt.
6. Reject nonempty Knowledge, tool, skill, function, or filter bindings.
7. Reject secret-bearing fields.
8. Strip owner and timestamp fields.
9. Produce an additive import payload with empty access grants.

The isolated instance shall use the model import operation. The sync operation is prohibited because it may delete models absent from the submitted list.

## 5. Pre-Runtime Sequence

1. Validate Git, protected files, image, port, and primary health.
2. Export the one deterministic model from the primary user interface.
3. Validate and sanitize the export.
4. Freeze the sanitized import payload checksum.
5. Create the isolated container and volume only under a separately authorized runtime packet.
6. Complete isolated first-run administrator setup without recording credentials.
7. Import the sanitized model through the user interface.
8. Verify the imported model through read-only database inspection.
9. Create and verify a cold backup of the isolated volume.
10. Restart and verify deterministic configuration persistence.
11. Complete one non-counted synthetic dry run.
12. Freeze the counted-run procedure only after the dry run passes.

## 6. Stop Conditions

Stop for any baseline drift, unexpected path, primary-instance change, public binding, image mismatch, model mismatch, secret exposure, model association, missing backup, failed restore test, failed evidence capture, failed runtime validation, or procedure change.

A material change after counted execution begins voids the affected run as `VOIDED_NOT_COUNTED` and requires reset, archive, re-freeze, and fresh execution.

## 7. Authorization

```text
REPOSITORY_PREPARATION=AUTHORIZED
VALIDATION_CONTAINER_CREATION=HOLD
VALIDATION_VOLUME_CREATION=HOLD
MODEL_IMPORT=HOLD
NON_COUNTED_DRY_RUN=HOLD
COUNTED_EXECUTION=HOLD
```
