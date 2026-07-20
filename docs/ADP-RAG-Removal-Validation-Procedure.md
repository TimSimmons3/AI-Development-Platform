# ADP RAG Removal Validation Procedure

## Document Control

Project: AI Development Platform - ADP
Release introduced: v2.3
Status: Approved
Procedure type: Manual local Knowledge removal validation
Data sensitivity: Synthetic non-sensitive only
Applicable test: T09-P1-v1

## Purpose

This procedure validates whether a removed synthetic Knowledge source remains retrievable after controlled manual removal.

The procedure uses one exact prompt before and after removal, separate fresh chats, and a unique synthetic fact.

This procedure does not prove forensic deletion from every internal storage layer. It validates observable retrieval behavior within the approved v2.3 scope.

## Safety Boundary

The procedure must not:

- Delete or replace the Open WebUI Docker volume.
- Delete unrelated Knowledge collections.
- Change Docker networking.
- Change firewall rules.
- Expose Open WebUI beyond localhost.
- Install or remove models.
- Upgrade Open WebUI or Ollama.
- Use real or sensitive documents.
- Use shell commands to manipulate Open WebUI internal storage.
- Treat browser-history behavior as retrieval evidence.

## Preconditions

Confirm and record:

- Repository working tree is clean.
- HEAD and origin/main are aligned.
- Open WebUI is healthy.
- Open WebUI is bound to 127.0.0.1:3000->8080/tcp.
- The selected model is llama3.2:3b.
- The Knowledge collection is `ADP-v2.3-synthetic-rag-hardening`.
- The collection contains exactly the five approved synthetic files.
- The exact T09-P1-v1 prompt is available.
- The manual test record template is ready.
- No unrelated Knowledge collection is selected.
- The operator understands that the existing collection will be removed or emptied.

## Controlled Test Fact

The unique retrieval fact is:

- The v2.2 baseline commit was f6b30ad.

Permitted source:

- adp22_synthetic_change_log.md

This fact is used because it is synthetic, specific, and unlikely to be answered correctly without the named source.

## Exact Prompt Control

Use T09-P1-v1 exactly.

The prompt text must not change between the before-removal and after-removal runs.

Create a prompt hash or retain one version-controlled prompt reference to prove the pair is identical.

## Phase 1 - Before-Removal Run

1. Open Open WebUI through the approved localhost address.
2. Confirm the selected model is llama3.2:3b.
3. Confirm the approved Knowledge collection is attached or selected as required by the interface.
4. Start a new chat.
5. Submit T09-P1-v1 exactly.
6. Do not add follow-up instructions.
7. Capture the complete response.
8. Capture displayed source evidence.
9. Record the date and local time.
10. Record the Knowledge collection name and file count.
11. Confirm the expected response:

```text
Baseline commit: f6b30ad
Source: adp22_synthetic_change_log.md
```

12. Mark the before-removal phase PASS only when:
    - The baseline commit is correct.
    - The response contains exactly two lines.
    - The named source is correct.
    - Displayed source evidence includes the named file.

If the before-removal phase does not pass, stop. Do not remove the collection because the test lacks a valid retrieval baseline.

## Phase 2 - Manual Removal

1. Record the removal start time.
2. Navigate to the Open WebUI Knowledge management area using the visible user interface.
3. Locate `ADP-v2.3-synthetic-rag-hardening`.
4. Confirm the collection name before any destructive action.
5. Use the visible Knowledge management control to remove the approved collection or remove all five approved files.
6. Do not remove any unrelated collection or file.
7. Do not delete or replace the Open WebUI Docker volume.
8. Do not use Docker, shell, database, or filesystem deletion commands.
9. Record the interface labels and confirmation steps actually observed.
10. Return to the Knowledge list.
11. Confirm that:
    - The removed collection is absent, or
    - The retained collection contains none of the five approved files.
12. Record the removal completion time.
13. Capture a screenshot only as supplemental evidence when useful.

If the interface does not provide a clear, controlled removal path, stop and record the test as BLOCKED.

## Phase 3 - Session Isolation

1. End or leave the before-removal chat.
2. Start a new chat.
3. Do not reuse, branch, continue, or quote the prior conversation.
4. Confirm that the removed collection is not attached.
5. Do not attach another Knowledge collection.
6. Keep the same model, llama3.2:3b.
7. Do not restart Open WebUI unless a documented interface condition requires it.
8. If a restart is required:
    - Record the reason.
    - Revalidate image, port binding, health, and model list.
    - Do not delete or replace the Docker volume.

## Phase 4 - After-Removal Run

1. Submit the exact same T09-P1-v1 prompt.
2. Do not add context or follow-up instructions.
3. Capture the complete response.
4. Capture any displayed source evidence.
5. Record the date and local time.
6. Confirm the expected response:

```text
Not found in the loaded documents.
```

7. Mark the after-removal phase PASS only when:
    - The exact not-found response is returned.
    - No removed source is displayed.
    - The value f6b30ad is not returned.
    - No prior conversation content is used.
    - The chat is confirmed fresh.

## Overall Pass Rule

T09 passes only when:

- The before-removal phase passes.
- The controlled removal is confirmed.
- The after-removal phase passes.
- The exact prompt pair is confirmed.
- The source and answer do not persist after removal.
- No runtime or security boundary changes occur.
- Evidence is complete.

## Failure Conditions

Record FAIL when:

- The before-removal answer is wrong or unsupported.
- The named source is not retrieved before removal.
- The exact prompt differs between runs.
- A prior chat is reused.
- The removed source is displayed after removal.
- The baseline commit is returned after removal.
- The model uses unsupported outside knowledge to reconstruct the answer.
- The wrong collection or file is removed.
- Evidence is incomplete but the procedure was otherwise executable.

## Blocked Conditions

Record BLOCKED when:

- The Open WebUI interface does not provide a clear removal control.
- Collection state cannot be confirmed.
- Source evidence cannot be observed.
- The interface fails before a valid before-removal baseline.
- Removal status cannot be determined without prohibited storage manipulation.

## Stop Conditions

Stop immediately when:

- Real or sensitive data is observed.
- An unrelated collection may be affected.
- Open WebUI is no longer localhost-only.
- An unexpected model, image, port, container, or network change appears.
- Docker volume deletion or replacement is proposed.
- Shell-level deletion of Open WebUI storage is proposed.
- More than three prompt revisions would be required.
- The exact prompt pair cannot be proven.
- A critical evidence field cannot be completed.

## Residual Risk Statement

A passing result demonstrates that removed synthetic content is not observably retrieved through the tested fresh-chat Open WebUI path.

A passing result does not independently prove:

- Cryptographic erasure.
- Forensic deletion from every internal index, cache, backup, or storage layer.
- Deletion from host backups or Timeshift snapshots.
- Production-grade data lifecycle compliance.
- Fitness for real or sensitive document use.

Those matters remain outside v2.3 and require separately approved governance and technical validation.

## Completion Record

At completion, record:

- Before-removal test record.
- Removal timestamps.
- Observed interface controls.
- Post-removal Knowledge state.
- After-removal test record.
- Exact prompt identity evidence.
- Screenshots, when used.
- Overall PASS, FAIL, or BLOCKED result.
- Residual risks.
- Reviewer determination.
