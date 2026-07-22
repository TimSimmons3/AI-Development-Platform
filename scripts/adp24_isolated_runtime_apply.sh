#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
REPO="${2:-$HOME/Labs/AI-Development-Platform}"
COMPOSE="$REPO/docker/open-webui-validation/docker-compose.yml"

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

bash "$REPO/scripts/adp24_isolated_runtime_preflight.sh" "$REPO" || fail PREFLIGHT

docker compose -f "$COMPOSE" up -d --no-build --pull never || fail VALIDATION_CREATE

for attempt in $(seq 1 60); do
  state="$(docker inspect open-webui-validation --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' 2>/dev/null || true)"
  if [ "$state" = "healthy" ]; then
    break
  fi
  if [ "$state" = "unhealthy" ] || [ "$state" = "exited" ] || [ "$state" = "dead" ]; then
    fail VALIDATION_HEALTH "$state"
  fi
  sleep 2
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
