# 02 - Independent Evidence Reconciliation

## Package-level reconciliation

| Test | Result |
|---|---|
| External ZIP checksum | PASS |
| ZIP CRC | PASS |
| ZIP entries | 109 |
| Unsafe paths | 0 |
| Duplicate paths | 0 |
| Symbolic links | 0 |
| ZIP modes | 109 at `0600` |
| Manifest-controlled files | 107 |
| Missing files | 0 |
| Extra controlled files | 0 |
| Hash mismatches | 0 |
| Size mismatches | 0 |
| Manifest sidecar | PASS |

## Independent control testing

`audit/independent-evidence-audit.csv` contains 829 controls.

```text
PASS=829
FAIL=0
```

The audit independently checked:

- Six raw GitHub evidence collections
- Collection-wide identifiers, unique envelope identifiers and contiguous sequence numbers
- Raw body Base64 decoding and body SHA-256 values
- API URLs, status codes and package-manifest bindings
- Initial and final pre-mutation state equality
- Main repository cleanliness and unchanged OID/tree before and after recovery
- Registry and preexisting control-state immutability
- Recovery authorization expiration at the first mutation
- Exactly two ruleset creations with no automatic deletion or retry
- Branch absence and prospective effective rules before branch creation
- Readiness freshness
- Adjudication, authorization, binding, readiness, genesis, anchor and receipt hash chains
- Seven detached Ed25519 SSHSIG signatures
- Exact two-path commit construction and parent-tree preservation
- Post-push and current-state branch/ruleset evidence
- Receipt and evidence-copy hashes
- Frozen full-history verifier PASS
- Secret scan and final gate

## Signature result

All seven detached signatures validate against the registered Ed25519 public key and their required namespaces:

- `adp-v2.4-candidate-v7-recovery`: 3
- `adp-v2.4-candidate-v7-start-gate`: 2
- `adp-v2.4-candidate-v7-execution`: 2

The evidence also records a PASS for the Git SSH commit signature and the frozen full-history verifier.
