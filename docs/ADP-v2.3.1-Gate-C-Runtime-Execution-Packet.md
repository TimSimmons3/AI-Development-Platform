# ADP v2.3.1 Gate C Fresh Runtime Execution Packet

## 1. Packet Control

- Packet ID: `V231-C-RUNTIME-02`
- Supersedes: `V231-C-RUNTIME-01` operator execution procedure
- Status: Approved after process-hardening promotion
- Scope: Full reset, one-time setup, and three independent Gate C runs
- Model: `llama3.2:3b`
- Collection: `ADP-v2.3.1-minimal-direct-retrieval`
- Source: `adp231_minimal_direct_retrieval.md`
- Prompt: `V231-R01-P1-v2`
- Canonical script:
  - `scripts/adp231_gate_c_fresh_runtime.sh`
- Governing standards:
  - `docs/ADP-Controlled-Execution-Packet-Standard.md`
  - `docs/ADP-Final-Delivery-Validation-Standard.md`
  - `docs/ADP-Test-Execution-Consistency-and-Evidence-Lifecycle-Standard.md`

## 2. First-Attempt Status

The earlier attempted Gate C runtime workflow is:

- `VOIDED_NOT_COUNTED`

Counted runs completed:

- 0

Do not reuse its evidence or external-system state.

## 3. Procedure Freeze

The procedure is frozen when:

- The process-hardening package is committed and pushed.
- `HEAD`, `main`, and `origin/main` are aligned.
- The working tree is clean.
- The canonical script and guide checksums pass.
- The process-quality gate passes.

Any material change after a run begins voids that run.

## 4. Reset

Run:

```bash
bash "$HOME/Labs/AI-Development-Platform/scripts/adp231_gate_c_fresh_runtime.sh" reset
```

The reset shall:

- Revalidate the repository and runtime boundary.
- Archive the old evidence workspace.
- Archive loose and superseded operator artifacts.
- Create a cleanup manifest.
- Verify active-workspace cleanup.
- Create a fresh evidence workspace.
- Copy and checksum the source and prompt.
- Create fresh record templates.
- Record the synchronized repository baseline.

Required fields:

- `FIRST_ATTEMPT_STATUS=VOIDED_NOT_COUNTED`
- `FIRST_ATTEMPT_FOLDER_CLEANUP_STATUS=PASS`
- `SUPERSEDED_ARTIFACT_CLEANUP_STATUS=PASS`
- `LOCAL_EVIDENCE_RESET_STATUS=PASS`
- `WEBUI_RESET_REQUIRED=YES`

## 5. Open WebUI Reset

The operator shall:

1. Delete all chats created for the voided attempt.
2. Delete the current Gate C collection.
3. Prove the collection is absent.
4. Recreate the exact collection.
5. Upload only the source from the new setup folder.
6. Prove exactly one file is present.

Setup evidence:

- `setup/01-prior-collection-absent.png`
- `setup/02-new-collection-one-file.png`

Verify with:

```bash
bash "$HOME/Labs/AI-Development-Platform/scripts/adp231_gate_c_fresh_runtime.sh" setup-verify
```

## 6. Counted Runs

For each run N, capture before prompt submission:

- `run-N/01-membership-before-run.png`
- `run-N/02-fresh-empty-chat.png`
- `run-N/03-collection-attached-before-prompt.png`

Start with:

```bash
bash "$HOME/Labs/AI-Development-Platform/scripts/adp231_gate_c_fresh_runtime.sh" run-start N
```

Submit the frozen prompt exactly once.

After the response, save:

- `run-N/response.txt`
- `run-N/04-complete-response.png`
- `run-N/05-displayed-source-panel.png`

Finish with:

```bash
bash "$HOME/Labs/AI-Development-Platform/scripts/adp231_gate_c_fresh_runtime.sh" run-finish N
```

## 7. Automatic Continuation

Proceed to the next run only when:

- `OVERALL_RUN_STATUS=PASS`
- No stop condition occurred
- The procedure and script remain unchanged
- The evidence is complete
- The repository and runtime boundary remain unchanged

No intermediate approval is required between successful runs.

## 8. Stop and Void Conditions

Stop immediately for:

- FAIL or INCONCLUSIVE
- Prompt truncation
- Missing evidence
- Wrong model, file, collection, or prompt
- Unsupported or automation output
- Source evidence unavailable
- Repository or runtime drift

Void the run and reset when:

- Script logic changes
- Evidence requirements or filenames change
- Scoring or prompt changes
- Operator instructions change materially
- A required state was not frozen before run start

## 9. Completion

After three PASS results:

```bash
bash "$HOME/Labs/AI-Development-Platform/scripts/adp231_gate_c_fresh_runtime.sh" package
```

Return the evidence archive and checksum.

## 10. Exclusions

This packet does not authorize:

- Prompt revision
- Same-chat retry
- Model comparison
- Multi-file expansion
- Formatting qualification
- Cleanup or removal validation
- Runtime configuration changes
- ADP v2.4 work
