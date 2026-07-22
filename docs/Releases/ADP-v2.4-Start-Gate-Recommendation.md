# ADP v2.4 Start-Gate Recommendation

## Decision

ADP v2.4 is recommended to proceed after post-closeout recovery completes.

## Mandatory Entry Conditions

- Git closeout commit synchronized
- Working tree clean
- Final Timeshift snapshot verified
- Git bundle verified
- Source archive checksummed
- Example-free RAG template retained
- Deterministic workspace model retained
- Temperature `0`
- Seed `42`

## Recommended v2.4 Scope

- Formalize configuration export or reproducible configuration-as-code
- Add an automated RAG-template lint check
- Add whitespace-normalized answer validation
- Test one bounded multi-fact source before corpus expansion
- Record model, Open WebUI, Ollama, embedding, and retrieval configuration together

## Exclusions

- No uncontrolled corpus expansion
- No default-temperature qualification
- No concrete examples in RAG templates
- No evidence-framework redesign unless a verified defect requires it
- No real or sensitive data


## Legacy Formatting Debt

Schedule a bounded normalization of `docs/ADP-Model-Selection-Standard.md` to remove pre-existing Unicode spacing without changing substantive content.
