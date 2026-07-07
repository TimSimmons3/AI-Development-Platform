# ADP Model Promotion and Evaluation Policy

## Status
Draft for ADP v1.7

## Date
2026-07-07

## Purpose
This policy defines how ADP local models are evaluated, approved, promoted, demoted, retained, or retired.

## Scope
- Local Ollama models used by ADP.
- Model validation through CLI, Open WebUI, scripts, and documented review.
- Model approval decisions for controlled ADP use.
- Promotion, demotion, retention, and retirement decisions.

## Current Approved Models
- llama3.2:1b
- llama3.2:3b

## Model States
- Candidate: identified for possible evaluation but not yet approved.
- Experimental: pulled or tested only under controlled evaluation.
- Approved: validated and accepted for controlled ADP use.
- Deferred: not approved because evidence is incomplete or risks remain.
- Demoted: previously approved but restricted due to quality, safety, performance, or operational concerns.
- Retired: removed from active use or removed from the host.

## Promotion Criteria
- Model purpose is documented.
- Model size and host resource impact are reviewed.
- License and usage constraints are reviewed.
- Standard validation prompts are completed.
- Output quality is reviewed by a human.
- Runtime behavior is acceptable for the host.
- Security posture remains unchanged.
- Evidence supports approval for a defined use case.

## Demotion Criteria
- Repeated format failures.
- Unacceptable hallucination or reasoning quality for intended use.
- Unsafe or noncompliant behavior.
- Excessive CPU, memory, disk, or responsiveness impact.
- Evidence gaps that prevent audit-ready use.
- Better approved model available for the same use case.

## Required Evaluation Evidence
- Model name and version or tag.
- Evaluation date.
- Host baseline.
- Prompt set used.
- Runtime result summary.
- Quality review findings.
- Format compliance findings where applicable.
- Security and operational observations.
- Approval, defer, demote, retain, or retire decision.

## Evidence Handling
- Raw runtime output remains local evidence unless sanitized and approved.
- Formal summaries, rubrics, standards, and findings may be committed after review.
- Evidence must be reproducible enough to support audit review.
- Runner success alone is not sufficient for model approval.

## Security Requirements
- Do not expose Open WebUI to LAN or Internet.
- Do not use Docker host networking for Open WebUI.
- Do not delete the Open WebUI Docker volume.
- Do not weaken UFW.
- Do not pull uncontrolled models.
- Treat Ollama port 11434 listening behavior as a residual risk controlled by firewall posture.

## Approval Rule
A model is approved only when documented evidence supports a defined ADP use case and the current security posture remains unchanged.

## ADP v1.7 Decision
ADP model promotion must remain controlled, evidence-based, reversible, and aligned to the approved localhost-only operating baseline.
