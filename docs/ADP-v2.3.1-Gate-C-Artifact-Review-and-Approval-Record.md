# ADP v2.3.1 Gate C Artifact Review and Approval Record

## 1. Document Control

- Project: AI Development Platform
- Release: ADP v2.3.1
- Review type: Gate C candidate red-team review
- Repository baseline represented: `253e9dd`
- Review decision: APPROVE AS REVISED FOR CONTROLLED REPOSITORY PROMOTION ONLY
- Runtime authorization: CONDITIONAL HOLD - released only when `V231-C-PROMOTE-01` records all required PASS fields and no relevant state changed
- Knowledge creation: AUTHORIZED ONLY INSIDE `V231-C-RUNTIME-01` AFTER ITS ENTRY CONDITIONS PASS
- Prompt execution: AUTHORIZED ONLY INSIDE `V231-C-RUNTIME-01`
- Optional model comparison: NOT AUTHORIZED
- ADP v2.4: BLOCKED

## 2. Evidence Reviewed

The review used the supplied:

- ADP v2.3 to v2.3.1 project handoff
- ADP v2.3.1 approved diagnostic plan
- ADP v2.3.1 Gate B baseline record
- Gate C project handoff and startup instructions
- Gate C candidate review notes
- Candidate data design, source, prompt library, test template, attachment procedure, and manifest

Package integrity observations:

- Candidate artifact checksums matched the supplied candidate manifest.
- The approved plan checksum matched `130a79ba28ef428e033b7b913f9545395d20d72511a8fbe68e6edc3c370943f7`.
- The Gate B record checksum matched `35fd09281bca5bc0c6e803bd9beed56bce9d4eccecd15a7ef79fb92d9fbf8e59`.
- Two uploaded startup files were byte-identical and created no content conflict.
- Direct access to the operator's local repository was not available during this document-only review. Repository state must be revalidated by the operator before promotion.

## 3. Executive Finding

The candidate package was not approval-ready because `V231-R01-P1-v1` combined three diagnostic dimensions:

1. Direct retrieval
2. Model-generated source filename
3. Exact two-line formatting

That design could classify a formatting or filename-echo defect as retrieval failure and would conflict with the approved sequence that assigns exact structure to `V231-F01` after direct retrieval is demonstrated.

The revised package removes that confound while retaining every source element required by the approved plan.

## 4. Point, Counterpoint, and Disposition

| Issue | Point | Counterpoint | Disposition |
|---|---|---|---|
| Exact two-line format in `V231-R01` | Strict output simplifies scoring. | It makes formatting a Gate C pass condition and obscures whether retrieval worked. | Remove strict format from Gate C; record formatting as an observation; test it under `V231-F01`. |
| Model-generated source filename | Echoing the filename appears to prove source use. | The model may omit or invent metadata even when Open WebUI retrieved the correct passage. | Prove source file and passage through displayed-source evidence under `V231-S01`. |
| Separate R01 and S01 execution blocks | Separate blocks may appear cleaner. | A second prompt block adds unnecessary executions and risks another changed condition. | Score `V231-R01` and `V231-S01` separately from the same three fresh-chat runs. |
| Archive marker in the first source | Removing it would minimize context. | The approved plan requires one distinct non-target fact. | Retain it; do not query it during `V231-R01`. |
| Explicit prohibition in the first source | Deferring it would reduce priming. | The approved plan requires one explicit prohibition in the first file. | Retain it; do not make it a separate Gate C query. |
| Rolling 15-minute log count | It is simple to run. | It can include earlier warnings and cannot unambiguously bind evidence to one run. | Use exact `RUN_START` and `RUN_END`; retain complete matching lines and count. |
| Attachment screenshot alone | It may show the collection is attached. | It may not prove the collection contains exactly one approved file. | Require per-run collection-membership, fresh-chat, and attachment evidence. |
| Source-plus-prompt byte estimate | It indicates a much smaller input than v2.3. | Platform wrappers and tokenizer behavior remain unknown. | Treat counts as planning indicators only; bounded Ollama logs control the decision. |
| Preface or extra source-supported text | It indicates instruction-following weakness. | It does not negate exact fact retrieval and belongs to later format testing. | Record as a Gate C observation; do not fail `V231-R01` solely for formatting. |
| New truncation warning | It could be classified inconclusive because the model saw incomplete input. | Gate C explicitly requires a non-truncated diagnostic request. | Classify the run FAIL and stop the block; preserve evidence for remediation. |
| Micro-gating after each successful substep | Repeated confirmations can appear cautious. | They add no control value when the next step is already authorized and conditionally validated. | Adopt consolidated execution packets with automatic continuation and evidence-based stop conditions. |

## 5. Approved Corrections

The revised package:

1. Replaces unapproved prompt `V231-R01-P1-v1` with frozen prompt `V231-R01-P1-v2`.
2. Removes exact line count, labels, and model-generated filename from Gate C scoring.
3. Separates `V231-R01` retrieval scoring from `V231-S01` displayed-source scoring.
4. Uses the same three runs for both tests.
5. Retains the archive marker and prohibition because the approved plan requires them.
6. Makes formatting an observation for later `V231-F01` work.
7. Replaces rolling truncation counts with exact per-run timestamp windows and complete log-line retention.
8. Requires independent collection-membership, fresh-chat, attachment, response, source, and truncation evidence for every run.
9. Aligns failure and inconclusive codes with the corrected Gate C boundary.
10. Keeps runtime authorization withheld.
11. Adds the cross-release Controlled Execution Packet Standard and release-specific promotion and runtime packets.
12. Removes unsupported micro-approvals while retaining material hold points and stop conditions.

## 6. Approval Conditions Before Repository Promotion

Before copying these artifacts into the repository, the operator must confirm:

- Branch: `main`
- `HEAD`: `253e9dd`
- Local `main`: `253e9dd`
- `origin/main`: `253e9dd`
- Working tree: clean
- Approved plan checksum unchanged
- Gate B record checksum unchanged

If the repository has legitimately advanced, stop and reconcile the later commits before relying on this baseline.

## 7. Promotion Requirements

Promote only the approved, non-candidate files in this package to their planned canonical paths.

Before commitment:

1. Validate SHA-256 checksums against the approved manifest.
2. Validate ASCII-only content.
3. Validate headings.
4. Validate no tab characters.
5. Validate no trailing whitespace.
6. Validate names, collection identifier, source filename, model, prompt ID, and test IDs.
7. Review the Git diff.

After commitment:

1. Push `main`.
2. Confirm `HEAD`, `main`, and `origin/main` alignment.
3. Confirm a clean working tree.
4. Record the final pre-runtime gate.

Only after those steps may the collection be created and the approved source uploaded.

## 8. Decision

Decision:

- APPROVE AS REVISED FOR CONTROLLED REPOSITORY PROMOTION ONLY

Basis:

- The revised package aligns Gate C with the approved plan.
- Direct retrieval is no longer confounded by strict formatting or filename generation.
- Displayed-source evidence is independently scored.
- The plan-required source content is retained.
- Prompt-truncation evidence is bounded to each run.
- Internal names, identifiers, and result boundaries are consistent.

Residual risk:

- The final Open WebUI assembled token count remains unknown until runtime.
- Open WebUI's ability to visibly prove collection attachment and displayed-source evidence remains untested for this exact block.
- The operator's current repository state has not been independently observed in this document-only review.

These residual risks are controlled by the final pre-runtime gate and the approved stop conditions.

## 9. Continuing Hold Point

This approval does not authorize runtime work.

Do not create a Knowledge collection, upload the source, run the prompt, change the model or context, alter networking or firewall controls, authorize model comparison, or begin ADP v2.4 until repository promotion, synchronization, cleanliness validation, and the final pre-runtime gate are complete.


## 10. Process-Efficiency Control

The following documents are approved as controlling process artifacts for this release and later ADP work:

- `ADP-Controlled-Execution-Packet-Standard.md`
- `skills/adp-controlled-execution-packets/SKILL.md`
- `ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md`
- `ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md`
- `ADP-v2.3.1-Gate-C-Execution-Model-Addendum.md`

The promotion packet combines baseline validation, package verification, controlled copy, Git review, commit, push, synchronization, cleanliness, and read-only pre-runtime validation.

The runtime packet combines setup and all three counted runs. Successful runs continue automatically. Only a documented stop condition or material boundary change requires a transition.

This control is intended to prevent unnecessary, untested, or unsupported back-and-forth from being reintroduced in later releases or new chats.

## Final Delivery Control Amendment

The prior ZIP-plus-checksum-plus-launcher delivery transaction is superseded.

The approved operator delivery is one self-contained installer that embeds the validated Gate C package and verifies it before invoking the promotion packet. This amendment does not alter the approved Gate C diagnostic scope, repository baseline, runtime controls, test identifiers, or authorization boundary.

The installer must pass the ADP Final Delivery Validation Standard before delivery. Target-host repository and runtime execution remain operator-dependent and may still stop on a genuine baseline, authorization, service, security, or Git condition.
