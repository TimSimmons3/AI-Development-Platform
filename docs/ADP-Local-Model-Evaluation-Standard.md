# ADP Local Model Evaluation Standard

## Purpose

This standard defines a lightweight, repeatable process for validating local Ollama models used by the AI Development Platform.

The goal is to compare local models using a consistent prompt set, structured runtime evidence, and documented scoring so future model decisions are evidence-based, reproducible, and appropriate for a small CPU-first development host.

## Scope

This standard applies to approved and candidate local models evaluated through Ollama and Open WebUI.

Current approved models:

- llama3.2:1b
- llama3.2:3b

No additional models should be pulled during ADP v1.3 unless a separate controlled model-expansion decision is documented.

## Evaluation Workflow

Use the ADP workflow:

1. Plan
2. Implement
3. Validate
4. Document
5. Snapshot
6. Release

For each model evaluation:

1. Confirm the ADP baseline is healthy.
2. Run the standard prompt set.
3. Capture local runtime output under tests/model-validation/results/.
4. Review output manually before sharing, committing, or summarizing.
5. Score the model using the evaluation criteria.
6. Document findings in the engineering log.
7. Commit only the harness, prompt set, templates, and documentation.
8. Do not commit raw runtime evidence unless intentionally sanitized and approved.

## Standard Prompt Set

Prompt files are stored under tests/model-validation/prompts/.

| Prompt File | Purpose |
|---|---|
| 01-basic-responsiveness.txt | Basic model usefulness and responsiveness |
| 02-adp-workflow-summary.txt | ADP workflow comprehension |
| 03-structured-json-output.txt | Structured JSON instruction-following |
| 04-risk-mitigation.txt | Risk analysis and markdown table output |
| 05-engineering-log-draft.txt | Engineering documentation usefulness |

## Evaluation Criteria

Score each category from 1 to 5.

| Category | Description |
|---|---|
| Response correctness | Did the model answer the prompt accurately? |
| Instruction following | Did it follow requested format and constraints? |
| Structure quality | Did markdown, JSON, or table formatting work? |
| Usefulness | Was the output practically useful for ADP work? |
| Speed and responsiveness | Was the response usable on the host? |
| Stability | Any errors, timeouts, browser issues, or Ollama failures? |
| Resource impact | Any obvious memory, swap, CPU, or disk concerns? |

## Result Handling

Raw model outputs are runtime evidence and are written to tests/model-validation/results/.

By default, raw result files are ignored by Git.

Commit:

- Prompt files
- Runner script
- Evaluation standard
- Scoring templates
- Sanitized summaries if approved

Do not commit:

- Raw model output files
- Temporary runtime evidence
- Large logs
- Sensitive content
- Unreviewed generated text

## Security and Operational Guardrails

Do not:

- Pull additional models during ADP v1.3.
- Expose Open WebUI to LAN or Internet.
- Use Docker host networking for Open WebUI.
- Delete the Open WebUI Docker volume.
- Disable UFW.
- Broaden Ollama or Open WebUI access without documented security review.
- Commit raw runtime evidence unless intentionally sanitized.

Continue to:

- Keep Open WebUI localhost-only.
- Validate after each material change.
- Document residual risk.
- Preserve Timeshift recovery discipline.
- Commit and push controlled documentation and harness changes.
