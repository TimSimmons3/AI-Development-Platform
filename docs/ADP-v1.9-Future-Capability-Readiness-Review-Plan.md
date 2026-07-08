# ADP v1.9 Future Capability Readiness Review Plan Candidate

## Release Objective
ADP v1.9 will perform a readiness and design review for future local content loading, RAG, and document QA testing capabilities without implementing those capabilities.

## Current Baseline
- ADP v1.8 is complete, documented, committed, pushed, snapshotted, and recoverable.
- Current branch is main.
- Current validated HEAD and origin/main are 21ea1ac.
- Open WebUI remains localhost-only on 127.0.0.1:3000->8080/tcp.
- Open WebUI image remains ghcr.io/open-webui/open-webui:v0.10.2.
- Approved Ollama models remain llama3.2:1b and llama3.2:3b.

## In Scope
- Define future content-loading assumptions.
- Define future RAG readiness assumptions.
- Define future document QA readiness assumptions.
- Identify prerequisites, constraints, risks, and decision gates for later implementation.
- Confirm the current foundation does not block future content-loading work.
- Preserve the current security posture.

## Out of Scope
- RAG installation.
- Vector database installation.
- Document ingestion.
- Content indexing.
- Local file loading into Open WebUI.
- Model additions.
- Network exposure changes.
- Firewall weakening.
- Docker host networking.
- Open WebUI volume deletion or replacement.

## Planned Artifacts
- docs/ADP-v1.9-Future-Capability-Readiness-Review-Plan.md
- docs/ADP-Future-Capability-Readiness-Review.md
- docs/ADP-Local-Content-RAG-Assumptions.md
- docs/ADP-Engineering-Log.md

## Validation Gates
- Confirm clean Git status before implementation.
- Validate candidate files are ASCII-clean before promotion.
- Validate candidate files have no trailing whitespace before promotion.
- Validate required v1.9 sections are present before release.
- Validate no runtime, model, network, firewall, or Open WebUI volume changes occurred.
- Validate engineering log update before commit.

## Security Guardrails
- Keep Open WebUI localhost-only.
- Do not expose Open WebUI to LAN or Internet.
- Do not use Docker host networking.
- Do not weaken UFW or firewall posture.
- Do not delete or replace the Open WebUI Docker volume.
- Do not add models during v1.9.
- Do not ingest, index, or load local content during v1.9.

## Future Capability Assumptions
- Future local content loading must use non-sensitive test data first.
- Future RAG work must have documented rollback and data-removal procedures.
- Future document QA testing must define source files, expected answers, evidence retention, and pass/fail criteria.
- Future storage and indexing decisions must consider data classification, retention, backup, and recovery.
- Future model suitability decisions must use controlled evaluation prompts and documented acceptance criteria.

## Acceptance Criteria
- v1.9 readiness assumptions are documented.
- v1.9 risks, constraints, prerequisites, and decision gates are documented.
- v1.9 confirms whether the current foundation blocks future content-loading work.
- v1.9 makes no implementation changes to RAG, models, networking, firewall, Docker runtime, or Open WebUI volume.
- v1.9 artifacts pass ASCII and trailing-whitespace validation.


## Supplemental Readiness Controls
- Data classification must be defined before any future content loading.
- Sensitive, regulated, confidential, customer, financial, health, credential, and production data must be excluded from initial future testing.
- Future test data must be synthetic, public, or deliberately non-sensitive.
- Future content-loading tests must define source location, owner, purpose, retention period, removal method, and rollback method.
- Future indexing decisions must document storage location, persistence behavior, backup impact, recovery impact, and deletion expectations.
- Future document QA testing must include expected-answer files, citation expectations, hallucination checks, and evidence-retention rules.
- Future RAG enablement must have a go/no-go gate before any installation, ingestion, indexing, or Open WebUI configuration change.
- v1.9 remains documentation-only and must not make runtime implementation changes.
