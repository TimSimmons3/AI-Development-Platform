# ADP v2.4 Candidate v7 Controlled Remediation Design Plan v2

## 1. Control boundary

PLAN_STATUS=CANDIDATE_V7_EXTERNAL_DESIGN_V2_PENDING_INDEPENDENT_REVIEW
DESIGN_PARENT_COMMIT=b934c7bd84bfbc35563f3681712c4d5bd8478196
CANDIDATE_V6_STATUS=SUPERSEDED_DO_NOT_COMMIT_DO_NOT_REAPPLY
CANDIDATE_V6_FAILURE_RECORD_SHA256=0a26bd3bc6596cf3766bf459d9ba8c1ba11f3d9635ba436d0e1e55e87eaa4785
V7_PLAN_V1_SHA256=46edb15963660d8d1798a644f82a60ea00ca8a6d0c53c10603a35f0edac43729
V7_PLAN_V1_REVIEW_SHA256=bce4311ac5c5075abae0552f74ebddc980db37f86bf1b64992e791513f9406fa
V7_PLAN_V1_STATUS=SUPERSEDED_BY_THIS_PLAN
CANDIDATE_V7_REPOSITORY_IMPLEMENTATION_AUTHORIZATION=HOLD
RUNTIME_MUTATION=NONE
REMEDIATION_REHEARSAL_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD

## 2. Objective

Candidate v7 will retain independently validated response-classification behavior while replacing Candidate v6 execution binding with a reachable, non-self-referential, cryptographically authenticated, exact-state promotion and execution trust chain.

## 3. Lifecycle and commit model

Candidate v7 uses two repository commits and one signed external authorization record.

1. C1 is the Candidate v7 implementation commit.
2. C1 contains the complete frozen implementation, scripts, schemas, fixtures, procedures, evidence design, and authorization holds.
3. C1 receives an independent full-diff review.
4. A promotion attestation is generated after C1 and binds C1 and its tree.
5. C2 is the final freeze commit. It contains the promotion attestation, independent review record, final procedure-freeze record, and no unreviewed implementation changes.
6. A signed external execution-authorization record is generated after C2.
7. EXECUTION mode requires repository HEAD and tree to equal C2 exactly.

Ancestor-only authorization is prohibited.

## 4. Signing trust anchor

Before implementation, the start gate must select and validate one approved signing mechanism: Git SSH signing or GPG signing.

The approved signer public-key fingerprint must be recorded in a checksum-bound external start-gate record created before Candidate v7 implementation.

PROMOTION and EXECUTION validation must verify the applicable signature against that exact fingerprint.

An unsigned attestation, unsigned authorization record, unknown signer, invalid signature, changed signer fingerprint, or unavailable signature verifier causes a controlled failure and retains all authorization holds.

## 5. DESIGN mode

DESIGN mode must validate:

- Canonical repository root
- Expected repository origin
- Approved parent commit
- Expected branch
- Clean source repository
- Clean disposable Candidate v7 workspace before application
- Exact frozen Candidate v7 write set
- Exact path inventory and file modes
- Contract and manifest schemas
- Repository dependencies and hashes
- Candidate-file hashes
- Scripts, fixtures, documents, syntax, semantics, security controls, and authorization holds

DESIGN mode must never emit promotion or execution authorization.

## 6. Promotion-attestation schema

The promotion attestation must be canonical JSON with a separately frozen schema and include:

- Schema version
- ADP release
- Candidate version
- Canonical repository origin
- Canonical repository root identifier
- Expected branch
- C1 commit SHA
- C1 tree SHA
- C1 parent SHA
- Candidate package or applied-state SHA-256
- Contract SHA-256
- Governing manifest SHA-256
- Exact Candidate v7 path inventory
- Each candidate path, Git mode, blob identifier, and SHA-256
- Quality-gate record SHA-256
- Independent full-diff review SHA-256
- Procedure-freeze record SHA-256
- UTC creation time
- Unique attestation identifier
- Approved signer fingerprint
- Promotion decision

The attestation must be signed. Its detached signature and SHA-256 must use unique filenames.

## 7. PROMOTION mode

PROMOTION mode must:

- Verify the promotion-attestation schema
- Verify the attestation signature and signer fingerprint
- Verify C1 exists
- Verify the attested C1 tree and parent
- Verify every attested path, mode, blob, and SHA-256 against C1
- Verify the Candidate v7 exact write set and absence of unexpected paths
- Verify the quality-gate and independent-review records
- Verify all authorization holds required before C2
- Reject dirty state, wrong repository, wrong origin, wrong branch, wrong commit, wrong tree, wrong mode, symlink substitution, duplicate path, and path traversal

PROMOTION validation may authorize only creation of C2.

## 8. Final freeze commit C2

C2 may add or update only the frozen paths explicitly approved for finalization:

- Promotion attestation
- Promotion-attestation signature or repository-safe signature reference
- Independent full-diff review record
- Final procedure-freeze record
- Final artifact manifest
- Status fields changing Candidate v7 from design-reviewed to final-frozen while counted execution remains held

No validator logic, fixture, expected result, procedure action, prompt, evidence filename, security control, or acceptance rule may change between C1 and C2.

Any other change voids the Candidate v7 attempt.

## 9. Execution-authorization schema

The signed external execution-authorization record must include:

- Schema version
- ADP release
- Candidate version
- Canonical repository origin
- Exact C2 commit SHA
- Exact C2 tree SHA
- Promotion-attestation SHA-256
- Final artifact-manifest SHA-256
- Final procedure-freeze record SHA-256
- Approved runtime identifier
- Approved model identity and deterministic parameters
- Approved evidence-workspace identifier
- New counted-evidence filename map SHA-256
- Authorization scope
- Authorization time
- Expiration time or explicit single-use rule
- Unique authorization identifier
- Approved signer fingerprint
- COUNTED_EXECUTION_AUTHORIZATION=PASS

The authorization record must be signed and verified before execution.

## 10. Replay and substitution controls

Promotion attestations and execution authorizations require unique identifiers and unique filenames.

An execution authorization is single-use unless the governing procedure explicitly defines another bounded use.

The validator must reject an expired, previously consumed, duplicate, wrong-release, wrong-candidate, wrong-repository, wrong-commit, wrong-tree, or wrong-workspace authorization.

Consumption evidence must be written only to the new counted evidence workspace and must not overwrite the authorization record.

## 11. EXECUTION mode

EXECUTION mode must require:

- Exact HEAD equals authorized C2
- Exact repository tree equals authorized C2 tree
- Clean tracked and untracked repository state
- Correct repository origin and branch
- Valid promotion attestation and signature
- Valid execution-authorization record and signature
- Complete promotion-binding report
- Complete execution-binding report
- Frozen procedure and evidence-filename map
- Current runtime, model, Knowledge, association, access-grant, backup, and network-boundary validation

No ancestor-only, descendant, branch-tip-only, unsigned, or partially validated state may pass.

## 12. Historical and new evidence separation

Historical Candidate v6 and non-counted evidence may be validated only as immutable baseline dependencies.

Historical files must not be copied, renamed, regenerated, relabeled, or counted as new Candidate v7 rehearsal or counted-run evidence.

Candidate v7 requires a new evidence workspace, new filenames, new checksums, and a new evidence manifest.

The evidence manifest must classify each item as BASELINE_REFERENCE, DESIGN_EVIDENCE, PROMOTION_EVIDENCE, REHEARSAL_EVIDENCE, or COUNTED_EXECUTION_EVIDENCE.

## 13. Synthetic positive reachability

The quality gate must construct an isolated disposable synthetic Git repository and exercise the same production validator entry points and shared functions used for real DESIGN, PROMOTION, and EXECUTION validation.

Test-only code may supply synthetic files, repository identity, signer keys, commits, trees, runtime metadata, and evidence roots, but it must not bypass, disable, replace, or weaken any production validation control.

The synthetic test must prove:

- DESIGN pass
- C1 creation
- Signed promotion-attestation creation and verification
- PROMOTION pass
- C2 creation
- Signed execution-authorization creation and verification
- EXECUTION binding pass
- Response-validator execution-context pass
- No mutation of the real source repository, Candidate v6 worktree, or runtime

Production and synthetic validator code hashes must be identical because they must be the same files.

## 14. Required negative tests

- Wrong signer
- Invalid signature
- Missing signature
- Changed signer fingerprint
- Wrong C1 or C2 commit
- Wrong C1 or C2 tree
- Ancestor-only match
- Descendant commit
- Modified candidate file
- Wrong file mode
- Dirty tracked state
- Unexpected untracked path
- Symlink substitution
- Path traversal
- Duplicate manifest path
- Tampered attestation
- Tampered binding report
- Missing authorization
- Expired authorization
- Replayed authorization
- Wrong evidence workspace
- Historical evidence relabeled as counted evidence
- Output collision
- Output alias
- Missing arguments
- Oversized response
- Filesystem, decoding, JSON, Git, signature-verification, and subprocess failure

## 15. Security hardening

1. Bound response and structured-input sizes.
2. Reject symbolic links for controlled inputs and outputs.
3. Use exclusive atomic output creation with restrictive permissions.
4. Validate complete report schemas and all security-relevant fields.
5. Apply subprocess timeouts.
6. Convert errors to controlled HOLD results without leaking secrets.
7. Canonicalize paths and prohibit traversal outside approved roots.
8. Require unique output and evidence filenames.

## 16. Candidate v7 frozen write-set requirement

Before implementation, create and independently review an exact Candidate v7 write-set manifest listing every added, modified, or deleted path and its intended mode and purpose.

No Candidate v7 workspace may be created until the write-set manifest, signing mechanism, signer fingerprint, schemas, test design, stop conditions, and evidence filenames pass the start gate.

## 17. Stop conditions

Stop for any baseline mismatch, unexpected path, path-count mismatch, mode mismatch, hash mismatch, signature failure, signer mismatch, schema failure, dirty state, branch or origin mismatch, self-reference, ancestor-only authorization, stale status, evidence reuse, output collision, masked failure, synthetic bypass, runtime drift, unresolved material risk, or security exposure.

Do not repair an affected counted candidate in place. Preserve, void, reset, and advance to a new candidate version.

## 18. Current authorization

CANDIDATE_V7_PLAN_V2_DRAFT=COMPLETE_PENDING_INDEPENDENT_REVIEW
CANDIDATE_V7_REPOSITORY_IMPLEMENTATION_AUTHORIZATION=HOLD
GIT_COMMIT_AUTHORIZATION=HOLD
GIT_PUSH_AUTHORIZATION=HOLD
TAG_CREATION_AUTHORIZATION=HOLD
RUNTIME_MUTATION=NONE
REMEDIATION_REHEARSAL_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD

## 19. Unknown-risk statement

This plan addresses the known Candidate v6 and Candidate v7 plan-v1 design gaps. It does not establish that all unknown implementation defects, semantic gaps, operational risks, or security exposures are absent.
