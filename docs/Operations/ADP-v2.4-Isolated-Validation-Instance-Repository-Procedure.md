# ADP v2.4 Isolated Validation Instance Repository Procedure

## 1. Packet Status

```text
PACKET=ADP-v2.4-REPOSITORY-ONLY-IMPLEMENTATION-v3
V1_PACKET=SUPERSEDED_DO_NOT_REUSE
V2_PACKET=SUPERSEDED_DO_NOT_REUSE
RUNTIME_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
EXPECTED_BASELINE=c9de7d74e4b3dd31887567820052220d61954d6f
```

## 2. Objective

Install and validate only the refrozen repository artifacts for the isolated validation-instance design.

## 3. Prerequisites

- Repository path: `~/Labs/AI-Development-Platform`
- Branch: `main`
- `HEAD`, `main`, and `origin/main`: `c9de7d74e4b3dd31887567820052220d61954d6f`
- Clean working tree after the v2 safe recovery
- Docker and Docker Compose available for static configuration validation
- Primary Compose file unchanged
- Checksum-validated v3 packet

## 4. Automatic Continuation

The installer continues automatically through extraction, candidate validation, controlled copy, and repository quality validation when every preceding control passes.

No intermediate approval is required within this repository-only authorization boundary.

## 5. Stop Conditions

Stop before mutation for:

- Git baseline mismatch
- Dirty working tree
- Existing target path
- Primary Compose checksum mismatch
- Payload checksum mismatch
- ASCII, syntax, JSON, template, or Compose failure

After controlled copy, any gate failure removes only the exact package-created paths. It does not remove unknown paths. It reports whether the worktree returned to a clean state.

## 6. Corrected Validation Methods

The v3 gate uses:

```text
git status --short --untracked-files=all
```

Every approved path must appear individually with status `??`. Directory summaries, extra paths, and tracked modifications fail the gate.

Docker Compose is first checked with `docker compose config --quiet`. Its canonical JSON data model is then validated structurally. The gate does not grep human-formatted YAML output, because Compose expands short port syntax into long canonical fields.

## 7. Evidence Returned

The installer returns one transcript containing:

- Package payload checksum
- Baseline status
- Primary Compose protection status
- Exact file-level write-set status
- Static validation results
- Semantic traceability result
- Tracked-diff result
- Repository-only result
- Runtime and counted-execution holds

## 8. Success Boundary

A successful packet leaves the new files uncommitted for controlled diff review.

It does not start a container, create a volume, modify the primary instance, modify Ollama, or change the firewall.

## 9. Next Gate

After this packet passes, review the exact Git status and file contents and create the repository implementation gate record. Runtime remains blocked pending a separately frozen pre-runtime packet.
