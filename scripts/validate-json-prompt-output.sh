#!/usr/bin/env bash
set -euo pipefail

RESULT_FILE="${1:-}"
PROMPT_NAME_FILTER="${2:-03-structured-json-output.txt}"

if [[ -z "$RESULT_FILE" ]]; then
echo "Usage: $0 <result-jsonl-file> [prompt-name]"
echo "Example: $0 tests/model-validation/results/20260702-200115-llama3.2_1b.jsonl 03-structured-json-output.txt"
exit 1
fi

if [[ ! -f "$RESULT_FILE" ]]; then
echo "ERROR: Result file not found: $RESULT_FILE"
exit 1
fi

python3 - "$RESULT_FILE" "$PROMPT_NAME_FILTER" <<'PY'
import json
import sys
from pathlib import Path

result_path = Path(sys.argv[1])
prompt_filter = sys.argv[2]

records = []

with result_path.open("r", encoding="utf-8") as handle:
    for line_number, line in enumerate(handle, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"FAIL: Invalid JSONL at line {line_number}: {exc}")
        if record.get("prompt_name") == prompt_filter:
            records.append(record)

if not records:
    raise SystemExit(f"FAIL: No result found for prompt: {prompt_filter}")

failures = 0

for record in records:
    raw_text = record.get("raw_response_text", "")

    try:
        ollama_payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        print(f"FAIL: Raw Ollama response is not valid JSON for {record.get('prompt_name')}: {exc}")
        failures += 1
        continue

    response_text = ollama_payload.get("response", "")

    if not isinstance(response_text, str) or not response_text.strip():
        print(f"FAIL: Missing response text for {record.get('prompt_name')}")
        failures += 1
        continue

    candidate = response_text.strip()

    if candidate.startswith("```"):
        print(f"FAIL: Response uses markdown code fences instead of JSON-only output for {record.get('prompt_name')}")
        failures += 1
        continue

    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError as exc:
        print(f"FAIL: Model response is not valid JSON for {record.get('prompt_name')}: {exc}")
        failures += 1
        continue

    if not isinstance(parsed, dict):
        print(f"FAIL: Model JSON output is valid JSON but not a JSON object for {record.get('prompt_name')}")
        failures += 1
        continue

    print(f"PASS: Valid JSON object output for {record.get('prompt_name')}")

if failures:
    raise SystemExit(1)
PY
