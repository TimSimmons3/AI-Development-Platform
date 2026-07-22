# ADP v2.3.1 Response Capture Installer Recovery Record

## Status

- Failed installer baseline: `f41d0d6`
- Commit created by failed attempt: none
- Push performed by failed attempt: none
- Repository state: controlled partial copy only
- Runtime or Open WebUI mutation by failed installer: none

## Consolidated Defect

The response-capture package quality gate required `response.txt` to appear in both the runtime packet and operator guide. The guide contained it, but the runtime packet did not explicitly name the file after the atomic capture command.

The gate used `set -e`, so it exited on the missing filename without identifying the failed control. Its overall PASS was also placed before the final response-capture checks.

## Correction

This recovery:

1. Accepts only the known partial-copy paths.
2. Restores the clean `f41d0d6` working tree.
3. Applies the corrected package.
4. Makes quality-gate failures explicit.
5. Places the overall PASS at the true end.
6. Adds a graphical paste-dialog fallback.
7. Commits, pushes, synchronizes, and reruns the gate.
