# ADP Five-Pass Readiness Review Standard

## 1. Purpose

This standard prevents authorization based on a single successful check. Before any controlled commit, branch push, promotion to `main`, annotated-tag creation, runtime mutation, Knowledge upload, non-counted execution, counted execution, or closeout, the reviewer must ask and answer the following question five independent times:

> Have we caught everything material, and are we ready to proceed?

A prior pass may not be copied forward as the answer to a later pass. Each pass must use a different review perspective and identify its evidence, findings, residual risk, and authorization result.

## 2. Applicability

This standard applies to all ADP controlled changes and executions, including:

- Repository implementation and remediation
- Procedure and evidence-design freezes
- Git commits, pushes, merges, promotions, and tags
- Container, volume, model, Knowledge, configuration, and backup actions
- Non-counted simulations
- Counted validation runs
- Recovery, reset, restart, and closeout decisions

## 3. Mandatory Five Passes

### Pass 1: Scope and Baseline Integrity

Ask and answer whether the exact baseline, branch, worktree, write set, file modes, artifact hashes, and repository cleanliness are correct.

Minimum evidence:

- Full commit identifiers
- Exact changed-path list
- File-mode validation
- Patch or diff SHA-256
- Source-repository protection result

### Pass 2: Technical and Structural Correctness

Ask and answer whether all scripts, data files, documents, schemas, and validators are syntactically and structurally valid.

Minimum evidence:

- Bash syntax
- Python compilation
- JSON parsing
- Text-quality and final-newline checks
- Positive and negative fixture results

### Pass 3: Semantic and Traceability Correctness

Ask and answer whether all status fields, authorization states, tags, hashes, filenames, procedures, evidence purposes, stop conditions, and governing records agree semantically.

Minimum evidence:

- Cross-file state-matrix comparison
- No stale or contradictory status language
- Input-hash binding
- Procedure-to-contract binding
- Evidence-map-to-contract binding
- Semantic traceability result

### Pass 4: Failure, Recovery, and Abuse Resistance

Ask and answer whether failures stop safely, cannot be masked, and do not mutate protected state.

Minimum evidence:

- Explicit nonzero-exit propagation
- Collision and unexpected-path rejection
- Wrong-fact and unsupported-shape rejection
- Missing-argument rejection
- No retry or regeneration path
- Recovery or reset boundary
- No self-matching audit logic

### Pass 5: Operational Readiness and Residual Risk

Ask and answer whether the planned action is operationally authorized, reversible where required, evidence-complete, and free of unresolved material risk.

Minimum evidence:

- Runtime and primary-instance boundary
- Model and association boundary
- Backup and recovery-point validation
- Evidence collision check
- Repository cleanliness
- Residual-risk statement
- Explicit authorization decision

## 4. Independence Rule

The five passes must not be five repetitions of the same command or conclusion. Each pass must use its designated perspective. A pass fails if its evidence is absent, stale, ambiguous, or derived only from another pass.

## 5. Stop Rule

Any `FAIL`, unresolved inconsistency, unverified assumption, stale status, unexpected path, masked command failure, runtime drift, evidence collision, or material residual risk causes:

```text
FIVE_PASS_READINESS_STATUS=FAIL
PROCEED_AUTHORIZATION=HOLD
```

The action must stop. Corrective work must be reviewed from Pass 1 again. Earlier pass results may be retained as historical evidence but may not authorize the corrected attempt.

## 6. Authorization Rule

Proceed only when all five independent passes report `PASS` in the same reviewed attempt:

```text
READINESS_PASS_1_SCOPE_BASELINE=PASS
READINESS_PASS_2_TECHNICAL_STRUCTURE=PASS
READINESS_PASS_3_SEMANTIC_TRACEABILITY=PASS
READINESS_PASS_4_FAILURE_RECOVERY=PASS
READINESS_PASS_5_OPERATIONAL_RESIDUAL_RISK=PASS
FIVE_PASS_READINESS_STATUS=PASS
PROCEED_AUTHORIZATION=PASS
```

Authorization remains limited to the next explicitly named action. It does not authorize later actions.

## 7. Required Record

The readiness record must state:

- Baseline and target action
- Reviewer or validating mechanism
- Date or evidence timestamp when applicable
- Evidence used for each pass
- Findings and corrective actions
- Residual risks
- Five pass results
- Exact next action authorized
- Actions that remain held

## 8. Procedure-Freeze Rule

The five-pass standard itself is a governing control. A controlled procedure must reference this standard and must not authorize execution until the five-pass readiness record for that procedure has passed.

## 9. Counted-Run Rule

A counted run requires a new five-pass review after the final procedure, prompts, expected answers, citation policy, scripts, evidence schema, filenames, checksums, and stop conditions are frozen together. A non-counted review cannot authorize counted execution.

## 10. No-Certainty Overstatement

A `PASS` means the specified evidence found no unresolved material defect within the reviewed scope. It does not claim absolute certainty. Unknowns and residual risks must be stated explicitly.
