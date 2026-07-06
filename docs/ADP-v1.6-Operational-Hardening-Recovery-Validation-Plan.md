# ADP v1.6 Operational Hardening and Recovery Validation Plan

## Status

Draft

## Date

2026-07-06

## Purpose

ADP v1.6 proves that the AI Development Platform is operationally repeatable, recoverable, and supportable before adding new capabilities.

This milestone focuses on operational hardening, recovery validation, health checks, startup and shutdown procedure, snapshot discipline, and baseline runbook quality.

## Scope

- Scope: Operational runbook documentation.
- Scope: Recovery validation checklist.
- Scope: Snapshot and rollback procedure.
- Scope: Health-check procedure.
- Scope: Git and GitHub recovery validation.
- Scope: Docker and Open WebUI validation.
- Scope: Open WebUI volume preservation checks.
- Scope: Ollama service and approved-model validation.
- Scope: Residual risk documentation.
- Scope: Engineering log update after validation.

## Explicit Exclusions

- Exclusion: New local models.
- Exclusion: New RAG, document QA, or content-loading capability.
- Exclusion: Open WebUI exposure to LAN or Internet.
- Exclusion: Docker network posture changes.
- Exclusion: Open WebUI volume deletion or recreation.
- Exclusion: UFW disablement.
- Exclusion: Production or compliance use of local model output.
- Exclusion: Automated recovery scripts unless separately approved and QA-gated.

## Current Baseline

- Baseline: Host is smt-ai.
- Baseline: Workspace is /home/tim/Labs/AI-Development-Platform.
- Baseline: Branch is main.
- Baseline: HEAD and origin/main are aligned at 36d6fad after the quality gate commit.
- Baseline: Open WebUI image is ghcr.io/open-webui/open-webui:v0.10.2.
- Baseline: Open WebUI binding is 127.0.0.1:3000->8080/tcp.
- Baseline: Open WebUI volume is open-webui.
- Baseline: Ollama version observed after outage recovery is 0.30.11.
- Baseline: Approved model is llama3.2:1b.
- Baseline: Approved model is llama3.2:3b.

## Required QA Strategy

- QA: Follow docs/ADP-Command-and-Content-Quality-Gate.md before creating or promoting v1.6 files.
- QA: Use short command blocks by default.
- QA: Write generated content to temporary files before repo promotion.
- QA: Reject non-ASCII findings as hard stops unless explicitly approved.
- QA: Avoid nested Markdown bullets in generated documents.
- QA: Avoid manual leading spaces in generated content.
- QA: Run content checks before promotion.
- QA: Run git diff --check after promotion.
- QA: Keep validation scoped to v1.6 content unless legacy cleanup is explicitly approved.

## Planned Deliverables

- Deliverable: docs/ADP-Command-and-Content-Quality-Gate.md.
- Deliverable: docs/ADP-v1.6-Operational-Hardening-Recovery-Validation-Plan.md.
- Deliverable: docs/ADP-Operational-Runbook.md.
- Deliverable: docs/ADP-Recovery-Validation-Checklist.md.
- Deliverable: docs/ADP-Snapshot-and-Rollback-Procedure.md.
- Deliverable: docs/ADP-Engineering-Log.md update.

## Acceptance Criteria

- Acceptance: Baseline validation passes before implementation.
- Acceptance: Quality gate document is committed and pushed.
- Acceptance: Operational runbook is documented.
- Acceptance: Recovery validation checklist is documented.
- Acceptance: Snapshot and rollback procedure is documented.
- Acceptance: Health-check commands are documented.
- Acceptance: Git and GitHub recovery validation is documented.
- Acceptance: Docker and Open WebUI validation is documented.
- Acceptance: Open WebUI volume preservation checks are documented.
- Acceptance: Ollama approved-model validation is documented.
- Acceptance: Security posture remains unchanged.
- Acceptance: Non-ASCII checks pass for v1.6 documents.
- Acceptance: git diff --check passes.
- Acceptance: Local main matches origin/main after push.
- Acceptance: Final Timeshift snapshot is created and confirmed.

## Security Posture

- Security: Open WebUI remains localhost-only.
- Security: Open WebUI image remains pinned to ghcr.io/open-webui/open-webui:v0.10.2.
- Security: Open WebUI binding remains 127.0.0.1:3000->8080/tcp.
- Security: Do not expose Open WebUI to LAN or Internet.
- Security: Do not use --network=host.
- Security: Do not delete the open-webui Docker volume.
- Security: Do not disable UFW.
- Security: Ollama listening on all interfaces at port 11434 remains a documented residual risk controlled by firewall posture.
- Security: No new models are added in v1.6.

## Residual Risks

- Risk: Host failure may require Timeshift rollback plus Git validation.
- Risk: Power loss may reset temporary files stored in /tmp.
- Risk: The Open WebUI Docker volume is critical local state and must be preserved.
- Risk: Local model output remains non-authoritative and requires human review.
- Risk: Ollama listening on port 11434 remains controlled by firewall posture.
- Risk: Runtime behavior may vary based on host load, service state, or updates.
- Risk: Paste, indentation, and hidden-character corruption remain known workflow risks.

## Implementation Sequence

- Step: Validate clean baseline.
- Step: Confirm command and content quality gate is committed and pushed.
- Step: Create v1.6 plan candidate in /tmp.
- Step: Validate v1.6 plan candidate before promotion.
- Step: Promote v1.6 plan into docs after validation.
- Step: Create operational runbook.
- Step: Create recovery validation checklist.
- Step: Create snapshot and rollback procedure.
- Step: Run documentation QA checks.
- Step: Update engineering log.
- Step: Review Git diff.
- Step: Commit and push v1.6 artifacts.
- Step: Confirm local main and origin/main match.
- Step: Create final Timeshift snapshot.
- Step: Confirm final snapshot name in GUI.

## Final Snapshot Name

ADP-v1.6-operational-hardening-recovery-validation-complete
