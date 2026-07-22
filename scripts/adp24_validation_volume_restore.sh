#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
ARCHIVE="${2:-}"
VOLUME="open-webui-validation"
CONTAINER="open-webui-validation"
IMAGE="ghcr.io/open-webui/open-webui:v0.10.2@sha256:9fcea9c6e32ab60b0498f3986c6cdf651ddbe61db48d2213a3d28048ddd673d4"

fail() {
  printf 'VALIDATION_VOLUME_RESTORE=FAIL\n'
  printf 'FAILED_CONTROL=%s\n' "$1"
  if [ "${2:-}" != "" ]; then
    printf 'FAILED_VALUE=%s\n' "$2"
  fi
  printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
  exit 1
}

if [ "$ACTION" != "--restore" ]; then
  fail RESTORE_FLAG_REQUIRED
fi
test "$ARCHIVE" != "" || fail ARCHIVE_REQUIRED
test -s "$ARCHIVE" || fail ARCHIVE_NOT_FOUND "$ARCHIVE"
test -s "$ARCHIVE.sha256" || fail CHECKSUM_FILE_NOT_FOUND "$ARCHIVE.sha256"
sha256sum -c "$ARCHIVE.sha256" >/dev/null || fail ARCHIVE_CHECKSUM
tar -tzf "$ARCHIVE" >/dev/null || fail ARCHIVE_LISTING
docker volume inspect "$VOLUME" >/dev/null || fail VALIDATION_VOLUME_ABSENT
curl -fsS http://127.0.0.1:3000/health | grep -Fq '"status":true' || fail PRIMARY_HEALTH_BEFORE

if docker inspect "$CONTAINER" >/dev/null 2>&1; then
  docker stop "$CONTAINER" >/dev/null || true
fi

backup_dir="$(cd "$(dirname "$ARCHIVE")" && pwd)"
backup_name="$(basename "$ARCHIVE")"
docker run --rm --network none -v "$VOLUME:/data" -v "$backup_dir:/backup:ro" "$IMAGE" bash -lc "find /data -mindepth 1 -maxdepth 1 -exec rm -rf -- {} + && tar -xzf '/backup/$backup_name' -C /data" || fail RESTORE_DATA

printf 'VALIDATION_VOLUME_RESTORE=PASS\n'
printf 'VALIDATION_VOLUME=%s\n' "$VOLUME"
printf 'PRIMARY_INSTANCE_CHANGE=NONE\n'
printf 'NEXT_ACTION=START_AND_VERIFY_VALIDATION_CONTAINER\n'
printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
