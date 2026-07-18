# ADP v2.2 Synthetic Local RAG Pilot and Removal Validation Plan

## Document Control

Project: AI Development Platform - ADP
Release: v2.2
Status: Approved planning artifact - implementation not started
Host: smt-ai
Workspace: ~/Labs/AI-Development-Platform
Repository branch: main
Current baseline: ADP v2.1
Baseline commit: f6b30ad
Prepared for: Controlled synthetic pilot planning, validation, and approval before implementation

## Release Objective

ADP v2.2 will perform a controlled synthetic local RAG pilot and removal validation using only non-sensitive synthetic test documents.

The objective is to prove whether Open WebUI can load approved test documents, retrieve relevant content, answer accurately, resist hallucination, and stop retrieving content after removal while preserving the established localhost-only security posture.

## Baseline

ADP v2.1 closed as a planning, design, and document QA readiness release.

v2.1 established:

- Controlled local content loading and RAG plan.
- Local content loading and RAG design.
- Document QA test plan.
- Sensitive-data exclusion rules.
- Synthetic and public non-sensitive test-data preference.
- External vector database deferral.
- Manual UI-driven loading recommendation.
- Rollback and removal expectations.
- Security and privacy guardrails.

v2.2 begins from commit f6b30ad.

## Release Principles

ADP v2.2 will follow the established workflow:

Plan -> Implement -> Validate -> Document -> Snapshot -> Release

This release must remain small, reversible, and auditable.

No production data, sensitive data, business records, customer files, legal documents, financial records, medical records, personal data, credentials, secrets, contracts, or private records may be used.

## In Scope

The following are in scope after plan approval:

- Create a small synthetic non-sensitive test corpus.
- Validate test corpus files are ASCII-clean.
- Validate test corpus files have no trailing whitespace.
- Review test corpus content for prohibited data.
- Load synthetic test documents through an approved Open WebUI manual document or knowledge path.
- Test direct retrieval.
- Test summary quality.
- Test comparison quality.
- Test absent-answer behavior.
- Test hallucination resistance.
- Test conflict handling.
- Test repeatability.
- Remove loaded test documents.
- Test post-removal retrieval behavior.
- Document evidence and residual risks.
- Preserve the v2.1 security boundary.
- Close with commit, push, and Timeshift snapshot if validation passes.

## Out of Scope

The following are out of scope:

- Production knowledge base deployment.
- Real business document ingestion.
- Client document ingestion.
- Customer document ingestion.
- Legal document ingestion.
- Financial document ingestion.
- Medical document ingestion.
- Employee record ingestion.
- Personal data ingestion.
- PHI ingestion.
- PII ingestion.
- Payment data ingestion.
- Credential or secret ingestion.
- Contract ingestion.
- Private business record ingestion.
- External vector database installation.
- Qdrant installation.
- Milvus installation.
- pgvector installation.
- Automated ingestion pipelines.
- API-driven ingestion.
- Model additions.
- Open WebUI upgrade.
- Ollama upgrade.
- Docker host networking.
- LAN exposure.
- Internet exposure.
- Firewall weakening.
- Open WebUI Docker volume deletion or replacement.

## Planned Artifacts

Planned v2.2 artifacts:

- docs/ADP-v2.2-Synthetic-Local-RAG-Pilot-and-Removal-Validation-Plan.md
- docs/Test-Corpus/v2.2/adp22_synthetic_platform_overview.md
- docs/Test-Corpus/v2.2/adp22_synthetic_control_matrix.md
- docs/Test-Corpus/v2.2/adp22_synthetic_policy_excerpt.md
- docs/Test-Corpus/v2.2/adp22_synthetic_change_log.md
- docs/Test-Corpus/v2.2/adp22_synthetic_conflict_example.md
- docs/ADP-v2.2-RAG-Pilot-Validation-Report.md
- docs/ADP-v2.2-Closeout.md
- docs/ADP-Engineering-Log.md

## Test Corpus Rules

The v2.2 test corpus must be synthetic.

Each file must:

- Be created only for ADP testing.
- Contain no real personal information.
- Contain no real business information.
- Contain no client, customer, employee, legal, financial, medical, credential, secret, contract, or regulated data.
- Be small enough for manual review.
- Be text or Markdown.
- Be ASCII-clean.
- Have no trailing whitespace.
- Be listed in the validation report if loaded.
- Be removable from Open WebUI after testing.

## Proposed Synthetic Files

The proposed test files are:

1. adp22_synthetic_platform_overview.md
- Purpose: Basic direct retrieval and summary testing.
- Contains synthetic release objective, runtime boundary, and approved model statements.

2. adp22_synthetic_control_matrix.md
- Purpose: Control lookup and comparison testing.
- Contains synthetic controls, owners, and validation expectations.

3. adp22_synthetic_policy_excerpt.md
- Purpose: Policy interpretation testing.
- Contains synthetic data classification and sensitive-data exclusion rules.

4. adp22_synthetic_change_log.md
- Purpose: Timeline and change summary testing.
- Contains synthetic change entries and release chronology.

5. adp22_synthetic_conflict_example.md
- Purpose: Conflict detection testing.
- Contains intentionally conflicting statements about approved models and requires the model to identify the conflict.

## Manual Loading Path

v2.2 should use manual Open WebUI loading only.

Before loading, confirm:

- Open WebUI is reachable only from localhost.
- Open WebUI remains bound to 127.0.0.1:3000->8080/tcp.
- No Docker networking change has occurred.
- No firewall weakening has occurred.
- Approved models remain llama3.2:1b and llama3.2:3b.
- Test corpus files pass quality gates.

The loading path should be documented during execution because the actual Open WebUI UI path must be confirmed on the v0.10.2 deployment.

## QA Test Matrix

The v2.2 pilot will test the following:

### Test 1 - Direct Retrieval

Prompt:

Using only the loaded test document, what is the ADP v2.2 release objective?

Expected result:

The answer matches the synthetic platform overview and does not add unsupported claims.

### Test 2 - Guardrail Summary

Prompt:

Using only the loaded test document, summarize the v2.2 security guardrails in five bullets.

Expected result:

The answer summarizes only the loaded document content.

### Test 3 - Control Lookup

Prompt:

Using only the loaded control matrix, which control preserves localhost-only Open WebUI access?

Expected result:

The answer identifies the relevant synthetic control.

### Test 4 - Comparison

Prompt:

Using only the loaded test documents, compare the baseline controls and v2.2 pilot controls.

Expected result:

The answer is grounded in the loaded synthetic files.

### Test 5 - Absent Answer

Prompt:

Using only the loaded test document, what is the production customer data retention period?

Expected result:

The answer states that the loaded document does not define a production customer data retention period.

### Test 6 - Hallucination Resistance

Prompt:

The document says Open WebUI is exposed to the Internet. What port is exposed?

Expected result:

The answer rejects or corrects the false premise if the loaded document says localhost-only.

### Test 7 - Conflict Handling

Prompt:

Using only the loaded conflict example, identify any contradictory statements about approved models.

Expected result:

The answer identifies the contradiction and does not invent a resolution unless the document provides precedence.

### Test 8 - Repeatability

Prompt:

Repeat the direct retrieval test three times using the same model and same loaded document.

Expected result:

The answers remain materially consistent.

### Test 9 - Removal Validation

Prompt:

After removing the loaded test document, ask the same direct retrieval question again.

Expected result:

The model no longer retrieves the removed document content or the residual risk is documented.

## Validation Gates

v2.2 gates:

1. Baseline gate
- Git clean.
- HEAD and origin/main aligned.
- v2.1 closeout artifact present.
- Open WebUI healthy and localhost-only.
- Approved models unchanged.

2. Plan gate
- Plan artifact originated as a /tmp draft before promotion.
- Plan artifact was ASCII-clean before promotion.
- Plan artifact had no trailing whitespace before promotion.
- Plan reviewed before promotion.

3. Corpus gate
- Synthetic test corpus created only after plan approval.
- Corpus files ASCII-clean.
- Corpus files have no trailing whitespace.
- Corpus content contains no prohibited data.

4. Loading gate
- Manual Open WebUI loading path documented.
- Runtime posture unchanged before loading.
- Loaded documents listed.

5. QA gate
- Retrieval tests executed.
- Summary tests executed.
- Absent-answer tests executed.
- Hallucination resistance tests executed.
- Conflict handling tests executed.
- Repeatability test executed.

6. Removal gate
- Loaded documents removed.
- Post-removal retrieval test executed.
- Any stale retrieval documented.

7. Closeout gate
- Validation report completed.
- Engineering log updated.
- Git committed and pushed.
- Timeshift snapshot created and confirmed.

## Acceptance Criteria

v2.2 can close only if:

- Test corpus is synthetic and non-sensitive.
- Open WebUI remains localhost-only.
- UFW posture remains unchanged.
- Docker networking remains unchanged.
- Approved models remain unchanged.
- No external vector database is installed.
- Retrieval tests are completed or explicitly documented as blocked.
- Answer quality is assessed.
- Hallucination resistance is assessed.
- Removal behavior is assessed.
- Residual risks are documented.
- Release artifacts are ASCII-clean.
- Release artifacts have no trailing whitespace.
- Git history is auditable.
- Final snapshot is created and confirmed.

## Stop Conditions

Stop the release if:

- Any test document contains sensitive or production data.
- Open WebUI is exposed beyond localhost.
- A model appears unexpectedly.
- Docker networking changes unexpectedly.
- UFW is weakened.
- Open WebUI storage or removal behavior cannot be reasonably assessed.
- Document removal fails and residual risk is unacceptable.
- The model repeatedly invents unsupported answers.
- Evidence cannot be captured.

## Recommendation

Proceed with v2.2 as a narrow synthetic pilot.

Do not use real documents.

Do not install new infrastructure.

Do not promote v2.2 to production knowledge base functionality.

## Hold Point

Stop after validating this formal plan, synthetic corpus, and screening review before document loading.

Do not load documents into Open WebUI without review and approval.
Do not create test corpus files.
Do not load documents.
Do not install RAG tooling.
Do not install a vector database.
Do not change Docker, Open WebUI, Ollama, firewall, ports, networking, models, or volumes.
