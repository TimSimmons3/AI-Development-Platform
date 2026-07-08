# ADP v2.0 Stable Local Foundation Baseline Plan

## Release Objective

ADP v2.0 establishes the stable local foundation baseline for the AI Development Platform before any future local content loading, RAG, document QA testing, vector database work, or expanded model activity.

## Current Baseline

- Host: smt-ai
- Workspace: ~/Labs/AI-Development-Platform
- Repository branch: main
- Current validated baseline: ADP v1.9
- Current HEAD and origin/main: b8661ce
- Open WebUI image: ghcr.io/open-webui/open-webui:v0.10.2
- Open WebUI binding: 127.0.0.1:3000->8080/tcp
- Ollama version observed at start gate: 0.30.11
- Approved models: llama3.2:1b and llama3.2:3b

## In Scope

- Consolidate the validated foundation from v1.0 through v1.9.
- Validate Git, Docker, Open WebUI, Ollama, documentation, runtime, and recovery controls.
- Confirm runbook, QA gates, maintenance procedure, governance, model controls, and future-readiness assumptions are aligned.
- Document the stable pre-RAG local foundation baseline.
- Define acceptance criteria for v2.0 release readiness.

## Out of Scope

- RAG installation or enablement.
- Vector database installation.
- Local document loading, ingestion, indexing, or embedding.
- Local file loading into Open WebUI.
- Network exposure changes.
- Firewall weakening.
- Docker host networking.
- Open WebUI Docker volume deletion or replacement.
- Unapproved model additions.

## Planned Artifacts

- docs/ADP-v2.0-Stable-Local-Foundation-Baseline-Plan.md
- docs/ADP-Stable-Local-Foundation-Baseline.md
- docs/ADP-v2.0-Foundation-Validation-Report.md
- docs/ADP-Engineering-Log.md

## Validation Gates

- Confirm clean Git status before implementation.
- Confirm branch main and HEAD aligned to origin/main.
- Confirm v1.9 artifacts remain present and unchanged unless explicitly planned.
- Confirm Open WebUI remains healthy and localhost-only.
- Confirm approved models remain present with no unexpected models.
- Confirm v2.0 documents are ASCII-clean.
- Confirm v2.0 documents have no trailing whitespace.
- Confirm no RAG, vector database, ingestion, networking, firewall, or Open WebUI exposure changes occurred.

## Security Guardrails

- Preserve localhost-only Open WebUI access.
- Preserve the current Open WebUI image and Docker binding unless a separately approved change is documented.
- Do not use Docker host networking.
- Do not weaken UFW or firewall posture.
- Do not delete or replace the Open WebUI Docker volume.
- Treat Ollama port 11434 listening behavior as a documented residual risk controlled by firewall posture.

## Stable Foundation Baseline Criteria

- The v1.0 through v1.9 foundation is consolidated and documented.
- Runtime, governance, QA, maintenance, recovery, and future-readiness controls are aligned.
- The platform is suitable as the pre-v2.1 baseline.
- The release remains documentation and validation focused unless a reviewed plan explicitly approves a change.

## Runtime Baseline Criteria

- Open WebUI is running and healthy.
- Open WebUI remains bound to 127.0.0.1:3000->8080/tcp.
- Ollama is available locally.
- llama3.2:1b and llama3.2:3b remain available.
- No unapproved runtime or model changes are introduced.

## Documentation Baseline Criteria

- v2.0 plan is reviewed before promotion to docs/.
- Foundation baseline document records the validated state.
- Validation report records checks, results, and exceptions.
- Engineering log records v2.0 implementation and closeout.

## Recovery Baseline Criteria

- Git state is clean after implementation.
- HEAD matches origin/main after commit and push.
- Final Timeshift snapshot is created after validation.
- Snapshot name is documented in the engineering log.

## Acceptance Criteria

- All planned v2.0 artifacts are present.
- All v2.0 artifacts are ASCII-clean and free of trailing whitespace.
- Runtime baseline remains stable and localhost-only.
- Approved model set is unchanged unless separately approved.
- No v2.1 work is started.
- Engineering log contains v2.0 implementation and closeout entries.
- Git status is clean.
- HEAD matches origin/main.
- Final v2.0 snapshot is documented.
