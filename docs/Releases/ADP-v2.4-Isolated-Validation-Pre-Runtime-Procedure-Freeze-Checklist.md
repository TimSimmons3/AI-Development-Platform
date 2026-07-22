# ADP v2.4 Isolated Validation Pre-Runtime Procedure Freeze Checklist

## Status

```text
CHECKLIST_STATUS=CANDIDATE
RUNTIME_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```

## Required Before Runtime Authorization

- [ ] Git baseline, branch, remote, and clean worktree confirmed.
- [ ] Primary Compose checksum confirmed.
- [ ] Validation Compose checksum and semantic validation confirmed.
- [ ] Approved RAG template checksum confirmed.
- [ ] Pinned Open WebUI image present and digest confirmed.
- [ ] Validation container, volume, and port state confirmed.
- [ ] Primary Open WebUI health confirmed.
- [ ] Native single-model export captured from the selected primary model.
- [ ] Raw export retained outside Git as restricted evidence.
- [ ] Sanitized import payload passes `adp24_validate_model_export.py`.
- [ ] Sanitized import payload checksum frozen.
- [ ] Model sync prohibition appears in every current guide and script.
- [ ] Runtime evidence workspace is empty and uniquely named.
- [ ] Evidence filename map passes validation.
- [ ] Volume backup and restore scripts pass static and negative tests.
- [ ] Runtime apply and verify scripts pass shell syntax and semantic review.
- [ ] Primary container, volume, port, and Compose file are outside the write set.
- [ ] Rollback boundary and stop conditions are frozen.
- [ ] Operator usability review passes.

## Required Before Counted Execution

- [ ] Isolated instance created and healthy.
- [ ] Imported model id, base model, temperature, and seed verified.
- [ ] No model-level Knowledge, tools, skills, functions, or filters verified.
- [ ] Validation-volume backup created and checksum verified.
- [ ] Restart-persistence validation passes.
- [ ] Synthetic Knowledge source checksum frozen.
- [ ] Collection identifier frozen.
- [ ] Prompt and expected-answer set frozen.
- [ ] Non-counted dry run passes.
- [ ] Raw response capture path passes positive and negative tests.
- [ ] One current guide, script set, evidence schema, and filename map identified.
- [ ] All checksums and semantic traceability results retained.

No unchecked item may be interpreted as passed.
