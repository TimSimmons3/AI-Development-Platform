# ADP v2.4 Isolated Validation Repository Implementation Artifact Manifest

## Status

```text
MANIFEST_STATUS=REFROZEN_V3
PACKET_VERSION=v3
PRIMARY_INSTANCE_CHANGE=NONE
RUNTIME_AUTHORIZATION=HOLD
V1_PACKET=SUPERSEDED_DO_NOT_REUSE
V2_PACKET=SUPERSEDED_DO_NOT_REUSE
```

## Exact Write Set

- `artifacts/Configuration/ADP-v2.4/approved-rag-template.txt`
- `artifacts/Configuration/ADP-v2.4/deterministic-model-discovery-record.json`
- `artifacts/Test-Data/ADP-v2.4/adp24_bounded_multi_fact_source.md`
- `artifacts/Test-Data/ADP-v2.4/lint-fixtures/contaminated-template.txt`
- `artifacts/Test-Data/ADP-v2.4/test-cases.json`
- `artifacts/Test-Data/ADP-v2.4/validator-fixtures/expected.txt`
- `artifacts/Test-Data/ADP-v2.4/validator-fixtures/factual-change.txt`
- `artifacts/Test-Data/ADP-v2.4/validator-fixtures/format-only.txt`
- `docker/open-webui-validation/docker-compose.yml`
- `docs/Operations/ADP-v2.4-Isolated-Validation-Configuration-Manifest.md`
- `docs/Operations/ADP-v2.4-Isolated-Validation-Instance-Repository-Procedure.md`
- `docs/Releases/ADP-v2.4-Isolated-Validation-Instance-Plan-Amendment.md`
- `docs/Releases/ADP-v2.4-Isolated-Validation-Instance-Repository-Implementation-Plan.md`
- `docs/Releases/ADP-v2.4-Isolated-Validation-Repository-Implementation-Artifact-Manifest.md`
- `docs/Releases/ADP-v2.4-Repository-Packet-v1-Delivery-Defect-and-Recovery-Record.md`
- `docs/Releases/ADP-v2.4-Repository-Packet-v2-Delivery-Defect-and-Recovery-Record.md`
- `scripts/adp24_lint_rag_template.py`
- `scripts/adp24_repository_quality_gate.sh`
- `scripts/adp24_validate_answer.py`
- `scripts/adp24_validate_compose_config.py`

## Supersession

- Rejected artifact: `ADP-v2.4-Isolated-Validation-Repository-Implementation-Packet-v1.sh`
- Rejected v1 SHA-256: `b63864b8496a0fbbc2cc45b6a5adb47d5bf0a9031fbca17a5615f41947a32d7e`
- V1 reason: invalid exact-write-set count caused by Git untracked-directory summarization
- Rejected artifact: `ADP-v2.4-Isolated-Validation-Repository-Implementation-Packet-v2.sh`
- Rejected v2 SHA-256: `22eac9e04cdffc4d286569617ace6f6ca9b8f191629e39dff63639b602a6aec9`
- V2 reason: human-formatted Compose output was grepped instead of validating canonical configuration fields
- Recovery: exact package paths removed; worktree clean; runtime unchanged
- Current artifact: checksum-validated v3 packet only

This artifact set implements the isolated-validation amendment and supersedes both the unimplemented primary-instance global-override approach and the rejected v1 delivery packet.
