# ADP Platform Runbook

## Purpose

This runbook defines the standard operating procedure for routine AI Development Platform operation, validation, and controlled recovery checks.

The runbook supports repeatable operation of the local ADP foundation while preserving the approved security posture.

## Operating Baseline

- Host: smt-ai
- Workspace: ~/Labs/AI-Development-Platform
- Repository: git@github.com:TimSimmons3/AI-Development-Platform.git
- Primary branch: main
- Engineering log: docs/ADP-Engineering-Log.md
- Open WebUI image: ghcr.io/open-webui/open-webui:v0.10.2
- Open WebUI binding: 127.0.0.1:3000->8080/tcp
- Approved models: llama3.2:1b and llama3.2:3b

## Standard Workflow

The standard ADP workflow is:

Plan -> Implement -> Validate -> Document -> Snapshot -> Release

No release should bypass validation, documentation, and recovery evidence.

## Routine Health Check

Run a routine health check before implementation work, after material changes, and before release closeout.

Minimum health check evidence includes:

- Current workspace path.
- Current host name.
- Current date and time.
- Git branch.
- Git status.
- Local HEAD.
- origin/main HEAD.
- Recent commit history.
- Required artifact presence.
- ASCII checks.
- Trailing whitespace checks.
- Open WebUI container status.
- Open WebUI image and port binding.
- Ollama version.
- Approved model list.

## Runtime Guardrails

- Keep Open WebUI localhost-only.
- Keep Open WebUI pinned to ghcr.io/open-webui/open-webui:v0.10.2 until a controlled update is approved.
- Do not expose Open WebUI to LAN or Internet.
- Do not use Docker host networking.
- Do not delete the open-webui Docker volume.
- Do not disable or weaken UFW.
- Do not add models outside the approved model list.
- Do not begin RAG or local content loading before the approved roadmap point.

## Pre-Change Checklist

- Confirm the planned change is in scope for the current release.
- Confirm the repo starts clean or document any expected staged work.
- Confirm HEAD matches origin/main unless intentionally working from local staged changes.
- Confirm no runtime or security posture change is required unless explicitly approved.
- Use temporary candidates before promoting new documentation into docs/.
- Validate temporary candidates for ASCII and trailing whitespace before promotion.

## Post-Change Checklist

- Confirm expected files changed.
- Confirm no unexpected files changed.
- Run ASCII checks on changed documentation.
- Run trailing whitespace checks on changed documentation.
- Confirm Open WebUI remains healthy and localhost-only when runtime validation is required.
- Confirm approved models remain unchanged when model validation is required.
- Update the engineering log with the change, validation evidence, and residual risks.

## Recovery Standard

- Use Git for repository-level recovery.
- Use Timeshift snapshots for system-level recovery.
- Confirm the final snapshot name in the engineering log during closeout.
- Do not treat a release as recoverable until Git, documentation, runtime, and snapshot evidence are complete.

## Evidence Standard

Runbook evidence should be sufficient for another ADP session to confirm the current state without relying on memory.

Required evidence should include commands executed, observed results, validation status, known residual risks, and final release state.
