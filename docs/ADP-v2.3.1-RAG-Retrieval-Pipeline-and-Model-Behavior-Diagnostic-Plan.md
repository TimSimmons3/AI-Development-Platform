# ADP v2.3.1 RAG Retrieval-Pipeline and Model-Behavior Diagnostic Plan

## 1. Document Control

- Project: AI Development Platform
- Release: ADP v2.3.1
- Release title: RAG Retrieval-Pipeline and Model-Behavior Diagnostic
- Status: Approved with conditions
- Canonical repository: `~/Labs/AI-Development-Platform`
- Branch: `main`
- Canonical repository path:
  - `docs/ADP-v2.3.1-RAG-Retrieval-Pipeline-and-Model-Behavior-Diagnostic-Plan.md`
- Current location: Approved outside the repository for controlled promotion
- Predecessor release: ADP v2.3
- ADP v2.4 status: BLOCKED

## 2. Authorization Boundary

This approved plan authorizes controlled promotion to the canonical repository path. It does not yet authorize runtime diagnostic work.

Runtime work may begin only after:

1. The approved plan is copied to the canonical repository path.
2. Markdown structure and ASCII-only content are validated.
3. The plan is committed and pushed.
4. `HEAD`, `main`, and `origin/main` are confirmed aligned.
5. The working tree is confirmed clean.
6. Gate B passes.

Until then, do not:

- Create or modify an Open WebUI Knowledge collection
- Upload diagnostic files
- Attach Knowledge to a chat
- Run diagnostic prompts
- Change model or runtime settings
- Install or download models
- Upgrade Open WebUI or Ollama
- Change Docker networking or firewall rules
- Delete or replace the Open WebUI Docker volume
- Use real, sensitive, confidential, privileged, or regulated data
- Begin ADP v2.4 work

## 3. Source of Truth

The release shall use these committed records as authoritative predecessor evidence:

- `docs/ADP-v2.3-Final-Recoverability-Record.md`
- `docs/ADP-v2.3-Closeout.md`
- `docs/ADP-v2.3-Remediation-Decision-Record.md`
- `docs/ADP-v2.3-RAG-Hardening-Validation-Report.md`
- `docs/ADP-v2.3-T01-Controlled-Test-Evidence-Record.md`
- `docs/ADP-v2.3-Administrative-Knowledge-Cleanup-Record.md`
- `docs/ADP-RAG-Prompt-Control-Standard.md`
- `docs/ADP-RAG-Removal-Validation-Procedure.md`
- `docs/ADP-Engineering-Log.md`

Validated predecessor baseline:

- Branch: `main`
- Final recoverability commit: `f4641da`
- `HEAD`: `f4641da`
- `main`: `f4641da`
- `origin/main`: `f4641da`
- Working tree: clean
- Open WebUI image: `ghcr.io/open-webui/open-webui:v0.10.2`
- Binding: `127.0.0.1:3000->8080/tcp`
- Ollama version: `0.30.11`
- Approved models:
  - `llama3.2:1b`
  - `llama3.2:3b`
- Final Timeshift snapshot:
  - Identifier: `2026-07-20_11-32-48`
  - Actual description: `ADP-v2.3-reg-hardening-t01-failure-closeout`
- Prior collection:
  - `ADP-v2.3-synthetic-rag-hardening`
  - Entry status: absent, confirmed by manual user review

## 4. Predecessor Failure Position

ADP v2.3 closed as a controlled failed RAG hardening release.

Observed failures included:

- Intermittent correct retrieval
- Wrong-passage selection from the correct source
- Unrelated automation and iCalendar output
- Correct content in an unauthorized structure
- Unauthorized prefaces and format deviations
- Invented or unsupported source content
- Unsupported claims about machine-learning training data and algorithm evaluation
- Inconsistent displayed-source evidence capture
- Non-reproducible behavior

T01 exhausted its maximum three controlled prompt revisions. T01 shall not be reopened under v2.3.

## 5. Release Purpose

ADP v2.3.1 shall determine, with bounded and reproducible evidence, whether the v2.3 failures originated from one or more of the following:

1. Knowledge attachment or chat-state uncertainty
2. Retrieval failure
3. Wrong-chunk or wrong-passage ranking
4. Prompt-routing or interface-state contamination
5. Model instruction-following limitations
6. Unsupported outside knowledge
7. Displayed-source evidence limitations
8. Interaction among the approved model, Open WebUI, and the configured Knowledge path
9. A cause that cannot be isolated within the approved platform boundary

This is a diagnostic release. It is not a qualification, production-readiness, or v2.4 promotion release.

## 6. Objectives

The release shall:

- Verify Knowledge attachment state before every counted run.
- Isolate direct retrieval using one minimal synthetic file.
- Determine whether the correct passage is retrieved consistently.
- Determine whether displayed source evidence is present and correct.
- Separate retrieval correctness from output-format compliance.
- Test whether unsupported outside knowledge appears.
- Determine whether unrelated automation output is linked to chat state, routing, interface state, or model behavior.
- Compare `llama3.2:1b` and `llama3.2:3b` only if separately authorized.
- Produce an evidence-backed root-cause conclusion or bounded residual-risk statement.
- Preserve recoverability and the localhost-only security boundary.

## 7. Governing Principles

- Synthetic, non-sensitive data only
- Localhost-only operation
- Existing approved Open WebUI image only
- Existing approved Ollama version only
- Existing approved models only
- One controlled variable changed at a time
- Fresh chat for every independent run
- Exact prompt retention
- Full response retention
- Displayed source-evidence capture
- Timestamp, model, collection, and attachment-state retention
- No silent correction or reinterpretation of failed output
- No reuse of a failed chat as an independent rerun
- No prompt optimization during a frozen test block
- No v2.4 promotion based on partial or intermittent success
- Immediate stop on safety, evidence-integrity, or boundary violations

## 8. In Scope

After plan approval and repository synchronization:

- Read-only baseline validation
- Read-only Open WebUI and container log inspection
- Creation of one uniquely named synthetic diagnostic Knowledge collection
- Upload of one minimal synthetic diagnostic file
- Verification of attachment state before each run
- Fresh-chat direct retrieval testing
- Displayed-source evidence capture
- Wrong-passage isolation
- Exact-format testing after retrieval is demonstrated
- Unsupported-knowledge resistance testing
- Chat-state and prompt-routing isolation
- Optional comparison of the two already-approved models
- One-file-at-a-time bounded corpus expansion
- Administrative cleanup
- Approved removal validation
- Closeout and recoverability work

## 9. Exclusions

- ADP v2.4 qualification or implementation
- New model installation, download, or replacement
- Open WebUI or Ollama upgrade
- External vector database
- API or automated ingestion
- Multi-user access
- Docker host networking
- Firewall changes
- LAN or Internet exposure
- Open WebUI Docker volume deletion or replacement
- Production deployment
- Real business, client, legal, financial, medical, personnel, contract, or production data
- PII, credentials, secrets, tokens, passwords, confidential data, or regulated data

## 10. Diagnostic Questions

- DQ-01: Can the operator prove the intended Knowledge collection is attached before every run?
- DQ-02: Can one exact fact be retrieved from one minimal file in three of three fresh chats?
- DQ-03: Does each run show the correct source file and passage?
- DQ-04: Can the system avoid wrong-passage selection within a multi-fact file?
- DQ-05: After retrieval passes, can the model meet the exact output structure?
- DQ-06: Does the model introduce claims absent from displayed source evidence?
- DQ-07: Can unrelated automation, reminder, scheduling, or iCalendar output be reproduced?
- DQ-08: Does behavior differ between confirmed fresh chat and reused chat state?
- DQ-09: If authorized, do the two approved models behave materially differently?
- DQ-10: Does behavior remain stable as approved synthetic files are added one at a time?
- DQ-11: After cleanup, is the collection absent and removed content unavailable under the approved procedure?

## 11. Hypotheses

- H1: The intended Knowledge collection was not consistently attached.
- H2: Retrieval returned no source context, causing an answer from model knowledge.
- H3: Retrieval returned the correct file but ranked the wrong passage.
- H4: Retrieval was correct, but the model failed grounding or format instructions.
- H5: Reused chat or interface state introduced unrelated automation behavior.
- H6: Prompt routing or tool behavior introduced unrelated automation output.
- H7: Displayed-source evidence was incomplete even when retrieval occurred.
- H8: One approved model is materially more stable than the other.
- H9: The failure cannot be isolated without an out-of-scope platform change.

Each hypothesis shall be classified:

- Supported
- Partially supported
- Not supported
- Not testable within scope
- Inconclusive

## 12. Required Run Evidence

Record for every run:

- Release identifier
- Test identifier
- Run number
- Local timestamp
- Host
- Open WebUI image, status, and binding
- Ollama version
- Model
- Fresh-chat evidence
- Knowledge collection name
- Attachment confirmation method
- Source file name and SHA-256
- Prompt identifier and exact prompt
- Full response
- Displayed source file
- Displayed source passage
- Displayed source order
- Retrieval score, if exposed
- Result
- Failure classification
- Evidence-file reference
- Operator notes

No unrecorded variable change is permitted within a repeated block.

## 13. Minimal Synthetic Data Design

The first diagnostic file shall be:

- Plain text or Markdown
- Small and manually reviewable
- Synthetic and non-sensitive
- Written with unique identifiers
- Free of ambiguous synonyms
- Free of external factual dependencies
- Free of tool, reminder, calendar, or scheduling syntax
- Checksummed before upload

It shall contain:

- One unique platform identifier
- One exact release objective
- One exact owner or role label
- One distinct non-target fact
- One explicit prohibition

It shall not contain:

- Machine-learning training claims
- Algorithm-evaluation claims
- Calendar or reminder syntax
- Tool instructions
- Real names or organizations
- Credentials or sensitive information

No second file may be added until the single-file direct-retrieval gate passes.

## 14. Test Sequence

### Phase 0: Plan and Repository Gate

Required:

- Plan approved
- Plan copied to canonical path
- ASCII scan passed
- Markdown heading review passed
- Git diff reviewed
- Plan committed and pushed
- `HEAD`, `main`, and `origin/main` aligned
- Working tree clean

No runtime work before Phase 0 passes.

### Phase 1: Read-Only Baseline

Activities:

- Revalidate Git state
- Revalidate Open WebUI image, binding, and health
- Revalidate Ollama and approved models
- Reconfirm the prior collection remains absent
- Inspect approved read-only logs
- Confirm no prohibited drift

Pass:

- Baseline matches the release boundary
- Evidence record complete

Stop:

- Runtime drift
- Unexpected model
- Non-localhost binding
- Missing predecessor evidence
- Unexplained Knowledge collection
- Inability to capture baseline evidence

### Phase 2: Single-File Direct Retrieval

Activities:

- Create one uniquely named collection
- Upload one approved minimal file
- Record checksum and collection membership
- Confirm attachment before every run
- Execute one frozen direct-retrieval prompt in three fresh chats
- Capture complete response and source evidence

Pass:

- Three of three exact target facts
- Three of three correct source files
- Three of three correct passages
- Zero unsupported claims
- Zero automation or scheduling output

Failure handling:

- Do not revise the prompt during the block
- Preserve and classify every result
- Stop after the third run
- Apply the Gate C decision

### Phase 3: Wrong-Passage Isolation

Entry: Phase 2 passed.

Activities:

- Use the approved multi-fact design
- Ask an unambiguous question targeting one passage
- Run three fresh chats
- Capture source order and score if exposed

Pass:

- Three of three correct passages
- Zero wrong-passage selections
- Correct displayed source evidence every time

### Phase 4: Format and Grounding Isolation

Entry: Phase 3 passed.

Activities:

- Use the proven target fact
- Require a small exact structure
- Run three fresh chats
- Separately test unsupported-knowledge resistance

Pass:

- Three of three exact structures
- No unauthorized preface or extra section
- No missing field
- No unsupported claim
- Correct source evidence every time

### Phase 5: Automation and Chat-State Isolation

Entry: Phase 2 completed and continuation is safe.

Activities:

- Confirm fresh chat before each run
- Use no date, reminder, scheduling, or calendar language
- Attempt to reproduce the unrelated automation output
- Compare with preserved v2.3 evidence
- Inspect read-only logs immediately if it appears

Pass:

- No unrelated automation, reminder, scheduling, or iCalendar output in three fresh chats

Immediate stop:

- If automation output appears, stop prompt execution and preserve UI and log evidence before another run.

### Phase 6: Optional Approved-Model Comparison

This phase is not automatically authorized.

A separate explicit approval entry is required.

Controls:

- Same file
- Same collection
- Same prompt
- Same Open WebUI configuration
- Same evidence method
- One model changed at a time

Allowed models only:

- `llama3.2:1b`
- `llama3.2:3b`

Minimum:

- Three fresh-chat runs per model

The comparison is diagnostic only and shall not promote or replace a model.

### Phase 7: Bounded Corpus Expansion

Entry:

- Phases 2, 3, and 4 passed
- No unresolved automation condition
- Evidence capture stable

Activities:

- Add one synthetic file at a time
- Revalidate after each addition
- Stop at the first unexplained regression
- Do not exceed five files without a new plan

Pass at each step:

- Three of three correct retrievals
- Correct file and passage every run
- No unsupported knowledge
- No wrong-passage selection
- Stable structure
- No automation output

### Phase 8: Cleanup and Removal

Activities:

- Remove the diagnostic collection by the approved method
- Confirm collection absence
- Confirm no unrelated collection was removed
- Execute the approved removal-validation procedure only when authorized
- Do not delete or replace the Open WebUI volume

Classify separately:

- Administrative cleanup
- Removal validation

Cleanup alone shall not be represented as successful removal validation.

### Phase 9: Analysis and Closeout

Required:

- Evidence records
- Root-cause analysis
- Hypothesis disposition
- Residual-risk statement
- Validation report
- Remediation decision
- Cleanup or removal record
- Engineering log update
- Closeout
- Final recoverability record
- Confirmed Timeshift snapshot
- Clean synchronized Git state

## 15. Test Identifiers

- `V231-B00`: Entry and runtime baseline
- `V231-L01`: Read-only log review
- `V231-R01`: Single-file direct retrieval
- `V231-R02`: Wrong-passage selection
- `V231-F01`: Exact output structure
- `V231-G01`: Unsupported-knowledge resistance
- `V231-S01`: Displayed-source evidence stability
- `V231-C01`: Fresh-chat and chat-state isolation
- `V231-A01`: Automation-output isolation
- `V231-M01`: Optional model comparison
- `V231-X01`: Bounded corpus expansion
- `V231-RM01`: Administrative cleanup
- `V231-RM02`: Removal validation

## 16. Prompt Control and Revision Limits

- Each test block uses a frozen prompt identifier.
- The exact prompt is retained.
- No semantic revision is allowed during a three-run block.
- One typographical or demonstrable prompt defect may receive one corrective revision for the entire test identifier.
- A correction requires:
  - New prompt version
  - Written defect description
  - Written necessity
  - Invalidation of the affected block
  - New three-run block
- Prompt changes shall not conceal or reinterpret a failure.
- If the one correction fails, the test closes failed or inconclusive.
- v2.3 T01 prompt versions shall not be reused as proof of v2.3.1 qualification.

## 17. Acceptance Criteria

Diagnostic stability requires all of the following:

- Three of three correct direct retrieval runs in fresh chats
- Correct displayed source file every run
- Correct displayed source passage every run
- Zero wrong-passage selections
- Zero unrelated automation, reminder, scheduling, or iCalendar outputs
- Zero unsupported outside-knowledge claims
- Stable required output structure
- Repeatable attachment-state verification
- Complete evidence for every counted run
- Documented root cause or bounded residual-risk explanation
- Clean synchronized Git state
- Confirmed recoverability

These criteria do not authorize v2.4.

## 18. Failure and Inconclusive Rules

FAIL when:

- The returned fact is incorrect
- The correct file is shown but the wrong passage is used
- Source evidence conflicts with the answer
- Unsupported content is introduced
- Required structure is materially violated
- Unrelated automation or scheduling output appears
- The result is not reproducible

INCONCLUSIVE when:

- Attachment state cannot be proven
- Source evidence cannot be captured
- Runtime or UI state changes unexpectedly
- Required logs or screenshots are unavailable
- A variable changes within the block
- Retrieval failure cannot be distinguished from model behavior

Inconclusive results do not count as passes.

## 19. Stop Conditions

Stop runtime work immediately if:

- Real or sensitive data is introduced
- Open WebUI is exposed beyond localhost
- The approved image or Ollama version changes
- An unapproved model appears
- The Open WebUI volume is deleted or replaced
- Firewall or Docker networking changes
- Evidence integrity is lost
- Attachment state cannot be verified
- A prohibited variable changes
- Automation output appears before evidence is preserved
- A block reaches its run limit
- The permitted prompt correction is exhausted
- Repository or recoverability state becomes uncertain

After a stop:

1. Preserve evidence.
2. Do not retry immediately.
3. Record the condition.
4. Revalidate the baseline.
5. Obtain an explicit decision before continuing.

## 20. Root-Cause Classification

- RC-01: Knowledge attachment-state failure
- RC-02: Retrieval returned no relevant context
- RC-03: Wrong-file retrieval
- RC-04: Wrong-passage or chunk-ranking failure
- RC-05: Model instruction-following failure
- RC-06: Unsupported outside-knowledge use
- RC-07: Chat-state contamination
- RC-08: Prompt-routing or interface-state anomaly
- RC-09: Source-evidence display or capture limitation
- RC-10: Model-dependent instability
- RC-11: Multi-file scaling instability
- RC-12: Unresolved within approved scope

Every classification shall cite its exact supporting test and evidence.

## 21. Decision Gates

### Gate A: Plan Approval

Pass:

- Scope, exclusions, sequence, evidence, revision limits, and stop conditions approved

### Gate B: Repository and Runtime Baseline

Pass:

- Approved plan committed and pushed
- Git synchronized and clean
- Runtime baseline intact
- Prior collection absent
- No prohibited drift

### Gate C: Minimal Retrieval

Pass:

- `V231-R01` passes three of three
- `V231-S01` passes three of three

Fail:

- No corpus expansion
- Bounded analysis and explicit remediation or closeout decision

### Gate D: Passage, Format, and Grounding

Pass:

- `V231-R02`, `V231-F01`, and `V231-G01` pass
- No unresolved automation condition

### Gate E: Optional Model Comparison

Requires separate explicit approval.

### Gate F: Corpus Expansion

Pass:

- Gates C and D passed
- Evidence capture stable
- One-file-at-a-time expansion approved

### Gate G: Closeout and Recoverability

Pass:

- Evidence complete
- Hypotheses dispositioned
- Root cause or residual risk documented
- Cleanup complete
- Removal state accurately classified
- Engineering log updated
- Git synchronized
- Timeshift snapshot confirmed
- Final recoverability record complete

## 22. Planned Artifacts

- `docs/ADP-v2.3.1-RAG-Retrieval-Pipeline-and-Model-Behavior-Diagnostic-Plan.md`
- `docs/ADP-v2.3.1-Entry-and-Runtime-Baseline-Record.md`
- `docs/ADP-v2.3.1-Synthetic-Diagnostic-Data-Design.md`
- `docs/ADP-v2.3.1-Diagnostic-Prompt-Library.md`
- `docs/ADP-v2.3.1-Diagnostic-Test-Record-Template.md`
- `docs/ADP-v2.3.1-Diagnostic-Evidence-Record.md`
- `docs/ADP-v2.3.1-Root-Cause-Analysis.md`
- `docs/ADP-v2.3.1-Diagnostic-Validation-Report.md`
- `docs/ADP-v2.3.1-Remediation-Decision-Record.md`
- `docs/ADP-v2.3.1-Knowledge-Cleanup-and-Removal-Record.md`
- `docs/ADP-v2.3.1-Closeout.md`
- `docs/ADP-v2.3.1-Final-Recoverability-Record.md`
- Updated `docs/ADP-Engineering-Log.md`

Consolidation requires an approved amendment that preserves traceability.

## 23. Evidence Quality

Every counted run requires complete evidence. A run missing required evidence is INCONCLUSIVE.

Screenshots shall:

- Show enough interface context to establish state
- Avoid unnecessary personal information
- Use stable filenames
- Be referenced from the evidence record
- Not be cropped to remove material context

Logs shall be reviewed before Git commitment for credentials, tokens, or unnecessary personal data.

## 24. Change Control

A documented amendment is required before changing:

- Test order
- Model comparison authorization
- Prompt revision allowance
- Collection naming
- Synthetic data design
- Acceptance criteria
- Stop conditions
- Runtime version
- Open WebUI image
- Ollama version
- Network boundary
- Number of files
- Evidence fields
- Cleanup method

No implicit change is permitted.

## 25. Security and Privacy

Preserve:

- Localhost-only access
- Existing firewall posture
- Existing Docker binding
- Existing approved image
- Existing approved models
- Synthetic content only
- No credentials in prompts, files, screenshots, logs, or Git
- Minimum necessary evidence capture

## 26. Recoverability

Before runtime work:

- Confirm the final v2.3 Timeshift snapshot remains listed.
- Confirm Git is synchronized and clean.

At closeout:

- Create a new Timeshift snapshot with a reviewed description.
- Confirm the actual stored description.
- Record any variance without silently rewriting it.
- Confirm Git synchronization and clean status.
- Record final artifact checksums.
- Create the final recoverability record.

A snapshot does not substitute for committed evidence.

## 27. Permitted Release Outcomes

### Outcome 1: Diagnostic Stability Demonstrated

The minimal path meets every acceptance criterion. This supports planning a separate qualification release but does not authorize v2.4.

### Outcome 2: Root Cause Identified, Remediation Required

A bounded cause is supported, but acceptance criteria are not met. A separate remediation plan is required.

### Outcome 3: Model Limitation Identified

Retrieval is correct, but one or both approved models cannot reliably meet grounding or format controls. No new model is authorized.

### Outcome 4: Platform or Interface Limitation Identified

The approved Open WebUI path cannot provide stable attachment, routing, retrieval, or source evidence. A separate architecture or upgrade evaluation is required.

### Outcome 5: Inconclusive Within Scope

The cause cannot be isolated without prohibited changes. The release closes inconclusive with bounded residual risk. v2.4 remains blocked.

## 28. Initial Order After Approval

1. Create the entry and runtime baseline record.
2. Run read-only baseline validation.
3. Inspect approved read-only Open WebUI and container logs.
4. Draft and approve the minimal synthetic file.
5. Draft and approve the frozen diagnostic prompt.
6. Create the uniquely named diagnostic collection.
7. Upload only the approved file.
8. Execute the three-run direct-retrieval block.
9. Stop and assess Gate C before broader testing.

## 29. First Runtime Action

After the approved plan is committed and pushed, the first runtime diagnostic action shall be read-only inspection of the approved Open WebUI and container state.

No collection shall be created and no prompt shall be run until the baseline record is complete and Gate B passes.

## 30. Approval Record

Plan decision:

- [ ] APPROVED
- [x] APPROVED WITH CONDITIONS
- [ ] REVISE
- [ ] REJECTED

Optional model comparison:

- [x] NOT AUTHORIZED
- [ ] AUTHORIZED

Approver:

- Name or role: Project Owner
- Date: 2026-07-20
- Conditions: Complete Gate B and Gate C before considering model comparison.
- Decision evidence reference: ADP v2.3.1 entry-gate review and project-owner instruction to proceed, 2026-07-20.

## 31. Current Hold Point

This plan is approved with conditions outside the repository and is authorized for controlled promotion to the canonical repository path.

No runtime diagnostic work is authorized until the repository synchronization conditions are satisfied and Gate B passes.
