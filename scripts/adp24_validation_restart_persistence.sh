\
#!/usr/bin/env bash
set -euo pipefail
umask 077

ACTION="${1:-}"
REPO="${2:-$HOME/Labs/AI-Development-Platform}"
EVIDENCE_DIR="${3:-}"
COMPOSE="$REPO/docker/open-webui-validation/docker-compose.yml"
CONTAINER="open-webui-validation"
IMAGE_REF="ghcr.io/open-webui/open-webui:v0.10.2"
BEFORE="$EVIDENCE_DIR/10-restart-before.txt"
AFTER="$EVIDENCE_DIR/11-restart-after.txt"
MAX_ATTEMPTS="${ADP24_HEALTH_ATTEMPTS:-300}"
SLEEP_SECONDS="${ADP24_HEALTH_SLEEP_SECONDS:-2}"
TEMP="$(mktemp -d)"
trap 'rm -rf "$TEMP"' EXIT

fail() {
  printf 'RESTART_PERSISTENCE_GATE=FAIL\n'
  printf 'FAILED_CONTROL=%s\n' "$1"
  if [ "${2:-}" != "" ]; then
    printf 'FAILED_VALUE=%s\n' "$2"
  fi
  printf 'NON_COUNTED_RAG_EXECUTION_AUTHORIZATION=HOLD\n'
  printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
  exit 1
}

capture_database() {
  docker exec "$CONTAINER" python -c '
import json
import sqlite3

db = sqlite3.connect("file:/app/backend/data/webui.db?mode=ro", uri=True)
quick = db.execute("PRAGMA quick_check").fetchone()[0]
users = db.execute("SELECT COUNT(*) FROM user").fetchone()[0]
admins = db.execute("SELECT COUNT(*) FROM user WHERE role=?", ("admin",)).fetchone()[0]
rows = db.execute(
    "SELECT id,base_model_id,name,params,meta,is_active FROM model WHERE id=?",
    ("llama-32-3b-rag-deterministic-test",),
).fetchall()
assert len(rows) == 1
row = rows[0]
params = json.loads(row[3]) if isinstance(row[3], str) else row[3]
meta = json.loads(row[4]) if isinstance(row[4], str) else row[4]
association_keys = (
    "knowledge", "knowledge_ids", "tools", "tool_ids", "skills", "skill_ids",
    "functions", "function_ids", "filters", "filter_ids", "files",
)
associations = [
    key for key in association_keys
    if meta.get(key) not in (None, "", [], {}, False)
]
result = {
    "quick_check": quick,
    "user_count": users,
    "admin_count": admins,
    "target_model_count": len(rows),
    "model": {
        "id": row[0],
        "base_model_id": row[1],
        "name": row[2],
        "temperature": params.get("temperature"),
        "seed": params.get("seed"),
        "system_prompt": "ABSENT" if params.get("system") in (None, "") else "PRESENT",
        "is_active": bool(row[5]),
        "associations": associations,
    },
}
assert quick == "ok"
assert users == 1
assert admins == 1
assert row[1] == "llama3.2:3b"
assert params.get("temperature") == 0
assert params.get("seed") == 42
assert params.get("system") in (None, "")
assert row[5] == 1
assert not associations
print(json.dumps(result, ensure_ascii=True, sort_keys=True))
db.close()
'
}

capture_state() {
  phase="$1"
  output="$2"
  docker compose -f "$COMPOSE" config --format json > "$TEMP/compose-$phase.json"
  docker inspect "$CONTAINER" > "$TEMP/container-$phase.json"
  docker image inspect "$IMAGE_REF" > "$TEMP/image-$phase.json"
  capture_database > "$TEMP/database-$phase.json"
  python3 "$REPO/scripts/adp24_capture_restart_state.py" \
    --phase "$phase" \
    --compose-json "$TEMP/compose-$phase.json" \
    --container-inspect-json "$TEMP/container-$phase.json" \
    --image-inspect-json "$TEMP/image-$phase.json" \
    --database-json "$TEMP/database-$phase.json" \
    --output "$output"
  chmod 600 "$output"
}

if [ "$ACTION" != "--execute" ]; then
  fail EXECUTION_FLAG_REQUIRED
fi
test "$EVIDENCE_DIR" != "" || fail EVIDENCE_DIRECTORY_REQUIRED
test -d "$EVIDENCE_DIR" || fail EVIDENCE_DIRECTORY "$EVIDENCE_DIR"
test ! -e "$BEFORE" || fail BEFORE_OUTPUT_ALREADY_EXISTS "$BEFORE"
test ! -e "$AFTER" || fail AFTER_OUTPUT_ALREADY_EXISTS "$AFTER"
test -z "$(git -C "$REPO" status --short)" || fail REPOSITORY_NOT_CLEAN

case "$MAX_ATTEMPTS" in
  ''|*[!0-9]*) fail HEALTH_ATTEMPTS "$MAX_ATTEMPTS" ;;
esac
case "$SLEEP_SECONDS" in
  ''|*[!0-9]*) fail HEALTH_SLEEP_SECONDS "$SLEEP_SECONDS" ;;
esac
test "$MAX_ATTEMPTS" -gt 0 || fail HEALTH_ATTEMPTS "$MAX_ATTEMPTS"

curl -fsS http://127.0.0.1:3000/health | grep -Fq '"status":true' || fail PRIMARY_HEALTH_BEFORE
state="$(docker inspect "$CONTAINER" --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' 2>/dev/null || true)"
test "$state" = "healthy" || fail VALIDATION_HEALTH_BEFORE "$state"

capture_state before "$BEFORE"
before_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["runtime_identity"]["container_id"])' "$BEFORE")"
before_sha="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["stable_state_sha256"])' "$BEFORE")"

docker restart "$CONTAINER" >/dev/null || fail VALIDATION_RESTART

previous_state=""
for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  state="$(docker inspect "$CONTAINER" --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' 2>/dev/null || true)"
  if [ "$state" != "$previous_state" ]; then
    printf 'RESTART_WAIT_ATTEMPT=%s STATE=%s\n' "$attempt" "$state"
    previous_state="$state"
  fi
  if [ "$state" = "healthy" ]; then
    break
  fi
  if [ "$state" = "exited" ] || [ "$state" = "dead" ]; then
    fail VALIDATION_TERMINAL_STATE "$state"
  fi
  sleep "$SLEEP_SECONDS"
done

state="$(docker inspect "$CONTAINER" --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}')"
test "$state" = "healthy" || fail VALIDATION_HEALTH_TIMEOUT "$state"
bash "$REPO/scripts/adp24_isolated_runtime_verify.sh" "$REPO" || fail RUNTIME_VERIFY_AFTER_RESTART

capture_state after "$AFTER"
after_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["runtime_identity"]["container_id"])' "$AFTER")"
after_sha="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["stable_state_sha256"])' "$AFTER")"

test "$after_id" = "$before_id" || fail CONTAINER_ID_DRIFT "$before_id->$after_id"
test "$after_sha" = "$before_sha" || fail STABLE_STATE_DRIFT "$before_sha->$after_sha"
curl -fsS http://127.0.0.1:3000/health | grep -Fq '"status":true' || fail PRIMARY_HEALTH_AFTER
test -z "$(git -C "$REPO" status --short)" || fail REPOSITORY_CHANGED

printf 'RESTART_PERSISTENCE_GATE=PASS\n'
printf 'CONTAINER_ID_PRESERVED=PASS\n'
printf 'STABLE_STATE_SHA256=%s\n' "$after_sha"
printf 'MODEL_STATE_PERSISTENCE=PASS\n'
printf 'CONFIGURATION_PERSISTENCE=PASS\n'
printf 'VOLUME_PERSISTENCE=PASS\n'
printf 'PRIMARY_INSTANCE_STATUS=PASS\n'
printf 'REPOSITORY_CLEANLINESS=PASS\n'
printf 'BEFORE_EVIDENCE_SHA256=%s\n' "$(sha256sum "$BEFORE" | awk '{print $1}')"
printf 'AFTER_EVIDENCE_SHA256=%s\n' "$(sha256sum "$AFTER" | awk '{print $1}')"
printf 'NON_COUNTED_RAG_EXECUTION_AUTHORIZATION=HOLD_PENDING_REVIEW\n'
printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
