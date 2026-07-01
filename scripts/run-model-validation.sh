#!/usr/bin/env bash
set -euo pipefail
MODEL="${1:-}"
PROMPT_DIR="${PROMPT_DIR:-tests/model-validation/prompts}"
RESULT_DIR="${RESULT_DIR:-tests/model-validation/results}"
OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-180}"
if [[ -z "$MODEL" ]]; then
echo "Usage: $0 <ollama-model-name>"
echo "Example: $0 llama3.2:1b"
exit 1
fi
if [[ ! -d "$PROMPT_DIR" ]]; then
echo "ERROR: Prompt directory not found: $PROMPT_DIR"
exit 1
fi
mkdir -p "$RESULT_DIR"
RUN_ID="$(date +%Y%m%d-%H%M%S)"
SAFE_MODEL="$(echo "$MODEL" | tr '/:' '__')"
RESULT_FILE="$RESULT_DIR/${RUN_ID}-${SAFE_MODEL}.jsonl"
echo "===== ADP LOCAL MODEL VALIDATION ====="
echo "Model: $MODEL"
echo "Prompt directory: $PROMPT_DIR"
echo "Result file: $RESULT_FILE"
echo "Ollama URL: $OLLAMA_URL"
echo
echo "===== OLLAMA HEALTH CHECK ====="
curl -sS --fail --max-time 20 "$OLLAMA_URL/api/version" >/dev/null
echo "Ollama API reachable"
echo
PROMPT_COUNT=0
for PROMPT_FILE in "$PROMPT_DIR"/*.txt; do
if [[ ! -e "$PROMPT_FILE" ]]; then
echo "ERROR: No prompt files found in $PROMPT_DIR"
exit 1
fi
PROMPT_COUNT=$((PROMPT_COUNT + 1))
PROMPT_NAME="$(basename "$PROMPT_FILE")"
echo "===== RUNNING PROMPT: $PROMPT_NAME ====="
START_EPOCH="$(date +%s)"
TMP_PAYLOAD="$(mktemp)"
TMP_RESPONSE="$(mktemp)"
python3 -c 'import json,sys; from pathlib import Path; model=sys.argv[1]; prompt=Path(sys.argv[2]).read_text(encoding="utf-8"); print(json.dumps({"model":model,"prompt":prompt,"stream":False}))' "$MODEL" "$PROMPT_FILE" > "$TMP_PAYLOAD"
if curl -sS --fail --max-time "$TIMEOUT_SECONDS" -H 'Content-Type: application/json' -d @"$TMP_PAYLOAD" "$OLLAMA_URL/api/generate" > "$TMP_RESPONSE"; then
STATUS="success"
else
STATUS="error"
fi
END_EPOCH="$(date +%s)"
DURATION_SECONDS=$((END_EPOCH - START_EPOCH))
python3 -c 'import json,sys; from datetime import datetime,timezone; from pathlib import Path; raw=Path(sys.argv[6]).read_text(encoding="utf-8", errors="replace"); rec={"timestamp_utc":datetime.now(timezone.utc).isoformat(),"model":sys.argv[1],"prompt_name":sys.argv[2],"prompt_file":sys.argv[3],"status":sys.argv[4],"duration_seconds":int(sys.argv[5]),"raw_response_text":raw}; print(json.dumps(rec, ensure_ascii=False))' "$MODEL" "$PROMPT_NAME" "$PROMPT_FILE" "$STATUS" "$DURATION_SECONDS" "$TMP_RESPONSE" >> "$RESULT_FILE"
rm -f "$TMP_RESPONSE" "$TMP_PAYLOAD"
echo "Status: $STATUS"
echo "Duration seconds: $DURATION_SECONDS"
echo
done
echo "===== VALIDATION RUN COMPLETE ====="
echo "Prompts executed: $PROMPT_COUNT"
echo "Result file: $RESULT_FILE"
echo
echo "Reminder: raw result files are runtime evidence and should remain uncommitted unless sanitized and approved."
