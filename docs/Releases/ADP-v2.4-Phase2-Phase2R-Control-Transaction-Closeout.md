# 01 - Executive Closeout Decision

## Final disposition

```text
PHASE2_EPOCH1=FAILED_CHANGED_PATH_SCOPE_PRESERVED
PHASE2R_EPOCH2=PASS
PHASE2_PHASE2R_CONTROL_TRANSACTION=CLOSED_PASS
MAIN_BRANCH=UNCHANGED
REGISTRY=UNCHANGED_ONE_CONSUMED_RESERVED_ENTRY
AUTOMATIC_RERUN=PROHIBITED
COUNTED_RAG_EXECUTION=NOT_AUTHORIZED
CANDIDATE_V7_PROMOTION=NOT_AUTHORIZED
```

## Authoritative identities

| Item | Value |
|---|---|
| Main OID | `b934c7bd84bfbc35563f3681712c4d5bd8478196` |
| Main tree | `97a35b2861c4408bdad3fcc16770fcaaa7843493` |
| Preserved Epoch-1 OID | `cc2c3c9dccc1de11127d3dd9cd62e5d2c1b01d7c` |
| Authoritative Epoch-2 OID | `1f47c560e735ad41619da72dfcf916f822cfb2ef` |
| Epoch-2 tree | `55622c6b935a637c9b7529ae39e3d9ef244c1187` |
| Registry head | `a17b91ebdc20136d18e6477127867a3d191e505ca6ec725a9dbcd8a8866769d4` |
| Registry SHA-256 | `f93e847e3b8d5aaa44bb117333f176778080f69dddf1bf27921621450d0de309` |
| Epoch-2 integrity ruleset | `20181456` |
| Epoch-2 writer ruleset | `20181457` |
| Accepted evidence SHA-256 | `dd255eb2a03ab6da71f727417419f38fd07009ec038e05a285b0987b3b31f406` |

## Governing conclusion

Epoch 1 is not deleted, force-pushed, corrected in place, or treated as valid. Its defect and evidence remain part of the audit history.

Epoch 2 is an additive recovery from the original approved design parent. The remote commit is one commit ahead of that parent and adds only the anchor and detached-signature paths. The complete parent tree is preserved.

The single registry reservation remains consumed. Epoch 2 did not append or reuse the registry reservation; it witnesses the existing authoritative registry state through the signed recovery adjudication and genesis transition.
