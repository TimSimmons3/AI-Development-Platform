# ADP v2.3.1 Gate C Approved Artifact Manifest

## 1. Package Control

- Package status: APPROVED AS REVISED WITH CONSOLIDATED EXECUTION AND FINAL-DELIVERY CONTROL
- Repository baseline represented: `253e9dd`
- Promotion packet: `V231-C-PROMOTE-01`
- Runtime packet: `V231-C-RUNTIME-01`
- Operator delivery: One self-contained installer with an embedded verified payload
- Runtime authorization: CONDITIONAL ON PROMOTION PACKET PASS
- Knowledge creation: AUTHORIZED ONLY INSIDE `V231-C-RUNTIME-01` AFTER ALL ENTRY CONDITIONS PASS
- Prompt execution: AUTHORIZED ONLY INSIDE `V231-C-RUNTIME-01`
- Optional model comparison: NOT AUTHORIZED
- ADP v2.4: BLOCKED

## 2. Approved Identifiers

- Collection: `ADP-v2.3.1-minimal-direct-retrieval`
- Source file: `adp231_minimal_direct_retrieval.md`
- Source SHA-256: `ea0288d0d8666438e8cf9ae7dd54e6da8aaa0818f42d15f29bdf7467acf77afc`
- Model: `llama3.2:3b`
- Direct-retrieval test: `V231-R01`
- Displayed-source test: `V231-S01`
- Frozen prompt: `V231-R01-P1-v2`
- Frozen prompt SHA-256: `0c8ea2c72e6b6e3a002261e95308a3a2722a675d730cc2bd3c14eebe964befce`

## 3. Governing Process Controls

- `ADP-Controlled-Execution-Packet-Standard.md`
- `ADP-Final-Delivery-Validation-Standard.md`
- `skills/adp-controlled-execution-packets/SKILL.md`

Safe dependent substeps continue automatically within a packet. Final delivery must be validated against the exact final artifact. The previous multiple-file operator transaction is superseded.

## 4. Artifact Validation

| Artifact | SHA-256 | Lines | Bytes | ASCII | No tabs | No trailing whitespace |
|---|---|---:|---:|---|---|---|
| `ADP-Controlled-Execution-Packet-Standard.md` | `714aafc834d2d8afb69348dbd1996443d78f06d429c1c41b8cb57bc4bf74a4a4` | 198 | 7283 | PASS | PASS | PASS |
| `ADP-Final-Delivery-Validation-Standard.md` | `b2bd130cd0cca20f76a5eab55d1e471dfbe174971e7f7449c9baa96c0edecddf` | 135 | 5027 | PASS | PASS | PASS |
| `skills/adp-controlled-execution-packets/SKILL.md` | `660a19bb0776fb99a17bc9a7e023fa321dfc45b081b98ace23cd05c9c0342fd1` | 66 | 3204 | PASS | PASS | PASS |
| `ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md` | `22328965a59d113684e412f8506b907a891c41929b1ed906503002ea478da446` | 82 | 3139 | PASS | PASS | PASS |
| `ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md` | `b42a0c3d71d65ba412d7a750b2e55c9fb184c47b45c9c7063f52a471d3080daa` | 108 | 3614 | PASS | PASS | PASS |
| `ADP-v2.3.1-Gate-C-New-Chat-Startup-v2.md` | `7c42b94720aecfdb7779763fb3abd8a19ae260e33b52bff10cc7197aee7300b5` | 40 | 1345 | PASS | PASS | PASS |
| `ADP-v2.3.1-Gate-C-Execution-Model-Addendum.md` | `b894ca7ba225a66fda55a0d050ec373fe912e5a3827f34a05ddebe227a8c3ed1` | 41 | 1695 | PASS | PASS | PASS |
| `ADP-v2.3.1-Synthetic-Diagnostic-Data-Design.md` | `d9f941f670f6623993cc41a7ec61d410af1f1f8ebb9d66f8f4ed5964e04f4063` | 159 | 5721 | PASS | PASS | PASS |
| `adp231_minimal_direct_retrieval.md` | `ea0288d0d8666438e8cf9ae7dd54e6da8aaa0818f42d15f29bdf7467acf77afc` | 11 | 474 | PASS | PASS | PASS |
| `ADP-v2.3.1-Diagnostic-Prompt-Library.md` | `8e4744a2a756c67451641af836caa79e8c8c11bcbe13a84b14c894a9b2605cfb` | 111 | 3948 | PASS | PASS | PASS |
| `ADP-v2.3.1-Diagnostic-Test-Record-Template.md` | `bb64cbd8a4404f41aea8d536549ff318e7eaba07816d296d8277c96785ccc52f` | 218 | 6155 | PASS | PASS | PASS |
| `ADP-v2.3.1-Knowledge-Attachment-Evidence-Procedure.md` | `0c74f375bf892c709307a55b127f7fb0aaf1f3f7a27dfdd89a7c177a31a01f47` | 204 | 6796 | PASS | PASS | PASS |
| `ADP-v2.3.1-Gate-C-Artifact-Review-and-Approval-Record.md` | `df5cfc582d497464bf12e2d1320cb8396af466c2f791ef76ae9488d9e10cab29` | 169 | 9981 | PASS | PASS | PASS |
| `scripts/adp231_gate_c_promote.sh` | `23ebeb5e008b73281ee0b24ec98129b1e317e6f8d394e45e31309b5458318def` | 157 | 7923 | PASS | PASS | PASS |

## 5. Promotion Paths

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
- `scripts/adp231_gate_c_promote.sh` -> `scripts/adp231_gate_c_promote.sh`

## 6. Execution Authorization

Execute the self-contained installer once. It shall verify and extract its embedded payload before invoking `V231-C-PROMOTE-01`. When the promotion transcript contains all required PASS fields and no relevant state changed, proceed directly to `V231-C-RUNTIME-01` without intermediate assistant approval.

A FAIL or INCONCLUSIVE result, missing evidence, or boundary change stops automatic continuation.

## 7. Manifest Integrity

This manifest does not list its own checksum because that would be circular. The package checksum file validates this manifest with every promotable artifact.
