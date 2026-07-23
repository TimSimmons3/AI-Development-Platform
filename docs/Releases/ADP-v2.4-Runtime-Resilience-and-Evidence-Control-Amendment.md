# ADP v2.4 Runtime Resilience and Evidence Control Amendment

## 1. Decision

ADP v2.4 will not perform restart-persistence testing or a non-counted RAG dry run until the repository contains promoted, quality-gated controls for restart-state capture, semantic before-and-after comparison, bounded startup readiness, and protected backup artifacts.

Planned annotated tag:

```text
adp-v2.4-runtime-resilience-controls-v2
```

## 2. Audit Findings

The read-only audit at commit `334f1c3456647464137428dbd08a3c1ea4df3ffe` identified four bounded defects:

1. `scripts/adp24_isolated_runtime_apply.sh` treated a transient `unhealthy` state as an immediate terminal failure, even though the first isolated startup later recovered without restart.
2. The evidence map reserved `10-restart-before.txt` and `11-restart-after.txt`, but no executable restart-persistence procedure existed.
3. `scripts/adp24_validation_volume_backup.sh` created the archive as root with mode 644 and lacked a cleanup trap to restart the isolated container after an intermediate failure.
4. The runtime operator guide retained a stale candidate-not-promoted status after the model-import correction had been promoted.

## 3. Existing Backup Classification

The post-import archive with SHA-256 `93e615d0e7c0fae2c30b6f7d77b14437f76df76ef3278dfafb2d3e1a57928b12` remains valid:

- Checksum validation passed.
- Archive listing passed.
- The parent directory has mode 700.
- Model state and database integrity passed before and after backup.
- The isolated and primary instances returned healthy.

The root ownership and mode 644 are metadata weaknesses, not byte-integrity failures. The artifact remains historical evidence and will not be silently rewritten.

## 4. Correction Scope

The repository correction:

- Extends the apply health wait to a bounded 300 attempts by default.
- Allows transient `starting` and `unhealthy` states during the bounded wait.
- Fails immediately for `exited` or `dead`.
- Adds a restart-state capture utility with canonical stable-state hashing.
- Adds an executable restart-persistence procedure bound to evidence filenames 10 and 11.
- Adds a repository quality gate with semantic equivalence and drift fixtures.
- Adds backup `umask 077`, mode-700 destination handling, host-user ownership, mode-600 archive and checksum handling, and failure cleanup.
- Updates the operator guide to a non-stale status.

## 5. Exact Repository Write Set

```text
M  scripts/adp24_isolated_runtime_apply.sh
M  scripts/adp24_validation_volume_backup.sh
M  docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md
A  scripts/adp24_capture_restart_state.py
A  scripts/adp24_validation_restart_persistence.sh
A  scripts/adp24_runtime_resilience_quality_gate.sh
A  docs/Operations/ADP-v2.4-Isolated-Validation-Restart-Persistence-Procedure.md
A  docs/Releases/ADP-v2.4-Runtime-Resilience-and-Evidence-Control-Amendment.md
```

## 6. Runtime Boundary

Installation and repository quality validation do not restart, stop, recreate, or modify any container or volume. They do not modify the primary Open WebUI instance, import or toggle a model, attach Knowledge, create evidence files 10 or 11, or start RAG execution.

```text
VALIDATION_RUNTIME_MUTATION=NONE
RESTART_PERSISTENCE_AUTHORIZATION=HOLD_PENDING_PROMOTION
NON_COUNTED_RAG_EXECUTION_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

## 7. Promotion and Execution Rule

After byte review, the eight-path correction must be committed and pushed, and the new annotated `adp-v2.4-runtime-resilience-controls-v2` tag must be synchronized. The prior `adp-v2.4-runtime-resilience-controls` tag remains immutable at commit `be4b3be4093be3409261ea28b66e9ad01b38dec6` as historical defective-promotion evidence. A post-promotion read-only gate must verify the new tag, repository cleanliness, current runtime health, active model state, and backup integrity before the restart-persistence procedure is authorized.

## 8. Historical Defective Promotion and Git-Native Recovery

The prior runtime-resilience promotion introduced one unintended leading backslash line in each of the eight approved files. The defect affected executable first-line handling and document publication quality but did not change either Open WebUI runtime, the validation volume, the deterministic model, or the primary instance.

The authoritative diagnostic record is:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Model-Import-Reset/20260722T234427Z/09a-runtime-resilience-leading-backslash-defect-audit.txt
SHA256=fbd7e2578837030f48ac6b5460c8de12bac5407ed1270f34c35df5d75627d661
```

The corrective implementation uses a disposable Git worktree and a transparent unified patch against commit `be4b3be4093be3409261ea28b66e9ad01b38dec6`. Self-extracting correction packets and recursive execution wrappers are not authorized for this recovery.

```text
GIT_NATIVE_RECOVERY=REQUIRED
HISTORICAL_DEFECTIVE_TAG=adp-v2.4-runtime-resilience-controls
CORRECTED_TAG=adp-v2.4-runtime-resilience-controls-v2
VALIDATION_RUNTIME_MUTATION=NONE
RESTART_PERSISTENCE_AUTHORIZATION=HOLD_PENDING_V2_PROMOTION
NON_COUNTED_RAG_EXECUTION_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```
