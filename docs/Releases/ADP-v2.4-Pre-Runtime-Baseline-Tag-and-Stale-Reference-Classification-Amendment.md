# ADP v2.4 Pre-Runtime Baseline Tag and Stale-Reference Classification Amendment

## 1. Status

```text
AMENDMENT_STATUS=REPOSITORY_CANDIDATE
RELEASE=ADP_v2.4
AUTHORITATIVE_PRE_CORRECTION_COMMIT=bc9b0f900bf3df532b6918257d887348533478e9
RUNTIME_BASELINE_TAG=adp-v2.4-pre-runtime-controls
TAG_TYPE=ANNOTATED_REQUIRED
TAG_CREATION_AUTHORIZATION=HOLD_PENDING_PROMOTION
RUNTIME_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

## 2. Defect

The promoted runtime preflight script hardcoded the pre-runtime package starting commit:

```text
079f30d909114aca450207c37c84ac471b9db828
```

After promotion, the authoritative repository commit became:

```text
bc9b0f900bf3df532b6918257d887348533478e9
```

A hardcoded self-containing commit cannot remain current after the correction itself is committed. Replacing one embedded commit SHA with another would recreate the same defect after every promotion.

## 3. Corrective Architecture

The current runtime preflight shall resolve an annotated Git tag:

```text
adp-v2.4-pre-runtime-controls
```

The tag shall be created and pushed only after the correction commit is created. The preflight shall require:

- The local tag exists and is annotated.
- The local tag resolves to one commit.
- The peeled remote tag resolves to the same commit.
- `HEAD`, `main`, and `origin/main` equal that commit.
- The worktree is clean.

This removes recursive commit pinning while preserving an immutable, auditable runtime-entry baseline.

## 4. Stale-Reference Classification

The baseline audit results are classified as follows.

### Current executable defect

- `scripts/adp24_isolated_runtime_preflight.sh`
  - Disposition: correct to annotated-tag enforcement.
  - Runtime use before correction and tag promotion: prohibited.

### Historical pre-promotion controls

- `scripts/adp24_pre_runtime_quality_gate.sh`
  - Purpose: validate the 20 untracked pre-runtime repository candidate files before promotion.
  - Starting baseline `079f30d...` remains historically correct.
  - Runtime use after promotion: prohibited.
  - Do not update only its SHA because it would still expect the historical untracked candidate state.

- `scripts/adp24_repository_quality_gate.sh`
  - Purpose: validate the earlier repository-only candidate package.
  - Starting baseline `c9de7d...` remains historically correct.
  - Runtime use: prohibited.

### Prior-release historical scripts

- `scripts/adp231_gate_c_post_promotion_correct.sh`
- `scripts/adp231_gate_c_promote.sh`

Their release-specific baselines remain historical evidence and shall not be rewritten.

### Historical plan and gate-record fields

The following fields record the valid starting commit for their original controlled transaction and shall not be rewritten:

- `AUTHORITATIVE_BASELINE=079f30d...` in the pre-runtime execution plan.
- `AUTHORITATIVE_STARTING_COMMIT=079f30d...` in the pre-runtime repository gate record.
- `EXPECTED_BASELINE=c9de7d...` and `AUTHORITATIVE_STARTING_COMMIT=c9de7d...` in earlier v2.4 repository records.

They do not authorize runtime entry. This amendment and the annotated tag govern current runtime entry.

## 5. Current-Artifact Rule

The only current runtime-entry command is:

```text
scripts/adp24_isolated_runtime_preflight.sh
```

The current operator guide shall identify the pre-promotion quality gate as historical and not a runtime command.

## 6. Promotion and Tag Boundary

The correction promotion shall contain exactly:

1. The corrected runtime preflight script.
2. The corrected runtime operator guide.
3. This amendment.

After the commit is created and pushed, create and push the annotated tag:

```text
adp-v2.4-pre-runtime-controls
```

The tag must point exactly to the correction promotion commit. Runtime preflight remains blocked until the local and remote tag checks pass.

## 7. Authorization

```text
REPOSITORY_CORRECTION=AUTHORIZED_AFTER_PACKET_VALIDATION
GIT_PROMOTION=HOLD_PENDING_REVIEW
ANNOTATED_TAG_CREATION=HOLD_PENDING_PROMOTION
MODEL_EXPORT=HOLD
VALIDATION_CONTAINER_CREATION=HOLD
RUNTIME_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```
