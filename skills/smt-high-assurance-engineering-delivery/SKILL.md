# SMT High-Assurance Engineering Delivery Skill

## Mandatory assurance invariant

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

## 1. Status and scope

```text
SKILL_STATUS=CANONICAL_REPO_INTEGRATION_RECORD
APPLIES_TO=CODE_SCRIPTS_DOCUMENTS_PACKAGES_DATA_CONVERSIONS_INFRASTRUCTURE_AND_LIVE_CHANGES
DEFAULT_ASSURANCE_LEVEL=HIGH
```

This skill is mandatory for Send Manna Too LLC and ADP deliverables unless a written exception narrows the scope. It is a repo-integrable skill record; it does not modify ChatGPT's system-level built-in skills by itself.

## 2. Operating objective

Deliver the best supportable version in the first user-visible pass. Minimize user-visible revisions without hiding uncertainty. Accuracy, safety, evidence, reproducibility, and recoverability take precedence over speed or polish.

## 3. Mandatory gate model

### Gate 0 - Intent and authorization

- Define the requested outcome, exclusions, authority, mutation boundary, and success criteria.
- Identify whether the task is read-only, local-write, remote-write, runtime mutation, or irreversible.
- Refuse to proceed when authority or required inputs are missing.

### Gate 1 - Source-of-truth inventory

- Identify every authoritative input.
- Record file names, versions, paths, sizes, hashes, dates, and provenance.
- Distinguish authoritative, supporting, stale, superseded, and missing sources.
- Do not silently infer missing fields.

### Gate 2 - Design and dependency review

- Produce a design before implementation.
- Inventory direct and transitive dependencies, commands, libraries, APIs, schemas, UI steps, and external contracts.
- Define state transitions, rollback boundaries, preserve-state boundaries, and failure dispositions.
- Classify risks and residual uncertainty.

### Gate 3 - Implementation

- Use the least complex mechanism that satisfies the control objective.
- Prefer simple, inspectable, standard tools over custom automation.
- Keep frozen source directories byte-identical.
- Use corrected revisions for implementation or test defects; do not inflate package versions.
- Use restrictive permissions and no-follow filesystem operations where relevant.
- Never package secrets, private keys, tokens, or unnecessary PII.

### Gate 4 - Static and structural validation

As applicable, require:

- syntax and AST validation;
- bytecode or compilation checks;
- shell syntax and linting;
- schema validation;
- duplicate-key rejection;
- dependency and import inventory;
- file-set, size, mode, and SHA-256 reconciliation;
- deterministic archive construction;
- secret and token scanning;
- grammar, headings, counts, dates, and cross-reference checks.

### Gate 5 - Success-path rehearsal

Rehearse the complete path end to end in an isolated environment, including:

- exact inputs;
- exact commands;
- outputs and markers;
- created files;
- state transitions;
- signature and checksum validation;
- cleanup;
- final non-mutation or intended mutation result.

Testing isolated functions is not a substitute for a full workflow rehearsal.

### Gate 6 - Failure-path testing

Test every identified failure path, including:

- missing inputs;
- wrong hashes;
- stale state;
- malformed data;
- duplicate data;
- permissions;
- symlinks;
- wrong owner or mode;
- API omissions and additional fields;
- ordering;
- defaults;
- timeouts;
- partial writes;
- interrupted execution;
- wrong signer, namespace, or key;
- rollback failure;
- preserve-state boundary.

The test matrix must state the expected end state, not merely the expected error message.

### Gate 7 - Independent review

The reviewer must be structurally independent:

- do not reuse the implementation's expected-output builder;
- do not rely solely on the same fixtures;
- independently derive expected values;
- challenge source completeness and external-contract coverage;
- verify mutation and non-mutation claims;
- rehearse the user workflow;
- reconcile artifacts and manifests.

A self-test plus a reviewer using the same assumptions is not independent assurance.

### Gate 8 - Release and delivery

Before delivery:

- confirm every linked artifact exists;
- verify package and report hashes;
- verify archive extraction and manifest round trip;
- provide exact names and no-renaming instructions where required;
- state assumptions, holds, residual risks, and data currency;
- provide only commands already rehearsed;
- ensure commands are flat, ASCII-safe, and appropriate for the user's environment.

### Gate 9 - Live execution

- Use live mutation only after all prior gates pass.
- Set an explicit maximum live-attempt count, normally one.
- A live failure stops the gate and triggers evidence preservation and disposition.
- Do not issue incremental recovery packages automatically.
- Do not use production or live platform mutation as a test harness.

### Gate 10 - Closeout

- independently verify final state;
- reconcile repository, remote, artifacts, evidence, and checksums;
- confirm all holds or authorizations;
- create closeout, backup, checksum, and handoff records;
- document defects, lessons, and residual risk;
- ensure recovery is possible.

## 4. Defect classification and revision policy

Every defect must be classified:

- Design defect: the intended behavior or control model was wrong or incomplete.
- Implementation defect: the design was correct but the code or document did not implement it.
- Review/test defect: validation failed to detect a defect or relied on invalid assumptions.
- Delivery defect: the artifact was missing, mislabeled, unlinked, or unusable.
- External constraint: the platform cannot support the required behavior.

Implementation and review defects produce corrected revisions, not new conceptual versions, unless the external contract or architecture changes materially.

## 5. Anti-loop policy

```text
LIVE_ATTEMPTS_PER_GATE_MAXIMUM=1
INCREMENTAL_RECOVERY_PACKAGE_CHAIN=PROHIBITED
USER_VISIBLE_REPLACEMENT_PACKAGE_TARGET: 0
FINAL_LABEL_REQUIRES_FULL_EXTERNAL_CONTRACT_COVERAGE=TRUE
```

When a failure occurs:

1. preserve evidence;
2. confirm remote and local end state;
3. classify the defect;
4. decide whether the phase is blocked, manual, redesigned, or abandoned;
5. do not assume a patch and retry is the correct response.

## 6. External API and platform rule

- Enumerate every consumed request and response field.
- Separate semantic fields from metadata and provenance fields.
- Treat arrays as ordered only when the contract guarantees order.
- Treat missing values as defaults only when the platform contract or captured evidence supports that exact normalization.
- Permit additional fields only through an explicit projection, never by silently ignoring the entire response.
- Preserve raw responses for audit.
- Use official documentation and captured real responses as independent fixtures.
- Revalidate time-sensitive platform behavior before execution.

## 7. Artifact assurance rule

Every package must include:

- release or handoff record;
- manifest;
- SHA-256 checksum companion;
- validation report;
- source inventory;
- file count;
- modes and sizes when relevant;
- deterministic or reproducible build method;
- extraction and read-back test;
- secret scan;
- residual-risk statement.

Never tell the user to download an artifact until its exact path exists and is verified.

## 8. Terminal command standard

Commands supplied to the user must:

- be flat ASCII;
- avoid heredocs unless explicitly approved;
- avoid nested shell constructs when a simpler gate is possible;
- not use `exit` or destructive fall-through;
- use staged prechecks before mutation;
- print unambiguous markers;
- capture return codes;
- stop after each authorized gate;
- avoid hidden side effects;
- preserve complete output for review.

## 9. Manual versus automation decision

Choose manual execution when:

- the task is one-time or rare;
- the platform offers exact import or UI configuration;
- automation adds more states than the change itself;
- the API response contract is unstable or poorly represented;
- human review of every field materially reduces risk.

Choose automation when it is repeatable, fully contract-tested, recoverable, and simpler than the manual alternative.

## 10. Definition of ready

A deliverable is ready for implementation only when:

```text
INTENT_DEFINED=PASS
AUTHORITY_CONFIRMED=PASS
SOURCE_INVENTORY=PASS
DEPENDENCY_INVENTORY=PASS
EXTERNAL_CONTRACT_INVENTORY=PASS
DESIGN_REVIEW=PASS
MUTATION_BOUNDARY=PASS
FAILURE_DISPOSITION_MATRIX=PASS
TEST_PLAN=PASS
INDEPENDENT_REVIEW_PLAN=PASS
```

## 11. Definition of done

A deliverable is done only when:

```text
STATIC_VALIDATION=PASS
SUCCESS_PATH_REHEARSAL=PASS
FAILURE_PATH_TESTS=PASS
INDEPENDENT_REVIEW=PASS
ARTIFACT_RECONCILIATION=PASS
SECRET_SCAN=PASS
DELIVERY_LINK_VALIDATION=PASS
FINAL_STATE_VERIFICATION=PASS
RECOVERY_EVIDENCE=PASS
CLOSEOUT_AND_HANDOFF=PASS
```

## 12. Prohibited practices

- claiming completion before external state is verified;
- issuing code that has not passed the complete workflow rehearsal;
- reusing the same fixture generator for implementation and independent review;
- adding retries to conceal unresolved deterministic defects;
- using live execution to discover expected API behavior;
- referring to an artifact that has not been created and linked;
- calling a package final while known contract gaps remain;
- asking the user to repeat information already available;
- continuing a failing strategy merely because rollback succeeds.

## 13. Mandatory ADP v2.4 assurance controls

The following controls are mandatory for future ADP work and for any other workstream that adopts this skill.

### 13.1 Validation claim levels

Every validation report must state the highest level actually proven:

```text
LEVEL_1=STATIC_AND_PACKAGE_PASS
LEVEL_2=ISOLATED_PRODUCTION_PATH_PASS
LEVEL_3=TARGET_PRE_MUTATION_GATE_PASS
LEVEL_4=LIVE_MUTATION_AND_INDEPENDENT_POST_STATE_PASS
LEVEL_5=RELEASE_CLOSEOUT_AND_RECOVERABILITY_PASS
```

A lower level must not be described as live-ready when unresolved target-specific holds remain. A generic `PASS` must not imply a higher level than the evidence supports.

### 13.2 Production-path parity and exact launcher rehearsal

- Identify the exact production functions exercised by each success rehearsal.
- Publish a production-versus-test call-path comparison.
- Do not monkeypatch, stub, bypass, or replace security-critical or mutation-critical production functions in a release-authorizing rehearsal.
- Authoritative recorded network responses may replace transport only when the real collector, parser, normalizer, signer, verifier, registry writer, Git constructor, pusher, receipt writer, and evidence sealer still execute.
- Do not label a test `full success` when any critical production function is replaced.
- Rehearse the actual launcher from a clean archive extraction.
- When signing is in scope, use a temporary encrypted SSH key, a real temporary SSH agent, the production signer, actual Git SSH commit signing, a temporary bare remote, pseudo-terminal prompt capture, and the production failure sealer.
- State the exact expected prompt count and order. Any unexpected prompt after the authorized credential stage is a failure.

### 13.3 Agent-only signing and namespace isolation

After `ssh-add`:

- preserve `SSH_AUTH_SOCK`;
- sign through the agent using the public-key path;
- never reopen the encrypted private-key file;
- disable askpass and terminal fallback for later signing;
- use `stdin=DEVNULL` or equivalent for noninteractive subprocesses;
- apply explicit timeouts;
- verify loaded key count, full OpenSSH public-key encoding, and fingerprint.

Use separate allowed-signers policies for recovery, start-gate, execution, and Git commit verification under namespace `git`. Evidence valid for one namespace must not be reused as proof for another.

### 13.4 Git parent-tree and changed-path controls

For governed Git object construction:

- verify the final tree contents;
- verify the parent commit;
- verify changed paths and statuses with `git diff-tree`;
- preserve every unrelated parent-tree entry;
- require status `A` when governed witness paths must be new;
- test the root-tree negative case explicitly.

A correct final tree does not by itself prove a correct commit delta.

### 13.5 External API contract and permission matrix

For every endpoint or platform function, record:

- authentication mode;
- required token or account permission;
- endpoint path and method;
- consumed request and response fields;
- ordering and omission semantics;
- freshness requirement;
- pagination behavior;
- authoritative fixture source.

Prefer unauthenticated public endpoints for public registration data when this avoids unnecessary permissions. Prove required write permissions before the first mutation with a non-mutating operation that requires equivalent permission.

### 13.6 Final pre-mutation recheck

Immediately before the first mutation:

- recollect local and external state;
- compare it with the initial preflight;
- bind both collections into signed authorization or binding records when signing is in scope;
- verify authorization expiration;
- require zero mutation-capable calls before the boundary.

### 13.7 Evidence identity, projection, and timestamps

- Use one immutable collection identifier for each complete collection stage.
- Use different collection identifiers for distinct stages such as pre-mutation and post-mutation.
- Require unique envelope identifiers and contiguous sequence numbers.
- Preserve complete raw responses.
- Compare an explicit semantic projection.
- Normalize only documented non-semantic variation and record every normalization.
- Treat omitted explicit `false` as equivalent only when the contract supports it.
- Match unordered effective-rule collections by stable identity.
- Reject duplicate rules, wrong provenance, actor drift, and undocumented semantic fields.
- Do not require exact timestamp equality across resources unless the contract guarantees it. Validate documented ordering and identity relationships instead.

### 13.8 Failure evidence sealer and visible failure preservation

The production failure sealer is release-critical code. Test it through the actual production path for:

- pre-mutation failure;
- post-first-mutation preserve-state failure;
- parent-directory creation;
- dotted filenames;
- archive member names;
- checksum generation;
- visible output;
- archive CRC and clean extraction.

Append archive extensions with basename-preserving logic. Do not use `Path.with_suffix()` to append `.zip` to a dotted artifact name. Do not convert a missing evidence path to `Path('')`.

Failure handling must:

- preserve the exact root-cause output;
- prevent `set -e` or cleanup from hiding the error;
- create a mode-0600 failure report and evidence archive;
- state whether a token was requested;
- state whether the mutation boundary was crossed;
- state the exact local and remote end state;
- retain the only failure record.

### 13.9 Schema, hash, and determinism controls

- Design the artifact-binding and hash dependency graph as a directed acyclic graph before schemas are finalized.
- Reject circular hash dependencies.
- Recompute and retest all dependent hashes and cross-bindings after any schema or policy change.
- Use fixed timestamps and deterministic identities where repeated commit IDs or outputs are claimed.
- Require byte-identical repeated validation when determinism is claimed.

### 13.10 Timeshift and tabular parser controls

When selecting a newly created snapshot or platform row:

- compare before and after identifier sets;
- require exactly one new identifier;
- match the exact row containing the unique comment or label;
- do not search an adjacent-line window;
- preserve the creation transcript and final list;
- after a parser HOLD, continue from preserved state and do not create a duplicate object.

### 13.11 Communication truthfulness and live-iteration governance

Use only these delivery-state declarations:

```text
DELIVERABLE_COMPLETE
BLOCKED_WITH_EXACT_REASON
PARTIAL_WORK_COMPLETED_AND_NOT_RELEASED
```

Do not imply that work continues while the chat is idle. Do not present an artifact and simultaneously instruct the user not to run it. Do not call an artifact ready while a host-specific dependency remains unresolved.

```text
USER_VISIBLE_REPLACEMENT_PACKAGES_TARGET=0
LIVE_MUTATION_ATTEMPTS_PER_GATE_MAX=1
AUTOMATIC_PATCH_AND_RETRY=PROHIBITED
PRODUCTION_AS_TEST_ENVIRONMENT: PROHIBITED
```

A pre-mutation HOLD preserves the live-mutation budget but does not justify repeated user-visible candidates. Repeated pre-mutation failures require a release reset and independent review.

## 18. Final assurance state-model and trust-root gate

For release-authorizing work, test count is supporting evidence and is never the denominator. Before release, enumerate externally observable state and equivalence classes, freeze an independently derived oracle, and disposition 100% of applicable cells. The expected result must be derived from requirements and architecture, not from the implementation under test. Required release results are `APPLICABLE_STATE_COVERAGE=100_PERCENT`, `INDEPENDENT_VS_IMPLEMENTATION_EXPECTATION_DELTA=0`, `UNHANDLED_EXCEPTION_SURFACES=0`, and `UNRESOLVED_MATERIAL_FINDINGS=0`.

Repository-diff governance must use a shared NUL-delimited, fail-closed Git object/status contract. A/M/D/T, mode-only, regular/symlink/gitlink, D+A rename/move, file/tree replacement, unusual safe pathnames, invalid base refs, and unexpected statuses must be dispositioned in real disposable repositories. Release-authorizing validation must bind exact base SHA, merge base, head SHA, candidate tree, and committed HEAD object identity; working-tree-only evidence is insufficient.

Security-sensitive validators, policies, workflows, and oracle assets form an assurance trust root. Future privileged validation must execute default-branch trusted code and treat pull-request content only as data. Ordinary self-modification of trust-root controls is prohibited. A trust-root migration requires an explicit migration record plus exact owner approval bound to the final head and changed trust-root path digest.

A material finding that escapes a candidate described as comprehensive is a CAPA effectiveness failure. Stop release, preserve evidence, reset to model/oracle root cause, and complete fresh adversarial review before another executable is exposed. Review administration is metadata-only; repository content create/update/delete actions are prohibited unless separately authorized as engineering mutation.

A release denominator is requirements-governed, not reviewer-governed. After authoritative requirements and materially distinct enforcement outcomes are mapped, do not create new denominator cells solely because a reviewer can subdivide an equivalent case further. Same-requirement, same-expected-outcome, same-material-enforcement-branch variants become mandatory independently executed probe subcases. Reopen the denominator only for an unmapped authoritative requirement, a contradictory expected outcome, a materially distinct enforcement branch, or a scenario that cannot be proven without ambiguity under an existing cell.

## Post-R1 permanent process institutionalization

```text
POST_R1_PROCESS_INSTITUTIONALIZATION=MANDATORY
REQUIREMENTS_INVENTORY_BEFORE_IMPLEMENTATION=MANDATORY
PRODUCTION_CHANGE_REQUIRES_FAILED_EXACT_PROBE=TRUE
SCENARIO_FAITHFUL_EVIDENCE=MANDATORY
EXTERNAL_EVIDENCE_DEFAULT=HOLD_ONLY
POST_PUBLICATION_MATERIAL_ESCAPE=CAPA_EFFECTIVENESS_HOLD
```

Future work must apply PI-01 through PI-16 and report P01-P14. Test count is supporting evidence, not completeness. Reviewer silence is not a release criterion. Evidence must be bound to the exact clean candidate. Lessons learned are not considered institutionalized until represented in skills, standards, policy, tests, handoff fields, release gates, and recoverability evidence.

## PR #6 material-review escape enforcement

```text
PROCESS_METRICS_IDENTITY_VERIFICATION=MANDATORY
PROCESS_METRICS_DELETION=FAIL_CLOSED
HANDOFF_REQUIRED_SECTION_CONTENT=MANDATORY
```

Treat commit/tree identity, governed evidence-record deletion, and completed handoff bodies as release-enforcement surfaces, not documentation quality suggestions.
