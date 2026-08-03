# ADP v2.4 Candidate-v7 Corrective and Preventive Action Record

## Closed Candidate-v7 corrective actions

- Preserved terminal failure history without retry or registry rewrite.
- Preserved cleanup of the temporary API key, uploaded source, and ephemeral knowledge collection.
- Invalidated the exposed administrator JWT through controlled secret rotation.
- Persisted the Open WebUI signing secret through a host-managed read-only mount.
- Removed the plaintext JWT copy.
- Excluded whole-desktop secret-bearing screenshot evidence from ordinary artifacts.
- Replaced implicit repository Git-signing assumptions with explicit agent-only SSH signing policy and transaction-local Git configuration.

## Permanent remediation remains open

- Acquire the exact immutable R2 operator ZIP.
- Complete source-level RCA of upload, processing, association, membership verification, and attempt-boundary logic.
- Replace manual screenshots with machine-readable evidence.
- Move the counted-attempt marker immediately before the first counted inference.
- Complete one real-host non-counted Candidate-v8 rehearsal for the immutable replacement package.
