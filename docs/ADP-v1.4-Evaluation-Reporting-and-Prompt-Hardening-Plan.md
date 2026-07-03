# ADP v1.4 — Evaluation Reporting, Prompt Hardening, and Resource-Aware Model Comparison

Date: 2026-07-02

Status: Planned

Project: AI Development Platform — ADP

Host: smt-ai

Workspace: ~/Labs/AI-Development-Platform

Repository: git@github.com:TimSImmons3/AI-Development-Platform.git

Engineering log: docs/ADP-Engineering-Log.md

## Purpose

ADP v1.4 improves the local model evaluation capability created in ADP v1.3.

The v1.3 harness successfully validated controlled prompt execution for approved local models. However, the prompt set exposed contextual drift, and the raw runtime outputs require stronger reporting and comparison structure before they can support consistent review.

ADP v1.4 focuses on strengthening evaluation quality without changing the approved model baseline or Open WebUI deployment posture.

## Current Baseline

ADP v1.3 remains the latest completed release.

Last completed release commit:

- 281079c Add ADP local model evaluation harness

Approved local models:

- llama3.2:1b
- llama3.2:3b

Post-Docker-update baseline validation was completed before beginning v1.4 planning.

Observed Ollama version:

- 0.30.11

Open WebUI baseline:

- Image: ghcr.io/open-webui/open-webui:v0.10.2
- Binding: 127.0.0.1:3000->8080/tcp
- Scope: localhost-only

Security posture remains unchanged:

- Do not expose Open WebUI to LAN or Internet.
- Do not use --network=host.
- Do not delete the open-webui Docker volume.
- Do not disable UFW.
- Ollama listening on *:11434 remains a documented residual risk controlled by firewall posture.

## v1.4 Objectives

ADP v1.4 will deliver three controlled improvements:

1. Harden the prompt validation set with stronger ADP-specific context.
2. Add a lightweight evaluation reporting template for human review.
3. Add a resource-aware comparison structure that can capture duration and observed resource notes without overcomplicating the runner.

## In Scope

The following items are in scope for ADP v1.4:

- Review and improve the five existing validation prompts.
- Preserve the v1.3 prompt categories:
    - Basic responsiveness
    - ADP workflow summary
    - Structured JSON output
    - Risk mitigation
    - Engineering log draft
- Add stronger ADP/Ollama/Open WebUI context to reduce contextual drift.
- Add an evaluation report template under docs/.
- Add a model comparison summary template under tests/model-validation/results/.
- Preserve raw JSONL result exclusion through .gitignore.
- Re-run the validation harness against:
    - llama3.2:1b
    - llama3.2:3b
- Record observed duration and qualitative review findings.
- Update docs/ADP-Engineering-Log.md after validation.

## Out of Scope

The following items are not in scope for ADP v1.4:

- No new model approvals.
- No Docker Compose architecture changes.
- No Open WebUI exposure changes.
- No LAN or Internet exposure.
- No --network=host use.
- No deletion or recreation of the open-webui Docker volume.
- No UFW disablement.
- No heavy benchmarking suite.
- No GPU tuning.
- No automated audit-readiness claim for model outputs.

## Acceptance Criteria

ADP v1.4 is complete only when all of the following are true:

- Git baseline is clean before implementation.
- Prompt files are updated intentionally and reviewed.
- Evaluation reporting template exists.
- Model comparison summary template exists.
- Validation harness executes successfully for llama3.2:1b.
- Validation harness executes successfully for llama3.2:3b.
- Each approved model completes all validation prompts successfully.
- Raw runtime JSONL results remain ignored and uncommitted.
- Human review notes are documented.
- docs/ADP-Engineering-Log.md is updated with a v1.4 entry.
- Git commit is created and pushed.
- Final post-commit validation confirms local main and origin/main match.
- Timeshift snapshot is taken and confirmed after release.

## Recommended Implementation Order

1. Create this v1.4 planning document.
2. Harden the five prompt files.
3. Add evaluation reporting template.
4. Add model comparison summary template.
5. Run validation harness for llama3.2:1b.
6. Run validation harness for llama3.2:3b.
7. Review output quality and runtime behavior.
8. Update engineering log.
9. Commit and push.
10. Confirm clean post-commit state.
11. Take final Timeshift snapshot.

## Quality Notes

The evaluation harness confirms technical execution and basic response behavior. It does not make local model output audit-ready by itself.

All model outputs must remain subject to human review before being used for security, governance, compliance, financial, legal, or operational decisions.

## v1.4 Release Target

Target release name:

ADP v1.4 — Evaluation Reporting / Prompt Hardening / Resource-Aware Model Comparison
