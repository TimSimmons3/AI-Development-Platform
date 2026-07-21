# ADP v2.3.1 Gate C Promotion and Synchronization Execution Packet

## 1. Packet Control

- Packet ID: `V231-C-PROMOTE-01`
- Status: Approved for operator execution after package checksum validation
- Authorization: Repository promotion, commit, push, synchronization, and read-only pre-runtime validation
- Runtime mutation: NOT AUTHORIZED
- Knowledge creation or upload: NOT AUTHORIZED within this packet
- Governing standard: `docs/ADP-Controlled-Execution-Packet-Standard.md`

## 2. Objective

Complete all Gate C repository-promotion and read-only pre-runtime controls in one operator session and return one transcript.

## 3. Inputs

- Package ZIP: `ADP-v2.3.1-Gate-C-Integrated-Execution-Package.zip`
- ZIP checksum file: `ADP-v2.3.1-Gate-C-Integrated-Execution-Package.zip.sha256`
- Repository: `~/Labs/AI-Development-Platform`
- Expected starting commit: `253e9dd`
- Branch: `main`

## 4. Execution Method

1. Validate the ZIP checksum.
2. Extract the ZIP outside the repository.
3. Run `scripts/adp231_gate_c_promote.sh` from the extracted package.
4. Enter a sudo password only if requested for the read-only UFW status check.
5. Do not pause for external approval between successful substeps.

The script performs:

- Git baseline and controlling-checksum validation
- Package checksum and static validation
- Controlled canonical-path copy
- Git diff and staged validation
- Commit and push
- `HEAD`, `main`, and `origin/main` synchronization confirmation
- Working-tree cleanliness confirmation
- Read-only Open WebUI, Ollama, listener, model, and UFW checks
- One consolidated transcript

## 5. Automatic Continuation

The script continues automatically when each check passes. A successful baseline check authorizes package validation; successful package validation authorizes controlled copy; successful diff validation authorizes commit; successful commit authorizes push; successful synchronization authorizes read-only pre-runtime checks.

No separate user or assistant approval is required between those steps.

## 6. Stop Conditions

The packet stops automatically when:

- Branch, commit, or synchronization differs from the expected baseline.
- The working tree is not clean before promotion.
- A controlling checksum or package checksum fails.
- ASCII, tab, trailing-whitespace, or Git diff validation fails.
- A canonical destination conflicts with an unexpected file state.
- Commit or push fails.
- Post-push synchronization or cleanliness fails.
- Open WebUI image, health, or loopback binding differs.
- Ollama version, service state, listener setting, or approved model set differs.
- UFW is not active.

A stop requires one returned transcript; do not continue manually around the failed control.

## 7. Success Criteria

The packet passes only when the transcript ends with:

- `PROMOTION_STATUS=PASS`
- `SYNCHRONIZATION_STATUS=PASS`
- `READ_ONLY_PRE_RUNTIME_STATUS=PASS`
- `NEXT_PACKET=V231-C-RUNTIME-01`

## 8. Return Bundle

Return only one item after the packet:

- The complete transcript path and contents, or the transcript file itself.

No intermediate output is required when the packet succeeds.
