#!/usr/bin/env python3
"""Validate exact project-owner authorization for exception-bearing pull requests."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

APPROVAL_PREFIX = "APPROVE SMT MANDATORY ASSURANCE EXCEPTION"
HEAD_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
UTC_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
MAX_JSON_BYTES = 8 * 1024 * 1024
ARTIFACT_MANIFEST_ROOT = "docs/Exceptions/Artifacts/"
ARTIFACT_MANIFEST_RECORD_TYPE = "SMT_MANDATORY_ASSURANCE_EXCEPTION_ARTIFACT_MANIFEST"
ARTIFACT_MANIFEST_FIELDS = frozenset({"record_type", "schema_version", "artifacts"})
ARTIFACT_ENTRY_FIELDS = {
    "REPO_PATH": frozenset({"type", "path", "sha256"}),
    "EXTERNAL_ARTIFACT": frozenset({"type", "artifact_id", "sha256"}),
    "EXTERNAL_INCIDENT": frozenset({"type", "incident_id", "sha256"}),
}
APPROVAL_BASIS_FIELDS = (
    "EXCEPTION_STATUS",
    "APPROVED_BY",
    "APPROVED_GITHUB_LOGIN",
    "APPROVED_UTC",
    "CONTROL_IDS",
    "SCOPE",
    "RATIONALE",
    "RESIDUAL_RISK",
    "COMPENSATING_CONTROLS",
    "EXPIRATION_UTC",
    "ARTIFACT_MANIFEST",
    "ARTIFACT_SHA256_SET",
)
EXCEPTION_ASSIGNMENT_FIELDS = frozenset((*APPROVAL_BASIS_FIELDS, "APPROVAL_TEXT_SHA256"))


def load_json_strict(path: Path, max_bytes: int = MAX_JSON_BYTES) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    try:
        size = path.stat().st_size
    except OSError as exc:
        raise ValueError(f"cannot stat JSON input: {type(exc).__name__}: {exc}") from exc
    if size > max_bytes:
        raise ValueError(f"JSON input size {size} exceeds limit {max_bytes}")
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ValueError(f"cannot read JSON input: {type(exc).__name__}: {exc}") from exc
    if len(data) > max_bytes:
        raise ValueError(f"JSON input exceeds limit {max_bytes}")
    try:
        text = data.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise ValueError("JSON input is not valid UTF-8") from exc
    return json.loads(text, object_pairs_hook=reject_duplicates)


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
    return f"{APPROVAL_PREFIX} PR={pr_number} HEAD={head_sha} EXCEPTIONS={','.join(records)}"


def parse_assignments(text: str) -> dict[str, list[str]]:
    values: dict[str, list[str]] = {}
    for raw in text.splitlines():
        match = re.fullmatch(r"([A-Z][A-Z0-9_]*)=(.*)", raw.strip())
        if match:
            values.setdefault(match.group(1), []).append(match.group(2))
    return values


def one_value(assignments: dict[str, list[str]], key: str) -> str | None:
    values = assignments.get(key, [])
    return values[0] if len(values) == 1 else None


def parse_utc(value: str, context: str) -> datetime:
    if not isinstance(value, str) or not UTC_PATTERN.fullmatch(value):
        raise ValueError(f"{context} must be strict UTC YYYY-MM-DDTHH:MM:SSZ")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise ValueError(f"{context} must be a valid UTC timestamp") from exc
    return parsed


def normalized_relative(repo_root: Path, value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("empty repository path")
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts or "." in pure.parts:
        raise ValueError(f"unsafe repository path: {value}")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        raise ValueError(f"repository path contains prohibited control character: {value!r}")
    candidate = repo_root / pure.as_posix()
    try:
        candidate.resolve(strict=False).relative_to(repo_root.resolve(strict=True))
    except ValueError as exc:
        raise ValueError(f"path outside repository: {value}") from exc
    return pure.as_posix()


def canonical_approval_basis(assignments: dict[str, list[str]]) -> str:
    lines: list[str] = []
    for field in APPROVAL_BASIS_FIELDS:
        value = one_value(assignments, field)
        if value is None:
            raise ValueError(f"requires exactly one {field} for approval-basis hashing")
        if "\n" in value or "\r" in value:
            raise ValueError(f"{field} contains prohibited line break")
        lines.append(f"{field}={value}")
    return "\n".join(lines) + "\n"


def approval_basis_sha256(assignments: dict[str, list[str]]) -> str:
    return hashlib.sha256(canonical_approval_basis(assignments).encode("utf-8")).hexdigest()


def artifact_identity(entry: dict[str, Any]) -> str:
    typ = entry.get("type")
    if typ == "REPO_PATH":
        return f"REPO_PATH:{entry.get('path', '')}"
    if typ == "EXTERNAL_ARTIFACT":
        return f"EXTERNAL_ARTIFACT:{entry.get('artifact_id', '')}"
    if typ == "EXTERNAL_INCIDENT":
        return f"EXTERNAL_INCIDENT:{entry.get('incident_id', '')}"
    return f"UNKNOWN:{typ!r}"


def validate_artifact_manifest(repo_root: Path, manifest_path: str) -> tuple[list[str], list[dict[str, Any]], str]:
    errors: list[str] = []
    try:
        rel = normalized_relative(repo_root, manifest_path)
    except ValueError as exc:
        return [str(exc)], [], ""
    if not rel.startswith(ARTIFACT_MANIFEST_ROOT) or not rel.endswith(".json"):
        errors.append(f"artifact manifest must be JSON under {ARTIFACT_MANIFEST_ROOT}")
        return errors, [], ""
    full = repo_root / rel
    if full.is_symlink() or not full.is_file():
        errors.append(f"artifact manifest is missing or not a regular file: {rel}")
        return errors, [], ""
    try:
        value = load_json_strict(full)
    except Exception as exc:
        errors.append(f"artifact manifest invalid: {type(exc).__name__}: {exc}")
        return errors, [], ""
    if not isinstance(value, dict):
        return ["artifact manifest root must be an object"], [], ""
    extra = sorted(set(value) - ARTIFACT_MANIFEST_FIELDS)
    if extra:
        errors.append("artifact manifest unexpected fields: " + ",".join(extra))
    if value.get("record_type") != ARTIFACT_MANIFEST_RECORD_TYPE:
        errors.append("artifact manifest record_type mismatch")
    if value.get("schema_version") != "1.0":
        errors.append("artifact manifest schema_version mismatch")
    artifacts = value.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifact manifest artifacts must be a non-empty list")
        return errors, [], ""
    identities: list[str] = []
    validated: list[dict[str, Any]] = []
    for index, raw in enumerate(artifacts):
        context = f"artifact[{index}]"
        if not isinstance(raw, dict):
            errors.append(f"{context} must be an object")
            continue
        typ = raw.get("type")
        allowed_fields = ARTIFACT_ENTRY_FIELDS.get(typ)
        if allowed_fields is None:
            errors.append(f"{context} unsupported type {typ!r}")
            continue
        if set(raw) != allowed_fields:
            errors.append(f"{context} fields must be exactly {','.join(sorted(allowed_fields))}")
        digest = raw.get("sha256")
        if not isinstance(digest, str) or not SHA256_PATTERN.fullmatch(digest):
            errors.append(f"{context} sha256 invalid")
        if typ == "REPO_PATH":
            try:
                path = normalized_relative(repo_root, raw.get("path"))
            except (TypeError, ValueError) as exc:
                errors.append(f"{context} {exc}")
            else:
                target = repo_root / path
                if target.is_symlink() or not target.is_file():
                    errors.append(f"{context} repository artifact missing or non-regular: {path}")
                elif isinstance(digest, str) and SHA256_PATTERN.fullmatch(digest):
                    actual = hashlib.sha256(target.read_bytes()).hexdigest()
                    if actual != digest:
                        errors.append(f"{context} repository artifact sha256 mismatch: {path}")
        else:
            key = "artifact_id" if typ == "EXTERNAL_ARTIFACT" else "incident_id"
            ident = raw.get(key)
            if not isinstance(ident, str) or not ident.strip() or any(ord(ch) < 32 or ord(ch) == 127 for ch in ident):
                errors.append(f"{context} {key} must be a non-empty printable string")
        identities.append(artifact_identity(raw))
        validated.append(raw)
    if identities != sorted(identities):
        errors.append("artifact manifest entries must be sorted by canonical identity")
    if len(set(identities)) != len(identities):
        errors.append("artifact manifest contains duplicate canonical identities")
    digest_list = ",".join(str(entry.get("sha256", "")) for entry in validated)
    return errors, validated, digest_list


def exception_binding_errors(repo_root: Path, record_path: str, text: str) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    assignments = parse_assignments(text)
    unexpected = sorted(set(assignments) - EXCEPTION_ASSIGNMENT_FIELDS)
    if unexpected:
        errors.append(f"{record_path}: unexpected exception assignment fields: {','.join(unexpected)}")
    for field in EXCEPTION_ASSIGNMENT_FIELDS:
        if len(assignments.get(field, [])) != 1:
            errors.append(f"{record_path}: requires exactly one {field}")
    approved_text = one_value(assignments, "APPROVED_UTC")
    expiration_text = one_value(assignments, "EXPIRATION_UTC")
    approved = expiration = None
    if approved_text:
        try:
            approved = parse_utc(approved_text, f"{record_path}: APPROVED_UTC")
        except ValueError as exc:
            errors.append(str(exc))
    if expiration_text:
        try:
            expiration = parse_utc(expiration_text, f"{record_path}: EXPIRATION_UTC")
        except ValueError as exc:
            errors.append(str(exc))
    if approved is not None and expiration is not None and approved >= expiration:
        errors.append(f"{record_path}: APPROVED_UTC must be earlier than EXPIRATION_UTC")
    expected_hash = None
    try:
        expected_hash = approval_basis_sha256(assignments)
    except ValueError as exc:
        errors.append(f"{record_path}: {exc}")
    declared_hash = one_value(assignments, "APPROVAL_TEXT_SHA256")
    if expected_hash is not None and declared_hash != expected_hash:
        errors.append(f"{record_path}: APPROVAL_TEXT_SHA256 does not match canonical approval basis")
    manifest_path = one_value(assignments, "ARTIFACT_MANIFEST")
    manifest_entries: list[dict[str, Any]] = []
    derived_hash_set = ""
    if manifest_path:
        manifest_errors, manifest_entries, derived_hash_set = validate_artifact_manifest(repo_root, manifest_path)
        errors.extend(f"{record_path}: {message}" for message in manifest_errors)
    declared_hash_set = one_value(assignments, "ARTIFACT_SHA256_SET")
    if derived_hash_set and declared_hash_set != derived_hash_set:
        errors.append(f"{record_path}: ARTIFACT_SHA256_SET does not match canonical artifact manifest order")
    return errors, {
        "assignments": assignments,
        "approved_utc": approved_text,
        "expiration_utc": expiration_text,
        "artifact_manifest": manifest_path,
        "artifact_count": len(manifest_entries),
        "approval_basis_sha256": expected_hash,
        "artifact_sha256_set": derived_hash_set,
    }


def validate_approval(
    report: dict[str, Any],
    comments_value: Any,
    owner_login: str,
    pr_number: int,
    head_sha: str,
    repo_root: Path | None = None,
    evaluation_utc: str | None = None,
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
        "schema_version": "2.0",
        "owner_login": owner_login,
        "pr_number": pr_number,
        "head_sha": head_sha,
        "evaluation_utc": evaluation_utc,
        "exception_records": records,
        "exception_bindings": [],
        "approval_required": bool(records),
        "expected_approval": None,
        "matching_comment_count": 0,
        "matching_comment_created_at": None,
        "violations": violations,
    }

    if not owner_login or not re.fullmatch(r"[A-Za-z0-9-]+", owner_login):
        violations.append("owner login is invalid")

    if records:
        if repo_root is None:
            violations.append("repo_root is required when exception records are present")
        try:
            evaluation = parse_utc(evaluation_utc or "", "evaluation_utc")
        except ValueError as exc:
            violations.append(str(exc))
            evaluation = None

        bindings: list[dict[str, Any]] = []
        if repo_root is not None:
            repo_root = repo_root.resolve(strict=True)
            for record in records:
                try:
                    rel = normalized_relative(repo_root, record)
                    full = repo_root / rel
                    if full.is_symlink() or not full.is_file():
                        raise ValueError(f"exception record missing or non-regular: {rel}")
                    text = full.read_bytes().decode("utf-8", "strict")
                    binding_errors, binding = exception_binding_errors(repo_root, rel, text)
                except Exception as exc:
                    violations.append(f"{record}: exception binding validation failed: {type(exc).__name__}: {exc}")
                    continue
                violations.extend(binding_errors)
                binding["path"] = rel
                bindings.append(binding)
        result["exception_bindings"] = bindings

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
                matches: list[dict[str, Any]] = []
                for comment in comments:
                    user = comment.get("user")
                    login = user.get("login") if isinstance(user, dict) else None
                    body = comment.get("body")
                    if login == owner_login and body == expected:
                        matches.append(comment)
                result["matching_comment_count"] = len(matches)
                if len(matches) != 1:
                    violations.append(f"requires exactly one current exact owner approval comment; observed {len(matches)}")
                else:
                    created_text = matches[0].get("created_at")
                    result["matching_comment_created_at"] = created_text
                    try:
                        created = parse_utc(created_text, "owner approval comment created_at")
                    except ValueError as exc:
                        violations.append(str(exc))
                    else:
                        if evaluation is not None and created > evaluation:
                            violations.append("owner approval comment is later than trusted evaluation instant")
                        for binding in bindings:
                            try:
                                approved = parse_utc(binding["approved_utc"], f"{binding['path']}: APPROVED_UTC")
                                expiration = parse_utc(binding["expiration_utc"], f"{binding['path']}: EXPIRATION_UTC")
                            except ValueError as exc:
                                violations.append(str(exc))
                                continue
                            if created < approved:
                                violations.append(f"{binding['path']}: owner approval comment predates APPROVED_UTC")
                            if evaluation is not None and evaluation >= expiration:
                                violations.append(f"{binding['path']}: exception is expired at trusted evaluation instant")

    result["status"] = "PASS" if not violations else "FAIL"
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--comments", required=True)
    parser.add_argument("--owner-login", required=True)
    parser.add_argument("--pr-number", required=True, type=int)
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--evaluation-utc", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
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
            repo_root=Path(args.repo_root),
            evaluation_utc=args.evaluation_utc,
        )
    except Exception as exc:
        result = {
            "record_type": "SMT_OWNER_EXCEPTION_APPROVAL_VALIDATION",
            "schema_version": "2.0",
            "status": "FAIL",
            "owner_login": args.owner_login,
            "pr_number": args.pr_number,
            "head_sha": args.head_sha,
            "evaluation_utc": args.evaluation_utc,
            "exception_records": [],
            "exception_bindings": [],
            "approval_required": False,
            "expected_approval": None,
            "matching_comment_count": 0,
            "matching_comment_created_at": None,
            "violations": [f"owner approval validation failed closed: {type(exc).__name__}: {exc}"],
        }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
