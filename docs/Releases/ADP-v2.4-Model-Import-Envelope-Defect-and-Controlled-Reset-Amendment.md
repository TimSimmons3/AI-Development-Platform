# ADP v2.4 Model Import Envelope Defect and Controlled Reset Amendment

## 1. Record Status

```text
RECORD_STATUS=CANDIDATE_PENDING_REPOSITORY_PROMOTION
DEFECT_CLASS=SANITIZED_IMPORT_ROOT_ENVELOPE_INCOMPATIBILITY
AFFECTED_ATTEMPT=NON_COUNTED_MODEL_IMPORT_SELECTION
AFFECTED_WORKSPACE=artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/20260722T215656Z
AFFECTED_SANITIZED_SHA256=cfedcc29fc4e7fa43dbffae3c2302e1a542a78a2dff49026e679a416a7b0d83f
TARGET_MODEL_COUNT_AFTER_ATTEMPT=0
PRIMARY_INSTANCE_CHANGE=NONE
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

## 2. Evidence-Based Root Cause

Open WebUI v0.10.2 Workspace Models imports a JSON file by parsing the top-level value and iterating directly over it as the model collection. The native single-model export is a top-level array containing one model object.

The prior ADP sanitizer created a wrapper object:

```text
{"models":[<model>]}
```

The v0.10.2 import handler therefore did not iterate over the model object and did not create the target model. Read-only inspection after the attempt reported:

```text
TARGET_MODEL_COUNT=0
```

The defect is in the ADP sanitized-import artifact design and validation coverage, not in operator execution.

## 3. Attempt Classification

The model-import selection attempt is void and non-counted. Preserve all prior evidence without overwrite, deletion, or relabeling.

The prior sanitized import artifact is superseded and prohibited from reuse:

```text
03-deterministic-model-import-sanitized.json
```

The prior selection screenshot, if present, is failed-attempt evidence and is not successful import evidence:

```text
08-model-import-selection.png
```

Do not create `09-model-import-complete.png` in the voided workspace.

## 4. Corrective Controls

The corrected sanitizer shall:

- Emit a top-level JSON array.
- Emit exactly one model object.
- Preserve the approved deterministic id, name, base model, temperature, seed, active state, safe metadata, and empty access grants.
- Strip source ownership, timestamps, write-access data, and any other unapproved field.
- Record `SANITIZED_IMPORT_ROOT=TOP_LEVEL_ARRAY`.
- Record `SANITIZED_IMPORT_MODEL_COUNT=1`.

An independent import-payload validator shall reject:

- Wrapper objects.
- Multiple or zero models.
- Unexpected model fields.
- Wrong deterministic parameters.
- Secret-bearing fields.
- Nonempty model associations.
- Nonempty access grants.

The repository quality gate shall exercise both the compatible positive path and the wrapped-object negative path.

## 5. Controlled Reset Boundary

A full validation-volume restore is not required before the corrected attempt because read-only evidence established that the failed selection did not create or update the target model.

Reuse of the retained initialized runtime is authorized only after a new reset workspace records all of these conditions:

- Validation container healthy.
- Primary instance healthy.
- One isolated user.
- One isolated administrator.
- Zero target deterministic models.
- Pristine pre-administrator backup checksum valid.
- Repository clean.
- Prior raw export SHA-256 equals `dc5f11638c994e7204b7a8e2b0920bd7f8ccf324253260ac65dd7efcf99269fa`.

This is a reset at the model-import boundary. It is not continuation of the voided attempt.

## 6. Cross-Workspace Reference Authorization

The corrected validator may read the unchanged raw export from the voided workspace solely to generate new corrected outputs:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/20260722T215656Z/01-primary-deterministic-model-export-raw.json
```

No other prior setup, screenshot, validator output, import payload, manifest, backup, restart, or dry-run evidence may be reused as evidence of the corrected attempt.

The new corrected attempt shall use:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Model-Import-Reset/<UTC-PACKET-ID>/
```

## 7. Procedure Freeze Impact

This amendment changes the import artifact, validator output contract, operator steps, evidence workspace, evidence filenames, and stop conditions. Therefore:

- The prior model-import procedure version is superseded.
- The failed import selection remains void.
- No model import may resume until this repository correction is promoted, tagged, and revalidated on the target host.
- Counted execution remains prohibited.
