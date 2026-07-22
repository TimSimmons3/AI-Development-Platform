#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$HOME/Labs/AI-Development-Platform}"
COMPOSE="$REPO/docker/open-webui-validation/docker-compose.yml"
TEMPLATE="$REPO/artifacts/Configuration/ADP-v2.4/approved-rag-template.txt"
TEMP="$(mktemp -d)"
trap 'rm -rf "$TEMP"' EXIT

fail() {
  printf 'ISOLATED_RUNTIME_VERIFY=FAIL\n'
  printf 'FAILED_CONTROL=%s\n' "$1"
  if [ "${2:-}" != "" ]; then
    printf 'FAILED_VALUE=%s\n' "$2"
  fi
  printf 'RUNTIME_AUTHORIZATION=HOLD\n'
  printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
  exit 1
}

docker compose -f "$COMPOSE" config --format json > "$TEMP/compose.json" || fail COMPOSE_JSON
python3 "$REPO/scripts/adp24_validate_compose_config.py" --compose-json "$TEMP/compose.json" --approved-template "$TEMPLATE" || fail COMPOSE_SEMANTIC

docker inspect open-webui-validation > "$TEMP/container.json" || fail CONTAINER_INSPECT
docker image inspect ghcr.io/open-webui/open-webui:v0.10.2 > "$TEMP/image.json" || fail IMAGE_INSPECT

state="$(docker inspect open-webui-validation --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}')"
test "$state" = "healthy" || fail VALIDATION_HEALTH "$state"

docker volume inspect open-webui-validation >/dev/null || fail VALIDATION_VOLUME
curl -fsS http://127.0.0.1:3001/health | grep -Fq '"status":true' || fail VALIDATION_HTTP_HEALTH
curl -fsS http://127.0.0.1:3000/health | grep -Fq '"status":true' || fail PRIMARY_HEALTH

docker exec open-webui-validation python -c 'import urllib.request; print(urllib.request.urlopen("http://host.docker.internal:11434/api/version",timeout=5).read().decode())' | grep -Fq 'version' || fail OLLAMA_CONNECTIVITY

printf 'ISOLATED_RUNTIME_VERIFY=PASS\n'
printf 'VALIDATION_HEALTH=PASS\n'
printf 'VALIDATION_VOLUME=open-webui-validation\n'
printf 'OLLAMA_CONNECTIVITY=PASS\n'
printf 'PRIMARY_INSTANCE_STATUS=PASS\n'
printf 'PRIMARY_INSTANCE_CHANGE=NONE\n'
printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
