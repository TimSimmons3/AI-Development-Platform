# ADP v1.4 — Local Model Evaluation Report

Date: 2026-07-02

Evaluator: Timothy Simmons

Host: smt-ai

Workspace: ~/Labs/AI-Development-Platform

## Evaluation Purpose

This report summarizes local model validation results for ADP v1.4.

The evaluation compared approved local models across controlled prompts, runtime behavior, response quality expectations, and human-review requirements.

## Approved Models Evaluated

- llama3.2:1b
- llama3.2:3b

## Validation Scope

Prompt categories:

- Basic responsiveness
- ADP workflow summary
- Structured JSON output
- Risk mitigation
- Engineering log draft

## Baseline Controls

Open WebUI baseline:

- Image: ghcr.io/open-webui/open-webui:v0.10.2
- Binding: 127.0.0.1:3000->8080/tcp
- Scope: localhost-only

Security constraints:

- Do not expose Open WebUI to LAN or Internet.
- Do not use --network=host.
- Do not delete the open-webui Docker volume.
- Do not disable UFW.
- Ollama listening on *:11434 remains a documented residual risk controlled by firewall posture.

## Execution Summary

| Model | Prompts Run | Successes | Failures | Total Duration | Average Duration | Result |
|---|---:|---:|---:|---:|---:|---|
| llama3.2:1b | 5 | 5 | 0 | 68 seconds | 13.6 seconds | Passed |
| llama3.2:3b | 5 | 5 | 0 | 112 seconds | 22.4 seconds | Passed |

## Prompt-Level Review

| Prompt | Model | Technical Result | Quality Notes | Human Review Required |
|---|---|---|---|---|
| 01-basic-responsiveness | llama3.2:1b | Success | Hardened ADP context prompt completed. | Yes |
| 01-basic-responsiveness | llama3.2:3b | Success | Hardened ADP context prompt completed. | Yes |
| 02-adp-workflow-summary | llama3.2:1b | Success | Workflow summary prompt completed. | Yes |
| 02-adp-workflow-summary | llama3.2:3b | Success | Workflow summary prompt completed. | Yes |
| 03-structured-json-output | llama3.2:1b | Success | Structured-output prompt completed. JSON still requires validation before downstream use. | Yes |
| 03-structured-json-output | llama3.2:3b | Success | Structured-output prompt completed. JSON still requires validation before downstream use. | Yes |
| 04-risk-mitigation | llama3.2:1b | Success | Risk-mitigation prompt completed. Security conclusions require human review. | Yes |
| 04-risk-mitigation | llama3.2:3b | Success | Risk-mitigation prompt completed. Security conclusions require human review. | Yes |
| 05-engineering-log-draft | llama3.2:1b | Success | Engineering-log draft prompt completed. Draft content must be reviewed before use. | Yes |
| 05-engineering-log-draft | llama3.2:3b | Success | Engineering-log draft prompt completed. Draft content must be reviewed before use. | Yes |

## Resource Observation Notes

Observed from validation run:

- Both approved models completed all five prompts successfully.
- llama3.2:1b completed the validation set faster than llama3.2:3b.
- llama3.2:3b required longer runtime, especially for workflow summary and risk mitigation prompts.
- No validation output indicated Ollama API failure.
- No validation output indicated Open WebUI container failure.
- Raw runtime JSONL files remained ignored and uncommitted.

## Findings

### llama3.2:1b

Strengths:

- Fastest approved baseline model.
- Completed all hardened prompts successfully.
- Suitable for quick local responsiveness and validation checks.

Limitations:

- Output still requires human review.
- Not approved for audit-ready conclusions.
- May be less suitable for deeper reasoning tasks than the larger controlled expansion model.

Recommended use:

- Fast baseline checks.
- Lightweight local validation.
- Initial prompt behavior testing.

### llama3.2:3b

Strengths:

- Completed all hardened prompts successfully.
- Remains the stronger controlled expansion model.
- Suitable for more detailed local reasoning checks.

Limitations:

- Slower than llama3.2:1b.
- Output still requires human review.
- Not approved for audit-ready conclusions.

Recommended use:

- Stronger local reasoning validation.
- More detailed ADP workflow, risk, and documentation prompts.
- Controlled comparison against the fast baseline model.

## Decision

Approved baseline status after v1.4 validation:

- llama3.2:1b: Remains approved as the fast baseline model.
- llama3.2:3b: Remains approved as the stronger controlled expansion model.

No model status change is required.

## Human Review Statement

The validation harness confirms technical execution and basic response behavior only.

Model outputs are not audit-ready without human review.

## Residual Risks

- Local model outputs may be incomplete, inaccurate, or contextually weak.
- Structured output may still require validation before downstream use.
- Runtime duration may vary based on host load.
- Ollama listening on *:11434 remains a documented residual risk controlled by firewall posture.

## Next Steps

- Update docs/ADP-Engineering-Log.md with the ADP v1.4 validation entry.
- Commit and push v1.4 artifacts after review.
- Confirm clean post-commit state.
- Take final Timeshift snapshot after release.
