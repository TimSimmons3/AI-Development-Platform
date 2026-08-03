# ADP v2.4 Candidate-v7 Terminal Failure and Security Containment Closeout

## Decision

```text
CANDIDATE_V7_STATUS=TERMINAL_FAILED_CLOSED
COUNTED_INFERENCE_COUNT=0
CANDIDATE_V7_RETRY_AUTHORIZED=FALSE
R2_OPERATOR_REUSE=PROHIBITED
R1_CR2_WRAPPER_REUSE=PROHIBITED
R1_R1_CR1_R1_CR2_CLOSEOUT_PACKAGES_REUSE=PROHIBITED
TEMPORARY_API_KEY=REVOKED
EXPOSED_ADMINISTRATOR_JWT=INVALIDATED
PLAINTEXT_JWT_COPIES=0
OPENWEBUI_SECRET_PERSISTENCE=HARDENED
```

## Terminal governance state

```text
REGISTRY_SHA256=b554e68f3dd814cd68e4284872c70ef1bcb558164cbd63c0b6d0f384695fc79c
REGISTRY_ENTRY_COUNT=2
TERMINAL_EVENT=FAILED
TERMINAL_ENTRY_SHA256=1455725cf527378565c684f1580249822a160a08e90aa24748399e6d259f43d5
WITNESS_OID=298fec40395f923da83e28fb311c5d3faca0c3b0
PRE_CLOSEOUT_REPOSITORY_HEAD=228bec488313c901519e0a1377ffb7a370c6b9f5
```

## Security containment

Open WebUI remains pinned to v0.10.2 and bound to `127.0.0.1:3000`. A host-managed secret is mounted read-only at `/app/backend/.webui_secret_key`. The exposed administrator JWT no longer validates against the active runtime secret. The plaintext token file was deleted and the exact-token scan returned zero matches.

The original screenshot remains restricted evidence and is referenced only by SHA-256:

```text
79ae7fd23a670518574251dde332379726abf3ba4860c33e44a8e85bb05efb44
```

## Administrative completion evidence

This repository record is the signed closeout-publication content. The transaction's external evidence set records the exact commit, recovery bundle, Timeshift snapshot identifier, exact-SHA push receipt, and final seven-item closure reconciliation. Those post-commit facts are not asserted prospectively inside this commit.

## Permanent remediation boundary

Candidate-v7 closeout does not certify counted-RAG for reuse. Exact R2 source-level RCA and Candidate-v8 remediation remain separate blocked work.
