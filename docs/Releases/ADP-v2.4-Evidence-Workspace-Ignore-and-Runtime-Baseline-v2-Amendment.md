# ADP v2.4 Evidence Workspace Ignore and Runtime Baseline v2 Amendment

## 1. Status

```text
AMENDMENT_STATUS=REPOSITORY_CANDIDATE
RELEASE=ADP_v2.4
AUTHORITATIVE_PRE_CORRECTION_COMMIT=4f6be2a77c76c04cd51a255faaf3bb13c3b88be6
PRIOR_RUNTIME_BASELINE_TAG=adp-v2.4-pre-runtime-controls
NEW_RUNTIME_BASELINE_TAG=adp-v2.4-pre-runtime-controls-v2
TAG_TYPE=ANNOTATED_REQUIRED
TAG_CREATION_AUTHORIZATION=HOLD_PENDING_PROMOTION
MODEL_EXPORT=HOLD
RUNTIME_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

## 2. Confirmed Defect

The committed evidence schema requires active pre-runtime evidence beneath:

```text
artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/<UTC-PACKET-ID>/
```

The repository did not ignore that path. Creating the required evidence workspace would therefore make the worktree dirty. The runtime apply script reruns the current preflight, and the preflight rejects a dirty worktree.

The defect was confirmed by `git check-ignore`, which returned no matching rule.

## 3. Corrective Design

The correction shall:

1. Add one exact ignore rule for the active ADP v2.4 pre-runtime evidence root.
2. Keep the ignore scope bounded to this release workspace.
3. Preserve tracked historical evidence elsewhere in `artifacts/Evidence`.
4. Add an explicit preflight control that requires the evidence probe path to be ignored.
5. Update the operator guide so evidence is created only beneath the ignored workspace.
6. Advance the runtime baseline to a new annotated tag after the correction commit.

The correction shall not ignore the entire `artifacts/Evidence` tree.

## 4. Runtime Baseline Advancement

The prior annotated tag remains immutable historical evidence:

```text
adp-v2.4-pre-runtime-controls
```

It shall not be moved or deleted.

After this correction is committed and pushed, create a new annotated tag:

```text
adp-v2.4-pre-runtime-controls-v2
```

The new tag shall point exactly to the correction promotion commit. The runtime preflight shall require the local and remote peeled tag to resolve to the same commit and shall require `HEAD`, `main`, and `origin/main` to equal it.

## 5. Exact Write Set

```text
M  .gitignore
M  scripts/adp24_isolated_runtime_preflight.sh
M  docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md
A  docs/Releases/ADP-v2.4-Evidence-Workspace-Ignore-and-Runtime-Baseline-v2-Amendment.md
```

No other repository path is authorized.

## 6. Validation Requirements

Before promotion:

- Byte comparison against the validated package
- Exact four-path status
- ASCII, tab, trailing-whitespace, and shell-syntax checks
- `git diff --check`
- Positive `git check-ignore` result for the evidence probe
- Negative check confirming unrelated `artifacts/Evidence` paths are not newly ignored
- New baseline tag present in the preflight and operator guide
- Prior tag absent from current runtime-entry artifacts
- No runtime mutation

After promotion:

- Commit and push synchronization
- New annotated tag creation and push
- Local and remote peeled tag equality
- Clean worktree
- Tag-based preflight pass
- Primary instance unchanged
- Validation container and volume absent
- Model export still separately authorized

## 7. Authorization

```text
REPOSITORY_CORRECTION=AUTHORIZED_AFTER_PACKET_VALIDATION
GIT_PROMOTION=HOLD_PENDING_BYTE_REVIEW
ANNOTATED_TAG_CREATION=HOLD_PENDING_PROMOTION
MODEL_EXPORT=HOLD
VALIDATION_CONTAINER_CREATION=HOLD
RUNTIME_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```
