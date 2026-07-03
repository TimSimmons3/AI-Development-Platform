# ADP v1.5 Validation Findings

## Release

ADP v1.5

## Focus

Runner Quality / Result Parsing / Evaluation Automation Hardening

## Baseline

ADP v1.5 started from the validated post-system-update baseline snapshot:

ADP-pre-v1.5-system-updates-baseline-validated

## Purpose

This document records v1.5 implementation and validation findings from the result summary generator and JSON-only prompt validator.

## Evidence Reviewed

- tests/model-validation/results/20260702-200115-llama3.2_1b.jsonl
- tests/model-validation/results/20260702-200458-llama3.2_3b.jsonl
- tests/model-validation/results/20260702-200115-llama3.2_1b-summary.md
- tests/model-validation/results/20260702-200458-llama3.2_3b-summary.md
- scripts/summarize-model-validation-results.sh
- scripts/validate-json-prompt-output.sh

## Summary Generator Findings

The summary generator successfully created readable Markdown summaries from existing runtime JSONL evidence.

### llama3.2:1b

- Prompts executed: 5
- Runner successes: 5
- Runner failures: 0
- Total duration seconds: 68
- Average duration seconds: 13.6

### llama3.2:3b

- Prompts executed: 5
- Runner successes: 5
- Runner failures: 0
- Total duration seconds: 112
- Average duration seconds: 22.4

## JSON Validation Findings

The JSON-only validator was tested against the structured JSON prompt result.

### llama3.2:1b

Result:

PASS

Finding:

The model response for 03-structured-json-output.txt was valid JSON object output.

### llama3.2:3b

Result:

FAIL

Finding:

The model response for 03-structured-json-output.txt was not valid JSON.

Root cause:

The response was missing the final closing object brace.

Observed ending:

"not_audit_ready_without_review": true

Expected ending:

"not_audit_ready_without_review": true
}

## Quality Interpretation

The v1.4 runner correctly confirmed that the model returned a response.

The v1.5 validator added a stronger quality check and correctly identified that runner execution success does not equal structured-output compliance.

This is a prompt-output quality finding, not an ADP platform health failure.

## QA Process Correction

During v1.5 implementation, invisible Unicode spacing characters were introduced into pasted script content and caused Python syntax failures.

The process correction is mandatory for executable scripts:

1. Convert known Unicode spacing characters U+2005 and U+2006 to normal ASCII spaces.
2. Remove remaining non-ASCII characters.
3. Run a non-ASCII scan.
4. Run bash syntax validation with bash -n.
5. Extract embedded Python from shell heredocs.
6. Compile embedded Python with python3 -m py_compile.
7. Execute the script only after all checks pass.

## Artifact Policy

Raw JSONL runtime files remain local evidence and must not be committed unless explicitly sanitized and approved.

Timestamped generated Markdown summaries are local runtime artifacts and are ignored by Git.

Formal templates, rubrics, and release findings documents may be committed when reviewed and approved.

## v1.5 Acceptance Impact

This finding supports the v1.5 objective.

Required next actions:

- Keep the summary generator and JSON validator.
- Keep timestamped generated summaries ignored.
- Commit this findings document as a sanitized formal artifact.
- Add workflow guidance and scoring rubric before final v1.5 closeout.
