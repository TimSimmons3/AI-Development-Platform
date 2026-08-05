#!/usr/bin/env python3
"""Validate mandatory one-pass assurance invariants in changed governance Markdown."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

DEFAULT_POLICY = "config/mandatory-assurance-invariant-policy.json"
DEFAULT_REPORT = "mandatory-assurance-invariant-report.json"
PLACEHOLDER_MARKERS = ("<", ">", "TBD", "TODO", "PLACEHOLDER")


def load_json_strict(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    if not isinstance(data, dict):
        raise ValueError("policy root must be an object")
    return data


def run_git(repo_root: Path, args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def changed_files(repo_root: Path, base_ref: str) -> list[str]:
    output = run_git(repo_root, ["diff", "--name-only", "--diff-filter=ACMR", f"{base_ref}...HEAD"])
    return [line.strip() for line in output.splitlines() if line.strip()]


def normalized_relative(repo_root: Path, value: str) -> str:
    path = Path(value)
    if path.is_absolute():
        try:
            path = path.resolve(strict=False).relative_to(repo_root.resolve(strict=True))
        except ValueError as exc:
            raise ValueError(f"path outside repository: {value}") from exc
    pure = PurePosixPath(path.as_posix())
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"unsafe repository path: {value}")
    return pure.as_posix()


def is_governed(path: str, policy: dict[str, Any]) -> bool:
    lower = path.lower()
    if not lower.endswith(".md"):
        return False
    roots = policy.get("governed_markdown_roots", [])
    if any(path.startswith(str(root)) for root in roots):
        return True
    name = PurePosixPath(path).name.lower()
    return any(str(keyword).lower() in name for keyword in policy.get("governed_filename_keywords", []))


def parse_assignments(text: str) -> dict[str, list[str]]:
    values: dict[str, list[str]] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = re.fullmatch(r"([A-Z][A-Z0-9_]*)=(.*)", line)
        if match:
            values.setdefault(match.group(1), []).append(match.group(2))
    return values


def one_value(assignments: dict[str, list[str]], key: str) -> str | None:
    values = assignments.get(key, [])
    if len(values) != 1:
        return None
    return values[0]


def has_placeholder(value: str) -> bool:
    upper = value.upper()
    return any(marker in upper for marker in PLACEHOLDER_MARKERS)


def validate_exception_record(path: str, text: str, policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    assignments = parse_assignments(text)
    exception = policy["exception"]

    for key, expected in exception["required_values"].items():
        values = assignments.get(key, [])
        if values != [expected]:
            errors.append(f"{path}: requires exactly `{key}={expected}`")

    for key in exception["required_nonempty_fields"]:
        value = one_value(assignments, key)
        if value is None or not value.strip():
            errors.append(f"{path}: requires one non-empty `{key}`")
        elif has_placeholder(value):
            errors.append(f"{path}: `{key}` contains a placeholder")

    checks = {
        "APPROVAL_TEXT_SHA256": exception["approval_hash_pattern"],
        "ARTIFACT_SHA256_SET": exception["artifact_hash_set_pattern"],
        "APPROVED_UTC": exception["utc_pattern"],
        "EXPIRATION_UTC": exception["utc_pattern"],
    }
    for key, pattern in checks.items():
        value = one_value(assignments, key)
        if value and not re.fullmatch(pattern, value):
            errors.append(f"{path}: `{key}` does not match required format")

    return errors


def validate_governed_document(
    repo_root: Path,
    path: str,
    text: str,
    policy: dict[str, Any],
) -> tuple[list[str], str | None]:
    errors: list[str] = []
    assignments = parse_assignments(text)
    required = policy["required_block"]
    exception_status = one_value(assignments, "EXCEPTION_STATUS")
    order = policy.get("required_block_order", list(required))
    block_values = dict(required)
    if exception_status == "APPROVED":
        block_values["EXCEPTION_STATUS"] = "APPROVED"
    canonical_block = "\n".join(f"{key}={block_values[key]}" for key in order)
    if text.count(canonical_block) != 1:
        errors.append(f"{path}: canonical invariant block must appear exactly once in required order")

    for key, expected in required.items():
        if key == "EXCEPTION_STATUS" and exception_status == "APPROVED":
            continue
        values = assignments.get(key, [])
        if values != [expected]:
            errors.append(f"{path}: requires exactly `{key}={expected}`")

    exception_record: str | None = None
    if exception_status == "APPROVED":
        record_values = assignments.get("EXCEPTION_RECORD", [])
        if len(record_values) != 1:
            errors.append(f"{path}: approved exception requires exactly one `EXCEPTION_RECORD`")
        else:
            try:
                exception_record = normalized_relative(repo_root, record_values[0])
            except ValueError as exc:
                errors.append(f"{path}: {exc}")
            else:
                expected_dir = str(policy["exception"]["directory"])
                if not exception_record.startswith(expected_dir) or not exception_record.endswith(".md"):
                    errors.append(f"{path}: exception record must be Markdown under `{expected_dir}`")
                record_path = repo_root / exception_record
                if not record_path.is_file() or record_path.is_symlink():
                    errors.append(f"{path}: exception record is missing or not a regular file: {exception_record}")
                else:
                    record_text = record_path.read_text(encoding="utf-8")
                    errors.extend(validate_exception_record(exception_record, record_text, policy))
    elif exception_status != required["EXCEPTION_STATUS"]:
        errors.append(f"{path}: `EXCEPTION_STATUS` must be NOT_GRANTED or APPROVED")

    return errors, exception_record


def validate_files(repo_root: Path, paths: list[str], policy: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    governed: list[str] = []
    exception_records: set[str] = set()
    file_records: list[dict[str, Any]] = []

    for raw_path in sorted(set(paths)):
        try:
            path = normalized_relative(repo_root, raw_path)
        except ValueError as exc:
            violations.append(str(exc))
            continue
        full = repo_root / path
        if not full.exists():
            violations.append(f"{path}: changed path does not exist")
            continue
        if full.is_symlink() or not full.is_file():
            violations.append(f"{path}: must be a regular non-symlink file")
            continue
        if not is_governed(path, policy):
            continue
        governed.append(path)
        data = full.read_bytes()
        if b"\r" in data:
            violations.append(f"{path}: contains CR characters")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            violations.append(f"{path}: is not valid UTF-8")
            continue
        if any(line.rstrip(" \t") != line for line in text.splitlines()):
            violations.append(f"{path}: contains trailing whitespace")

        exception_dir = str(policy["exception"]["directory"])
        is_exception_record = path.startswith(exception_dir) and PurePosixPath(path).name.lower() != "readme.md"
        if is_exception_record:
            errors = validate_exception_record(path, text, policy)
            exception_records.add(path)
        else:
            errors, record = validate_governed_document(repo_root, path, text, policy)
            if record:
                exception_records.add(record)
        violations.extend(errors)
        file_records.append(
            {
                "path": path,
                "sha256": hashlib.sha256(data).hexdigest(),
                "status": "PASS" if not errors else "FAIL",
            }
        )

    return {
        "record_type": "SMT_MANDATORY_ASSURANCE_INVARIANT_VALIDATION",
        "schema_version": "1.0",
        "status": "PASS" if not violations else "FAIL",
        "governed_file_count": len(governed),
        "governed_files": governed,
        "exception_record_count": len(exception_records),
        "exception_records": sorted(exception_records),
        "violations": violations,
        "files": file_records,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--policy", default=DEFAULT_POLICY)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--base-ref")
    source.add_argument("--files", nargs="+")
    parser.add_argument("--report", default=DEFAULT_REPORT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    repo_root = Path(args.repo_root).resolve(strict=True)
    policy_path = Path(args.policy)
    if not policy_path.is_absolute():
        policy_path = repo_root / policy_path
    policy = load_json_strict(policy_path)
    paths = changed_files(repo_root, args.base_ref) if args.base_ref else list(args.files)
    report = validate_files(repo_root, paths, policy)
    report_path = Path(args.report)
    if not report_path.is_absolute():
        report_path = repo_root / report_path
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
