# ADP v2.3.1 Gate C Runtime Execution Packet

## 1. Packet Control

- Packet ID: `V231-C-RUNTIME-01`
- Status: Prepared; executable only after `V231-C-PROMOTE-01` passes
- Scope: One-time collection setup and three independent Gate C runs
- Model: `llama3.2:3b`
- Collection: `ADP-v2.3.1-minimal-direct-retrieval`
- Source: `adp231_minimal_direct_retrieval.md`
- Prompt: `V231-R01-P1-v2`
- Governing standard: `docs/ADP-Controlled-Execution-Packet-Standard.md`

## 2. Objective

Execute the complete three-run Gate C block in one operator session without returning to chat between successful runs.

## 3. Entry Conditions

Proceed only when the original promotion transcript contains:

- `PROMOTION_STATUS=PASS`
- `SYNCHRONIZATION_STATUS=PASS`
- `READ_ONLY_PRE_RUNTIME_STATUS=PASS`
- Promotion commit `efa97c5`

Proceed only when the post-promotion correction transcript also contains:

- `CORRECTION_STATUS=PASS`
- `SEMANTIC_TRACEABILITY_STATUS=PASS`
- `TIMESHIFT_BASELINE_STATUS=PASS`
- `POST_CORRECTION_SYNCHRONIZATION_STATUS=PASS`
- `RUNTIME_ENTRY_STATUS=PASS`
- `NEXT_PACKET=V231-C-RUNTIME-01`

The required predecessor snapshot is:

- Identifier: `2026-07-20_11-32-48`
- Stored description: `ADP-v2.3-reg-hardening-t01-failure-closeout`

Also confirm no relevant repository, runtime, service, model, network, security, or recoverability state changed after the correction transcript.

## 4. One-Time Setup

1. Confirm the prior `ADP-v2.3-synthetic-rag-hardening` collection remains absent.
2. Create exactly one collection named `ADP-v2.3.1-minimal-direct-retrieval`.
3. Upload only `adp231_minimal_direct_retrieval.md`.
4. Confirm the collection contains exactly that one file.
5. Preserve setup screenshots and local source checksum evidence.

Do not execute a prompt during setup verification.

## 5. Three-Run Block

Perform runs 1, 2, and 3 using the approved test-record template and Knowledge Attachment Evidence Procedure.

For each run:

1. Capture new collection-membership evidence.
2. Start and prove a new empty chat.
3. Confirm `llama3.2:3b` and no enabled tool or automation feature.
4. Attach the exact collection and capture attachment evidence.
5. Capture `RUN_START`.
6. Submit the frozen prompt exactly once.
7. Preserve the complete response and displayed-source evidence.
8. Capture `RUN_END` and the exact bounded truncation evidence.
9. Complete `V231-R01`, `V231-S01`, environment, and overall classification.

## 6. Automatic Continuation Between Runs

After run 1 or run 2, proceed directly to the next run without external approval only when:

- Overall run result is PASS.
- No stop condition occurred.
- Required evidence is complete.
- No controlled variable changed.

Do not pause merely to report that a run passed.

## 7. Stop Conditions

Stop the packet immediately and do not submit another prompt when any run is FAIL or INCONCLUSIVE, or when any procedure stop condition occurs.

A formatting observation alone does not stop Gate C unless it also creates an unsupported claim, automation output, or another defined failure.

## 8. Completion Conditions

The packet completes successfully only when all three runs are PASS for:

- `V231-R01`
- `V231-S01`
- Prompt-truncation assessment
- Evidence and control assessment
- Overall run classification

## 9. Return Bundle

Return one consolidated evidence bundle after run 3 passes or immediately after the first stop condition. The bundle shall contain:

- Setup evidence
- Three completed run records, or completed records through the stop
- Screenshots
- Exact prompt and responses
- Displayed-source evidence
- `RUN_START`, `RUN_END`, and bounded Ollama logs
- Packet status: PASS, FAIL, or INCONCLUSIVE
- Stop reason when applicable

No intermediate chat transition is required between successful runs.

## 10. Exclusions

This packet does not authorize:

- Prompt revision
- Same-chat retry
- Model comparison
- Multi-file expansion
- Formatting qualification
- Cleanup or removal validation
- Runtime, model, network, firewall, Docker, or context changes
- ADP v2.4 work
