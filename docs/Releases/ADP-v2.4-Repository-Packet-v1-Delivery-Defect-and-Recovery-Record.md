# ADP v2.4 Repository Packet v1 Delivery Defect and Recovery Record

## 1. Status

```text
DEFECT_RECORD_STATUS=CLOSED_WITH_SUPERSEDING_PACKET
FAILED_PACKET=ADP-v2.4-Isolated-Validation-Repository-Implementation-Packet-v1.sh
FAILED_PACKET_SHA256=b63864b8496a0fbbc2cc45b6a5adb47d5bf0a9031fbca17a5615f41947a32d7e
FAILED_CONTROL=EXACT_WRITE_SET_COUNT
REPOSITORY_RECOVERY=PASS
RUNTIME_MUTATION=NONE
LATEST_SUPERSEDING_PACKET_VERSION=v3
```

## 2. Observed Failure

The v1 packet copied all 17 approved payload files and then reported:

```text
EXPECTED_PATHS=17
ACTUAL_PATHS=11
ADP24_REPOSITORY_QUALITY_GATE=FAIL
FAILED_CONTROL=EXACT_WRITE_SET_COUNT
RECOVERY_COMPLETED=YES
```

No Open WebUI, Docker runtime, Ollama, firewall, model, Knowledge, or counted-test state was changed.

## 3. Root Cause

The repository quality gate used:

```text
git status --short
```

Git may summarize a wholly untracked directory tree as one directory entry. The quality gate therefore counted directory summaries instead of every untracked file. The payload was complete, but the validation method was invalid for a nested all-new write set.

## 4. Recovery

The packet removed only the exact package-created paths after the gate failed. The returned transcript reported successful recovery. The v3 packet independently requires a clean starting worktree before any copy operation.

## 5. Corrective Actions

The v3 packet retains the v2 exact-write-set corrections and:

1. Uses `git status --short --untracked-files=all`.
2. Requires every approved path to appear individually.
3. Requires every approved path to have status `??`.
4. Rejects any additional or modified path.
5. Runs a full synthetic repository installation during self-test.
6. Runs a negative unexpected-path test.
7. Verifies recovery leaves the synthetic repository clean.
8. Records this v1 defect in the promoted repository artifact set.

## 6. Supersession

The v1 packet is rejected and shall not be reused. The v2 packet was later rejected for a separate Docker Compose validation defect. Only the checksum-validated v3 packet may be used for the repository-only implementation attempt.
