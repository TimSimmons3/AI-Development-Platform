# ADP v2.3.1 Gate C Approved Artifact Manifest

## 1. Package Control

- Package status: POST-PROMOTION CORRECTION APPROVED
- Original repository baseline represented: `253e9dd`
- Successful Gate C promotion commit:
  - `efa97c5 Add ADP v2.3.1 Gate C artifacts and execution packet standard`
- Corrective action:
  - `CA-231-C-01 Final semantic traceability correction`
- Runtime authorization: CONDITIONAL ON CORRECTION PACKET FULL PASS
- Knowledge creation: AUTHORIZED ONLY INSIDE `V231-C-RUNTIME-01` AFTER ALL CORRECTED ENTRY CONDITIONS PASS
- Prompt execution: AUTHORIZED ONLY INSIDE `V231-C-RUNTIME-01`
- Optional model comparison: NOT AUTHORIZED
- ADP v2.4: BLOCKED
- Approved original operator artifact:
  - `ADP-v2.3.1-Gate-C-Self-Contained-Installer-v2.sh`
- Original installer SHA-256:
  - `4033e7fe81b82adb5a8c1a1a261632749fdf20fb641c4bf3c4d8b0fda7c75e01`
- Original embedded package SHA-256:
  - `6e1f0a43dd2edc76d8a1bfba2fe12a1766f3c6359c89b7f58dc3a452490dab5a`

## 2. Approved Identifiers

- Collection: `ADP-v2.3.1-minimal-direct-retrieval`
- Source file: `adp231_minimal_direct_retrieval.md`
- Source SHA-256: `ea0288d0d8666438e8cf9ae7dd54e6da8aaa0818f42d15f29bdf7467acf77afc`
- Model: `llama3.2:3b`
- Direct-retrieval test: `V231-R01`
- Displayed-source test: `V231-S01`
- Frozen prompt: `V231-R01-P1-v2`
- Frozen prompt SHA-256: `0c8ea2c72e6b6e3a002261e95308a3a2722a675d730cc2bd3c14eebe964befce`
- Required predecessor Timeshift snapshot:
  - Identifier: `2026-07-20_11-32-48`
  - Stored description: `ADP-v2.3-reg-hardening-t01-failure-closeout`

## 3. Governing Process Controls

- `ADP-Controlled-Execution-Packet-Standard.md`
- `ADP-Final-Delivery-Validation-Standard.md`
- `skills/adp-controlled-execution-packets/SKILL.md`
- `ADP-v2.3.1-Gate-C-Post-Promotion-Audit-Correction-Record.md`

Technical validation and semantic traceability must both pass. Superseded delivery references are not current instructions. Runtime authorization requires explicit Timeshift confirmation.

## 4. Artifact Validation

| Artifact | SHA-256 | Lines | Bytes | ASCII | No tabs | No trailing whitespace |
|---|---|---:|---:|---|---|---|
| `ADP-Controlled-Execution-Packet-Standard.md` | `bb90ec6f8020b77b4fdb67de8b0312e888224bc75a2ec8e2827002229774ab54` | 216 | 8585 | PASS | PASS | PASS |
| `ADP-Final-Delivery-Validation-Standard.md` | `b409040c9caaf5ea5cbfe671067f862b45c4d1213ec347626b0cc1ac76d63645` | 150 | 6147 | PASS | PASS | PASS |
| `skills/adp-controlled-execution-packets/SKILL.md` | `e60e37dee429a2171f2b6be04d9b5314cf8f145e1c484b534535970b42082ac0` | 78 | 4123 | PASS | PASS | PASS |
| `ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md` | `8f6d68908b68a4c14a0aef94cc78e83abb12f5aa5081c98f8e8d0e860d5402d8` | 103 | 4132 | PASS | PASS | PASS |
| `ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md` | `02df4a9348dc9d9e8e3ed84db007c7a59149599eb130e335e3f43aa22bf30c4a` | 122 | 4069 | PASS | PASS | PASS |
| `ADP-v2.3.1-Gate-C-New-Chat-Startup-v2.md` | `c03137ddcf0f68a75298b22244f09b5d0579be6e1445a56a0fc741c4de455586` | 48 | 1721 | PASS | PASS | PASS |
| `ADP-v2.3.1-Gate-C-Execution-Model-Addendum.md` | `b894ca7ba225a66fda55a0d050ec373fe912e5a3827f34a05ddebe227a8c3ed1` | 41 | 1695 | PASS | PASS | PASS |
| `ADP-v2.3.1-Synthetic-Diagnostic-Data-Design.md` | `d9f941f670f6623993cc41a7ec61d410af1f1f8ebb9d66f8f4ed5964e04f4063` | 159 | 5721 | PASS | PASS | PASS |
| `adp231_minimal_direct_retrieval.md` | `ea0288d0d8666438e8cf9ae7dd54e6da8aaa0818f42d15f29bdf7467acf77afc` | 11 | 474 | PASS | PASS | PASS |
| `ADP-v2.3.1-Diagnostic-Prompt-Library.md` | `8e4744a2a756c67451641af836caa79e8c8c11bcbe13a84b14c894a9b2605cfb` | 111 | 3948 | PASS | PASS | PASS |
| `ADP-v2.3.1-Diagnostic-Test-Record-Template.md` | `bb64cbd8a4404f41aea8d536549ff318e7eaba07816d296d8277c96785ccc52f` | 218 | 6155 | PASS | PASS | PASS |
| `ADP-v2.3.1-Knowledge-Attachment-Evidence-Procedure.md` | `0c74f375bf892c709307a55b127f7fb0aaf1f3f7a27dfdd89a7c177a31a01f47` | 204 | 6796 | PASS | PASS | PASS |
| `ADP-v2.3.1-Gate-C-Artifact-Review-and-Approval-Record.md` | `6b5b2605a61ba368a0363d3db1d35774d6e3e09a660fbab80d316d379adb8a2f` | 209 | 11944 | PASS | PASS | PASS |
| `ADP-v2.3.1-Gate-C-Post-Promotion-Audit-Correction-Record.md` | `9541b7e1542b480333d1be34285bb0e4efae8f441c707660afb7d66cc3f32c2e` | 125 | 4423 | PASS | PASS | PASS |
| `scripts/adp231_gate_c_promote.sh` | `7bbba5182beae5df4b2d49e184c6f6f8b0f4bb273243eadaf7653547693e9808` | 168 | 8419 | PASS | PASS | PASS |
| `scripts/adp231_gate_c_post_promotion_correct.sh` | `b1f8995ea2cdedd8b2d08b062de5f2ac6d446c6f829c71b49b3e17e24f6db606` | 164 | 9466 | PASS | PASS | PASS |

## 5. Canonical Paths

- `ADP-Controlled-Execution-Packet-Standard.md` -> `docs/ADP-Controlled-Execution-Packet-Standard.md`
- `ADP-Final-Delivery-Validation-Standard.md` -> `docs/ADP-Final-Delivery-Validation-Standard.md`
- `skills/adp-controlled-execution-packets/SKILL.md` -> `skills/adp-controlled-execution-packets/SKILL.md`
- `ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md` -> `docs/ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md`
- `ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md` -> `docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md`
- `ADP-v2.3.1-Gate-C-New-Chat-Startup-v2.md` -> `docs/ADP-v2.3.1-Gate-C-New-Chat-Startup-v2.md`
- `ADP-v2.3.1-Gate-C-Execution-Model-Addendum.md` -> `docs/ADP-v2.3.1-Gate-C-Execution-Model-Addendum.md`
- `ADP-v2.3.1-Synthetic-Diagnostic-Data-Design.md` -> `docs/ADP-v2.3.1-Synthetic-Diagnostic-Data-Design.md`
- `adp231_minimal_direct_retrieval.md` -> `test-data/rag/v2.3.1/adp231_minimal_direct_retrieval.md`
- `ADP-v2.3.1-Diagnostic-Prompt-Library.md` -> `docs/ADP-v2.3.1-Diagnostic-Prompt-Library.md`
- `ADP-v2.3.1-Diagnostic-Test-Record-Template.md` -> `docs/ADP-v2.3.1-Diagnostic-Test-Record-Template.md`
- `ADP-v2.3.1-Knowledge-Attachment-Evidence-Procedure.md` -> `docs/ADP-v2.3.1-Knowledge-Attachment-Evidence-Procedure.md`
- `ADP-v2.3.1-Gate-C-Artifact-Review-and-Approval-Record.md` -> `docs/ADP-v2.3.1-Gate-C-Artifact-Review-and-Approval-Record.md`
- `ADP-v2.3.1-Gate-C-Post-Promotion-Audit-Correction-Record.md` -> `docs/ADP-v2.3.1-Gate-C-Post-Promotion-Audit-Correction-Record.md`
- `scripts/adp231_gate_c_promote.sh` -> `scripts/adp231_gate_c_promote.sh`
- `scripts/adp231_gate_c_post_promotion_correct.sh` -> `scripts/adp231_gate_c_post_promotion_correct.sh`

## 6. Correction Execution Authorization

Execute the single self-contained post-promotion correction installer once.

The correction packet shall:

- Validate the repository at promotion commit `efa97c5`.
- Validate prior canonical artifact hashes.
- Confirm the required Timeshift snapshot before repository mutation.
- Validate and copy the corrected artifact set.
- Perform static and semantic traceability checks.
- Commit, push, synchronize, and confirm a clean working tree.
- Emit one consolidated transcript.

Proceed directly to `V231-C-RUNTIME-01` only when the transcript contains:

- `CORRECTION_STATUS=PASS`
- `SEMANTIC_TRACEABILITY_STATUS=PASS`
- `TIMESHIFT_BASELINE_STATUS=PASS`
- `POST_CORRECTION_SYNCHRONIZATION_STATUS=PASS`
- `RUNTIME_ENTRY_STATUS=PASS`
- `NEXT_PACKET=V231-C-RUNTIME-01`

A FAIL, INCONCLUSIVE condition, missing evidence, or state change stops automatic continuation.

## 7. Manifest Integrity

This manifest does not list its own checksum because that would be circular.

The correction payload checksum file validates this manifest and every file delivered by the correction installer.


## 8. Runtime Procedure Hardening Amendment

The first attempted runtime workflow is `VOIDED_NOT_COUNTED`.

Current runtime artifacts are:

- `docs/ADP-Test-Execution-Consistency-and-Evidence-Lifecycle-Standard.md`
- `docs/ADP-Process-Quality-Gate-Checklist.md`
- `docs/ADP-v2.3.1-Gate-C-Runtime-Procedure-Reset-and-Supersession-Record.md`
- `docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md`
- `docs/ADP-v2.3.1-Gate-C-Fresh-Runtime-Operator-Guide.md`
- `scripts/adp231_gate_c_fresh_runtime.sh`
- `scripts/adp_process_quality_gate.sh`

Earlier Gate C runtime operator scripts, toolkit directories, and guides are superseded.

A counted run may begin only after the process-quality gate and fresh reset pass.
