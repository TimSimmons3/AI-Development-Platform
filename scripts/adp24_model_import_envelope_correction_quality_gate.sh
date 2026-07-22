#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$HOME/Labs/AI-Development-Platform}"
BASELINE="${2:-dccb467631c415f287ace128adc0e710b2dc2515}"
SKIP_RUNTIME="${ADP24_SKIP_RUNTIME_CHECKS:-0}"

MODIFIED=(
  .gitignore
  docs/Operations/ADP-v2.4-Isolated-Validation-Model-Export-Import-Procedure.md
  docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Evidence-Schema.md
  docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md
  scripts/adp24_validate_model_export.py
)

ADDED=(
  artifacts/Configuration/ADP-v2.4/model-import-reset-evidence-filename-map.json
  artifacts/Test-Data/ADP-v2.4/model-export-fixtures/invalid-wrapped-import.json
  docs/Releases/ADP-v2.4-Model-Import-Envelope-Defect-and-Controlled-Reset-Amendment.md
  scripts/adp24_model_import_envelope_correction_quality_gate.sh
  scripts/adp24_validate_model_import_payload.py
)

EXPECTED=("${MODIFIED[@]}" "${ADDED[@]}")

fail() {
  printf 'ADP24_MODEL_IMPORT_ENVELOPE_CORRECTION_QUALITY_GATE=FAIL\n'
  printf 'FAILED_CONTROL=%s\n' "$1"
  if [ "${2:-}" != "" ]; then
    printf 'FAILED_VALUE=%s\n' "$2"
  fi
  printf 'REPOSITORY_CORRECTION_PROMOTION=HOLD\n'
  printf 'MODEL_IMPORT_AUTHORIZATION=HOLD\n'
  printf 'RUNTIME_AUTHORIZATION=HOLD\n'
  printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
  exit 1
}

printf '===== ADP v2.4 MODEL IMPORT ENVELOPE CORRECTION QUALITY GATE =====\n'

test -d "$REPO/.git" || fail REPOSITORY "$REPO"
test "$(git -C "$REPO" rev-parse HEAD)" = "$BASELINE" || fail GIT_BASELINE "$(git -C "$REPO" rev-parse HEAD)"
git -C "$REPO" diff --cached --quiet || fail STAGED_CHANGES_PRESENT

mapfile -t actual_paths < <(
  git -C "$REPO" status --short --untracked-files=all |
    cut -c4- |
    LC_ALL=C sort
)
mapfile -t expected_paths < <(printf '%s\n' "${EXPECTED[@]}" | LC_ALL=C sort)

printf 'EXPECTED_PATHS=%s\n' "${#expected_paths[@]}"
printf 'ACTUAL_PATHS=%s\n' "${#actual_paths[@]}"

test "${#actual_paths[@]}" -eq "${#expected_paths[@]}" ||
  fail EXACT_WRITE_SET_COUNT "${#actual_paths[@]}"

for index in "${!expected_paths[@]}"; do
  test "${actual_paths[$index]}" = "${expected_paths[$index]}" ||
    fail EXACT_WRITE_SET "${actual_paths[$index]}"
done

mapfile -t modified_actual < <(git -C "$REPO" diff --name-only | LC_ALL=C sort)
mapfile -t modified_expected < <(printf '%s\n' "${MODIFIED[@]}" | LC_ALL=C sort)

test "${#modified_actual[@]}" -eq "${#modified_expected[@]}" ||
  fail MODIFIED_WRITE_SET_COUNT "${#modified_actual[@]}"

for index in "${!modified_expected[@]}"; do
  test "${modified_actual[$index]}" = "${modified_expected[$index]}" ||
    fail MODIFIED_WRITE_SET "${modified_actual[$index]}"
done

for path in "${ADDED[@]}"; do
  git -C "$REPO" status --short --untracked-files=all -- "$path" |
    grep -Fxq "?? $path" ||
    fail ADDED_PATH_STATUS "$path"
done

printf 'EXACT_WRITE_SET_STATUS=PASS\n'

for path in "${EXPECTED[@]}"; do
  test -s "$REPO/$path" || fail REQUIRED_ARTIFACT "$path"
  if LC_ALL=C grep -n '[^ -~]' "$REPO/$path"; then
    fail NON_ASCII "$path"
  fi
  if grep -n $'\x09' "$REPO/$path"; then
    fail TAB_CHARACTER "$path"
  fi
  if grep -nE '[[:blank:]]+$' "$REPO/$path"; then
    fail TRAILING_WHITESPACE "$path"
  fi
done

printf 'TEXT_QUALITY_STATUS=PASS\n'

bash -n "$REPO/scripts/adp24_model_import_envelope_correction_quality_gate.sh" ||
  fail SHELL_SYNTAX

PYCACHE="$(mktemp -d)"
PYTHONPYCACHEPREFIX="$PYCACHE" python3 -m py_compile \
  "$REPO/scripts/adp24_validate_model_export.py" \
  "$REPO/scripts/adp24_validate_model_import_payload.py" ||
  fail PYTHON_COMPILE
rm -rf "$PYCACHE"

printf 'SCRIPT_SYNTAX_STATUS=PASS\n'

python3 -m json.tool \
  "$REPO/artifacts/Configuration/ADP-v2.4/model-import-reset-evidence-filename-map.json" \
  >/dev/null ||
  fail RESET_FILENAME_MAP_JSON

python3 -m json.tool \
  "$REPO/artifacts/Test-Data/ADP-v2.4/model-export-fixtures/invalid-wrapped-import.json" \
  >/dev/null ||
  fail WRAPPED_FIXTURE_JSON

TEMP="$(mktemp -d)"
trap 'rm -rf "$TEMP"' EXIT

python3 "$REPO/scripts/adp24_validate_model_export.py" \
  --input "$REPO/artifacts/Test-Data/ADP-v2.4/model-export-fixtures/valid-single-model.json" \
  --sanitized-output "$TEMP/import.json" \
  --report-output "$TEMP/report.json" \
  > "$TEMP/export-validator.txt" ||
  fail MODEL_EXPORT_VALIDATOR_POSITIVE

grep -Fxq 'SANITIZED_IMPORT_ROOT=TOP_LEVEL_ARRAY' "$TEMP/export-validator.txt" ||
  fail EXPORT_ROOT_OUTPUT
grep -Fxq 'SANITIZED_IMPORT_MODEL_COUNT=1' "$TEMP/export-validator.txt" ||
  fail EXPORT_MODEL_COUNT_OUTPUT

python3 -c '
import json
import sys

payload = json.load(open(sys.argv[1], encoding="utf-8"))
report = json.load(open(sys.argv[2], encoding="utf-8"))

assert isinstance(payload, list)
assert len(payload) == 1
assert payload[0]["id"] == "llama-32-3b-rag-deterministic-test"
assert report["sanitized_import_root"] == "TOP_LEVEL_ARRAY"
assert report["sanitized_import_model_count"] == 1
assert report["open_webui_import_compatibility"] == "V0.10.2_WORKSPACE_MODELS"
' "$TEMP/import.json" "$TEMP/report.json" ||
  fail SANITIZED_IMPORT_SEMANTICS

python3 "$REPO/scripts/adp24_validate_model_import_payload.py" \
  --input "$TEMP/import.json" \
  > "$TEMP/import-validator.txt" ||
  fail IMPORT_PAYLOAD_VALIDATOR_POSITIVE

grep -Fxq 'MODEL_IMPORT_PAYLOAD_VALIDATION=PASS' "$TEMP/import-validator.txt" ||
  fail IMPORT_PAYLOAD_PASS_OUTPUT
grep -Fxq 'IMPORT_ROOT=TOP_LEVEL_ARRAY' "$TEMP/import-validator.txt" ||
  fail IMPORT_PAYLOAD_ROOT_OUTPUT

if python3 "$REPO/scripts/adp24_validate_model_import_payload.py" \
  --input "$REPO/artifacts/Test-Data/ADP-v2.4/model-export-fixtures/invalid-wrapped-import.json" \
  > "$TEMP/wrapped-output.txt" 2>&1; then
  fail WRAPPED_IMPORT_NEGATIVE_ACCEPTED
fi

grep -Fxq 'FAILED_CONTROL=IMPORT_ROOT_FORMAT' "$TEMP/wrapped-output.txt" ||
  fail WRAPPED_IMPORT_NEGATIVE_CONTROL

printf 'MODEL_IMPORT_FORMAT_TEST_STATUS=PASS\n'

mapfile -t reset_names < <(
  python3 -c '
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
for item in data["files"]:
    print(item["name"])
' "$REPO/artifacts/Configuration/ADP-v2.4/model-import-reset-evidence-filename-map.json"
)

test "${#reset_names[@]}" -eq 17 ||
  fail RESET_EVIDENCE_FILENAME_COUNT "${#reset_names[@]}"

test "$(printf '%s\n' "${reset_names[@]}" | LC_ALL=C sort -u | wc -l)" -eq 17 ||
  fail RESET_EVIDENCE_FILENAME_DUPLICATE

printf 'RESET_EVIDENCE_FILENAME_MAP_STATUS=PASS\n'

git -C "$REPO" check-ignore -q -- \
  artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/TEST/file.txt ||
  fail PRE_RUNTIME_EVIDENCE_IGNORE

git -C "$REPO" check-ignore -q -- \
  artifacts/Evidence/ADP-v2.4-Isolated-Validation-Model-Import-Reset/TEST/file.txt ||
  fail RESET_EVIDENCE_IGNORE

if git -C "$REPO" check-ignore -q -- \
  artifacts/Evidence/UNRELATED/file.txt; then
  fail UNRELATED_EVIDENCE_IGNORE_SCOPE
fi

printf 'EVIDENCE_IGNORE_SCOPE_STATUS=PASS\n'

grep -Fq 'OPEN_WEBUI_IMPORT_ROOT=TOP_LEVEL_ARRAY' \
  "$REPO/docs/Operations/ADP-v2.4-Isolated-Validation-Model-Export-Import-Procedure.md" ||
  fail PROCEDURE_IMPORT_ROOT

grep -Fq 'there is no separate confirmation button' \
  "$REPO/docs/Operations/ADP-v2.4-Isolated-Validation-Model-Export-Import-Procedure.md" ||
  fail PROCEDURE_IMMEDIATE_IMPORT

grep -Fq 'TARGET_MODEL_COUNT_AFTER_ATTEMPT=0' \
  "$REPO/docs/Releases/ADP-v2.4-Model-Import-Envelope-Defect-and-Controlled-Reset-Amendment.md" ||
  fail DEFECT_MODEL_COUNT

grep -Fq 'This is a reset at the model-import boundary.' \
  "$REPO/docs/Releases/ADP-v2.4-Model-Import-Envelope-Defect-and-Controlled-Reset-Amendment.md" ||
  fail CONTROLLED_RESET_BOUNDARY

grep -Fq 'No other prior setup, screenshot, validator output, import payload, manifest, backup, restart, or dry-run evidence may be reused' \
  "$REPO/docs/Releases/ADP-v2.4-Model-Import-Envelope-Defect-and-Controlled-Reset-Amendment.md" ||
  fail EVIDENCE_REUSE_BOUNDARY

grep -Fq 'MODEL_IMPORT_CORRECTION_TAG=adp-v2.4-model-import-envelope-correction' \
  "$REPO/docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md" ||
  fail CORRECTION_TAG_REFERENCE

printf 'SEMANTIC_TRACEABILITY_STATUS=PASS\n'

if [ "$SKIP_RUNTIME" != "1" ]; then
  curl -fsS http://127.0.0.1:3000/health |
    grep -Fq '"status":true' ||
    fail PRIMARY_HEALTH

  state="$(
    docker inspect open-webui-validation \
      --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' \
      2>/dev/null || true
  )"
  test "$state" = "healthy" ||
    fail VALIDATION_HEALTH "$state"

  docker volume inspect open-webui-validation >/dev/null ||
    fail VALIDATION_VOLUME

  docker exec open-webui-validation python -c '
import sqlite3

db = sqlite3.connect(
    "file:/app/backend/data/webui.db?mode=ro",
    uri=True,
)
users = db.execute("SELECT COUNT(*) FROM user").fetchone()[0]
admins = db.execute(
    "SELECT COUNT(*) FROM user WHERE role=?",
    ("admin",),
).fetchone()[0]
target = db.execute(
    "SELECT COUNT(*) FROM model WHERE id=?",
    ("llama-32-3b-rag-deterministic-test",),
).fetchone()[0]
print("USER_COUNT=" + str(users))
print("ADMIN_COUNT=" + str(admins))
print("TARGET_MODEL_COUNT=" + str(target))
assert users == 1
assert admins == 1
assert target == 0
db.close()
' ||
    fail RETAINED_RUNTIME_STATE

  old_raw="$REPO/artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/20260722T215656Z/01-primary-deterministic-model-export-raw.json"
  old_sanitized="$REPO/artifacts/Evidence/ADP-v2.4-Isolated-Validation-Pre-Runtime/20260722T215656Z/03-deterministic-model-import-sanitized.json"

  test -s "$old_raw" ||
    fail PRIOR_RAW_EXPORT_MISSING
  test -s "$old_sanitized" ||
    fail PRIOR_SANITIZED_IMPORT_MISSING

  test "$(sha256sum "$old_raw" | awk '{print $1}')" = \
    "dc5f11638c994e7204b7a8e2b0920bd7f8ccf324253260ac65dd7efcf99269fa" ||
    fail PRIOR_RAW_EXPORT_HASH

  test "$(sha256sum "$old_sanitized" | awk '{print $1}')" = \
    "cfedcc29fc4e7fa43dbffae3c2302e1a542a78a2dff49026e679a416a7b0d83f" ||
    fail PRIOR_SANITIZED_IMPORT_HASH

  printf 'RETAINED_RUNTIME_STATE_STATUS=PASS\n'
fi

test -z "$(find "$REPO/scripts" -type d -name __pycache__ -print -quit)" ||
  fail PYCACHE_SIDE_EFFECT

git -C "$REPO" diff --check ||
  fail GIT_DIFF_CHECK

printf 'TRACKED_DIFF_CHECK_STATUS=PASS\n'
printf 'ADP24_MODEL_IMPORT_ENVELOPE_CORRECTION_QUALITY_GATE=PASS\n'
printf 'EXPECTED_PATHS=10\n'
printf 'ACTUAL_PATHS=10\n'
printf 'SANITIZED_IMPORT_ROOT=TOP_LEVEL_ARRAY\n'
printf 'WRAPPED_IMPORT_REJECTION=PASS\n'
printf 'REPOSITORY_CORRECTION_INSTALL=PASS\n'
printf 'PRIMARY_INSTANCE_CHANGE=NONE\n'
printf 'VALIDATION_RUNTIME_MUTATION=NONE\n'
printf 'MODEL_IMPORT_AUTHORIZATION=HOLD_PENDING_PROMOTION_AND_RESET_GATE\n'
printf 'RUNTIME_AUTHORIZATION=HOLD\n'
printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
