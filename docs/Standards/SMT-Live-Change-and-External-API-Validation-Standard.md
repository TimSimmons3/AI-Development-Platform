# SMT Live Change and External API Validation Standard

## 1. Purpose

Prevent production, repository, cloud, SaaS, and administrative changes from becoming test iterations.

## 2. Change classes

- Class R: read-only inspection.
- Class L: local reversible write.
- Class G: remote Git or repository write.
- Class P: platform administrative change.
- Class U: runtime or user-impacting mutation.
- Class I: irreversible or materially costly change.

Class G, P, U, and I changes require an explicit pre-state, mutation, post-state, and failure disposition.

## 3. Required external-contract record

For every API or platform response consumed, record:

- endpoint or UI function;
- request fields;
- response fields used;
- semantic fields;
- metadata and provenance fields;
- required and optional fields;
- ordering guarantees;
- documented defaults;
- observed omissions;
- allowed additional fields;
- freshness requirements;
- authoritative source of the contract.

No code may assume an absent field equals a default without explicit evidence.

## 4. Fixture hierarchy

From strongest to weakest:

1. checksum-bound real response captured from the target platform;
2. official documented example containing the complete consumed shape;
3. independently constructed contract fixture;
4. implementation-generated synthetic fixture.

Level 4 alone cannot authorize a live change.

## 5. Projection and normalization

- Compare only an explicit semantic projection.
- Preserve the complete raw response.
- Do not reject documented provenance metadata merely because it is not part of the semantic projection.
- Do not silently ignore unknown semantic fields.
- Match unordered collections by stable identity, not serialized object order.
- Record each normalization event.
- Produce field-level differences on mismatch.

## 6. Live-change hard cap

```text
DEFAULT_MAXIMUM_LIVE_ATTEMPTS=1
AUTOMATIC_PATCH_AND_RETRY=PROHIBITED
PRODUCTION_AS_TEST_ENVIRONMENT=PROHIBITED
```

A second attempt requires a new governance decision, not merely a code patch.

## 7. Manual-first criterion

Use a manual controlled change when:

- the change occurs once;
- the platform provides importable configuration;
- exact visual review is possible;
- automation would require substantial response normalization or rollback logic;
- evidence can be captured independently.

## 8. Evidence requirements

Capture:

- pre-state;
- exact intended configuration;
- operator identity;
- mutation time;
- raw response or screenshots;
- exact return code;
- created or modified object IDs;
- post-state;
- effective controls;
- rollback or preserve-state result;
- secret scan;
- hashes and archive manifest.

## 9. Review independence

The independent reviewer must challenge:

- whether the external response shape is complete;
- whether the fixture source is authoritative;
- whether defaults and order assumptions are justified;
- whether manual execution is safer;
- whether the end state, not just the command, was verified.

## 10. Stop conditions

Stop immediately when:

- a new undocumented field changes control interpretation;
- an expected artifact is missing;
- rollback cannot be confirmed;
- remote state is ambiguous;
- the authenticated identity is wrong;
- the change exceeds the authorized boundary;
- the same phase has already consumed its live-attempt budget.

## 11. Validation claim levels

Every report must state the highest proven level:

```text
LEVEL_1=STATIC_AND_PACKAGE_PASS
LEVEL_2=ISOLATED_PRODUCTION_PATH_PASS
LEVEL_3=TARGET_PRE_MUTATION_GATE_PASS
LEVEL_4=LIVE_MUTATION_AND_INDEPENDENT_POST_STATE_PASS
LEVEL_5=RELEASE_CLOSEOUT_AND_RECOVERABILITY_PASS
```

A lower level cannot authorize a higher-level claim. Live readiness requires Level 3 with no unresolved target-specific hold. Completion of a live transaction requires Level 4. Release completion and recoverability require Level 5.

## 12. Production-path parity

A release-authorizing rehearsal must identify and execute the critical production call path. It must not replace security-critical or mutation-critical functions with mocks, stubs, monkeypatches, or bypasses.

Recorded transport responses may be used only when the real collector, parser, normalizer, signer, verifier, registry writer, Git constructor, pusher, receipt writer, and evidence sealer execute. The validation report must include a production-versus-test call-path comparison.

## 13. Exact launcher and prompt rehearsal

Before release, run the actual launcher from a clean archive extraction. When signing and Git mutation are in scope, use:

- a temporary encrypted SSH key;
- a real temporary SSH agent;
- the production signer;
- actual Git SSH commit signing;
- a temporary bare Git remote;
- pseudo-terminal prompt capture;
- the production failure sealer.

The acceptance record must state the exact authorized prompt count and order. Any later unexpected prompt fails the rehearsal.

## 14. Agent-only signing

After `ssh-add`, preserve `SSH_AUTH_SOCK`. Later signing must use the public-key path and the agent-held private key without reopening the encrypted private-key file.

Disable askpass and terminal fallback after the authorized credential step. Use closed standard input and timeouts for noninteractive subprocesses. Verify loaded key count, full OpenSSH public-key encoding, and fingerprint.

## 15. Namespace-specific signing policy

Maintain separate allowed-signers policies for recovery, start gate, execution, and Git commit verification under namespace `git`. A policy or signature valid for one namespace is not proof for another.

## 16. Git tree, parent, and changed-path controls

For Git object construction, independently verify:

1. final tree contents;
2. parent commit;
3. changed paths and statuses from `git diff-tree`;
4. preservation of unrelated parent-tree entries;
5. status `A` when governed paths must be new;
6. the root-tree negative case.

A correct final tree is not sufficient evidence of a correct commit delta.

## 17. External API permission matrix

The external-contract record must also include:

- authentication mode;
- required token or account permission;
- endpoint path and method;
- pagination behavior;
- authoritative fixture source.

Prefer unauthenticated public endpoints for public registration data when appropriate. Before the first write, prove the required permission using a non-mutating endpoint or function with equivalent permission requirements.

## 18. Final pre-mutation recheck

Immediately before the first mutation:

- recollect local and external state;
- compare it with the initial preflight;
- bind both collections to the signed authorization or binding record when signing is in scope;
- verify authorization expiration;
- verify that zero mutation-capable calls occurred before the boundary.

A mismatch produces HOLD without repair or mutation.

## 19. Collection-wide evidence identity

Use one immutable collection identifier for the complete collection stage. Use different identifiers for initial preflight, final pre-mutation, and post-mutation stages.

Every envelope identifier must be unique. Sequence numbers must be contiguous. Missing, repeated, or reordered envelope identities fail the collection.

## 20. Raw evidence, semantic projection, and timestamps

Preserve complete raw responses and compare an explicit semantic projection. Normalize only documented non-semantic variation and record every normalization.

Omitted explicit `false` may be treated as equivalent only when the contract supports it. Match unordered effective-rule collections by stable identity. Reject duplicate rules, wrong provenance, actor drift, and undocumented semantic fields.

Do not require exact timestamp equality across separate API resources unless the contract guarantees it. Validate documented ordering and identity relationships.

## 21. Failure evidence sealer

The production failure sealer is release-critical. Exercise it through the actual production path for:

- pre-mutation failure;
- post-first-mutation preserve-state failure;
- parent-directory creation;
- dotted filenames;
- archive-member names;
- checksum generation;
- visible output;
- archive CRC and clean extraction.

Append `.zip` with basename-preserving logic rather than `Path.with_suffix()` when the artifact name contains dots. Never use `Path('')` as a missing-path sentinel.

## 22. Visible failure preservation

Shell error handling and cleanup must not erase the root cause. Print the exact error and preserve a mode-0600 failure report and evidence archive.

The report must state:

- whether a token was requested;
- whether the mutation boundary was crossed;
- the exact local end state;
- the exact remote end state;
- the preserved evidence paths.

Cleanup must not delete the only failure record.

## 23. Schema, hash, determinism, and parser controls

Design the artifact-binding and hash dependency graph as a directed acyclic graph. Reject circular hash dependencies. Recompute and retest every dependent hash and cross-binding after schema or policy changes.

Use fixed timestamps and deterministic identities when repeatable commit IDs or validation output are claimed. Repeated validation must be byte-identical when determinism is claimed.

For Timeshift or tabular platform rows:

- compare before and after identifier sets;
- require exactly one new identifier;
- match the exact row containing the unique label;
- do not inspect an adjacent-line window;
- preserve the creation transcript and final list;
- after a parser HOLD, continue from preserved state without creating a duplicate object.

## 24. Communication and live-iteration governance

Use only these release-state declarations:

```text
DELIVERABLE_COMPLETE
BLOCKED_WITH_EXACT_REASON
PARTIAL_WORK_COMPLETED_AND_NOT_RELEASED
```

Do not imply background work while the chat is idle. Do not present a package and simultaneously instruct the user not to run it. Do not call a package ready while a host-specific dependency remains unresolved.

```text
USER_VISIBLE_REPLACEMENT_PACKAGES_TARGET=0
LIVE_MUTATION_ATTEMPTS_PER_GATE_MAX=1
AUTOMATIC_PATCH_AND_RETRY=PROHIBITED
PRODUCTION_AS_TEST_ENVIRONMENT=PROHIBITED
```

A pre-mutation HOLD preserves the live-attempt budget. Repeated pre-mutation failures are release-process failures and require a release reset and independent review.
