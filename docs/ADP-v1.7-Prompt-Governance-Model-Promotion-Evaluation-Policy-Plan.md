# ADP v1.7 Prompt Governance, Model Promotion, and Evaluation Policy Plan

## Status
Planned

## Date
2026-07-07

## Purpose
ADP v1.7 defines the governance standards for prompts, model promotion, model demotion, evaluation evidence, and controlled model approval.

## Scope
- Define prompt governance standards.
- Define prompt review and change expectations.
- Define model promotion and demotion criteria.
- Define evaluation evidence requirements.
- Preserve the current localhost-only security posture.
- Do not add new models unless a controlled approval process is explicitly documented and validated.

## Out of Scope
- No Open WebUI exposure changes.
- No Docker host networking.
- No Open WebUI volume deletion.
- No UFW weakening.
- No uncontrolled model downloads.
- No production workload claims.

## Planned Artifacts
- docs/ADP-v1.7-Prompt-Governance-Model-Promotion-Evaluation-Policy-Plan.md
- docs/ADP-Prompt-Governance-Standard.md
- docs/ADP-Model-Promotion-and-Evaluation-Policy.md
- docs/ADP-Engineering-Log.md

## Acceptance Criteria
- Prompt governance standard is documented.
- Model promotion and demotion policy is documented.
- Evaluation evidence requirements are documented.
- Existing approved models remain llama3.2:1b and llama3.2:3b unless a new model is explicitly approved through the documented process.
- Open WebUI remains pinned to ghcr.io/open-webui/open-webui:v0.10.2.
- Open WebUI remains bound to 127.0.0.1:3000->8080/tcp.
- Required documentation passes ASCII checks.
- Required documentation passes trailing whitespace checks.
- Git status is clean after commit and push.
- Final Timeshift snapshot is created and documented after validation.

## Security Requirements
- Preserve localhost-only access for Open WebUI.
- Preserve existing Docker volume state.
- Preserve firewall posture.
- Treat Ollama port 11434 listening behavior as a documented residual risk controlled by firewall posture.

## Validation Plan
- Validate clean Git baseline before changes.
- Validate candidate files before promotion.
- Validate promoted files after copy into docs.
- Run git diff --check before commit.
- Confirm HEAD matches origin/main after push.
- Confirm Open WebUI and Ollama baseline remain unchanged.

## Release Decision
ADP v1.7 may proceed only after the plan, standards, policy, engineering log update, final QA, Git commit, push, and Timeshift snapshot are complete.
