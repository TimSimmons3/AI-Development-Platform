# ADP Operational Runbook

Version: v1.6 candidate
Project: AI Development Platform
Host: smt-ai
Workspace: /home/tim/Labs/AI-Development-Platform
Repository: git@github.com:TimSimmons3/AI-Development-Platform.git
Engineering log: docs/ADP-Engineering-Log.md

## Purpose

This runbook defines the standard operating process for the AI Development Platform.
It is intended to keep the platform stable, recoverable, secure, and auditable.

## Operating Workflow

Plan -> Implement -> Validate -> Document -> Snapshot -> Release

No implementation work should begin until the current baseline has been validated.
No release should be considered complete until documentation, Git, and snapshot evidence are complete.
## Scope

This runbook covers routine operational checks, change control, validation, documentation, snapshot handling, rollback readiness, and release closeout for the ADP local platform.

## In Scope

- Local ADP repository operations.
- Ollama service validation.
- Approved model validation.
- Open WebUI container validation.
- Localhost-only Open WebUI access posture.
- Git commit and push validation.
- Timeshift snapshot confirmation.
- Recovery readiness checks.

## Out of Scope

- Exposing Open WebUI to LAN or Internet.
- Adding unapproved models.
- Changing the Open WebUI image without a documented plan.
- Disabling UFW.
- Deleting the Open WebUI Docker volume.
- Using Docker host networking for Open WebUI.
- Local document ingestion or RAG workflows.
## Security Baseline

The ADP security baseline must remain stable unless a documented change plan is approved and validated.

- Open WebUI must remain localhost-only.
- Open WebUI must remain bound to 127.0.0.1:3000->8080/tcp.
- Open WebUI image must remain ghcr.io/open-webui/open-webui:v0.10.2 unless deliberately changed.
- Open WebUI must not be exposed to LAN or Internet.
- Open WebUI must not use Docker host networking.
- The open-webui Docker volume must not be deleted during routine operations.
- UFW must not be disabled during routine operations.
- Ollama port 11434 listening behavior remains a documented residual risk controlled by firewall posture.

## Approved Models

- llama3.2:1b
- llama3.2:3b

No other model should be treated as approved unless it is tested, documented, committed, pushed, and snapshotted through the ADP workflow.
## Quality Gate Requirements

The ADP command and content quality gate applies before creating, modifying, promoting, staging, committing, or executing ADP content or code.

- Use short command blocks by default.
- Use flat terminal commands with no leading indentation.
- Avoid long heredocs.
- Avoid nested Markdown bullets in generated documents.
- Avoid manual leading spaces in generated content.
- Avoid sed replacements that depend on leading spaces.
- Write generated content to temporary files first.
- Promote temporary files into the repository only after validation passes.
- Treat non-ASCII findings as hard stops.
- Treat command wrapping, filename corruption, or pasted fragments as hard stops.
- Run git diff --check before staging or committing promoted files.

If any quality gate check fails, stop and correct the temporary candidate before touching repository files.
## Routine Operational Checks

Run routine checks before material ADP work, after a reboot, after Docker or Ollama changes, and before release closeout.

- Confirm host and workspace.
- Confirm Git branch is main.
- Confirm Git status is clean before starting controlled work.
- Confirm local HEAD matches origin/main.
- Confirm Open WebUI container is healthy.
- Confirm Open WebUI remains localhost-only.
- Confirm Ollama is installed and responding.
- Confirm approved models are present.
- Confirm no unplanned repository files are present.

If any check fails, stop and resolve the baseline issue before continuing.
## Change Control

All ADP changes must be deliberate, validated, documented, and recoverable.

- Define the change objective before implementation.
- Confirm the change is within the active release scope.
- Use temporary files before promoting generated content into the repository.
- Validate temporary content before promotion.
- Validate promoted content after promotion.
- Review git diff before staging.
- Run git diff --check before committing.
- Commit only reviewed and validated files.
- Push the commit and verify local HEAD equals origin/main.

Do not combine unrelated changes in the same commit.
## Recovery Readiness

ADP recovery readiness depends on clean Git state, documented configuration, working platform checks, and confirmed Timeshift snapshots.

- Keep release documentation current.
- Keep Git commits small enough to review and recover.
- Confirm pushed commits before taking final release snapshots.
- Confirm Timeshift snapshot creation in the GUI or terminal.
- Record final snapshot name in the engineering log.
- Do not rely on an unverified snapshot for release recovery.

The planned v1.6 final snapshot name is ADP-v1.6-operational-hardening-recovery-validation-complete.
## Release Closeout

A release is complete only after implementation, validation, documentation, Git synchronization, and snapshot confirmation are complete.

- Confirm all planned artifacts exist.
- Confirm documentation is ASCII-clean.
- Confirm git diff --check passes.
- Commit release artifacts with a clear commit message.
- Push to origin/main.
- Verify local HEAD equals origin/main.
- Take or confirm the release Timeshift snapshot.
- Record release completion in docs/ADP-Engineering-Log.md.

If any release closeout check fails, the release remains incomplete.
