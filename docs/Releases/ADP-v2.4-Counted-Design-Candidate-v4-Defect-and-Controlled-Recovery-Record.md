# ADP v2.4 Counted-Design Candidate v4 Defect and Controlled Recovery Record

## Classification

```text
CANDIDATE_V4_STATUS=SUPERSEDED_DO_NOT_COMMIT_DO_NOT_REAPPLY
BASELINE_COMMIT=b934c7bd84bfbc35563f3681712c4d5bd8478196
APPLIED_STATE_SHA256=802660e7faf8647c00f906cecb6d754e169433eb717befd6262fa0bd8c803719
APPLICATION_RECORD_SHA256=cafff722054cec641180778692d25720b9cc9f740238a287ed7169e6e89c74a1
FAILURE_DIAGNOSIS_SHA256=4f169ae41ec7284c8ca4a8dde9fd53e82367822d7fd98e9a43315cd8a3a45336
SUPERSESSION_RECORD_SHA256=4623b43ec97a2e19a3fa5e1fd6fcdca86e400a94b253037a4b7f8fdfe11b02f9
```

Candidate v4 applied the intended 57-path semantic payload, but its quality gate rejected the valid linked Git worktree because it required `.git` to be a directory. In a linked worktree `.git` is correctly a file. The gate body, binding validator, fixture suite, and semantic self-tests did not run.

```text
ROOT_CAUSE=QUALITY_GATE_INVALID_GIT_WORKTREE_DIRECTORY_ASSUMPTION
QUALITY_GATE_BODY_EXECUTED=NO
CANDIDATE_V4_RERUN_AUTHORIZATION=PROHIBITED
COUNTED_EXECUTION_AUTHORIZATION=HOLD
```
