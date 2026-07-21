#!/usr/bin/env bash
set -euo pipefail

COMMAND="${1:-}"
RUN="${2:-}"

case "$COMMAND" in
  reset|setup-verify|run-start|run-finish|package|status) ;;
  *)
    printf 'USAGE:\n'
    printf '  %s reset\n' "$0"
    printf '  %s setup-verify\n' "$0"
    printf '  %s run-start 1|2|3\n' "$0"
    printf '  %s run-finish 1|2|3\n' "$0"
    printf '  %s package\n' "$0"
    printf '  %s status\n' "$0"
    exit 64
    ;;
esac

if [ "$COMMAND" = "run-start" ] || [ "$COMMAND" = "run-finish" ]; then
  case "$RUN" in
    1|2|3) ;;
    *) printf 'RUN must be 1, 2, or 3.\n'; exit 64 ;;
  esac
fi

REPO="${ADP_REPO:-$HOME/Labs/AI-Development-Platform}"
EVIDENCE_POINTER="${ADP_EVIDENCE_POINTER:-/tmp/adp231_gate_c_evidence_dir}"
EXPECTED_SOURCE_SHA="ea0288d0d8666438e8cf9ae7dd54e6da8aaa0818f42d15f29bdf7467acf77afc"
EXPECTED_PROMPT_SHA="0c8ea2c72e6b6e3a002261e95308a3a2722a675d730cc2bd3c14eebe964befce"
EXPECTED_RUNTIME_PACKET_SHA="02df4a9348dc9d9e8e3ed84db007c7a59149599eb130e335e3f43aa22bf30c4a"
EXPECTED_PROMPT_LIBRARY_SHA="8e4744a2a756c67451641af836caa79e8c8c11bcbe13a84b14c894a9b2605cfb"
EXPECTED_TEST_TEMPLATE_SHA="bb64cbd8a4404f41aea8d536549ff318e7eaba07816d296d8277c96785ccc52f"
EXPECTED_EVIDENCE_PROCEDURE_SHA="0c74f375bf892c709307a55b127f7fb0aaf1f3f7a27dfdd89a7c177a31a01f47"
EXPECTED_IMAGE="ghcr.io/open-webui/open-webui:v0.10.2"
EXPECTED_OLLAMA_VERSION="0.30.11"
EXPECTED_MODEL_SET="llama3.2:1b llama3.2:3b"
EXPECTED_TIMESHIFT_ID="2026-07-20_11-32-48"
EXPECTED_TIMESHIFT_DESC="ADP-v2.3-reg-hardening-t01-failure-closeout"
TARGET_SENTENCE="The release objective for NOVA-231-DELTA is to verify that one exact synthetic fact can be retrieved from one attached source without adding outside information."
COLLECTION_NAME="ADP-v2.3.1-minimal-direct-retrieval"
SOURCE_NAME="adp231_minimal_direct_retrieval.md"
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
DOWNLOAD_DIR="${ADP_DOWNLOAD_DIR:-$HOME/Downloads}"
ARCHIVE_ROOT="${ADP_ARCHIVE_ROOT:-$DOWNLOAD_DIR/ADP-v2.3.1-Gate-C-Archive}"

yes_no() {
  local prompt="$1"
  local answer
  while true; do
    read -r -p "$prompt [y/n]: " answer
    case "$answer" in
      y|Y) return 0 ;;
      n|N) return 1 ;;
      *) printf 'Enter y or n.\n' ;;
    esac
  done
}

require_file() {
  local file="$1"
  local reason="$2"
  if [ ! -s "$file" ]; then
    printf 'STATUS=INCONCLUSIVE\n'
    printf 'MISSING_OR_EMPTY=%s\n' "$file"
    printf 'REASON=%s\n' "$reason"
    exit 3
  fi
}

validate_repository() {
  test -d "$REPO"
  cd "$REPO"

  if [ "${ADP_SKIP_FETCH:-0}" != "1" ]; then
    git fetch origin main
  fi

  local branch head main origin count
  branch="$(git branch --show-current)"
  head="$(git rev-parse --short HEAD)"
  main="$(git rev-parse --short main)"
  origin="$(git rev-parse --short origin/main)"
  count="$(git status --porcelain | wc -l | tr -d ' ')"

  printf 'BRANCH=%s\n' "$branch"
  printf 'HEAD=%s\n' "$head"
  printf 'MAIN=%s\n' "$main"
  printf 'ORIGIN_MAIN=%s\n' "$origin"
  printf 'WORKTREE_COUNT=%s\n' "$count"

  test "$branch" = "main"
  test "$head" = "$main"
  test "$head" = "$origin"
  test "$count" = "0"

  if [ -n "${LOCKED_BASELINE_COMMIT:-}" ]; then
    test "$head" = "$LOCKED_BASELINE_COMMIT"
  fi

  git diff --check
  printf 'REPOSITORY_STATE_STATUS=PASS\n'
}

validate_canonical_artifacts() {
  cd "$REPO"
  if [ "${ADP_SKIP_CANONICAL_HASH_CHECK:-0}" = "1" ]; then
    printf 'CANONICAL_RUNTIME_ARTIFACT_STATUS=TEST_BYPASS\n'
    return
  fi
  printf '%s  %s\n' "5a0b341e3d6bad2c8ed1ba50d06f4e185b5fbb431bfc654bc83774876974bcc4" "docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md" | sha256sum -c -
  printf '%s  %s\n' "8e4744a2a756c67451641af836caa79e8c8c11bcbe13a84b14c894a9b2605cfb" "docs/ADP-v2.3.1-Diagnostic-Prompt-Library.md" | sha256sum -c -
  printf '%s  %s\n' "bb64cbd8a4404f41aea8d536549ff318e7eaba07816d296d8277c96785ccc52f" "docs/ADP-v2.3.1-Diagnostic-Test-Record-Template.md" | sha256sum -c -
  printf '%s  %s\n' "0c74f375bf892c709307a55b127f7fb0aaf1f3f7a27dfdd89a7c177a31a01f47" "docs/ADP-v2.3.1-Knowledge-Attachment-Evidence-Procedure.md" | sha256sum -c -
  printf '%s  %s\n' "4e084a40abd1181379885e436cb37d567a952bb39272e2e53bdd9943c79cb621" "docs/ADP-Test-Execution-Consistency-and-Evidence-Lifecycle-Standard.md" | sha256sum -c -
  printf '%s  %s\n' "58efddf327d74a7d3b702948dd7f8daef8fce6848b5d10a4bbaa0e0f86b58c05" "docs/ADP-Process-Quality-Gate-Checklist.md" | sha256sum -c -
  printf '%s  %s\n' "458c45e7584a3af2901da6fac482d6ce9b2d189e5c553fbc0b6abcf3b3d6f5b6" "docs/ADP-v2.3.1-Gate-C-Runtime-Procedure-Reset-and-Supersession-Record.md" | sha256sum -c -
  printf '%s  %s\n' "ba91c7d2d914762a33abc38b4bf036d6b29a3dcf687ebb548a149cf39108ed34" "docs/ADP-v2.3.1-Gate-C-Fresh-Runtime-Operator-Guide.md" | sha256sum -c -
  printf 'CANONICAL_RUNTIME_ARTIFACT_STATUS=PASS\n'
}

validate_runtime_boundary() {
  if [ "${ADP_SKIP_RUNTIME_BOUNDARY:-0}" = "1" ]; then
    printf 'RUNTIME_BOUNDARY_STATUS=TEST_BYPASS\n'
    return
  fi

  local image health port ollama_version ollama_service ollama_env model_set ufw_status timeshift_line
  image="$(docker inspect -f '{{.Config.Image}}' open-webui)"
  health="$(docker inspect -f '{{.State.Health.Status}}' open-webui)"
  port="$(docker port open-webui 8080/tcp)"
  ollama_version="$(ollama --version | awk '{print $NF}')"
  ollama_service="$(systemctl is-active ollama)"
  ollama_env="$(systemctl show ollama --property=Environment --value)"
  model_set="$(ollama list | awk 'NR>1 {print $1}' | sort | tr '\n' ' ' | sed 's/ $//')"
  ufw_status="$(sudo ufw status | sed -n '1p')"
  timeshift_line="$(sudo timeshift --list 2>/dev/null | grep -F "$EXPECTED_TIMESHIFT_ID" | tail -n 1)"

  printf 'OPEN_WEBUI_IMAGE=%s\n' "$image"
  printf 'OPEN_WEBUI_HEALTH=%s\n' "$health"
  printf 'OPEN_WEBUI_PORT=%s\n' "$port"
  printf 'OLLAMA_VERSION=%s\n' "$ollama_version"
  printf 'OLLAMA_SERVICE=%s\n' "$ollama_service"
  printf 'OLLAMA_ENV=%s\n' "$ollama_env"
  printf 'MODEL_SET=%s\n' "$model_set"
  printf 'UFW_STATUS=%s\n' "$ufw_status"
  printf 'TIMESHIFT_LINE=%s\n' "$timeshift_line"

  test "$image" = "$EXPECTED_IMAGE"
  test "$health" = "healthy"
  test "$port" = "127.0.0.1:3000"
  test "$ollama_version" = "$EXPECTED_OLLAMA_VERSION"
  test "$ollama_service" = "active"
  printf '%s\n' "$ollama_env" | grep -F 'OLLAMA_HOST=0.0.0.0:11434' >/dev/null
  test "$model_set" = "$EXPECTED_MODEL_SET"
  test "$ufw_status" = "Status: active"
  test -n "$timeshift_line"
  case "$timeshift_line" in
    *"$EXPECTED_TIMESHIFT_DESC"*) ;;
    *) printf 'RUNTIME_BOUNDARY_STATUS=FAIL\n'; exit 1 ;;
  esac
  printf 'RUNTIME_BOUNDARY_STATUS=PASS\n'
}

current_evidence_dir() {
  test -s "$EVIDENCE_POINTER"
  cat "$EVIDENCE_POINTER"
}

write_run_status() {
  local dir="$1"
  local status="$2"
  local code="$3"
  {
    printf 'OVERALL_RUN_STATUS=%s\n' "$status"
    printf 'RESULT_CODE=%s\n' "$code"
    printf 'RUN=%s\n' "$RUN"
    printf 'RECORDED_AT=%s\n' "$(date --iso-8601=seconds)"
  } > "$dir/run-$RUN-status.env"
}

archive_item() {
  local source="$1"
  local destination_dir="$2"
  local manifest="$3"

  if [ ! -e "$source" ]; then
    return
  fi

  mkdir -p "$destination_dir"
  local name destination
  name="$(basename "$source")"
  destination="$destination_dir/$name"

  if [ -e "$destination" ]; then
    destination="$destination_dir/${name}-$(date '+%H%M%S')"
  fi

  if [ -f "$source" ]; then
    local sha size
    sha="$(sha256sum "$source" | awk '{print $1}')"
    size="$(wc -c < "$source" | tr -d ' ')"
    printf 'FILE|%s|%s|%s|%s\n' "$source" "$destination" "$sha" "$size" >> "$manifest"
  else
    printf 'DIRECTORY|%s|%s|-|-\n' "$source" "$destination" >> "$manifest"
  fi

  mv "$source" "$destination"
}

if [ "$COMMAND" = "reset" ]; then
  printf '===== GATE C FRESH RUNTIME RESET V2 =====\n'
  validate_repository
  validate_canonical_artifacts
  validate_runtime_boundary

  STAMP="$(date '+%Y%m%d-%H%M%S')"
  ARCHIVE_SESSION="$ARCHIVE_ROOT/reset-$STAMP"
  VOIDED_DIR="$ARCHIVE_SESSION/voided-evidence"
  SUPERSEDED_DIR="$ARCHIVE_SESSION/superseded-runtime-tools"
  LOOSE_DIR="$ARCHIVE_SESSION/loose-first-attempt-files"
  CLEANUP_MANIFEST="$ARCHIVE_SESSION/CLEANUP-MANIFEST.txt"

  mkdir -p "$VOIDED_DIR" "$SUPERSEDED_DIR" "$LOOSE_DIR"
  {
    printf 'RESET_TIMESTAMP=%s\n' "$(date --iso-8601=seconds)"
    printf 'RESET_REASON=First runtime attempt voided because the procedure and evidence design changed before a valid counted run completed.\n'
    printf 'COUNTED_RUNS=0\n'
    printf 'ARCHIVE_SESSION=%s\n' "$ARCHIVE_SESSION"
    printf '\nTYPE|SOURCE|ARCHIVE_DESTINATION|SHA256|BYTES\n'
  } > "$CLEANUP_MANIFEST"

  OLD_E=""
  if [ -s "$EVIDENCE_POINTER" ]; then
    OLD_E="$(cat "$EVIDENCE_POINTER")"
  fi

  if [ -n "$OLD_E" ] && [ -d "$OLD_E" ]; then
    OLD_NAME="$(basename "$OLD_E")"
    VOIDED="$VOIDED_DIR/$OLD_NAME"
    mv "$OLD_E" "$VOIDED"
    {
      printf 'VOID_STATUS=VOIDED_NOT_COUNTED\n'
      printf 'VOID_REASON=Runtime procedure and evidence design changed before a valid counted run completed.\n'
      printf 'VOIDED_AT=%s\n' "$(date --iso-8601=seconds)"
      printf 'ORIGINAL_PATH=%s\n' "$OLD_E"
      printf 'VOIDED_PATH=%s\n' "$VOIDED"
      printf 'COUNTED_RUNS=0\n'
    } > "$VOIDED/VOID-RECORD.txt"
    printf 'DIRECTORY|%s|%s|-|-\n' "$OLD_E" "$VOIDED" >> "$CLEANUP_MANIFEST"
    printf 'VOIDED_EVIDENCE_DIR=%s\n' "$VOIDED"
    printf 'FIRST_ATTEMPT_STATUS=VOIDED_NOT_COUNTED\n'
  else
    printf 'FIRST_ATTEMPT_STATUS=NO_EXISTING_WORKSPACE\n'
  fi

  # Archive loose first-attempt evidence and upload copies.
  archive_item "$DOWNLOAD_DIR/prior-collection-absent.png" "$LOOSE_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/new-collection-membership.png" "$LOOSE_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/adp231_minimal_direct_retrieval.md" "$LOOSE_DIR" "$CLEANUP_MANIFEST"

  # Archive superseded runtime scripts, toolkits, checksum files, and guides.
  archive_item "$DOWNLOAD_DIR/adp231_gate_c_runtime_prep_revalidate.sh" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/adp231_gate_c_runtime_prep_revalidate.sh.sha256" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/gatec_setup_finalize_v2.sh" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/gatec_setup_finalize_v2.sh.sha256" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/gatec_run_v2.sh" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/gatec_run_v2.sh.sha256" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/gatec_runtime_tools.sh" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/gatec_runtime_tools.sh.sha256" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/ADP-v2.3.1-Gate-C-Runtime-Tools-Installer-v1.sh" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/ADP-v2.3.1-Gate-C-Runtime-Tools-Installer-v1.sh.sha256" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/ADP-v2.3.1-Gate-C-Runtime-Tools-v1" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/ADP_v2.3.1_Gate_C_Runtime_Operator_Guide_v1.0.docx" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/ADP_v2.3.1_Gate_C_Fresh_Runtime_Operator_Guide_v2.0.docx" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/gatec_fresh_runtime_v1.sh" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"
  archive_item "$DOWNLOAD_DIR/gatec_fresh_runtime_v1.sh.sha256" "$SUPERSEDED_DIR" "$CLEANUP_MANIFEST"

  # Verify the active Downloads area no longer contains known superseded items.
  for stale in \
    prior-collection-absent.png \
    new-collection-membership.png \
    adp231_minimal_direct_retrieval.md \
    adp231_gate_c_runtime_prep_revalidate.sh \
    gatec_setup_finalize_v2.sh \
    gatec_run_v2.sh \
    gatec_runtime_tools.sh \
    ADP-v2.3.1-Gate-C-Runtime-Tools-Installer-v1.sh \
    ADP-v2.3.1-Gate-C-Runtime-Tools-v1 \
    ADP_v2.3.1_Gate_C_Runtime_Operator_Guide_v1.0.docx \
    ADP_v2.3.1_Gate_C_Fresh_Runtime_Operator_Guide_v2.0.docx \
    gatec_fresh_runtime_v1.sh
  do
    test ! -e "$DOWNLOAD_DIR/$stale"
  done

  test -s "$CLEANUP_MANIFEST"
  printf 'FIRST_ATTEMPT_FOLDER_CLEANUP_STATUS=PASS\n'
  printf 'SUPERSEDED_ARTIFACT_CLEANUP_STATUS=PASS\n'
  printf 'CLEANUP_ARCHIVE=%s\n' "$ARCHIVE_SESSION"
  printf 'CLEANUP_MANIFEST=%s\n' "$CLEANUP_MANIFEST"

  E="$DOWNLOAD_DIR/ADP-v2.3.1-Gate-C-Evidence-FRESH-$STAMP"
  mkdir -p "$E/setup" "$E/run-1" "$E/run-2" "$E/run-3"
  printf '%s\n' "$E" > "$EVIDENCE_POINTER"

  cd "$REPO"
  LOCKED_BASELINE_COMMIT="$(git rev-parse --short HEAD)"
  SCRIPT_SHA256="$(sha256sum "$SCRIPT_PATH" | awk '{print $1}')"
  {
    printf 'LOCKED_BASELINE_COMMIT=%s\n' "$LOCKED_BASELINE_COMMIT"
    printf 'SCRIPT_SHA256=%s\n' "$SCRIPT_SHA256"
    printf 'PROCEDURE_PACKET=V231-C-RUNTIME-02\n'
    printf 'PROCEDURE_STATUS=FROZEN\n'
    printf 'FROZEN_AT=%s\n' "$(date --iso-8601=seconds)"
  } > "$E/setup/baseline.env"

  SOURCE_FILE="test-data/rag/v2.3.1/$SOURCE_NAME"
  PROMPT_LIBRARY="docs/ADP-v2.3.1-Diagnostic-Prompt-Library.md"
  TEST_TEMPLATE="docs/ADP-v2.3.1-Diagnostic-Test-Record-Template.md"

  test "$(sha256sum "$SOURCE_FILE" | awk '{print $1}')" = "$EXPECTED_SOURCE_SHA"
  cp "$SOURCE_FILE" "$E/setup/$SOURCE_NAME"
  test "$(sha256sum "$E/setup/$SOURCE_NAME" | awk '{print $1}')" = "$EXPECTED_SOURCE_SHA"

  awk 'BEGIN{s=0;c=0} /^## 3\. Approved Frozen Prompt$/ {s=1} s && /^```text$/ {c=1; next} c && /^```$/ {exit} c {print}' "$PROMPT_LIBRARY" > "$E/setup/V231-R01-P1-v2.txt"
  truncate -s -1 "$E/setup/V231-R01-P1-v2.txt"
  test "$(sha256sum "$E/setup/V231-R01-P1-v2.txt" | awk '{print $1}')" = "$EXPECTED_PROMPT_SHA"

  for n in 1 2 3; do
    cp "$TEST_TEMPLATE" "$E/run-$n/run-$n-record.md"
  done

  {
    printf 'COLLECTION_TO_DELETE=%s\n' "$COLLECTION_NAME"
    printf 'COLLECTION_TO_RECREATE=%s\n' "$COLLECTION_NAME"
    printf 'UPLOAD_FILE=%s\n' "$E/setup/$SOURCE_NAME"
    printf 'SETUP_SCREENSHOT_1=%s\n' "$E/setup/01-prior-collection-absent.png"
    printf 'SETUP_SCREENSHOT_2=%s\n' "$E/setup/02-new-collection-one-file.png"
    printf 'VOIDED_CHAT_ACTION=Delete every Open WebUI chat created for the voided first attempt.\n'
  } > "$E/setup/NEXT-STEPS.txt"

  printf 'PROCEDURE_FREEZE_STATUS=PASS\n'
  printf 'LOCKED_BASELINE_COMMIT=%s\n' "$LOCKED_BASELINE_COMMIT"
  printf 'LOCAL_EVIDENCE_RESET_STATUS=PASS\n'
  printf 'NEW_EVIDENCE_DIR=%s\n' "$E"
  printf 'WEBUI_RESET_REQUIRED=YES\n'
  printf 'NEXT_STEP=DELETE_VOIDED_CHATS_AND_RECREATE_KNOWLEDGE_COLLECTION\n'
  printf '\n'
  printf 'In Open WebUI:\n'
  printf '1. Delete every chat created for the voided first attempt.\n'
  printf '2. Delete the current collection named %s.\n' "$COLLECTION_NAME"
  printf '3. Return to the Knowledge list and prove the collection is absent.\n'
  printf '4. Save that screenshot as 01-prior-collection-absent.png in the new setup folder.\n'
  printf '5. Recreate the same collection name.\n'
  printf '6. Upload only %s from the new setup folder.\n' "$SOURCE_NAME"
  printf '7. Save the one-file collection screenshot as 02-new-collection-one-file.png.\n'
  printf '8. Run: bash "$HOME/Labs/AI-Development-Platform/scripts/adp231_gate_c_fresh_runtime.sh" setup-verify\n'
  exit 0
fi

if [ "$COMMAND" = "status" ]; then
  printf '===== GATE C FRESH RUNTIME STATUS =====\n'
  validate_repository
  E="$(current_evidence_dir)"
  require_file "$E/setup/baseline.env" "The frozen baseline record is missing."
  source "$E/setup/baseline.env"
  test "$(sha256sum "$SCRIPT_PATH" | awk '{print $1}')" = "$SCRIPT_SHA256"
  validate_repository
  printf 'LOCKED_BASELINE_COMMIT=%s\n' "$LOCKED_BASELINE_COMMIT"
  printf 'EVIDENCE_DIR=%s\n' "$E"
  if [ -f "$E/setup/setup-status.env" ]; then
    cat "$E/setup/setup-status.env"
  else
    printf 'OPEN_WEBUI_SETUP_STATUS=NOT_COMPLETE\n'
  fi
  for n in 1 2 3; do
    if [ -f "$E/run-$n/run-$n-status.env" ]; then
      printf 'RUN_%s_STATUS_FILE=%s\n' "$n" "$E/run-$n/run-$n-status.env"
      cat "$E/run-$n/run-$n-status.env"
    else
      printf 'RUN_%s_STATUS=NOT_COMPLETE\n' "$n"
    fi
  done
  exit 0
fi

E="$(current_evidence_dir)"
test -d "$E"
require_file "$E/setup/baseline.env" "The frozen baseline record is missing."
source "$E/setup/baseline.env"
test "$PROCEDURE_STATUS" = "FROZEN"
test "$PROCEDURE_PACKET" = "V231-C-RUNTIME-02"
test "$(sha256sum "$SCRIPT_PATH" | awk '{print $1}')" = "$SCRIPT_SHA256"
validate_repository

if [ "$COMMAND" = "setup-verify" ]; then
  printf '===== GATE C FRESH WEBUI SETUP VERIFICATION =====\n'
  validate_canonical_artifacts
  validate_runtime_boundary

  ABSENCE="$E/setup/01-prior-collection-absent.png"
  MEMBERSHIP="$E/setup/02-new-collection-one-file.png"
  require_file "$ABSENCE" "Fresh Knowledge-list screenshot is required after deleting the current collection."
  require_file "$MEMBERSHIP" "Fresh one-file membership screenshot is required after recreating the collection."

  yes_no "Does 01-prior-collection-absent.png show that $COLLECTION_NAME is absent before recreation?" || { printf 'OPEN_WEBUI_SETUP_STATUS=INCONCLUSIVE\n'; exit 3; }
  yes_no "Does 02-new-collection-one-file.png show $COLLECTION_NAME with exactly one file named $SOURCE_NAME?" || { printf 'OPEN_WEBUI_SETUP_STATUS=INCONCLUSIVE\n'; exit 3; }
  yes_no "Have all Open WebUI chats created for the voided first attempt been deleted?" || { printf 'OPEN_WEBUI_SETUP_STATUS=INCONCLUSIVE\n'; exit 3; }

  {
    printf 'OPEN_WEBUI_SETUP_STATUS=PASS\n'
    printf 'COLLECTION=%s\n' "$COLLECTION_NAME"
    printf 'SOURCE_FILE=%s\n' "$SOURCE_NAME"
    printf 'ABSENCE_EVIDENCE=01-prior-collection-absent.png\n'
    printf 'MEMBERSHIP_EVIDENCE=02-new-collection-one-file.png\n'
    printf 'VOIDED_CHAT_CLEANUP_CONFIRMED=YES\n'
    printf 'VERIFIED_AT=%s\n' "$(date --iso-8601=seconds)"
  } > "$E/setup/setup-status.env"

  printf 'OPEN_WEBUI_SETUP_STATUS=PASS\n'
  printf 'NEXT_STEP=RUN_1_PREPARE_SCREENSHOTS\n'
  printf '\n'
  printf 'For Run 1 create only these three pre-prompt screenshots:\n'
  printf '%s\n' "$E/run-1/01-membership-before-run.png"
  printf '%s\n' "$E/run-1/02-fresh-empty-chat.png"
  printf '%s\n' "$E/run-1/03-collection-attached-before-prompt.png"
  printf 'Then run: bash "$HOME/Labs/AI-Development-Platform/scripts/adp231_gate_c_fresh_runtime.sh" run-start 1\n'
  exit 0
fi

test -f "$E/setup/setup-status.env"
grep -Fx 'OPEN_WEBUI_SETUP_STATUS=PASS' "$E/setup/setup-status.env" >/dev/null
D="$E/run-$RUN"

if [ "$COMMAND" = "run-start" ]; then
  printf '===== GATE C FRESH RUN START =====\n'
  printf 'RUN=%s\n' "$RUN"

  if [ "$RUN" -gt 1 ]; then
    PREV=$((RUN - 1))
    test -f "$E/run-$PREV/run-$PREV-status.env"
    grep -Fx 'OVERALL_RUN_STATUS=PASS' "$E/run-$PREV/run-$PREV-status.env" >/dev/null
  fi

  if [ -f "$D/run-$RUN-status.env" ]; then
    cat "$D/run-$RUN-status.env"
    exit 0
  fi
  if [ -f "$D/run-window-start.env" ]; then
    printf 'RUN_START_STATUS=ALREADY_STARTED\n'
    printf 'NEXT_STEP=COMPLETE_CURRENT_RUN_OR_VOID_AND_RESET\n'
    exit 0
  fi

  MEMBERSHIP="$D/01-membership-before-run.png"
  FRESH="$D/02-fresh-empty-chat.png"
  ATTACHED="$D/03-collection-attached-before-prompt.png"

  require_file "$MEMBERSHIP" "Per-run membership screenshot is required immediately before the counted run."
  require_file "$FRESH" "Fresh empty chat screenshot is required."
  require_file "$ATTACHED" "Attached-collection screenshot is required before prompt submission."

  yes_no "Does 01-membership-before-run.png show the exact collection with exactly one approved file?" || { printf 'RUN_START_STATUS=INCONCLUSIVE\n'; exit 3; }
  yes_no "Does 02-fresh-empty-chat.png show a new empty chat with llama3.2:3b and no tools enabled?" || { printf 'RUN_START_STATUS=INCONCLUSIVE\n'; exit 3; }
  yes_no "Does 03-collection-attached-before-prompt.png show the exact collection attached before any prompt was submitted?" || { printf 'RUN_START_STATUS=INCONCLUSIVE\n'; exit 3; }

  PROMPT_FILE="$E/setup/V231-R01-P1-v2.txt"
  test "$(sha256sum "$PROMPT_FILE" | awk '{print $1}')" = "$EXPECTED_PROMPT_SHA"
  cp "$PROMPT_FILE" "$D/V231-R01-P1-v2.txt"

  RUN_START="$(date --iso-8601=seconds)"
  RUN_START_EPOCH="$(date +%s)"
  {
    printf 'RUN=%s\n' "$RUN"
    printf 'RUN_START=%s\n' "$RUN_START"
    printf 'RUN_START_EPOCH=%s\n' "$RUN_START_EPOCH"
    printf 'PROMPT_SHA256=%s\n' "$EXPECTED_PROMPT_SHA"
  } > "$D/run-window-start.env"

  printf 'RUN_START_STATUS=PASS\n'
  printf 'SUBMIT_PROMPT_EXACTLY_ONCE=YES\n'
  printf '\n===== APPROVED FROZEN PROMPT =====\n'
  cat "$D/V231-R01-P1-v2.txt"
  printf '\n===== END APPROVED FROZEN PROMPT =====\n'
  printf '\n'
  printf 'After the response save only these three items:\n'
  printf '%s\n' "$D/response.txt"
  printf '%s\n' "$D/04-complete-response.png"
  printf '%s\n' "$D/05-displayed-source-panel.png"
  printf 'Then run: bash "$HOME/Labs/AI-Development-Platform/scripts/adp231_gate_c_fresh_runtime.sh" run-finish %s\n' "$RUN"
  exit 0
fi

if [ "$COMMAND" = "run-finish" ]; then
  printf '===== GATE C FRESH RUN FINISH =====\n'
  printf 'RUN=%s\n' "$RUN"

  test -f "$D/run-window-start.env"
  source "$D/run-window-start.env"

  RESPONSE_TEXT="$D/response.txt"
  RESPONSE_SCREENSHOT="$D/04-complete-response.png"
  SOURCE_SCREENSHOT="$D/05-displayed-source-panel.png"

  require_file "$RESPONSE_TEXT" "The complete uncorrected response text is required."
  require_file "$RESPONSE_SCREENSHOT" "A complete response screenshot is required."
  require_file "$SOURCE_SCREENSHOT" "A screenshot of the opened displayed-source panel is required."

  RUN_END="$(date --iso-8601=seconds)"
  RUN_END_EPOCH="$(date +%s)"
  {
    printf 'RUN=%s\n' "$RUN"
    printf 'RUN_END=%s\n' "$RUN_END"
    printf 'RUN_END_EPOCH=%s\n' "$RUN_END_EPOCH"
  } > "$D/run-window-end.env"
  test "$RUN_END_EPOCH" -ge "$RUN_START_EPOCH"

  if [ -n "${ADP_JOURNAL_FIXTURE:-}" ]; then
    cat "$ADP_JOURNAL_FIXTURE" > "$D/ollama-run-window-full.log"
  else
    journalctl -u ollama --since "$RUN_START" --until "$RUN_END" --no-pager > "$D/ollama-run-window-full.log"
  fi

  awk '/truncating input prompt/ {print}' "$D/ollama-run-window-full.log" > "$D/ollama-truncation-lines.log"
  TRUNCATION_COUNT="$(wc -l < "$D/ollama-truncation-lines.log" | tr -d ' ')"
  printf 'TRUNCATION_WARNING_COUNT=%s\n' "$TRUNCATION_COUNT" | tee "$D/ollama-truncation-count.txt"

  if [ "$TRUNCATION_COUNT" != "0" ]; then
    write_run_status "$D" "FAIL" "ENV-F01"
    printf 'TRUNCATION_RESULT=FAIL\n'
    printf 'OVERALL_RUN_STATUS=FAIL\n'
    exit 2
  fi
  printf 'TRUNCATION_RESULT=PASS\n'

  if ! grep -Fq "$TARGET_SENTENCE" "$RESPONSE_TEXT"; then
    write_run_status "$D" "FAIL" "R01-F01"
    printf 'TARGET_SENTENCE_STATUS=FAIL\n'
    exit 2
  fi
  printf 'TARGET_SENTENCE_STATUS=PASS\n'

  if yes_no "Does the response contain any unsupported or contradictory factual claim?"; then
    write_run_status "$D" "FAIL" "R01-F02"
    printf 'GROUNDING_STATUS=FAIL\n'
    exit 2
  fi
  printf 'GROUNDING_STATUS=PASS\n'

  if yes_no "Does the response contain automation, reminder, scheduling, or iCalendar output?"; then
    write_run_status "$D" "FAIL" "R01-F03"
    printf 'AUTOMATION_OUTPUT_STATUS=FAIL\n'
    exit 2
  fi
  printf 'AUTOMATION_OUTPUT_STATUS=PASS\n'

  yes_no "Does 05-displayed-source-panel.png visibly show the filename $SOURCE_NAME?" || { write_run_status "$D" "INCONCLUSIVE" "S01-I01"; printf 'DISPLAYED_SOURCE_FILENAME_STATUS=INCONCLUSIVE\n'; exit 3; }
  printf 'DISPLAYED_SOURCE_FILENAME_STATUS=PASS\n'

  yes_no "Does the same source-panel screenshot visibly show the complete target sentence?" || { write_run_status "$D" "INCONCLUSIVE" "S01-I01"; printf 'DISPLAYED_SOURCE_PASSAGE_STATUS=INCONCLUSIVE\n'; exit 3; }
  printf 'DISPLAYED_SOURCE_PASSAGE_STATUS=PASS\n'

  yes_no "Do the response and source-panel evidence agree, and were they preserved without correction?" || { write_run_status "$D" "INCONCLUSIVE" "ENV-I06"; printf 'EVIDENCE_INTEGRITY_STATUS=INCONCLUSIVE\n'; exit 3; }
  printf 'EVIDENCE_INTEGRITY_STATUS=PASS\n'

  write_run_status "$D" "PASS" "NONE"
  printf 'V231_R01_STATUS=PASS\n'
  printf 'V231_S01_STATUS=PASS\n'
  printf 'OVERALL_RUN_STATUS=PASS\n'

  if [ "$RUN" -lt 3 ]; then
    NEXT=$((RUN + 1))
    printf 'NEXT_STEP=RUN_%s_PREPARE_SCREENSHOTS\n' "$NEXT"
  else
    printf 'THREE_RUN_BLOCK_STATUS=PASS\n'
    printf 'NEXT_STEP=PACKAGE_EVIDENCE\n'
  fi
  exit 0
fi

if [ "$COMMAND" = "package" ]; then
  printf '===== GATE C FRESH EVIDENCE PACKAGE =====\n'
  PACKET_STATUS="PASS"
  STOP_RUN="NONE"

  for n in 1 2 3; do
    STATUS_FILE="$E/run-$n/run-$n-status.env"
    if [ ! -f "$STATUS_FILE" ]; then
      PACKET_STATUS="INCONCLUSIVE"
      STOP_RUN="$n"
      break
    fi
    STATUS="$(sed -n 's/^OVERALL_RUN_STATUS=//p' "$STATUS_FILE")"
    case "$STATUS" in
      PASS) ;;
      FAIL|INCONCLUSIVE)
        PACKET_STATUS="$STATUS"
        STOP_RUN="$n"
        break
        ;;
      *)
        PACKET_STATUS="INCONCLUSIVE"
        STOP_RUN="$n"
        break
        ;;
    esac
  done

  {
    printf 'PACKET_ID=V231-C-RUNTIME-01\n'
    printf 'PACKET_STATUS=%s\n' "$PACKET_STATUS"
    printf 'STOP_RUN=%s\n' "$STOP_RUN"
    printf 'PACKAGED_AT=%s\n' "$(date --iso-8601=seconds)"
  } > "$E/packet-status.env"

  PARENT="$(dirname "$E")"
  NAME="$(basename "$E")"
  ARCHIVE="$E.tar.gz"
  CHECKSUM="$ARCHIVE.sha256"

  tar -czf "$ARCHIVE" -C "$PARENT" "$NAME"
  tar -tzf "$ARCHIVE" >/dev/null
  sha256sum "$ARCHIVE" > "$CHECKSUM"

  printf 'PACKET_STATUS=%s\n' "$PACKET_STATUS"
  printf 'STOP_RUN=%s\n' "$STOP_RUN"
  printf 'EVIDENCE_ARCHIVE=%s\n' "$ARCHIVE"
  printf 'EVIDENCE_SHA256_FILE=%s\n' "$CHECKSUM"
  printf 'EVIDENCE_PACKAGE_STATUS=PASS\n'
  exit 0
fi
