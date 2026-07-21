#!/usr/bin/env bash
set -euo pipefail

EXPECTED_BASELINE="253e9dd"
EXPECTED_PLAN_SHA="130a79ba28ef428e033b7b913f9545395d20d72511a8fbe68e6edc3c370943f7"
EXPECTED_GATE_B_SHA="35fd09281bca5bc0c6e803bd9beed56bce9d4eccecd15a7ef79fb92d9fbf8e59"
EXPECTED_IMAGE="ghcr.io/open-webui/open-webui:v0.10.2"
EXPECTED_OLLAMA_VERSION="0.30.11"
EXPECTED_TIMESHIFT_ID="2026-07-20_11-32-48"
EXPECTED_TIMESHIFT_DESC="ADP-v2.3-reg-hardening-t01-failure-closeout"
REPO="$HOME/Labs/AI-Development-Platform"
PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAMP="$(date '+%Y%m%d-%H%M%S')"
TRANSCRIPT="/tmp/ADP-v2.3.1-Gate-C-Promotion-$STAMP.log"

exec > >(tee "$TRANSCRIPT") 2>&1

printf '\n===== PACKET =====\n'
printf 'PACKET_ID=V231-C-PROMOTE-01\n'
printf 'PACKAGE_DIR=%s\n' "$PACKAGE_DIR"
printf 'REPO=%s\n' "$REPO"
printf 'TRANSCRIPT=%s\n' "$TRANSCRIPT"

printf '\n===== STARTING REPOSITORY BASELINE =====\n'
cd "$REPO"
git fetch origin main
printf 'BRANCH=%s\n' "$(git branch --show-current)"
printf 'HEAD=%s\n' "$(git rev-parse --short HEAD)"
printf 'MAIN=%s\n' "$(git rev-parse --short main)"
printf 'ORIGIN_MAIN=%s\n' "$(git rev-parse --short origin/main)"
printf 'WORKTREE_COUNT=%s\n' "$(git status --porcelain | wc -l | tr -d ' ')"
test "$(git branch --show-current)" = "main"
test "$(git rev-parse --short HEAD)" = "$EXPECTED_BASELINE"
test "$(git rev-parse --short main)" = "$EXPECTED_BASELINE"
test "$(git rev-parse --short origin/main)" = "$EXPECTED_BASELINE"
test -z "$(git status --porcelain)"
git diff --check
printf 'STARTING_BASELINE_STATUS=PASS\n'

printf '\n===== CONTROLLING CHECKSUMS =====\n'
printf '%s  %s\n' "$EXPECTED_PLAN_SHA" "docs/ADP-v2.3.1-RAG-Retrieval-Pipeline-and-Model-Behavior-Diagnostic-Plan.md" | sha256sum -c -
printf '%s  %s\n' "$EXPECTED_GATE_B_SHA" "docs/ADP-v2.3.1-Entry-and-Runtime-Baseline-Record.md" | sha256sum -c -
printf 'CONTROLLING_CHECKSUM_STATUS=PASS\n'

printf '\n===== PACKAGE VALIDATION =====\n'
cd "$PACKAGE_DIR"
sha256sum -c ADP-v2.3.1-Gate-C-Validated-Delivery-Package-SHA256.txt
while IFS= read -r file; do
    LC_ALL=C grep -n '[^ -~]' "$file" && false
    grep -n $'\t' "$file" && false
    grep -nE '[[:blank:]]+$' "$file" && false
    test -s "$file"
done < <(find . -type f \( -name '*.md' -o -name '*.sh' \) -print | sort)
bash -n scripts/adp231_gate_c_promote.sh
printf 'PACKAGE_VALIDATION_STATUS=PASS\n'

printf '\n===== CONTROLLED COPY =====\n'
cd "$REPO"
install -d docs test-data/rag/v2.3.1 skills/adp-controlled-execution-packets scripts
cp "$PACKAGE_DIR/ADP-Controlled-Execution-Packet-Standard.md" docs/ADP-Controlled-Execution-Packet-Standard.md
cp "$PACKAGE_DIR/ADP-Final-Delivery-Validation-Standard.md" docs/ADP-Final-Delivery-Validation-Standard.md
cp "$PACKAGE_DIR/skills/adp-controlled-execution-packets/SKILL.md" skills/adp-controlled-execution-packets/SKILL.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md" docs/ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md" docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Gate-C-New-Chat-Startup-v2.md" docs/ADP-v2.3.1-Gate-C-New-Chat-Startup-v2.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Gate-C-Execution-Model-Addendum.md" docs/ADP-v2.3.1-Gate-C-Execution-Model-Addendum.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Synthetic-Diagnostic-Data-Design.md" docs/ADP-v2.3.1-Synthetic-Diagnostic-Data-Design.md
cp "$PACKAGE_DIR/adp231_minimal_direct_retrieval.md" test-data/rag/v2.3.1/adp231_minimal_direct_retrieval.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Diagnostic-Prompt-Library.md" docs/ADP-v2.3.1-Diagnostic-Prompt-Library.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Diagnostic-Test-Record-Template.md" docs/ADP-v2.3.1-Diagnostic-Test-Record-Template.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Knowledge-Attachment-Evidence-Procedure.md" docs/ADP-v2.3.1-Knowledge-Attachment-Evidence-Procedure.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Gate-C-Artifact-Review-and-Approval-Record.md" docs/ADP-v2.3.1-Gate-C-Artifact-Review-and-Approval-Record.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Gate-C-Approved-Artifact-Manifest.md" docs/ADP-v2.3.1-Gate-C-Approved-Artifact-Manifest.md
cp "$PACKAGE_DIR/scripts/adp231_gate_c_promote.sh" scripts/adp231_gate_c_promote.sh
chmod 0755 scripts/adp231_gate_c_promote.sh
printf 'CONTROLLED_COPY_STATUS=PASS\n'

printf '\n===== PRE-COMMIT VALIDATION =====\n'
git status --short
git diff --check
while IFS= read -r file; do
    LC_ALL=C grep -n '[^ -~]' "$file" && false
    grep -n $'\t' "$file" && false
    grep -nE '[[:blank:]]+$' "$file" && false
done < <(git status --porcelain | awk '{print $2}' | grep -E '\.(md|sh)$' | sort)
bash -n scripts/adp231_gate_c_promote.sh
git diff --stat
git diff -- docs test-data skills scripts
printf 'PRE_COMMIT_VALIDATION_STATUS=PASS\n'

printf '\n===== COMMIT AND PUSH =====\n'
git add docs/ADP-Controlled-Execution-Packet-Standard.md
git add docs/ADP-Final-Delivery-Validation-Standard.md
git add docs/ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md
git add docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md
git add docs/ADP-v2.3.1-Gate-C-New-Chat-Startup-v2.md
git add docs/ADP-v2.3.1-Gate-C-Execution-Model-Addendum.md
git add docs/ADP-v2.3.1-Synthetic-Diagnostic-Data-Design.md
git add docs/ADP-v2.3.1-Diagnostic-Prompt-Library.md
git add docs/ADP-v2.3.1-Diagnostic-Test-Record-Template.md
git add docs/ADP-v2.3.1-Knowledge-Attachment-Evidence-Procedure.md
git add docs/ADP-v2.3.1-Gate-C-Artifact-Review-and-Approval-Record.md
git add docs/ADP-v2.3.1-Gate-C-Approved-Artifact-Manifest.md
git add test-data/rag/v2.3.1/adp231_minimal_direct_retrieval.md
git add skills/adp-controlled-execution-packets/SKILL.md
git add scripts/adp231_gate_c_promote.sh
git diff --cached --check
git diff --cached --stat
git diff --cached -- docs test-data skills scripts
git commit -m "Add ADP v2.3.1 Gate C artifacts and execution packet standard"
git push origin main
printf 'PROMOTION_STATUS=PASS\n'

printf '\n===== POST-PUSH SYNCHRONIZATION =====\n'
git fetch origin main
POST_HEAD="$(git rev-parse --short HEAD)"
POST_MAIN="$(git rev-parse --short main)"
POST_ORIGIN="$(git rev-parse --short origin/main)"
printf 'POST_HEAD=%s\n' "$POST_HEAD"
printf 'POST_MAIN=%s\n' "$POST_MAIN"
printf 'POST_ORIGIN_MAIN=%s\n' "$POST_ORIGIN"
test "$POST_HEAD" = "$POST_MAIN"
test "$POST_HEAD" = "$POST_ORIGIN"
test -z "$(git status --porcelain)"
printf 'SYNCHRONIZATION_STATUS=PASS\n'

printf '\n===== READ-ONLY PRE-RUNTIME VALIDATION =====\n'
OPEN_WEBUI_IMAGE="$(docker inspect -f '{{.Config.Image}}' open-webui)"
OPEN_WEBUI_HEALTH="$(docker inspect -f '{{.State.Health.Status}}' open-webui)"
OPEN_WEBUI_PORT="$(docker port open-webui 8080/tcp)"
OLLAMA_VERSION_OUTPUT="$(ollama --version 2>&1)"
OLLAMA_SERVICE="$(systemctl is-active ollama)"
OLLAMA_ENV="$(systemctl show ollama --property=Environment --value)"
MODEL_SET="$(ollama list | awk 'NR>1 {print $1}' | sort | tr '\n' ' ' | sed 's/ $//')"
UFW_STATUS="$(sudo ufw status | sed -n '1p')"
TIMESHIFT_LINE="$(sudo timeshift --list 2>/dev/null | grep -F "$EXPECTED_TIMESHIFT_ID" | tail -n 1)"
printf 'OPEN_WEBUI_IMAGE=%s\n' "$OPEN_WEBUI_IMAGE"
printf 'OPEN_WEBUI_HEALTH=%s\n' "$OPEN_WEBUI_HEALTH"
printf 'OPEN_WEBUI_PORT=%s\n' "$OPEN_WEBUI_PORT"
printf 'OLLAMA_VERSION=%s\n' "$OLLAMA_VERSION_OUTPUT"
printf 'OLLAMA_SERVICE=%s\n' "$OLLAMA_SERVICE"
printf 'OLLAMA_ENV=%s\n' "$OLLAMA_ENV"
printf 'MODEL_SET=%s\n' "$MODEL_SET"
printf 'UFW_STATUS=%s\n' "$UFW_STATUS"
printf 'TIMESHIFT_LINE=%s\n' "$TIMESHIFT_LINE"
test "$OPEN_WEBUI_IMAGE" = "$EXPECTED_IMAGE"
test "$OPEN_WEBUI_HEALTH" = "healthy"
test "$OPEN_WEBUI_PORT" = "127.0.0.1:3000"
printf '%s\n' "$OLLAMA_VERSION_OUTPUT" | grep -F "$EXPECTED_OLLAMA_VERSION"
test "$OLLAMA_SERVICE" = "active"
printf '%s\n' "$OLLAMA_ENV" | grep -F 'OLLAMA_HOST=0.0.0.0:11434'
test "$MODEL_SET" = "llama3.2:1b llama3.2:3b"
test "$UFW_STATUS" = "Status: active"
test -n "$TIMESHIFT_LINE"
case "$TIMESHIFT_LINE" in
  *"$EXPECTED_TIMESHIFT_DESC"*) ;;
  *) printf 'TIMESHIFT_BASELINE_STATUS=FAIL\n'; exit 1 ;;
esac
printf 'TIMESHIFT_BASELINE_STATUS=PASS\n'
printf 'READ_ONLY_PRE_RUNTIME_STATUS=PASS\n'

printf '\n===== PACKET RESULT =====\n'
printf 'PROMOTION_STATUS=PASS\n'
printf 'SYNCHRONIZATION_STATUS=PASS\n'
printf 'READ_ONLY_PRE_RUNTIME_STATUS=PASS\n'
printf 'TIMESHIFT_BASELINE_STATUS=PASS\n'
printf 'NEXT_PACKET=V231-C-RUNTIME-01\n'
printf 'TRANSCRIPT=%s\n' "$TRANSCRIPT"
