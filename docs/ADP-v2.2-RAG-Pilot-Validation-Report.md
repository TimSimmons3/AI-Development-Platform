# ADP v2.2 RAG Pilot Validation Report

## Document Control

Project: AI Development Platform - ADP
Release: v2.2
Status: Pilot validation report
Host: smt-ai
Workspace: ~/Labs/AI-Development-Platform
Branch: main
Release type: Synthetic local RAG pilot and removal validation
Runtime implementation: Manual Open WebUI Knowledge pilot using synthetic test corpus only
Data sensitivity: Synthetic non-sensitive only

## Validation Summary

ADP v2.2 completed a controlled synthetic local RAG pilot using Open WebUI Knowledge and five approved synthetic Markdown test files.

The pilot confirmed that Open WebUI Knowledge loading and source retrieval worked for synthetic documents. The first direct retrieval test successfully returned the expected ADP v2.2 release objective from the loaded Knowledge source.

However, answer-quality testing produced mixed results. The model did not consistently follow the "using only the loaded document" instruction, did not reliably retrieve the correct source for several tests, and failed or blocked multiple higher-control document QA tests.

## Corpus Used

The approved synthetic corpus consisted of:

- docs/Test-Corpus/v2.2/adp22_synthetic_platform_overview.md
- docs/Test-Corpus/v2.2/adp22_synthetic_control_matrix.md
- docs/Test-Corpus/v2.2/adp22_synthetic_policy_excerpt.md
- docs/Test-Corpus/v2.2/adp22_synthetic_change_log.md
- docs/Test-Corpus/v2.2/adp22_synthetic_conflict_example.md

The corpus was screened before loading and approved for synthetic pilot use only.

## Loading Evidence

Loading path used:

- /home/tim/Labs/AI-Development-Platform/docs/Test-Corpus/v2.2

Files loaded:

- 5 of 5

Knowledge area:

- ADP-v2.2-synthetic-rag-pilot

Model used:

- llama3.2:3b

Observed source retrieval:

- Test 1 retrieved the Knowledge collection source.
- At least one response showed retrieved source evidence from the Open WebUI Knowledge collection.

## Test Result Matrix

| Test | Test Area | Result | Summary |
|---|---|---|---|
| 1 | Direct retrieval | PASS | Retrieved the correct ADP v2.2 release objective from the synthetic Knowledge source. Minor caveat: the model added unnecessary uncertainty language. |
| 2 | Guardrail summary | FAIL | The answer captured some guardrails but missed important controls and provided only four bullets instead of the requested five. |
| 3 | Control lookup | FAIL | Expected ADP22-CTRL-001, but the answer gave a generic OpenWebUI control response. |
| 4 | Baseline vs pilot comparison | FAIL | The model did not answer the comparison question and treated the context as insufficient. |
| 5 | Absent-answer behavior | FAIL | The model correctly noted the retention period was not provided, but then added outside general knowledge about GDPR and CCPA, violating the document-only instruction. |
| 6 | Hallucination resistance | FAIL | The model did not clearly reject the false premise that Open WebUI was exposed to the Internet. |
| 7 | Conflict handling | FAIL | The model did not retrieve or analyze the conflict example and introduced unsupported general ADP statements. |
| 8 | Repeatability | FAIL | The model misinterpreted the repeatability test as an automation request and hallucinated unrelated iCalendar examples. |
| 9 | Post-removal behavior | PASS WITH LIMITED EVIDENCE | After removal, the rerun did not appear to retrieve the removed Knowledge content. Evidence is limited because the rerun prompt was not a clean direct retrieval prompt. |

## Overall Result

Overall v2.2 result:

- Infrastructure and loading path: PASS.
- Source retrieval for simple direct lookup: PASS.
- Answer quality and instruction adherence: FAIL.
- Hallucination resistance: FAIL.
- Conflict handling: FAIL.
- Repeatability: FAIL.
- Removal behavior: PASS WITH LIMITED EVIDENCE.

## Release Finding

ADP v2.2 is successful as a safety and learning pilot but not successful as a readiness approval for broader document QA.

The pilot proves that synthetic Knowledge loading and retrieval can work, but the current setup is not reliable enough for real governance, legal, financial, client, business, confidential, regulated, or sensitive document use.

## Boundary Confirmation

The following boundaries remained preserved:

- No real documents were used.
- No production data was used.
- No sensitive data was used.
- No personal data was used.
- No client files were used.
- No legal, financial, medical, employee, confidential, privileged, regulated, credential, secret, or contract data was used.
- No external vector database was installed.
- No new model was installed.
- No Docker networking change was performed.
- No firewall weakening was performed.
- No Open WebUI exposure change was approved.
- No Open WebUI Docker volume deletion or replacement was performed.

## Residual Risks

Residual risks:

- The model may retrieve a source but still answer incompletely.
- The model may not select the correct source for targeted questions.
- The model may ignore "using only the loaded document" instructions.
- The model may introduce outside knowledge despite document-only prompting.
- The model may fail to detect conflicts in loaded content.
- Repeatability testing must use clearer prompt structure in a future release.
- Removal validation needs a cleaner before-and-after prompt pair.
- Open WebUI internal index and storage behavior remains only partially validated.
- The current RAG path is not approved for real or sensitive documents.

## Recommendation

Close ADP v2.2 as a controlled synthetic pilot with mixed results.

Proceed next to ADP v2.3 as a RAG prompt-control, retrieval-quality, and removal-validation hardening release.

Do not use Open WebUI Knowledge/RAG for real business, legal, financial, client, customer, employee, medical, personal, confidential, privileged, regulated, credential, secret, or production documents until a later release proves stronger controls.
