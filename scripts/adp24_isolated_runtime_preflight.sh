#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$HOME/Labs/AI-Development-Platform}"
BASELINE="079f30d909114aca450207c37c84ac471b9db828"
COMPOSE="$REPO/docker/open-webui-validation/docker-compose.yml"
TEMPLATE="$REPO/artifacts/Configuration/ADP-v2.4/approved-rag-template.txt"
PRIMARY_COMPOSE="$REPO/docker/open-webui/docker-compose.yml"
PRIMARY_SHA="dc2d3ef43ccde7ad77f7f70ae55928d234cabc5f921f5c52e74d349710f7ad2e"
IMAGE="ghcr.io/open-webui/open-webui:v0.10.2"
IMAGE_ID="sha256:9fcea9c6e32ab60b0498f3986c6cdf651ddbe61db48d2213a3d28048ddd673d4"
TEMP=""

cleanup() {
  if [ "$TEMP" != "" ]; then
    rm -f "$TEMP"
  fi
}
trap cleanup EXIT

fail() {
  printf 'ISOLATED_RUNTIME_PREFLIGHT=FAIL\n'
  printf 'FAILED_CONTROL=%s\n' "$1"
  if [ "${2:-}" != "" ]; then
    printf 'FAILED_VALUE=%s\n' "$2"
  fi
  printf 'RUNTIME_AUTHORIZATION=HOLD\n'
  printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
  exit 1
}

test -d "$REPO/.git" || fail REPOSITORY "$REPO"
git -C "$REPO" fetch origin main >/dev/null
test "$(git -C "$REPO" rev-parse HEAD)" = "$BASELINE" || fail GIT_HEAD "$(git -C "$REPO" rev-parse HEAD)"
test "$(git -C "$REPO" rev-parse main)" = "$BASELINE" || fail GIT_MAIN "$(git -C "$REPO" rev-parse main)"
test "$(git -C "$REPO" rev-parse origin/main)" = "$BASELINE" || fail GIT_ORIGIN_MAIN "$(git -C "$REPO" rev-parse origin/main)"
test -z "$(git -C "$REPO" status --short)" || fail WORKTREE_DIRTY

test "$(sha256sum "$PRIMARY_COMPOSE" | awk '{print $1}')" = "$PRIMARY_SHA" || fail PRIMARY_COMPOSE_CHECKSUM
test "$(sha256sum "$TEMPLATE" | awk '{print $1}')" = "def3db3e05b1651aa33b921a03573074d8033ca5d2ce691446638e362ef92d96" || fail TEMPLATE_CHECKSUM

docker compose -f "$COMPOSE" config --quiet || fail COMPOSE_CONFIG
TEMP="$(mktemp)"
docker compose -f "$COMPOSE" config --format json > "$TEMP" || fail COMPOSE_JSON
python3 "$REPO/scripts/adp24_validate_compose_config.py" --compose-json "$TEMP" --approved-template "$TEMPLATE" || fail COMPOSE_SEMANTIC

if docker container inspect open-webui-validation >/dev/null 2>&1; then
  fail VALIDATION_CONTAINER_EXISTS
fi
if docker volume inspect open-webui-validation >/dev/null 2>&1; then
  fail VALIDATION_VOLUME_EXISTS
fi
if ss -ltn | grep -q '127.0.0.1:3001'; then
  fail VALIDATION_PORT_IN_USE
fi

actual_image_id="$(docker image inspect "$IMAGE" --format '{{.Id}}')"
test "$actual_image_id" = "$IMAGE_ID" || fail IMAGE_ID "$actual_image_id"

docker ps --filter name='^open-webui$' --format '{{.Names}}' | grep -Fxq open-webui || fail PRIMARY_CONTAINER
curl -fsS http://127.0.0.1:3000/health | grep -Fq '"status":true' || fail PRIMARY_HEALTH
curl -fsS http://127.0.0.1:3000/api/version | grep -Fq '"version":"0.10.2"' || fail PRIMARY_VERSION

printf 'ISOLATED_RUNTIME_PREFLIGHT=PASS\n'
printf 'VALIDATION_CONTAINER=ABSENT\n'
printf 'VALIDATION_VOLUME=ABSENT\n'
printf 'VALIDATION_PORT_3001=FREE\n'
printf 'PRIMARY_INSTANCE_STATUS=PASS\n'
printf 'PRIMARY_INSTANCE_CHANGE=NONE\n'
printf 'RUNTIME_AUTHORIZATION=HOLD\n'
printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
