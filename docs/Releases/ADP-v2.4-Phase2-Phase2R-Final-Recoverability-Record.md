# 05 - Recoverability Record

## Recovery sources retained

The `sources/` directory contains:

1. Original Phase-2 handoff package
2. Preserved Epoch-1 CR6 live evidence
3. Post-live independent review and recovery decision package
4. Authoritative Epoch-2 CR4 transaction package
5. Accepted Epoch-2 live evidence
6. Available checksum sidecars

All source hashes are listed in `audit/source-hash-inventory.csv`.

## Authoritative recovery points

| State | Identifier |
|---|---|
| Main baseline | `b934c7bd84bfbc35563f3681712c4d5bd8478196` |
| Preserved Epoch 1 | `cc2c3c9dccc1de11127d3dd9cd62e5d2c1b01d7c` |
| Valid Epoch 2 | `1f47c560e735ad41619da72dfcf916f822cfb2ef` |
| Registry head | `a17b91ebdc20136d18e6477127867a3d191e505ca6ec725a9dbcd8a8866769d4` |
| Registry SHA-256 | `f93e847e3b8d5aaa44bb117333f176778080f69dddf1bf27921621450d0de309` |
| Epoch-2 evidence | `dd255eb2a03ab6da71f727417419f38fd07009ec038e05a285b0987b3b31f406` |

## Verification sequence

1. Validate this closeout package ZIP and sidecar.
2. Validate the embedded source sidecars.
3. Validate the accepted Epoch-2 evidence ZIP and its internal manifest.
4. Confirm main remains at the recorded baseline or a later separately governed closeout commit.
5. Confirm Epoch 1 remains unchanged.
6. Confirm Epoch 2 resolves to `1f47c560e735ad41619da72dfcf916f822cfb2ef`.
7. Compare the design parent to Epoch 2 and require exactly the two approved added paths.
8. Confirm the registry has one entry with the recorded SHA-256 and head.
9. Confirm the two Epoch-2 rulesets remain active.
10. Verify the signed receipt and current-state evidence.

## Limitation

A final Timeshift snapshot of the host after Epoch-2 recovery is not included in this package. The remote repository, evidence archives and hash chain are sufficient to verify the completed transaction, but a host-level snapshot remains required by the broader ADP release recoverability standard.

## Final host closeout

Date UTC: `2026-08-01T12:23:08Z`

| Item | Value |
|---|---|
| Host | `smt-ai` |
| Workspace | `/home/tim/Labs/AI-Development-Platform` |
| Branch | `main` |
| Closeout publication commit | `73007c9575a4b192d40214d814f2ef6b88c75bb0` |
| Timeshift snapshot identifier | `2026-08-01_07-04-34` |
| Timeshift tags | `O` |
| Timeshift description | `ADP-v2.4-phase2-phase2r-closeout-20260801T120434Z` |
| Snapshot-time working tree | `CLEAN` |
| Snapshot-time local main | `73007c9575a4b192d40214d814f2ef6b88c75bb0` |
| Snapshot-time remote main | `73007c9575a4b192d40214d814f2ef6b88c75bb0` |
| Preserved Epoch-1 witness | `cc2c3c9dccc1de11127d3dd9cd62e5d2c1b01d7c` |
| Valid Epoch-2 witness | `1f47c560e735ad41619da72dfcf916f822cfb2ef` |
| Registry SHA-256 | `f93e847e3b8d5aaa44bb117333f176778080f69dddf1bf27921621450d0de309` |
| Registry head | `a17b91ebdc20136d18e6477127867a3d191e505ca6ec725a9dbcd8a8866769d4` |

## Continuation adjudication

The original closeout launcher created and verified the snapshot but entered HOLD because its parser collected historical identifiers from adjacent rows. This continuation independently verified the uploaded HOLD evidence and the current Timeshift row, reused the existing snapshot, and did not execute a snapshot-creation command.

## Recovery boundary

The Timeshift snapshot captures the stable closeout-publication commit. This final recoverability record is the intentional post-snapshot audit-tail commit. A verified Git bundle containing final `main`, Epoch 1 and Epoch 2 is generated after the final push and retained in the sealed continuation evidence package.

No witness branch, registry, receipt or ruleset mutation is authorized or performed.
