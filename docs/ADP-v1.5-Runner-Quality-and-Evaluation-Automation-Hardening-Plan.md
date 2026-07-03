# ADP v1.5 Runner Quality and Evaluation Automation Hardening Plan

## Release

ADP v1.5

## Release Name

Runner Quality / Result Parsing / Evaluation Automation Hardening

## Baseline

ADP v1.5 starts from the validated post-system-update baseline snapshot:

ADP-pre-v1.5-system-updates-baseline-validated

The prior completed release is ADP v1.4:

ADP-v1.4-evaluation-reporting-prompt-hardening-complete

## Current Baseline State

- Host: smt-ai
- Workspace: /home/tim/Labs/AI-Development-Platform
- Branch: main
- HEAD: 1d494c5
- origin/main: 1d494c5
- Git status at baseline validation: clean
- Open WebUI image: ghcr.io/open-webui/open-webui:v0.10.2
- Open WebUI binding: 127.0.0.1:3000->8080/tcp
- Ollama version observed during validation: 0.30.11
- Approved models:
  - llama3.2:1b
  - llama3.2:3b

## Objective

Improve the local model evaluation workflow so runtime results are easier to review, compare, summarize, and evaluate without committing raw JSONL runtime evidence.

ADP v1.5 focuses on evaluation quality, result parsing, review repeatability, and controlled scoring.

## Scope

ADP v1.5 will include:

1. Improve model validation runner output readability.
2. Preserve raw runtime JSONL evidence locally while keeping it excluded from Git.
3. Add a sanitized Markdown summary generator for human review.
4. Add structured validation checks for JSON-only prompt output.
5. Add a lightweight prompt-level pass/fail scoring rubric.
6. Add guidance for interpreting model behavior, runtime results, and prompt changes.
7. Document the v1.5 workflow in the engineering log.

## Out of Scope

ADP v1.5 will not include:

- Adding new models.
- Changing Docker configuration.
- Changing Open WebUI image version.
- Changing Open WebUI network exposure.
- Changing UFW posture.
- Using host networking.
- Deleting or recreating the Open WebUI Docker volume.
- Heavy benchmarking.
- GPU tuning.
- LAN or Internet exposure.
- Treating local model output as audit-ready without human review.

## Planned Deliverables

### Documentation

- docs/ADP-v1.5-Runner-Quality-and-Evaluation-Automation-Hardening-Plan.md
- docs/ADP-v1.5-Evaluation-Workflow-Guide.md
- Updated docs/ADP-Engineering-Log.md

### Scripts

Potential script additions or updates:

- scripts/run-model-validation.sh
- scripts/summarize-model-validation-results.sh
- scripts/validate-json-prompt-output.sh

Final script names may be adjusted during implementation if a simpler structure is justified.

### Test and Result Artifacts

Potential artifacts:

- tests/model-validation/results/ADP-v1.5-Review-Summary-Template.md
- tests/model-validation/results/ADP-v1.5-Scoring-Rubric.md

Raw runtime JSONL results must remain ignored by Git.

## Quality Requirements

ADP v1.5 must preserve these quality controls:

- Raw model outputs remain available locally for evidence review.
- Sanitized Markdown summaries must be commit-safe.
- Prompt-level review must distinguish:
  - execution success
  - content quality
  - format compliance
  - JSON validity where applicable
  - human-review findings
- JSON-only prompt validation must fail clearly when output is not valid JSON.
- Scoring must remain lightweight, explainable, and human-reviewable.
- Results must not be overclaimed as audit-ready.

## Security Requirements

ADP v1.5 must preserve the current security posture:

- Open WebUI remains localhost-only.
- Open WebUI remains pinned to ghcr.io/open-webui/open-webui:v0.10.2.
- Open WebUI port binding remains 127.0.0.1:3000->8080/tcp.
- Open WebUI Docker volume must not be deleted.
- UFW must not be disabled.
- No LAN or Internet exposure.
- No --network=host.
- Ollama listening on *:11434 remains a documented residual risk controlled by firewall posture.

## Validation Plan

Validation will include:

1. Confirm repository state before changes.
2. Run existing model validation harness against approved models.
3. Confirm raw JSONL result generation still works.
4. Confirm raw JSONL files remain ignored by Git.
5. Run summary generation against current result files.
6. Confirm generated summaries are readable and sanitized.
7. Validate JSON-only prompt output for the structured JSON prompt.
8. Confirm scoring rubric can be applied consistently.
9. Confirm Git only tracks intended scripts, documentation, and templates.
10. Confirm Open WebUI and Docker posture remain unchanged.

## Acceptance Criteria

ADP v1.5 is complete only when:

- All planned scripts and documentation are created or updated.
- Existing model validation still runs successfully for:
  - llama3.2:1b
  - llama3.2:3b
- Sanitized Markdown summaries can be generated from runtime JSONL results.
- Raw JSONL files remain untracked and ignored.
- JSON-only prompt validation produces clear pass/fail results.
- Scoring rubric is documented and usable.
- Engineering log is updated.
- Git status is clean after commit.
- Changes are pushed to origin/main.
- Final Timeshift GUI snapshot is created and confirmed.

## Release Workflow

ADP v1.5 will follow the established workflow:

Plan -> Implement -> Validate -> Document -> Snapshot -> Release

## Initial Recommendation

Start with runner quality and result parsing.

Do not add new models in ADP v1.5.

Do not change Docker, Open WebUI, UFW, volumes, or network exposure.
