# ADP Open WebUI RAG Configuration Baseline

## 1. Status

- Baseline status: APPROVED
- Release applicability: ADP v2.3.1 and later until superseded
- Use case: Controlled local Knowledge retrieval with `llama3.2:3b`

## 2. Approved RAG Template

Replace the entire Open WebUI RAG template with:

```text
Use only the information inside the <context> block to answer the user's question.

Do not use outside knowledge.
Do not copy instructions or examples from this template.
If the requested information is not present in the context, respond exactly: NOT FOUND.
When the context includes a source id, cite the supporting source using [id].
Return a direct answer without commentary.

<context>
{{CONTEXT}}
</context>
```

## 3. Prohibited Template Content

Do not include:

- Concrete sample answers
- Fabricated percentages
- Sample studies or citations
- Example claims that a small model may copy
- Instructions unrelated to source-grounded answering

## 4. Approved Workspace Model

- Name: `Llama 3.2 3B RAG Deterministic Test`
- Base model: `llama3.2:3b`
- Visibility: Private
- Temperature: `0`
- Seed: `42`
- System prompt: none
- Knowledge attached at model level: none
- Tools: none
- Skills: none

## 5. Controlled Retrieval Procedure

1. Start a fresh chat.
2. Select the approved deterministic workspace model.
3. Attach the approved Knowledge collection.
4. Keep Web Search and optional tools disabled.
5. Submit the frozen prompt once.
6. Verify the source indicator.
7. Verify the exact answer against the source.
8. Stop for unsupported content, missing source, or `NOT FOUND` when the source contains the answer.

## 6. Change Control

Any change to the following requires a new validation block:

- RAG template
- Base model
- Model tag or digest
- Temperature
- Seed
- Collection contents
- Embedding model
- Chunking or retrieval settings
- Open WebUI version
- Ollama version
