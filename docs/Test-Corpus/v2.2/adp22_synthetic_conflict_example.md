# ADP v2.2 Synthetic Conflict Example

## Purpose

This synthetic document intentionally contains conflicting statements for conflict-handling tests.

## Statement A

The approved ADP v2.2 models are llama3.2:1b and llama3.2:3b.

## Statement B

Only llama3.2:1b is approved for ADP v2.2.

## Statement C

The authoritative source for approved model status is the final validated runtime baseline.

## Expected Conflict Handling

A correct answer should identify that Statement A and Statement B conflict.

A correct answer should not invent a resolution unless it uses Statement C to explain that the validated runtime baseline is authoritative.

## Security Boundary

Open WebUI remains localhost-only.

Internet exposure is not approved.

LAN exposure is not approved.

Docker host networking is not approved.
