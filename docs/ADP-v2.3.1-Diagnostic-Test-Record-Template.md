# ADP v2.3.1 Diagnostic Test Record Template

## 1. Test Identification

- Release: ADP v2.3.1
- Gate: Gate C - Minimal Retrieval
- Run number:
- Local date:
- Local start timestamp:
- Local end timestamp:
- Operator:
- Host: `smt-ai`
- Open WebUI image: `ghcr.io/open-webui/open-webui:v0.10.2`
- Open WebUI binding: `127.0.0.1:3000->8080/tcp`
- Ollama version: `0.30.11`
- Model: `llama3.2:3b`
- Knowledge collection: `ADP-v2.3.1-minimal-direct-retrieval`
- Source file: `adp231_minimal_direct_retrieval.md`
- Source SHA-256: `ea0288d0d8666438e8cf9ae7dd54e6da8aaa0818f42d15f29bdf7467acf77afc`
- Prompt ID: `V231-R01-P1-v2`
- Prompt SHA-256: `0c8ea2c72e6b6e3a002261e95308a3a2722a675d730cc2bd3c14eebe964befce`
- Fresh-chat evidence reference:
- Collection-membership evidence reference:
- Knowledge-attachment evidence reference:

## 2. Pre-Run Controls

- [ ] Repository working tree clean
- [ ] `HEAD`, `main`, and `origin/main` synchronized
- [ ] Approved Gate C artifacts present at canonical paths
- [ ] Open WebUI healthy and loopback-bound
- [ ] Ollama version remains `0.30.11`
- [ ] Only approved models present
- [ ] `llama3.2:3b` selected
- [ ] Fresh chat confirmed
- [ ] Intended Knowledge collection visibly attached
- [ ] Collection membership visibly shows exactly one approved source file
- [ ] No tool, web, function, terminal, or automation feature enabled in the chat
- [ ] Exact run-start timestamp captured before prompt submission
- [ ] No controlled variable changed

Run-start timestamp variable and evidence reference:

## 3. Exact Prompt

Paste the exact prompt without correction:

```text
[PASTE EXACT PROMPT]
```

Prompt SHA-256 verified against `0c8ea2c72e6b6e3a002261e95308a3a2722a675d730cc2bd3c14eebe964befce`:

- [ ] Yes
- [ ] No

Prompt comparison evidence reference:

## 4. Complete Response

Paste the complete response without correction:

```text
[PASTE COMPLETE RESPONSE]
```

Response screenshot reference:

## 5. V231-R01 Direct-Retrieval Assessment

Target sentence:

```text
The release objective for NOVA-231-DELTA is to verify that one exact synthetic fact can be retrieved from one attached source without adding outside information.
```

- [ ] Complete target sentence appears verbatim
- [ ] Target sentence is not contradicted
- [ ] No unsupported factual claim appears
- [ ] No automation, reminder, scheduling, or iCalendar output appears

`V231-R01` result:

- [ ] PASS
- [ ] FAIL
- [ ] INCONCLUSIVE

Failure or inconclusive code:

- `R01-F01` Target sentence absent, incomplete, or incorrect
- `R01-F02` Contradictory or unsupported factual content
- `R01-F03` Automation, reminder, scheduling, or iCalendar output
- `R01-I01` Response evidence incomplete
- `R01-I02` Retrieval cannot be distinguished from another uncontrolled condition

Assessment notes:

## 6. V231-S01 Displayed-Source Assessment

- Displayed source filename:
- Displayed source passage:
- Displayed source order:
- Retrieval score, if exposed:
- Source-evidence screenshot reference:

- [ ] Displayed source evidence is available
- [ ] Displayed source filename is exactly `adp231_minimal_direct_retrieval.md`
- [ ] Displayed passage contains the complete target sentence
- [ ] Displayed source evidence does not conflict with the answer

`V231-S01` result:

- [ ] PASS
- [ ] FAIL
- [ ] INCONCLUSIVE

Failure or inconclusive code:

- `S01-F01` Wrong displayed source file
- `S01-F02` Wrong displayed source passage
- `S01-F03` Displayed source evidence conflicts with the answer
- `S01-I01` Displayed source evidence unavailable or incomplete

Assessment notes:

## 7. Formatting Observation Only

The following observations do not independently fail Gate C. They are retained for later `V231-F01` planning.

- [ ] Response contains only the target sentence
- [ ] Response contains a preface
- [ ] Response contains additional source-supported text
- [ ] Response contains labels or other structure
- [ ] Response has another formatting deviation

Formatting observation:

## 8. Prompt-Truncation Assessment

- Exact run-start timestamp:
- Exact run-end timestamp:
- Bounded Ollama log evidence reference:
- Matching warning count:
- Full matching warning line or lines:

- [ ] No new `truncating input prompt` warning appears in the exact run window
- [ ] A new `truncating input prompt` warning appears in the exact run window
- [ ] Required log evidence is unavailable

Truncation result:

- [ ] PASS
- [ ] FAIL
- [ ] INCONCLUSIVE

Failure or inconclusive code:

- `ENV-F01` New prompt-truncation warning
- `ENV-I01` Bounded truncation evidence unavailable or ambiguous

## 9. Evidence and Control Assessment

- [ ] Fresh-chat state proven
- [ ] Collection membership proven
- [ ] Attachment state proven
- [ ] Exact prompt retained
- [ ] Complete response retained
- [ ] Displayed-source evidence retained
- [ ] Bounded truncation evidence retained
- [ ] Model and runtime boundary unchanged

Evidence or control code:

- `ENV-I02` Fresh-chat state unproven
- `ENV-I03` Collection membership unproven
- `ENV-I04` Attachment state unproven
- `ENV-I05` Controlled variable changed
- `ENV-I06` Required evidence incomplete

## 10. Overall Run Classification

A run is PASS only when:

- `V231-R01` is PASS
- `V231-S01` is PASS
- Truncation result is PASS
- Evidence and control assessment is complete

Overall result:

- [ ] PASS
- [ ] FAIL
- [ ] INCONCLUSIVE

Count toward the three-run block:

- [ ] Yes
- [ ] No

Block status after this run:

- [ ] Continue automatically to next run
- [ ] Three-run block PASS
- [ ] STOP

Automatic-continuation rule:

- When this run is PASS, required evidence is complete, no stop condition occurred, and the run number is less than 3, continue directly to the next fresh-chat run without external approval.
- When this run is FAIL or INCONCLUSIVE, stop the packet immediately.

Decision rationale:

## 11. Evidence Integrity Statement

I preserved the exact prompt, complete response, displayed-source evidence, timestamps, model, collection state, attachment state, and bounded truncation evidence without silently correcting or reinterpreting the output.

- Operator confirmation:
- Date:
