# ADP v1.4 — Model Comparison Summary

Date: 2026-07-02

Evaluator: Timothy Simmons

Validation Run:

- llama3.2:1b result file: tests/model-validation/results/20260702-200115-llama3.2_1b.jsonl
- llama3.2:3b result file: tests/model-validation/results/20260702-200458-llama3.2_3b.jsonl

## Models Compared

| Model | Role | Status |
|---|---|---|
| llama3.2:1b | Fast baseline model | Passed |
| llama3.2:3b | Stronger controlled expansion model | Passed |

## Runtime Summary

| Model | Prompt Count | Success Count | Failure Count | Total Duration Seconds | Average Duration Seconds |
|---|---:|---:|---:|---:|---:|
| llama3.2:1b | 5 | 5 | 0 | 68 | 13.6 |
| llama3.2:3b | 5 | 5 | 0 | 112 | 22.4 |

## Prompt Duration Detail

| Prompt | llama3.2:1b Seconds | llama3.2:3b Seconds |
|---|---:|---:|
| 01-basic-responsiveness | 10 | 17 |
| 02-adp-workflow-summary | 18 | 35 |
| 03-structured-json-output | 12 | 13 |
| 04-risk-mitigation | 16 | 29 |
| 05-engineering-log-draft | 12 | 18 |

## Qualitative Comparison

| Category | llama3.2:1b | llama3.2:3b | Notes |
|---|---|---|---|
| Responsiveness | Passed | Passed | Both models completed the responsiveness prompt successfully. |
| ADP context retention | Passed technically | Passed technically | Output quality still requires human review. |
| Structured output discipline | Passed technically | Passed technically | JSON output should be validated before downstream use. |
| Risk reasoning | Passed technically | Passed technically | Security recommendations require human review. |
| Engineering-log usefulness | Passed technically | Passed technically | Draft content must be reviewed before documentation use. |
| Human review burden | Required | Required | Neither model is audit-ready without human review. |

## Recommended Use

### llama3.2:1b

Recommended for:

- Fast baseline checks.
- Lightweight prompt validation.
- Quick local responsiveness testing.

Not recommended for:

- Audit-ready conclusions.
- Final security or governance decisions without human review.

### llama3.2:3b

Recommended for:

- Stronger local reasoning checks.
- More detailed comparison prompts.
- Controlled expansion testing.

Not recommended for:

- Audit-ready conclusions.
- Final security or governance decisions without human review.

## Final Comparison Decision

- Fast baseline model: llama3.2:1b remains approved.
- Stronger controlled expansion model: llama3.2:3b remains approved.
- Any model status change required: No.

## Human Review Statement

All outputs require human review before use in security, governance, compliance, financial, legal, or operational decisions.
