# ADP v2.3.1 Closeout Installer Repository-Architecture Correction

## Status

- Failed installer: `ADP-v2.3.1-Deterministic-RAG-Closeout-Installer-v1.sh`
- Starting baseline: `cf25056`
- Commit created by failed installer: none
- Push performed by failed installer: none
- Repository mutation before failure: none

## Defect

The v1 installer required a root `CHANGELOG.md` and attempted to append to it.

The ADP repository does not use a root changelog as an established canonical record. Its established running record is:

```text
docs/ADP-Engineering-Log.md
```

Creating a new changelog solely to satisfy the installer would introduce an unapproved duplicate record.

## Correction

The v2 installer:

1. Removes the invalid `CHANGELOG.md` prerequisite.
2. Does not create a new changelog.
3. Appends the closeout entry only to `docs/ADP-Engineering-Log.md`.
4. Preserves the detailed release and closeout records under `docs/Releases`.
5. Retains all evidence, standards, configuration baseline, Git, and recovery controls.
