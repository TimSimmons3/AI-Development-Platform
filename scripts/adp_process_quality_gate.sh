#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$HOME/Labs/AI-Development-Platform}"
cd "$REPO"

printf '===== ADP PROCESS QUALITY GATE =====\n'

required=(
  docs/ADP-Controlled-Execution-Packet-Standard.md
  docs/ADP-Final-Delivery-Validation-Standard.md
  docs/ADP-Test-Execution-Consistency-and-Evidence-Lifecycle-Standard.md
  docs/ADP-Process-Quality-Gate-Checklist.md
  docs/ADP-v2.3.1-Gate-C-Runtime-Procedure-Reset-and-Supersession-Record.md
  docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md
  docs/ADP-v2.3.1-Gate-C-Fresh-Runtime-Operator-Guide.md
  scripts/adp231_gate_c_fresh_runtime.sh
  skills/adp-controlled-execution-packets/SKILL.md
)

for file in "${required[@]}"; do
  test -s "$file"
done
printf 'REQUIRED_ARTIFACT_STATUS=PASS\n'

while IFS= read -r file; do
  LC_ALL=C grep -n '[^ -~]' "$file" && false
  grep -n $'\t' "$file" && false
  grep -nE '[[:blank:]]+$' "$file" && false
done < <(printf '%s\n' "${required[@]}")
printf 'TEXT_QUALITY_STATUS=PASS\n'

bash -n scripts/adp231_gate_c_fresh_runtime.sh
printf 'SCRIPT_SYNTAX_STATUS=PASS\n'

current_docs=(
  docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md
  docs/ADP-v2.3.1-Gate-C-Fresh-Runtime-Operator-Guide.md
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
    printf 'SUPERSEDED_REFERENCE_STATUS=FAIL\n'
    printf 'TOKEN=%s\n' "$token"
    exit 1
  fi
done
printf 'SUPERSEDED_REFERENCE_STATUS=PASS\n'

grep -Fq 'scripts/adp231_gate_c_fresh_runtime.sh' "${current_docs[@]}"
grep -Fq 'VOIDED_NOT_COUNTED' docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md
grep -Fq 'No Mid-Run Patching' docs/ADP-Test-Execution-Consistency-and-Evidence-Lifecycle-Standard.md
grep -Fq 'Active Workspace Hygiene' docs/ADP-Test-Execution-Consistency-and-Evidence-Lifecycle-Standard.md
grep -Fq 'Operator Usability Gate' docs/ADP-Test-Execution-Consistency-and-Evidence-Lifecycle-Standard.md
printf 'SEMANTIC_CONTROL_STATUS=PASS\n'

for name in \
  01-membership-before-run.png \
  02-fresh-empty-chat.png \
  03-collection-attached-before-prompt.png \
  response.txt \
  04-complete-response.png \
  05-displayed-source-panel.png
do
  grep -Fq "$name" docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md
  grep -Fq "$name" docs/ADP-v2.3.1-Gate-C-Fresh-Runtime-Operator-Guide.md
done
printf 'EVIDENCE_FILENAME_ALIGNMENT_STATUS=PASS\n'

git diff --check
printf 'GIT_DIFF_CHECK_STATUS=PASS\n'
printf 'PROCESS_QUALITY_GATE_STATUS=PASS\n'
