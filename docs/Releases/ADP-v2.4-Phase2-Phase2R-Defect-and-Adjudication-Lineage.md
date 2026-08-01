# 04 - Defect and Adjudication Lineage

## Epoch 1

CR6 completed its authorized transaction but constructed a root tree containing only two files. Because its parent was the full main tree, the commit diff removed all other parent paths. The transaction was preserved and not rewritten.

Disposition:

- Epoch-1 branch preserved
- Epoch-1 receipt preserved
- Registry preserved
- No force push
- No branch deletion
- No registry append or truncation
- Additive recovery required

## Phase2R pre-mutation package failures

CR1, CR2 and CR3 were pre-mutation failures or withheld candidates. None created an Epoch-2 ruleset or branch and none consumed the recovery authorization.

CR4 is the authoritative recovery implementation.

## Epoch 2

CR4 created two Epoch-2-only rulesets, collected fresh pre-creation evidence, created a signed parent-tree-preserving witness commit, pushed once, created a signed receipt and passed the frozen full-history verifier.

The defect lineage is closed for the witness-tree construction issue. Epoch 1 remains historical evidence and Epoch 2 is the valid witness epoch.
