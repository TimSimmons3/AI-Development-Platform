# ADP v2.3.1 Deterministic RAG Validation Record

## 1. Record Status

- Release: ADP v2.3.1
- Validation block: Deterministic minimal direct retrieval
- Final result: `PASS_WITH_REQUIRED_CONFIGURATION`
- Repeatability result: `3_OF_3_PASS`
- Evidence archive SHA-256: `7648d869b7bb80696f74e45546b6a43f84a5a7d7f62e30d580a7f57459170ebf`
- Evidence package integrity: PASS
- Original counted Gate C attempts: `VOIDED_NOT_COUNTED`

## 2. Objective

Verify that Open WebUI can retrieve one exact synthetic fact from one approved Knowledge source and produce a grounded response without unsupported factual additions.

## 3. Approved Source

- File: `adp231_minimal_direct_retrieval.md`
- Source SHA-256: `ea0288d0d8666438e8cf9ae7dd54e6da8aaa0818f42d15f29bdf7467acf77afc`
- Platform identifier: `NOVA-231-DELTA`
- Required sentence:

```text
The release objective for NOVA-231-DELTA is to verify that one exact synthetic fact can be retrieved from one attached source without adding outside information.
```

## 4. Diagnostic Findings

### 4.1 Source and retrieval path

The following controls passed:

- Approved source checksum
- Open WebUI collection attachment
- Knowledge indexing
- Retrieval of the correct source passage
- Display of one retrieved source
- Correct source filename during live review

### 4.2 Original RAG template contamination

The original Open WebUI RAG template contained this concrete answer example:

```text
According to the study, the proposed method increases efficiency by 20% [1].
```

During a failed 3b Knowledge test, the model returned materially the same example instead of answering from the retrieved source. The displayed source passage was correct.

This establishes template-example contamination as a confirmed root cause.

### 4.3 Default generation inconsistency

After removal of the concrete example, default `llama3.2:3b` behavior remained inconsistent:

- One fresh Knowledge test passed.
- One fresh Knowledge test returned `NOT FOUND`.
- The failed test still displayed the correct source passage containing the requested sentence.

This establishes generation variability as a contributing control weakness.

### 4.4 Deterministic configuration

A private Open WebUI workspace model preset was created with:

- Name: `Llama 3.2 3B RAG Deterministic Test`
- Base model: `llama3.2:3b`
- Temperature: `0`
- Seed: `42`
- System prompt: none
- Attached Knowledge in preset: none
- Tools and skills in preset: none

Using the corrected RAG template and this preset, three independent fresh chats each produced:

- The exact required sentence
- One retrieved source indicator
- No unsupported factual additions

Final deterministic result: `3_OF_3_PASS`.

## 5. Evidence Inventory

- `ADP Deterministic Test 1.png`
  - SHA-256: `d0ff1a0566c0555960c2249b64da033ca041935984ab0292065f08960fa52f1e`
- `ADP Deterministic Test 2.png`
  - SHA-256: `49efc8ad6cbac8dd571efb2a5deff14daa2f36e2e5ded5340ecbc7d613cb2c45`
- `ADP Deterministic Test 3.png`
  - SHA-256: `92a61002cd1dfcdab37991ac25a3ab3fe2a14a019530dd4d4eb888e0d970e27e`
- Internal `SHA256SUMS.txt`: PASS
- External archive checksum: PASS

Each screenshot is a valid `935 x 685` PNG and visibly shows:

- The deterministic workspace model
- A separately named test chat
- `Retrieved 1 source`
- The exact required response

## 6. Classification

| Control | Result |
|---|---|
| Source integrity | PASS |
| Collection attachment | PASS |
| Indexing and retrieval | PASS |
| Correct passage retrieval | PASS |
| Original template safety | FAIL |
| Corrected template safety | PASS |
| Default 3b repeatability | FAIL |
| Deterministic 3b repeatability | PASS, 3 of 3 |
| Unsupported factual additions under approved configuration | None observed |

## 7. Final Decision

The Gate C technical objective is achieved only under the frozen configuration documented in the configuration baseline.

Final status:

```text
GATE_C_TECHNICAL_OBJECTIVE=PASS
GATE_C_CLOSEOUT_STATUS=PASS_WITH_REQUIRED_CONFIGURATION
DETERMINISTIC_REPEATABILITY=3_OF_3_PASS
```

## 8. Residual Risks

- The screenshots display `Retrieved 1 source`, but do not show the expanded source filename.
- The filename was confirmed during each live test but is not self-contained in the screenshot package.
- Open WebUI configuration was manually established; a native configuration export was not available in this evidence block.
- Default `llama3.2:3b` behavior remains outside the approved operating baseline.

These limitations do not invalidate the deterministic result, but they must remain documented.
