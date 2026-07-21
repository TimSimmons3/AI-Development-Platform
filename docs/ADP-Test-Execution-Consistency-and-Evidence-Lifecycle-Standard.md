# ADP Test Execution Consistency and Evidence Lifecycle Standard

## 1. Document Control

- Project: AI Development Platform
- Standard type: Cross-release execution-integrity control
- Status: Approved for controlled repository promotion
- Effective release: ADP v2.3.1 and later
- Canonical path:
  - `docs/ADP-Test-Execution-Consistency-and-Evidence-Lifecycle-Standard.md`
- Applies to:
  - Diagnostic tests
  - Qualification tests
  - Security and recovery validation
  - Manual and automated evidence collection
  - Operator scripts and guides
  - External-system interactions
  - Release gates and closeout

## 2. Purpose

Prevent invalid, inconsistent, patched, duplicated, or ambiguously evidenced test execution.

A technically correct test can still be invalid when the procedure, script, evidence schema, filenames, scoring rules, or operator instructions change after execution begins. This standard establishes the mandatory procedure-freeze, void, reset, cleanup, evidence, and supersession controls required before a run may count.

## 3. Procedure-Freeze Gate

No counted run may begin until one authoritative execution package is frozen.

The frozen package shall include:

1. Approved plan and gate record.
2. One current execution packet.
3. One current operator script or script set.
4. One current operator guide.
5. Exact prompt, source, model, collection, and test identifiers.
6. Evidence schema and unique filenames.
7. Pass, fail, and inconclusive criteria.
8. Stop conditions.
9. Reset and cleanup procedure.
10. Checksums and semantic traceability results.
11. Positive and negative end-to-end test evidence.
12. Current-artifact inventory and supersession statement.

The freeze gate passes only when the exact files delivered to the operator match the exact files reviewed and validated.

## 4. No Mid-Run Patching

Do not patch, reinterpret, rename, resume, or retrofit a counted run after a material procedure change.

Material changes include:

- Script logic
- Commands
- Operator steps
- Evidence requirements
- Evidence filenames
- Prompt wording
- Source content
- Collection state
- Model selection
- Scoring criteria
- Pass, fail, or inconclusive rules
- Timestamp or log boundaries
- Required screenshots
- Source-evidence handling
- Runtime or security prerequisites

When a material change occurs after a run starts:

1. Stop immediately.
2. Mark the affected run `VOIDED_NOT_COUNTED`.
3. Preserve the exact partial evidence.
4. Record the reason and change that invalidated the run.
5. Move the evidence outside the active workspace.
6. Reset external-system state as required.
7. Freeze and validate the corrected procedure.
8. Start again with fresh independent evidence.

## 5. Void Classification

A void is neither PASS, FAIL, nor INCONCLUSIVE.

Use:

- `VOIDED_NOT_COUNTED`

A void means the evidence cannot answer the approved diagnostic question because the governing procedure changed or was not stable.

The void record shall contain:

- Test and run identifiers
- Start and stop timestamps when known
- Procedure version used
- Defect or change requiring the void
- Files and external state affected
- Counted-run total, which must exclude the void
- Archive location
- Reset completion evidence

## 6. Evidence Namespace and Filename Control

Every evidence item shall have one purpose and one unique filename.

Do not:

- Reuse a filename for pre-run and post-run evidence.
- Require the operator to overwrite evidence.
- Use generic names that can refer to different states.
- Require duplicate evidence without a documented independence reason.
- Create expected-result text files unless the result was actually observed.

Use ordered, purpose-specific names such as:

- `01-membership-before-run.png`
- `02-fresh-empty-chat.png`
- `03-collection-attached-before-prompt.png`
- `04-complete-response.png`
- `05-displayed-source-panel.png`

The script, guide, template, and checklist shall use the same names.

## 7. Active Workspace Hygiene

Voided, superseded, duplicate, and prior-version artifacts shall not remain in the active operator workspace.

The reset procedure shall:

1. Archive the old evidence workspace.
2. Archive loose screenshots and duplicate upload files.
3. Archive superseded scripts, toolkits, checksum files, and guides.
4. Create a cleanup manifest with source, destination, checksum, and size.
5. Verify stale items are absent from active locations.
6. Create a new evidence workspace.
7. Preserve auditability without permitting reuse.

Do not permanently delete evidence when archival is practical and lawful.

## 8. External-System Reset

When a test uses an external interface or stateful application, the reset shall address that state explicitly.

Examples include:

- Chats
- Knowledge collections
- Uploaded files
- Cached sessions
- Temporary projects
- Test records
- Automation state
- Queues or jobs

For Open WebUI Gate C, a fresh reset requires:

- Deletion of voided-attempt chats.
- Deletion and recreation of the diagnostic collection.
- Fresh upload of the approved source.
- Fresh setup screenshots.
- Fresh chats for every counted run.

## 9. Authoritative-Artifact Rule

At every execution point, there shall be exactly one current:

- Procedure
- Script
- Guide
- Evidence schema
- Filename map
- Prompt version
- Source version
- Test template

Superseded artifacts shall be:

- Clearly marked historical, or
- Archived outside active use.

Current instructions shall not reference superseded artifact names.

## 10. Operator Usability Gate

Before delivery, test whether a reasonable operator can determine:

1. What to run now.
2. What to do in the external interface.
3. What evidence to capture.
4. Where to save it.
5. What filename to use.
6. What output to expect.
7. When to stop.
8. What not to reuse.
9. What command comes next.

Instructions shall use plain English and avoid conflicting or implicit steps.

A guide fails the usability gate when two reasonable interpretations could produce different evidence or execution state.

## 11. Verification and Validation Requirements

The final package shall pass:

- ASCII and shell syntax validation
- Checksum validation
- Clean-room installation or execution
- Positive workflow simulation
- Negative missing-file test
- Negative truncation or stop-condition test
- Reset and archive test
- Duplicate and superseded-artifact cleanup test
- Evidence filename collision test
- Semantic traceability review
- Operator usability review
- Current-artifact inventory review

Source-level validation alone is insufficient.

## 12. Change-Control Matrix

| Change timing | Change type | Required action |
|---|---|---|
| Before procedure freeze | Any | Revise, revalidate, and freeze |
| After freeze, before run start | Non-material typo with no execution meaning | Correct, checksum, and re-freeze |
| After freeze, before run start | Material | Correct, revalidate, and re-freeze |
| After run start | Any material change | Void run, reset, and restart |
| After run completion, before classification | Material scoring or evidence change | Void run and restart |
| After classification | Discovery of evidence-integrity defect | Reopen gate, void affected evidence, and remediate |

## 13. Handoff and Future-Task Requirement

Every future handoff, release plan, runtime packet, validation package, and operator guide shall:

- Reference this standard.
- Identify the frozen procedure version.
- List current and superseded artifacts.
- Include a reset path.
- Include a cleanup path.
- State whether any prior evidence may be reused.
- Default to no reuse after a material change.
- Include one authoritative next command.
- Include expected PASS fields.

## 14. Enforcement

A test shall not be represented as valid, complete, repeatable, or audit-ready unless this standard passes.

Efficiency does not justify continuing a patched run. Safety does not justify unnecessary transitions. The required outcome is a stable procedure, fresh evidence, clear operator action, and reproducible classification.
