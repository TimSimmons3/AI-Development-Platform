#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$HOME/Labs/AI-Development-Platform}"
cd "$REPO"

fail() {
  printf 'PROCESS_QUALITY_GATE_STATUS=FAIL\n'
  printf 'FAILED_CONTROL=%s\n' "$1"
  if [ "${2:-}" != "" ]; then
    printf 'FAILED_VALUE=%s\n' "$2"
  fi
  exit 1
}

printf '===== ADP PROCESS QUALITY GATE =====\n'

required=(
  docs/ADP-Controlled-Execution-Packet-Standard.md
  docs/ADP-Final-Delivery-Validation-Standard.md
  docs/ADP-Test-Execution-Consistency-and-Evidence-Lifecycle-Standard.md
  docs/ADP-Process-Quality-Gate-Checklist.md
  docs/ADP-v2.3.1-Gate-C-Runtime-Procedure-Reset-and-Supersession-Record.md
  docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md
  docs/ADP-v2.3.1-Gate-C-Fresh-Runtime-Operator-Guide.md
  docs/ADP-v2.3.1-Gate-C-Response-Capture-Corrective-Record.md
  scripts/adp231_gate_c_fresh_runtime.sh
  scripts/adp_process_quality_gate.sh
  skills/adp-controlled-execution-packets/SKILL.md
)

for file in "${required[@]}"; do
  test -s "$file" || fail "REQUIRED_ARTIFACT" "$file"
done
printf 'REQUIRED_ARTIFACT_STATUS=PASS\n'

while IFS= read -r file; do
  if LC_ALL=C grep -n '[^ -~]' "$file"; then
    fail "NON_ASCII_TEXT" "$file"
  fi
  if grep -n $'\t' "$file"; then
    fail "TAB_CHARACTER" "$file"
  fi
  if grep -nE '[[:blank:]]+$' "$file"; then
    fail "TRAILING_WHITESPACE" "$file"
  fi
done < <(printf '%s\n' "${required[@]}")
printf 'TEXT_QUALITY_STATUS=PASS\n'

bash -n scripts/adp231_gate_c_fresh_runtime.sh || fail "RUNTIME_SCRIPT_SYNTAX"
bash -n scripts/adp_process_quality_gate.sh || fail "QUALITY_GATE_SCRIPT_SYNTAX"
printf 'SCRIPT_SYNTAX_STATUS=PASS\n'

current_docs=(
  docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md
  docs/ADP-v2.3.1-Gate-C-Fresh-Runtime-Operator-Guide.md
  docs/ADP-v2.3.1-Gate-C-Response-Capture-Corrective-Record.md
  docs/ADP-v2.3.1-Gate-C-New-Chat-Startup-v2.md
  skills/adp-controlled-execution-packets/SKILL.md
)

banned=(
  gatec_fresh_runtime_v1.sh
  gatec_fresh_runtime_v2.sh
  gatec_run_v2.sh
  gatec_setup_finalize_v2.sh
  ADP-v2.3.1-Gate-C-Runtime-Tools-v1
)

for token in "${banned[@]}"; do
  if grep -Fq "$token" "${current_docs[@]}"; then
    fail "SUPERSEDED_REFERENCE" "$token"
  fi
done
printf 'SUPERSEDED_REFERENCE_STATUS=PASS\n'

grep -Fq 'scripts/adp231_gate_c_fresh_runtime.sh' "${current_docs[@]}" || fail "CANONICAL_SCRIPT_REFERENCE"
grep -Fq 'VOIDED_NOT_COUNTED' docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md || fail "VOID_CLASSIFICATION"
grep -Fq 'No Mid-Run Patching' docs/ADP-Test-Execution-Consistency-and-Evidence-Lifecycle-Standard.md || fail "NO_PATCHING_CONTROL"
grep -Fq 'Active Workspace Hygiene' docs/ADP-Test-Execution-Consistency-and-Evidence-Lifecycle-Standard.md || fail "WORKSPACE_HYGIENE_CONTROL"
grep -Fq 'Operator Usability Gate' docs/ADP-Test-Execution-Consistency-and-Evidence-Lifecycle-Standard.md || fail "OPERATOR_USABILITY_CONTROL"
printf 'SEMANTIC_CONTROL_STATUS=PASS\n'

for name in \
  01-membership-before-run.png \
  02-fresh-empty-chat.png \
  03-collection-attached-before-prompt.png \
  response.txt \
  04-complete-response.png \
  05-displayed-source-panel.png
do
  grep -Fq "$name" docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md || fail "PACKET_FILENAME_ALIGNMENT" "$name"
  grep -Fq "$name" docs/ADP-v2.3.1-Gate-C-Fresh-Runtime-Operator-Guide.md || fail "GUIDE_FILENAME_ALIGNMENT" "$name"
done
printf 'EVIDENCE_FILENAME_ALIGNMENT_STATUS=PASS\n'

grep -Fq 'capture-response' scripts/adp231_gate_c_fresh_runtime.sh || fail "CAPTURE_COMMAND_SCRIPT"
grep -Fq 'capture-response' docs/ADP-v2.3.1-Gate-C-Fresh-Runtime-Operator-Guide.md || fail "CAPTURE_COMMAND_GUIDE"
grep -Fq 'capture-response' docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md || fail "CAPTURE_COMMAND_PACKET"

if grep -Fq 'cat > "$E/run-' docs/ADP-v2.3.1-Gate-C-Fresh-Runtime-Operator-Guide.md docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md; then
  fail "PROHIBITED_RAW_CAPTURE_METHOD"
fi
printf 'RESPONSE_CAPTURE_METHOD_STATUS=PASS\n'

git diff --check || fail "GIT_DIFF_CHECK"
printf 'GIT_DIFF_CHECK_STATUS=PASS\n'
printf 'PROCESS_QUALITY_GATE_STATUS=PASS\n'
