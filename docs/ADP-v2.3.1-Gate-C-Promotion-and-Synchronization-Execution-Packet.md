# ADP v2.3.1 Gate C Promotion and Synchronization Execution Packet

## 1. Packet Control

- Packet ID: `V231-C-PROMOTE-01`
- Status: Executed successfully through the approved self-contained installer
- Promotion commit: `efa97c5 Add ADP v2.3.1 Gate C artifacts and execution packet standard`
- Authorization: Repository promotion, commit, push, synchronization, and read-only pre-runtime validation
- Runtime mutation: NOT AUTHORIZED
- Knowledge creation or upload: NOT AUTHORIZED within this packet
- Governing standards:
  - `docs/ADP-Controlled-Execution-Packet-Standard.md`
  - `docs/ADP-Final-Delivery-Validation-Standard.md`

## 2. Objective

Complete all Gate C repository-promotion and read-only pre-runtime controls in one operator session and return one transcript.

## 3. Approved Operator Delivery

The approved operator artifact was:

- `ADP-v2.3.1-Gate-C-Self-Contained-Installer-v2.sh`
- Installer SHA-256:
  - `4033e7fe81b82adb5a8c1a1a261632749fdf20fb641c4bf3c4d8b0fda7c75e01`
- Embedded package SHA-256:
  - `6e1f0a43dd2edc76d8a1bfba2fe12a1766f3c6359c89b7f58dc3a452490dab5a`
- Repository:
  - `~/Labs/AI-Development-Platform`
- Expected starting commit:
  - `253e9dd`
- Branch:
  - `main`

The earlier external ZIP-plus-checksum and separate-launcher workflow is superseded and shall not be used.

## 4. Execution Method

Execute the self-contained installer once from the operator's `Downloads` directory.

The installer:

1. Verifies its embedded payload checksum.
2. Extracts the payload into a clean temporary directory outside the repository.
3. Validates the package file set, internal checksums, ASCII content, and Bash syntax.
4. Invokes `scripts/adp231_gate_c_promote.sh`.
5. Stops before repository mutation if final-delivery validation fails.

The promotion script performs:

- Git baseline and controlling-checksum validation
- Package checksum and static validation
- Controlled canonical-path copy
- Git staged-diff validation
- Commit and push
- `HEAD`, `main`, and `origin/main` synchronization confirmation
- Working-tree cleanliness confirmation
- Read-only Open WebUI, Ollama, listener, model, and UFW checks
- Final predecessor Timeshift snapshot confirmation
- One consolidated transcript

## 5. Automatic Continuation

The script continues automatically when each check passes. No separate user or assistant approval is required between safe dependent substeps.

Runtime work may begin only after every required promotion, synchronization, read-only runtime, and Timeshift status field is present and no relevant state changed.

## 6. Stop Conditions

The packet stops automatically when:

- Branch, commit, or synchronization differs from the expected baseline.
- The working tree is not clean before promotion.
- A controlling checksum or package checksum fails.
- ASCII, tab, trailing-whitespace, Bash syntax, or Git staged-diff validation fails.
- A canonical destination conflicts with an unexpected file state.
- Commit or push fails.
- Post-push synchronization or cleanliness fails.
- Open WebUI image, health, or loopback binding differs.
- Ollama version, service state, listener setting, or approved model set differs.
- UFW is not active.
- Timeshift snapshot `2026-07-20_11-32-48` is absent.
- The stored snapshot description does not contain `ADP-v2.3-reg-hardening-t01-failure-closeout`.

A stop requires one returned transcript. Do not continue manually around a failed control.

## 7. Success Criteria

A fully current execution of this packet passes only when the transcript contains:

- `PROMOTION_STATUS=PASS`
- `SYNCHRONIZATION_STATUS=PASS`
- `READ_ONLY_PRE_RUNTIME_STATUS=PASS`
- `TIMESHIFT_BASELINE_STATUS=PASS`
- `NEXT_PACKET=V231-C-RUNTIME-01`

The original promotion transcript passed promotion, synchronization, and read-only runtime checks at commit `efa97c5`. The post-promotion correction packet supplies the missing Timeshift confirmation and semantic consistency correction before runtime authorization.

## 8. Return Bundle

Return one consolidated transcript after the packet completes or stops.

No intermediate output is required when the packet succeeds.
