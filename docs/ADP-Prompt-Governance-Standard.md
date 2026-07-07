# ADP Prompt Governance Standard

## Status
Draft for ADP v1.7

## Date
2026-07-07

## Purpose
This standard defines how ADP prompts are created, reviewed, changed, tested, approved, and retired.

## Scope
- System prompts used for ADP workflows.
- Validation prompts used for local model evaluation.
- Prompt templates used in repeatable scripts or guides.
- Prompt changes that affect model behavior, evidence quality, safety, security, or audit readiness.

## Prompt Classes
- Baseline prompts: stable prompts used for repeatable model validation.
- Candidate prompts: proposed prompts under review.
- Experimental prompts: temporary prompts used for exploration only.
- Retired prompts: prompts removed from active use because they are obsolete, unsafe, misleading, or no longer useful.

## Required Prompt Metadata
- Prompt name.
- Prompt purpose.
- Intended model or model class.
- Expected output format.
- Review status.
- Known risks or limitations.
- Evidence location when tested.

## Prompt Creation Rules
- Prompts must be clear, bounded, and testable.
- Prompts must state required output format when format matters.
- Prompts must avoid hidden assumptions when the intended use is evaluative.
- Prompts must avoid requesting unsafe, illegal, private, or uncontrolled behavior.
- Prompts must avoid claims that a model is approved before evaluation evidence supports approval.

## Prompt Change Review
- Material prompt changes require review before promotion.
- A material change is any change that affects task scope, expected output, safety behavior, security posture, scoring, evidence, or reproducibility.
- Cosmetic changes may be promoted after ASCII, whitespace, and content validation.
- Prompt changes must preserve auditability and repeatability.

## Required Validation
- Candidate prompt files must be created outside docs before promotion.
- Candidate prompt files must pass ASCII checks.
- Candidate prompt files must pass trailing whitespace checks.
- Promoted prompt files must be validated again after copy into docs or tests.
- Git diff checks must pass before staging or committing.

## Evidence Rules
- Raw runtime output is local evidence unless intentionally sanitized and approved.
- Formal findings, scoring rubrics, prompt templates, and standards may be committed after review.
- Evidence must identify the prompt, model, date, result, and reviewer decision when practical.
- A successful model response is not by itself sufficient evidence of prompt quality.

## Approval States
- Draft: created but not reviewed.
- Candidate: ready for validation.
- Approved: validated and accepted for controlled ADP use.
- Deferred: not approved yet because evidence is incomplete or risks remain.
- Retired: removed from active use.

## Stop Conditions
- Stop if a prompt weakens the localhost-only security posture.
- Stop if a prompt encourages uncontrolled model downloads.
- Stop if output format requirements cannot be tested.
- Stop if evidence cannot be tied back to the prompt and model tested.
- Stop if hidden characters, non-ASCII content, or trailing whitespace are detected.

## ADP v1.7 Decision
ADP prompts may be promoted only when they are clear, bounded, testable, evidence-backed, and aligned with the current ADP security posture.
