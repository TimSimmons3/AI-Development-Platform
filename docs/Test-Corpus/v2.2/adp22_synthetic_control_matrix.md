# ADP v2.2 Synthetic Control Matrix

## Purpose

This synthetic control matrix supports ADP v2.2 retrieval and comparison testing.

## Controls

| Control ID | Control Name | Requirement | Validation Expectation |
|---|---|---|---|
| ADP22-CTRL-001 | Localhost-only access | Open WebUI remains bound to 127.0.0.1:3000->8080/tcp | docker ps output confirms localhost binding |
| ADP22-CTRL-002 | Approved model control | Only llama3.2:1b and llama3.2:3b are approved | ollama list shows only approved models |
| ADP22-CTRL-003 | Synthetic corpus only | Test documents contain no sensitive or production data | Manual review and keyword screening pass |
| ADP22-CTRL-004 | No external vector database | No Qdrant, Milvus, pgvector, or other vector database is installed | No new vector database service is present |
| ADP22-CTRL-005 | Manual loading only | Test documents are loaded manually through Open WebUI | Validation report records the manual loading path |
| ADP22-CTRL-006 | Removal validation | Loaded test documents are removed after testing | Post-removal prompts no longer retrieve removed content |
| ADP22-CTRL-007 | No firewall weakening | UFW posture is not weakened | No firewall change is performed |
| ADP22-CTRL-008 | No Docker network expansion | Docker host networking is not used | No host networking change is performed |

## Control Owner

The synthetic control owner for all controls is ADP Local Lab Owner.

## Validation Rule

A control passes only when the validation evidence supports the stated requirement.
