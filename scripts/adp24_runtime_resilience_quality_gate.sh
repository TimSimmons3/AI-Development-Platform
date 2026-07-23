#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$HOME/Labs/AI-Development-Platform}"
BASELINE="${2:-}"
TEMP="$(mktemp -d)"
trap 'rm -rf "$TEMP"' EXIT

EXPECTED_PATHS=(
  "docs/Operations/ADP-v2.4-Isolated-Validation-Restart-Persistence-Procedure.md"
  "docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md"
  "docs/Releases/ADP-v2.4-Runtime-Resilience-and-Evidence-Control-Amendment.md"
  "scripts/adp24_capture_restart_state.py"
  "scripts/adp24_isolated_runtime_apply.sh"
  "scripts/adp24_runtime_resilience_quality_gate.sh"
  "scripts/adp24_validation_restart_persistence.sh"
  "scripts/adp24_validation_volume_backup.sh"
)

fail() {
  printf 'ADP24_RUNTIME_RESILIENCE_QUALITY_GATE=FAIL\n'
  printf 'FAILED_CONTROL=%s\n' "$1"
  if [ "${2:-}" != "" ]; then
    printf 'FAILED_VALUE=%s\n' "$2"
  fi
  printf 'RUNTIME_AUTHORIZATION=HOLD\n'
  printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
  exit 1
}

test "$BASELINE" != "" || fail BASELINE_ARGUMENT_REQUIRED

cd "$REPO"
test "$(git rev-parse HEAD)" = "$BASELINE" || fail GIT_BASELINE "$(git rev-parse HEAD)"

printf '%s\n' "${EXPECTED_PATHS[@]}" | LC_ALL=C sort > "$TEMP/expected.txt"
git status --short --untracked-files=all | awk '{print $2}' | LC_ALL=C sort > "$TEMP/actual.txt"
expected_count="$(wc -l < "$TEMP/expected.txt")"
actual_count="$(wc -l < "$TEMP/actual.txt")"
printf 'EXPECTED_PATHS=%s\n' "$expected_count"
printf 'ACTUAL_PATHS=%s\n' "$actual_count"
diff -u "$TEMP/expected.txt" "$TEMP/actual.txt" >/dev/null || fail EXACT_WRITE_SET
printf 'EXACT_WRITE_SET_STATUS=PASS\n'

python3 - "$REPO" "${EXPECTED_PATHS[@]}" <<'PY'
from pathlib import Path
import sys
root = Path(sys.argv[1])
for rel in sys.argv[2:]:
    path = root / rel
    data = path.read_bytes()
    assert data
    assert b"\r" not in data
    assert data.endswith(b"\n")
    assert not data.endswith(b"\n\n"), f"{rel}: blank line at EOF"
    text = data.decode("ascii")
    lines = text.splitlines()
    if rel.endswith(".py"):
        assert lines[0] == "#!/usr/bin/env python3", rel
    elif rel.endswith(".sh"):
        assert lines[0] == "#!/usr/bin/env bash", rel
    else:
        assert lines[0].startswith("# "), rel
    for number, line in enumerate(lines, 1):
        assert line == line.rstrip(), f"{rel}:{number}"
print("TEXT_QUALITY_STATUS=PASS")
print("FIRST_LINE_VALIDATION_STATUS=PASS")
PY

bash -n scripts/adp24_isolated_runtime_apply.sh
bash -n scripts/adp24_validation_volume_backup.sh
bash -n scripts/adp24_validation_restart_persistence.sh
bash -n scripts/adp24_runtime_resilience_quality_gate.sh
printf 'SCRIPT_SYNTAX_STATUS=PASS\n'

PYTHONPYCACHEPREFIX="$TEMP/pycache" python3 -m py_compile scripts/adp24_capture_restart_state.py
printf 'PYTHON_SYNTAX_STATUS=PASS\n'

grep -Fq 'MAX_ATTEMPTS="${ADP24_HEALTH_ATTEMPTS:-300}"' scripts/adp24_isolated_runtime_apply.sh || fail APPLY_WAIT_LIMIT
grep -Fq 'if [ "$state" = "exited" ] || [ "$state" = "dead" ]' scripts/adp24_isolated_runtime_apply.sh || fail APPLY_TERMINAL_STATE
if grep -Fq 'if [ "$state" = "unhealthy" ] ||' scripts/adp24_isolated_runtime_apply.sh; then
  fail APPLY_PREMATURE_UNHEALTHY_FAILURE
fi
printf 'HEALTH_WAIT_HARDENING_STATUS=PASS\n'

grep -Fq 'umask 077' scripts/adp24_validation_volume_backup.sh || fail BACKUP_UMASK
grep -Fq "chown '\$HOST_UID:\$HOST_GID'" scripts/adp24_validation_volume_backup.sh || fail BACKUP_CHOWN
grep -Fq "chmod 600 '/backup/\$name'" scripts/adp24_validation_volume_backup.sh || fail BACKUP_CHMOD
grep -Fq 'trap cleanup EXIT' scripts/adp24_validation_volume_backup.sh || fail BACKUP_CLEANUP_TRAP
printf 'BACKUP_PROTECTION_STATUS=PASS\n'

cat > "$TEMP/compose.json" <<'JSON'
{"services":{"open-webui-validation":{"environment":{"OLLAMA_BASE_URL":"http://host.docker.internal:11434","OLLAMA_BASE_URLS":"http://host.docker.internal:11434","ENABLE_PERSISTENT_CONFIG":"False","RAG_TEMPLATE":"template","RAG_EMBEDDING_MODEL":"sentence-transformers/all-MiniLM-L6-v2","CHUNK_SIZE":"1000","CHUNK_OVERLAP":"100","RAG_TEXT_SPLITTER":"character","ENABLE_MARKDOWN_HEADER_TEXT_SPLITTER":"True","RAG_TOP_K":"3","RAG_RELEVANCE_THRESHOLD":"0","ENABLE_RAG_HYBRID_SEARCH":"False","BYPASS_EMBEDDING_AND_RETRIEVAL":"False","RAG_FULL_CONTEXT":"False","ENABLE_WEB_SEARCH":"False","ENABLE_RETRIEVAL_QUERY_GENERATION":"True"},"image":"image@sha256:test","network_mode":"bridge","ports":["127.0.0.1:3001:8080"]}}}
JSON
cat > "$TEMP/container-before.json" <<'JSON'
[{"Id":"container","Name":"/open-webui-validation","Image":"sha256:test","RestartCount":0,"State":{"Status":"running","Running":true,"StartedAt":"before","Health":{"Status":"healthy"}},"Mounts":[{"Type":"volume","Name":"open-webui-validation","Destination":"/app/backend/data"}],"NetworkSettings":{"Networks":{"bridge":{"IPAddress":"172.17.0.2"}}}}]
JSON
sed 's/"StartedAt":"before"/"StartedAt":"after"/' "$TEMP/container-before.json" > "$TEMP/container-after.json"
cat > "$TEMP/image.json" <<'JSON'
[{"Id":"sha256:test","RepoDigests":["image@sha256:test"]}]
JSON
cat > "$TEMP/database.json" <<'JSON'
{"admin_count":1,"model":{"associations":[],"base_model_id":"llama3.2:3b","id":"llama-32-3b-rag-deterministic-test","is_active":true,"name":"Llama 3.2 3B RAG Deterministic Test","seed":42,"system_prompt":"ABSENT","temperature":0},"quick_check":"ok","target_model_count":1,"user_count":1}
JSON
python3 scripts/adp24_capture_restart_state.py --phase before --compose-json "$TEMP/compose.json" --container-inspect-json "$TEMP/container-before.json" --image-inspect-json "$TEMP/image.json" --database-json "$TEMP/database.json" --output "$TEMP/before.txt" >/dev/null
python3 scripts/adp24_capture_restart_state.py --phase after --compose-json "$TEMP/compose.json" --container-inspect-json "$TEMP/container-after.json" --image-inspect-json "$TEMP/image.json" --database-json "$TEMP/database.json" --output "$TEMP/after.txt" >/dev/null
before_sha="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["stable_state_sha256"])' "$TEMP/before.txt")"
after_sha="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["stable_state_sha256"])' "$TEMP/after.txt")"
test "$before_sha" = "$after_sha" || fail SEMANTIC_EQUIVALENCE_FIXTURE

python3 - "$TEMP/database.json" "$TEMP/database-drift.json" <<'PY'
import json
import sys
data = json.load(open(sys.argv[1]))
data["model"]["is_active"] = False
with open(sys.argv[2], "w", encoding="utf-8") as handle:
    json.dump(data, handle, sort_keys=True)
PY
python3 scripts/adp24_capture_restart_state.py --phase after --compose-json "$TEMP/compose.json" --container-inspect-json "$TEMP/container-after.json" --image-inspect-json "$TEMP/image.json" --database-json "$TEMP/database-drift.json" --output "$TEMP/drift.txt" >/dev/null
drift_sha="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["stable_state_sha256"])' "$TEMP/drift.txt")"
test "$before_sha" != "$drift_sha" || fail SEMANTIC_DRIFT_FIXTURE
printf 'SEMANTIC_PERSISTENCE_FIXTURE_STATUS=PASS\n'

grep -Fq '10-restart-before.txt' scripts/adp24_validation_restart_persistence.sh || fail BEFORE_FILENAME_BINDING
grep -Fq '11-restart-after.txt' scripts/adp24_validation_restart_persistence.sh || fail AFTER_FILENAME_BINDING
grep -Fq 'stable_state_sha256' scripts/adp24_validation_restart_persistence.sh || fail SEMANTIC_HASH_BINDING
grep -Fq 'GUIDE_STATUS=RUNTIME_RESILIENCE_CONTROLS_V2_DEFINED' docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md || fail GUIDE_STATUS
grep -Fq 'HISTORICAL_RUNTIME_RESILIENCE_TAG=adp-v2.4-runtime-resilience-controls' docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md || fail HISTORICAL_GUIDE_TAG
grep -Fq 'RUNTIME_RESILIENCE_CORRECTION_TAG=adp-v2.4-runtime-resilience-controls-v2' docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md || fail CORRECTED_GUIDE_TAG
grep -Fq 'scripts/adp24_validation_restart_persistence.sh' docs/Operations/ADP-v2.4-Isolated-Validation-Restart-Persistence-Procedure.md || fail PROCEDURE_BINDING
grep -Fq 'HISTORICAL_RUNTIME_RESILIENCE_TAG=adp-v2.4-runtime-resilience-controls' docs/Operations/ADP-v2.4-Isolated-Validation-Restart-Persistence-Procedure.md || fail HISTORICAL_PROCEDURE_TAG
grep -Fq 'RUNTIME_RESILIENCE_TAG=adp-v2.4-runtime-resilience-controls-v2' docs/Operations/ADP-v2.4-Isolated-Validation-Restart-Persistence-Procedure.md || fail CORRECTED_PROCEDURE_TAG
grep -Fq 'SHA256=fbd7e2578837030f48ac6b5460c8de12bac5407ed1270f34c35df5d75627d661' docs/Releases/ADP-v2.4-Runtime-Resilience-and-Evidence-Control-Amendment.md || fail DEFECT_AUDIT_TRACEABILITY
grep -Fq 'adp-v2.4-runtime-resilience-controls-v2' docs/Releases/ADP-v2.4-Runtime-Resilience-and-Evidence-Control-Amendment.md || fail CORRECTED_TAG_TRACEABILITY
printf 'SEMANTIC_TRACEABILITY_STATUS=PASS\n'

git diff --check
printf 'TRACKED_DIFF_CHECK_STATUS=PASS\n'
printf 'ADP24_RUNTIME_RESILIENCE_QUALITY_GATE=PASS\n'
printf 'ADP24_RUNTIME_RESILIENCE_V2_QUALITY_GATE=PASS\n'
printf 'REPOSITORY_ONLY_IMPLEMENTATION=PASS\n'
printf 'VALIDATION_RUNTIME_MUTATION=NONE\n'
printf 'RESTART_PERSISTENCE_AUTHORIZATION=HOLD_PENDING_V2_PROMOTION\n'
printf 'NON_COUNTED_RAG_EXECUTION_AUTHORIZATION=HOLD\n'
printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
