#!/usr/bin/env bash
set -euo pipefail

RESULT_FILE="${1:-}"

if [[ -z "$RESULT_FILE" ]]; then
echo "Usage: $0 <result-jsonl-file>"
echo "Example: $0 tests/model-validation/results/20260702-200115-llama3.2_1b.jsonl"
exit 1
fi

if [[ ! -f "$RESULT_FILE" ]]; then
echo "ERROR: Result file not found: $RESULT_FILE"
exit 1
fi

SUMMARY_FILE="${RESULT_FILE%.jsonl}-summary.md"

python3 - "$RESULT_FILE" "$SUMMARY_FILE" <<'PY'
import json
import sys
from pathlib import Path

result_path = Path(sys.argv[1])
summary_path = Path(sys.argv[2])

records = []

with result_path.open("r", encoding="utf-8") as handle:
    for line_number, line in enumerate(handle, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"ERROR: Invalid JSONL at line {line_number}: {exc}")

if not records:
    raise SystemExit("ERROR: No records found in result file")

model = records[0].get("model", "unknown")
successes = sum(1 for record in records if record.get("status") == "success")
failures = sum(1 for record in records if record.get("status") != "success")

durations = []
for record in records:
    value = record.get("duration_seconds", 0)
    try:
        durations.append(int(value))
    except Exception:
        pass

total_duration = sum(durations)
average_duration = round(total_duration / len(durations), 2) if durations else 0

def extract_response_text(raw_text):
    try:
        payload = json.loads(raw_text)
    except Exception:
        return raw_text.strip()
    if isinstance(payload, dict):
        value = payload.get("response")
        if isinstance(value, str):
            return value.strip()
    return raw_text.strip()

lines = []
lines.append("# ADP Model Validation Summary")
lines.append("")
lines.append("## Source")
lines.append("")
lines.append(f"- Result file: `{result_path}`")
lines.append(f"- Model: `{model}`")
lines.append(f"- Prompts executed: {len(records)}")
lines.append(f"- Successes: {successes}")
lines.append(f"- Failures: {failures}")
lines.append(f"- Total duration seconds: {total_duration}")
lines.append(f"- Average duration seconds: {average_duration}")
lines.append("")
lines.append("## Prompt Results")
lines.append("")
lines.append("| Prompt | Status | Duration Seconds | Extracted Response Preview |")
lines.append("|---|---:|---:|---|")

for record in records:
    prompt_name = record.get("prompt_name", "unknown")
    status = record.get("status", "unknown")
    duration = record.get("duration_seconds", "")
    raw_text = record.get("raw_response_text", "")
    response_text = extract_response_text(raw_text)
    preview = " ".join(response_text.split())
    if len(preview) > 220:
        preview = preview[:217] + "..."
    preview = preview.replace("|", "\\|")
    lines.append(f"| `{prompt_name}` | {status} | {duration} | {preview} |")

lines.append("")
lines.append("## Human Review Notes")
lines.append("")
lines.append("- Execution success does not mean the model output is audit-ready.")
lines.append("- Review response quality, instruction adherence, format compliance, and risk of unsupported claims.")
lines.append("- Raw JSONL remains local runtime evidence and should not be committed unless explicitly sanitized and approved.")
lines.append("")

summary_path.write_text("\n".join(lines), encoding="utf-8")
print(f"Summary written: {summary_path}")
PY

echo
echo "Reminder: review generated summaries before committing."
