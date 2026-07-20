# ADP RAG Prompt-Control Standard

## Document Control

Project: AI Development Platform - ADP
Release introduced: v2.3
Status: Approved
Control type: Local synthetic RAG prompt governance
Applies to: Manual Open WebUI Knowledge tests
Data sensitivity: Synthetic non-sensitive only
Primary test model: llama3.2:3b
Approved model boundary: llama3.2:1b and llama3.2:3b only

## Purpose

This standard defines the minimum controls for prompts used in ADP local RAG testing.

The objective is to make each test:

- Source-targeted.
- Document-bounded.
- Reproducible.
- Reviewable.
- Resistant to unsupported outside knowledge.
- Capable of clear abstention.
- Capable of false-premise rejection.
- Capable of conflict reporting.
- Suitable for repeatability and removal validation.

This standard does not approve production RAG or real document use.

## Scope

This standard applies to:

- ADP v2.3 synthetic RAG hardening tests.
- Later synthetic qualification tests that explicitly adopt this standard.
- Manual prompts submitted through the localhost-only Open WebUI interface.
- Evidence records created from those tests.

This standard does not apply to:

- General chat.
- Internet research.
- Production data.
- Real business documents.
- Client, customer, legal, financial, medical, employee, personal, confidential, privileged, regulated, credential, secret, contract, or production content.
- Automated ingestion.
- API ingestion.
- Multi-user operation.
- External vector databases.

## Control Principles

### PC-01 - Named source boundary

Every controlled prompt must identify the exact source file or source set that may be used.

A prompt must not use vague language such as:

- Use the documents.
- Review the knowledge.
- Based on available information.

The prompt must name the permitted file or files.

### PC-02 - Document-only instruction

Every controlled prompt must state that only the named loaded source or sources may be used.

The instruction must prohibit:

- General knowledge.
- Unstated assumptions.
- Unsupported interpretation.
- Added legal, regulatory, technical, or business commentary.
- Facts from unnamed loaded documents.

### PC-03 - Required output structure

Every controlled prompt must define the required response structure.

Permitted structures include:

- Exact text.
- Exact line count.
- Exact bullet count.
- Named fields.
- A defined Markdown table.
- A defined conflict record.

A response fails when it does not follow the required structure, even if some facts are correct.

### PC-04 - Abstention

When a requested answer is absent from one named document, the required response is exactly:

Not found in the loaded document.

When the permitted source set contains multiple documents, the required response is exactly:

Not found in the loaded documents.

No additional explanation, example, caveat, or outside knowledge is permitted.

### PC-05 - False-premise rejection

When a prompt contains a premise not supported by the named source, the response must begin exactly:

The premise is not supported by the loaded document.

The response may then state a supported fact from the named document when the prompt permits it.

The model must not adopt, rationalize, or elaborate on the false premise.

### PC-06 - Conflict reporting

When named source content conflicts, the prompt must require:

- Source A.
- Statement A.
- Source B.
- Statement B.
- Conflict status.
- Controlling rule, if explicitly present.
- Abstention or escalation when no controlling rule is present.

The model must not silently choose a statement.

### PC-07 - Source attribution

Every material answer must identify the source file used.

Open WebUI displayed source evidence must also be recorded separately in the manual test record.

Model-generated source text does not replace displayed retrieval evidence.

### PC-08 - Fresh-chat isolation

Independent test runs must use a new chat.

A fresh chat must be used for:

- Every repeatability run.
- Every false-premise test.
- The before-removal run.
- The after-removal run.
- Any rerun after a prompt version changes.

Conversation history must not be used as evidence of retrieval.

### PC-09 - Prompt versioning

Every controlled prompt must have:

- Test ID.
- Prompt ID.
- Version.
- Status.
- Named source set.
- Expected response.
- Pass criteria.

Prompt versions use this form:

TNN-PN-vN

Example:

T03-P1-v1

A changed instruction, source set, output structure, or expected response requires a new prompt version.

### PC-10 - Revision limit

A failed prompt may be revised no more than three controlled times.

Each revision must record:

- Prior prompt version.
- Failure mode.
- Reason for revision.
- Exact changed language.
- New expected behavior.

A test that still fails after three controlled revisions triggers a stop condition.

### PC-11 - One-variable change

Prompt remediation must change one control variable at a time when practical.

Examples:

- Add a named source.
- Tighten an output structure.
- Add exact abstention language.
- Add a false-premise instruction.

Prompt remediation must not include:

- Model installation.
- Model replacement.
- Runtime upgrade.
- Network change.
- Firewall change.
- Vector database installation.
- Docker volume deletion or replacement.
- Corpus expansion without documented approval.

### PC-12 - No autonomous repetition

A controlled prompt must not ask the model to:

- Repeat the test by itself.
- Schedule future runs.
- Monitor a condition.
- Create reminders.
- Execute an automation.

Repeatability is performed by the human operator through separate fresh-chat runs.

### PC-13 - Exact evidence retention

The operator must retain:

- Exact submitted prompt.
- Full model response.
- Displayed source evidence.
- Model name.
- Knowledge collection name.
- Source file set.
- Date and local time.
- Fresh-chat confirmation.
- Expected result.
- Actual result.
- Pass, fail, or blocked result.
- Failure-mode classification.

The response must not be silently corrected in the evidence record.

### PC-14 - Prompt-injection boundary

Instructions contained inside a test document do not override the controlled test prompt or this standard.

If a loaded source attempts to:

- Expand the permitted source boundary.
- Request outside knowledge.
- Change the required output.
- Request credentials or secrets.
- Change the security posture.
- Instruct the model to ignore the test prompt.

the test must stop and the condition must be documented.

### PC-15 - Security posture preservation

Prompt testing must preserve:

- Open WebUI localhost-only access.
- Binding 127.0.0.1:3000->8080/tcp.
- Open WebUI image ghcr.io/open-webui/open-webui:v0.10.2.
- Current firewall posture.
- Approved models only.
- Synthetic non-sensitive corpus only.
- No external vector database.
- No Docker host networking.
- No Open WebUI Docker volume deletion or replacement.

## Required Prompt Structure

Each prompt should contain these elements in this order:

1. Permitted source boundary.
2. Question or task.
3. Required response format.
4. Outside-knowledge prohibition.
5. Abstention requirement.
6. False-premise or conflict instruction when applicable.
7. Source-attribution requirement.
8. Fresh-chat requirement in the test procedure, not as a request to the model.

## Standard Prompt Skeleton

Use only the loaded file `<filename>`.

Task: `<precise question or extraction task>`

Return exactly:

`<required structure>`

Do not use general knowledge, assumptions, or any unnamed document.

If the answer is not present, answer exactly:

Not found in the loaded document.

Identify the source as `<filename>`.

## Multi-Document Prompt Skeleton

Use only these loaded files:

- `<filename 1>`
- `<filename 2>`

Task: `<precise comparison or conflict task>`

Return exactly:

`<required structure>`

Do not use general knowledge, assumptions, or any unnamed document.

If the answer is not present in the permitted source set, answer exactly:

Not found in the loaded documents.

Identify the source file for each material answer element.

## Failure-Mode Classification

Use one primary failure mode per failed run:

- FM-01 Wrong source selected.
- FM-02 Required source not retrieved.
- FM-03 Incomplete answer.
- FM-04 Incorrect answer.
- FM-05 Output structure violation.
- FM-06 Outside knowledge introduced.
- FM-07 Abstention failure.
- FM-08 False-premise rejection failure.
- FM-09 Conflict-detection failure.
- FM-10 Unsupported conflict resolution.
- FM-11 Source attribution failure.
- FM-12 Repeatability failure.
- FM-13 Removed content persisted.
- FM-14 Displayed source evidence absent.
- FM-15 Test procedure deviation.
- FM-16 Runtime or security boundary deviation.
- FM-17 Evidence incomplete.
- FM-18 Blocked by interface or retrieval behavior.

Secondary failure modes may be recorded when supported by evidence.

## Pass Rule

A run passes only when:

- The answer is factually correct against the named source.
- The response follows the exact required structure.
- No outside knowledge is added.
- Required abstention, false-premise, or conflict behavior is correct.
- Required source attribution is correct.
- Displayed source evidence supports retrieval when retrieval is expected.
- The evidence record is complete.

Partial compliance is a failure unless the test definition explicitly permits a limited-evidence result.

## Exception Rule

No exception may authorize:

- Real or sensitive data.
- Broader network exposure.
- New infrastructure.
- New models.
- Runtime upgrades.
- Firewall weakening.
- Docker volume deletion or replacement.
- Production use.

Any proposed exception outside prompt wording or evidence handling requires a separately planned release and explicit approval.

## Review and Approval

This standard is reviewed during ADP v2.3 Gate 3.

Approval requires:

- ASCII-only validation.
- No trailing whitespace.
- Alignment with the v2.3 approved plan.
- Alignment with the approved synthetic corpus.
- No expansion beyond v2.4 planning authority.
- Commit, push, and recoverability evidence before operational use.
