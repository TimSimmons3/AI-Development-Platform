# ADP v2.3.1 Closeout Partial-State Recovery Record

## Status

- Failed installer: `ADP-v2.3.1-Deterministic-RAG-Closeout-Installer-v2.sh`
- Expected baseline: `cf25056`
- Commit created: none
- Push performed: none
- Failure point: post-copy repository-wide non-ASCII scan
- Current state before recovery: known partial closeout copy

## Root Cause

The v2 installer scanned every Markdown and shell file in the historical repository after copying the closeout package.

That scan found pre-existing Unicode spacing in `docs/ADP-Model-Selection-Standard.md`, an unchanged file already present in baseline `cf25056`.

The gate scope was invalid for this closeout.

## Recovery Controls

The v3 recovery installer:

1. Accepts only the exact known dirty paths from the v2 partial copy.
2. Restores tracked files to `cf25056`.
3. Removes only package-created untracked files.
4. Verifies a clean worktree.
5. Validates the package source before copying.
6. Applies changed-artifact validation rather than a global historical scan.
7. Records the legacy non-ASCII debt separately.
8. Commits, pushes, and synchronizes the closeout.
