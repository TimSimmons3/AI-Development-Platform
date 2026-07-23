\
#!/usr/bin/env bash
set -euo pipefail
umask 077

ACTION="${1:-}"
DEST="${2:-}"
VOLUME="open-webui-validation"
CONTAINER="open-webui-validation"
IMAGE="ghcr.io/open-webui/open-webui:v0.10.2@sha256:9fcea9c6e32ab60b0498f3986c6cdf651ddbe61db48d2213a3d28048ddd673d4"
HOST_UID="$(id -u)"
HOST_GID="$(id -g)"
WAS_RUNNING=0
ARCHIVE=""

cleanup() {
  if [ "$WAS_RUNNING" -eq 1 ] && docker inspect "$CONTAINER" >/dev/null 2>&1; then
    running="$(docker inspect "$CONTAINER" --format '{{.State.Running}}' 2>/dev/null || true)"
    if [ "$running" != "true" ]; then
      docker start "$CONTAINER" >/dev/null 2>&1 || true
    fi
  fi
}
trap cleanup EXIT

fail() {
  printf 'VALIDATION_VOLUME_BACKUP=FAIL\n'
  printf 'FAILED_CONTROL=%s\n' "$1"
  if [ "${2:-}" != "" ]; then
    printf 'FAILED_VALUE=%s\n' "$2"
  fi
  printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
  exit 1
}

if [ "$ACTION" != "--execute" ]; then
  fail EXECUTION_FLAG_REQUIRED
fi
test "$DEST" != "" || fail BACKUP_DIRECTORY_REQUIRED
mkdir -p "$DEST"
chmod 700 "$DEST"
test -d "$DEST" || fail BACKUP_DIRECTORY "$DEST"
docker volume inspect "$VOLUME" >/dev/null || fail VALIDATION_VOLUME_ABSENT
curl -fsS http://127.0.0.1:3000/health | grep -Fq '"status":true' || fail PRIMARY_HEALTH_BEFORE

if docker inspect "$CONTAINER" >/dev/null 2>&1; then
  running="$(docker inspect "$CONTAINER" --format '{{.State.Running}}')"
  if [ "$running" = "true" ]; then
    WAS_RUNNING=1
    docker stop "$CONTAINER" >/dev/null || fail VALIDATION_STOP
  fi
fi

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
name="ADP-v2.4-open-webui-validation-${timestamp}.tar.gz"
ARCHIVE="$DEST/$name"
test ! -e "$ARCHIVE" || fail BACKUP_ALREADY_EXISTS "$ARCHIVE"

docker run --rm --network none \
  -v "$VOLUME:/data:ro" \
  -v "$DEST:/backup" \
  "$IMAGE" \
  bash -lc "tar -czf '/backup/$name' -C /data . && chown '$HOST_UID:$HOST_GID' '/backup/$name' && chmod 600 '/backup/$name'" \
  || fail BACKUP_ARCHIVE

test -s "$ARCHIVE" || fail BACKUP_EMPTY
test "$(stat -c '%u:%g' "$ARCHIVE")" = "$HOST_UID:$HOST_GID" || fail BACKUP_OWNERSHIP "$(stat -c '%u:%g' "$ARCHIVE")"
test "$(stat -c '%a' "$ARCHIVE")" = "600" || fail BACKUP_PERMISSIONS "$(stat -c '%a' "$ARCHIVE")"
sha256sum "$ARCHIVE" > "$ARCHIVE.sha256"
chmod 600 "$ARCHIVE.sha256"
sha256sum -c "$ARCHIVE.sha256" >/dev/null || fail BACKUP_CHECKSUM
tar -tzf "$ARCHIVE" >/dev/null || fail BACKUP_LISTING

if [ "$WAS_RUNNING" -eq 1 ]; then
  docker start "$CONTAINER" >/dev/null || fail VALIDATION_RESTART
  WAS_RUNNING=0
fi
curl -fsS http://127.0.0.1:3000/health | grep -Fq '"status":true' || fail PRIMARY_HEALTH_AFTER

printf 'VALIDATION_VOLUME_BACKUP=PASS\n'
printf 'BACKUP_ARCHIVE=%s\n' "$ARCHIVE"
printf 'BACKUP_SHA256=%s\n' "$(sha256sum "$ARCHIVE" | awk '{print $1}')"
printf 'BACKUP_OWNER=%s:%s\n' "$HOST_UID" "$HOST_GID"
printf 'BACKUP_PERMISSIONS=600\n'
printf 'PRIMARY_INSTANCE_CHANGE=NONE\n'
printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
