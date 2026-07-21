# ADP Process Quality Gate Checklist

## Document Control

- Project: AI Development Platform
- Status: Approved for controlled repository promotion
- Canonical path:
  - `docs/ADP-Process-Quality-Gate-Checklist.md`

## Gate A - Authorization and Traceability

- [ ] Approved plan identified
- [ ] Current gate record identified
- [ ] Authorization boundary identified
- [ ] Every prerequisite mapped to a step or hold point
- [ ] Current and superseded artifacts listed

## Gate B - Procedure Freeze

- [ ] One current script
- [ ] One current guide
- [ ] One evidence schema
- [ ] One filename map
- [ ] Prompt and source checksums fixed
- [ ] Pass, fail, inconclusive, and void rules fixed
- [ ] Reset and cleanup procedure fixed
- [ ] Procedure version recorded

## Gate C - Operator Clarity

- [ ] Every step states terminal or application
- [ ] Every screenshot purpose is explicit
- [ ] Every filename is unique
- [ ] Every destination is explicit
- [ ] No expected result is recorded before observation
- [ ] No duplicate or contradictory instruction remains
- [ ] One next command is identified
- [ ] Expected PASS fields are listed

## Gate D - Technical Validation

- [ ] ASCII scan
- [ ] `bash -n`
- [ ] Checksums
- [ ] Clean-room execution
- [ ] Positive workflow test
- [ ] Negative missing-file test
- [ ] Negative stop-condition test
- [ ] Reset and cleanup test
- [ ] Evidence-collision test
- [ ] No unintended mutation

## Gate E - Semantic Validation

- [ ] Script and guide agree
- [ ] Script and packet agree
- [ ] Filename map agrees everywhere
- [ ] Superseded names absent from current instructions
- [ ] Success fields correspond to collected evidence
- [ ] Historical records are labeled
- [ ] No invalid evidence reuse is allowed

## Gate F - Counted-Run Entry

- [ ] Procedure freeze PASS
- [ ] Active workspace clean
- [ ] External-system reset complete
- [ ] Fresh evidence workspace exists
- [ ] Runtime baseline locked
- [ ] No material change after freeze

## Defect Rule

Any material defect found after a run starts voids the run.

Do not patch and continue.
