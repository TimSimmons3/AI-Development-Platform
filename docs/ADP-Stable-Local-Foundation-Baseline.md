# ADP Stable Local Foundation Baseline

## Purpose

This document defines the ADP v2.0 stable local foundation baseline for the AI Development Platform. It consolidates the validated foundation established through v1.9 and confirms the platform is ready to serve as the controlled pre-v2.1 baseline.

## Baseline Scope

- ADP v2.0 is a documentation, validation, and baseline consolidation release.
- ADP v2.0 preserves the current security, runtime, model, Docker, firewall, and recovery posture.
- ADP v2.0 does not implement RAG, vector databases, document ingestion, indexing, embedding, or local content loading.
- ADP v2.0 does not add models or expose Open WebUI beyond localhost.

## Validated Starting Point

- Host: smt-ai
- Workspace: ~/Labs/AI-Development-Platform
- Repository branch: main
- Starting baseline: ADP v1.9
- Starting HEAD: b8661ce
- Starting origin/main: b8661ce
- v1.9 closeout commit: b8661ce Document ADP v1.9 release closeout
- v1.9 implementation commit: 5e8580f Add ADP v1.9 future capability readiness review

## Runtime Baseline

- Open WebUI container: open-webui
- Open WebUI image: ghcr.io/open-webui/open-webui:v0.10.2
- Open WebUI binding: 127.0.0.1:3000->8080/tcp
- Open WebUI status at v2.0 start gate: Up and healthy
- Ollama version observed at v2.0 start gate: 0.30.11
- Approved models: llama3.2:1b and llama3.2:3b
- Unexpected models at v2.0 start gate: none observed

## Security Baseline

- Open WebUI remains localhost-only.
- Open WebUI must not be exposed to the LAN or Internet.
- Docker host networking must not be used.
- UFW and firewall posture must not be weakened.
- The Open WebUI Docker volume must not be deleted or replaced.
- Ollama port 11434 listening behavior remains a documented residual risk controlled by firewall posture.

## Documentation Baseline

- Engineering log: docs/ADP-Engineering-Log.md
- v2.0 plan: docs/ADP-v2.0-Stable-Local-Foundation-Baseline-Plan.md
- v2.0 baseline document: docs/ADP-Stable-Local-Foundation-Baseline.md
- v2.0 validation report: docs/ADP-v2.0-Foundation-Validation-Report.md

## Governance Baseline

- Release workflow remains Plan -> Implement -> Validate -> Document -> Snapshot -> Release.
- Model additions require explicit planning, review, approval, validation, and documentation.
- Prompt governance and model promotion controls remain part of the governed baseline.
- Future local content loading and RAG work remains deferred to v2.1 or later.

## QA Gate Baseline

- Git state must be clean before closeout.
- HEAD must match origin/main after commit and push.
- Required artifacts must be present.
- Markdown artifacts must be ASCII-clean.
- Markdown artifacts must have no trailing whitespace.
- Runtime checks must confirm Open WebUI health, localhost binding, Ollama availability, and approved model presence.

## Recovery Baseline

- Git remains the source of truth for versioned ADP documentation.
- Timeshift snapshots remain the recovery checkpoint mechanism for material release milestones.
- Final v2.0 snapshot must be created after validation and documented in the engineering log.
- Recovery posture must preserve the ability to return to the validated v2.0 foundation baseline.

## Pre-v2.1 Readiness Boundary

- v2.0 may document readiness for future local content and RAG work.
- v2.0 must not load local documents, install RAG tooling, install a vector database, or create embeddings.
- v2.1 must begin only after v2.0 is validated, documented, committed, pushed, snapshotted, and recoverable.

## Stable Foundation Criteria

- v1.0 through v1.9 artifacts and controls are consolidated into a stable baseline.
- Runtime, security, recovery, QA, maintenance, governance, and model-control baselines are documented.
- No unauthorized scope expansion occurs.
- The platform remains suitable for controlled future expansion.

## Release Acceptance

- v2.0 plan, foundation baseline, validation report, and engineering log entries are complete.
- All v2.0 artifacts pass ASCII and trailing-whitespace gates.
- Runtime remains healthy and localhost-only.
- Approved model set remains unchanged.
- Git status is clean after final commit.
- HEAD matches origin/main after push.
- Final v2.0 Timeshift snapshot is created and documented.
