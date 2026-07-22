# ADP v2.4 Isolated Validation Configuration Manifest

## 1. Status

```text
MANIFEST_STATUS=REPOSITORY_CANDIDATE_V2
PRIMARY_INSTANCE_CHANGE=NONE
RUNTIME_AUTHORIZATION=HOLD
MODEL_SYNC_OPERATION=PROHIBITED
```

## 2. Validated Runtime References

- Open WebUI version: `0.10.2`
- Open WebUI image digest: `sha256:9fcea9c6e32ab60b0498f3986c6cdf651ddbe61db48d2213a3d28048ddd673d4`
- Ollama version: `0.30.11`
- `llama3.2:3b` source blob: `sha256-dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff`
- Embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- Primary Open WebUI binding: `127.0.0.1:3000`
- Validation binding: `127.0.0.1:3001`

## 3. Qualification-Critical Validation Settings

The isolated instance explicitly controls:

- Example-free RAG template
- `sentence-transformers/all-MiniLM-L6-v2`
- Character text splitter
- Markdown-header preprocessing enabled
- Chunk size `1000`
- Chunk overlap `100`
- Top K `3`
- Relevance threshold `0`
- Hybrid search disabled
- Bypass embedding and retrieval disabled
- Full context disabled
- Web Search disabled
- Retrieval query generation enabled

## 4. Observed but Not Forced Settings

The following starting values are recorded for drift review but are not forced through the repository Compose candidate because they are inactive, defaulted, or outside the bounded path:

- Embedding engine: local default
- Content extraction engine: local default
- Minimum chunk merge target: `0`
- Top K reranker: `3`
- Reranking engine: empty
- Reranking model: empty
- Hybrid BM25 weight: `0.5`

They require separate approval before activation or qualification use.

## 5. Template Integrity

Canonical approved template:

`artifacts/Configuration/ADP-v2.4/approved-rag-template.txt`

SHA-256:

```text
def3db3e05b1651aa33b921a03573074d8033ca5d2ce691446638e362ef92d96
```

## 6. Model Portability Boundary

The repository contains a sanitized discovery record only. It is not an import artifact.

Before runtime procedure freeze:

1. Export only `Llama 3.2 3B RAG Deterministic Test` through Open WebUI's native single-model export function.
2. Validate that the export contains the expected model ID, base model, temperature, and seed.
3. Review it for credentials, user identifiers, unintended tools, skills, or Knowledge bindings.
4. Import it into the validation instance through the model import operation.
5. Never use the model synchronization operation with a one-model file.

## 7. Security Boundary

- Primary container and volume remain unchanged.
- Validation port is loopback-only.
- Docker host networking is prohibited.
- Existing Ollama and UFW settings remain unchanged.
- The validation instance shall use Docker bridge networking and the existing host-gateway path.
- Failure to reach Ollama is a stop condition, not authorization to weaken the firewall.
