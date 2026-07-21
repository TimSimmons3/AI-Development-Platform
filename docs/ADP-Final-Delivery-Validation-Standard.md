# ADP Final Delivery Validation Standard

## 1. Document Control

- Project: AI Development Platform
- Standard type: Cross-release final-delivery control
- Status: Approved for controlled repository promotion
- Planned canonical path:
  - `docs/ADP-Final-Delivery-Validation-Standard.md`
- Effective release: ADP v2.3.1 and later
- Applies to: Every script, archive, checksum file, command packet, handoff package, and executable artifact delivered for operator use

## 2. Purpose

Prevent delivery-path failures that occur after source-level validation but before or during operator execution.

Source validation is necessary but is not sufficient. Readiness may be claimed only after the exact final artifact delivered to the operator passes the controls in this standard.

## 3. Mandatory Final-Artifact Rule

Validation shall be performed against the exact final downloadable artifact, exact final filename, exact companion-file requirements, and exact operator command.

Do not claim that an artifact is ready based only on:

- Validation of an earlier package version
- Validation of unpackaged source files
- Validation of a script before its final embedding or packaging
- A checksum that does not correspond to the final delivered byte stream
- A command that was not tested through the expected operator path

## 4. Single-Artifact Default

Use one self-contained executable artifact whenever practical.

A self-contained artifact shall:

- Carry or generate every required payload file
- Verify its embedded payload before use
- Avoid dependency on separately downloaded archives or checksum files
- Avoid operator-entered filenames, hashes, and extraction paths
- Handle the expected download directory directly
- Produce clear PASS or FAIL fields
- Stop before repository or runtime mutation when delivery validation fails

Multiple coordinated downloads require a documented necessity and an end-to-end test proving that the complete set is present and correctly paired.

## 5. Required Delivery-Path Tests

Before delivery, validate:

1. Final artifact SHA-256
2. ASCII-only content for operator-executed shell artifacts
3. Shell syntax with `bash -n`
4. Exact download filename and path assumptions
5. Browser-added suffix risk or elimination of filename dependence
6. Embedded or companion payload integrity
7. Extraction into a clean temporary directory
8. Expected executable path after extraction
9. Required command availability
10. No dependency on chat-rendered non-ASCII spaces or wrapped paths
11. Failure behavior when a prerequisite is missing
12. Success behavior through a clean-room delivery self-test
13. Package-to-source byte comparison after extraction
14. Validation-report accuracy against the final artifact

## 6. Clean-Room Delivery Self-Test

The final artifact shall support or be subjected to a clean-room test from the operator's expected starting directory.

The test shall use:

- A new temporary home or staging directory
- No preexisting extracted package
- No separately supplied payload unless explicitly required
- The exact final artifact bytes
- The exact documented invocation pattern

The test shall prove at minimum:

- Artifact discovery is not required or is deterministic
- Payload extraction succeeds
- Payload checksum verification succeeds
- Required script exists at the expected path
- Required script is ASCII-only and syntactically valid
- No repository or runtime mutation occurs in self-test mode

## 7. Mutation Boundary

Delivery validation must complete before repository, Git, runtime, firewall, model, Knowledge, or evidence state is changed.

The executable shall stop with an explicit delivery failure when:

- The embedded payload checksum differs
- Extraction fails
- The expected script is absent
- Shell syntax fails
- Non-ASCII content is detected in an operator-executed script
- An undeclared companion artifact is required

## 8. Evidence Required

Retain:

- Final artifact filename
- Final artifact byte count
- Final artifact SHA-256
- Embedded payload SHA-256 when applicable
- `bash -n` result
- ASCII scan result
- Clean-room self-test transcript
- Extracted payload comparison result
- Validation date
- Residual dependencies and risks

## 9. Release Gate

A delivery is not approved when any required delivery-path test is unexecuted, failed, or based on a different artifact version.

The final response shall distinguish:

- Source validation
- Package validation
- Final-delivery validation
- Target-environment execution, which remains operator-dependent

## 10. Defect Response

After a delivery-path defect:

1. Stop reusing the failed transaction design.
2. Identify whether the failure arose from packaging, pairing, filename handling, command transport, extraction, or target prerequisites.
3. Correct the standard, skill, package, and operator artifact together.
4. Re-run the complete final-delivery validation.
5. Supersede the failed artifacts explicitly.
6. Do not ask the operator to repeat the same uncorrected pattern.

## 11. Semantic Delivery Consistency

The final-delivery gate shall include a semantic comparison of the exact final artifact and its operator instructions against the approved plan, current gate records, amendments, canonical manifest, and executable packet.

The comparison shall confirm:

- Every current prerequisite is enforced before mutation or runtime authorization.
- Superseded download methods, filenames, checksum pairings, and execution paths are removed from current instructions or clearly labeled as historical.
- The final artifact, embedded payload, extracted files, canonical promotion paths, and documented workflow agree.
- Runtime-entry status fields are not emitted unless every required security, recoverability, synchronization, and evidence prerequisite was actually checked.
- The current operator command was tested and matches the workflow documented in the canonical packet.
- Any post-delivery correction updates the standard, skill, packet, script, manifest, and audit record together when they are affected.

This review is required in addition to byte-level and clean-room validation.


## 12. Procedure and Evidence Consistency Gate

Final-delivery validation shall compare the exact operator artifact against:

- The frozen procedure
- The evidence schema
- The filename map
- The reset and cleanup procedure
- The current-artifact inventory
- The supersession record

The delivered script and guide shall agree on every command, filename, path, question, status field, and stop condition.

## 13. Operator Usability Test

Before delivery, perform a task-based review in which the operator path is evaluated from start to finish.

The review shall identify:

- Duplicate steps
- Reused filenames
- Missing files
- Unclear application context
- Hidden prerequisites
- Contradictory instructions
- Expected-result fabrication risk
- Ambiguous next actions
- Mid-run change risk

A delivery is not approved when the operator must infer what a screenshot or file should contain.

## 14. In-Progress Defect Rule

If a delivery or procedure defect is discovered after a counted run begins:

1. Do not patch the run.
2. Void the affected run.
3. Archive its evidence.
4. Correct all affected standards, skills, scripts, guides, and templates together.
5. Re-run final-delivery and semantic validation.
6. Reset the active workspace and external-system state.
7. Restart under the new frozen version.
