#!/usr/bin/env python3
"""Validate exact project-owner authorization for exception-bearing pull requests."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

APPROVAL_PREFIX = "APPROVE SMT MANDATORY ASSURANCE EXCEPTION"
HEAD_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def load_json_strict(path: Path) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


def normalize_comments(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ValueError("comments JSON must be a list")
    flattened: list[Any] = []
    for item in value:
        if isinstance(item, list):
            flattened.extend(item)
        else:
            flattened.append(item)
    comments: list[dict[str, Any]] = []
    for index, item in enumerate(flattened):
        if not isinstance(item, dict):
            raise ValueError(f"comment entry {index} must be an object")
        comments.append(item)
    return comments


def canonical_exception_records(report: dict[str, Any]) -> list[str]:
    records = report.get("exception_records")
    count = report.get("exception_record_count")
    if not isinstance(records, list) or any(not isinstance(item, str) or not item for item in records):
        raise ValueError("report exception_records must be a list of non-empty strings")
    if not isinstance(count, int) or count != len(records):
        raise ValueError("report exception_record_count does not match exception_records")
    if len(set(records)) != len(records):
        raise ValueError("report exception_records contains duplicates")
    canonical = sorted(records)
    if records != canonical:
        raise ValueError("report exception_records must be sorted")
    if any("," in item or "\n" in item or "\r" in item for item in records):
        raise ValueError("exception record paths contain prohibited delimiters")
    return records


def expected_approval(pr_number: int, head_sha: str, records: list[str]) -> str:
    if pr_number < 1:
        raise ValueError("PR number must be positive")
    if not HEAD_SHA_PATTERN.fullmatch(head_sha):
        raise ValueError("head SHA must be 40 lowercase hexadecimal characters")
    if not records:
        raise ValueError("at least one exception record is required")
    return (
        f"{APPROVAL_PREFIX} PR={pr_number} HEAD={head_sha} "
        f"EXCEPTIONS={','.join(records)}"
    )


def validate_approval(
    report: dict[str, Any],
    comments_value: Any,
    owner_login: str,
    pr_number: int,
    head_sha: str,
) -> dict[str, Any]:
    violations: list[str] = []
    if report.get("status") != "PASS":
        violations.append("invariant validation report status is not PASS")

    try:
        records = canonical_exception_records(report)
    except ValueError as exc:
        violations.append(str(exc))
        records = []

    result: dict[str, Any] = {
        "record_type": "SMT_OWNER_EXCEPTION_APPROVAL_VALIDATION",
        "schema_version": "1.0",
        "owner_login": owner_login,
        "pr_number": pr_number,
        "head_sha": head_sha,
        "exception_records": records,
        "approval_required": bool(records),
        "expected_approval": None,
        "matching_comment_count": 0,
        "violations": violations,
    }

    if not owner_login or not re.fullmatch(r"[A-Za-z0-9-]+", owner_login):
        violations.append("owner login is invalid")

    if records:
        try:
            expected = expected_approval(pr_number, head_sha, records)
        except ValueError as exc:
            violations.append(str(exc))
        else:
            result["expected_approval"] = expected
            try:
                comments = normalize_comments(comments_value)
            except ValueError as exc:
                violations.append(str(exc))
            else:
                matches = 0
                for comment in comments:
                    user = comment.get("user")
                    login = user.get("login") if isinstance(user, dict) else None
                    body = comment.get("body")
                    if login == owner_login and body == expected:
                        matches += 1
                result["matching_comment_count"] = matches
                if matches != 1:
                    violations.append(
                        f"requires exactly one current exact owner approval comment; observed {matches}"
                    )

    result["status"] = "PASS" if not violations else "FAIL"
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--comments", required=True)
    parser.add_argument("--owner-login", required=True)
    parser.add_argument("--pr-number", required=True, type=int)
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    report = load_json_strict(Path(args.report))
    if not isinstance(report, dict):
        raise ValueError("report JSON root must be an object")
    comments = load_json_strict(Path(args.comments))
    result = validate_approval(
        report=report,
        comments_value=comments,
        owner_login=args.owner_login,
        pr_number=args.pr_number,
        head_sha=args.head_sha,
    )
    output = Path(args.output)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
