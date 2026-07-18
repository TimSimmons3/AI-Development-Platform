# ADP v2.2 Synthetic Policy Excerpt

## Purpose

This synthetic policy excerpt supports document QA, summary, and absent-answer testing.

## Data Classification Rule

ADP v2.2 test data must be synthetic and non-sensitive.

Approved test data may include:

- Synthetic platform notes.
- Synthetic control examples.
- Synthetic policy excerpts.
- Synthetic change logs.
- Synthetic conflict examples.

Prohibited test data includes:

- Production data.
- Sensitive data.
- Personal data.
- Medical data.
- Payment data.
- Credentials.
- Secrets.
- Tokens.
- API keys.
- Passwords.
- Contracts.
- Client records.
- Customer records.
- Employee records.
- Legal records.
- Financial records.
- Private business records.

## Loading Rule

Synthetic files may be loaded only after the plan and corpus gates pass.

Loading must be manual.

Automated ingestion is prohibited in ADP v2.2.

## Answer Rule

When asked to answer using only loaded test documents, the model should not use unsupported outside information.

If the loaded document does not contain the answer, the model should say the answer is not found in the loaded document.

## Removal Rule

Loaded synthetic documents must be removed after testing.

After removal, the same direct retrieval prompts must be repeated to check whether removed content is still retrievable.
