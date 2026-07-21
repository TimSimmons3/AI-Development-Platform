# ADP Controlled Execution Packets Skill

## Activation

Use this skill for AI Development Platform work and other controlled projects that involve multiple dependent validation, file, Git, runtime, evidence, or closeout steps.

## Governing Rule

Design the work as the fewest practical consolidated execution packets. Do not split safe dependent steps into separate user transitions.

## Required Behavior

1. Read the current handoff, approved plan, gate record, and `docs/ADP-Controlled-Execution-Packet-Standard.md`.
2. Identify the current authorization boundary.
3. Group all safe dependent actions inside that boundary into one packet.
4. Define prerequisites, continuation conditions, stop conditions, evidence, and success criteria.
5. Permit automatic continuation after successful substeps.
6. Require a user transition only for human judgment, an external-system result, a material approval, a boundary change, an irreversible action, or a stop condition.
7. Do not repeat a validation unless relevant state changed or independent per-run evidence is required.
8. Return or request one consolidated evidence bundle per packet.
9. Preserve project terminal controls: flat ASCII commands, staged validation, no unnecessary editors, and no unreviewed runtime or security changes.

## Default Packet Sequence

1. Planning and approval
2. Promotion, synchronization, and read-only pre-runtime validation
3. Runtime evidence execution
4. Closeout and recoverability

Combine adjacent packets when the plan permits and the evidence remains unambiguous.

## Disallowed Patterns

- Check one item, return to chat, then check the next unchanged item.
- Ask for confirmation between copy, stage, commit, push, and synchronization when all are already authorized and conditionally controlled.
- Add a gate that has no evidence basis, risk basis, or approved-plan basis.
- Repeat remote, firewall, service, or checksum tests when no relevant state changed and the prior evidence remains current.
- Require the user to restate information contained in the handoff or current packet.

## Output Standard

For each packet provide:

- Packet objective
- Exact scope
- Preconditions
- Ordered actions or validated script
- Automatic continuation conditions
- Stop conditions
- Evidence retained
- Final status fields
- One return-bundle instruction

## Final Delivery Enforcement

Before presenting any operator-executed artifact:

1. Read `docs/ADP-Final-Delivery-Validation-Standard.md` when present.
2. Validate the exact final downloadable bytes, not an earlier build or unpackaged source.
3. Prefer one self-contained installer or launcher with an embedded verified payload.
4. Eliminate separate ZIP, checksum, and launcher coordination unless technically necessary.
5. Test the exact documented command from a clean expected download directory.
6. Run ASCII, `bash -n`, payload checksum, extraction, executable-path, and clean-room self-test controls.
7. Preserve a final-delivery validation report and SHA-256.
8. Do not state that execution is ready until this gate passes.
9. On a delivery-path defect, supersede the failed artifact design rather than asking the operator to retry the same pattern.

## Semantic Traceability Enforcement

Before delivery or runtime authorization:

1. Build a requirement-coverage map from the approved plan, current gate record, handoff, amendments, and recoverability requirements to the packet steps and status fields.
2. Verify that each mandatory prerequisite is tested, evidenced, or explicitly retained as a hold point.
3. Search all current instructions for superseded filenames, package pairings, execution methods, baselines, and authorization language.
4. Reconcile the manifest, checksums, canonical paths, scripts, and operator command.
5. Distinguish historical records from current executable instructions.
6. Do not declare a full pass when static and delivery tests pass but semantic traceability remains incomplete.
7. When a post-delivery audit finds multiple linked inconsistencies, correct them in one consolidated corrective packet and return one evidence bundle.
