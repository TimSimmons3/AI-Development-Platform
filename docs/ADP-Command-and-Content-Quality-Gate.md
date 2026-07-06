# ADP Command and Content Quality Gate

## Status

Draft for ADP v1.6

## Date

2026-07-06

## Purpose

This gate prevents recurring paste, indentation, hidden-character, and command-corruption failures during ADP work.

This gate applies before creating, modifying, validating, executing, committing, or promoting ADP files.

## Mandatory Rules

- Rule: Use short command blocks by default.
- Rule: Avoid long heredocs for generated documents.
- Rule: Avoid nested Markdown bullets in generated documents.
- Rule: Avoid manual leading spaces in generated content.
- Rule: Avoid sed replacements that depend on leading spaces.
- Rule: Write generated content to a temporary file first.
- Rule: Promote temporary files into the repo only after validation passes.
- Rule: Treat any non-ASCII finding as a hard stop.

## Required Candidate Validation

- Check: Candidate file exists.
- Check: Candidate file is ASCII-clean unless a documented exception is approved.
- Check: Required headings are present.
- Check: Required control statements are present.
- Check: Repo status remains unchanged before promotion.

## Required Promotion Validation

- Check: Promoted file exists in the intended repo path.
- Check: Promoted file is ASCII-clean unless a documented exception is approved.
- Check: Required headings are present after promotion.
- Check: git diff --check passes.
- Check: git status shows only expected files.

## Script and Code Gate

- Check: Shell scripts pass bash -n before execution.
- Check: Embedded Python is extracted and checked with python3 -m py_compile where applicable.
- Check: New scripts include fail-fast behavior where appropriate.
- Check: Validation wrappers include content-completeness checks, not syntax checks only.

## Stop Conditions

- Stop: Non-ASCII characters are detected.
- Stop: Command text appears wrapped, duplicated, fragmented, or corrupted.
- Stop: A filename or path appears altered by paste behavior.
- Stop: git diff --check reports whitespace or formatting issues.
- Stop: Git status shows unexpected files.
- Stop: Any validation command fails.


## Security Control Reminders

- Control: Do not expose Open WebUI to LAN or Internet.
- Control: Do not use --network=host.
- Control: Do not delete the open-webui Docker volume.
- Control: Do not disable UFW.
- Control: Do not add models during v1.6.

## ADP v1.6 Decision

This quality gate is the first ADP v1.6 control artifact and must be followed before additional v1.6 documents are created.
