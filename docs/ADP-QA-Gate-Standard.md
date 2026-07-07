# ADP QA Gate Standard

## Purpose

This standard defines the required quality gates for ADP planning, implementation, validation, documentation, snapshot, and release activities.

The goal is to ensure that each ADP release is repeatable, auditable, recoverable, and aligned with the approved security posture.

## Gate Principles

- Validate before implementation.
- Use temporary candidates before promoting documentation.
- Prefer short ASCII-only command blocks.
- Avoid hidden Unicode, smart quotes, and paste-fragile commands.
- Confirm expected changes before commit.
- Preserve Open WebUI localhost-only exposure.
- Preserve the approved model list unless a controlled model decision is approved.
- Document validation evidence before release closeout.

## Planning Gate

A release must not begin implementation until the release objective, scope, artifacts, out-of-scope items, validation gates, and acceptance criteria are documented.

Planning evidence must confirm:

- Release objective is defined.
- In-scope and out-of-scope items are documented.
- Planned artifacts are identified.
- Validation gates are defined.
- Security guardrails are documented.
- Acceptance criteria are documented.

## Implementation Gate

Implementation must use controlled, reviewable changes and must preserve the approved runtime and security baseline unless a change is explicitly approved.

Implementation evidence must confirm:

- Expected files were created or modified.
- No unexpected files were created or modified.
- No unauthorized model additions occurred.
- No Docker exposure or network posture weakening occurred.
- No Open WebUI volume deletion occurred.
- No firewall weakening occurred.

## Validation Gate

Validation must confirm that documentation, repository state, runtime state, model state, and security posture meet the release acceptance criteria.

Validation evidence must confirm:

- Git status is understood and expected.
- Changed documentation is ASCII-clean.
- Changed documentation has no trailing whitespace.
- Required artifacts are present.
- Open WebUI remains healthy when runtime validation is required.
- Open WebUI remains bound to 127.0.0.1 only.
- Approved Ollama models remain unchanged unless a controlled model decision is approved.

## Documentation Gate

Documentation must be updated before release closeout so the current platform state can be recovered and audited in a future session.

Documentation evidence must confirm:

- Release plan is present.
- New or updated standards are present.
- Engineering log records implementation progress.
- Engineering log records validation evidence.
- Engineering log records residual risks.
- Engineering log records release closeout after final validation.

## Snapshot Gate

A material ADP release is not complete until a recovery snapshot is created and documented.

Snapshot evidence must confirm:

- Snapshot was created after validation and push.
- Snapshot name is documented.
- Snapshot purpose is documented.
- Engineering log records the snapshot.

## Release Gate

Release closeout must confirm that the repository, documentation, runtime, model list, security posture, and recovery evidence are complete and consistent.

Release evidence must confirm:

- Git status is clean after commit.
- Local HEAD matches origin/main after push.
- Required artifacts are present.
- Changed artifacts are ASCII-clean.
- Changed artifacts have no trailing whitespace.
- Runtime and model state remain approved.
- Final snapshot is documented.
