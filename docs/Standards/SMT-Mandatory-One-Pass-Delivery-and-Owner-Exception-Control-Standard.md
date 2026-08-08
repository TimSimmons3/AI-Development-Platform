# SMT Mandatory One-Pass Delivery and Owner Exception Control Standard

## 1. Control status

```text
ONE_PASS_WORKING_DELIVERABLE=MANDATORY
EXACT_DISTRIBUTED_ARTIFACT_REHEARSAL=MANDATORY
EXACT_OPERATOR_WORKFLOW_REHEARSAL=MANDATORY
ACTUAL_TARGET_STATE_FIXTURE=MANDATORY
SUCCESS_PATH_END_TO_END=MANDATORY
FAILURE_AND_PRESERVE_STATE_PATHS=MANDATORY
INDEPENDENT_REQUIREMENTS_REVIEW=MANDATORY
UNRESOLVED_ASSUMPTIONS_BEFORE_DELIVERY=0
USER_VISIBLE_REPLACEMENT_PACKAGE_TARGET=0
PATCH_AND_RETRY_CYCLE=PROHIBITED
PRODUCTION_AS_TEST_ENVIRONMENT=PROHIBITED
EXCEPTION_AUTHORITY=PROJECT_OWNER_ONLY
EXCEPTION_STATUS=NOT_GRANTED
```

This standard establishes the mandatory one-pass delivery invariant for ADP and Send Manna Too LLC engineering, documentation, packaging, conversion, infrastructure, repository, administrative, and live-change work.

## 2. Precedence

This standard supplements and, where stricter, supersedes permissive exception or revision language in earlier project records. Historical records remain immutable evidence; future work and any modified governance record must comply with this standard.

## 3. Definition of validated

“Validated” means the exact final distributed artifact completed the exact intended operator workflow, using the exact command and interaction model supplied to the user, against an isolated but target-faithful state fixture, with final state and recovery evidence reconciled.

Validation is incomplete when any of the following remains unproven:

- final archive extraction;
- launcher selection;
- current working directory;
- shell and quoting behavior;
- arguments, stdin, prompts, credentials, or authorization transport;
- exact path and filename resolution;
- owner, mode, file type, or symlink behavior;
- target-host dependencies and state;
- output location and result contract;
- source cleanup or preserve-state behavior;
- final remote, archive, repository, or recovery state.

## 4. Mandatory delivery gate

Before delivery, the release record must prove:

| Control | Required evidence |
|---|---|
| Final artifact identity | Exact filename, size, SHA-256, manifest, and source provenance |
| Exact extraction | Clean extraction with safe paths, no duplicate entries, and manifest reconciliation |
| Exact launcher | Final packaged launcher executed from the extracted package |
| Exact operator workflow | User command executed byte-for-byte with the intended shell and environment |
| Target-state fidelity | Checksum-bound real target capture or independently justified equivalent fixture |
| Complete success | End-to-end completion through final state, evidence, and recovery |
| Complete failure coverage | Material failure and preserve-state paths with expected end states |
| Independent review | Requirements-derived expectations and separate fixtures or calculations |
| Assumptions | Zero unresolved assumptions before delivery |
| Iteration control | Zero user-visible replacement packages as the release target |

## 5. Failure and release reset

A user-visible failure triggers a release reset. The team must not automatically provide another executable revision. The reset requires:

1. evidence preservation;
2. exact state reconciliation;
3. design, implementation, review/test, delivery, and external-constraint classification;
4. systemic root-cause analysis;
5. refreshed requirements and threat model;
6. end-to-end test redesign;
7. independent review of the final distributed artifact and operator workflow;
8. new package-bound owner authorization when mutation is in scope.

## 6. Exception authority

Only Tim Simmons may approve a deviation. Approval must be exact, written, scoped, time-bounded, artifact-bound, and recorded under `docs/Exceptions/` before delivery.

No exception may be inferred from:

- “proceed” or “continue” instructions;
- schedule pressure;
- prior approvals for another package or gate;
- preserved mutation budget;
- a successful rollback;
- a non-mutating failure;
- an assistant or reviewer recommendation.

## 7. Exception record and authorization requirements

An approved exception record must include the owner identity, GitHub login, exact approval-text hash, approval and expiration timestamps, control identifiers, scope, rationale, residual risk, compensating controls, and artifact SHA-256 set. Placeholders, open-ended approvals, inherited approvals, and post-execution approvals are invalid.

The approval-text SHA-256 is the digest of a non-circular canonical authorization-basis preimage, encoded as UTF-8 with LF line endings and a final LF. The fixed field order is: exception status, approved by, approved GitHub login, approved UTC, control IDs, scope, rationale, residual risk, compensating controls, expiration UTC, artifact manifest path, and artifact SHA-256 set. The candidate head SHA and the approval-text SHA-256 field itself are excluded from that preimage. The exact GitHub owner comment separately binds the approved exception-record path set to the PR number and candidate head, so a new commit invalidates the approval without creating a self-referential commit hash.

Every approved exception must name one canonical JSON artifact manifest under `docs/Exceptions/Artifacts/`. The manifest contains a sorted, unique identity-to-SHA-256 list using only repository paths, external artifact IDs, or external incident IDs. Repository-path artifacts are verified against candidate bytes and must be regular non-symlink files. External identities are bound to their pre-verified digest but are not fetched by the repository validator. The exception record's artifact SHA-256 set must exactly equal the manifest digests in canonical identity order.

Time validity is evaluated only from trusted evidence. For GitHub qualification the authoritative evaluation instant is the GitHub pull-request event `updated_at` timestamp and the exact owner comment uses its GitHub `created_at` timestamp. Valid ordering is approved UTC less than or equal to owner-comment creation, owner-comment creation less than or equal to the trusted evaluation instant, and trusted evaluation instant strictly earlier than expiration UTC. Equality at expiration is expired. Offline tests must supply an explicit immutable fixture timestamp; local process wall-clock time is not release-authorizing evidence.

For a pull request that contains one or more approved exception records, the GitHub gate requires exactly one comment authored by `TimSimmons3` with this canonical form:

```text
APPROVE SMT MANDATORY ASSURANCE EXCEPTION PR=<PR_NUMBER> HEAD=<CURRENT_HEAD_SHA> EXCEPTIONS=<SORTED_COMMA_SEPARATED_EXCEPTION_PATHS>
```

The approval is valid only for the exact PR number, exact current head SHA, and exact sorted exception-record set. A new commit invalidates the prior approval. Wrong-owner, stale-head, duplicate, incomplete, expanded, or whitespace-altered comments fail closed.

GitHub pull-request review approval is not the owner-exception mechanism because pull-request authors cannot approve their own pull requests. The exact owner comment provides an auditable approval path for a repository currently operated by one project owner without creating a review deadlock or requiring an administrator bypass.

## 8. Handoff and Markdown requirements

Every new or modified governance Markdown file covered by the machine-readable policy must contain the invariant block exactly once. A governed file may declare an approved exception only by citing a valid exception record. Historical files are not rewritten solely to add the block, but modifying a historical governed file brings the complete file under this standard.

## 9. Enforcement

The canonical policy JSON, invariant validator, owner-approval validator, test suite, workflow, CODEOWNERS ownership map, and required GitHub status check form the enforcement chain.

The protected `main` branch must use an active repository ruleset with:

- pull requests required before merge;
- the `Mandatory assurance invariant gate` required;
- no ordinary bypass actor;
- review conversations resolved before merge;
- force pushes blocked;
- branch deletion blocked.

A required approval count or required CODEOWNER review is not used while the repository has only one owner and that owner authors the pull request. CODEOWNERS remains the authoritative ownership map and review-notification source. Owner approval is mandatory only for exception-bearing changes and is enforced by the exact bound comment mechanism above.

## 10. Audit outcomes

Use only:

```text
DELIVERABLE_COMPLETE
BLOCKED_WITH_EXACT_REASON
PARTIAL_WORK_COMPLETED_AND_NOT_RELEASED
```

Any violation of this standard is a release-process defect and must be recorded in the next handoff and corrective-action record.

## 11. Final assurance recovery controls

Release readiness requires complete applicable-state disposition, a requirements-derived independent oracle, zero expectation delta, zero unhandled exception surfaces, exact committed-candidate production-path qualification, and final adversarial review. Post-publication material defects have a target of zero. A material escape after a comprehensive/readiness claim is a release-process CAPA effectiveness failure and requires an assurance reset rather than a routine patch cycle.

Trust-root controls may not approve their own weakening. Default-branch trusted validation is the independent enforcement path after bootstrap adoption. Any trust-root migration requires exact project-owner authorization bound to the final head and exact changed trust-root path set.

## Post-R1 institutionalization control

```text
POST_R1_PROCESS_INSTITUTIONALIZATION=MANDATORY
POST_PUBLICATION_MATERIAL_ESCAPE=CAPA_EFFECTIVENESS_HOLD
AUTOMATIC_NEXT_CORRECTION_AFTER_ESCAPE=PROHIBITED
```

A material defect discovered after publication is evidence that a prior closure criterion failed. Preserve the exact candidate and evidence, classify the defect, identify the failed closure control, and obtain owner disposition before any new correction. Bounded accepted risk is permitted only with a fail-safe that prevents silent PASS.
