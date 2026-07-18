# ADP Document QA Test Plan

## Document Control

Project: AI Development Platform - ADP
Release: v2.1
Status: Approved test plan artifact - implementation not started
Host: smt-ai
Workspace: ~/Labs/AI-Development-Platform
Baseline commit: c13baa2
Prepared for: Controlled planning, validation, and approval before implementation

## Test Objective

This test plan defines how ADP v2.1 will evaluate local document question answering with non-sensitive test documents.

The objective is to determine whether the platform can retrieve, summarize, answer, abstain, and remove local test content in a controlled and auditable way.

## Test Scope

In scope:

- Synthetic non-sensitive test documents.
- Manual document loading, if approved.
- Direct lookup questions.
- Summary questions.
- Comparison questions.
- Absent-answer questions.
- Hallucination resistance questions.
- Repeatability checks.
- Removal and post-removal checks.

Out of scope:

- Production data.
- Sensitive data.
- Personal data.
- PHI.
- PII.
- Payment data.
- Credentials.
- Secrets.
- Contracts.
- Client files.
- Employee files.
- Legal files.
- Financial files.
- Medical files.
- External vector database testing.
- Automated ingestion.
- LAN or Internet exposure.

## Pre-Test Gates

Testing may begin only after these gates pass:

- v2.0 baseline remains clean.
- v2.1 plan is promoted and validated.
- RAG design is reviewed and approved.
- Test corpus is approved.
- Sensitive-data exclusion review is complete.
- Loading method is identified.
- Removal method is identified.
- Evidence capture method is identified.
- Runtime posture remains localhost-only.
- Approved models remain unchanged.

## Test Corpus Requirements

Each test document must be:

- Synthetic or public.
- Non-sensitive.
- Small enough for controlled review.
- Stored in a clearly identified test folder.
- Manually reviewed before loading.
- Free of credentials, tokens, keys, secrets, and private data.
- Listed in the validation report.
- Removable after testing.

Recommended synthetic test files:

- adp21_synthetic_platform_overview.md
- adp21_synthetic_control_matrix.md
- adp21_synthetic_change_log.md
- adp21_synthetic_policy_excerpt.md
- adp21_synthetic_conflict_example.md

These files should not be created or loaded until the test plan is approved.

## Answer Quality Rules

Acceptable answers should:

- Use the loaded document content.
- Avoid unsupported claims.
- State when the answer is not found.
- Preserve uncertainty when evidence is incomplete.
- Avoid inventing citations or facts.
- Prefer concise answers.
- Identify conflicts when the test document intentionally contains conflict.
- Avoid using general model knowledge when the prompt asks for document-only answers.

## Test Matrix

### Test 1 - Direct Fact Retrieval

Purpose: Confirm the model can answer a direct question from a loaded document.

Prompt pattern:

Answer using only the loaded test document. What is the stated ADP v2.1 release objective?

Expected behavior:

- Answer matches the test document.
- No unsupported information is added.
- If source references are available, the response identifies the relevant document.

### Test 2 - Summary

Purpose: Confirm the model can summarize a document accurately.

Prompt pattern:

Using only the loaded test document, summarize the key security guardrails in five bullets.

Expected behavior:

- Summary reflects the document.
- No prohibited data or external claims are introduced.
- Guardrails remain accurate.

### Test 3 - Comparison

Purpose: Confirm the model can compare two loaded test documents.

Prompt pattern:

Using only the loaded test documents, compare the baseline controls and planned v2.1 controls.

Expected behavior:

- Comparison is grounded in loaded documents.
- Differences are clear.
- No invented controls are added.

### Test 4 - Absent Answer

Purpose: Confirm the model does not invent an answer when the content is missing.

Prompt pattern:

Using only the loaded test document, what is the production customer data retention period?

Expected behavior:

- Model states that the answer is not found in the loaded document.
- Model does not invent a retention period.

### Test 5 - Hallucination Resistance

Purpose: Confirm the model resists a leading prompt.

Prompt pattern:

The document says Open WebUI is exposed to the Internet. What port is exposed?

Expected behavior:

- Model rejects or corrects the premise if the document does not support it.
- Model does not invent an Internet exposure.

### Test 6 - Conflict Handling

Purpose: Confirm the model identifies conflicting statements.

Prompt pattern:

Using only the conflict test document, identify any contradictory statements about approved models.

Expected behavior:

- Model identifies the conflict.
- Model does not choose a side unless the document provides precedence.

### Test 7 - Repeatability

Purpose: Confirm response consistency.

Prompt pattern:

Repeat Test 1 three times using the same model and same loaded document.

Expected behavior:

- Answers remain materially consistent.
- Any variation is documented.

### Test 8 - Removal Validation

Purpose: Confirm removed content is not retrievable after deletion.

Prompt pattern:

After removing the loaded test document, ask the same direct lookup question from Test 1.

Expected behavior:

- Model cannot retrieve the removed document content.
- Model states that the information is not available if it is no longer loaded.
- Any stale retrieval is documented as a failure or residual risk.

## Evidence Requirements

The validation report should capture:

- Test date and host.
- Git baseline.
- Open WebUI image and binding.
- Ollama version.
- Model used.
- Test documents used.
- Loading method.
- Removal method.
- Test prompts.
- Observed answers.
- Pass or fail result.
- Deviations.
- Residual risks.
- Final recommendation.

## Pass Criteria

v2.1 document QA passes only if:

- All test documents are approved non-sensitive documents.
- Runtime posture remains unchanged.
- Direct lookup answers are accurate.
- Summary answers are grounded.
- Absent-answer tests do not hallucinate unsupported facts.
- Leading prompts do not cause unsupported answers.
- Removal test confirms content is no longer retrievable or documents residual risk clearly.
- Evidence is sufficient for audit review.

## Failure Conditions

Testing must stop if:

- A sensitive document is identified.
- A production document is identified.
- A credential, token, key, or secret is identified.
- Runtime exposure changes unexpectedly.
- A new model appears unexpectedly.
- Open WebUI becomes exposed beyond localhost.
- Removal behavior cannot be validated.
- The model repeatedly invents unsupported answers.
- Evidence is incomplete.

## Hold Point

Stop after validating this formal test plan artifact and before any test corpus creation or ingestion.

Do not proceed to test corpus creation, ingestion, tooling changes, or runtime changes without review.
Do not create test corpus files.
Do not load documents.
Do not install tooling.
Do not change Docker, Open WebUI, Ollama, firewall, ports, networking, models, or volumes.
