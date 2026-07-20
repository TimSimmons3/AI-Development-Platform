# ADP v2.3 Remediation Decision Record

## Document Control

Project: AI Development Platform - ADP
Release: v2.3
Status: Approved decision record
Decision type: Post-stop-condition RAG roadmap decision
Decision date: 2026-07-20
Baseline commit: 5574663
Current Knowledge collection: ADP-v2.3-synthetic-rag-hardening
Decision authority boundary: v2.4 or earlier only

## Decision

Select:

- Remediate in another v2.3-series hardening release.

Do not proceed to v2.4.

Do not continue prompt revisions or broader testing in v2.3.

## Evidence Basis

The decision is based on:

- T01 failed after the maximum three controlled prompt revisions.
- Correct source retrieval occurred intermittently but was not reproducible.
- The correct source file sometimes produced the wrong passage.
- Exact response structure was inconsistent.
- An unrelated automation response occurred.
- The final prompt version returned invented machine-learning and algorithm-performance claims.
- Displayed retrieval evidence was not captured consistently.
- T02 through T09 were not reached.
- Security and data boundaries remained controlled.

## Alternatives Considered

### Proceed to v2.4

Rejected.

Reason:

- The v2.4 entry gate requires T01 through T09 to pass.
- T01 failed.
- T02 through T09 were not run.
- Repeatability and removal validation were not completed.
- Critical source-fidelity and instruction-adherence risks remain.

### Continue revising T01 in v2.3

Rejected.

Reason:

- The approved three-revision limit was reached.
- Additional prompt tuning would violate the v2.3 stop condition.
- The observed failures are not limited to wording or formatting.
- The final run demonstrated unsupported content despite increasingly explicit constraints.

### Defer all RAG work indefinitely

Not selected at this time.

Reason:

- Correct retrieval occurred in some runs.
- The governance and synthetic-data controls operated as intended.
- A limited diagnostic release may determine whether the failure is caused by retrieval, chunk selection, model behavior, interface context, or collection configuration.

### Stop the current RAG approach permanently

Not selected at this time.

Reason:

- The evidence is sufficient to block qualification but not yet sufficient to conclude that every controlled local RAG approach is infeasible.
- A bounded diagnostic release can test the current approach without expanding data, infrastructure, or exposure.

## Recommended Next Release

Recommended identifier:

- ADP v2.3.1.

Recommended title:

- RAG Retrieval-Pipeline and Model-Behavior Diagnostic.

The exact title and scope must be confirmed in a new release plan after v2.3 closeout.

## Recommended v2.3.1 Objective

Determine why the current approved synthetic Knowledge configuration produces intermittent correct retrieval, wrong-passage selection, unrelated automation output, format noncompliance, and unsupported content.

The release should diagnose before attempting broader qualification.

## Recommended v2.3.1 Scope

Potential in-scope diagnostic activities:

- Validate Knowledge collection attachment state for every run.
- Validate whether displayed source evidence corresponds to the response passage.
- Record source excerpts, source ordering, and any retrieval score displayed by Open WebUI.
- Use a minimal one-file synthetic diagnostic collection before returning to the five-file corpus.
- Use exact unique identifiers and unambiguous source facts.
- Compare direct file attachment behavior with Knowledge collection behavior only if supported by the approved interface and separately planned.
- Consider a controlled comparison of the already-approved llama3.2:1b and llama3.2:3b models only if the plan explicitly authorizes one-variable model comparison.
- Inspect approved read-only Open WebUI and container logs for retrieval or context anomalies.
- Determine whether unrelated automation content originates from chat context, prompt routing, model behavior, or interface state.
- Establish three-of-three correct direct retrieval before any multi-file or higher-order test.
- Preserve exact outputs and displayed source evidence.

## Recommended v2.3.1 Exclusions

- Real or sensitive documents.
- v2.4 qualification testing.
- New models.
- Model downloads.
- Open WebUI upgrade.
- Ollama upgrade.
- External vector database.
- Automated ingestion.
- API ingestion.
- Multi-user access.
- Docker host networking.
- Firewall changes.
- LAN or Internet exposure.
- Open WebUI Docker volume deletion or replacement.
- Production deployment.

## v2.3.1 Entry Conditions

Before v2.3.1 begins:

- v2.3 must be closed and recoverable.
- The current Knowledge collection must be removed through controlled cleanup.
- Git status must be clean.
- HEAD and origin/main must align.
- Final v2.3 snapshot must be confirmed.
- The new release plan must define exact diagnostic questions, evidence fields, stop conditions, and acceptance criteria.

## v2.3.1 Minimum Exit Criteria

A future qualification release must remain blocked until a diagnostic release demonstrates:

- Three of three correct direct retrieval runs from a fresh chat.
- Correct displayed source evidence for every run.
- No wrong-passage selection.
- No unrelated automation or scheduling output.
- No unsupported outside knowledge.
- Stable required output structure.
- A documented root-cause conclusion or a bounded residual-risk explanation.

## Current Cleanup Decision

The current Knowledge collection must remain untouched until the v2.3 evidence candidates are reviewed and secured.

After evidence promotion and commit:

- Remove ADP-v2.3-synthetic-rag-hardening through the visible Open WebUI Knowledge interface.
- Confirm the collection or all five approved files are absent.
- Do not delete or replace the Open WebUI Docker volume.
- Do not run a post-removal prompt.
- Record cleanup as administrative cleanup, not T09 validation.

## Final Roadmap Position

- v2.3: Controlled failed hardening release; closeout pending.
- v2.3.1: Recommended diagnostic remediation; not yet authorized.
- v2.4: Blocked.
- v2.5 and later: Deferred and unauthorized.
