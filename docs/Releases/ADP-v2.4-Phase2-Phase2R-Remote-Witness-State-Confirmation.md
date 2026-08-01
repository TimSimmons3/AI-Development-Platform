# 03 - Remote Witness State Confirmation

## Epoch-2 branch

Branch:

`adp-v2.4-candidate-v7-registry-head-epoch-2`

Head:

`1f47c560e735ad41619da72dfcf916f822cfb2ef`

Parent:

`b934c7bd84bfbc35563f3681712c4d5bd8478196`

Commit relationship:

```text
AHEAD_BY=1
BEHIND_BY=0
TOTAL_COMMITS=1
```

## Changed paths

Exactly two paths were added:

1. `control/ADP-v2.4/candidate-v7/registry-head-anchor.json`
2. `control/ADP-v2.4/candidate-v7/registry-head-anchor.json.sig`

No unrelated file was removed, changed, or renamed.

## Remote content

The remote anchor and signature bytes match the accepted Epoch-2 evidence package. The anchor binds:

- Epoch number 2
- Preserved Epoch-1 remote head `cc2c3c9dccc1de11127d3dd9cd62e5d2c1b01d7c`
- Design parent `b934c7bd84bfbc35563f3681712c4d5bd8478196`
- Unchanged registry SHA-256 and registry head
- Recovery adjudication, failure record, genesis and readiness hashes
- The approved signer fingerprint and execution namespace
