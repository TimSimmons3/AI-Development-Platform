# ADP RAG Template and Deterministic Generation Standard

## 1. Purpose

Prevent prompt-template contamination and uncontrolled output variability in local Retrieval-Augmented Generation workflows.

## 2. Template Requirements

RAG templates shall:

- Contain instructions, placeholders, and control language only.
- Avoid concrete factual examples that could be emitted as answers.
- Delimit retrieved context clearly.
- Define exact behavior when context does not contain the answer.
- Prohibit unsupported factual additions.
- Use citation instructions only when a source identifier exists.

## 3. Small-Model Determinism

For controlled qualification of small local models:

- Temperature shall be `0`.
- A fixed seed shall be used when supported.
- The parameters shall be stored in a persistent model preset.
- Each repeatability run shall use a fresh chat.
- The same source, prompt, and model preset shall be used.

## 4. Validation Order

Testing shall proceed in this order:

1. Model literal-copy control
2. Model inline-context control
3. Open WebUI inline-context control
4. Knowledge retrieval verification
5. Prompt and answer grounding verification
6. Deterministic repeatability qualification
7. Evidence packaging and closeout

Qualification evidence shall not be expanded until the preceding pipeline stage passes.

## 5. Validator Requirements

Exact-answer validators shall:

- Normalize line wrapping and repeated whitespace.
- Distinguish content failure from formatting differences.
- Preserve the raw response.
- Report the failed control explicitly.
- Avoid silently exiting before final status output.

## 6. Stop Conditions

Stop and classify the test when:

- A concrete template example appears in the answer.
- The displayed source does not support the answer.
- The correct passage is retrieved but the answer is unsupported.
- A required deterministic parameter does not persist.
- The test harness or evidence method fails.

Do not patch an active counted test.
