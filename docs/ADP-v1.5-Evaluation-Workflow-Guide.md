# ADP v1.5 Evaluation Workflow Guide

## Purpose

This guide explains how to interpret ADP local model validation results after v1.5 runner-quality and evaluation-automation hardening.

## Core Principle

Runner execution success is not the same as model-output quality success.

A model can successfully return a response while still failing format, content, safety, or audit-readiness checks.

## Evidence Types

ADP model validation produces or uses three evidence types.

| Evidence Type | Example | Git Policy |
|---|---|---|
| Raw runtime JSONL | tests/model-validation/results/YYYYMMDD-HHMMSS-model.jsonl | Local evidence; ignored unless explicitly sanitized and approved. |
| Timestamped generated summary | tests/model-validation/results/YYYYMMDD-HHMMSS-model-summary.md | Local runtime artifact; ignored by Git. |
| Formal review artifact | ADP-v1.5-Validation-Findings.md, ADP-v1.5-Scoring-Rubric.md | Commit when reviewed and approved. |

## Standard v1.5 Review Flow

1. Run the model validation harness.
2. Preserve the raw JSONL result locally.
3. Generate a timestamped Markdown summary.
4. Run structured validators where applicable.
5. Apply the scoring rubric.
6. Document findings in a formal review artifact.
7. Commit only approved scripts, guides, templates, rubrics, and formal findings.

## Summary Generator

Use:

scripts/summarize-model-validation-results.sh

Purpose:

- Reads a runtime JSONL result file.
- Extracts model, prompt, status, duration, and response previews.
- Writes a timestamped Markdown summary next to the source JSONL file.

Example:

scripts/summarize-model-validation-results.sh tests/model-validation/results/20260702-200115-llama3.2_1b.jsonl

Expected output:

tests/model-validation/results/20260702-200115-llama3.2_1b-summary.md

## JSON-Only Validator

Use:

scripts/validate-json-prompt-output.sh

Purpose:

- Reads a runtime JSONL result file.
- Locates the structured JSON prompt result.
- Extracts the model response from the Ollama payload.
- Verifies the response is valid JSON.
- Verifies the response is a JSON object.
- Fails if the output uses Markdown code fences or non-JSON explanatory text.

Example:

scripts/validate-json-prompt-output.sh tests/model-validation/results/20260702-200115-llama3.2_1b.jsonl

Expected pass result:

PASS: Valid JSON object output for 03-structured-json-output.txt

## Script QA Gate

Before executing any new or modified script, apply this gate:

1. Convert known Unicode spacing characters U+2005 and U+2006 to normal ASCII spaces.
2. Remove remaining non-ASCII characters.
3. Confirm no non-ASCII characters remain.
4. Run bash syntax validation with bash -n.
5. If the script contains embedded Python, extract it and run python3 -m py_compile.
6. Execute only after all checks pass.

## Interpreting Results

### Runner Success

Runner success means:

- Ollama API was reachable.
- The prompt was submitted.
- The model returned a response.
- A runtime result record was written.

Runner success does not prove:

- The output followed instructions.
- The output format is valid.
- The output is accurate.
- The output is safe.
- The output is audit-ready.

### Format Compliance

Format compliance should be evaluated separately.

Examples:

- JSON-only prompt must return valid JSON.
- Engineering-log draft should use the requested documentation style.
- Risk decision prompt should clearly state approve, defer, or reject where requested.

### Human Review

Human review remains required for:

- Security-impacting changes.
- Compliance claims.
- Audit evidence.
- Release decisions.
- Network exposure decisions.
- Production-facing documentation.

## v1.5 Known Finding

During v1.5 testing:

- llama3.2:1b passed runner execution and structured JSON validation.
- llama3.2:3b passed runner execution but failed structured JSON validation.

The llama3.2:3b response was missing the final closing object brace.

This confirms the need for separate quality validation after runner execution.

## Security Boundaries

ADP v1.5 does not change the security posture.

The following remain unchanged:

- Open WebUI remains localhost-only.
- Open WebUI image remains ghcr.io/open-webui/open-webui:v0.10.2.
- Open WebUI port binding remains 127.0.0.1:3000->8080/tcp.
- Open WebUI Docker volume remains preserved.
- UFW must not be disabled.
- No LAN or Internet exposure.
- No --network=host.
- No new models are added in v1.5.

## Release Rule

ADP v1.5 is not complete until:

- Scripts pass QA validation.
- Existing approved models are validated.
- Summary and validator behavior are confirmed.
- Findings and rubric are documented.
- Engineering log is updated.
- Git commit and push complete.
- Final Timeshift GUI snapshot is confirmed.
