# ADP Snapshot and Rollback Procedure

Version: v1.6 candidate
Project: AI Development Platform
Host: smt-ai
Workspace: /home/tim/Labs/AI-Development-Platform
Repository: git@github.com:TimSimmons3/AI-Development-Platform.git
Engineering log: docs/ADP-Engineering-Log.md

## Purpose

This procedure defines how ADP snapshots and rollback decisions are handled.
It supports controlled recovery after release work, maintenance, or platform drift.
## Snapshot Standard

A snapshot is valid only when it is taken after validation and Git synchronization.

- Confirm Git status is clean before a final release snapshot.
- Confirm local HEAD matches origin/main before a final release snapshot.
- Confirm required release documentation exists.
- Confirm required release documentation is ASCII-clean.
- Confirm Open WebUI is healthy and localhost-only.
- Confirm approved Ollama models are present.
- Record the final snapshot name in the engineering log.
## ADP v1.6 Final Snapshot Name

Use this planned final snapshot name for ADP v1.6:

ADP-v1.6-operational-hardening-recovery-validation-complete

Do not mark ADP v1.6 complete until this snapshot is created or confirmed.
## When To Take A Snapshot

Take or confirm a snapshot at controlled recovery points.

- After a completed release milestone.
- After Git commit and push validation passes.
- After platform recovery validation passes.
- Before higher-risk maintenance.
- Before changing Docker, Ollama, or Open WebUI behavior.
- After successful recovery from a prior failure.
## Rollback Triggers

Rollback should be considered when the current platform state cannot be trusted or repaired safely.

- Repository history is corrupted or unintentionally rewritten.
- Required release artifacts are missing after recovery.
- Open WebUI no longer starts or remains unhealthy after troubleshooting.
- Open WebUI security posture changes unexpectedly.
- Approved Ollama models are missing and cannot be restored cleanly.
- Docker or Open WebUI volume state is damaged.
- A maintenance change creates unstable or unknown platform behavior.
- Recovery validation returns Fail, Degraded, or Unknown.
## Before Rollback

Collect enough evidence to make rollback deliberate and auditable.

- Record the observed failure condition.
- Record current Git branch, HEAD, and origin/main.
- Record current Docker and Open WebUI state.
- Record current Ollama version and model list.
- Confirm whether uncommitted repository work exists.
- Do not delete Docker volumes as a first response.
- Do not disable firewall controls as a first response.
- Prefer the most recent trusted ADP snapshot that predates the failure.
## Rollback Validation

After rollback, validate before resuming ADP work.

- Confirm host is smt-ai.
- Confirm workspace is /home/tim/Labs/AI-Development-Platform.
- Confirm Git branch is main.
- Confirm Git status is clean.
- Confirm local HEAD is expected for the restored point.
- Confirm Open WebUI is healthy.
- Confirm Open WebUI remains bound to 127.0.0.1:3000->8080/tcp.
- Confirm Ollama responds.
- Confirm approved models are present.
- Confirm required ADP documentation exists and is ASCII-clean.
## Completion Standard

Snapshot and rollback activity is complete only when the resulting state is validated and documented.

- Confirm recovery validation passes.
- Confirm security posture is unchanged or explicitly documented.
- Confirm Git state is understood and recoverable.
- Confirm final snapshot name is recorded when applicable.
- Update docs/ADP-Engineering-Log.md with the outcome.
- Stop if evidence is incomplete or inconsistent.

Do not mark a rollback or snapshot event complete based only on apparent system availability.
