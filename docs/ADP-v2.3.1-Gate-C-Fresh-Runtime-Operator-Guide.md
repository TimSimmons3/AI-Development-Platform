# ADP v2.3.1 Gate C Fresh Runtime Operator Guide

## Current Status

- First attempt: `VOIDED_NOT_COUNTED`
- Counted runs: 0
- Current packet: `V231-C-RUNTIME-02`
- Current script: `scripts/adp231_gate_c_fresh_runtime.sh`
- Earlier scripts and guides: superseded

## Rule

Use only this guide and the canonical script.

Do not reuse old chats, screenshots, files, timestamps, or evidence.

Do not patch a run after it starts. A material change means the run is void and the process restarts.

## Step 1 - Reset

From the repository:

```bash
bash scripts/adp231_gate_c_fresh_runtime.sh reset
```

The script archives old active material, creates a cleanup manifest, and creates a new evidence workspace.

Do not continue unless all cleanup and reset fields are PASS.

## Step 2 - Reset Open WebUI

1. Delete every chat created for the voided attempt.
2. Delete `ADP-v2.3.1-minimal-direct-retrieval`.
3. Return to the Knowledge list.
4. Save proof that the collection is absent as:
   - `setup/01-prior-collection-absent.png`
5. Recreate `ADP-v2.3.1-minimal-direct-retrieval`.
6. Upload only the source from the new setup folder printed by the script.
7. Save proof of exactly one file as:
   - `setup/02-new-collection-one-file.png`

Verify:

```bash
bash scripts/adp231_gate_c_fresh_runtime.sh setup-verify
```

## Step 3 - Run N

Before the prompt, save:

- `01-membership-before-run.png`
- `02-fresh-empty-chat.png`
- `03-collection-attached-before-prompt.png`

Start:

```bash
bash scripts/adp231_gate_c_fresh_runtime.sh run-start N
```

Submit the printed prompt exactly once.

After the response, save:

- `response.txt`
- `04-complete-response.png`
- `05-displayed-source-panel.png`

Finish:

```bash
bash scripts/adp231_gate_c_fresh_runtime.sh run-finish N
```

Proceed only after PASS.

## Step 4 - Package

After Run 3 PASS or immediately after a stop:

```bash
bash scripts/adp231_gate_c_fresh_runtime.sh package
```

## Stop

Stop for any FAIL, INCONCLUSIVE, missing evidence, truncation, drift, or material procedure change.

Do not create `source-filename.txt` or `source-passage.txt`.

Do not reuse filenames for another purpose.
