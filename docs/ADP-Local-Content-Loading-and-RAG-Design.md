# ADP Local Content Loading and RAG Design

## Document Control

Project: AI Development Platform - ADP
Release: v2.1
Status: Approved design artifact - implementation not started
Host: smt-ai
Workspace: ~/Labs/AI-Development-Platform
Baseline commit: c13baa2
Prepared for: Controlled planning, validation, and approval before implementation

## Design Objective

This design defines a controlled local content loading and retrieval augmented generation approach for ADP v2.1.

The objective is to test local document question answering safely, using non-sensitive test documents only, while preserving the stable v2.0 runtime baseline.

## Recommended v2.1 Architecture

Use the lowest-change architecture for v2.1.

Recommended path:

- Use existing Open WebUI local document or knowledge capabilities only if available in the current v0.10.2 deployment.
- Use manual UI-driven loading for the first controlled test.
- Use only synthetic or public non-sensitive documents.
- Do not add an external vector database in v2.1.
- Do not install Qdrant, Milvus, pgvector, or other indexing services in v2.1.
- Do not add models in v2.1.
- Do not change Open WebUI image version in v2.1.
- Do not change Ollama version in v2.1.
- Do not use API automation for initial ingestion.
- Do not enable automated ingestion pipelines.

## Rationale

A lowest-change approach is preferred because v2.1 is the first local content loading and document QA release.

This approach reduces risk by avoiding new infrastructure, avoiding new network services, preserving localhost-only access, and testing removal behavior before broader use.

External vector databases and production knowledge base patterns should remain deferred until ADP has validated local loading, retrieval quality, removal behavior, and recovery controls.

## Architecture Boundary

The v2.1 design boundary is:

- Local workstation only.
- Open WebUI remains bound to 127.0.0.1.
- Ollama remains local.
- Approved models remain llama3.2:1b and llama3.2:3b.
- Test documents remain non-sensitive.
- Manual test loading only.
- No production data.
- No sensitive data.
- No remote exposure.
- No firewall weakening.
- No Docker host networking.

## Components

Current components preserved from v2.0:

- Linux Mint host smt-ai.
- Docker.
- Open WebUI container.
- Open WebUI image ghcr.io/open-webui/open-webui:v0.10.2.
- Ollama.
- llama3.2:1b.
- llama3.2:3b.
- UFW firewall posture.
- Localhost-only Open WebUI binding.

Potential v2.1 test interaction:

- User creates or selects approved non-sensitive test documents.
- User manually loads approved test documents through Open WebUI document or knowledge functionality.
- User asks controlled QA prompts.
- User records answer behavior.
- User removes the loaded test documents.
- User retests to confirm removed content is no longer available.

## Data Flow

Expected data flow for a controlled pilot:

1. Create or select non-sensitive test documents.
2. Store test documents in a clearly marked local test folder.
3. Review documents for prohibited data.
4. Load documents manually into Open WebUI, if approved.
5. Ask controlled test prompts.
6. Record answers and observations.
7. Remove documents through Open WebUI file or knowledge controls.
8. Retest prompts after removal.
9. Record removal evidence.
10. Preserve final evidence in the validation report.

## Storage Considerations

v2.1 must identify and document:

- Source test document location.
- Whether Open WebUI stores a copy of the document.
- Whether Open WebUI generates embeddings or indexes.
- Whether document deletion removes source text, embeddings, and file references.
- Whether backups or snapshots could retain test content.
- What evidence supports successful removal.

Because storage behavior may not be fully visible from the UI, v2.1 must use only low-risk non-sensitive test documents.

## Indexing Considerations

v2.1 must not assume that deleting the source file deletes all indexes.

Before broader use, the release must validate:

- File removal.
- Knowledge entry removal.
- Post-removal prompt behavior.
- Absence of stale retrieval.
- Any visible file manager or data-control cleanup results.

If removal behavior is unclear, v2.1 must stop before broader ingestion.

## Security Guardrails

Mandatory guardrails:

- Keep Open WebUI bound to 127.0.0.1.
- Do not expose Open WebUI to LAN.
- Do not expose Open WebUI to the Internet.
- Do not use Docker host networking.
- Do not disable UFW.
- Do not weaken UFW.
- Do not delete the Open WebUI Docker volume.
- Do not replace the Open WebUI Docker volume.
- Do not install external vector database tooling.
- Do not install new models.
- Do not ingest sensitive data.
- Do not ingest production data.
- Do not ingest personal data.
- Do not store credentials in test documents.
- Do not store secrets in prompts, logs, files, or screenshots.

## Test Corpus Design

The preferred v2.1 test corpus is synthetic.

Recommended initial corpus:

- Synthetic ADP platform overview.
- Synthetic control matrix.
- Synthetic change log.
- Synthetic policy excerpt.
- Synthetic conflict example.

Each synthetic document should be small, plain text or Markdown, and intentionally designed to support validation.

## Decision Points Before Pilot

The following must be answered before ingestion:

- Which Open WebUI feature will be used for loading?
- Will the test use individual files or a knowledge base?
- Where will source test files reside?
- How will each file be screened?
- How will loaded files be listed?
- How will each file be removed?
- How will retrieval after removal be tested?
- What evidence will be captured?
- What is the stop condition if behavior is unclear?

## Recommended v2.1 Decision

Approve planning and design documentation first.

Then decide whether v2.1 should include a small synthetic pilot or defer pilot ingestion to v2.2.

Default recommendation:

- Complete the design and QA test plan in v2.1.
- Include a pilot only if the UI path, removal path, evidence requirements, and test corpus are approved.
- Avoid external vector databases until a later release.

## Residual Risks

Known residual risks:

- Open WebUI internal storage and index behavior may not be fully transparent from the UI.
- Local models may have limited context windows and may not use all retrieved content.
- RAG answers may be incomplete or overconfident.
- Deletion behavior may require more than deleting the original test file.
- Screenshots may accidentally capture UI metadata.
- Future backups or snapshots could retain test content.

Risk treatment:

- Use only non-sensitive synthetic test content.
- Avoid production data.
- Validate deletion and post-removal behavior.
- Document uncertainty explicitly.

## Hold Point

Stop after validating this formal design artifact and before any implementation activity.

Do not proceed to ingestion, tooling changes, or runtime changes without review.
Do not ingest documents.
Do not install RAG tooling.
Do not install a vector database.
Do not change Docker, Open WebUI, Ollama, firewall, ports, networking, models, or volumes.
