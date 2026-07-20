# ADP v2.3 RAG Manual Test Record Template

## Document Control

Project: AI Development Platform - ADP
Release: v2.3
Status: Approved template
Evidence type: Manual local RAG test record
Data sensitivity: Synthetic non-sensitive only

## Record Instructions

Create one completed copy of this template for each test run.

Do not overwrite a prior run.

Preserve:

- The exact prompt.
- The complete response.
- Displayed source evidence.
- The original failure.
- Any interface or execution anomaly.

Do not correct model output inside the evidence section.

## Test Identification

Test ID:

Prompt ID and version:

Run number:

Test area:

Operator:

Reviewer:

Date:

Local time and timezone:

Result: PASS / FAIL / BLOCKED

Primary failure mode:

Secondary failure modes:

## Baseline Evidence

Host:

Repository:

Branch:

HEAD:

origin/main:

Git working tree clean: YES / NO

Open WebUI image:

Open WebUI binding:

Open WebUI health:

Ollama version:

Selected model:

Installed model list reviewed: YES / NO

Unexpected runtime change observed: YES / NO

## Knowledge Evidence

Knowledge collection name:

Knowledge collection status:

Named permitted source file or files:

Expected file count:

Observed file count:

Fresh chat used: YES / NO

Prior conversation reused: YES / NO

Displayed source evidence present: YES / NO

Displayed source file or files:

Unexpected source displayed: YES / NO

## Exact Prompt

```text
Paste the exact submitted prompt here.
```

## Expected Response or Required Behavior

```text
Paste the exact expected response or describe the controlled expected behavior here.
```

## Full Actual Response

```text
Paste the full unedited model response here.
```

## Source-Evidence Record

Record the source indicator displayed by Open WebUI.

Source name:

Source type:

Source excerpt, when displayed:

Source order:

Source confidence or score, when displayed:

Screenshot reference, when used:

Notes:

## Structured Validation

Factually correct against named source: PASS / FAIL / NOT APPLICABLE

Named source boundary followed: PASS / FAIL / NOT APPLICABLE

Required output structure followed: PASS / FAIL / NOT APPLICABLE

Outside knowledge excluded: PASS / FAIL / NOT APPLICABLE

Required abstention followed: PASS / FAIL / NOT APPLICABLE

False premise rejected: PASS / FAIL / NOT APPLICABLE

Conflict identified: PASS / FAIL / NOT APPLICABLE

Controlling rule handled correctly: PASS / FAIL / NOT APPLICABLE

Source attribution correct: PASS / FAIL / NOT APPLICABLE

Displayed source evidence supports answer: PASS / FAIL / NOT APPLICABLE

Fresh-chat requirement followed: PASS / FAIL / NOT APPLICABLE

Prompt submitted without modification: PASS / FAIL

Evidence complete: PASS / FAIL

Security boundary preserved: PASS / FAIL

## Expected-to-Actual Comparison

Expected facts:

- None recorded.

Observed facts:

- None recorded.

Missing facts:

- None recorded.

Incorrect facts:

- None recorded.

Unsupported facts:

- None recorded.

Structural differences:

- None recorded.

## Failure Analysis

Primary failure mode code:

Primary failure description:

Contributing conditions:

Interface behavior:

Retrieval behavior:

Instruction-following behavior:

Evidence limitation:

Security impact:

Data-boundary impact:

## Prompt Revision Decision

Revision required: YES / NO

Current revision cycle: 0 / 1 / 2 / 3

One variable proposed for change:

Reason:

Prior evidence retained: YES / NO

Approval required before rerun: YES / NO

New prompt ID, when approved:

## Repeatability Section

Complete only for T08 or another approved repeatability test.

Underlying prompt ID:

Run 1 record reference:

Run 1 result:

Run 2 record reference:

Run 2 result:

Run 3 record reference:

Run 3 result:

Three of three passed: YES / NO

Material facts equivalent: YES / NO

Required structure equivalent: YES / NO

Outside knowledge absent in all runs: YES / NO

Repeatability result: PASS / FAIL / BLOCKED

## Removal Validation Section

Complete only for T09.

Knowledge collection before removal:

Before-removal run reference:

Before-removal timestamp:

Before-removal exact prompt hash or reference:

Before-removal response:

Before-removal displayed source evidence:

Removal action start timestamp:

Removal action completed timestamp:

Removal interface control used:

Collection absent from Knowledge list after removal: YES / NO

Files absent from collection after removal: YES / NO

Docker volume deleted or replaced: NO

Runtime restarted: YES / NO

Reason for runtime restart, if any:

Fresh post-removal chat used: YES / NO

After-removal run reference:

After-removal timestamp:

After-removal exact prompt hash or reference:

Exact prompt pair confirmed: YES / NO

After-removal response:

After-removal displayed source evidence:

Removed source evidence persisted: YES / NO

Removed answer content persisted: YES / NO

Removal result: PASS / FAIL / BLOCKED

## Stop-Condition Review

Real or sensitive data introduced: YES / NO

Unexplained Git change: YES / NO

Unexpected model, image, port, or network change: YES / NO

Open WebUI no longer localhost-only: YES / NO

More than three prompt revisions required: YES / NO

Critical test not reproducible: YES / NO

Removal not verifiable: YES / NO

Evidence incomplete: YES / NO

Any stop condition triggered: YES / NO

Stop-condition action:

## Reviewer Determination

Final run result: PASS / FAIL / BLOCKED

Evidence sufficient: YES / NO

Rerun authorized: YES / NO

Prompt revision authorized: YES / NO

Test closed: YES / NO

Reviewer rationale:

Reviewer name:

Review date:

## Evidence Integrity

Record file path:

Record SHA-256:

Screenshot or attachment inventory:

Related prompt-library version:

Related prompt-control-standard version:

Related commit:

Additional notes:
