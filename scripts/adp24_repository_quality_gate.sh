#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$HOME/Labs/AI-Development-Platform}"
BASELINE="${2:-c9de7d74e4b3dd31887567820052220d61954d6f}"
PRIMARY="docker/open-webui/docker-compose.yml"
PRIMARY_HASH_A="7933b0cbf02a635a083f662adaa6d77d0a64381039933047705d927fd3d83db6"
PRIMARY_HASH_B="dc2d3ef43ccde7ad77f7f70ae55928d234cabc5f921f5c52e74d349710f7ad2e"

required=(
  artifacts/Configuration/ADP-v2.4/approved-rag-template.txt
  artifacts/Configuration/ADP-v2.4/deterministic-model-discovery-record.json
  artifacts/Test-Data/ADP-v2.4/adp24_bounded_multi_fact_source.md
  artifacts/Test-Data/ADP-v2.4/lint-fixtures/contaminated-template.txt
  artifacts/Test-Data/ADP-v2.4/test-cases.json
  artifacts/Test-Data/ADP-v2.4/validator-fixtures/expected.txt
  artifacts/Test-Data/ADP-v2.4/validator-fixtures/factual-change.txt
  artifacts/Test-Data/ADP-v2.4/validator-fixtures/format-only.txt
  docker/open-webui-validation/docker-compose.yml
  docs/Operations/ADP-v2.4-Isolated-Validation-Configuration-Manifest.md
  docs/Operations/ADP-v2.4-Isolated-Validation-Instance-Repository-Procedure.md
  docs/Releases/ADP-v2.4-Isolated-Validation-Instance-Plan-Amendment.md
  docs/Releases/ADP-v2.4-Isolated-Validation-Instance-Repository-Implementation-Plan.md
  docs/Releases/ADP-v2.4-Isolated-Validation-Repository-Implementation-Artifact-Manifest.md
  docs/Releases/ADP-v2.4-Repository-Packet-v1-Delivery-Defect-and-Recovery-Record.md
  docs/Releases/ADP-v2.4-Repository-Packet-v2-Delivery-Defect-and-Recovery-Record.md
  scripts/adp24_lint_rag_template.py
  scripts/adp24_repository_quality_gate.sh
  scripts/adp24_validate_answer.py
  scripts/adp24_validate_compose_config.py
)

fail() {
  printf 'ADP24_REPOSITORY_QUALITY_GATE=FAIL\n'
  printf 'FAILED_CONTROL=%s\n' "$1"
  if [ "${2:-}" != "" ]; then
    printf 'FAILED_VALUE=%s\n' "$2"
  fi
  printf 'RUNTIME_AUTHORIZATION=HOLD\n'
  printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
  exit 1
}


cd "$REPO"
gate_tmp="$(mktemp -d)"
trap 'rm -rf "$gate_tmp" /tmp/adp24-negative-lint.log /tmp/adp24-validator-positive.log /tmp/adp24-validator-negative.log' EXIT
printf '===== ADP v2.4 REPOSITORY QUALITY GATE v3 =====\n'

test "$(git rev-parse HEAD)" = "$BASELINE" || fail GIT_BASELINE "$(git rev-parse HEAD)"
test "$(git rev-parse main)" = "$BASELINE" || fail MAIN_BASELINE "$(git rev-parse main)"
test "$(git rev-parse origin/main)" = "$BASELINE" || fail ORIGIN_BASELINE "$(git rev-parse origin/main)"
printf 'GIT_BASELINE_STATUS=PASS\n'

primary_hash="$(sha256sum "$PRIMARY" | awk '{print $1}')"
if [ "$primary_hash" != "$PRIMARY_HASH_A" ] && [ "$primary_hash" != "$PRIMARY_HASH_B" ]; then
  fail PRIMARY_COMPOSE_UNCHANGED "$primary_hash"
fi
printf 'PRIMARY_COMPOSE_UNCHANGED=PASS\n'

for path in "${required[@]}"; do
  test -s "$path" || fail REQUIRED_ARTIFACT "$path"
done
printf 'REQUIRED_ARTIFACT_STATUS=PASS\n'

validate_exact_write_set() {
  mapfile -t status_lines < <(git status --short --untracked-files=all | LC_ALL=C sort)
  actual=()
  for line in "${status_lines[@]}"; do
    status="${line:0:2}"
    path="${line:3}"
    test "$status" = "??" || fail EXACT_WRITE_SET_STATUS "$line"
    actual+=("$path")
  done
  mapfile -t expected < <(printf '%s\n' "${required[@]}" | LC_ALL=C sort)
  if [ "${#actual[@]}" -ne "${#expected[@]}" ]; then
    printf 'EXPECTED_PATHS=%s\n' "${#expected[@]}"
    printf 'ACTUAL_PATHS=%s\n' "${#actual[@]}"
    printf '%s\n' "${actual[@]}"
    fail EXACT_WRITE_SET_COUNT
  fi
  for index in "${!expected[@]}"; do
    test "${actual[$index]}" = "${expected[$index]}" || fail EXACT_WRITE_SET "${actual[$index]}"
  done
  printf 'EXPECTED_PATHS=%s\n' "${#expected[@]}"
  printf 'ACTUAL_PATHS=%s\n' "${#actual[@]}"
  printf 'EXACT_WRITE_SET_STATUS=PASS\n'
}

validate_exact_write_set

for path in "${required[@]}"; do
  if LC_ALL=C grep -n '[^ -~]' "$path"; then
    fail NON_ASCII_TEXT "$path"
  fi
  if grep -n $'\x09' "$path"; then
    fail TAB_CHARACTER "$path"
  fi
  if grep -nE '[[:blank:]]+$' "$path"; then
    fail TRAILING_WHITESPACE "$path"
  fi
done
printf 'TEXT_QUALITY_STATUS=PASS\n'

bash -n scripts/adp24_repository_quality_gate.sh || fail QUALITY_GATE_SYNTAX
PYTHONPYCACHEPREFIX="$gate_tmp/pycache" python3 -m py_compile scripts/adp24_lint_rag_template.py scripts/adp24_validate_answer.py scripts/adp24_validate_compose_config.py || fail PYTHON_COMPILE
printf 'SCRIPT_SYNTAX_STATUS=PASS\n'

python3 scripts/adp24_lint_rag_template.py artifacts/Configuration/ADP-v2.4/approved-rag-template.txt || fail APPROVED_TEMPLATE_LINT
if python3 scripts/adp24_lint_rag_template.py artifacts/Test-Data/ADP-v2.4/lint-fixtures/contaminated-template.txt >/tmp/adp24-negative-lint.log 2>&1; then
  fail CONTAMINATED_TEMPLATE_ACCEPTED
fi
grep -Fq 'RAG_TEMPLATE_LINT_STATUS=FAIL' /tmp/adp24-negative-lint.log || fail NEGATIVE_LINT_REPORT
printf 'LINTER_FIXTURE_STATUS=PASS\n'

validator_tmp="$gate_tmp/validator"
mkdir -p "$validator_tmp"
python3 scripts/adp24_validate_answer.py --expected artifacts/Test-Data/ADP-v2.4/validator-fixtures/expected.txt --raw artifacts/Test-Data/ADP-v2.4/validator-fixtures/format-only.txt --normalized-output "$validator_tmp/format-only.normalized.txt" >/tmp/adp24-validator-positive.log
if python3 scripts/adp24_validate_answer.py --expected artifacts/Test-Data/ADP-v2.4/validator-fixtures/expected.txt --raw artifacts/Test-Data/ADP-v2.4/validator-fixtures/factual-change.txt --normalized-output "$validator_tmp/factual-change.normalized.txt" >/tmp/adp24-validator-negative.log 2>&1; then
  fail FACTUAL_CHANGE_ACCEPTED
fi
grep -Fq 'ANSWER_VALIDATION_STATUS=PASS' /tmp/adp24-validator-positive.log || fail POSITIVE_VALIDATOR_REPORT
grep -Fq 'FAILED_CONTROL=FACTUAL_CONTENT_MISMATCH' /tmp/adp24-validator-negative.log || fail NEGATIVE_VALIDATOR_REPORT
printf 'VALIDATOR_FIXTURE_STATUS=PASS\n'

python3 -m json.tool artifacts/Configuration/ADP-v2.4/deterministic-model-discovery-record.json >/dev/null || fail MODEL_JSON
python3 -m json.tool artifacts/Test-Data/ADP-v2.4/test-cases.json >/dev/null || fail TEST_CASE_JSON
printf 'JSON_VALIDATION_STATUS=PASS\n'

template_hash="$(sha256sum artifacts/Configuration/ADP-v2.4/approved-rag-template.txt | awk '{print $1}')"
test "$template_hash" = 'def3db3e05b1651aa33b921a03573074d8033ca5d2ce691446638e362ef92d96' || fail TEMPLATE_HASH "$template_hash"
printf 'TEMPLATE_HASH_STATUS=PASS\n'

compose_file="docker/open-webui-validation/docker-compose.yml"
command -v docker >/dev/null 2>&1 || fail DOCKER_COMMAND_MISSING
docker compose -f "$compose_file" config --quiet || fail COMPOSE_CONFIG
compose_json="$gate_tmp/compose-config.json"
docker compose -f "$compose_file" config --format json > "$compose_json" || fail COMPOSE_JSON_RENDER
python3 scripts/adp24_validate_compose_config.py --compose-json "$compose_json" --approved-template artifacts/Configuration/ADP-v2.4/approved-rag-template.txt || fail COMPOSE_SEMANTIC_VALIDATION
printf 'COMPOSE_VALIDATION_MODE=DOCKER_JSON\n'
for prohibited in RAG_EMBEDDING_ENGINE CONTENT_EXTRACTION_ENGINE CHUNK_MIN_SIZE_TARGET RAG_TOP_K_RERANKER RAG_RERANKING_ENGINE RAG_RERANKING_MODEL RAG_HYBRID_BM25_WEIGHT; do
  if grep -Eq "^[[:space:]]+$prohibited:" "$compose_file"; then
    fail UNNECESSARY_CONFIG_OVERRIDE "$prohibited"
  fi
done
printf 'COMPOSE_STATIC_STATUS=PASS\n'

grep -Fq 'PRIMARY_INSTANCE_CHANGE=PROHIBITED' docs/Releases/ADP-v2.4-Isolated-Validation-Instance-Plan-Amendment.md || fail PRIMARY_PROTECTION_TRACEABILITY
grep -Fq 'RUNTIME_AUTHORIZATION=HOLD' docs/Operations/ADP-v2.4-Isolated-Validation-Instance-Repository-Procedure.md || fail RUNTIME_HOLD_TRACEABILITY
grep -Fq 'MODEL_SYNC_OPERATION=PROHIBITED' docs/Operations/ADP-v2.4-Isolated-Validation-Configuration-Manifest.md || fail MODEL_SYNC_PROHIBITION
grep -Fq 'PROVISIONAL_NOT_AUTHORIZED_FOR_COUNTED_USE' artifacts/Test-Data/ADP-v2.4/test-cases.json || fail PROVISIONAL_TEST_BOUNDARY
grep -Fq 'VOIDED_NOT_COUNTED' docs/Releases/ADP-v2.4-Isolated-Validation-Instance-Repository-Implementation-Plan.md || fail VOID_CONTROL
grep -Fq 'FAILED_CONTROL=EXACT_WRITE_SET_COUNT' docs/Releases/ADP-v2.4-Repository-Packet-v1-Delivery-Defect-and-Recovery-Record.md || fail V1_DEFECT_TRACEABILITY
grep -Fq 'FAILED_CONTROL=VALIDATION_BINDING' docs/Releases/ADP-v2.4-Repository-Packet-v2-Delivery-Defect-and-Recovery-Record.md || fail V2_DEFECT_TRACEABILITY
grep -Fq 'V1_PACKET=SUPERSEDED_DO_NOT_REUSE' docs/Releases/ADP-v2.4-Isolated-Validation-Repository-Implementation-Artifact-Manifest.md || fail V1_SUPERSESSION_TRACEABILITY
grep -Fq 'V2_PACKET=SUPERSEDED_DO_NOT_REUSE' docs/Releases/ADP-v2.4-Isolated-Validation-Repository-Implementation-Artifact-Manifest.md || fail V2_SUPERSESSION_TRACEABILITY
grep -Fq 'PACKET_VERSION=v3' docs/Releases/ADP-v2.4-Isolated-Validation-Repository-Implementation-Artifact-Manifest.md || fail CURRENT_PACKET_TRACEABILITY
printf 'SEMANTIC_TRACEABILITY_STATUS=PASS\n'

validate_exact_write_set
printf 'FINAL_EXACT_WRITE_SET_STATUS=PASS\n'

test -z "$(git diff --name-only)" || fail TRACKED_FILE_CHANGED "$(git diff --name-only)"
git diff --check || fail TRACKED_DIFF_CHECK
printf 'TRACKED_DIFF_CHECK_STATUS=PASS\n'
printf 'ADP24_REPOSITORY_QUALITY_GATE=PASS\n'
printf 'REPOSITORY_ONLY_IMPLEMENTATION=PASS\n'
printf 'PRIMARY_INSTANCE_CHANGE=NONE\n'
printf 'RUNTIME_CHANGE=NONE\n'
printf 'RUNTIME_AUTHORIZATION=HOLD\n'
printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
