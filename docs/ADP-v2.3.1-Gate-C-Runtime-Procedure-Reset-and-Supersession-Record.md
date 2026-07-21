# ADP v2.3.1 Gate C Runtime Procedure Reset and Supersession Record

## 1. Document Control

- Project: AI Development Platform
- Release: ADP v2.3.1
- Record type: Runtime procedure reset and supersession
- Status: Approved for controlled repository promotion
- Canonical path:
  - `docs/ADP-v2.3.1-Gate-C-Runtime-Procedure-Reset-and-Supersession-Record.md`
- First attempted runtime block:
  - VOIDED
  - NOT COUNTED
- Counted Gate C runs completed:
  - 0

## 2. Reason for Reset

The first attempted runtime workflow encountered procedure and evidence-design changes after preparation began.

Observed control defects included:

- Duplicate evidence requirements
- Filename reuse and collision
- Ambiguous distinction between setup, pre-run, and post-response screenshots
- Manual source-text files that could be confused with expected rather than observed evidence
- Multiple active scripts and guides
- In-progress patching and resume instructions
- Incomplete active-workspace cleanup

Continuing would not provide a stable, repeatable, or audit-ready test.

## 3. Decision

The first attempt is:

- `VOIDED_NOT_COUNTED`

Do not score, resume, rename, patch, or reuse its chats, timestamps, screenshots, prompts, responses, or evidence.

## 4. Required Reset

Before a counted run:

1. Archive the prior evidence workspace.
2. Archive loose first-attempt screenshots and duplicate upload files.
3. Archive superseded scripts, toolkits, checksums, and guides.
4. Retain a cleanup manifest.
5. Verify the active Downloads directory no longer contains known superseded artifacts.
6. Delete voided-attempt Open WebUI chats.
7. Delete and recreate the Gate C Knowledge collection.
8. Upload the source from the new evidence workspace.
9. Capture fresh setup evidence.
10. Start Run 1 with fresh independent evidence.

## 5. Authoritative Runtime Artifacts

Current script:

- `scripts/adp231_gate_c_fresh_runtime.sh`

Current operator guide:

- `docs/ADP-v2.3.1-Gate-C-Fresh-Runtime-Operator-Guide.md`

Current cross-release standard:

- `docs/ADP-Test-Execution-Consistency-and-Evidence-Lifecycle-Standard.md`

All earlier Gate C runtime scripts, toolkits, and guides are superseded.

## 6. Evidence Filenames

Each counted run uses:

1. `01-membership-before-run.png`
2. `02-fresh-empty-chat.png`
3. `03-collection-attached-before-prompt.png`
4. `response.txt`
5. `04-complete-response.png`
6. `05-displayed-source-panel.png`

No filename is reused for another purpose.

The current process does not require `source-filename.txt` or `source-passage.txt`.

## 7. Runtime Authorization

Runtime may restart only after:

- Process-hardening promotion passes.
- The repository is clean and synchronized.
- The reset command passes.
- Open WebUI chats and collection are reset.
- Setup verification passes.
- The procedure remains unchanged.

Any later material change voids the affected run and requires another reset.
