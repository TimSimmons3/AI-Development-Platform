# ADP v2.3 RAG Test Prompt Library

## Document Control

Project: AI Development Platform - ADP
Release: v2.3
Status: Approved
Library version: 1.0
Primary test model: llama3.2:3b
Knowledge collection: ADP-v2.3-synthetic-rag-hardening
Corpus: Existing five-file v2.2 synthetic corpus only
Data sensitivity: Synthetic non-sensitive only

## Purpose

This library provides exact prompts, expected responses, and pass criteria for ADP v2.3 RAG hardening.

The prompts are designed to remediate the v2.2 failures while preserving the existing runtime, model, network, and corpus boundaries.

## Preconditions

Before any prompt is run:

- The approved v2.3 plan is committed and pushed.
- The prompt-control standard is approved.
- The manual test record template is approved.
- Open WebUI is healthy and localhost-only.
- Open WebUI remains bound to 127.0.0.1:3000->8080/tcp.
- Open WebUI remains at ghcr.io/open-webui/open-webui:v0.10.2.
- Ollama remains at the validated version.
- Only llama3.2:1b and llama3.2:3b are installed.
- llama3.2:3b is selected for the v2.3 answer-quality tests.
- The Knowledge collection contains exactly the approved five synthetic files.
- Every run starts in a fresh chat.
- No real or sensitive data is used.

## Approved Source Files

- adp22_synthetic_platform_overview.md
- adp22_synthetic_control_matrix.md
- adp22_synthetic_policy_excerpt.md
- adp22_synthetic_change_log.md
- adp22_synthetic_conflict_example.md

## General Execution Rules

- Submit prompts exactly as written.
- Do not add conversational prefaces.
- Do not correct the model during a run.
- Capture the full output.
- Capture displayed source evidence.
- Record a pass, fail, or blocked result.
- Start a new chat before the next independent run.
- Do not revise a prompt until the failed output has been preserved.
- Use no more than three controlled prompt revisions.

## T01 - Direct Retrieval

Prompt ID: T01-P1-v1
Status: Approved
Permitted source: adp22_synthetic_platform_overview.md

### Exact Prompt

Use only the loaded file `adp22_synthetic_platform_overview.md`.

What is the ADP v2.2 release objective?

Return exactly two lines:

Release objective: <the complete release-objective sentence from the document>
Source: adp22_synthetic_platform_overview.md

Do not use general knowledge, assumptions, or any unnamed document.

If the answer is not present, answer exactly:

Not found in the loaded document.

### Expected Response

Release objective: ADP v2.2 validates synthetic local RAG document loading, retrieval, answer quality, hallucination resistance, and removal behavior while preserving the localhost-only ADP security boundary.
Source: adp22_synthetic_platform_overview.md

### Pass Criteria

- Exact release objective.
- Exactly two lines.
- Correct source.
- No caveat.
- No outside knowledge.
- Displayed source evidence includes the named file.

## T02 - Exact Guardrail Extraction

Prompt ID: T02-P1-v1
Status: Approved
Permitted source: adp22_synthetic_platform_overview.md

### Exact Prompt

Use only the `Runtime Boundary` section of the loaded file `adp22_synthetic_platform_overview.md`.

Return exactly five bullets in this order:

1. Access boundary.
2. Approved binding.
3. Docker networking restriction.
4. Firewall restriction.
5. Docker volume restriction.

Use one complete document statement per bullet.

Do not add a heading, introduction, conclusion, caveat, or outside knowledge.

If all five statements are not present, answer exactly:

Not found in the loaded document.

### Expected Response

- Open WebUI must remain localhost-only.
- The approved Open WebUI binding is 127.0.0.1:3000->8080/tcp.
- Docker host networking is prohibited.
- Firewall weakening is prohibited.
- Open WebUI Docker volume deletion or replacement is prohibited.

### Pass Criteria

- Exactly five bullets.
- Correct order.
- Complete source statements.
- No duplicate or invented guardrail.
- No additional text.
- Displayed source evidence includes the named file.

## T03 - Source-Targeted Control Lookup

Prompt ID: T03-P1-v1
Status: Approved
Permitted source: adp22_synthetic_control_matrix.md

### Exact Prompt

Use only the loaded file `adp22_synthetic_control_matrix.md`.

Return control ADP22-CTRL-001 in exactly four lines:

Control ID: <value>
Control name: <value>
Requirement: <value>
Source: adp22_synthetic_control_matrix.md

Do not use general knowledge, assumptions, or any unnamed document.

If the control is not present, answer exactly:

Not found in the loaded document.

### Expected Response

Control ID: ADP22-CTRL-001
Control name: Localhost-only access
Requirement: Open WebUI remains bound to 127.0.0.1:3000->8080/tcp
Source: adp22_synthetic_control_matrix.md

### Pass Criteria

- Correct control ID.
- Correct control name.
- Correct requirement.
- Exactly four lines.
- Correct source.
- No outside knowledge.
- Displayed source evidence includes the named file.

## T04 - Structured Cross-Source Comparison

Prompt ID: T04-P1-v1
Status: Approved
Permitted sources:

- adp22_synthetic_change_log.md
- adp22_synthetic_control_matrix.md

### Exact Prompt

Use only these loaded files:

- `adp22_synthetic_change_log.md`
- `adp22_synthetic_control_matrix.md`

Compare the v2.2 baseline statement with the corresponding control for exactly these three topics:

- Open WebUI access.
- Approved models.
- External vector database.

Return exactly this Markdown table and no other text:

| Topic | Baseline statement | Pilot control requirement | Difference | Sources |
|---|---|---|---|---|
| Open WebUI access | <value> | <value> | <value> | <value> |
| Approved models | <value> | <value> | <value> | <value> |
| External vector database | <value> | <value> | <value> | <value> |

For `Difference`, state only what the control adds beyond the baseline statement.

Do not use general knowledge, assumptions, or any unnamed document.

If a required value is not present, answer exactly:

Not found in the loaded documents.

### Expected Content

The response must preserve these facts:

- Open WebUI baseline: Open WebUI remained localhost-only.
- Open WebUI control: Open WebUI remains bound to 127.0.0.1:3000->8080/tcp.
- Open WebUI difference: the control adds the exact approved binding and validation expectation.
- Model baseline: the approved models remained llama3.2:1b and llama3.2:3b.
- Model control: only llama3.2:1b and llama3.2:3b are approved.
- Model difference: the control converts the baseline observation into an explicit allowlist and validation expectation.
- Vector baseline: no vector database was installed.
- Vector control: no Qdrant, Milvus, pgvector, or other vector database is installed.
- Vector difference: the control names prohibited external vector database types and requires absence of a new service.
- Sources must identify the correct source file for each baseline and control statement.

Exact prose may vary only in the `Difference` cells.

### Pass Criteria

- Exactly one header row, one separator row, and three data rows.
- All baseline and control facts are correct.
- Difference cells add no unsupported facts.
- Correct sources are identified.
- No outside knowledge.
- Displayed source evidence includes both named files.

## T05 - Absent-Answer Behavior

Prompt ID: T05-P1-v1
Status: Approved
Permitted source: adp22_synthetic_policy_excerpt.md

### Exact Prompt

Use only the loaded file `adp22_synthetic_policy_excerpt.md`.

What is the required retention period for ADP v2.2 synthetic test files?

Do not use general knowledge, assumptions, legal requirements, regulatory commentary, or any unnamed document.

If the answer is not present, answer exactly:

Not found in the loaded document.

### Expected Response

Not found in the loaded document.

### Pass Criteria

- Exact response.
- No additional text.
- No GDPR, CCPA, legal, regulatory, or general retention commentary.
- No source citation is required in an abstention response.
- Displayed source evidence may be present or absent, but no unrelated source may support an answer.

## T06 - False-Premise Rejection

Prompt ID: T06-P1-v1
Status: Approved
Permitted source: adp22_synthetic_platform_overview.md

### Exact Prompt

Use only the loaded file `adp22_synthetic_platform_overview.md`.

Explain why Open WebUI is approved for Internet exposure in ADP v2.2.

The question contains a premise that may be unsupported.

If the premise is unsupported, return exactly three lines:

The premise is not supported by the loaded document.
Supported fact: <the complete supported access-boundary sentence>
Source: adp22_synthetic_platform_overview.md

Do not use general knowledge, assumptions, or any unnamed document.

### Expected Response

The premise is not supported by the loaded document.
Supported fact: Open WebUI must remain localhost-only.
Source: adp22_synthetic_platform_overview.md

### Pass Criteria

- Required first line.
- Correct supported fact.
- Exactly three lines.
- Correct source.
- No adoption of the false premise.
- No outside explanation.
- Displayed source evidence includes the named file.

## T07 - Conflict Detection and Controlling Rule

Prompt ID: T07-P1-v1
Status: Approved
Permitted source: adp22_synthetic_conflict_example.md

### Exact Prompt

Use only the loaded file `adp22_synthetic_conflict_example.md`.

Analyze Statement A, Statement B, and Statement C.

Return exactly six lines:

Source A: adp22_synthetic_conflict_example.md - Statement A
Statement A: <complete statement>
Source B: adp22_synthetic_conflict_example.md - Statement B
Statement B: <complete statement>
Conflict status: <state whether Statement A and Statement B conflict>
Controlling rule: <complete Statement C rule>

Do not use general knowledge, assumptions, or any unnamed document.

Do not resolve the conflict beyond the controlling rule stated in Statement C.

If the required statements are not present, answer exactly:

Not found in the loaded document.

### Expected Response

Source A: adp22_synthetic_conflict_example.md - Statement A
Statement A: The approved ADP v2.2 models are llama3.2:1b and llama3.2:3b.
Source B: adp22_synthetic_conflict_example.md - Statement B
Statement B: Only llama3.2:1b is approved for ADP v2.2.
Conflict status: Statement A and Statement B conflict.
Controlling rule: The authoritative source for approved model status is the final validated runtime baseline.

### Pass Criteria

- Exactly six lines.
- Complete Statement A.
- Complete Statement B.
- Conflict identified.
- Complete Statement C.
- No invented resolution.
- Correct source attribution.
- Displayed source evidence includes the named file.

## T08 - Repeatability

Prompt ID: T08-RUN-T03-P1-v1
Status: Approved
Reused prompt: T03-P1-v1
Independent runs required: Three

### Procedure

- Start a new chat.
- Run T03-P1-v1 exactly.
- Record Run 1.
- Start a second new chat.
- Run T03-P1-v1 exactly.
- Record Run 2.
- Start a third new chat.
- Run T03-P1-v1 exactly.
- Record Run 3.
- Do not ask the model to repeat the test.
- Do not reuse a prior conversation.

### Expected Result

All three runs produce the complete T03 expected response and displayed source evidence from `adp22_synthetic_control_matrix.md`.

### Pass Criteria

- Three of three runs pass T03.
- Material facts are identical.
- Required four-line structure is identical.
- No run adds outside knowledge.
- No run uses an unrelated source.
- All three evidence records are complete.

## T09 - Before-and-After Removal Validation

Prompt ID: T09-P1-v1
Status: Approved
Permitted source before removal: adp22_synthetic_change_log.md
Exact same prompt required after removal: Yes

### Exact Prompt

Use only the currently loaded Knowledge sources.

In `adp22_synthetic_change_log.md`, what baseline commit is stated for ADP v2.2?

If the named file and answer are available, return exactly two lines:

Baseline commit: <value>
Source: adp22_synthetic_change_log.md

Do not use general knowledge, assumptions, conversation history, or any unnamed document.

If the named file or answer is unavailable, answer exactly:

Not found in the loaded documents.

### Expected Before-Removal Response

Baseline commit: f6b30ad
Source: adp22_synthetic_change_log.md

### Expected After-Removal Response

Not found in the loaded documents.

### Pass Criteria

Before removal:

- Correct baseline commit.
- Exactly two lines.
- Correct source.
- Displayed source evidence includes the named file.

After removal:

- Exact not-found response.
- No removed source evidence.
- No baseline commit value.
- No use of conversation history.
- Fresh chat confirmed.
- Exact same prompt confirmed.

## Prompt Revision Record

Use this structure for each controlled revision:

- Test ID:
- Prior prompt ID:
- New prompt ID:
- Prior failure mode:
- Reason for revision:
- One variable changed:
- Exact prior language:
- Exact new language:
- Expected effect:
- Approval:
- Date:

## Library Approval Gate

This library may be promoted only when:

- All prompts are ASCII-only.
- No trailing whitespace exists.
- Expected answers match the committed synthetic corpus.
- The test model and Knowledge collection are explicit.
- Repeatability uses separate fresh chats.
- Removal uses one exact prompt before and after.
- No prompt requests automation or future execution.
- No prompt expands the data or runtime boundary.
