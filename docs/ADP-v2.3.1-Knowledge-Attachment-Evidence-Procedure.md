# ADP v2.3.1 Knowledge Attachment Evidence Procedure

## 1. Document Control

- Project: AI Development Platform
- Release: ADP v2.3.1
- Status: Approved for controlled repository promotion
- Repository baseline represented: `253e9dd`
- Planned canonical path:
  - `docs/ADP-v2.3.1-Knowledge-Attachment-Evidence-Procedure.md`
- Applies to:
  - `V231-R01`
  - `V231-S01`

## 2. Purpose

Provide repeatable evidence that the approved Knowledge collection contains exactly one approved file and is visibly attached to the intended fresh chat before each counted Gate C run.

## 3. Required Collection and Source

Collection name:

- `ADP-v2.3.1-minimal-direct-retrieval`

The name must be used exactly.

The collection must contain exactly one file:

- `adp231_minimal_direct_retrieval.md`

Approved source SHA-256:

- `ea0288d0d8666438e8cf9ae7dd54e6da8aaa0818f42d15f29bdf7467acf77afc`

No other file may be present.

## 4. Authorization Boundary

Do not create the collection, upload the file, or submit a prompt until:

1. All approved Gate C artifacts are promoted to canonical repository paths.
2. ASCII, Markdown, identifier, and checksum validation pass.
3. The Git diff is reviewed.
4. The artifacts are committed and pushed.
5. `HEAD`, `main`, and `origin/main` are aligned.
6. The working tree is clean.
7. The final pre-runtime gate is recorded as passed.

## 5. Per-Run Collection-Membership Evidence

Immediately before each counted run:

1. Open the approved collection details.
2. Confirm the collection name exactly matches the required name.
3. Confirm exactly one file is listed.
4. Confirm the listed filename exactly matches `adp231_minimal_direct_retrieval.md`.
5. Capture a screenshot that shows the collection name and complete file membership.
6. Reference the screenshot in the run record.

Do not reuse a membership screenshot from another counted run.

If the collection name or complete one-file membership cannot be shown, classify the attempt INCONCLUSIVE and do not submit the prompt.

## 6. Per-Run Fresh-Chat Evidence

Immediately before each counted run:

1. Start a new chat.
2. Confirm the message area is empty.
3. Confirm no prior messages appear.
4. Confirm `llama3.2:3b` is selected.
5. Confirm no tool, web, function, terminal, or automation feature is enabled in the chat.
6. Capture a screenshot showing the empty fresh chat and selected model.
7. Reference the screenshot in the run record.

If fresh-chat state cannot be proven, classify the attempt INCONCLUSIVE and do not submit the prompt.

## 7. Per-Run Attachment Evidence

Before submitting the prompt:

1. Attach the exact collection `ADP-v2.3.1-minimal-direct-retrieval` to the fresh chat.
2. Verify the collection name is visibly associated with the current chat.
3. Capture a screenshot showing the current fresh chat, selected model, and attached collection.
4. Reference the screenshot in the run record.

If attachment state is not visible, classify the attempt INCONCLUSIVE and do not submit the prompt.

Do not infer attachment from a previous chat, a prior run, or later displayed-source evidence.

## 8. Exact Run-Window Start

After all pre-run screenshots are saved and immediately before prompt submission, capture the exact local run-start timestamp:

```bash
RUN_START="$(date '+%Y-%m-%d %H:%M:%S')"
printf 'RUN_START=%s\n' "$RUN_START"
```

Record the printed timestamp in the run record.

## 9. Prompt Submission

Submit approved prompt `V231-R01-P1-v2` exactly once.

Do not:

- Edit after submission
- Add a follow-up instruction
- Retry in the same chat
- Correct the response
- Switch models
- Change the collection
- Add a file
- Enable a tool or automation feature

## 10. Response and Displayed-Source Evidence

Immediately after the response:

1. Preserve the complete response without correction.
2. Capture a screenshot showing the complete response.
3. Open or display the source evidence associated with the response.
4. Record the displayed source filename.
5. Record the displayed source passage.
6. Record source order and retrieval score if exposed.
7. Capture a screenshot showing enough interface context to prove the response-to-source relationship.
8. Reference all evidence in the run record.

If displayed-source evidence cannot be captured, classify `V231-S01` as INCONCLUSIVE and stop the run block.

## 11. Exact Bounded Truncation Check

Immediately after evidence capture, record the local run-end timestamp and query only the exact run window:

```bash
RUN_END="$(date '+%Y-%m-%d %H:%M:%S')"
printf 'RUN_END=%s\n' "$RUN_END"
journalctl -u ollama --since "$RUN_START" --until "$RUN_END" --no-pager | awk '/truncating input prompt/ {print; count++} END {printf "TRUNCATION_WARNING_COUNT=%d\n", count+0}'
```

Retain:

- `RUN_START`
- `RUN_END`
- Every matching warning line
- `TRUNCATION_WARNING_COUNT`

A new matching warning makes the run FAIL and triggers an immediate stop before another prompt is submitted.

If the bounded log evidence is unavailable or ambiguous, classify the attempt INCONCLUSIVE and stop the run block.

## 12. Block Execution and Automatic Continuation

The three counted runs are executed within one runtime execution packet.

After run 1 or run 2, proceed directly to the next fresh-chat run without external approval only when:

- The current run is PASS.
- Required evidence is complete.
- No stop condition occurred.
- No controlled variable changed.

Do not pause merely to report a successful run. A FAIL or INCONCLUSIVE result stops the block immediately.

## 13. Independence Requirement

Each counted run must use:

- A new chat
- A new collection-membership screenshot
- A new fresh-chat screenshot
- A new attachment screenshot
- A new response and source-evidence set
- A new exact bounded log window
- The same model
- The same collection
- The same file
- The same frozen prompt

No per-run evidence may be reused to prove another counted run.

## 14. Stop Conditions

Stop before or during the block when:

- Collection membership cannot be proven
- Attachment state cannot be proven
- Fresh-chat state cannot be proven
- More than one file is present
- The wrong model is selected
- A tool, web, function, terminal, automation, reminder, or scheduling feature is enabled
- The prompt is altered
- A new truncation warning appears
- Automation, reminder, scheduling, or iCalendar output appears
- Displayed-source evidence cannot be captured
- A runtime, network, repository, or recoverability variable changes
- Real or sensitive data is introduced

## 15. Hold Point

This procedure is approved for controlled repository promotion only.

It does not authorize collection creation, file upload, prompt execution, model comparison, configuration change, or ADP v2.4 work until the final pre-runtime gate passes.
