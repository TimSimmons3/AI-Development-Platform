# ADP v2.4 Non-Counted RAG Dry-Run Result and Defect Record

```text
NON_COUNTED_CASE=C
NON_COUNTED_CHAT_COUNT=1
NON_COUNTED_PROMPT_SUBMISSION_COUNT=1
FACTUAL_RETRIEVAL_RESULT=PASS
ANSWER_FORMAT_ADHERENCE=FAIL
FROZEN_CLASSIFIER_RESULT=FAIL_PRESERVED
NON_COUNTED_RAG_DRY_RUN_RESULT=FAIL_PRESERVED_NO_RETRY
NON_COUNTED_RAG_RERUN_AUTHORIZATION=PROHIBITED
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

The exact response was:

```text
Verification color: amber
Review window: thirty-six hours
```

The response contained both requested facts, but it did not match the frozen expected sentence. Evidence files 12 through 17 are immutable. The failed classifier result is preserved and may not be replaced by a retry.
