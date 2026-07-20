# ADP v2.3 RAG Prompt-Control and Retrieval-Quality Hardening Plan

## Document Control

Project: AI Development Platform - ADP
Release: v2.3
Status: Approved release plan
Host: smt-ai
Workspace: ~/Labs/AI-Development-Platform
Branch: main
Release type: Synthetic RAG prompt-control, retrieval-quality, repeatability, and removal-validation hardening
Data sensitivity: Synthetic non-sensitive only
Authorized roadmap boundary: Complete v2.3, then proceed to v2.4 only if the v2.3 entry gate is met

## Release Objective

Harden the controlled local RAG pilot process so that prompts, source targeting, document-only behavior, abstention, false-premise rejection, conflict handling, repeatability, and removal validation can be tested with complete and reproducible evidence.

This release does not approve broader document use. It determines whether the current localhost-only Open WebUI and approved-model baseline can support a formal synthetic qualification release in v2.4.

## Current Baseline

The validated v2.2 baseline is:

- Host: smt-ai.
- Branch: main.
- HEAD: 2b584ef.
- origin/main: 2b584ef.
- Working tree: clean.
- Open WebUI image: ghcr.io/open-webui/open-webui:v0.10.2.
- Open WebUI binding: 127.0.0.1:3000->8080/tcp.
- Open WebUI status: healthy.
- Ollama version: 0.30.11.
- Approved models: llama3.2:1b and llama3.2:3b.
- Approved v2.2 synthetic corpus: five Markdown files.
- No external vector database.
- No network, firewall, model, runtime, or Docker volume change.

## v2.2 Lessons Requiring Remediation

The v2.2 pilot showed that loading and simple direct retrieval worked, but controlled answer behavior was not reliable enough.

The following failures or limitations must be addressed:

- Guardrail extraction was incomplete.
- Source-specific control lookup failed.
- Cross-source comparison failed.
- Document-only behavior failed when outside knowledge was added.
- False-premise rejection was unclear.
- Conflict handling failed.
- Repeatability testing was misinterpreted.
- Removal evidence did not use a clean fixed before-and-after prompt pair.
- Source selection and source attribution were inconsistent.
- Open WebUI internal index and storage behavior remain only partially validated.

## Planning Principles

- Change one control variable at a time.
- Reuse the existing five-file v2.2 synthetic corpus unless a documented test defect requires a synthetic correction.
- Do not expand corpus scope merely to improve model performance.
- Use fresh chats for independent test runs.
- Preserve exact prompts for repeatability and removal testing.
- Record failures without rewriting evidence.
- Limit prompt remediation to three controlled revision cycles.
- Treat v2.4 as blocked unless all v2.3 entry criteria are satisfied.

## In Scope

- Validate the clean v2.2 baseline before any write or runtime action.
- Create and review this v2.3 release plan.
- Create a durable RAG prompt-control standard.
- Create a version-controlled v2.3 test prompt library.
- Create a manual evidence-record template.
- Define source-targeting and source-attribution rules.
- Define document-only response rules.
- Define exact abstention language.
- Define false-premise rejection language.
- Define conflict-reporting requirements.
- Define independent repeatability procedures.
- Define exact before-and-after removal validation.
- Run synthetic tests using the approved local baseline.
- Record prompt revisions and failure modes.
- Document residual risks.
- Commit, push, snapshot, and record final recoverability if closeout gates are met.
- Define the v2.4 qualification entry decision.

## Out of Scope

- Real business documents.
- Client or customer documents.
- Legal, contract, or privileged documents.
- Financial, payment, or tax records.
- Medical, health, or PHI records.
- Employee or personnel records.
- Personal data or PII.
- Confidential, regulated, credential, secret, token, API key, or password data.
- Production data.
- Public-content pilot activity.
- Production RAG deployment.
- Automated or API ingestion.
- External vector database installation.
- New model installation.
- Open WebUI upgrade.
- Ollama upgrade.
- Docker networking changes.
- Firewall changes.
- LAN or Internet exposure.
- Multi-user access.
- Open WebUI Docker volume deletion or replacement.
- v2.5 or later implementation.

## Planned Artifacts

Required candidate artifacts:

- docs/ADP-v2.3-RAG-Prompt-Control-and-Retrieval-Quality-Hardening-Plan.md
- docs/ADP-RAG-Prompt-Control-Standard.md
- docs/ADP-v2.3-RAG-Test-Prompt-Library.md
- docs/ADP-v2.3-RAG-Manual-Test-Record-Template.md
- docs/ADP-v2.3-RAG-Hardening-Validation-Report.md
- docs/ADP-v2.3-Closeout.md
- docs/ADP-v2.3-Final-Recoverability-Record.md
- docs/ADP-Engineering-Log.md

Optional durable artifact, only if the plan review confirms that a separate procedure improves reuse and auditability:

- docs/ADP-RAG-Removal-Validation-Procedure.md

No v2.4 plan artifact is created during initial v2.3 implementation. The v2.4 plan is created only after v2.3 closeout evidence supports its entry gate.

## Prompt-Control Requirements

Every controlled prompt must identify:

- The intended source file or source set.
- The permitted information boundary.
- The required output structure.
- The required not-found response.
- The required false-premise response when applicable.
- The required conflict response when applicable.
- Whether source evidence must be displayed.
- Whether the run must occur in a fresh chat.

The prompt library must use stable prompt identifiers and versions.

A prompt must not request autonomous repetition, scheduling, monitoring, or future execution.

## Document-Only Response Rules

Controlled prompts must direct the model to:

- Use only the loaded named document or named document set.
- Exclude general knowledge and unstated assumptions.
- Avoid caveats unless the source is incomplete or conflicting.
- Return the required abstention statement when the answer is absent.
- Reject unsupported premises directly.
- Identify conflicts without resolving them unless the documents provide a controlling rule.
- Provide only the requested fields, bullets, or table structure.
- Identify the source file used for each material answer element.

## Required Abstention Language

When requested information is absent, the controlled response must be exactly:

Not found in the loaded document.

For a multi-document prompt, the allowed response is:

Not found in the loaded documents.

No additional general knowledge, legal commentary, examples, or speculation is permitted.

## Required False-Premise Language

When a prompt includes a premise not supported by the named loaded source, the response must begin with:

The premise is not supported by the loaded document.

The response may then state the supported fact from the document, if one exists.

## Required Conflict-Handling Structure

When named sources conflict, the response must provide:

- Source A.
- Statement A.
- Source B.
- Statement B.
- Conflict status.
- Controlling rule, if explicitly present.
- Required escalation or abstention when no controlling rule exists.

The model must not silently choose one statement.

## Test Matrix

### T01 - Direct Retrieval

Purpose: Confirm precise source-backed direct retrieval.

Pass criteria:

- Correct answer.
- Correct named source.
- No unnecessary caveat.
- No outside knowledge.

### T02 - Exact Guardrail Extraction

Purpose: Confirm complete constrained extraction.

Pass criteria:

- Exactly five bullets.
- Each bullet maps to a source statement.
- No duplicate guardrails.
- No invented guardrails.

### T03 - Source-Targeted Control Lookup

Purpose: Confirm retrieval from the named control matrix.

Pass criteria:

- Correct control ID.
- Correct control name.
- Correct requirement.
- Correct source file.

### T04 - Structured Cross-Source Comparison

Purpose: Confirm comparison across two named synthetic files.

Pass criteria:

- Required table structure.
- Accurate baseline column.
- Accurate pilot column.
- Accurate difference column.
- Source identified for each row.

### T05 - Absent-Answer Behavior

Purpose: Confirm strict abstention.

Pass criteria:

- Exact required not-found response.
- No additional language.
- No outside knowledge.

### T06 - False-Premise Rejection

Purpose: Confirm hallucination resistance.

Pass criteria:

- Required false-premise opening.
- Correct supported fact, if present.
- No adoption of the false premise.
- No unsupported explanation.

### T07 - Conflict Detection

Purpose: Confirm retrieval and reporting of the synthetic conflict.

Pass criteria:

- Correct Source A and Statement A.
- Correct Source B and Statement B.
- Conflict clearly identified.
- No unsupported resolution.

### T08 - Repeatability

Purpose: Confirm stable behavior.

Procedure:

- Run the same approved prompt three times.
- Use a fresh chat for each run.
- Use the same model, Knowledge collection, and source files.
- Record each response separately.
- Do not ask the model to repeat the test itself.

Pass criteria:

- Three of three runs pass the underlying test.
- Material facts and required structure are equivalent.
- No run introduces outside knowledge.

### T09 - Removal Validation

Purpose: Confirm clean before-and-after behavior.

Procedure:

- Use a fixed direct-retrieval prompt with a unique synthetic fact.
- Run the prompt before removal in a fresh chat.
- Capture the answer and displayed source evidence.
- Remove the approved Knowledge collection or approved files using the documented manual procedure.
- Start a new fresh chat.
- Run the exact same prompt after removal.
- Capture the answer and displayed source evidence.
- Record whether content or source retrieval persists.

Pass criteria:

- Before removal: correct answer and source evidence.
- After removal: no removed source evidence.
- After removal: required not-found response.
- No answer content persists from conversation history.
- Removal steps and timestamps are recorded.

## Evidence Requirements

For every test run, record:

- Test ID.
- Prompt version.
- Exact prompt.
- Date and local time.
- Host.
- Open WebUI image.
- Ollama version.
- Model.
- Knowledge collection name.
- Named source file or files.
- Fresh-chat confirmation.
- Full response.
- Displayed source evidence.
- Expected result.
- Actual result.
- Pass, fail, or blocked status.
- Failure mode.
- Prompt revision cycle.
- Reviewer decision.

Evidence may be manually transcribed into Markdown. Screenshots may supplement but must not replace the structured record.

## Prompt Revision Controls

- Maximum revision cycles: three.
- Each revision must have a new prompt version.
- The reason for revision must be documented.
- Prior prompt versions and outputs must be retained.
- A prompt may not be tuned using real or sensitive data.
- A test that still fails after three controlled revisions triggers a stop condition.
- Changes to runtime, models, networking, or infrastructure are not prompt remediation.

## Security Guardrails

- Preserve localhost-only Open WebUI access.
- Preserve 127.0.0.1:3000->8080/tcp.
- Preserve the current firewall posture.
- Preserve Open WebUI v0.10.2.
- Preserve Ollama 0.30.11 unless a separately approved release changes it.
- Use only llama3.2:1b and llama3.2:3b.
- Use only screened synthetic non-sensitive documents.
- Do not add infrastructure.
- Do not install a vector database.
- Do not delete or replace the Open WebUI Docker volume.
- Do not expose the service to a LAN or the Internet.
- Stop if an unexpected runtime or security change is observed.

## Validation Gates

### Gate 1 - Baseline

Required:

- Clean working tree.
- main branch.
- HEAD and origin/main aligned at 2b584ef before v2.3 changes.
- Expected v2.2 artifacts and five-file corpus present.
- Open WebUI healthy and localhost-only.
- Only approved models present.

### Gate 2 - Plan Promotion

Required:

- Temporary plan candidate reviewed.
- ASCII-only validation passes.
- No trailing whitespace.
- Required sections are complete.
- Scope and exclusions are explicit.
- Planned artifact set is approved.
- No repository file is created before this gate passes.

### Gate 3 - Control Artifact Readiness

Required:

- Prompt-control standard reviewed.
- Prompt library versioned.
- Manual evidence template complete.
- Test expected results documented.
- Removal procedure reviewed before any Knowledge removal.

### Gate 4 - Test Execution

Required:

- Synthetic corpus only.
- Fresh-chat controls followed.
- Exact prompts retained.
- Evidence complete.
- Maximum revision cycles enforced.
- Security posture unchanged.

### Gate 5 - Closeout

Required:

- Validation report complete.
- All pass, fail, and blocked results preserved.
- Residual risks documented.
- v2.4 entry decision documented.
- Git status reviewed.
- Changes committed and pushed.
- Timeshift snapshot created and confirmed.
- Final recoverability record committed and pushed.

## Acceptance Criteria

v2.3 may close as successfully hardened only when:

- T01 through T09 pass.
- T08 passes three of three independent fresh-chat runs.
- No controlled answer introduces outside knowledge.
- All required source targeting and source attribution are correct.
- The exact removal prompt pair produces the required before-and-after behavior.
- Evidence is complete and reviewable.
- Security and data boundaries remain unchanged.
- No critical or high unresolved residual risk remains for a synthetic v2.4 qualification test.

v2.3 may close with mixed or failed results for learning and recoverability, but v2.4 remains blocked.

## v2.4 Entry Gate

Proceed to v2.4 only when:

- v2.3 is closed and recoverable.
- T01 through T09 pass.
- Repeatability is three of three.
- Removal validation is complete.
- Prompt versions and expected answers are frozen.
- No prohibited data was used.
- Runtime and security posture remain controlled.
- Residual risks are acceptable for an expanded synthetic qualification corpus.
- A formal go decision is recorded.

v2.4 remains a synthetic qualification release. It does not authorize real, sensitive, confidential, regulated, privileged, client, employee, financial, medical, personal, credential, contract, or production data.

## Stop Conditions

Stop implementation or testing when:

- Real or sensitive content is introduced or proposed.
- The working tree contains unexplained changes.
- HEAD or origin/main differs unexpectedly.
- Open WebUI is no longer localhost-only or healthy.
- An unapproved model, image, container, port, or network change appears.
- A prompt requires more than three controlled revision cycles.
- A critical test cannot be reproduced.
- Removal cannot be verified.
- Removed content persists in a fresh post-removal chat.
- Evidence is incomplete or cannot be reconciled.
- A required artifact fails ASCII or trailing-whitespace validation.
- A change would require infrastructure, upgrade, firewall, Docker volume, or exposure modification.
- The release scope would expand beyond synthetic hardening.

## Closeout Decision Categories

The v2.3 closeout must select one:

- Proceed to v2.4.
- Remediate in another v2.3-series hardening release.
- Defer RAG work.
- Stop the current RAG approach.

No release beyond v2.4 is authorized by this plan.

## First Controlled Action

Create only a temporary plan candidate outside docs/.

Validate:

- File path.
- SHA-256.
- ASCII-only content.
- No trailing whitespace.
- Required headings.
- Git working tree remains unchanged.

Promote the plan into docs/ only after explicit review and approval.
