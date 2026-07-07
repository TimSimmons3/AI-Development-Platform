# ADP v1.8 Platform Runbook, QA Gates, and Maintenance Procedure Plan

## Release Objective

ADP v1.8 will standardize the recurring platform runbook, QA gates, health checks, maintenance cadence, and controlled update review process for the AI Development Platform.

The release will preserve the current ADP security posture and will not add models, expose services, begin RAG, or load local content.

## Current Baseline

- Prior release: ADP v1.7
- Baseline commit: 0c3888f
- Branch: main
- Host: smt-ai
- Workspace: ~/Labs/AI-Development-Platform
- Open WebUI image: ghcr.io/open-webui/open-webui:v0.10.2
- Open WebUI binding: 127.0.0.1:3000->8080/tcp
- Approved models: llama3.2:1b and llama3.2:3b

## In Scope

- Platform runbook for routine ADP operation.
- Recurring health check standard.
- QA gate standard for release readiness.
- Maintenance procedure for controlled reviews and updates.
- Evidence expectations for validation and closeout.
- Security posture preservation checks.
- Engineering log updates for v1.8 progress and closeout.

## Out of Scope

- Adding new models.
- Model promotion or demotion decisions.
- RAG implementation.
- Local document or content loading.
- Exposing Open WebUI to LAN or Internet.
- Changing Docker networking.
- Deleting or replacing the Open WebUI Docker volume.
- Weakening firewall posture.

## Planned Artifacts

- docs/ADP-v1.8-Platform-Runbook-QA-Gates-Maintenance-Procedure-Plan.md
- docs/ADP-Platform-Runbook.md
- docs/ADP-QA-Gate-Standard.md
- docs/ADP-Maintenance-Procedure.md
- docs/ADP-Engineering-Log.md

## Validation Gates

- Git status must be clean before implementation begins.
- HEAD must match origin/main before implementation begins.
- v1.7 artifacts must remain present.
- v1.8 artifacts must be ASCII-clean.
- v1.8 artifacts must have no trailing whitespace.
- Open WebUI must remain healthy and localhost-only.
- Open WebUI image must remain pinned to v0.10.2.
- Approved Ollama models must remain limited to llama3.2:1b and llama3.2:3b.
- Engineering log must record implementation, validation, and closeout evidence.

## Implementation Sequence

1. Validate clean v1.7 baseline.
2. Create and validate v1.8 plan.
3. Create platform runbook.
4. Create QA gate standard.
5. Create maintenance procedure.
6. Update engineering log.
7. Run final validation.
8. Commit and push.
9. Create final Timeshift snapshot.
10. Document v1.8 closeout.

## Security Guardrails

- Keep Open WebUI bound to 127.0.0.1 only.
- Do not use Docker host networking.
- Do not expose Open WebUI to LAN or Internet.
- Do not delete the open-webui Docker volume.
- Do not disable or weaken UFW.
- Do not add unapproved models.
- Treat Ollama port 11434 listening behavior as a residual risk controlled by firewall posture.

## Acceptance Criteria

- v1.8 plan is documented.
- Platform runbook is documented.
- QA gate standard is documented.
- Maintenance procedure is documented.
- Engineering log includes v1.8 entries.
- Final validation passes.
- Git status is clean after commit.
- Local HEAD matches origin/main after push.
- Final v1.8 snapshot is created and documented.
