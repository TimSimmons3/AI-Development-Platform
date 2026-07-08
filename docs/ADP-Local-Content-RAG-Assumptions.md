# ADP Local Content and RAG Assumptions Candidate

## Purpose
This document defines assumptions for future local content loading, RAG, and document QA testing after the ADP v2.0 stable foundation baseline.

## Release Boundary
- v1.9 documents assumptions only.
- v1.9 does not load local files.
- v1.9 does not ingest documents.
- v1.9 does not create embeddings or indexes.
- v1.9 does not install a vector database.
- v1.9 does not enable RAG.
- v1.9 does not add models or change runtime exposure.

## Local Content Assumptions
- Future testing must start with synthetic, public, or deliberately non-sensitive data.
- Initial test data must exclude confidential, regulated, customer, health, financial, credential, and production data.
- Each future test file must have a documented owner, source, purpose, classification, and retention period.
- Future content loading must define how files are removed from upload stores, indexes, caches, backups, and generated artifacts.

## RAG Assumptions
- RAG implementation remains deferred until after v2.0.
- Future RAG work must define architecture, storage, indexing, access control, rollback, and deletion procedures before enablement.
- Future RAG testing must require source-grounded answers and citation expectations.
- Future RAG testing must include hallucination checks and known-answer validation.
- Future persistent indexes must have documented storage location, backup impact, and deletion method.

## Document QA Assumptions
- Future document QA testing must use predefined questions and expected answers.
- Future document QA testing must require evidence citations or source references.
- Future document QA testing must record pass, fail, partial, and unsupported-answer outcomes.
- Future document QA testing must separately track retrieval failure, reasoning failure, and citation failure.
- Future document QA testing must preserve evidence sufficient for repeatable validation.

## Security and Privacy Assumptions
- Open WebUI remains localhost-only unless a later release explicitly approves a different posture.
- Firewall posture must not be weakened for content-loading tests.
- Test content must not include secrets, passwords, tokens, private keys, or credentials.
- Sensitive-data testing requires a separate approval gate and is out of scope for initial future tests.
- Future content handling must document privacy, retention, deletion, and recovery expectations.

## Storage and Indexing Assumptions
- Future storage design must identify where uploaded files, extracted text, embeddings, indexes, logs, and generated answers reside.
- Future indexing design must define persistence behavior across restarts, upgrades, backups, restores, and deletions.
- Future backup design must account for index growth, uploaded file retention, and recovery validation.
- Future deletion design must confirm whether source files, extracted content, embeddings, indexes, and logs are all removable.

## Model Suitability Assumptions
- Approved models remain llama3.2:1b and llama3.2:3b during v1.9.
- Future model suitability must be evaluated with controlled prompts, expected answers, and resource observations.
- Future model changes require a separate model-promotion gate and are not part of v1.9.
- Small local models may be sufficient for basic tests but must not be assumed reliable for document-grounded QA without evidence.

## Future Go No-Go Gates
- Approve test-data classification and source list.
- Approve storage, indexing, backup, restore, and deletion design.
- Approve document QA test cases and expected answers.
- Approve rollback and data-removal procedure.
- Approve resource-impact limits for CPU, memory, disk, and backup growth.
- Approve implementation timing after v2.0 stable foundation baseline.

## Assumption Conclusion
The current ADP foundation supports future planning for local content loading, RAG, and document QA testing. Future implementation should remain deferred until after v2.0 and should begin only with controlled, non-sensitive test data, documented rollback, documented deletion, and evidence-based QA gates.

