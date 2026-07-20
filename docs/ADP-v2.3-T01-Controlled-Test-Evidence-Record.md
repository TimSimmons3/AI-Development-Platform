# ADP v2.3 T01 Controlled Test Evidence Record

## Document Control

Project: AI Development Platform - ADP
Release: v2.3
Status: Final evidence record
Test ID: T01
Test area: Direct retrieval and response control
Primary model: llama3.2:3b
Knowledge collection: ADP-v2.3-synthetic-rag-hardening
Permitted source: adp22_synthetic_platform_overview.md
Data sensitivity: Synthetic non-sensitive only
Baseline commit: 5574663

## Purpose

This record preserves the complete T01 execution history, including an invalid preliminary submission, controlled prompt revisions, observed outputs, failure classifications, evidence limitations, and the final stop-condition decision.

## Approved Source Truth

The required source sentence is:

ADP v2.2 validates synthetic local RAG document loading, retrieval, answer quality, hallucination resistance, and removal behavior while preserving the localhost-only ADP security boundary.

The required source filename is:

adp22_synthetic_platform_overview.md

## Required T01 Behavior

A passing T01 response must:

- Use only adp22_synthetic_platform_overview.md.
- Return the complete release-objective sentence.
- Return exactly two logical lines.
- Place the release objective on line 1.
- Place the source filename on line 2.
- Add no preface, caveat, quotation marks, or outside knowledge.
- Display source evidence supporting retrieval from the named file.
- Use a fresh chat for each independent run.

## Execution Summary

| Sequence | Prompt ID | Revision Cycle | Disposition | Primary Finding |
|---|---|---:|---|---|
| Preliminary | Incomplete submission | Not scored | INVALID | Only the question was submitted; the controlled prompt was incomplete. |
| Run 1 | T01-P1-v1 | 0 | FAIL | Correct answer content, but required two-line structure was not followed. |
| Run 2 | T01-P1-v2 | 1 | FAIL | Wrong passage was returned from the correct source file. |
| Run 3 | T01-P1-v3 Run 1 | 2 | FAIL | Unrelated automation and iCalendar response was returned. |
| Run 4 | T01-P1-v3 Run 2 | 2 | FAIL | Correct passage was retrieved, but unauthorized preface and one-paragraph structure were returned. |
| Run 5 | T01-P1-v4 | 3 | FAIL | Required structure passed, but the answer was invented and unsupported by the source. |

## Preliminary Incomplete Submission

Disposition:

- INVALID.
- NOT SCORED.

Reason:

- Only the question "What is the ADP v2.2 release objective?" was submitted.
- The named-source boundary was omitted.
- The output structure was omitted.
- The outside-knowledge prohibition was omitted.
- The abstention rule was omitted.

Failure mode:

- FM-15 Test procedure deviation.

Evidence limitation:

- The preliminary response was not retained as controlled evidence.

## T01-P1-v1

Revision cycle:

- 0.

Observed response:

```text
Release objective: ADP v2.2 validates synthetic local RAG document loading, retrieval, answer quality, hallucination resistance, and removal behavior while preserving the localhost-only ADP security boundary. Source: adp22_synthetic_platform_overview.md
```

Evaluation:

- Correct source passage: PASS.
- Correct model-generated source attribution: PASS.
- Outside knowledge excluded: PASS.
- Exactly two logical lines: FAIL.
- Displayed Open WebUI source evidence: Not conclusively demonstrated by the retained capture.

Result:

- FAIL.

Primary failure mode:

- FM-05 Output structure violation.

Secondary evidence limitations:

- FM-14 Displayed source evidence absent or not conclusively captured.
- FM-17 Evidence incomplete.

## T01-P1-v2

Revision cycle:

- 1.

Observed response:

```text
Release objective: This synthetic document supports ADP v2.2 local RAG pilot testing. It contains no real personal information, no real business records, no customer data, no employee data, no legal records, no financial records, no medical records, no credentials, no secrets, and no production data.
Source: adp22_synthetic_platform_overview.md
```

Evaluation:

- Correct source filename: PASS.
- Two logical lines: PASS.
- Correct Release Objective section: FAIL.
- Correct source passage: FAIL.
- Outside knowledge excluded: PASS.
- Displayed Open WebUI source evidence: Not demonstrated by the retained capture.

Result:

- FAIL.

Primary failure mode:

- FM-04 Incorrect answer.

Contributing failure mode:

- FM-03 Incomplete or wrong passage selection.

## T01-P1-v3 Run 1

Revision cycle:

- 2.

Observed response reported by the operator:

```text
The DTSTART time should reflect the desired execution time. Use COUNT=1 for one-time automations.
```

Evaluation:

- Expected source retrieved: FAIL.
- Expected answer returned: FAIL.
- Outside knowledge excluded: FAIL.
- Response relevant to test: FAIL.

Result:

- FAIL.

Primary failure mode:

- FM-18 Blocked by interface or retrieval behavior.

Secondary failure mode:

- FM-06 Outside knowledge introduced.

Evidence limitation:

- The exact response was operator-reported and was not preserved in a separate uploaded response file.

## T01-P1-v3 Run 2

Revision cycle:

- 2.

Observed response:

```text
According to the ADP v2.3 synthetic RAG hardening collection, the release objective is: "ADP v2.2 validates synthetic local RAG document loading, retrieval, answer quality, hallucination resistance, and removal behavior while preserving the localhost-only ADP security boundary." Source: adp22_synthetic_platform_overview.md
```

Evaluation:

- Correct source passage: PASS.
- Correct source attribution: PASS.
- Retrieval from the named source: Appears supported by the retained source indicator.
- Exactly two logical lines: FAIL.
- Unauthorized preface: FAIL.
- Unauthorized quotation marks: FAIL.
- Knowledge collection mentioned despite prohibition: FAIL.

Result:

- FAIL.

Primary failure mode:

- FM-05 Output structure violation.

Secondary failure modes:

- FM-03 Incomplete instruction adherence.
- FM-11 Source-attribution format deviation.

## T01-P1-v4

Revision cycle:

- 3.

Observed response:

```text
Release objective: The primary goal of ADP v2.2 Synthetic Platform is to provide a realistic and controlled testing environment for ADP products, with an emphasis on synthetic data that can be used to train machine learning models and evaluate the performance of algorithms.
Source: adp22_synthetic_platform_overview.md
```

Evaluation:

- Correct source filename: PASS.
- Required two-line structure: PASS.
- Correct release objective: FAIL.
- Document-only behavior: FAIL.
- Outside knowledge excluded: FAIL.
- Displayed Open WebUI source evidence: Not demonstrated by the retained capture.

Unsupported additions included:

- A realistic and controlled testing environment for ADP products.
- Synthetic data used to train machine learning models.
- Evaluation of algorithm performance.

None of those statements appear in the approved release-objective source sentence.

Result:

- FAIL.

Primary failure mode:

- FM-04 Incorrect answer.

Secondary failure mode:

- FM-06 Outside knowledge introduced.

Additional evidence limitation:

- FM-14 Displayed source evidence absent.

## Revision-Control Determination

The approved revision limit was reached:

- Initial approved prompt: T01-P1-v1.
- Revision 1: T01-P1-v2.
- Revision 2: T01-P1-v3.
- Revision 3: T01-P1-v4.

No further T01 prompt revision is authorized in v2.3.

The stop condition requiring termination after more than three controlled revision cycles is preserved by stopping after T01-P1-v4.

## Overall T01 Result

Final T01 result:

- FAIL.

What worked intermittently:

- The correct source file was sometimes identified.
- The correct release-objective sentence was retrieved in T01-P1-v1 and T01-P1-v3 Run 2.
- The two-line response structure was achieved in T01-P1-v2 and T01-P1-v4.

What did not work reliably:

- Correct passage selection.
- Exact output control.
- Prohibition of unauthorized prefaces.
- Consistent document-only behavior.
- Exclusion of outside knowledge.
- Reproducibility.
- Complete displayed-source evidence capture.

## Security and Data Boundary

The following boundaries remained preserved during T01:

- Synthetic non-sensitive files only.
- No real or production documents.
- No client, legal, financial, medical, employee, personal, confidential, privileged, regulated, credential, secret, contract, or production data.
- Open WebUI remained localhost-only.
- No model was installed.
- No external vector database was installed.
- No network or firewall change was approved.
- No Docker volume deletion or replacement was performed.

## Stop-Condition Decision

T01 triggered the approved stop condition because the test still failed after the maximum controlled prompt revisions.

Required actions:

- Do not run T02 through T09.
- Do not revise T01 again in v2.3.
- Preserve all evidence.
- Block v2.4.
- Prepare v2.3 validation and remediation decision records.
- Remove the synthetic Knowledge collection through a separately controlled cleanup after evidence records are secured.
