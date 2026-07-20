# ADP v2.3 RAG Hardening Validation Report

## Document Control

Project: AI Development Platform - ADP
Release: v2.3
Status: Final validation report
Host: smt-ai
Workspace: ~/Labs/AI-Development-Platform
Branch: main
Baseline commit: 5574663
Release type: Synthetic RAG prompt-control and retrieval-quality hardening
Data sensitivity: Synthetic non-sensitive only
Current release state: Testing stopped after T01 failure and revision-limit stop condition

## Validation Objective

Determine whether the approved localhost-only Open WebUI RAG baseline can reliably follow strict named-source, document-only, exact-format, abstention, false-premise, conflict, repeatability, and removal controls using only the approved five-file synthetic corpus.

## Completed Governance and Preparation

The following preparation controls were completed:

- v2.3 hardening plan created, approved, committed, and pushed.
- RAG prompt-control standard created, approved, committed, and pushed.
- v2.3 test prompt library created, approved, committed, and pushed.
- Manual test-record template created, approved, committed, and pushed.
- Removal-validation procedure created, approved, committed, and pushed.
- Open WebUI runtime preflight passed.
- The Knowledge collection ADP-v2.3-synthetic-rag-hardening was created.
- Exactly five approved synthetic Markdown files were loaded.
- All five files processed successfully.
- No unexpected file was loaded.
- Runtime, model, network, and security posture remained unchanged.

## Test Execution Scope

Only T01 was executed.

T02 through T09 were not executed because T01 reached the maximum controlled prompt revisions and triggered the approved stop condition.

## Test Matrix

| Test | Test Area | Result | Summary |
|---|---|---|---|
| T01 | Direct retrieval and response control | FAIL | Correct retrieval occurred intermittently, but exact response control, correct passage selection, outside-knowledge exclusion, and reproducibility failed after three revisions. |
| T02 | Exact guardrail extraction | NOT RUN | Blocked by T01 stop condition. |
| T03 | Source-targeted control lookup | NOT RUN | Blocked by T01 stop condition. |
| T04 | Structured cross-source comparison | NOT RUN | Blocked by T01 stop condition. |
| T05 | Absent-answer behavior | NOT RUN | Blocked by T01 stop condition. |
| T06 | False-premise rejection | NOT RUN | Blocked by T01 stop condition. |
| T07 | Conflict detection | NOT RUN | Blocked by T01 stop condition. |
| T08 | Repeatability | NOT RUN | Blocked by T01 stop condition. |
| T09 | Removal validation | NOT RUN | Blocked by T01 stop condition. Controlled administrative cleanup remains pending. |

## T01 Summary

T01 produced five scored controlled runs across four prompt versions, plus one invalid preliminary submission.

Observed behavior included:

- Correct answer with incorrect one-paragraph structure.
- Wrong section retrieved from the correct source file.
- Unrelated automation and iCalendar output.
- Correct answer with an unauthorized preface, quotation marks, and collection reference.
- Structurally correct but invented answer containing unsupported machine-learning and algorithm-performance claims.

The final T01 run demonstrated that additional prompt constraints did not produce reliable source fidelity.

## Acceptance-Criteria Assessment

| Acceptance Criterion | Result |
|---|---|
| T01 through T09 pass | FAIL |
| T08 passes three of three | NOT TESTED |
| No controlled answer introduces outside knowledge | FAIL |
| Required source targeting and attribution are correct | FAIL |
| Exact removal prompt pair passes | NOT TESTED |
| Evidence is complete and reviewable | PARTIAL |
| Security and data boundaries remain unchanged | PASS |
| No critical or high unresolved risk remains for v2.4 | FAIL |

## Overall Release Finding

ADP v2.3 succeeded in establishing stronger governance, prompt controls, exact expected answers, evidence requirements, and stop conditions.

ADP v2.3 did not succeed in proving reliable RAG answer behavior on the current Open WebUI and llama3.2:3b configuration.

The result is:

- Governance and preparation: PASS.
- Synthetic collection creation and loading: PASS.
- T01 retrieval fidelity: INTERMITTENT.
- T01 exact response control: FAIL.
- T01 document-only behavior: FAIL.
- T01 reproducibility: FAIL.
- Broader hardening qualification: NOT ACHIEVED.
- v2.4 entry gate: BLOCKED.

## Residual Risks

Critical or high residual risks include:

- The model may identify the correct source but select the wrong passage.
- The model may retrieve the correct passage but ignore exact output constraints.
- The model may add unauthorized prefaces or collection-level commentary.
- The model may return unrelated automation content.
- The model may invent plausible but unsupported objectives.
- Model-generated source attribution may appear correct even when answer content is wrong.
- Displayed source evidence was not captured consistently.
- A correct result in one run does not predict the next run.
- Current prompt controls are not sufficient for synthetic qualification, real document use, or production use.

## Security Boundary Confirmation

The following remained unchanged:

- Open WebUI remained localhost-only.
- Binding remained 127.0.0.1:3000->8080/tcp.
- Open WebUI remained pinned to ghcr.io/open-webui/open-webui:v0.10.2.
- Ollama remained at the validated version.
- Only llama3.2:1b and llama3.2:3b remained installed.
- No external vector database was installed.
- No Docker networking change was made.
- No firewall weakening was performed.
- No Open WebUI Docker volume deletion or replacement was performed.
- No real or sensitive data was used.

## Stop-Condition Confirmation

The approved stop condition was triggered because T01 required the maximum three controlled prompt revisions and still failed.

Testing stopped before T02.

No additional prompt testing is authorized in v2.3.

## v2.4 Decision

v2.4 is blocked because:

- T01 failed.
- T02 through T09 were not executed.
- Repeatability was not established.
- Removal validation was not completed.
- Prompt behavior was not frozen as reliable.
- Critical residual source-fidelity and instruction-adherence risks remain.

## Pending Controlled Actions

Before v2.3 can close as recoverable:

- Promote and commit the T01 evidence record.
- Promote and commit this validation report.
- Promote and commit the remediation decision record.
- Append the approved v2.3 stop-condition entry to the engineering log.
- Remove the ADP-v2.3-synthetic-rag-hardening Knowledge collection through a controlled administrative cleanup.
- Confirm the five files are no longer present in the active Knowledge collection.
- Revalidate runtime and Git state.
- Create the v2.3 closeout and final recoverability records.
- Commit, push, snapshot, and confirm recoverability.

The cleanup is administrative and must not be scored as T09 removal validation.

## Recommended Release Position

Close v2.3 as a controlled failed hardening release with useful diagnostic evidence.

Select:

- Remediate in another v2.3-series hardening release.

Do not proceed to v2.4.
