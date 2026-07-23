# ADP v2.4 Isolated Validation Restart-Persistence Procedure

## 1. Purpose

This procedure validates that the isolated Open WebUI validation instance preserves its approved runtime configuration, dedicated volume, administrator state, and deterministic model state across one controlled container restart.

## 2. Authorization Boundary

```text
PROCEDURE_STATUS=CORRECTED_NOT_YET_EXECUTED
HISTORICAL_RUNTIME_RESILIENCE_TAG=adp-v2.4-runtime-resilience-controls
RUNTIME_RESILIENCE_TAG=adp-v2.4-runtime-resilience-controls-v2
REQUIRED_SCRIPT=scripts/adp24_validation_restart_persistence.sh
REQUIRED_BEFORE_EVIDENCE=10-restart-before.txt
REQUIRED_AFTER_EVIDENCE=11-restart-after.txt
PRIMARY_INSTANCE_CHANGE=NONE
NON_COUNTED_RAG_EXECUTION_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

The procedure may run only after the corrected runtime-resilience repository commit is promoted, the new annotated `adp-v2.4-runtime-resilience-controls-v2` tag is synchronized, the historical defective tag is preserved unchanged, the post-import backup gate passes, and the active evidence workspace is confirmed.

## 3. Preconditions

- Repository, `main`, and `origin/main` are synchronized at the promoted runtime-resilience v2 commit.
- The annotated `adp-v2.4-runtime-resilience-controls-v2` tag resolves to that commit locally and remotely.
- The prior annotated `adp-v2.4-runtime-resilience-controls` tag remains immutable as historical defective-promotion evidence.
- The repository worktree is clean.
- `open-webui-validation` is healthy.
- The primary instance on port 3000 is healthy.
- The deterministic model exists exactly once, is active, uses `llama3.2:3b`, has temperature 0 and seed 42, and has no Knowledge, tool, skill, function, filter, file, or access-grant association.
- `10-restart-before.txt` and `11-restart-after.txt` do not already exist.
- Counted execution has not started.

## 4. Execution

Run:

```bash
bash scripts/adp24_validation_restart_persistence.sh \
  --execute \
  "$HOME/Labs/AI-Development-Platform" \
  "$HOME/Labs/AI-Development-Platform/artifacts/Evidence/ADP-v2.4-Isolated-Validation-Model-Import-Reset/<ACTIVE-RESET-ID>"
```

The script performs one `docker restart open-webui-validation`. It does not recreate the container, replace the volume, pull an image, modify the primary instance, import a model, or attach Knowledge.

## 5. Health-Wait Rule

A transient Docker health state of `starting` or `unhealthy` is not by itself a terminal failure during the bounded wait. The script continues checking for up to 300 attempts at two-second intervals by default.

The script fails immediately for `exited` or `dead`, and fails closed if `healthy` is not reached before the bounded timeout.

## 6. Evidence and Semantic Comparison

Before restart, the script creates `10-restart-before.txt`. After restart and technical verification, it creates `11-restart-after.txt`.

Each file contains:

- Container identity and health
- Configured and effective image identity
- Port and network configuration
- Dedicated volume mount
- Qualification environment values
- Database quick check
- User and administrator counts
- Deterministic model identity, parameters, active state, system-prompt absence, and association absence
- A canonical SHA-256 over the stable semantic state

Volatile values such as capture time and container start time are recorded but excluded from the stable-state fingerprint.

## 7. Pass Criteria

```text
RESTART_PERSISTENCE_GATE=PASS
CONTAINER_ID_PRESERVED=PASS
MODEL_STATE_PERSISTENCE=PASS
CONFIGURATION_PERSISTENCE=PASS
VOLUME_PERSISTENCE=PASS
PRIMARY_INSTANCE_STATUS=PASS
REPOSITORY_CLEANLINESS=PASS
```

The before and after stable-state SHA-256 values must match exactly.

## 8. Stop Conditions

Stop and preserve evidence for any terminal container state, timeout, container-ID drift, stable-state hash mismatch, model drift, configuration drift, volume drift, primary-instance degradation, or repository change.

Do not repeat the restart or patch evidence inside the same attempt. Review and classify the failure before further runtime action.
