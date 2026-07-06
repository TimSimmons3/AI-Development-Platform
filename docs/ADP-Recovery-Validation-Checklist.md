# ADP Recovery Validation Checklist

Version: v1.6 candidate
Project: AI Development Platform
Host: smt-ai
Workspace: /home/tim/Labs/AI-Development-Platform
Repository: git@github.com:TimSimmons3/AI-Development-Platform.git
Engineering log: docs/ADP-Engineering-Log.md

## Purpose

This checklist validates that ADP can be trusted after reboot, power interruption, platform maintenance, suspected drift, or recovery activity.
It confirms repository integrity, platform health, security posture, approved models, documentation state, and release readiness.
## When To Run

Run this checklist in the following conditions:

- After a power outage.
- After a system reboot.
- After Docker maintenance.
- After Ollama maintenance.
- After Open WebUI maintenance.
- Before starting material ADP work.
- Before release closeout.
- Before taking a final release snapshot.
- After restoring from a Timeshift snapshot.
- Whenever platform drift is suspected.
## Pass Fail Standard

The checklist passes only when every required validation item is confirmed.

- Git branch must be main.
- Git status must be clean unless the active task explicitly expects a controlled change.
- Local HEAD must match origin/main after completed commits.
- Required documentation must exist.
- Required documentation must be ASCII-clean.
- Open WebUI must be healthy.
- Open WebUI must remain localhost-only.
- Ollama must respond.
- Approved models must be present.
- No unapproved security posture change may be present.

Any failed item is a hard stop until resolved or documented as an accepted residual risk.
## Repository Validation

Validate repository state before trusting the working tree.

- Confirm current directory is /home/tim/Labs/AI-Development-Platform.
- Confirm branch is main.
- Confirm git status is clean.
- Confirm local HEAD is known and expected.
- Confirm origin/main matches local HEAD after release commits.
- Review recent commits for expected release sequence.
- Stop if unexpected modified or untracked files are present.
- Stop if local and remote history diverge.
## Platform Validation

Validate the local platform before relying on ADP services.

- Confirm Docker is running.
- Confirm the Open WebUI container exists.
- Confirm the Open WebUI container status is healthy.
- Confirm the Open WebUI image is ghcr.io/open-webui/open-webui:v0.10.2.
- Confirm the Open WebUI port binding is 127.0.0.1:3000->8080/tcp.
- Stop if Open WebUI is exposed beyond localhost.
- Stop if Open WebUI is using Docker host networking.
- Stop if the open-webui Docker volume is missing after an unexpected change.
## Ollama Validation

Validate Ollama service availability and approved model presence.

- Confirm ollama --version returns successfully.
- Confirm ollama list returns successfully.
- Confirm llama3.2:1b is present.
- Confirm llama3.2:3b is present.
- Stop if an approved model is missing.
- Document any unexpected model before treating it as approved.
- Do not add new models during recovery validation unless there is an approved change plan.
## Documentation Validation

Validate documentation required for the active release and recovery process.

- Confirm docs/ADP-Command-and-Content-Quality-Gate.md exists.
- Confirm docs/ADP-v1.6-Operational-Hardening-Recovery-Validation-Plan.md exists.
- Confirm docs/ADP-Operational-Runbook.md exists.
- Confirm docs/ADP-Recovery-Validation-Checklist.md exists after it is promoted.
- Confirm release documentation is ASCII-clean.
- Confirm release documentation has no trailing whitespace.
- Confirm documentation reflects the current security baseline.
## Recovery Decision

Use the validation results to make a clear recovery decision.

- Pass means ADP is ready for controlled work or release closeout.
- Fail means ADP is not ready for controlled work.
- Degraded means ADP can be inspected but not changed until the issue is resolved.
- Unknown means required evidence is missing or inconclusive.

Do not proceed with implementation, staging, commit, push, or snapshot closeout when the recovery decision is Fail, Degraded, or Unknown.
