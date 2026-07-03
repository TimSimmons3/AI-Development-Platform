# ADP v1.5 Prompt-Level Scoring Rubric

## Purpose

This rubric provides a lightweight, human-reviewable scoring structure for ADP local model validation.

It separates runner execution from model-output quality.

## Scoring Dimensions

Each prompt result should be reviewed across five dimensions.

| Dimension | Description | Pass Standard |
|---|---|---|
| Execution Status | Whether the runner completed the prompt without transport or runtime failure. | Runner status is success. |
| Instruction Adherence | Whether the model followed the prompt instructions. | Response addresses the requested task without major drift. |
| Format Compliance | Whether the response followed the required format. | Required structure, sections, or output constraints are satisfied. |
| Content Quality | Whether the response is clear, relevant, and useful. | Response is understandable, coherent, and appropriate for the ADP context. |
| Human Review Risk | Whether the output contains unsupported claims, unsafe guidance, or audit-readiness overclaims. | No material unsupported claims or unsafe recommendations are accepted without review. |

## JSON-Only Prompt Additional Check

For JSON-only prompts, format compliance requires:

- Output is valid JSON.
- Output is a JSON object unless another structure is explicitly required.
- Output does not use Markdown code fences.
- Output does not include explanatory text outside the JSON object.
- Required keys are present if the prompt defines required keys.

## Rating

Use this rating scale:

| Rating | Meaning |
|---|---|
| PASS | Meets the requirement with no material issue. |
| PASS WITH REVIEW NOTE | Mostly acceptable but has a minor issue that should be documented. |
| FAIL | Does not meet the requirement or requires prompt/model correction. |
| NOT APPLICABLE | Dimension does not apply to the prompt. |

## Prompt-Level Outcome

A prompt-level result should be classified as:

| Outcome | Criteria |
|---|---|
| Pass | Execution passes and all applicable quality checks pass. |
| Pass with Review Note | Execution passes, no blocking quality failure exists, but review notes are required. |
| Fail | Execution fails or a required output-quality check fails. |

## v1.5 Example Findings

### llama3.2:1b Structured JSON Prompt

- Execution Status: PASS
- JSON Format Compliance: PASS
- Prompt-Level Outcome: PASS

### llama3.2:3b Structured JSON Prompt

- Execution Status: PASS
- JSON Format Compliance: FAIL
- Prompt-Level Outcome: FAIL

Reason:

The model returned a response, but the structured JSON output was missing the final closing object brace.

## Review Rule

Execution success alone must not be treated as model-output success.

Human review remains required before using local model output for audit, compliance, security, release, or production-facing decisions.
