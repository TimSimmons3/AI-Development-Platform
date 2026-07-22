# ADP v2.4 Repository Packet v2 Delivery Defect and Recovery Record

## 1. Status

```text
DEFECT_RECORD_STATUS=CLOSED_WITH_SUPERSEDING_PACKET
FAILED_PACKET=ADP-v2.4-Isolated-Validation-Repository-Implementation-Packet-v2.sh
FAILED_PACKET_SHA256=22eac9e04cdffc4d286569617ace6f6ca9b8f191629e39dff63639b602a6aec9
FAILED_CONTROL=VALIDATION_BINDING
SELF_TEST_RESULT=FAIL_SAFE
TARGET_INSTALL_RESULT=FAIL_SAFE
REPOSITORY_RECOVERY=PASS
RUNTIME_MUTATION=NONE
SUPERSEDING_PACKET_VERSION=v3
```

## 2. Observed Failure

The v2 self-test and the target repository installation both passed payload, exact-write-set, text, script, fixture, JSON, and template-hash controls. Both then stopped at:

```text
ADP24_REPOSITORY_QUALITY_GATE=FAIL
FAILED_CONTROL=VALIDATION_BINDING
RECOVERY_COMPLETED=YES
RECOVERY_WORKTREE_CLEAN=YES
```

The target repository returned to a clean state. No Open WebUI container, Docker volume, Ollama service, firewall rule, model, Knowledge collection, or counted-test state was changed.

## 3. Root Cause

The v2 gate validated the loopback binding by grepping the human-readable output of:

```text
docker compose config
```

Docker Compose normalizes short port syntax into canonical long syntax. The valid source mapping `127.0.0.1:3001:8080` can therefore render as separate `host_ip`, `published`, and `target` fields instead of the original combined string. The gate treated a presentation-format difference as a configuration failure.

The v2 clean-room self-test did not expose the defect because its no-Docker fallback parsed the source YAML rather than exercising Docker Compose canonical output.

## 4. Corrective Actions

The v3 packet:

1. Retains `docker compose config --quiet` for Compose syntax and consistency validation.
2. Renders the canonical Compose data model with `docker compose config --format json`.
3. Parses the JSON structurally instead of grepping formatted YAML.
4. Validates `host_ip=127.0.0.1`, `published=3001`, and `target=8080` independently.
5. Validates the separate volume, bridge network mode, no-pull policy, image digest, environment controls, and approved RAG template semantically.
6. Uses a fake Docker Compose command and representative canonical JSON during clean-room self-test so the target validation path is exercised even when Docker is unavailable in the build environment.
7. Preserves safe failure and exact-path recovery.

## 5. Supersession

The v2 packet is rejected and shall not be reused. Only the checksum-validated v3 packet may be used for the repository-only implementation attempt.
