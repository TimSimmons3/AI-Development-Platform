# ADP v2.3.1 Entry and Runtime Baseline Record

## 1. Document Control

- Project: AI Development Platform
- Release: ADP v2.3.1
- Release title: RAG Retrieval-Pipeline and Model-Behavior Diagnostic
- Record type: Entry and Runtime Baseline Record
- Status: Approved
- Planned canonical path:
  - `docs/ADP-v2.3.1-Entry-and-Runtime-Baseline-Record.md`
- Governing plan:
  - `docs/ADP-v2.3.1-RAG-Retrieval-Pipeline-and-Model-Behavior-Diagnostic-Plan.md`
- Governing plan commit:
  - `a4c910c Add ADP v2.3.1 diagnostic release plan`
- Gate assessed:
  - Gate B - Repository and Runtime Baseline
- Gate decision:
  - PASS WITH RECORDED DIAGNOSTIC FINDINGS
- ADP v2.4 status:
  - BLOCKED
- Optional model comparison:
  - NOT AUTHORIZED

## 2. Purpose

This record preserves the evidence used to determine whether ADP v2.3.1 may proceed from read-only entry validation to controlled preparation of the minimal synthetic diagnostic data and frozen prompt.

This record does not authorize:

- Creation of an Open WebUI Knowledge collection
- Upload of a diagnostic file
- Execution of a diagnostic prompt
- Model or context configuration changes
- Open WebUI or Ollama upgrades
- Docker or firewall changes
- Use of real or sensitive data
- ADP v2.4 work

## 3. Repository Baseline

Validated state:

- Repository: `~/Labs/AI-Development-Platform`
- Branch: `main`
- `HEAD`: `a4c910c`
- Local `main`: `a4c910c`
- `origin/main`: `a4c910c`
- Latest commit:
  - `a4c910c Add ADP v2.3.1 diagnostic release plan`
- Working tree: clean

Decision:

- PASS

## 4. Approved Plan Integrity

Canonical plan:

- `docs/ADP-v2.3.1-RAG-Retrieval-Pipeline-and-Model-Behavior-Diagnostic-Plan.md`

SHA-256:

- `130a79ba28ef428e033b7b913f9545395d20d72511a8fbe68e6edc3c370943f7`

Validation:

- Source-to-canonical checksum match: PASS
- ASCII-only validation: PASS
- Markdown structure validation: PASS
- Trailing-whitespace validation: PASS
- Tab validation: PASS

## 5. Open WebUI Baseline

Validated state:

- Container: `open-webui`
- Image: `ghcr.io/open-webui/open-webui:v0.10.2`
- Port binding: `127.0.0.1:3000->8080/tcp`
- Status: healthy
- Restart policy: `always`
- Persistent data mount:
  - Type: volume
  - Name: `open-webui`
  - Destination: `/app/backend/data`
- Docker network mode: `open-webui_default`
- Ollama connection:
  - `http://host.docker.internal:11434`

Decision:

- PASS

## 6. Ollama Baseline

Validated state:

- Ollama version: `0.30.11`
- Service state: active and running
- Service command:
  - `/usr/local/bin/ollama serve`
- Listener configuration:
  - `OLLAMA_HOST=0.0.0.0:11434`
- Approved installed models:
  - `llama3.2:1b`
  - `llama3.2:3b`
- No additional model was observed.

Model metadata reported:

- `llama3.2:3b`
  - Parameters: 3.2B
  - Advertised context length: 131072
  - Quantization: Q4_K_M
- `llama3.2:1b`
  - Parameters: 1.2B
  - Advertised context length: 131072
  - Quantization: Q8_0

The advertised model context length is model metadata and is not the active served context for the observed runtime.

Decision:

- PASS WITH FINDING F-231-B-01

## 7. Network Boundary

### 7.1 Open WebUI

Open WebUI was bound to:

- `127.0.0.1:3000`

A valid remote test from a separate macOS host returned:

- HTTP code: `000`
- Curl exit: `28`
- Result: timeout

Decision:

- PASS

### 7.2 Ollama

Ollama listened on:

- `*:11434`

UFW state:

- Active
- Default incoming: deny
- Default routed: deny
- Port 11434 allowed only for the approved local Docker path:
  - `docker0`
  - `172.18.0.0/16`

A valid remote test from a separate macOS host returned:

- HTTP code: `000`
- Curl exit: `28`
- Result: timeout

Security classification:

- Open WebUI is loopback-bound.
- Ollama is wildcard-bound for the approved container-to-host path.
- UFW blocks physical-LAN access and is a required compensating control.

Residual risk:

- The Ollama boundary depends on UFW remaining active and correctly scoped.

Decision:

- PASS WITH DOCUMENTED RESIDUAL RISK

## 8. Timeshift Baseline

Validated snapshot:

- Identifier: `2026-07-20_11-32-48`
- Actual description:
  - `ADP-v2.3-reg-hardening-t01-failure-closeout`

Decision:

- PASS

## 9. Prior Knowledge Collection State

Prior collection:

- `ADP-v2.3-synthetic-rag-hardening`

Evidence:

- Manual operator review confirmed that the collection was absent.
- Open WebUI logs recorded a successful Knowledge deletion request followed by a search refresh.
- No later authorized Knowledge creation or modification was evidenced during Gate B.

Classification:

- Prior administrative cleanup remains confirmed.
- This does not retroactively convert the cleanup into a successful T09 removal-validation test.

Decision:

- PASS

## 10. Read-Only Log Severity Review

### 10.1 Open WebUI

Targeted severity scan:

- Error and warning count: `0`

Some model-profile image requests returned `401` or `405`. They were not correlated with chat or retrieval failure and were not a Gate B blocker.

Decision:

- PASS

### 10.2 Ollama

Targeted severity scan:

- Error count: `0`
- Warning count: `7`
- All seven warnings reported prompt truncation.

Decision:

- PASS WITH FINDING F-231-B-01

## 11. Finding F-231-B-01 - Prior Prompt Truncation

### 11.1 Observed Events

| Local timestamp | Original prompt tokens | Applied input limit | Resulting prompt tokens |
|---|---:|---:|---:|
| 2026-07-20 08:41:43 CDT | 5210 | 2050 | 2050 |
| 2026-07-20 08:49:47 CDT | 5250 | 2050 | 2050 |
| 2026-07-20 09:03:43 CDT | 5352 | 2050 | 2050 |
| 2026-07-20 09:14:59 CDT | 5332 | 2050 | 2050 |
| 2026-07-20 09:22:26 CDT | 5329 | 2050 | 2050 |
| 2026-07-20 09:31:31 CDT | 5354 | 2050 | 2050 |
| 2026-07-20 13:36:01 CDT | 4583 | 2050 | 2050 |

Each event used:

- `keep=4`
- `new=2050`

The surrounding Ollama records showed:

- Successful `POST "/api/chat"` requests
- Prompt-cache limits of 4096 tokens
- No service crash
- No inference error

### 11.2 Correlation to T01 Activity

The first six events occurred between 08:41 and 09:31 CDT.

The v2.3 T01 evidence record contains:

- One invalid preliminary submission
- Five scored T01 runs

The count and sequence strongly align with those six events.

Because exact per-run timestamps were not preserved in the T01 record, a one-to-one mapping is:

- Strongly supported
- Not conclusively proven

The seventh event at 13:36 CDT occurred after the logged Knowledge deletion and is not attributed to the T01 execution set.

### 11.3 Retrieval Correlation

Open WebUI logs recorded chat-completion and retrieval activity at corresponding timestamps after accounting for the observed five-hour UTC-to-CDT offset.

Retrieved candidates included combinations of:

- `adp22_synthetic_platform_overview.md`
- `adp22_synthetic_change_log.md`
- `adp22_synthetic_conflict_example.md`
- `adp22_synthetic_control_matrix.md`

The target overview file was often present, but competing files were also included.

Bounded conclusion:

1. Retrieval was active.
2. Multi-file context was often supplied.
3. The combined prompt exceeded the active input budget.
4. Ollama truncated the prompt before inference.
5. The retained prompt was not the complete prompt assembled by Open WebUI.

The evidence does not show which exact instruction or source segment was discarded in each run.

### 11.4 Diagnostic Significance

Prompt truncation is a material contributor candidate for:

- Loss of grounding instructions
- Loss of exact-format instructions
- Loss of retrieved source content
- Wrong-passage effects
- Unsupported outside-knowledge responses
- Non-repeatable behavior as retrieved context changed

Prompt truncation does not by itself explain:

- The unrelated automation or iCalendar response
- All source-evidence display inconsistencies
- Whether model behavior remains unstable under a non-truncated input

## 12. Active Context Interpretation

Observed runtime evidence:

- Prompt-cache context limit: 4096 tokens
- Applied input limit: 2050 tokens
- Model metadata context length: 131072 tokens

The exact internal allocation that produced the 2050-token input limit was not directly exposed.

The 2050-token limit is consistent with a 4096-token served context with a substantial portion reserved for output and runtime overhead. This is an inference, not a directly observed configuration value.

No context-size or output-reservation setting shall be changed in v2.3.1 without a documented plan amendment.

## 13. Gate B Decision

Gate B is:

- PASS WITH RECORDED DIAGNOSTIC FINDINGS

Pass basis:

- Repository synchronized and clean
- Approved plan present and validated
- Approved Open WebUI image and binding intact
- Approved Ollama version and models intact
- Effective physical-LAN blocking validated
- Timeshift baseline confirmed
- Prior collection absence confirmed
- No Open WebUI severity event identified
- Ollama truncation condition characterized and bounded
- No prohibited drift identified

## 14. Controls Carried Forward

1. Use one minimal synthetic file.
2. Use one unambiguous target fact.
3. Use unique synthetic identifiers.
4. Keep the source and prompt substantially below 2050 tokens.
5. Use a fresh chat for every counted run.
6. Verify Knowledge attachment state before every run.
7. Capture exact prompt, full response, displayed source file, and displayed source passage.
8. Capture a bounded post-run truncation-log window.
9. A counted run fails or is inconclusive if a new truncation warning is generated.
10. Do not change context size, output reservation, model, Open WebUI, Ollama, Docker networking, or firewall configuration.
11. Do not use the five-file corpus until the single-file Gate C block passes.
12. Do not authorize optional model comparison.

## 15. Gate C Entry Boundary

Gate B passage authorizes preparation only of:

- The synthetic diagnostic data design
- One minimal synthetic diagnostic file
- The frozen direct-retrieval prompt
- The diagnostic test-record structure
- The controlled Knowledge-attachment evidence procedure

Before any Knowledge collection is created or any prompt is run:

- Those artifacts must be reviewed and approved.
- Canonical copies must be committed and pushed.
- Git synchronization and a clean working tree must be confirmed.
- A final pre-runtime hold point must be recorded.

## 16. Privacy and Evidence Handling

Raw logs contained internal account and object identifiers. This record excludes those identifiers and retains only evidence necessary for auditability.

## 17. Final Hold Point

Gate B is closed as PASS WITH RECORDED DIAGNOSTIC FINDINGS.

No Knowledge collection, upload, prompt execution, model comparison, configuration change, or ADP v2.4 work is authorized by this record.

The next authorized action is preparation and approval of the minimal Gate C diagnostic artifacts outside the repository.
