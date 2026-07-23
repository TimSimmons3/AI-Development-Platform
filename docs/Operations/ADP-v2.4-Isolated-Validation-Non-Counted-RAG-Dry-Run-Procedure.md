# ADP v2.4 Isolated Validation Non-Counted RAG Dry-Run Procedure

## 1. Status

```text
PROCEDURE_STATUS=FROZEN_FOR_SINGLE_NON_COUNTED_DRY_RUN_NOT_YET_EXECUTED
PROCEDURE_FREEZE_STARTING_COMMIT=83e0103ab6daa67c822763769e9c685b7d38ac6b
PROCEDURE_FREEZE_TAG=adp-v2.4-non-counted-rag-dry-run-procedure-freeze
SELECTED_NON_COUNTED_CASE=C
NON_COUNTED_CHAT_COUNT=1
NON_COUNTED_PROMPT_SUBMISSION_COUNT=1
RERUN=PROHIBITED_PENDING_REVIEW
KNOWLEDGE_UPLOAD_AUTHORIZATION=HOLD_PENDING_SEPARATE_AUTHORIZATION
NON_COUNTED_RAG_EXECUTION_AUTHORIZATION=HOLD_PENDING_SEPARATE_AUTHORIZATION
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

## 2. Purpose

Perform one bounded, non-counted RAG dry run on the isolated validation instance. The run observes factual-answer behavior and citation shape before final counted prompts, expected answers, and citation requirements are frozen.

This procedure does not authorize counted execution. Cases A, B, and D remain unexecuted and provisional.

## 3. Frozen Contract

The authoritative contract is:

```text
artifacts/Configuration/ADP-v2.4/non-counted-rag-dry-run-contract.json
```

The frozen dry run uses:

- Validation instance: `http://127.0.0.1:3001`
- Model: `Llama 3.2 3B RAG Deterministic Test`
- Model id: `llama-32-3b-rag-deterministic-test`
- Base model: `llama3.2:3b`
- Temperature: `0`
- Seed: `42`
- Collection name: `ADP-v2.4-AURORA-24-KITE-Non-Counted`
- Source: `artifacts/Test-Data/ADP-v2.4/adp24_bounded_multi_fact_source.md`
- Source SHA-256: `18dc6a195e566da27dd4fe4be525d716a32dd0c753b6f1890c9c2ad7c3e12cfd`
- Selected provisional case: `C`
- Prompt: `State the verification color and review window for AURORA-24-KITE.`
- Expected factual answer: `The verification color for AURORA-24-KITE is amber, and the review window is thirty-six hours.`

Allowed non-counted citation classifications are `ABSENT`, `NUMERIC_BRACKET`, and `SOURCE_ID_BRACKET`. These are observations for procedure design and are not yet counted-run acceptance criteria.

## 4. Required Prior Evidence

The following prior evidence must remain present and unchanged:

```text
10-restart-before.txt SHA256=86626ad992356b49eb9cbe8cf0c6624b09f7b5b6718d017c7a5a197eda23dd67
11-restart-after.txt SHA256=3acfc43ccccc317259a80ccb0eb23d692327e9e2bf5ad55284cc1261ad68306c
STABLE_STATE_SHA256=ff524630a4c95728017f80cc5728aff5c70796db663ec833653071c7c3a73d60
POST_IMPORT_BACKUP_SHA256=93e615d0e7c0fae2c30b6f7d77b14437f76df76ef3278dfafb2d3e1a57928b12
```

The repository, `main`, `origin/main`, and the procedure-freeze tag must resolve to the promoted procedure-freeze commit before execution is authorized.

## 5. Required Evidence Files

The following files are required and must not exist before the run:

1. `12-non-counted-source-upload.png`
2. `13-non-counted-collection-ready.png`
3. `14-non-counted-response-raw.txt`
4. `15-non-counted-response-normalized.txt`
5. `16-non-counted-validator-report.txt`
6. `17-non-counted-source-panel.png`

All files must be created inside the active corrected evidence workspace. Text evidence must have mode `600`. Screenshots must be validated as PNG files and changed to mode `600`.

## 6. Five-Pass Readiness Requirement

Before Knowledge upload or dry-run execution is separately authorized, complete and retain a five-pass readiness record under:

```text
docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md
```

All five passes must independently report `PASS` for the same reviewed attempt. Any correction restarts the review at Pass 1. This procedure freeze does not itself authorize execution.

## 7. Pre-Execution Gate

Before opening the Knowledge interface:

1. Confirm the repository and procedure-freeze tag are synchronized.
2. Confirm the active evidence directory is ignored by Git.
3. Confirm evidence files 12 through 17 are absent.
4. Confirm the restart evidence hashes and stable-state hash.
5. Confirm the post-import backup checksum.
6. Confirm both Open WebUI instances are healthy.
7. Confirm exactly one administrator and one active target model.
8. Confirm model temperature `0`, seed `42`, no system prompt, no model-level Knowledge, tools, skills, functions, filters, files, or access grants.
9. Confirm the source, test-case, template, model-record, and contract hashes.
10. Confirm Web Search and optional tools will remain disabled.

Any failed precondition stops the run.

## 8. Single Authorized Human Workflow

1. Open only `http://127.0.0.1:3001`.
2. Use the validation instance Knowledge interface to create exactly one collection named `ADP-v2.4-AURORA-24-KITE-Non-Counted`.
3. Upload exactly `adp24_bounded_multi_fact_source.md` from the repository test-data directory.
4. Do not upload any other file.
5. After the exact source is accepted, capture `12-non-counted-source-upload.png` with the source filename visible.
6. Wait until the source is ready for retrieval.
7. Start one fresh chat.
8. Select `Llama 3.2 3B RAG Deterministic Test`.
9. Attach the exact collection to the fresh chat only. Do not attach Knowledge at model level.
10. Confirm Web Search and optional tools are disabled.
11. Before submitting a prompt, capture `13-non-counted-collection-ready.png` showing the fresh chat and exact attached collection.
12. Submit exactly once: `State the verification color and review window for AURORA-24-KITE.`
13. Do not edit, regenerate, retry, or submit another prompt.
14. Copy only the complete assistant response text into `14-non-counted-response-raw.txt`. Do not add source-panel labels, commentary, or corrections.
15. Expand the source panel and capture `17-non-counted-source-panel.png` showing the retrieved source and filename.
16. Run the frozen response classifier to create evidence 15 and 16.
17. Stop and return all six evidence hashes, the classifier result, runtime health, primary health, and repository cleanliness.

## 9. Raw Response Capture

Use a restrictive umask. The operator may create the raw text file with:

```bash
umask 077
cat > "$EVIDENCE_DIR/14-non-counted-response-raw.txt"
```

Paste the exact assistant response, press Enter once if needed, and press `Ctrl-D` on a new line. Do not reopen or edit the file after classification begins.

## 10. Frozen Classifier Command

```bash
set -o pipefail

python3 scripts/adp24_validate_non_counted_rag_response.py \
  --contract artifacts/Configuration/ADP-v2.4/non-counted-rag-dry-run-contract.json \
  --raw "$EVIDENCE_DIR/14-non-counted-response-raw.txt" \
  --normalized-output "$EVIDENCE_DIR/15-non-counted-response-normalized.txt" \
  2>&1 | tee "$EVIDENCE_DIR/16-non-counted-validator-report.txt"

VALIDATOR_EXIT="${PIPESTATUS[0]}"
```

The validator classifies factual content and citation shape. It does not inspect the source panel; source-panel validation remains a separate evidence review.

## 11. Result Classification

A dry-run candidate passes technical classification only when:

- The exact factual answer is present with no unsupported commentary.
- The citation classification is one of the three frozen observational classes.
- The source panel shows the exact synthetic source.
- The model, collection, runtime, primary instance, and repository remain within the frozen boundary.
- All six evidence files exist, validate, and have recorded hashes.

A nonzero validator exit, unsupported response shape, wrong fact, missing source, wrong source, multiple sources, `NOT FOUND`, model drift, association drift, or missing evidence is a non-counted failure. Preserve the attempt and do not retry.

## 12. Immediate Stop Conditions

Stop without improvisation for:

- Repository or tag mismatch
- Missing or changed prior evidence
- Backup checksum failure
- Evidence collision
- Wrong validation URL
- Primary-instance degradation
- Validation-container terminal state
- Wrong administrator or model count
- Model parameter or association drift
- Wrong collection name
- Wrong or additional source file
- Prompt submitted before evidence 13
- More than one prompt submission
- Regeneration, retry, or response editing
- Missing or wrong source-panel evidence
- Unexpected repository change

## 13. Post-Run Hold

```text
NON_COUNTED_RAG_DRY_RUN_RESULT=HOLD_PENDING_EVIDENCE_REVIEW
FINAL_PROMPT_FREEZE=HOLD
FINAL_EXPECTED_ANSWER_FREEZE=HOLD
FINAL_CITATION_POLICY_FREEZE=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```
