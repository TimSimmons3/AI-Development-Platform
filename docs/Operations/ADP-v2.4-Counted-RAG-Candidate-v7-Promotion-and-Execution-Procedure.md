# ADP v2.4 Counted RAG Candidate v7 Promotion and Execution Procedure

## Current boundary

C1 is an applied, uncommitted design state. It authorizes no runtime action, Git commit, push, tag, C2 freeze, registry creation, or counted execution.

## Promotion order

1. Validate all 68 C1 paths, modes, and hashes.
2. Run the Candidate v7 quality gate and five independent readiness passes.
3. Perform a full-diff review from `b934c7bd84bfbc35563f3681712c4d5bd8478196` to the applied C1 state.
4. Issue a separate C1 commit authorization only after all reviews pass.
5. Create C1, generate the canonical promotion attestation, and sign it under `adp-v2.4-candidate-v7-promotion`.
6. Validate exact C1 commit, tree, parent, changed paths, artifact hashes, and signature.
7. Apply only the six frozen C2 paths.
8. Independently review C2 and create the final procedure freeze.
9. Generate and sign the single-use execution authorization under `adp-v2.4-candidate-v7-execution`.
10. Only after C2 and execution authorization exist, create the durable registry reservation and signed witness anchor.
11. Counted execution remains separately authorized, single-use, fail-closed, and no-retry.

## Immediate stop conditions

Stop for any hash, path, mode, signature, namespace, commit, tree, branch, registry, witness, evidence, runtime, or authorization mismatch. Preserve evidence. Do not improvise or retry.
