#!/usr/bin/env bash
set -euo pipefail
RESULT_1B="tests/model-validation/results/20260702-200115-llama3.2_1b.jsonl"
RESULT_3B="tests/model-validation/results/20260702-200458-llama3.2_3b.jsonl"
echo "===== ADP v1.5 FUNCTIONAL VALIDATION ====="
echo
echo "Step 1: Generate summary for llama3.2:1b"
scripts/summarize-model-validation-results.sh "$RESULT_1B"
echo
echo "Step 2: Generate summary for llama3.2:3b"
scripts/summarize-model-validation-results.sh "$RESULT_3B"
echo
echo "Step 3: Validate structured JSON for llama3.2:1b"
scripts/validate-json-prompt-output.sh "$RESULT_1B"
echo
echo "Step 4: Expected negative test for llama3.2:3b structured JSON"
echo "Expected result: validator must reject the known malformed v1.4 3b JSON output."
set +e
THREE_B_OUTPUT="$(scripts/validate-json-prompt-output.sh "$RESULT_3B" 2>&1)"
THREE_B_STATUS=$?
set -e
if [[ "$THREE_B_STATUS" -eq 0 ]]; then
echo "ERROR: 3b known-bad JSON unexpectedly passed validation"
exit 1
fi
echo "PASS: 3b known-bad JSON was rejected as expected"
printf "%s\n" "$THREE_B_OUTPUT" | sed "s/^FAIL:/EXPECTED NEGATIVE TEST DETAIL:/"
echo
echo "PASS: ADP v1.5 functional validation completed"
