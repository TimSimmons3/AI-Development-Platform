#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$HOME/Labs/AI-Development-Platform}"
BASELINE="079f30d909114aca450207c37c84ac471b9db828"
EXPECTED=(
  artifacts/Configuration/ADP-v2.4/runtime-evidence-filename-map.json
  artifacts/Test-Data/ADP-v2.4/model-export-fixtures/invalid-associated-model.json
  artifacts/Test-Data/ADP-v2.4/model-export-fixtures/invalid-multi-model.json
  artifacts/Test-Data/ADP-v2.4/model-export-fixtures/invalid-secret-model.json
  artifacts/Test-Data/ADP-v2.4/model-export-fixtures/valid-single-model.json
  docs/Operations/ADP-v2.4-Isolated-Validation-Model-Export-Import-Procedure.md
  docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Evidence-Schema.md
  docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md
  docs/Operations/ADP-v2.4-Isolated-Validation-Volume-Backup-Rollback-Procedure.md
  docs/Releases/ADP-v2.4-Isolated-Validation-Pre-Runtime-Execution-Plan.md
  docs/Releases/ADP-v2.4-Isolated-Validation-Pre-Runtime-Procedure-Freeze-Checklist.md
  docs/Releases/ADP-v2.4-Read-Only-Gate-Invocation-Defect-Record.md
  scripts/adp24_capture_runtime_manifest.py
  scripts/adp24_isolated_runtime_apply.sh
  scripts/adp24_isolated_runtime_preflight.sh
  scripts/adp24_isolated_runtime_verify.sh
  scripts/adp24_pre_runtime_quality_gate.sh
  scripts/adp24_validate_model_export.py
  scripts/adp24_validation_volume_backup.sh
  scripts/adp24_validation_volume_restore.sh
)

fail() {
  printf 'ADP24_PRE_RUNTIME_QUALITY_GATE=FAIL\n'
  printf 'FAILED_CONTROL=%s\n' "$1"
  if [ "${2:-}" != "" ]; then
    printf 'FAILED_VALUE=%s\n' "$2"
  fi
  printf 'RUNTIME_AUTHORIZATION=HOLD\n'
  printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
  exit 1
}

printf '===== ADP v2.4 PRE-RUNTIME REPOSITORY QUALITY GATE =====\n'
test -d "$REPO/.git" || fail REPOSITORY "$REPO"
test "$(git -C "$REPO" rev-parse HEAD)" = "$BASELINE" || fail GIT_BASELINE "$(git -C "$REPO" rev-parse HEAD)"
test -z "$(git -C "$REPO" diff --name-only)" || fail TRACKED_FILES_CHANGED

mapfile -t actual < <(git -C "$REPO" status --short --untracked-files=all | awk '{print $2}' | LC_ALL=C sort)
mapfile -t expected < <(printf '%s\n' "${EXPECTED[@]}" | LC_ALL=C sort)
printf 'EXPECTED_PATHS=%s\n' "${#expected[@]}"
printf 'ACTUAL_PATHS=%s\n' "${#actual[@]}"
test "${#actual[@]}" -eq "${#expected[@]}" || fail EXACT_WRITE_SET_COUNT "${#actual[@]}"
for index in "${!expected[@]}"; do
  test "${actual[$index]}" = "${expected[$index]}" || fail EXACT_WRITE_SET "${actual[$index]}"
done
while read -r status path; do
  test "$status" = "??" || fail PATH_STATUS "$status:$path"
done < <(git -C "$REPO" status --short --untracked-files=all)
printf 'EXACT_WRITE_SET_STATUS=PASS\n'

for path in "${EXPECTED[@]}"; do
  test -s "$REPO/$path" || fail REQUIRED_ARTIFACT "$path"
  if LC_ALL=C grep -n '[^ -~]' "$REPO/$path"; then fail NON_ASCII "$path"; fi
  if grep -n $'\x09' "$REPO/$path"; then fail TAB_CHARACTER "$path"; fi
  if grep -nE '[[:blank:]]+$' "$REPO/$path"; then fail TRAILING_WHITESPACE "$path"; fi
done
printf 'TEXT_QUALITY_STATUS=PASS\n'

for script in \
  scripts/adp24_isolated_runtime_apply.sh \
  scripts/adp24_isolated_runtime_preflight.sh \
  scripts/adp24_isolated_runtime_verify.sh \
  scripts/adp24_pre_runtime_quality_gate.sh \
  scripts/adp24_validation_volume_backup.sh \
  scripts/adp24_validation_volume_restore.sh
do
  bash -n "$REPO/$script" || fail SHELL_SYNTAX "$script"
done
PYTHONPYCACHEPREFIX="$(mktemp -d)" python3 -m py_compile "$REPO/scripts/adp24_validate_model_export.py" "$REPO/scripts/adp24_capture_runtime_manifest.py" || fail PYTHON_COMPILE
printf 'SCRIPT_SYNTAX_STATUS=PASS\n'

python3 -m json.tool "$REPO/artifacts/Configuration/ADP-v2.4/runtime-evidence-filename-map.json" >/dev/null || fail FILENAME_MAP_JSON
for fixture in "$REPO"/artifacts/Test-Data/ADP-v2.4/model-export-fixtures/*.json; do
  python3 -m json.tool "$fixture" >/dev/null || fail FIXTURE_JSON "$fixture"
done

TEMP="$(mktemp -d)"
python3 "$REPO/scripts/adp24_validate_model_export.py" \
  --input "$REPO/artifacts/Test-Data/ADP-v2.4/model-export-fixtures/valid-single-model.json" \
  --sanitized-output "$TEMP/import.json" \
  --report-output "$TEMP/report.json" >/dev/null || fail MODEL_FIXTURE_POSITIVE
for fixture in invalid-multi-model.json invalid-secret-model.json invalid-associated-model.json; do
  if python3 "$REPO/scripts/adp24_validate_model_export.py" \
    --input "$REPO/artifacts/Test-Data/ADP-v2.4/model-export-fixtures/$fixture" \
    --sanitized-output "$TEMP/$fixture.import" \
    --report-output "$TEMP/$fixture.report" >/dev/null 2>&1; then
    fail MODEL_FIXTURE_NEGATIVE "$fixture"
  fi
done
rm -rf "$TEMP"
printf 'MODEL_EXPORT_VALIDATOR_STATUS=PASS\n'

mapfile -t names < <(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); [print(x["name"]) for x in d["files"]]' "$REPO/artifacts/Configuration/ADP-v2.4/runtime-evidence-filename-map.json")
test "${#names[@]}" -eq 20 || fail EVIDENCE_FILENAME_COUNT "${#names[@]}"
test "$(printf '%s\n' "${names[@]}" | sort -u | wc -l)" -eq 20 || fail EVIDENCE_FILENAME_DUPLICATE
printf 'EVIDENCE_FILENAME_MAP_STATUS=PASS\n'

prohibited_paths=(
  "$REPO/docs/Operations/ADP-v2.4-Isolated-Validation-Model-Export-Import-Procedure.md"
  "$REPO/docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md"
  "$REPO/docs/Operations/ADP-v2.4-Isolated-Validation-Volume-Backup-Rollback-Procedure.md"
  "$REPO/docs/Releases/ADP-v2.4-Isolated-Validation-Pre-Runtime-Execution-Plan.md"
  "$REPO/scripts/adp24_isolated_runtime_apply.sh"
  "$REPO/scripts/adp24_isolated_runtime_preflight.sh"
  "$REPO/scripts/adp24_isolated_runtime_verify.sh"
  "$REPO/scripts/adp24_validation_volume_backup.sh"
  "$REPO/scripts/adp24_validation_volume_restore.sh"
)
if grep -nE '(/api/v1/models/sync|docker compose down -v|docker volume rm open-webui|--network=host|0\.0\.0\.0:3001)' "${prohibited_paths[@]}"; then
  fail PROHIBITED_OPERATION
fi

grep -Fq 'MODEL_SYNC_OPERATION=PROHIBITED' "$REPO/docs/Operations/ADP-v2.4-Isolated-Validation-Model-Export-Import-Procedure.md" || fail MODEL_SYNC_CONTROL
grep -Fq 'PRIMARY_INSTANCE_CHANGE=NONE' "$REPO/docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md" || fail PRIMARY_BOUNDARY
grep -Fq 'VOIDED_NOT_COUNTED' "$REPO/docs/Releases/ADP-v2.4-Isolated-Validation-Pre-Runtime-Execution-Plan.md" || fail VOID_CONTROL
grep -Fq 'restricted evidence' "$REPO/docs/Operations/ADP-v2.4-Isolated-Validation-Model-Export-Import-Procedure.md" || fail RAW_EXPORT_CONTROL
printf 'SEMANTIC_TRACEABILITY_STATUS=PASS\n'

test -z "$(find "$REPO/scripts" -type d -name __pycache__ -print -quit)" || fail PYCACHE_SIDE_EFFECT
git -C "$REPO" diff --check || fail GIT_DIFF_CHECK
printf 'TRACKED_DIFF_CHECK_STATUS=PASS\n'
printf 'ADP24_PRE_RUNTIME_QUALITY_GATE=PASS\n'
printf 'REPOSITORY_ONLY_IMPLEMENTATION=PASS\n'
printf 'PRIMARY_INSTANCE_CHANGE=NONE\n'
printf 'RUNTIME_MUTATION=NONE\n'
printf 'RUNTIME_AUTHORIZATION=HOLD\n'
printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
