# ADP Model Selection Standard

## Version

ADP v1.2

## Purpose

Define the controlled process for selecting, pulling, testing, documenting, and retaining local AI models in the AI Development Platform.

## Current Host Baseline

Host: smt-ai    
OS: Linux Mint 22.3    
CPU: AMD Ryzen 3 4300U with Radeon Graphics    
CPU capacity: 4 cores / 4 threads    
RAM: 14 GiB total    
Disk: approximately 391 GB available at inventory capture    
GPU: No NVIDIA GPU detected; AMD Radeon RX Vega 6 integrated graphics observed    
Runtime: Ollama 0.30.11 active    
Current baseline model: llama3.2:1b    
Open WebUI image: ghcr.io/open-webui/open-webui:v0.10.2    
Open WebUI binding: 127.0.0.1:3000->8080/tcp    

## Operating Principle

Model expansion must be controlled, evidence-based, and reversible.

Do not pull multiple models at once.    
Do not pull large models before validating smaller models.    
Do not assume GPU acceleration unless validated.    
Do not weaken UFW or expose Open WebUI to LAN or Internet for model testing.    

## Preferred Model Classes

Default class: 1B to 3B parameter models.    
Stretch class: 4B parameter models only after successful 1B to 3B validation.    
Deferred class: 7B or 8B quantized models only after performance, memory, and recovery criteria are proven.    
Avoid class: 12B and larger models on this host unless hardware changes materially.    

## Required Selection Gates

A candidate model must pass these gates before pull:

1. Hardware fit
      - Must be appropriate for a 4-core CPU-first host with 14 GiB RAM.
      - Must not be expected to cause sustained swap pressure.

2. Disk impact
      - Expected local model size must be reviewed before pull.
      - Disk headroom must remain acceptable after pull.

3. Source trust
      - Prefer official Ollama library entries.
      - Trusted upstream information must be reviewed where relevant.

4. License review
      - License or usage terms must be reviewed before adoption.
      - Any restriction or uncertainty must be documented.

5. Use-case fit
      - Candidate must support a defined ADP purpose, such as:
          - local baseline comparison
          - summarization
          - prompt rewriting
          - structured output
          - coding support
          - retrieval or agentic workflow testing

6. Validation
      - Must validate in Ollama CLI.
      - Must validate in Open WebUI.
      - Must complete at least one standard prompt-response test.

7. Rollback
      - Removal command must be documented.
      - Existing baseline model must remain available unless intentionally retired.

8. Documentation
      - Engineering log must record candidate, rationale, validation result, and retain/remove decision.

## Scoring Rubric

Score each candidate from 1 to 5.

| Category | Weight | Description |
|---|---:|---|
| Hardware fit | 25% | Fit for CPU-first 14 GiB RAM host |
| ADP usefulness | 20% | Practical value for ADP tasks |
| Operational risk | 20% | Low instability, memory, or usability risk |
| Source trust | 15% | Official Ollama or trusted upstream |
| License clarity | 10% | License reviewed and acceptable for evaluation |
| Differentiation | 10% | Adds useful capability beyond existing model |

## Initial Candidate Assessment

Recommended first model expansion:

llama3.2:3b

Rationale:
- Same model family as the current llama3.2:1b baseline.
- Low-risk controlled expansion from 1B to 3B.
- Appropriate for general local assistant tasks.
- Useful for instruction following, summarization, prompt rewriting, and tool-use comparison.
- Better controlled first step than introducing a different family or pulling a 7B-class model.

Deferred candidates:
- qwen2.5-coder:1.5b for coding-focused testing.
- gemma3:1b for lightweight cross-family comparison.
- qwen2.5:1.5b for multilingual and structured-output comparison.

Do not pull deferred candidates until llama3.2:3b is validated and documented.

## Standard Validation Prompt Set

Each model must be tested with:

1. Basic responsiveness
      Prompt:
      Explain in one paragraph what this local model is useful for.

2. Summarization
      Prompt:
      Summarize the ADP workflow: Plan, Implement, Validate, Document, Snapshot, Release.

3. Structured output
      Prompt:
      Return a JSON object with keys: model_name, use_case, risks, and recommendation.

4. Reasoning / instruction following
      Prompt:
      Give three risks of pulling too many local models at once and one mitigation for each.

5. ADP-specific usefulness
      Prompt:
      Draft a short engineering-log entry for validating a local model in Ollama and Open WebUI.

## Retain / Remove Decision

After validation, record one of:

- Retain as approved ADP model
- Retain as experimental model
- Remove due to poor fit
- Defer further testing

## Rollback / Removal Pattern

To remove a model:

ollama rm MODEL_NAME

After removal, validate:

ollama list

Confirm the baseline model remains available:

llama3.2:1b

## Current Approved Baseline

Approved baseline model:

llama3.2:1b

Next controlled candidate:

llama3.2:3b
