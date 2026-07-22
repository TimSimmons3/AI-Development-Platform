# ADP v2.3.1 Gate C Diagnostic Closeout

## 1. Closeout Decision

ADP v2.3.1 Gate C is closed as:

```text
PASS_WITH_REQUIRED_CONFIGURATION
```

The original execution path is not counted because procedure and evidence-capture defects caused the affected runs to be classified as `VOIDED_NOT_COUNTED`.

The replacement bounded diagnostic isolated the working configuration and produced three independent successful retrieval responses.

## 2. Confirmed Root Cause

Primary root cause:

```text
RAG_TEMPLATE_EXAMPLE_CONTAMINATION
```

The original RAG template contained a concrete answer example that the 3b model reproduced instead of using the correct retrieved passage.

Contributing weakness:

```text
DEFAULT_GENERATION_VARIABILITY
```

Even after the template correction, default 3b generation was not repeatable.

## 3. Required Corrective Configuration

The approved operating configuration is:

- Example-free RAG template
- `llama3.2:3b` base model
- Private deterministic workspace model
- Temperature `0`
- Seed `42`
- Fresh chat for each controlled test
- Exact Knowledge collection attachment
- Web search and optional tools disabled during controlled retrieval validation

## 4. Control Disposition

| Item | Disposition |
|---|---|
| Original RAG template | Superseded |
| Default 3b controlled RAG use | Not approved |
| Deterministic workspace preset | Approved for controlled RAG use |
| Original Gate C counted evidence | Voided and retained as historical |
| Deterministic evidence package | Approved closeout evidence |
| Further repeated minimal-fact testing | Not required for v2.3.1 |

## 5. Lessons Incorporated

- Test the model and transport path before building extensive evidence automation.
- Use qualification testing only after the pipeline is proven.
- Concrete examples in system or RAG templates are prohibited unless independently shown not to contaminate output.
- Small local models require explicit generation controls for repeatability.
- Validators must normalize line wrapping before exact-sentence comparison.
- A tooling failure must not be conflated with a model failure.
- Stop-on-first-failure remains appropriate only after the test harness itself is proven.

## 6. Exit Criteria

The phase may close when:

- This record and the validation record are committed.
- The evidence archive is preserved in the repository.
- The engineering log and release records are updated.
- Git is synchronized and clean.
- A final Timeshift snapshot is verified.
- A recoverability bundle and source archive are created and checksummed.

## 7. Next Release Boundary

ADP v2.4 may begin only after the post-closeout recovery script reports full PASS.

The next release should not expand the RAG corpus until the deterministic operating baseline and template controls are treated as mandatory.
