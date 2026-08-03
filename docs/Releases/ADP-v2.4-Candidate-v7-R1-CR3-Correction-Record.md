# ADP v2.4 Candidate-v7 Closeout Package R1-CR3 Correction Record

## Superseded package

```text
PACKAGE=ADP-v2.4-Candidate-v7-One-Pass-Containment-and-Closeout-Transaction-Package-R1-CR2.zip
SHA256=e2fad3e9aac6eabe78bc7873b95ebf28070a37f4d484ec2927f675b93112b1be
DISPOSITION=WITHDRAWN_DO_NOT_RERUN
```

## Root cause

R1-CR2 treated a stale local remote-tracking witness as authoritative even though the remote witness and terminal registry were correct. It also classified ordinary OAuth metadata such as scopes, URLs, claims, roles, domains, and provider labels as active credential dependencies through broad substring matching. The exact host-derived preflight fixture proved that every other gate passed.

## Corrective action

R1-CR3 establishes an explicit evidence hierarchy. The terminal registry and authoritative remote witness remain blocking controls; the local remote-tracking witness is recorded as informational derived cache state. The database inventory now uses exact credential-bearing PersistentConfig keys and exact credential leaf names. OAuth metadata is recorded informationally and cannot block rotation.

## Test correction

The exact failed host fixture is hash-bound as a mandatory regression fixture and must pass the actual production preflight evaluator. Negative fixture mutations must fail for remote-witness mismatch, registry mismatch, active credential value, active OAuth session, API key, tool, function, dirty Git state, and database-integrity failure. Stale or absent local witness state and the observed OAuth metadata must remain nonblocking.
