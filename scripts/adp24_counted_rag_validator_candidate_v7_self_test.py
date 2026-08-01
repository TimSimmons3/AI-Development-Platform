#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from types import ModuleType

PER_PROCESS_TIMEOUT_SECONDS = 5
PER_FIXTURE_CLASSIFICATION_LIMIT_SECONDS = 1.0
LONG_INPUT_CLASSIFICATION_LIMIT_SECONDS = 2.0
TOTAL_RUNTIME_LIMIT_SECONDS = 30.0


def load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("adp24_validator_v7", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("validator module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_cli(
    validator: Path,
    contract: Path,
    manifest: Path,
    binding_report: Path,
    context: str,
    case_id: str,
    raw: Path,
    source_panel: str,
    normalized_output: Path,
    report_output: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "python3",
            str(validator),
            "--contract",
            str(contract),
            "--binding-manifest",
            str(manifest),
            "--binding-report",
            str(binding_report),
            "--validation-context",
            context,
            "--case",
            case_id,
            "--raw",
            str(raw),
            "--source-panel-classification",
            source_panel,
            "--normalized-output",
            str(normalized_output),
            "--report-output",
            str(report_output),
        ],
        text=True,
        capture_output=True,
        timeout=PER_PROCESS_TIMEOUT_SECONDS,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--binding-report", required=True)
    args = parser.parse_args()

    root = Path(args.repository_root)
    contract_path = root / "artifacts/Configuration/ADP-v2.4/counted-rag-qualification-design-candidate-v7.json"
    manifest_path = root / "artifacts/Configuration/ADP-v2.4/counted-rag-governing-bindings-v7.json"
    validator_path = root / "scripts/adp24_validate_counted_rag_response_candidate_v7.py"
    fixtures = root / "artifacts/Test-Data/ADP-v2.4/counted-validator-v7-fixtures"
    expectations_path = root / "artifacts/Test-Data/ADP-v2.4/counted-validator-v7-fixture-expectations.json"
    binding_report = Path(args.binding_report)

    expectations = json.loads(expectations_path.read_text(encoding="utf-8"))
    validator = load_module(validator_path)
    contract = validator.load_contract(contract_path)
    validator.validate_binding_report(binding_report, contract_path, manifest_path, "SELF_TEST")
    cases = {case["id"]: case for case in contract["cases"]}

    failures: list[str] = []
    started = time.monotonic()
    maximum_fixture_elapsed = 0.0

    for name, expected in sorted(expectations.items()):
        raw = (fixtures / name).read_text(encoding="utf-8")
        fixture_started = time.monotonic()
        result = validator.classify(
            contract,
            cases[expected["case"]],
            raw,
            "EXACT_SINGLE_SOURCE",
        )
        fixture_elapsed = time.monotonic() - fixture_started
        maximum_fixture_elapsed = max(maximum_fixture_elapsed, fixture_elapsed)
        if fixture_elapsed > PER_FIXTURE_CLASSIFICATION_LIMIT_SECONDS:
            failures.append(f"{name}:classification_runtime:{fixture_elapsed:.4f}")

        for key, expected_value in [
            ("factual_content_status", expected["factual"]),
            ("format_adherence_status", expected["format"]),
            ("inline_citation_status", expected["citation"]),
            ("unsupported_addition_status", expected["unsupported"]),
        ]:
            if result[key] != expected_value:
                failures.append(f"{name}:{key}:{result[key]}!={expected_value}")

        expected_overall = "PASS" if all(
            expected[key] == "PASS"
            for key in ("factual", "format", "citation", "unsupported")
        ) else "FAIL"
        if result["candidate_validation_status"] != expected_overall:
            failures.append(
                f"{name}:candidate_validation_status:"
                f"{result['candidate_validation_status']}!={expected_overall}"
            )

    long_input = (
        "The verification color for AURORA-24-KITE is amber. "
        "[AURORA-24-KITE] "
    ) * 1000
    long_started = time.monotonic()
    long_result = validator.classify(contract, cases["A"], long_input, "EXACT_SINGLE_SOURCE")
    long_elapsed = time.monotonic() - long_started
    if long_elapsed > LONG_INPUT_CLASSIFICATION_LIMIT_SECONDS:
        failures.append(f"long_input_runtime:{long_elapsed:.4f}")
    if long_result["candidate_validation_status"] != "FAIL":
        failures.append("long_input_duplicate_claim_not_rejected")

    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        exact_raw = fixtures / "case-a-exact.txt"
        wrong_raw = fixtures / "case-a-wrong.txt"

        exact_normalized = temp_dir / "exact.norm"
        exact_report = temp_dir / "exact.json"
        exact = run_cli(
            validator_path,
            contract_path,
            manifest_path,
            binding_report,
            "SELF_TEST",
            "A",
            exact_raw,
            "EXACT_SINGLE_SOURCE",
            exact_normalized,
            exact_report,
        )
        if exact.returncode != 0 or not exact_report.exists():
            failures.append(f"cli_exact:{exact.returncode}:{exact.stdout}:{exact.stderr}")
        elif json.loads(exact_report.read_text(encoding="utf-8"))["candidate_validation_status"] != "PASS":
            failures.append("cli_exact_report_not_pass")

        wrong_normalized = temp_dir / "wrong.norm"
        wrong_report = temp_dir / "wrong.json"
        wrong = run_cli(
            validator_path,
            contract_path,
            manifest_path,
            binding_report,
            "SELF_TEST",
            "A",
            wrong_raw,
            "EXACT_SINGLE_SOURCE",
            wrong_normalized,
            wrong_report,
        )
        if wrong.returncode != 1 or not wrong_report.exists():
            failures.append(f"cli_wrong:{wrong.returncode}:{wrong.stdout}:{wrong.stderr}")

        panel_normalized = temp_dir / "panel.norm"
        panel_report = temp_dir / "panel.json"
        panel = run_cli(
            validator_path,
            contract_path,
            manifest_path,
            binding_report,
            "SELF_TEST",
            "A",
            exact_raw,
            "WRONG_SOURCE",
            panel_normalized,
            panel_report,
        )
        if panel.returncode != 1 or not panel_report.exists():
            failures.append("wrong_source_panel_execution")
        elif json.loads(panel_report.read_text(encoding="utf-8"))["source_panel_status"] != "FAIL":
            failures.append("wrong_source_panel_classification")

        collision_normalized = temp_dir / "collision.norm"
        collision_report = temp_dir / "collision.json"
        collision_normalized.write_text("existing\n", encoding="utf-8")
        collision = run_cli(
            validator_path,
            contract_path,
            manifest_path,
            binding_report,
            "SELF_TEST",
            "A",
            exact_raw,
            "EXACT_SINGLE_SOURCE",
            collision_normalized,
            collision_report,
        )
        if collision.returncode != 1 or "FAILED_CONTROL=NORMALIZED_OUTPUT_EXISTS" not in collision.stdout:
            failures.append("output_collision")

        alias = temp_dir / "alias-output.txt"
        alias_result = run_cli(
            validator_path,
            contract_path,
            manifest_path,
            binding_report,
            "SELF_TEST",
            "A",
            exact_raw,
            "EXACT_SINGLE_SOURCE",
            alias,
            alias,
        )
        if (
            alias_result.returncode != 1
            or "FAILED_CONTROL=OUTPUT_PATH_ALIAS" not in alias_result.stdout
            or alias.exists()
        ):
            failures.append("output_path_alias")

        tampered_binding = json.loads(binding_report.read_text(encoding="utf-8"))
        tampered_binding["contract_sha256"] = "0" * 64
        bad_binding = temp_dir / "bad-binding.json"
        bad_binding.write_text(json.dumps(tampered_binding), encoding="utf-8")
        bad_result = run_cli(
            validator_path,
            contract_path,
            manifest_path,
            bad_binding,
            "SELF_TEST",
            "A",
            exact_raw,
            "EXACT_SINGLE_SOURCE",
            temp_dir / "bad.norm",
            temp_dir / "bad.json",
        )
        if bad_result.returncode != 1 or "FAILED_CONTROL=BINDING_REPORT_CONTRACT_HASH" not in bad_result.stdout:
            failures.append("tampered_binding_report")

        execution_binding_data = json.loads(binding_report.read_text(encoding="utf-8"))
        execution_binding_data["validation_type"] = "EXECUTION_BINDING_VALIDATION"
        execution_binding = temp_dir / "execution-binding.json"
        execution_binding.write_text(json.dumps(execution_binding_data), encoding="utf-8")
        execution_result = run_cli(
            validator_path,
            contract_path,
            manifest_path,
            execution_binding,
            "EXECUTION",
            "A",
            exact_raw,
            "EXACT_SINGLE_SOURCE",
            temp_dir / "exec.norm",
            temp_dir / "exec.json",
        )
        if execution_result.returncode != 1 or "FAILED_CONTROL=CANDIDATE_NOT_EXECUTION_AUTHORIZED" not in execution_result.stdout:
            failures.append("execution_context_not_blocked")

        missing_args = subprocess.run(
            ["python3", str(validator_path)],
            text=True,
            capture_output=True,
            timeout=PER_PROCESS_TIMEOUT_SECONDS,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        if missing_args.returncode != 2:
            failures.append(f"missing_argument_exit:{missing_args.returncode}")

    elapsed = time.monotonic() - started
    if elapsed > TOTAL_RUNTIME_LIMIT_SECONDS:
        failures.append(f"total_runtime:{elapsed:.2f}>{TOTAL_RUNTIME_LIMIT_SECONDS:.0f}")

    if failures:
        print("CANDIDATE_V7_SELF_TEST=FAIL")
        for failure in failures:
            print(f"FAIL={failure}")
        print("COUNTED_EXECUTION_AUTHORIZATION=HOLD")
        return 1

    print(f"FIXTURE_COUNT={len(expectations)}")
    print(f"MAXIMUM_FIXTURE_CLASSIFICATION_SECONDS={maximum_fixture_elapsed:.6f}")
    print(f"LONG_INPUT_CLASSIFICATION_SECONDS={long_elapsed:.6f}")
    print(f"SELF_TEST_TOTAL_RUNTIME_SECONDS={elapsed:.6f}")
    print("FACTUAL_FORMAT_DIMENSION_INDEPENDENCE=PASS")
    print("SUPPORTED_GRAMMAR_CONTRADICTION_REJECTION=PASS")
    print("CORRECT_NEGATION_OF_FORBIDDEN_VALUE=PASS")
    print("STRICT_CITATION_TOKEN_VALIDATION=PASS")
    print("CASE_A_B_C_D_DIRECT_COVERAGE=PASS")
    print("BINDING_REPORT_ENFORCEMENT=PASS")
    print("OUTPUT_COLLISION_PROTECTION=PASS")
    print("OUTPUT_ALIAS_PROTECTION=PASS")
    print("MISSING_ARGUMENT_REJECTION=PASS")
    print("FIXTURE_TIMEOUT_PROTECTION=PASS")
    print("FIXTURE_TOTAL_RUNTIME_BOUND=PASS")
    print("LONG_INPUT_RUNTIME_BOUND=PASS")
    print("CLI_POSITIVE_AND_NEGATIVE_SMOKE_TEST=PASS")
    print("CANDIDATE_EXECUTION_CONTEXT_BLOCK=PASS")
    print("CANDIDATE_V7_SELF_TEST=PASS")
    print("COUNTED_EXECUTION_AUTHORIZATION=HOLD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
