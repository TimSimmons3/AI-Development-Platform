#!/usr/bin/env bash
set -euo pipefail

REPO="$HOME/Labs/AI-Development-Platform"
OUT="$HOME/Downloads"
COMMENT="ADP-v2.3.1-deterministic-rag-validation-closeout"

fail() {
  printf 'POST_CLOSEOUT_RECOVERY_STATUS=FAIL\n'
  printf 'FAILED_CONTROL=%s\n' "$1"
  exit 1
}

cd "$REPO"
git fetch origin main

BRANCH="$(git branch --show-current)"
HEAD_SHA="$(git rev-parse --short HEAD)"
MAIN_SHA="$(git rev-parse --short main)"
ORIGIN_SHA="$(git rev-parse --short origin/main)"
WORKTREE_COUNT="$(git status --porcelain | wc -l | tr -d ' ')"

printf 'BRANCH=%s\n' "$BRANCH"
printf 'HEAD=%s\n' "$HEAD_SHA"
printf 'MAIN=%s\n' "$MAIN_SHA"
printf 'ORIGIN_MAIN=%s\n' "$ORIGIN_SHA"
printf 'WORKTREE_COUNT=%s\n' "$WORKTREE_COUNT"

test "$BRANCH" = "main" || fail "BRANCH"
test "$HEAD_SHA" = "$MAIN_SHA" || fail "MAIN_ALIGNMENT"
test "$HEAD_SHA" = "$ORIGIN_SHA" || fail "ORIGIN_ALIGNMENT"
test "$WORKTREE_COUNT" = "0" || fail "WORKTREE"
printf 'GIT_START_STATUS=PASS\n'

printf 'Timeshift requires sudo authentication when not already cached.\n'
sudo timeshift --create --comments "$COMMENT" --tags D
sudo timeshift --list | grep -F "$COMMENT" >/dev/null || fail "TIMESHIFT_VERIFICATION"
printf 'TIMESHIFT_SNAPSHOT_STATUS=PASS\n'

BUNDLE="$OUT/AI-Development-Platform-v2.3.1-closeout-$HEAD_SHA.bundle"
SOURCE="$OUT/AI-Development-Platform-v2.3.1-closeout-$HEAD_SHA-source.tar.gz"

rm -f "$BUNDLE" "$BUNDLE.sha256" "$SOURCE" "$SOURCE.sha256"

git bundle create "$BUNDLE" --all
git bundle verify "$BUNDLE"
sha256sum "$BUNDLE" > "$BUNDLE.sha256"
printf 'GIT_BUNDLE_STATUS=PASS\n'

git archive \
  --format=tar.gz \
  --prefix="AI-Development-Platform-$HEAD_SHA/" \
  --output="$SOURCE" \
  HEAD

tar -tzf "$SOURCE" >/dev/null
sha256sum "$SOURCE" > "$SOURCE.sha256"
printf 'SOURCE_ARCHIVE_STATUS=PASS\n'

sha256sum -c "$BUNDLE.sha256"
sha256sum -c "$SOURCE.sha256"
printf 'RECOVERABILITY_CHECKSUM_STATUS=PASS\n'

printf 'POST_CLOSEOUT_RECOVERY_STATUS=PASS\n'
printf 'CLOSEOUT_COMMIT=%s\n' "$HEAD_SHA"
printf 'TIMESHIFT_COMMENT=%s\n' "$COMMENT"
printf 'GIT_BUNDLE=%s\n' "$BUNDLE"
printf 'SOURCE_ARCHIVE=%s\n' "$SOURCE"
