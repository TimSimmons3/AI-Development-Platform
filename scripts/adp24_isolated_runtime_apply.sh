#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
REPO="${2:-$HOME/Labs/AI-Development-Platform}"
COMPOSE="$REPO/docker/open-webui-validation/docker-compose.yml"
MAX_ATTEMPTS="${ADP24_HEALTH_ATTEMPTS:-300}"
SLEEP_SECONDS="${ADP24_HEALTH_SLEEP_SECONDS:-2}"

fail() {
  printf 'ISOLATED_RUNTIME_APPLY=FAIL\n'
  printf 'FAILED_CONTROL=%s\n' "$1"
  if [ "${2:-}" != "" ]; then
    printf 'FAILED_VALUE=%s\n' "$2"
  fi
  printf 'PRIMARY_INSTANCE_CHANGE=NONE\n'
  printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
  exit 1
}

if [ "$ACTION" != "--execute" ]; then
  fail EXECUTION_FLAG_REQUIRED
fi

case "$MAX_ATTEMPTS" in
  ''|*[!0-9]*) fail HEALTH_ATTEMPTS "$MAX_ATTEMPTS" ;;
esac
case "$SLEEP_SECONDS" in
  ''|*[!0-9]*) fail HEALTH_SLEEP_SECONDS "$SLEEP_SECONDS" ;;
esac
test "$MAX_ATTEMPTS" -gt 0 || fail HEALTH_ATTEMPTS "$MAX_ATTEMPTS"

bash "$REPO/scripts/adp24_isolated_runtime_preflight.sh" "$REPO" || fail PREFLIGHT
docker compose -f "$COMPOSE" up -d --no-build --pull never || fail VALIDATION_CREATE

previous_state=""
for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  state="$(docker inspect open-webui-validation --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' 2>/dev/null || true)"
  if [ "$state" != "$previous_state" ]; then
    printf 'HEALTH_WAIT_ATTEMPT=%s STATE=%s\n' "$attempt" "$state"
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

state="$(docker inspect open-webui-validation --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}')"
test "$state" = "healthy" || fail VALIDATION_HEALTH_TIMEOUT "$state"

curl -fsS http://127.0.0.1:3001/health | grep -Fq '"status":true' || fail VALIDATION_HTTP_HEALTH
curl -fsS http://127.0.0.1:3001/api/version | grep -Fq '"version":"0.10.2"' || fail VALIDATION_VERSION
curl -fsS http://127.0.0.1:3000/health | grep -Fq '"status":true' || fail PRIMARY_POST_CREATE_HEALTH

printf 'ISOLATED_RUNTIME_APPLY=PASS\n'
printf 'VALIDATION_CONTAINER=CREATED_HEALTHY\n'
printf 'VALIDATION_VOLUME=CREATED\n'
printf 'VALIDATION_BINDING=127.0.0.1:3001\n'
printf 'PRIMARY_INSTANCE_STATUS=PASS\n'
printf 'PRIMARY_INSTANCE_CHANGE=NONE\n'
printf 'MODEL_IMPORT_AUTHORIZATION=HOLD_PENDING_ADMIN_SETUP\n'
printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
