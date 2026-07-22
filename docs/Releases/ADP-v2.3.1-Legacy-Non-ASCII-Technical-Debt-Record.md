# ADP v2.3.1 Legacy Non-ASCII Technical Debt Record

## Status

- Classification: `PRE_EXISTING_BASELINE_DEBT`
- Baseline: `cf25056`
- File: `docs/ADP-Model-Selection-Standard.md`
- Closeout impact: none
- Remediation in this closeout: deferred

## Finding

The existing model-selection standard contains Unicode spacing characters in multiple lines.

The defect existed in the synchronized Git baseline before the deterministic RAG closeout began. It was not introduced or modified by the closeout package.

## Decision

This legacy formatting debt shall not block an unrelated closeout when:

- The affected file is unchanged by the current work.
- The defect does not alter executable behavior.
- The current package is independently ASCII-clean.
- The debt is recorded and assigned to a future controlled remediation.

## Future Action

Remediate the file in a dedicated normalization change with:

- Before-and-after checksum evidence
- Content-equivalence review
- Markdown rendering review
- Git diff validation
- No substantive policy change
