# ADP v2.3.1 Synthetic Diagnostic Data Design

## 1. Document Control

- Project: AI Development Platform
- Release: ADP v2.3.1
- Status: Approved for controlled repository promotion
- Repository baseline represented: `253e9dd`
- Planned canonical path:
  - `docs/ADP-v2.3.1-Synthetic-Diagnostic-Data-Design.md`
- Governing plan commit:
  - `a4c910c Add ADP v2.3.1 diagnostic release plan`
- Gate B record commit:
  - `253e9dd Document ADP v2.3.1 Gate B baseline findings`
- Gate C tests:
  - `V231-R01 Single-File Direct Retrieval`
  - `V231-S01 Displayed-Source Evidence Stability`
- Model:
  - `llama3.2:3b`
- Optional model comparison:
  - NOT AUTHORIZED

## 2. Purpose

Define one minimal synthetic source that permits direct-retrieval and displayed-source evidence to be assessed without introducing real or sensitive data, multi-file competition, prompt-format qualification, or a runtime configuration change.

## 3. Source File

Approved filename:

- `adp231_minimal_direct_retrieval.md`

Planned repository path:

- `test-data/rag/v2.3.1/adp231_minimal_direct_retrieval.md`

SHA-256:

- `ea0288d0d8666438e8cf9ae7dd54e6da8aaa0818f42d15f29bdf7467acf77afc`

The source is intentionally short and contains the five elements required by the approved plan:

1. One unique platform identifier
2. One exact release objective
3. One exact owner-role label
4. One distinct non-target fact
5. One explicit prohibition

## 4. Approved Synthetic Content

Unique platform identifier:

- `NOVA-231-DELTA`

Target fact:

- `The release objective for NOVA-231-DELTA is to verify that one exact synthetic fact can be retrieved from one attached source without adding outside information.`

Owner role:

- `Diagnostic Custodian`

Distinct non-target fact:

- `The archive marker for NOVA-231-DELTA is ORCHID-74.`

Explicit prohibition:

- `Do not describe NOVA-231-DELTA as training machine-learning models or evaluating algorithms.`

## 5. Plan-Consistency Decision

The archive marker and prohibition remain in the first source because Section 13 of the approved plan requires both a distinct non-target fact and an explicit prohibition.

They are not queried during `V231-R01`. Their presence does not add a second file or a second changed runtime variable. They remain available for later approved phases without silently changing the source design.

No plan amendment is required because this design implements, rather than changes, the approved synthetic-data requirements.

## 6. Design Rationale

The source:

- Uses no real names, organizations, systems, clients, or business facts.
- Uses a unique identifier unlikely to be answered from general model knowledge.
- Contains one verbatim target sentence suitable for direct retrieval.
- Contains one distinct non-target fact required by the plan.
- Contains the explicit prohibition required by the plan.
- Contains no dates, reminders, schedules, calendar syntax, credentials, or personal data.
- Is small and manually reviewable.
- Does not by itself prove that the Open WebUI assembled request will avoid truncation.

The controlling prompt-budget evidence is the absence of a new Ollama `truncating input prompt` warning in the exact bounded run window.

## 7. Gate C Test Boundary

The same three fresh-chat runs produce two separately scored results:

- `V231-R01`: whether the exact target sentence is returned without unsupported factual content or unrelated automation output.
- `V231-S01`: whether Open WebUI displays the correct source file and target passage for that response.

Using the same runs avoids changing a variable or executing an unnecessary second prompt block. The three runs are performed as one consolidated runtime packet with automatic continuation after successful runs.

Gate C does not test:

- Exact line count
- Exact labels
- Model-generated filename text
- Citation-list formatting
- Broader multi-file retrieval
- Optional model comparison

Exact output structure remains assigned to `V231-F01` after Gate C.

## 8. Run Acceptance Criteria

### 8.1 V231-R01 PASS

A run passes `V231-R01` only when:

1. The complete target sentence appears verbatim in the response.
2. The response does not contradict the target sentence.
3. The response contains no unsupported factual claim.
4. The response contains no automation, reminder, scheduling, or iCalendar output.

A preface or other formatting deviation is recorded as an observation and does not by itself fail `V231-R01`. Exact formatting is assessed later under `V231-F01`.

### 8.2 V231-S01 PASS

The same run passes `V231-S01` only when:

1. Displayed source evidence is available.
2. The displayed source filename is exactly `adp231_minimal_direct_retrieval.md`.
3. The displayed source passage contains the complete target sentence.
4. Displayed source evidence does not conflict with the answer.

### 8.3 Environment PASS

The run remains countable only when:

1. Fresh-chat and attachment evidence are complete.
2. All controlled variables remain unchanged.
3. No new Ollama prompt-truncation warning appears in the exact run window.
4. Required response, screenshot, and log evidence is complete.

## 9. Gate C Block Decision

Gate C passes only when all three fresh-chat runs satisfy:

- `V231-R01`: PASS
- `V231-S01`: PASS
- Environment and evidence controls: PASS

Any failed counted run prevents Gate C passage. An inconclusive attempt does not count as a pass and must be handled under the approved plan's stop and change-control rules.

## 10. Hold Point

This approved design authorizes controlled repository promotion only.

It does not authorize Knowledge collection creation, file upload, prompt execution, model comparison, configuration change, or ADP v2.4 work.
