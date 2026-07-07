# ADP Maintenance Procedure

## Purpose

This procedure defines the controlled maintenance process for the AI Development Platform.

The procedure supports repeatable health checks, controlled update review, evidence capture, and recovery readiness while preserving the approved security posture.

## Maintenance Scope

Routine ADP maintenance includes:

- Repository state review.
- Documentation quality review.
- Open WebUI container health review.
- Open WebUI image and binding review.
- Ollama version and model list review.
- Snapshot and recovery evidence review.
- Security posture review.

## Maintenance Cadence

Maintenance should be performed at the following control points:

- Before starting a new ADP release.
- After material documentation changes.
- Before commit and push.
- After commit and push.
- Before final release snapshot.
- After controlled platform updates.

## Controlled Update Review

Updates must not be applied casually during release work.

A controlled update review must define:

- Update target.
- Update reason.
- Expected benefit.
- Known risk.
- Rollback path.
- Validation commands.
- Snapshot requirement.

## Routine Health Review

Routine health review must confirm the platform remains stable, recoverable, and within the approved operating baseline.

Health review evidence must include:

- Git branch and status.
- Local HEAD and origin/main HEAD.
- Required documentation presence.
- ASCII and trailing whitespace validation for changed documentation.
- Docker container status.
- Open WebUI image and binding.
- Ollama version and model list.

## Security Review

Security review must confirm that routine maintenance did not weaken the approved ADP security posture.

Security review evidence must confirm:

- Open WebUI remains bound to 127.0.0.1 only.
- Open WebUI remains pinned to the approved image unless a controlled update is approved.
- Docker host networking is not used.
- UFW posture is not weakened.
- Approved models remain unchanged unless a controlled model decision is approved.
- RAG and local content loading remain deferred until the approved roadmap point.

## Recovery Review

Recovery review must confirm that ADP can be restored from documented repository and system recovery points.

Recovery review evidence must confirm:

- Git remote state is current.
- Required documentation is committed and pushed.
- Latest release snapshot is documented.
- Rollback procedure remains available.
- Snapshot naming is clear and release-specific.

## Maintenance Closeout

Maintenance is complete only after validation evidence is reviewed and documented.

Closeout evidence must include:

- Summary of maintenance performed.
- Validation results.
- Open issues or residual risks.
- Snapshot status when applicable.
- Engineering log update when release-impacting work occurred.
