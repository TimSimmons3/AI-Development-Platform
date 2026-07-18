# ADP v2.1 Controlled Local Content, RAG, and Document QA Plan

## Document Control

Project: AI Development Platform - ADP
Release: v2.1
Status: Approved planning artifact - implementation not started
Host: smt-ai
Workspace: ~/Labs/AI-Development-Platform
Repository branch: main
Current baseline: ADP v2.0
Baseline commit: c13baa2
Prepared for: Controlled planning, design, validation, and approval before implementation

## Release Objective

ADP v2.1 will define and validate a controlled approach for local content loading, retrieval augmented generation, and document question-answer testing without weakening the stable v2.0 local foundation.

The release objective is to establish safe rules, architecture choices, test procedures, rollback controls, and validation gates before any content ingestion or RAG component activation occurs.

## Current v2.0 Baseline

The v2.0 baseline is complete, validated, documented, committed, pushed, snapshotted, and recoverable.

Confirmed baseline controls:

- Open WebUI remains localhost-only.
- Open WebUI image remains ghcr.io/open-webui/open-webui:v0.10.2.
- Open WebUI binding remains 127.0.0.1:3000->8080/tcp.
- Approved models remain llama3.2:1b and llama3.2:3b.
- No unexpected models are present.
- No RAG tooling is installed or enabled.
- No vector database is installed.
- No documents are loaded, ingested, indexed, embedded, or added to Open WebUI.
- No Docker networking changes have been made.
- No firewall weakening has been performed.
- No Open WebUI exposure change has been made.
- No Open WebUI Docker volume deletion or replacement has occurred.

## Release Principles

ADP v2.1 will follow the established workflow:

Plan -> Implement -> Validate -> Document -> Snapshot -> Release

Planning must precede implementation.

No local content loading, indexing, RAG enablement, vector database installation, model addition, Docker change, firewall change, or Open WebUI exposure change may occur until the relevant plan section and rollback path are reviewed and approved.

## In Scope

The following items are in scope for v2.1 planning:

- Controlled local content loading design.
- RAG architecture decision points.
- Document QA testing approach.
- Non-sensitive test corpus rules.
- Data classification rules.
- Sensitive-data exclusion controls.
- Storage and indexing considerations.
- Rollback and data-removal procedure.
- Security and privacy guardrails.
- Validation gates for ingestion, retrieval, answer quality, and removal.
- Evidence logging requirements.
- Recovery checkpoint requirements.
- Final release closeout criteria.

The following items may enter implementation scope only after review and approval:

- Small non-sensitive test corpus selection.
- Controlled loading of approved non-sensitive documents.
- Retrieval and answer-quality testing.
- Removal and rollback validation.

## Out of Scope

The following items are out of scope for v2.1 unless separately planned, reviewed, approved, and validated:

- Production knowledge base deployment.
- Real business document ingestion.
- Legal document ingestion.
- Financial document ingestion.
- Medical document ingestion.
- Customer or client file ingestion.
- Employee record ingestion.
- Confidential or privileged document ingestion.
- Regulated data ingestion.
- PHI, PII, payment data, credentials, secrets, contracts, or private business records.
- LAN or Internet exposure of Open WebUI.
- Docker host networking.
- Firewall weakening.
- Open WebUI Docker volume deletion or replacement.
- New model installation.
- Open WebUI image upgrade.
- Ollama upgrade.
- Multi-user production access.
- External sharing or remote access.
- Automated ingestion pipelines.

## Planned Artifacts

Planned v2.1 artifacts:

- docs/ADP-v2.1-Controlled-Local-Content-RAG-Document-QA-Plan.md
- docs/ADP-Local-Content-Loading-and-RAG-Design.md
- docs/ADP-Document-QA-Test-Plan.md
- docs/ADP-v2.1-Validation-Report.md
- docs/ADP-Engineering-Log.md

Optional artifacts, if needed:

- docs/ADP-Local-Content-Data-Classification-Standard.md
- docs/ADP-RAG-Rollback-and-Data-Removal-Procedure.md

Artifact decisions will be confirmed before file promotion.

## Data Classification Rules

v2.1 test data must be classified before use.

Allowed initial test data:

- Public documents.
- Artificially created sample documents.
- Non-sensitive synthetic business examples.
- Non-sensitive technical notes created only for testing.
- Documents that contain no personal, confidential, regulated, proprietary, or privileged information.

Prohibited initial test data:

- Personal data.
- Sensitive personal data.
- PHI.
- PII.
- Payment data.
- Credentials.
- Secrets.
- API keys.
- Tokens.
- Passwords.
- Contracts.
- Client files.
- Customer records.
- Employee records.
- Legal files.
- Financial files.
- Insurance files.
- Medical files.
- Private business records.
- Confidential or privileged materials.
- Production data.

## Test-Data Rules

Each proposed test document must satisfy these rules before use:

- It must be non-sensitive.
- It must be intentionally selected for testing.
- It must have a clear source or creation record.
- It must be small enough for controlled validation.
- It must not include private or regulated information.
- It must not include hidden credentials, tokens, keys, or secrets.
- It must be removable after testing.
- It must be documented in the validation report if used.

Synthetic documents are preferred for the first pilot because they are lower risk and easier to validate.

## Sensitive-Data Exclusion Controls

Before any test document is loaded, the release must define a screening gate.

Minimum screening expectations:

- Manual review of document purpose and source.
- Text scan for obvious sensitive terms.
- Credential and secret keyword review.
- Confirmation that no real business, legal, financial, medical, client, customer, employee, or personal data is present.
- Confirmation that the document may be safely indexed and later removed.
- Confirmation that document loading is limited to the test scope.

No document may be loaded if classification is uncertain.

## RAG Architecture Decision Points

v2.1 must answer these design questions before implementation:

- Should v2.1 use Open WebUI built-in document and knowledge features, if available and safe?
- Should external vector database tooling remain deferred?
- Where are document files stored before loading?
- Where are embeddings or indexes stored after loading?
- What component owns deletion and cleanup?
- What evidence proves content was removed?
- What quality standard is required for answers based on retrieved content?
- What failure modes must be tested?
- What logs or screenshots are needed for release evidence?

Default recommendation for v2.1:

Use the lowest-change architecture that preserves localhost-only access, avoids new infrastructure unless required, and supports clear rollback.

## Local Content Loading Assumptions

Initial assumptions:

- Content loading remains local only.
- Open WebUI remains localhost-only.
- No network exposure changes are made.
- No host networking is used.
- No firewall weakening is performed.
- No production or sensitive data is used.
- No new model is required.
- Any content loaded must be removable.
- Any test must be documented with evidence.
- If deletion behavior cannot be validated, ingestion must stop.

## Document QA Testing Approach

Document QA testing should evaluate whether the platform can answer questions using only approved local test content.

Minimum QA dimensions:

- Retrieval relevance.
- Answer accuracy.
- Citation or source-reference behavior, where supported.
- Refusal or uncertainty behavior when the answer is not in the document.
- Hallucination resistance.
- Consistency across repeated prompts.
- Handling of conflicting or missing information.
- Ability to remove documents and prevent later retrieval.

Representative test prompts should include:

- Direct lookup questions.
- Summary questions.
- Comparison questions.
- Questions with absent answers.
- Questions designed to test hallucination.
- Questions after document removal.

## Storage and Indexing Considerations

Before any ingestion, v2.1 must identify:

- Where source test documents will reside.
- Whether documents are copied into Open WebUI storage.
- Whether embeddings are generated.
- Where indexes are stored.
- Whether deletion removes source files only, index entries only, or both.
- Whether backups or snapshots may retain indexed content.
- How to verify removal.
- How to avoid retaining sensitive data in future releases.

For v2.1, test data must remain intentionally low sensitivity so that backup or cache uncertainty does not create material exposure.

## Rollback and Data-Removal Procedure

v2.1 must define rollback before ingestion.

Minimum rollback design:

- Stop before any uncertain ingestion.
- Record the test documents loaded.
- Record the loading method.
- Record storage locations, if known.
- Remove test documents from the UI or configured knowledge area.
- Remove local test files if required.
- Re-test questions after removal.
- Confirm that removed content is no longer retrievable.
- Preserve Open WebUI container and Docker volume unless a separately approved recovery procedure requires otherwise.
- Do not delete or replace the Open WebUI Docker volume during v2.1.

If content cannot be removed cleanly, v2.1 must document the residual risk and stop before broader use.

## Security Guardrails

Security controls to preserve:

- Keep Open WebUI bound to 127.0.0.1 only.
- Do not expose Open WebUI to LAN.
- Do not expose Open WebUI to Internet.
- Do not use Docker host networking.
- Do not disable or weaken UFW.
- Do not delete or replace the Open WebUI Docker volume.
- Do not add models without separate approval.
- Do not ingest sensitive or production data.
- Do not enable automated ingestion.
- Do not introduce external sharing.
- Do not store secrets in documents, scripts, logs, or prompts.

## Validation Gates

v2.1 validation gates:

1. Baseline gate
- Git clean.
- HEAD and origin/main aligned.
- v2.0 artifacts present.
- v2.0 files ASCII-clean.
- v2.0 files have no trailing whitespace.
- Open WebUI healthy and localhost-only.
- Approved models unchanged.

2. Plan gate
- Plan artifact originated as a /tmp draft before promotion.
- Draft is ASCII-clean before promotion.
- Draft has no trailing whitespace before promotion.
- Draft is reviewed before promotion.
- Git remains unchanged until promotion is approved.

3. Design gate
- Architecture decision documented.
- Test-data controls documented.
- Rollback path documented.
- No runtime changes performed before approval.

4. Test-data gate
- Test corpus approved.
- Sensitive-data exclusions confirmed.
- No production data included.

5. Ingestion gate, if approved
- Loading method documented.
- Loaded documents listed.
- Runtime posture unchanged.
- No unexpected models added.

6. QA gate, if approved
- Retrieval tests executed.
- Answer quality reviewed.
- Hallucination tests executed.
- Absent-answer tests executed.
- Removal tests executed.

7. Closeout gate
- Validation report completed.
- Engineering log updated.
- Git status clean after commit.
- Branch main confirmed.
- origin/main aligned after push.
- Snapshot created and documented.

## Acceptance Criteria

v2.1 can close only when the following criteria are met:

- The v2.0 baseline remains intact.
- Open WebUI remains localhost-only.
- Approved model controls remain unchanged.
- No sensitive data is ingested.
- The architecture decision is documented.
- The document QA test plan is documented.
- Test-data rules are documented.
- Rollback and removal expectations are documented.
- Any implemented pilot uses only approved non-sensitive test data.
- Any implemented pilot validates retrieval, answer quality, and removal.
- Residual risks are documented.
- Engineering log is updated.
- Release artifacts are ASCII-clean.
- Release artifacts have no trailing whitespace.
- Git history is clean and auditable.
- Final snapshot is created after release closeout.

## Initial Recommendation

Proceed with v2.1 as a controlled planning and readiness release first.

Recommended v2.1 implementation boundary:

- Create and approve the plan.
- Create the RAG and local content loading design.
- Create the document QA test plan.
- Decide whether a small synthetic non-sensitive pilot belongs in v2.1 or should be deferred to v2.2.
- Do not install new tooling or ingest documents until the design and rollback path are approved.

## Hold Point

Stop after validating this formal plan and any new draft artifacts.

Do not promote additional draft artifacts into docs/ without review.
Do not create additional v2.1 files.
Do not install or enable RAG tooling.
Do not load documents.
Do not change Docker, Open WebUI, Ollama, firewall, ports, networking, models, or volumes.
