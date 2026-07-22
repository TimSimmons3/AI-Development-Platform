# ADP v2.4 Isolated Validation Instance Repository Implementation Plan

## 1. Status

```text
PLAN_STATUS=REFROZEN_FOR_REPOSITORY_ONLY_IMPLEMENTATION_V3
PACKET_VERSION=v3
STARTING_COMMIT=c9de7d74e4b3dd31887567820052220d61954d6f
PRIMARY_INSTANCE_CHANGE=PROHIBITED
RUNTIME_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
V1_PACKET=SUPERSEDED_AFTER_SAFE_FAILURE
V2_PACKET=SUPERSEDED_AFTER_SAFE_FAILURE
```

## 2. Objective

Create and statically validate the repository artifacts required for an isolated deterministic RAG qualification instance without changing any running service or the primary Open WebUI deployment.

## 3. Current Packet Scope

The repository-only packet shall:

1. Add the isolated validation Compose definition.
2. Add the approved example-free RAG template.
3. Add a sanitized deterministic-model discovery record.
4. Add an automated RAG-template linter.
5. Add a whitespace-normalized exact-answer validator.
6. Add positive and negative fixtures.
7. Add provisional bounded multi-fact test data.
8. Add configuration and operator records.
9. Add the v1 and v2 delivery-defect and recovery records.
10. Add a canonical Docker Compose JSON semantic validator.
11. Run technical and semantic repository quality gates.

## 4. Explicit Exclusions

This packet shall not:

- Modify `docker/open-webui/docker-compose.yml`.
- Modify `docs/ADP-Engineering-Log.md`.
- Start or create the validation container.
- Create or modify a Docker volume.
- Restart the primary Open WebUI container.
- Restart Ollama.
- Modify UFW.
- Export or import a workspace model.
- Create a Knowledge collection.
- Use real or sensitive data.
- Execute a counted test.

## 5. Current Artifact Boundary

The bounded multi-fact source and test cases are marked `PROVISIONAL_NOT_AUTHORIZED_FOR_COUNTED_USE`.

They may be reviewed and used in a non-counted simulation only after a separate runtime packet passes. Final prompts, expected answers, citation behavior, evidence filenames, and checksums must be frozen after the non-counted dry run and before counted execution.

## 6. Quality Gates

The repository quality gate shall prove:

- Exact starting commit
- Primary Compose unchanged
- Exact file-level write set using `--untracked-files=all`
- Every package-created path has Git status `??`
- No additional or modified path
- ASCII-only changed artifacts
- No tabs or trailing whitespace
- Shell syntax
- Python compilation
- Positive and negative linter behavior
- Positive and negative validator behavior
- JSON validity
- Approved-template checksum
- Docker Compose static validity
- Canonical Compose JSON semantic validation
- Loopback-only validation port
- Bridge networking, never host networking
- No image pull policy
- Separate validation volume
- No unnecessary inactive setting overrides
- Semantic traceability to this plan, amendment, manifest, procedure, and defect record
- No tracked-file change

## 7. Final-Delivery Validation

The exact v3 packet shall pass:

- ASCII scan
- `bash -n`
- Embedded archive checksum validation
- File-level payload checksum validation
- Positive and negative fixture tests
- Full synthetic repository installation
- Negative unexpected-path test
- Synthetic recovery-to-clean-state test
- Safe failure when the target repository is missing

The v1 and v2 packets and their prior self-test results are not reusable evidence for v3. The v3 clean-room test must exercise the same canonical JSON validation path used on the target host.

## 8. Runtime Hold Point

Runtime remains blocked until all of the following exist and pass:

- Native single-model Open WebUI JSON export
- Model import procedure using import, not sync
- Open WebUI validation-volume backup and rollback procedure
- Pre-runtime host and network checks
- Exact operator guide
- Runtime validation script
- Evidence schema and filename map
- Non-counted clean-room dry run
- Procedure-freeze record

## 9. Counted-Run Integrity

Any material change after a counted run begins requires immediate stop, preservation of evidence, classification as `VOIDED_NOT_COUNTED`, reset, re-freeze, and restart with fresh evidence.
