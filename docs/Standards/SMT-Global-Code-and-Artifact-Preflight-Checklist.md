# SMT Global Code and Artifact Preflight Checklist

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


## 1. Release identification

- [ ] Deliverable name and corrected revision are unambiguous.
- [ ] Purpose, scope, exclusions, and authority are recorded.
- [ ] Data currency, timezone, units, and assumptions are stated.
- [ ] Source-of-truth files and hashes are recorded.
- [ ] Superseded inputs are identified and excluded.

## 2. Design assurance

- [ ] Design is documented before implementation.
- [ ] Dependencies and external contracts are complete.
- [ ] State machine and mutation boundaries are documented.
- [ ] Rollback and preserve-state boundaries are documented.
- [ ] Failure disposition is defined for every stage.
- [ ] Manual versus automated implementation has been justified.
- [ ] Complexity is proportionate to the task.

## 3. Code and configuration assurance

- [ ] Syntax, AST, compilation, or bytecode checks pass.
- [ ] Shell scripts pass syntax and applicable lint checks.
- [ ] Schemas parse and validate.
- [ ] Strict JSON duplicate-key behavior is tested.
- [ ] Canonicalization vectors pass.
- [ ] Default, ordering, optional-field, and additional-field behavior is tested.
- [ ] All changed components are included in the impact analysis.
- [ ] No frozen source file was modified.
- [ ] Permissions, owners, file types, links, and paths are validated.
- [ ] Secrets, tokens, private keys, and unnecessary PII are absent.

## 4. Workflow assurance

- [ ] Full success path passes in isolation.
- [ ] Every identified failure path is executed.
- [ ] Expected end state is verified after each failure.
- [ ] Cleanup and non-mutation checks pass.
- [ ] Crash and interruption behavior is tested.
- [ ] External command return codes and outputs are validated.
- [ ] User-facing commands have been rehearsed exactly.
- [ ] User interface evidence instructions are practical and unambiguous.

## 5. Independent review

- [ ] Reviewer uses independently derived expectations.
- [ ] Reviewer does not reuse the implementation fixture builder.
- [ ] External contracts are independently checked.
- [ ] File counts, paths, sizes, modes, and hashes reconcile.
- [ ] Manifest and archive round trip pass.
- [ ] Reviewer tests substantive negative cases.
- [ ] Reviewer verifies delivery links and artifact availability.
- [ ] Reviewer states unresolved risk and confidence.

## 6. Packaging and delivery

- [ ] Every deliverable exists at the exact linked path.
- [ ] Package checksum companion verifies.
- [ ] Validation report checksum companion verifies.
- [ ] Archive extraction and compressed-data tests pass.
- [ ] Extracted manifest reconciliation passes.
- [ ] Deterministic rebuild passes when required.
- [ ] Required runbook and closeout records are included.
- [ ] No misleading final or complete label is used.
- [ ] User-visible replacement package count is zero unless a defect was discovered after delivery.

## 7. Live-change gate

- [ ] Pre-state is captured and verified.
- [ ] External state is fresh enough for the decision.
- [ ] Maximum live-attempt count is explicit.
- [ ] Operator authorization phrase or confirmation is explicit.
- [ ] Mutation is minimal and bounded.
- [ ] Post-state verification is read-only and independent.
- [ ] Failure evidence capture is automatic or immediately available.
- [ ] No downstream action occurs until review.
- [ ] A failed live attempt stops rather than loops.

## 8. Closeout

- [ ] Final local and remote state reconcile.
- [ ] Working tree is clean.
- [ ] Commits, branches, tags, and origins align.
- [ ] Evidence archive and checksum pass.
- [ ] Backup and recovery records exist.
- [ ] Lessons learned are integrated into the canonical skill and standards.
- [ ] New-chat handoff is complete and copy-ready.

## 9. ADP v2.4 mandatory assurance delta

### 9.1 Validation claims and call-path parity

- [ ] The report states the highest proven validation level from Level 1 through Level 5.
- [ ] No generic `PASS` implies a higher level than the evidence supports.
- [ ] The production-versus-test call-path comparison identifies every critical function.
- [ ] No security-critical or mutation-critical production function is stubbed, monkeypatched, bypassed, or replaced in a release-authorizing rehearsal.
- [ ] Any recorded network transport still exercises the real collector, parser, normalizer, signer, verifier, writer, Git constructor, pusher, receipt writer, and evidence sealer.
- [ ] No test is labeled `full success` when a critical production function is replaced.

### 9.2 Exact launcher, prompts, and signing

- [ ] The actual launcher is rehearsed from a clean archive extraction.
- [ ] The signing rehearsal uses a temporary encrypted SSH key and a real temporary SSH agent.
- [ ] The production signer and actual Git SSH commit signing execute.
- [ ] A temporary bare Git remote is used when push behavior is in scope.
- [ ] Pseudo-terminal prompt capture records exact prompt count and order.
- [ ] Unexpected prompts after the authorized credential stage fail the test.
- [ ] `SSH_AUTH_SOCK` is preserved after `ssh-add`.
- [ ] Later signing uses the public-key path and agent-held private key without reopening the encrypted key file.
- [ ] Askpass and terminal fallback are disabled for noninteractive signing.
- [ ] Noninteractive subprocesses use closed standard input and explicit timeouts.
- [ ] Loaded key count, full OpenSSH public-key encoding, and fingerprint are verified.
- [ ] Separate allowed-signers policies exist for recovery, start gate, execution, and namespace `git`.

### 9.3 Git object and external-contract controls

- [ ] Final tree contents and parent commit are verified separately.
- [ ] `git diff-tree` changed paths and statuses match the authorization.
- [ ] Unrelated parent-tree entries are preserved.
- [ ] Governed new witness paths have status `A`, not `M`.
- [ ] The root-tree negative case is tested.
- [ ] Every endpoint records authentication mode, required permission, method, path, consumed fields, ordering, omission, freshness, pagination, and fixture source.
- [ ] Public unauthenticated endpoints are preferred for public data when appropriate.
- [ ] Required write permission is proven before mutation with a non-mutating equivalent-permission operation.

### 9.4 Final pre-mutation and evidence controls

- [ ] Initial and final pre-mutation local and external collections are both captured.
- [ ] The two collections are compared and bound to the authorization.
- [ ] Authorization expiration is verified immediately before mutation.
- [ ] Zero mutation-capable calls occurred before the boundary.
- [ ] Each collection stage has one immutable collection identifier.
- [ ] Envelope identifiers are unique and sequence numbers are contiguous.
- [ ] Complete raw responses are retained.
- [ ] Semantic projection and every normalization are documented.
- [ ] Omitted explicit `false` is normalized only when supported by the contract.
- [ ] Unordered effective rules are matched by stable identity.
- [ ] Duplicate rules, wrong provenance, actor drift, and undocumented semantic fields are rejected.
- [ ] Cross-resource timestamps are compared only according to documented ordering and identity guarantees.

### 9.5 Failure, hash, determinism, and parser controls

- [ ] The production failure sealer is exercised for pre-mutation and preserve-state failures.
- [ ] Failure-sealer tests cover path creation, dotted filenames, archive names, checksums, visible output, CRC, and clean extraction.
- [ ] Archive extension logic preserves dotted basenames.
- [ ] Missing evidence paths cannot become `Path('')` or render as `.`.
- [ ] Root-cause output survives shell error handling and cleanup.
- [ ] Failure reports and evidence archives use mode 0600.
- [ ] Failure evidence states token request, mutation-boundary status, and exact local and remote end state.
- [ ] The artifact-binding and hash graph is acyclic.
- [ ] Dependent hashes and cross-bindings are recomputed after policy or schema changes.
- [ ] Repeated deterministic validation is byte-identical.
- [ ] Snapshot or tabular-row selection compares before and after identifier sets.
- [ ] Exactly one new identifier and the exact uniquely labeled row are required.
- [ ] Parser continuation reuses preserved state and does not create a duplicate object.

### 9.6 Communication and iteration governance

- [ ] Delivery state is exactly `DELIVERABLE_COMPLETE`, `BLOCKED_WITH_EXACT_REASON`, or `PARTIAL_WORK_COMPLETED_AND_NOT_RELEASED`.
- [ ] No message implies background work while the chat is idle.
- [ ] No artifact is presented with contradictory instructions not to run it.
- [ ] No artifact is called ready while host-specific dependencies remain unresolved.
- [ ] Design, implementation, review/test, delivery, and external-constraint defects are distinguished.
- [ ] Implementation or test defects use corrected revisions rather than new conceptual versions.
- [ ] User-visible replacement package target is zero.
- [ ] Live mutation attempts per gate do not exceed one.
- [ ] Automatic patch-and-retry and production-as-test behavior are prohibited.
- [ ] Repeated pre-mutation failures trigger release reset and independent review.

## 10. Transition metrics and handoff governance

- [ ] M01-M28 snapshot exists at required collection gates.
- [ ] `UNKNOWN` values are explicit and are not zero/PASS.
- [ ] Timing intervals exclude external/user hold from M22 and use no surveillance telemetry.
- [ ] M24 runs include mandatory release-layer metadata.
- [ ] Repeated M25 defects link to the violated prior lesson/control.
- [ ] Handoff M26 is 100 percent with every canonical component and paired JSON/CSV.
- [ ] M27 is validator-derived and data gaps remain visible.
- [ ] Lifecycle/deviation records satisfy the canonical transition policy.
- [ ] Change records contain all mandatory scope, dependency, security, test, evidence, recovery, metrics, and authorization fields.
- [ ] Remote publication re-observes protected-main status before merge.

## Final assurance state-space preflight

Before release authorization, verify all of the following: applicable state/equivalence classes are enumerated; 100% of applicable oracle cells are dispositioned; independent expected results are fixed without implementation-derived expectations; oracle-versus-implementation delta is zero; A/M/D/T and Git object-mode transitions are covered in real repositories; parser/type/cardinality/depth/size/encoding exception surfaces have zero unhandled escapes; exact committed candidate passes production `--base-ref`; base/head/tree are current; exact artifact/operator and failure/preserve-state rehearsals pass; full regression passes; and final adversarial review has zero unresolved material findings.

If any item is unavailable, the release state is HOLD. A large test count cannot substitute for an undispositioned state class.

### Finite assurance-model convergence

Before implementation or publication, verify that denominator growth is controlled by authoritative requirements and materially distinct enforcement outcomes. Equivalent variants with the same governing requirement, expected disposition, and material enforcement branch must be enumerated as independently executed probe subcases instead of creating an unbounded cell/version loop. A new denominator cell requires a documented missing requirement, contradictory outcome, materially distinct enforcement branch, or proof ambiguity that cannot be resolved under an existing cell.

## Post-R1 process-institutionalization preflight

```text
PROCESS_INSTITUTIONALIZATION_PREFLIGHT=MANDATORY
SCENARIO_FAITHFUL_PROBE_MAPPING=MANDATORY
EXACT_CANDIDATE_EVIDENCE_BINDING=MANDATORY
PROXY_ONLY_QUALIFICATION_COUNT=0
SELF_DECLARED_OBSERVED_ENFORCEMENT_COUNT=0
```

Before implementation, reconcile authoritative requirements, materially distinct outcomes, Git state classes, external contracts, dependencies, exception states, and release states. Before delivery, prove every material production change with a pre-fix failing exact probe, reject stale candidate-bound evidence, rehearse the exact distributed operator, and require portable manifests.

### Committed candidate requirement for delta-aware validators

```text
COMMIT_DELTA_VALIDATOR_REQUIRES_COMMITTED_FIXTURE=TRUE
PRECOMMIT_EMPTY_DELTA_MAY_NOT_AUTHORIZE_RELEASE=TRUE
```

For change-aware validators, create or simulate an isolated committed candidate before claiming change-scope validation. Verify the validator observes the intended changed-path set. A PASS against an empty committed delta is non-authorizing.
