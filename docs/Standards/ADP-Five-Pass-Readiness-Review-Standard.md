# ADP Five-Pass Readiness Review Standard

## 1. Purpose

This standard prevents authorization based on a single successful check. Before any controlled commit, branch push, promotion to `main`, annotated-tag creation, runtime mutation, Knowledge upload, non-counted execution, counted execution, or closeout, the reviewer must ask and answer the following question five independent times:

> Have we caught everything material, and are we ready to proceed?

Pass 5 must also answer:

> Have all known material residual risks and security exposures been resolved, mitigated, formally accepted, or blocked with compensating controls?

A prior pass may not be copied forward as the answer to a later pass. Each pass must use a different review perspective and identify its evidence, findings, residual risk, security exposure, and authorization result.

## 2. Applicability

This standard applies to all ADP controlled changes and executions, including:

- Repository implementation and remediation
- Procedure and evidence-design freezes
- Git commits, pushes, merges, promotions, and tags
- Container, volume, model, Knowledge, configuration, and backup actions
- Non-counted simulations
- Counted validation runs
- Recovery, reset, restart, supersession, and closeout decisions

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
- Nonblank first-line and final-newline checks
- Positive, negative, adversarial, and collision-fixture results

### Pass 3: Semantic and Traceability Correctness

Ask and answer whether all status fields, authorization states, tags, hashes, filenames, procedures, evidence purposes, stop conditions, and governing records agree semantically and are actually bound by executable validation rather than string presence alone.

Minimum evidence:

- Cross-file state-matrix comparison
- No stale or contradictory status language
- Repository input-hash binding
- Procedure-to-contract binding
- Evidence-map-to-contract binding
- Historical evidence and backup binding design
- Model and access-boundary binding design
- Semantic traceability result

### Pass 4: Failure, Recovery, and Abuse Resistance

Ask and answer whether failures stop safely, cannot be masked, and do not mutate protected state.

Minimum evidence:

- Explicit nonzero-exit propagation
- Collision and unexpected-path rejection
- Wrong-fact, contradiction, mixed-citation, and unsupported-shape rejection
- Missing-argument and tampered-binding rejection
- No retry or regeneration path
- Recovery or reset boundary
- No self-matching audit logic
- Python cache isolation

### Pass 5: Operational Readiness, Residual Risk, and Security Exposure

Ask and answer whether the planned action is operationally authorized, reversible where required, evidence-complete, and free of unresolved material residual risk or security exposure.

Minimum evidence:

- Runtime and primary-instance boundary
- Model, association, and access-grant boundary
- Backup and recovery-point validation
- Evidence collision and confidentiality check
- Repository cleanliness
- Residual-risk and security-exposure register
- Unknown-risk statement
- Explicit authorization decision

Required outputs:

```text
READINESS_PASS_5_OPERATIONAL_RESIDUAL_RISK=PASS|FAIL
READINESS_PASS_5_SECURITY_EXPOSURE=PASS|FAIL
```

## 4. Independence Rule

The five passes must not be five repetitions of the same command or conclusion. Each pass must use its designated perspective. A pass fails if its evidence is absent, stale, ambiguous, self-referential, or derived only from another pass.

## 5. Stop and Procedure-Freeze Rule

Any `FAIL`, unresolved inconsistency, unverified assumption, stale status, unexpected path, masked command failure, runtime drift, evidence collision, material residual risk, or material security exposure causes:

```text
FIVE_PASS_READINESS_STATUS=FAIL
PROCEED_AUTHORIZATION=HOLD
```

The action must stop. A material change after a procedure, script, fixture, evidence schema, filename, checksum, prompt, or acceptance rule is frozen voids the affected attempt. Preserve it as non-authorizing historical evidence, reset the disposable workspace, and restart from Pass 1 with one newly frozen procedure and script set. Do not patch or rerun the affected attempt.

## 6. Authorization Rule

Proceed only when all five independent passes report `PASS` in the same reviewed attempt:

```text
READINESS_PASS_1_SCOPE_BASELINE=PASS
READINESS_PASS_2_TECHNICAL_STRUCTURE=PASS
READINESS_PASS_3_SEMANTIC_TRACEABILITY=PASS
READINESS_PASS_4_FAILURE_RECOVERY=PASS
READINESS_PASS_5_OPERATIONAL_RESIDUAL_RISK=PASS
READINESS_PASS_5_SECURITY_EXPOSURE=PASS
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
- Residual risks and security exposures
- Unknown-risk statement
- Five-pass results
- Exact next action authorized
- Actions that remain held

## 8. Independent Full-Diff Review Rule

A candidate quality gate or self-test cannot authorize commit by itself. Before commit, an independent full-diff review must test claims that are broader than named fixtures, inspect status and authorization language, verify executable hash bindings, and red-team classification boundaries. A material finding supersedes the candidate.

## 9. Procedure-Freeze Rule

The five-pass standard itself is a governing control. A controlled procedure must reference this standard and must not authorize execution until the five-pass readiness record for that exact procedure, script set, evidence schema, filenames, and checksums has passed.

## 10. Counted-Run Rule

A counted run requires a new five-pass review after the final procedure, prompts, expected answers, citation policy, binding manifest, scripts, evidence schema, filenames, checksums, stop conditions, promotion commit, model boundary, and access boundary are frozen together. A non-counted review or design-candidate review cannot authorize counted execution.

## 11. No-Certainty Overstatement

A `PASS` means the specified evidence found no unresolved material defect within the reviewed scope. It does not claim absolute certainty. Unknowns and residual risks must be stated explicitly.

## 12. Candidate v7 exact-state signing rule

A promotion or execution signature is valid only when the signed canonical record binds the exact commit, tree, parent, changed-path set, artifact hashes, signer fingerprint, namespace, and governing package. A signature over a mutable alias, incomplete path set, or unverified external record does not authorize action.

## 13. Canonical trust cross-binding rule

Every trust-companion hash in the evidence map, promotion record, execution authorization, and binding report must equal the exact current package-manifest hash. Legacy or ambiguous trust-hash aliases are prohibited.

## 14. Two-cycle release gate

For Candidate v7 C1 application, Cycle 1 is the consolidated offline package build and full preflight. Cycle 2 is one combined host application and independent review. An assistant-authored failure in Cycle 2 closes the automated path; no iterative host patch-and-rerun loop is authorized.
