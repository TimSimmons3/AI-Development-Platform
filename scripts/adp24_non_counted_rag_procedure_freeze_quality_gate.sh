#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$HOME/Labs/AI-Development-Platform}"
BASELINE="${2:-}"

fail() {
  printf 'NON_COUNTED_RAG_PROCEDURE_FREEZE_QUALITY_GATE=FAIL\n'
  printf 'FAILED_CONTROL=%s\n' "$1"
  if [ "${2:-}" != "" ]; then
    printf 'FAILED_VALUE=%s\n' "$2"
  fi
  printf 'KNOWLEDGE_UPLOAD_AUTHORIZATION=HOLD\n'
  printf 'NON_COUNTED_RAG_EXECUTION_AUTHORIZATION=HOLD\n'
  printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
  exit 1
}

test "$BASELINE" != "" || fail BASELINE_ARGUMENT_REQUIRED
cd "$REPO"

expected_paths=(
  artifacts/Configuration/ADP-v2.4/model-import-reset-evidence-filename-map.json
  artifacts/Configuration/ADP-v2.4/non-counted-rag-dry-run-contract.json
  docs/Operations/ADP-v2.4-Isolated-Validation-Non-Counted-RAG-Dry-Run-Procedure.md
  docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md
  docs/Releases/ADP-v2.4-Non-Counted-RAG-Dry-Run-Procedure-Freeze-Record.md
  docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md
  scripts/adp24_non_counted_rag_procedure_freeze_quality_gate.sh
  scripts/adp24_validate_non_counted_rag_response.py
)

modified_paths=(
  artifacts/Configuration/ADP-v2.4/model-import-reset-evidence-filename-map.json
  docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md
)

new_paths=(
  artifacts/Configuration/ADP-v2.4/non-counted-rag-dry-run-contract.json
  docs/Operations/ADP-v2.4-Isolated-Validation-Non-Counted-RAG-Dry-Run-Procedure.md
  docs/Releases/ADP-v2.4-Non-Counted-RAG-Dry-Run-Procedure-Freeze-Record.md
  docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md
  scripts/adp24_non_counted_rag_procedure_freeze_quality_gate.sh
  scripts/adp24_validate_non_counted_rag_response.py
)

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

test "$(git rev-parse HEAD)" = "$BASELINE" || fail GIT_BASELINE "$(git rev-parse HEAD)"
test "$(git rev-parse main)" = "$BASELINE" || fail MAIN_BASELINE "$(git rev-parse main)"
test "$(git rev-parse origin/main)" = "$BASELINE" || fail ORIGIN_BASELINE "$(git rev-parse origin/main)"
printf 'GIT_BASELINE_STATUS=PASS\n'

mapfile -t actual_paths < <(git status --short --untracked-files=all | awk '{print $2}' | LC_ALL=C sort)
mapfile -t expected_sorted < <(printf '%s\n' "${expected_paths[@]}" | LC_ALL=C sort)

printf 'EXPECTED_PATHS=%s\n' "${#expected_sorted[@]}"
printf 'ACTUAL_PATHS=%s\n' "${#actual_paths[@]}"

test "${#actual_paths[@]}" -eq "${#expected_sorted[@]}" || fail EXACT_WRITE_SET_COUNT

for index in "${!expected_sorted[@]}"; do
  test "${actual_paths[$index]}" = "${expected_sorted[$index]}" || fail EXACT_WRITE_SET "${actual_paths[$index]}"
done

for path in "${modified_paths[@]}"; do
  status="$(git status --short --untracked-files=all -- "$path" | cut -c1-2)"
  test "$status" = " M" || fail MODIFIED_PATH_STATUS "$path:$status"
done

for path in "${new_paths[@]}"; do
  status="$(git status --short --untracked-files=all -- "$path" | cut -c1-2)"
  test "$status" = "??" || fail NEW_PATH_STATUS "$path:$status"
done

printf 'EXACT_WRITE_SET_STATUS=PASS\n'

python3 - "${expected_paths[@]}" <<'PY'
from pathlib import Path
import sys

for rel in sys.argv[1:]:
    path = Path(rel)
    data = path.read_bytes()
    assert data
    assert b"\r" not in data
    assert data.endswith(b"\n")
    assert not data.endswith(b"\n\n")
    text = data.decode("ascii")
    lines = text.splitlines()
    assert all(line == line.rstrip() for line in lines), rel
    assert "\t" not in text, rel
    if rel.endswith(".py"):
        assert lines[0] == "#!/usr/bin/env python3", rel
    elif rel.endswith(".sh"):
        assert lines[0] == "#!/usr/bin/env bash", rel
    elif rel.endswith(".md"):
        assert lines[0].startswith("# "), rel
    elif rel.endswith(".json"):
        assert lines[0] == "{", rel

print("TEXT_QUALITY_STATUS=PASS")
print("FIRST_LINE_VALIDATION_STATUS=PASS")
print("FINAL_NEWLINE_VALIDATION_STATUS=PASS")
PY

bash -n scripts/adp24_non_counted_rag_procedure_freeze_quality_gate.sh || fail QUALITY_GATE_SYNTAX
PYTHONPYCACHEPREFIX="$tmp/pycache" python3 -m py_compile scripts/adp24_validate_non_counted_rag_response.py || fail VALIDATOR_COMPILE
printf 'SCRIPT_SYNTAX_STATUS=PASS\n'

python3 -m json.tool artifacts/Configuration/ADP-v2.4/model-import-reset-evidence-filename-map.json >/dev/null || fail EVIDENCE_MAP_JSON
python3 -m json.tool artifacts/Configuration/ADP-v2.4/non-counted-rag-dry-run-contract.json >/dev/null || fail CONTRACT_JSON
printf 'JSON_VALIDATION_STATUS=PASS\n'

test "$(sha256sum artifacts/Test-Data/ADP-v2.4/adp24_bounded_multi_fact_source.md | awk '{print $1}')" = "18dc6a195e566da27dd4fe4be525d716a32dd0c753b6f1890c9c2ad7c3e12cfd" || fail SOURCE_HASH
test "$(sha256sum artifacts/Test-Data/ADP-v2.4/test-cases.json | awk '{print $1}')" = "a631a0dfb0823ea7e24179b0f0113f057c79476e8e14e091f2c98a8a554357d9" || fail TEST_CASES_HASH
test "$(sha256sum artifacts/Configuration/ADP-v2.4/approved-rag-template.txt | awk '{print $1}')" = "def3db3e05b1651aa33b921a03573074d8033ca5d2ce691446638e362ef92d96" || fail TEMPLATE_HASH
test "$(sha256sum artifacts/Configuration/ADP-v2.4/deterministic-model-discovery-record.json | awk '{print $1}')" = "ed81f8a23aec8676f6a55d8034222ac92487e38f56e0f1a05798482c244a146a" || fail MODEL_RECORD_HASH
printf 'FROZEN_INPUT_HASH_STATUS=PASS\n'

python3 - artifacts/Configuration/ADP-v2.4/non-counted-rag-dry-run-contract.json artifacts/Configuration/ADP-v2.4/model-import-reset-evidence-filename-map.json artifacts/Test-Data/ADP-v2.4/test-cases.json <<'PY'
import json
import sys
from pathlib import Path

contract = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
mapping = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
cases = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))

assert contract["procedure_freeze_starting_commit"] == "83e0103ab6daa67c822763769e9c685b7d38ac6b"
assert contract["procedure_freeze_tag"] == "adp-v2.4-non-counted-rag-dry-run-procedure-freeze"
assert contract["readiness_review"]["governing_standard"] == "docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md"
assert contract["readiness_review"]["independent_passes_required"] == 5
assert contract["readiness_review"]["status"] == "REQUIRED_BEFORE_SEPARATE_EXECUTION_AUTHORIZATION"
assert contract["status"] == "FROZEN_FOR_SINGLE_NON_COUNTED_DRY_RUN"
assert contract["execution"]["selected_case_id"] == "C"
assert contract["execution"]["chat_count"] == 1
assert contract["execution"]["prompt_submission_count"] == 1
assert contract["execution"]["rerun"] == "PROHIBITED_PENDING_REVIEW"
assert contract["collection"]["attachment_scope"] == "CHAT_ONLY"
assert contract["collection"]["model_level_attachment"] == "PROHIBITED"
assert contract["collection"]["source_count"] == 1
assert contract["model"]["id"] == "llama-32-3b-rag-deterministic-test"
assert contract["model"]["base_model"] == "llama3.2:3b"
assert contract["model"]["temperature"] == 0
assert contract["model"]["seed"] == 42
assert contract["model"]["associations_required"] == "ABSENT"

selected = contract["selected_case"]
assert selected["id"] == "C"
assert selected["prompt"] == "State the verification color and review window for AURORA-24-KITE."
assert selected["expected_factual_answer"] == (
    "The verification color for AURORA-24-KITE is amber, "
    "and the review window is thirty-six hours."
)
assert selected["source_id"] == "AURORA-24-KITE"
assert selected["allowed_citation_classifications"] == [
    "ABSENT",
    "NUMERIC_BRACKET",
    "SOURCE_ID_BRACKET",
]

case_rows = {row["id"]: row for row in cases["cases"]}
assert case_rows["C"]["prompt"] == selected["prompt"]
assert case_rows["C"]["provisional_expected"] == selected["expected_factual_answer"]
assert cases["status"] == "PROVISIONAL_NOT_AUTHORIZED_FOR_COUNTED_USE"

map_rows = {row["order"]: row for row in mapping["files"]}
contract_rows = {row["order"]: row for row in contract["evidence"]}
assert mapping["schema_version"] == "1.1"
assert set(contract_rows) == set(range(12, 18))

for order in range(12, 18):
    assert map_rows[order]["name"] == contract_rows[order]["name"]
    assert map_rows[order]["purpose"] == contract_rows[order]["purpose"]
    assert map_rows[order]["required"] is True
    assert contract_rows[order]["required"] is True

print("CONTRACT_SEMANTIC_VALIDATION=PASS")
print("SELECTED_CASE_BINDING=PASS")
print("EVIDENCE_CONTRACT_BINDING=PASS")
PY

contract="artifacts/Configuration/ADP-v2.4/non-counted-rag-dry-run-contract.json"
validator="scripts/adp24_validate_non_counted_rag_response.py"
expected="The verification color for AURORA-24-KITE is amber, and the review window is thirty-six hours."

printf '%s\n' "$expected" > "$tmp/raw-absent.txt"
printf '%s [1]\n' "$expected" > "$tmp/raw-numeric.txt"
printf '%s [AURORA-24-KITE]\n' "$expected" > "$tmp/raw-source-id.txt"
printf '%s Additional commentary.\n' "$expected" > "$tmp/raw-extra.txt"
printf '%s\n' "The verification color for AURORA-24-KITE is blue." > "$tmp/raw-wrong.txt"

python3 "$validator" --contract "$contract" --raw "$tmp/raw-absent.txt" --normalized-output "$tmp/absent.normalized.txt" > "$tmp/absent.log"
grep -Fq 'NON_COUNTED_RESPONSE_VALIDATION=PASS' "$tmp/absent.log" || fail ABSENT_VALIDATOR
grep -Fq 'CITATION_CLASSIFICATION=ABSENT' "$tmp/absent.log" || fail ABSENT_CLASSIFICATION

python3 "$validator" --contract "$contract" --raw "$tmp/raw-numeric.txt" --normalized-output "$tmp/numeric.normalized.txt" > "$tmp/numeric.log"
grep -Fq 'CITATION_CLASSIFICATION=NUMERIC_BRACKET' "$tmp/numeric.log" || fail NUMERIC_CLASSIFICATION

python3 "$validator" --contract "$contract" --raw "$tmp/raw-source-id.txt" --normalized-output "$tmp/source-id.normalized.txt" > "$tmp/source-id.log"
grep -Fq 'CITATION_CLASSIFICATION=SOURCE_ID_BRACKET' "$tmp/source-id.log" || fail SOURCE_ID_CLASSIFICATION

if python3 "$validator" --contract "$contract" --raw "$tmp/raw-extra.txt" --normalized-output "$tmp/extra.normalized.txt" > "$tmp/extra.log" 2>&1; then
  fail UNSUPPORTED_RESPONSE_ACCEPTED
fi
grep -Fq 'FAILED_CONTROL=UNSUPPORTED_RESPONSE_SHAPE' "$tmp/extra.log" || fail UNSUPPORTED_RESPONSE_REPORT

if python3 "$validator" --contract "$contract" --raw "$tmp/raw-wrong.txt" --normalized-output "$tmp/wrong.normalized.txt" > "$tmp/wrong.log" 2>&1; then
  fail WRONG_FACT_ACCEPTED
fi
grep -Fq 'FAILED_CONTROL=FACTUAL_CONTENT_MISMATCH' "$tmp/wrong.log" || fail WRONG_FACT_REPORT

if python3 "$validator" --contract "$contract" --raw "$tmp/raw-absent.txt" --normalized-output "$tmp/absent.normalized.txt" > "$tmp/collision.log" 2>&1; then
  fail OUTPUT_COLLISION_ACCEPTED
fi
grep -Fq 'FAILED_CONTROL=NORMALIZED_OUTPUT_EXISTS' "$tmp/collision.log" || fail OUTPUT_COLLISION_REPORT

test "$(stat -c '%a' "$tmp/absent.normalized.txt")" = "600" || fail NORMALIZED_OUTPUT_MODE
printf 'CLASSIFIER_POSITIVE_FIXTURES=PASS\n'
printf 'CLASSIFIER_NEGATIVE_FIXTURES=PASS\n'
printf 'CLASSIFIER_OUTPUT_PROTECTION=PASS\n'

grep -Fq 'GUIDE_STATUS=NON_COUNTED_RAG_PROCEDURE_DEFINED_EXECUTION_HELD' docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md || fail GUIDE_STATUS
grep -Fq 'NON_COUNTED_RAG_CONTRACT=artifacts/Configuration/ADP-v2.4/non-counted-rag-dry-run-contract.json' docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md || fail GUIDE_CONTRACT
grep -Fq 'NON_COUNTED_RAG_PROCEDURE=docs/Operations/ADP-v2.4-Isolated-Validation-Non-Counted-RAG-Dry-Run-Procedure.md' docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md || fail GUIDE_PROCEDURE
grep -Fq 'PROCEDURE_STATUS=FROZEN_FOR_SINGLE_NON_COUNTED_DRY_RUN_NOT_YET_EXECUTED' docs/Operations/ADP-v2.4-Isolated-Validation-Non-Counted-RAG-Dry-Run-Procedure.md || fail PROCEDURE_STATUS
grep -Fq 'SELECTED_NON_COUNTED_CASE=C' docs/Operations/ADP-v2.4-Isolated-Validation-Non-Counted-RAG-Dry-Run-Procedure.md || fail PROCEDURE_CASE
grep -Fq 'FREEZE_RECORD_STATUS=PROCEDURE_FREEZE_DEFINED_EXECUTION_NOT_AUTHORIZED' docs/Releases/ADP-v2.4-Non-Counted-RAG-Dry-Run-Procedure-Freeze-Record.md || fail RECORD_STATUS
grep -Fq 'The correction is a direct Git-native procedure-freeze change.' docs/Releases/ADP-v2.4-Non-Counted-RAG-Dry-Run-Procedure-Freeze-Record.md || fail GIT_NATIVE_TRACEABILITY
grep -Fq 'FIVE_PASS_READINESS_STANDARD=docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md' docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md || fail GUIDE_READINESS_STANDARD
grep -Fq '## 6. Five-Pass Readiness Requirement' docs/Operations/ADP-v2.4-Isolated-Validation-Non-Counted-RAG-Dry-Run-Procedure.md || fail PROCEDURE_READINESS_REQUIREMENT
grep -Fq 'FIVE_PASS_READINESS_REVIEW=REQUIRED_BEFORE_EXECUTION' docs/Releases/ADP-v2.4-Non-Counted-RAG-Dry-Run-Procedure-Freeze-Record.md || fail RECORD_READINESS_REQUIREMENT
grep -Fq '## 3. Mandatory Five Passes' docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md || fail READINESS_STANDARD_PASSES
grep -Fq 'READINESS_PASS_1_SCOPE_BASELINE=PASS' docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md || fail READINESS_PASS_1
grep -Fq 'READINESS_PASS_2_TECHNICAL_STRUCTURE=PASS' docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md || fail READINESS_PASS_2
grep -Fq 'READINESS_PASS_3_SEMANTIC_TRACEABILITY=PASS' docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md || fail READINESS_PASS_3
grep -Fq 'READINESS_PASS_4_FAILURE_RECOVERY=PASS' docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md || fail READINESS_PASS_4
grep -Fq 'READINESS_PASS_5_OPERATIONAL_RESIDUAL_RISK=PASS' docs/Standards/ADP-Five-Pass-Readiness-Review-Standard.md || fail READINESS_PASS_5
grep -Fq 'Any correction restarts the review at Pass 1.' docs/Operations/ADP-v2.4-Isolated-Validation-Non-Counted-RAG-Dry-Run-Procedure.md || fail READINESS_RESET_RULE

python3 - <<'PY'
from pathlib import Path

paths = [
    Path("artifacts/Configuration/ADP-v2.4/non-counted-rag-dry-run-contract.json"),
    Path("docs/Operations/ADP-v2.4-Isolated-Validation-Non-Counted-RAG-Dry-Run-Procedure.md"),
    Path("docs/Operations/ADP-v2.4-Isolated-Validation-Runtime-Operator-Guide.md"),
    Path("docs/Releases/ADP-v2.4-Non-Counted-RAG-Dry-Run-Procedure-Freeze-Record.md"),
]

forbidden = (
    "CANDIDATE_NOT_PROMOTED",
    "HOLD_PENDING_PROMOTION",
    "HOLD_PENDING_DRY_CHECK",
    "PLANNED_BRANCH=",
    "PLANNED_TAG=",
    "PLANNED_PROCEDURE_FREEZE_TAG=",
    "PLANNED_NON_COUNTED_RAG_PROCEDURE_FREEZE_TAG=",
)

for path in paths:
    text = path.read_text(encoding="ascii")
    for token in forbidden:
        assert token not in text, (path, token)

print("PROMOTION_DURABLE_STATUS=PASS")
PY

printf 'FIVE_PASS_STANDARD_BINDING=PASS\n'
printf 'SEMANTIC_TRACEABILITY_STATUS=PASS\n'

grep -Fq 'set -euo pipefail' scripts/adp24_non_counted_rag_procedure_freeze_quality_gate.sh || fail STRICT_SHELL_MODE
grep -Fq 'test "$BASELINE" != "" || fail BASELINE_ARGUMENT_REQUIRED' scripts/adp24_non_counted_rag_procedure_freeze_quality_gate.sh || fail BASELINE_FAILURE_PROPAGATION
grep -Fq 'if python3 "$validator"' scripts/adp24_non_counted_rag_procedure_freeze_quality_gate.sh || fail NEGATIVE_FIXTURE_FAILURE_PROPAGATION
printf 'FAILURE_PROPAGATION_STATUS=PASS\n'

git diff --check || fail TRACKED_DIFF_CHECK
printf 'TRACKED_DIFF_CHECK_STATUS=PASS\n'

printf 'NON_COUNTED_RAG_PROCEDURE_FREEZE_QUALITY_GATE=PASS\n'
printf 'PROCEDURE_FREEZE_IMPLEMENTATION=PASS\n'
printf 'RUNTIME_MUTATION=NONE\n'
printf 'KNOWLEDGE_UPLOAD_AUTHORIZATION=HOLD_PENDING_SEPARATE_AUTHORIZATION\n'
printf 'NON_COUNTED_RAG_EXECUTION_AUTHORIZATION=HOLD_PENDING_SEPARATE_AUTHORIZATION\n'
printf 'COUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
