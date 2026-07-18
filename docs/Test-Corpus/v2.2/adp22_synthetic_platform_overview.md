# ADP v2.2 Synthetic Platform Overview

## Purpose

This synthetic document supports ADP v2.2 local RAG pilot testing.

It contains no real personal information, no real business records, no customer data, no employee data, no legal records, no financial records, no medical records, no credentials, no secrets, and no production data.

## Release Objective

ADP v2.2 validates synthetic local RAG document loading, retrieval, answer quality, hallucination resistance, and removal behavior while preserving the localhost-only ADP security boundary.

## Runtime Boundary

Open WebUI must remain localhost-only.

The approved Open WebUI binding is 127.0.0.1:3000->8080/tcp.

The approved Open WebUI image is ghcr.io/open-webui/open-webui:v0.10.2.

Docker host networking is prohibited.

Firewall weakening is prohibited.

Open WebUI Docker volume deletion or replacement is prohibited.

## Approved Models

The approved ADP v2.2 models are:

- llama3.2:1b
- llama3.2:3b

No additional models are approved for ADP v2.2.

## Pilot Boundary

The ADP v2.2 pilot may use only synthetic non-sensitive Markdown test documents.

Real documents are prohibited.

Production data is prohibited.

Sensitive data is prohibited.

The pilot must document loading, retrieval, answer quality, removal, and post-removal behavior.
