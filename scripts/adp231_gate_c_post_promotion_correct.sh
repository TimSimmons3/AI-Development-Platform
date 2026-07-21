#!/usr/bin/env bash
set -euo pipefail

EXPECTED_BASELINE="${ADP_EXPECTED_BASELINE:-efa97c5}"
EXPECTED_PLAN_SHA="130a79ba28ef428e033b7b913f9545395d20d72511a8fbe68e6edc3c370943f7"
EXPECTED_GATE_B_SHA="35fd09281bca5bc0c6e803bd9beed56bce9d4eccecd15a7ef79fb92d9fbf8e59"
EXPECTED_TIMESHIFT_ID="2026-07-20_11-32-48"
EXPECTED_TIMESHIFT_DESC="ADP-v2.3-reg-hardening-t01-failure-closeout"
REPO="${ADP_REPO:-$HOME/Labs/AI-Development-Platform}"
PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAMP="$(date '+%Y%m%d-%H%M%S')"
TRANSCRIPT="/tmp/ADP-v2.3.1-Gate-C-Post-Promotion-Correction-$STAMP.log"

exec > >(tee "$TRANSCRIPT") 2>&1

printf '\n===== CORRECTION PACKET =====\n'
printf 'PACKET_ID=CA-231-C-01\n'
printf 'PACKAGE_DIR=%s\n' "$PACKAGE_DIR"
printf 'REPO=%s\n' "$REPO"
printf 'TRANSCRIPT=%s\n' "$TRANSCRIPT"

printf '\n===== STARTING REPOSITORY BASELINE =====\n'
cd "$REPO"
git fetch origin main
printf 'BRANCH=%s\n' "$(git branch --show-current)"
printf 'HEAD=%s\n' "$(git rev-parse --short HEAD)"
printf 'MAIN=%s\n' "$(git rev-parse --short main)"
printf 'ORIGIN_MAIN=%s\n' "$(git rev-parse --short origin/main)"
printf 'WORKTREE_COUNT=%s\n' "$(git status --porcelain | wc -l | tr -d ' ')"
test "$(git branch --show-current)" = "main"
test "$(git rev-parse --short HEAD)" = "$EXPECTED_BASELINE"
test "$(git rev-parse --short main)" = "$EXPECTED_BASELINE"
test "$(git rev-parse --short origin/main)" = "$EXPECTED_BASELINE"
test -z "$(git status --porcelain)"
git diff --check
printf 'STARTING_BASELINE_STATUS=PASS\n'

printf '\n===== CONTROLLING RECORD INTEGRITY =====\n'
printf '%s  %s\n' "$EXPECTED_PLAN_SHA" "docs/ADP-v2.3.1-RAG-Retrieval-Pipeline-and-Model-Behavior-Diagnostic-Plan.md" | sha256sum -c -
printf '%s  %s\n' "$EXPECTED_GATE_B_SHA" "docs/ADP-v2.3.1-Entry-and-Runtime-Baseline-Record.md" | sha256sum -c -
printf 'CONTROLLING_RECORD_STATUS=PASS\n'

printf '\n===== PRIOR ARTIFACT INTEGRITY =====\n'
printf '%s  %s\n' "714aafc834d2d8afb69348dbd1996443d78f06d429c1c41b8cb57bc4bf74a4a4" "docs/ADP-Controlled-Execution-Packet-Standard.md" | sha256sum -c -
printf '%s  %s\n' "b2bd130cd0cca20f76a5eab55d1e471dfbe174971e7f7449c9baa96c0edecddf" "docs/ADP-Final-Delivery-Validation-Standard.md" | sha256sum -c -
printf '%s  %s\n' "22328965a59d113684e412f8506b907a891c41929b1ed906503002ea478da446" "docs/ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md" | sha256sum -c -
printf '%s  %s\n' "b42a0c3d71d65ba412d7a750b2e55c9fb184c47b45c9c7063f52a471d3080daa" "docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md" | sha256sum -c -
printf '%s  %s\n' "7c42b94720aecfdb7779763fb3abd8a19ae260e33b52bff10cc7197aee7300b5" "docs/ADP-v2.3.1-Gate-C-New-Chat-Startup-v2.md" | sha256sum -c -
printf '%s  %s\n' "63c375ddd2eb96c2c79b45c17d4f417920037888348c75adeaff67473c8834e5" "docs/ADP-v2.3.1-Gate-C-Approved-Artifact-Manifest.md" | sha256sum -c -
printf '%s  %s\n' "df5cfc582d497464bf12e2d1320cb8396af466c2f791ef76ae9488d9e10cab29" "docs/ADP-v2.3.1-Gate-C-Artifact-Review-and-Approval-Record.md" | sha256sum -c -
printf '%s  %s\n' "23ebeb5e008b73281ee0b24ec98129b1e317e6f8d394e45e31309b5458318def" "scripts/adp231_gate_c_promote.sh" | sha256sum -c -
printf '%s  %s\n' "660a19bb0776fb99a17bc9a7e023fa321dfc45b081b98ace23cd05c9c0342fd1" "skills/adp-controlled-execution-packets/SKILL.md" | sha256sum -c -
test ! -e docs/ADP-v2.3.1-Gate-C-Post-Promotion-Audit-Correction-Record.md
test ! -e scripts/adp231_gate_c_post_promotion_correct.sh
printf 'PRIOR_ARTIFACT_INTEGRITY_STATUS=PASS\n'

printf '\n===== REQUIRED TIMESHIFT BASELINE =====\n'
if [ -n "${ADP_TIMESHIFT_FIXTURE:-}" ]; then
  TIMESHIFT_OUTPUT="$(cat "$ADP_TIMESHIFT_FIXTURE")"
else
  TIMESHIFT_OUTPUT="$(sudo timeshift --list 2>&1)"
fi
TIMESHIFT_LINE="$(printf '%s\n' "$TIMESHIFT_OUTPUT" | grep -F "$EXPECTED_TIMESHIFT_ID" | tail -n 1)"
printf 'TIMESHIFT_LINE=%s\n' "$TIMESHIFT_LINE"
test -n "$TIMESHIFT_LINE"
case "$TIMESHIFT_LINE" in
  *"$EXPECTED_TIMESHIFT_DESC"*) ;;
  *) printf 'TIMESHIFT_BASELINE_STATUS=FAIL\n'; exit 1 ;;
esac
printf 'TIMESHIFT_BASELINE_STATUS=PASS\n'

printf '\n===== CORRECTION PACKAGE VALIDATION =====\n'
cd "$PACKAGE_DIR"
sha256sum -c ADP-v2.3.1-Gate-C-Post-Promotion-Correction-Payload-SHA256.txt
while IFS= read -r file; do
  LC_ALL=C grep -n '[^ -~]' "$file" && false
  grep -n $'\t' "$file" && false
  grep -nE '[[:blank:]]+$' "$file" && false
  test -s "$file"
done < <(find . -type f \( -name '*.md' -o -name '*.sh' \) -print | sort)
bash -n scripts/adp231_gate_c_promote.sh
bash -n scripts/adp231_gate_c_post_promotion_correct.sh
printf 'CORRECTION_PACKAGE_STATUS=PASS\n'

printf '\n===== CONTROLLED CORRECTION COPY =====\n'
cd "$REPO"
install -d docs scripts skills/adp-controlled-execution-packets
cp "$PACKAGE_DIR/ADP-Controlled-Execution-Packet-Standard.md" docs/ADP-Controlled-Execution-Packet-Standard.md
cp "$PACKAGE_DIR/ADP-Final-Delivery-Validation-Standard.md" docs/ADP-Final-Delivery-Validation-Standard.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md" docs/ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md" docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Gate-C-New-Chat-Startup-v2.md" docs/ADP-v2.3.1-Gate-C-New-Chat-Startup-v2.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Gate-C-Approved-Artifact-Manifest.md" docs/ADP-v2.3.1-Gate-C-Approved-Artifact-Manifest.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Gate-C-Artifact-Review-and-Approval-Record.md" docs/ADP-v2.3.1-Gate-C-Artifact-Review-and-Approval-Record.md
cp "$PACKAGE_DIR/ADP-v2.3.1-Gate-C-Post-Promotion-Audit-Correction-Record.md" docs/ADP-v2.3.1-Gate-C-Post-Promotion-Audit-Correction-Record.md
cp "$PACKAGE_DIR/scripts/adp231_gate_c_promote.sh" scripts/adp231_gate_c_promote.sh
cp "$PACKAGE_DIR/scripts/adp231_gate_c_post_promotion_correct.sh" scripts/adp231_gate_c_post_promotion_correct.sh
cp "$PACKAGE_DIR/skills/adp-controlled-execution-packets/SKILL.md" skills/adp-controlled-execution-packets/SKILL.md
chmod 0755 scripts/adp231_gate_c_promote.sh
chmod 0755 scripts/adp231_gate_c_post_promotion_correct.sh
printf 'CONTROLLED_CORRECTION_STATUS=PASS\n'

printf '\n===== POST-COPY STATIC AND SEMANTIC VALIDATION =====\n'
git status --short
git diff --check
while IFS= read -r file; do
  LC_ALL=C grep -n '[^ -~]' "$file" && false
  grep -n $'\t' "$file" && false
  grep -nE '[[:blank:]]+$' "$file" && false
done < <(git status --porcelain | awk '{print $2}' | grep -E '\.(md|sh)$' | sort)
bash -n scripts/adp231_gate_c_promote.sh
bash -n scripts/adp231_gate_c_post_promotion_correct.sh
! grep -Fq 'ADP-v2.3.1-Gate-C-Integrated-Execution-Package.zip' docs/ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md
grep -Fq 'ADP-v2.3.1-Gate-C-Self-Contained-Installer-v2.sh' docs/ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md
grep -Fq "$EXPECTED_TIMESHIFT_ID" docs/ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md
grep -Fq "$EXPECTED_TIMESHIFT_ID" docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md
grep -Fq 'TIMESHIFT_BASELINE_STATUS=PASS' docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md
grep -Fq 'EXPECTED_TIMESHIFT_ID=' scripts/adp231_gate_c_promote.sh
grep -Fq 'Semantic Traceability and Consistency Gate' docs/ADP-Controlled-Execution-Packet-Standard.md
grep -Fq 'Semantic Delivery Consistency' docs/ADP-Final-Delivery-Validation-Standard.md
grep -Fq 'Semantic Traceability Enforcement' skills/adp-controlled-execution-packets/SKILL.md
grep -Fq 'CA-231-C-01' docs/ADP-v2.3.1-Gate-C-Post-Promotion-Audit-Correction-Record.md
printf 'SEMANTIC_TRACEABILITY_STATUS=PASS\n'

printf '\n===== STAGE, REVIEW, COMMIT, AND PUSH =====\n'
git add docs/ADP-Controlled-Execution-Packet-Standard.md
git add docs/ADP-Final-Delivery-Validation-Standard.md
git add docs/ADP-v2.3.1-Gate-C-Promotion-and-Synchronization-Execution-Packet.md
git add docs/ADP-v2.3.1-Gate-C-Runtime-Execution-Packet.md
git add docs/ADP-v2.3.1-Gate-C-New-Chat-Startup-v2.md
git add docs/ADP-v2.3.1-Gate-C-Approved-Artifact-Manifest.md
git add docs/ADP-v2.3.1-Gate-C-Artifact-Review-and-Approval-Record.md
git add docs/ADP-v2.3.1-Gate-C-Post-Promotion-Audit-Correction-Record.md
git add scripts/adp231_gate_c_promote.sh
git add scripts/adp231_gate_c_post_promotion_correct.sh
git add skills/adp-controlled-execution-packets/SKILL.md
git diff --cached --check
git diff --cached --stat
git diff --cached -- docs scripts skills
git commit -m "Correct ADP v2.3.1 Gate C pre-runtime traceability controls"
git push origin main
printf 'CORRECTION_COMMIT_STATUS=PASS\n'

printf '\n===== POST-CORRECTION SYNCHRONIZATION =====\n'
git fetch origin main
POST_HEAD="$(git rev-parse --short HEAD)"
POST_MAIN="$(git rev-parse --short main)"
POST_ORIGIN="$(git rev-parse --short origin/main)"
printf 'POST_CORRECTION_HEAD=%s\n' "$POST_HEAD"
printf 'POST_CORRECTION_MAIN=%s\n' "$POST_MAIN"
printf 'POST_CORRECTION_ORIGIN_MAIN=%s\n' "$POST_ORIGIN"
test "$POST_HEAD" = "$POST_MAIN"
test "$POST_HEAD" = "$POST_ORIGIN"
test -z "$(git status --porcelain)"
printf 'POST_CORRECTION_SYNCHRONIZATION_STATUS=PASS\n'

printf '\n===== RUNTIME ENTRY RESULT =====\n'
printf 'CORRECTION_STATUS=PASS\n'
printf 'SEMANTIC_TRACEABILITY_STATUS=PASS\n'
printf 'TIMESHIFT_BASELINE_STATUS=PASS\n'
printf 'POST_CORRECTION_SYNCHRONIZATION_STATUS=PASS\n'
printf 'RUNTIME_ENTRY_STATUS=PASS\n'
printf 'NEXT_PACKET=V231-C-RUNTIME-01\n'
printf 'TRANSCRIPT=%s\n' "$TRANSCRIPT"
