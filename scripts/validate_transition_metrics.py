#!/usr/bin/env python3
"""Validate SMT transition metrics, handoff, lifecycle, and change-control records."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from smt_git_change_contract import GitContractError, commit_deltas, head_commit_and_tree, head_tree_entry, require_head_regular_blob, require_worktree_matches_head_regular_blob, resolve_commit

DEFAULT_POLICY = "config/transition-metrics-policy.json"
DEFAULT_REPORT = "transition-metrics-validation-report.json"
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
ASSIGNMENT_RE = re.compile(r"^([A-Z][A-Z0-9_]*)=(.*)$")
TRANSITION_CANONICAL_PATHS = {
    ".github/workflows/mandatory-assurance-invariant-gate.yml",
    "config/transition-metrics-policy.json",
    "docs/Integration/SMT-Transition-Governance-Integration-Addendum.md",
    "docs/Standards/SMT-Mandatory-Transition-Metrics-and-Handoff-Performance-Standard.md",
    "docs/Templates/SMT-Transition-Event-Metrics-Template.json",
    "docs/Templates/SMT-Transition-Metrics-Baseline-Projection.csv",
    "docs/Templates/SMT-Transition-Metrics-Baseline-Template.json",
    "scripts/validate_transition_metrics.py",
    "skills/smt-mandatory-transition-metrics-and-handoff/SKILL.md",
    "tests/test_validate_transition_metrics.py",
}
ABSOLUTE_RESOURCE_LIMITS = {"json_bytes": 1048576, "csv_bytes": 4194304, "markdown_bytes": 2097152}

POLICY_TOP_LEVEL_FIELDS = frozenset({
    "allow_overlapping_timing_intervals", "allowed_transitions", "baseline_commit_for_adoption",
    "change_record_filename_keywords", "classifications", "data_quality_states", "effective_date",
    "event_types", "governed_markdown_roots", "lifecycle_states", "m22_active_categories",
    "m23_rework_category", "m27_denominator_metric_ids", "metric_order", "metrics",
    "metrics_link_filename_keywords", "policy_id", "record_types", "required_change_record_fields",
    "required_handoff_components", "resource_limits", "safe_external_reference_types", "schema_version",
    "snapshot_types", "timing_categories", "transition_metrics_assignment",
})
SNAPSHOT_TOP_LEVEL_FIELDS = frozenset({
    "baseline_commit", "baseline_snapshot", "collection_method", "created_utc", "csv_projection_path",
    "defects", "handoff_components", "lifecycle_state", "metrics", "previous_record", "prior_handoff",
    "prior_handoff_available", "prior_handoff_unavailable_reason", "record_type", "schema_version",
    "snapshot_type", "test_runs", "timing_intervals", "workstream_id",
})
EVENT_COMMON_FIELDS = frozenset({
    "classification", "created_utc", "event_id", "event_type", "evidence_refs", "lifecycle_from",
    "lifecycle_to", "mutation_boundary_crossed", "previous_record", "record_type", "schema_version",
    "workstream_id",
})
EVENT_OPTIONAL_FIELD_BY_TYPE = {"DEVIATION":"deviation", "EXTERNAL_BLOCKER":"external_incident", "QUALIFICATION_RUN":"test_run"}
METRIC_FIELDS = frozenset({"metric_id","name","unit","value","data_quality","collection_method","reason","evidence_refs","numerator","denominator"})
TEST_RUN_FIELDS = frozenset({"run_id","test_layer","result","release_authorizing","test_id","requirement_id","production_function_path","fixture_provenance","expected_result_source","actual_result","mutation_boundary","cleanup_preserve_behavior","evidence_artifact"})
DEFECT_FIELDS = frozenset({"defect_id","classification","repeated","prior_lesson_or_control_ref"})
HANDOFF_COMPONENT_FIELDS = frozenset({"component_id","status","path","sha256"})
TIMING_INTERVAL_FIELDS = frozenset({"interval_id","category","start_utc","end_utc"})
BINDING_FIELDS = frozenset({"path","sha256"})
DEVIATION_FIELDS = frozenset({"deviation_id","timestamp_utc","category","planned_condition","observed_condition","impact","mutation_status","evidence_reference","owner_disposition","permanent_control_decision"})
EXTERNAL_INCIDENT_FIELDS = frozenset({"candidate_revision_action","code_revision_created","exposed_internal_defect"})
REFERENCE_FIELDS = {
    "REPO_PATH": frozenset({"type","path","sha256"}),
    "EXTERNAL_ARTIFACT": frozenset({"type","artifact_id","sha256"}),
    "EXTERNAL_INCIDENT": frozenset({"type","incident_id","sha256"}),
}

def reject_unexpected_fields(value: Any, allowed: frozenset[str], context: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        return
    extra = sorted(set(value) - set(allowed))
    if extra:
        errors.append(f"{context}: unexpected fields: {','.join(extra)}")

TRANSITION_CANONICAL_RECORD_PATHS = {
    "docs/Templates/SMT-Transition-Event-Metrics-Template.json",
    "docs/Templates/SMT-Transition-Metrics-Baseline-Template.json",
}


def load_json_text_strict(text: str) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_nonfinite_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON number is not permitted: {value}")

    return json.loads(
        text,
        object_pairs_hook=reject_duplicates,
        parse_constant=reject_nonfinite_constant,
    )


def read_limited_bytes(path: Path, limit: int, context: str) -> bytes:
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise ValueError(f"{context}: stat failed: {type(exc).__name__}: {exc}") from exc
    if size > limit:
        raise ValueError(f"{context}: file size {size} exceeds limit {limit}")
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ValueError(f"{context}: read failed: {type(exc).__name__}: {exc}") from exc
    if len(data) > limit:
        raise ValueError(f"{context}: file size exceeds limit {limit}")
    return data


def read_limited_text(path: Path, limit: int, context: str) -> str:
    data = read_limited_bytes(path, limit, context)
    try:
        return data.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{context}: not valid UTF-8") from exc


def load_json_strict(path: Path, limit: int = ABSOLUTE_RESOURCE_LIMITS["json_bytes"]) -> Any:
    return load_json_text_strict(read_limited_text(path, limit, str(path)))


def utc(value: Any) -> bool:
    if not isinstance(value, str) or not UTC_RE.fullmatch(value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False


def run_git(repo_root: Path, args: list[str]) -> str:
    proc = subprocess.run(["git", *args], cwd=repo_root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def merge_base_commit(repo_root: Path, base_ref: str) -> str:
    merge_base = run_git(repo_root, ["merge-base", base_ref, "HEAD"]).strip()
    if not SHA1_RE.fullmatch(merge_base):
        raise RuntimeError("git merge-base did not return a commit SHA")
    return merge_base


def repository_relative_file(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=True)).as_posix()
    except ValueError as exc:
        raise ValueError(f"policy path must be inside repository: {path}") from exc


def git_text_at_commit(repo_root: Path, commit: str, path: str, max_bytes: int = ABSOLUTE_RESOURCE_LIMITS["json_bytes"]) -> str | None:
    listed = run_git(repo_root, ["ls-tree", "--name-only", commit, "--", path])
    if path not in {line.strip() for line in listed.splitlines() if line.strip()}:
        return None
    size_text = run_git(repo_root, ["cat-file", "-s", f"{commit}:{path}"]).strip()
    try:
        size = int(size_text)
    except ValueError as exc:
        raise ValueError(f"historical repository object size is invalid for {path}") from exc
    if size > max_bytes:
        raise ValueError(f"historical repository object {path} size {size} exceeds limit {max_bytes}")
    return run_git(repo_root, ["show", f"{commit}:{path}"])


def string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and bool(item) for item in value)


def unique_string_list(value: Any) -> bool:
    return string_list(value) and len(value) == len(set(value))


def policy_shape_errors(policy: Any, context: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(policy, dict):
        return [f"{context}: policy must be an object"]
    extra_top = sorted(set(policy) - set(POLICY_TOP_LEVEL_FIELDS))
    if extra_top:
        errors.append(f"{context}: unexpected top-level fields: {','.join(extra_top)}")

    if not isinstance(policy.get("policy_id"), str) or not policy.get("policy_id"):
        errors.append(f"{context}: policy_id must be a non-empty string")
    if not isinstance(policy.get("schema_version"), str) or not policy.get("schema_version"):
        errors.append(f"{context}: schema_version must be a non-empty string")

    effective_date = policy.get("effective_date")
    if not isinstance(effective_date, str):
        errors.append(f"{context}: effective_date must be YYYY-MM-DD string")
    else:
        try:
            datetime.strptime(effective_date, "%Y-%m-%d")
        except ValueError:
            errors.append(f"{context}: effective_date must be valid YYYY-MM-DD")

    if not isinstance(policy.get("allow_overlapping_timing_intervals"), bool):
        errors.append(f"{context}: allow_overlapping_timing_intervals must be boolean")

    record_types = policy.get("record_types")
    if not isinstance(record_types, dict):
        errors.append(f"{context}: record_types must be an object")
    else:
        if set(record_types) != {"event", "snapshot"}:
            errors.append(f"{context}: record_types must contain exactly event and snapshot")
        event_type = record_types.get("event")
        snapshot_type = record_types.get("snapshot")
        if not isinstance(event_type, str) or not event_type:
            errors.append(f"{context}: record_types.event must be a non-empty string")
        if not isinstance(snapshot_type, str) or not snapshot_type:
            errors.append(f"{context}: record_types.snapshot must be a non-empty string")
        if isinstance(event_type, str) and event_type and event_type == snapshot_type:
            errors.append(f"{context}: event and snapshot record types must be distinct")

    list_fields = [
        "change_record_filename_keywords", "classifications", "data_quality_states",
        "event_types", "governed_markdown_roots", "lifecycle_states",
        "m22_active_categories", "m27_denominator_metric_ids", "metric_order",
        "metrics_link_filename_keywords", "required_change_record_fields",
        "required_handoff_components", "safe_external_reference_types",
        "snapshot_types", "timing_categories",
    ]
    for field in list_fields:
        if not unique_string_list(policy.get(field)):
            errors.append(f"{context}: {field} must be a non-empty unique-string list")

    if isinstance(policy.get("data_quality_states"), list) and set(policy["data_quality_states"]) != {
        "MEASURED", "DERIVED", "UNKNOWN", "NOT_APPLICABLE"
    }:
        errors.append(f"{context}: data_quality_states must match supported validator states")
    if isinstance(policy.get("safe_external_reference_types"), list) and set(policy["safe_external_reference_types"]) != {
        "EXTERNAL_ARTIFACT", "EXTERNAL_INCIDENT"
    }:
        errors.append(f"{context}: safe_external_reference_types must match supported validator types")

    roots = policy.get("governed_markdown_roots")
    if isinstance(roots, list):
        for root in roots:
            if not isinstance(root, str) or not root.endswith("/") or root.startswith("/") or ".." in PurePosixPath(root).parts:
                errors.append(f"{context}: governed_markdown_roots contains unsafe/non-directory root: {root!r}")

    for field in ["change_record_filename_keywords", "metrics_link_filename_keywords"]:
        values = policy.get(field)
        if isinstance(values, list):
            for value in values:
                if not isinstance(value, str) or value != value.lower() or "/" in value or "\\" in value:
                    errors.append(f"{context}: {field} contains invalid filename keyword: {value!r}")

    assignment = policy.get("transition_metrics_assignment")
    if not isinstance(assignment, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]*", assignment):
        errors.append(f"{context}: transition_metrics_assignment must be an uppercase assignment key")

    baseline = policy.get("baseline_commit_for_adoption")
    if not isinstance(baseline, str) or not SHA1_RE.fullmatch(baseline):
        errors.append(f"{context}: baseline_commit_for_adoption must be a 40-character commit SHA")

    lifecycle_states = policy.get("lifecycle_states")
    allowed_transitions = policy.get("allowed_transitions")
    if not isinstance(allowed_transitions, dict):
        errors.append(f"{context}: allowed_transitions must be an object")
    elif isinstance(lifecycle_states, list) and unique_string_list(lifecycle_states):
        if set(allowed_transitions) != set(lifecycle_states):
            errors.append(f"{context}: allowed_transitions keys must exactly match lifecycle_states")
        for state, targets in allowed_transitions.items():
            if not isinstance(targets, list) or any(not isinstance(t, str) for t in targets) or len(targets) != len(set(targets)):
                errors.append(f"{context}: allowed_transitions[{state}] must be a unique-string list")
            elif any(t not in lifecycle_states for t in targets):
                errors.append(f"{context}: allowed_transitions[{state}] contains unknown lifecycle state")

    metrics = policy.get("metrics")
    metric_order = policy.get("metric_order")
    if not isinstance(metrics, dict):
        errors.append(f"{context}: metrics must be an object")
    elif isinstance(metric_order, list) and unique_string_list(metric_order):
        if set(metrics) != set(metric_order):
            errors.append(f"{context}: metrics keys must exactly match metric_order")
        supported_value_types = {"COUNT", "DURATION_SECONDS", "PERCENT", "PASS_FAIL", "TEST_DISTRIBUTION"}
        required_metric_fields = {
            "allowed_data_quality", "applicability", "collection_cadence", "computed_by_validator",
            "definition", "evidence_required", "name", "ratio_inputs_required_when_numeric",
            "target", "trend_rule", "unit", "value_type", "zero_denominator_behavior",
        }
        for mid in metric_order:
            definition = metrics.get(mid)
            if not isinstance(definition, dict):
                errors.append(f"{context}: metrics[{mid}] must be an object")
                continue
            missing = required_metric_fields - set(definition)
            if missing:
                errors.append(f"{context}: metrics[{mid}] missing fields: {','.join(sorted(missing))}")
            extra = sorted(set(definition) - required_metric_fields)
            if extra:
                errors.append(f"{context}: metrics[{mid}] unexpected fields: {','.join(extra)}")
            if definition.get("value_type") not in supported_value_types:
                errors.append(f"{context}: metrics[{mid}] has unsupported value_type")
            if not unique_string_list(definition.get("allowed_data_quality")):
                errors.append(f"{context}: metrics[{mid}].allowed_data_quality must be a non-empty unique-string list")
            elif isinstance(policy.get("data_quality_states"), list) and any(
                dq not in policy["data_quality_states"] for dq in definition["allowed_data_quality"]
            ):
                errors.append(f"{context}: metrics[{mid}].allowed_data_quality contains unsupported state")
            if not unique_string_list(definition.get("collection_cadence")):
                errors.append(f"{context}: metrics[{mid}].collection_cadence must be a non-empty unique-string list")
            for bool_field in ["computed_by_validator", "evidence_required", "ratio_inputs_required_when_numeric"]:
                if not isinstance(definition.get(bool_field), bool):
                    errors.append(f"{context}: metrics[{mid}].{bool_field} must be boolean")
            for str_field in ["applicability", "definition", "name", "target", "trend_rule", "unit", "zero_denominator_behavior"]:
                if not isinstance(definition.get(str_field), str) or not definition.get(str_field):
                    errors.append(f"{context}: metrics[{mid}].{str_field} must be non-empty string")

    for field in ["m22_active_categories", "m27_denominator_metric_ids"]:
        values = policy.get(field)
        if not isinstance(values, list):
            continue
        universe = policy.get("timing_categories") if field == "m22_active_categories" else policy.get("metric_order")
        if isinstance(universe, list) and any(value not in universe for value in values):
            errors.append(f"{context}: {field} contains unknown value")
    m23 = policy.get("m23_rework_category")
    if not isinstance(m23, str) or not m23:
        errors.append(f"{context}: m23_rework_category must be a non-empty string")
    elif isinstance(policy.get("timing_categories"), list) and m23 not in policy["timing_categories"]:
        errors.append(f"{context}: m23_rework_category must be in timing_categories")

    limits = policy.get("resource_limits")
    if not isinstance(limits, dict) or set(limits) != set(ABSOLUTE_RESOURCE_LIMITS):
        errors.append(f"{context}: resource_limits must contain exactly json_bytes,csv_bytes,markdown_bytes")
    else:
        for key, ceiling in ABSOLUTE_RESOURCE_LIMITS.items():
            value = limits.get(key)
            if isinstance(value, bool) or not isinstance(value, int) or value < 1024 or value > ceiling:
                errors.append(f"{context}: resource_limits.{key} must be integer in [1024,{ceiling}]")

    return errors


def policy_identity_compatibility_errors(
    base_policy: dict[str, Any],
    current_policy: dict[str, Any],
) -> list[str]:
    """Prevent ordinary policy evolution from weakening the R1 semantic contract."""
    errors: list[str] = []
    immutable_fields = [
        "policy_id", "schema_version", "baseline_commit_for_adoption", "record_types",
        "transition_metrics_assignment", "allow_overlapping_timing_intervals",
        "classifications", "data_quality_states", "event_types", "lifecycle_states",
        "allowed_transitions", "m22_active_categories", "m23_rework_category",
        "m27_denominator_metric_ids", "metric_order", "metrics",
        "safe_external_reference_types", "snapshot_types", "timing_categories", "resource_limits",
    ]
    legacy_messages = {
        "policy_id": "merge-base policy_id does not match current policy_id",
        "baseline_commit_for_adoption": "baseline_commit_for_adoption is immutable after adoption",
        "record_types": "record_types identities are immutable after adoption",
        "transition_metrics_assignment": "transition_metrics_assignment identity is immutable after adoption",
    }
    for field in immutable_fields:
        if base_policy.get(field) != current_policy.get(field):
            errors.append(legacy_messages.get(field, f"{field} is immutable under ordinary R1 policy evolution"))

    # Governance/required-content sets may become stricter but may not shrink.
    for field in [
        "governed_markdown_roots", "metrics_link_filename_keywords",
        "change_record_filename_keywords", "required_change_record_fields",
    ]:
        removed = sorted(set(base_policy.get(field, [])) - set(current_policy.get(field, [])))
        if removed:
            errors.append(f"{field} may not remove R1 controls: {','.join(removed)}")

    # Handoff components are order-sensitive: additions are permitted only as an append.
    base_components = base_policy.get("required_handoff_components", [])
    current_components = current_policy.get("required_handoff_components", [])
    if not isinstance(base_components, list) or not isinstance(current_components, list) or current_components[:len(base_components)] != base_components:
        errors.append("required_handoff_components may not remove, reorder, or replace existing R1 components")

    # Effective date can advance for a stricter ordinary policy but cannot move backward.
    try:
        base_date = datetime.strptime(base_policy.get("effective_date", ""), "%Y-%m-%d")
        current_date = datetime.strptime(current_policy.get("effective_date", ""), "%Y-%m-%d")
        if current_date < base_date:
            errors.append("effective_date may not move backward")
    except (TypeError, ValueError):
        # Shape validation reports malformed dates.
        pass
    return errors


def load_base_policy_context(
    repo_root: Path,
    base_ref: str,
    policy_path: Path,
    current_policy: dict[str, Any],
) -> tuple[str, dict[str, Any] | None, str]:
    merge_base = merge_base_commit(repo_root, base_ref)
    policy_rel = repository_relative_file(repo_root, policy_path)
    text = git_text_at_commit(repo_root, merge_base, policy_rel)
    if text is None:
        if current_policy.get("baseline_commit_for_adoption") != merge_base:
            raise ValueError(
                f"merge-base policy absent at {policy_rel} and baseline_commit_for_adoption "
                f"does not equal merge-base {merge_base}"
            )
        return merge_base, None, "BOOTSTRAP_ABSENT_AUTHORIZED"
    try:
        base_policy = load_json_text_strict(text)
    except (UnicodeError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError(f"merge-base policy parse failed: {exc}") from exc
    errors = policy_shape_errors(base_policy, "merge-base policy")
    if errors:
        raise ValueError("; ".join(errors))
    compatibility_errors = policy_identity_compatibility_errors(base_policy, current_policy)
    if compatibility_errors:
        raise ValueError("; ".join(compatibility_errors))
    return merge_base, base_policy, "PRESENT_VALID"


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def policy_failure_report(message: str, *, current_policy_path: str | None = None) -> dict[str, Any]:
    return {
        "record_type": "SMT_TRANSITION_METRICS_VALIDATION",
        "schema_version": "1.0",
        "status": "FAIL",
        "file_count": 0,
        "files": [],
        "violations": [message],
        "direct_changed_paths": [],
        "reverse_reference_paths": [],
        "validation_paths": [],
        "deleted_paths": [],
        "base_governed_changed_paths": [],
        "base_governed_markdown_paths": [],
        "current_policy_path": current_policy_path,
        "base_policy_status": "UNAVAILABLE",
    }


def changed_files(repo_root: Path, base_ref: str) -> tuple[list[str], set[str]]:
    merge_base, deltas = commit_deltas(repo_root, base_ref)
    base_commit = resolve_commit(repo_root, base_ref)
    if merge_base != base_commit:
        raise GitContractError(f"base freshness failure: merge-base {merge_base} != base commit {base_commit}")
    current = sorted({delta.path for delta in deltas if not delta.deleted})
    deleted = {delta.path for delta in deltas if delta.deleted}
    return current, deleted


def safe_rel(repo_root: Path, value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("empty path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ValueError(f"unsafe repository path: {value}")
    normalized = path.as_posix()
    full = repo_root / normalized
    try:
        full.resolve(strict=False).relative_to(repo_root.resolve(strict=True))
    except ValueError as exc:
        raise ValueError(f"path outside repository: {value}") from exc
    return normalized


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_reference(repo_root: Path, ref: Any, errors: list[str], context: str) -> None:
    if not isinstance(ref, dict):
        errors.append(f"{context}: evidence reference must be an object")
        return
    typ = ref.get("type")
    allowed = REFERENCE_FIELDS.get(typ) if isinstance(typ, str) else None
    if allowed is not None:
        reject_unexpected_fields(ref, allowed, context, errors)
    if typ == "REPO_PATH":
        try:
            rel = safe_rel(repo_root, ref.get("path"))
        except (TypeError, ValueError) as exc:
            errors.append(f"{context}: {exc}")
            return
        full = repo_root / rel
        if not full.exists() or full.is_symlink() or not full.is_file():
            errors.append(f"{context}: referenced repository file missing/non-regular: {rel}")
            return
        expected = ref.get("sha256")
        if expected is not None:
            if not isinstance(expected, str) or not SHA256_RE.fullmatch(expected):
                errors.append(f"{context}: invalid reference sha256 for {rel}")
            elif sha256_file(full) != expected:
                errors.append(f"{context}: reference sha256 mismatch for {rel}")
    elif typ in ("EXTERNAL_ARTIFACT", "EXTERNAL_INCIDENT"):
        ident = ref.get("artifact_id") if typ == "EXTERNAL_ARTIFACT" else ref.get("incident_id")
        if not isinstance(ident, str) or not ident.strip():
            errors.append(f"{context}: {typ} requires non-empty identity")
        digest = ref.get("sha256")
        if digest is not None and (not isinstance(digest, str) or not SHA256_RE.fullmatch(digest)):
            errors.append(f"{context}: invalid external reference sha256")
    else:
        errors.append(f"{context}: unsupported evidence reference type: {typ}")


def validate_binding(
    repo_root: Path,
    binding: Any,
    errors: list[str],
    context: str,
    *,
    expected_record_types: set[str] | None = None,
    expected_workstream_id: str | None = None,
    expected_snapshot_type: str | None = None,
) -> dict[str, Any] | None:
    if binding is None:
        return None
    if not isinstance(binding, dict):
        errors.append(f"{context}: binding must be object or null")
        return None
    reject_unexpected_fields(binding, BINDING_FIELDS, context, errors)
    try:
        rel = safe_rel(repo_root, binding.get("path"))
    except (TypeError, ValueError) as exc:
        errors.append(f"{context}: {exc}")
        return None
    digest = binding.get("sha256")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        errors.append(f"{context}: binding sha256 invalid")
        return None
    full = repo_root / rel
    if not full.exists() or full.is_symlink() or not full.is_file():
        errors.append(f"{context}: bound file missing/non-regular: {rel}")
        return None
    if sha256_file(full) != digest:
        errors.append(f"{context}: bound file sha256 mismatch: {rel}")
        return None
    if expected_record_types is None and expected_workstream_id is None and expected_snapshot_type is None:
        return None
    try:
        target = load_json_strict(full)
    except Exception as exc:
        errors.append(f"{context}: bound transition record JSON parse failed: {rel}: {exc}")
        return None
    if not isinstance(target, dict):
        errors.append(f"{context}: bound transition record must be JSON object: {rel}")
        return None
    if expected_record_types is not None and target.get("record_type") not in tuple(expected_record_types):
        errors.append(f"{context}: bound record has incompatible record_type: {rel}")
    if expected_workstream_id is not None and target.get("workstream_id") != expected_workstream_id:
        errors.append(f"{context}: bound record workstream_id mismatch: {rel}")
    if expected_snapshot_type is not None and target.get("snapshot_type") != expected_snapshot_type:
        errors.append(f"{context}: bound record snapshot_type must be {expected_snapshot_type}: {rel}")
    return target


def finite_number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    try:
        result = float(value)
    except (OverflowError, TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def metric_value_domain(metric: dict[str, Any], definition: dict[str, Any], errors: list[str], context: str) -> None:
    dq = metric.get("data_quality")
    value = metric.get("value")
    if dq in ("UNKNOWN", "NOT_APPLICABLE"):
        if value is not None:
            errors.append(f"{context}: {dq} metric value must be null")
        if not isinstance(metric.get("reason"), str) or not metric.get("reason", "").strip():
            errors.append(f"{context}: {dq} requires non-empty reason")
        if not isinstance(metric.get("collection_method"), str) or not metric.get("collection_method", "").strip():
            errors.append(f"{context}: {dq} requires collection_method")
        if not isinstance(metric.get("evidence_refs"), list):
            errors.append(f"{context}: evidence_refs must be list")
        return
    if dq not in ("MEASURED", "DERIVED"):
        errors.append(f"{context}: invalid data_quality {dq}")
        return
    refs = metric.get("evidence_refs")
    if not isinstance(refs, list):
        errors.append(f"{context}: evidence_refs must be list")
        refs = []
    if not isinstance(metric.get("reason"), str):
        errors.append(f"{context}: reason must be string")
    if not refs:
        errors.append(f"{context}: measured/derived metric requires evidence_refs")
    if not isinstance(metric.get("collection_method"), str) or not metric.get("collection_method", "").strip():
        errors.append(f"{context}: measured/derived metric requires collection_method")
    typ = definition["value_type"]
    if typ in ("COUNT", "DURATION_SECONDS"):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            errors.append(f"{context}: {typ} value must be non-negative integer")
    elif typ == "PERCENT":
        numeric_value = finite_number(value)
        if numeric_value is None or not (0 <= numeric_value <= 100):
            errors.append(f"{context}: percent value must be finite in [0,100]")
    elif typ == "PASS_FAIL":
        if not isinstance(value, str) or value not in {"PASS", "FAIL"}:
            errors.append(f"{context}: PASS_FAIL value must be PASS or FAIL string")
    elif typ == "TEST_DISTRIBUTION":
        if not isinstance(value, dict):
            errors.append(f"{context}: TEST_DISTRIBUTION value must be object")


def ratio_check(metric: dict[str, Any], errors: list[str], context: str) -> None:
    if metric.get("data_quality") not in ("MEASURED","DERIVED"):
        return
    num = finite_number(metric.get("numerator"))
    den = finite_number(metric.get("denominator"))
    if num is None or den is None:
        errors.append(f"{context}: ratio metric requires finite numeric numerator and denominator")
        return
    if num < 0 or den < 0 or num > den:
        errors.append(f"{context}: invalid numerator/denominator domain")
        return
    if den == 0:
        errors.append(f"{context}: denominator zero requires NOT_APPLICABLE")
        return
    value = finite_number(metric.get("value"))
    if value is None:
        return
    expected = num / den * 100.0
    if abs(value - expected) > 1e-9:
        errors.append(f"{context}: value does not equal numerator/denominator percentage")


def parse_time(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")


def validate_intervals(record: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> tuple[int,int,int]:
    intervals = record.get("timing_intervals", [])
    if not isinstance(intervals, list):
        errors.append("timing_intervals must be list")
        return 0,0,0
    spans: list[tuple[datetime,datetime,str,str]] = []
    ids: set[str] = set()
    for idx, item in enumerate(intervals):
        ctx = f"timing_intervals[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{ctx}: must be object")
            continue
        reject_unexpected_fields(item, TIMING_INTERVAL_FIELDS, ctx, errors)
        iid = item.get("interval_id")
        iid_valid = isinstance(iid, str) and bool(iid) and iid not in ids
        if not iid_valid:
            errors.append(f"{ctx}: interval_id missing or duplicate")
        else:
            ids.add(iid)
        cat = item.get("category")
        cat_valid = isinstance(cat, str) and cat in policy["timing_categories"]
        if not cat_valid:
            errors.append(f"{ctx}: invalid category {cat}")
        s, e = item.get("start_utc"), item.get("end_utc")
        if not utc(s) or not utc(e):
            errors.append(f"{ctx}: timestamps must be strict UTC")
            continue
        sd, ed = parse_time(s), parse_time(e)
        if ed < sd:
            errors.append(f"{ctx}: end before start")
            continue
        if not cat_valid:
            continue
        span_id = iid if iid_valid else f"INVALID_INTERVAL_{idx}"
        spans.append((sd,ed,cat,span_id))
    spans.sort()
    if not policy.get("allow_overlapping_timing_intervals", False):
        for a, b in zip(spans, spans[1:]):
            if b[0] < a[1]:
                errors.append(f"timing_intervals overlap: {a[3]} and {b[3]}")
    ext = active = rework = 0
    for s,e,cat,_ in spans:
        sec = int((e-s).total_seconds())
        if cat == "HOLD_EXTERNAL": ext += sec
        if cat in policy["m22_active_categories"]: active += sec
        if cat == policy["m23_rework_category"]: rework += sec
    return ext, active, rework


def dist_from_runs(runs: Any, errors: list[str]) -> dict[str, Any] | None:
    if not isinstance(runs, list):
        errors.append("test_runs must be list")
        return None
    counts: Counter[tuple[str,str]] = Counter()
    ids: set[str] = set()
    for idx, run in enumerate(runs):
        ctx=f"test_runs[{idx}]"
        if not isinstance(run, dict):
            errors.append(f"{ctx}: must be object"); continue
        reject_unexpected_fields(run, TEST_RUN_FIELDS, ctx, errors)
        rid=run.get("run_id")
        if not isinstance(rid,str) or not rid or rid in ids:
            errors.append(f"{ctx}: run_id missing or duplicate")
        else: ids.add(rid)
        layer=run.get("test_layer"); result=run.get("result")
        if not isinstance(layer,str) or not layer.strip(): errors.append(f"{ctx}: test_layer required")
        if not isinstance(result,str) or result not in ("PASS","FAIL","BLOCKED"): errors.append(f"{ctx}: invalid result")
        if not isinstance(run.get("release_authorizing"), bool): errors.append(f"{ctx}: release_authorizing must be boolean")
        for field in ["test_id","requirement_id","production_function_path","fixture_provenance","expected_result_source","actual_result","mutation_boundary","cleanup_preserve_behavior","evidence_artifact"]:
            if not isinstance(run.get(field),str) or not run.get(field," ").strip(): errors.append(f"{ctx}: {field} required")
        if isinstance(layer,str) and isinstance(result,str) and result in ("PASS","FAIL","BLOCKED"): counts[(layer,result)] += 1
    items=[{"test_layer":k[0],"result":k[1],"count":v} for k,v in sorted(counts.items())]
    return {"total_runs": sum(counts.values()), "by_layer_result": items}


def repeat_defect_rate(defects: Any, errors: list[str]) -> float | None:
    if not isinstance(defects, list):
        errors.append("defects must be list")
        return None
    ids:set[str]=set(); repeated=0
    for idx,d in enumerate(defects):
        ctx=f"defects[{idx}]"
        if not isinstance(d,dict): errors.append(f"{ctx}: must be object"); continue
        reject_unexpected_fields(d, DEFECT_FIELDS, ctx, errors)
        did=d.get("defect_id")
        if not isinstance(did,str) or not did or did in ids: errors.append(f"{ctx}: defect_id missing or duplicate")
        else: ids.add(did)
        rep=d.get("repeated")
        if not isinstance(rep,bool): errors.append(f"{ctx}: repeated must be boolean")
        if rep:
            repeated += 1
            if not isinstance(d.get("prior_lesson_or_control_ref"),str) or not d.get("prior_lesson_or_control_ref","").strip():
                errors.append(f"{ctx}: repeated defect requires prior_lesson_or_control_ref")
    if not defects:
        return None
    return repeated / len(defects) * 100.0


def validate_snapshot(repo_root: Path, path: str, record: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    reject_unexpected_fields(record, SNAPSHOT_TOP_LEVEL_FIELDS, path, errors)
    if record.get("schema_version") != policy["schema_version"]: errors.append("schema_version mismatch")
    if record.get("snapshot_type") not in policy["snapshot_types"]: errors.append("invalid snapshot_type")
    if record.get("lifecycle_state") not in policy["lifecycle_states"]: errors.append("invalid lifecycle_state")
    if not utc(record.get("created_utc")): errors.append("created_utc invalid")
    if not isinstance(record.get("baseline_commit"),str) or not SHA1_RE.fullmatch(record.get("baseline_commit","")): errors.append("baseline_commit invalid")
    if not isinstance(record.get("baseline_snapshot"),str) or not record.get("baseline_snapshot","").strip(): errors.append("baseline_snapshot required")
    if not isinstance(record.get("workstream_id"),str) or not record.get("workstream_id","").strip(): errors.append("workstream_id required")
    if not isinstance(record.get("collection_method"),str) or not record.get("collection_method","").strip(): errors.append("collection_method required")
    transition_types = {policy["record_types"]["snapshot"], policy["record_types"]["event"]}
    validate_binding(
        repo_root, record.get("previous_record"), errors, "previous_record",
        expected_record_types=transition_types, expected_workstream_id=record.get("workstream_id")
    )
    if record.get("prior_handoff_available") is True:
        if record.get("prior_handoff") is None: errors.append("prior_handoff required when available")
        validate_binding(
            repo_root, record.get("prior_handoff"), errors, "prior_handoff",
            expected_record_types={policy["record_types"]["snapshot"]},
            expected_workstream_id=record.get("workstream_id"),
            expected_snapshot_type="HANDOFF",
        )
    elif record.get("prior_handoff_available") is False:
        if record.get("prior_handoff") is not None: errors.append("prior_handoff must be null when unavailable")
        if not isinstance(record.get("prior_handoff_unavailable_reason"),str) or not record.get("prior_handoff_unavailable_reason","").strip(): errors.append("prior_handoff_unavailable_reason required")
    else: errors.append("prior_handoff_available must be boolean")

    rows=record.get("metrics")
    if not isinstance(rows,list): return errors+["metrics must be list"]
    ids=[r.get("metric_id") if isinstance(r,dict) else None for r in rows]
    if ids != policy["metric_order"]: errors.append("metrics must contain M01-M28 exactly once in canonical order")
    byid={r.get("metric_id"):r for r in rows if isinstance(r,dict) and isinstance(r.get("metric_id"),str)}
    if len(byid) != len(rows): errors.append("duplicate or malformed metric IDs")
    ext, active, rework = validate_intervals(record, policy, errors)
    dist = dist_from_runs(record.get("test_runs", []), errors)
    repeat_rate = repeat_defect_rate(record.get("defects", []), errors)

    for mid in policy["metric_order"]:
        m=byid.get(mid)
        if not isinstance(m,dict): continue
        ctx=f"{path}:{mid}"
        reject_unexpected_fields(m, METRIC_FIELDS, ctx, errors)
        definition=policy["metrics"][mid]
        if m.get("name") != definition["name"]: errors.append(f"{ctx}: name mismatch")
        if m.get("unit") != definition["unit"]: errors.append(f"{ctx}: unit mismatch")
        metric_value_domain(m, definition, errors, ctx)
        for ref in m.get("evidence_refs", []) if isinstance(m.get("evidence_refs",[]),list) else []:
            validate_reference(repo_root, ref, errors, ctx)
        if definition.get("ratio_inputs_required_when_numeric"): ratio_check(m,errors,ctx)

    def numeric(mid:str) -> int | float | None:
        m=byid.get(mid,{})
        if m.get("data_quality") not in ("MEASURED","DERIVED"):
            return None
        value=m.get("value")
        value_type=policy["metrics"][mid]["value_type"]
        if value_type in ("COUNT", "DURATION_SECONDS"):
            if isinstance(value,bool) or not isinstance(value,int) or value < 0:
                return None
            return value
        return finite_number(value)
    for mid, expected in [('M21',ext),('M22',active)]:
        val=numeric(mid)
        if val is not None and val != expected: errors.append(f"{path}:{mid}: value does not match timing intervals")
    m23=byid.get('M23',{})
    if active == 0:
        if m23.get('data_quality') not in ('NOT_APPLICABLE','UNKNOWN'): errors.append(f"{path}:M23: zero active denominator requires NOT_APPLICABLE or UNKNOWN")
    else:
        val23=numeric('M23')
        if val23 is not None:
            expected=rework/active*100.0
            if abs(val23-expected)>1e-9: errors.append(f"{path}:M23: value does not match rework/active ratio")
    m24=byid.get('M24',{})
    if m24.get('data_quality') in ('MEASURED','DERIVED') and dist is not None and m24.get('value') != dist: errors.append(f"{path}:M24: distribution does not match test_runs")
    m25=byid.get('M25',{})
    if repeat_rate is None:
        if m25.get('data_quality') not in ('NOT_APPLICABLE','UNKNOWN'): errors.append(f"{path}:M25: no defects requires NOT_APPLICABLE or UNKNOWN")
    elif m25.get('data_quality') in ('MEASURED','DERIVED'):
        val25=numeric('M25')
        if val25 is not None and abs(val25-repeat_rate)>1e-9: errors.append(f"{path}:M25: value does not match defect ledger")

    m26=byid.get('M26',{})
    comps=record.get('handoff_components',[])
    if not isinstance(comps,list):
        errors.append(f"{path}: handoff_components must be list")
        comps=[]
    if record.get('snapshot_type') == 'HANDOFF':
        cids=[c.get('component_id') if isinstance(c,dict) else None for c in comps]
        if cids != policy['required_handoff_components']: errors.append(f"{path}: M26 handoff components incomplete/out of order")
        present=0
        for idx,c in enumerate(comps):
            if not isinstance(c,dict):
                continue
            cid=c.get('component_id')
            reject_unexpected_fields(c, HANDOFF_COMPONENT_FIELDS, f"{path}:handoff_components[{idx}]", errors)
            component_valid=True
            if c.get('status') != 'PRESENT':
                errors.append(f"{path}: handoff component not PRESENT: {cid}")
                component_valid=False
            try:
                rel=safe_rel(repo_root,c.get('path'))
            except (TypeError,ValueError) as exc:
                errors.append(f"{path}: handoff component {cid} path {exc}")
                component_valid=False
                rel=None
            digest=c.get('sha256')
            if not isinstance(digest,str) or not SHA256_RE.fullmatch(digest):
                errors.append(f"{path}: handoff component sha256 invalid: {cid}")
                component_valid=False
            if rel is not None:
                full=repo_root/rel
                if not full.exists() or full.is_symlink() or not full.is_file():
                    errors.append(f"{path}: handoff component missing/non-regular: {rel}")
                    component_valid=False
                elif isinstance(digest,str) and SHA256_RE.fullmatch(digest) and sha256_file(full) != digest:
                    errors.append(f"{path}: handoff component sha256 mismatch: {rel}")
                    component_valid=False
            if component_valid:
                present += 1
        expected=present/len(policy['required_handoff_components'])*100.0
        val26=numeric('M26')
        if m26.get('data_quality') not in ('MEASURED','DERIVED') or val26 is None or abs(val26-expected)>1e-9:
            errors.append(f"{path}:M26 value mismatch")
        if expected != 100.0: errors.append(f"{path}: handoff completeness must be 100%")
    else:
        if comps:
            errors.append(f"{path}: non-handoff snapshot must not contain handoff_components")
        if m26.get('data_quality') not in ('NOT_APPLICABLE','UNKNOWN'):
            errors.append(f"{path}:M26 non-handoff snapshot must be NOT_APPLICABLE or UNKNOWN")

    good=0
    for mid in policy['m27_denominator_metric_ids']:
        m=byid.get(mid,{})
        dq=m.get('data_quality')
        method=isinstance(m.get('collection_method'),str) and bool(m.get('collection_method','').strip())
        if dq in ('MEASURED','DERIVED'):
            refs=isinstance(m.get('evidence_refs'),list) and bool(m.get('evidence_refs'))
            if method and refs: good += 1
        elif dq == 'NOT_APPLICABLE':
            reason=isinstance(m.get('reason'),str) and bool(m.get('reason','').strip())
            if method and reason: good += 1
    expected_m27=good/len(policy['m27_denominator_metric_ids'])*100.0
    m27=byid.get('M27',{})
    if m27.get('data_quality') != 'DERIVED': errors.append(f"{path}:M27 must be DERIVED")
    else:
        val27=numeric('M27')
        if val27 is not None and abs(val27-expected_m27)>1e-9: errors.append(f"{path}:M27 value mismatch; expected {expected_m27}")

    csv_path=record.get('csv_projection_path')
    if not isinstance(csv_path,str) or not csv_path.strip():
        errors.append(f"{path}: csv_projection_path must be non-empty string")
    else:
        try: rel=safe_rel(repo_root,csv_path)
        except (TypeError,ValueError) as exc: errors.append(f"{path}: csv_projection_path {exc}")
        else:
            full=repo_root/rel
            if not full.is_file() or full.is_symlink(): errors.append(f"{path}: csv projection missing/non-regular: {rel}")
            else: errors.extend(validate_csv_projection(full, rows, path, policy['resource_limits']['csv_bytes']))
    return errors


def csv_cell(value: Any) -> str:
    if value is None: return ""
    if isinstance(value,(dict,list)): return json.dumps(value,sort_keys=True,separators=(",",":"))
    if isinstance(value,float): return format(value,'.12g')
    return str(value)


def validate_csv_projection(path: Path, rows: list[dict[str,Any]], context: str, max_bytes: int = ABSOLUTE_RESOURCE_LIMITS['csv_bytes']) -> list[str]:
    errors=[]
    expected_header=['metric_id','name','unit','value','data_quality','collection_method','reason']
    try:
        if path.stat().st_size > max_bytes:
            return [f"{context}: CSV file size exceeds limit {max_bytes}"]
        with path.open(newline='',encoding='utf-8') as fh:
            reader=csv.DictReader(fh)
            if reader.fieldnames != expected_header:
                return [f"{context}: CSV header mismatch"]
            actual=list(reader)
    except (UnicodeError, csv.Error, OSError) as exc:
        return [f"{context}: CSV decode/parse failed: {type(exc).__name__}: {exc}"]
    if len(actual)!=len(rows): return [f"{context}: CSV row count mismatch"]
    for i,(a,m) in enumerate(zip(actual,rows)):
        if not isinstance(m,dict):
            errors.append(f"{context}: CSV comparison metric row malformed at index {i}")
            continue
        expected={
            'metric_id':m.get('metric_id',''),'name':m.get('name',''),'unit':m.get('unit',''),
            'value':csv_cell(m.get('value')),'data_quality':m.get('data_quality',''),
            'collection_method':m.get('collection_method',''),'reason':m.get('reason','') or ''
        }
        if a != expected: errors.append(f"{context}: CSV row mismatch at index {i} metric {m.get('metric_id')}")
    return errors


def validate_event(repo_root: Path, path: str, record: dict[str,Any], policy: dict[str,Any]) -> list[str]:
    errors=[]
    event_type=record.get('event_type')
    allowed=set(EVENT_COMMON_FIELDS)
    optional=EVENT_OPTIONAL_FIELD_BY_TYPE.get(event_type) if isinstance(event_type,str) else None
    if optional: allowed.add(optional)
    reject_unexpected_fields(record, frozenset(allowed), path, errors)
    if record.get('schema_version') != policy['schema_version']: errors.append('schema_version mismatch')
    if record.get('event_type') not in policy['event_types']: errors.append('invalid event_type')
    if not utc(record.get('created_utc')): errors.append('created_utc invalid')
    if not isinstance(record.get('workstream_id'),str) or not record.get('workstream_id','').strip(): errors.append('workstream_id required')
    if not isinstance(record.get('event_id'),str) or not record.get('event_id','').strip(): errors.append('event_id required')
    frm,to=record.get('lifecycle_from'),record.get('lifecycle_to')
    transition_events=('LIFECYCLE','RELEASE_RESET','LIVE_ATTEMPT')
    if frm not in policy['lifecycle_states'] or to not in policy['lifecycle_states']:
        errors.append('invalid lifecycle state')
    elif record.get('event_type') in transition_events:
        if to not in policy['allowed_transitions'].get(frm,[]): errors.append(f'invalid lifecycle transition {frm}->{to}')
    elif to != frm and to not in policy['allowed_transitions'].get(frm,[]):
        errors.append(f'invalid lifecycle transition {frm}->{to}')
    if frm == 'CLOSED_AND_FROZEN': errors.append('closed workstream cannot be reopened; create a new named workstream')
    if record.get('classification') not in policy['classifications']: errors.append('invalid classification')
    if not isinstance(record.get('mutation_boundary_crossed'),bool): errors.append('mutation_boundary_crossed must be boolean')
    refs=record.get('evidence_refs')
    if not isinstance(refs,list) or not refs: errors.append('event requires evidence_refs')
    else:
        for ref in refs: validate_reference(repo_root,ref,errors,path)
    validate_binding(
        repo_root, record.get('previous_record'), errors, 'previous_record',
        expected_record_types={policy['record_types']['snapshot'], policy['record_types']['event']},
        expected_workstream_id=record.get('workstream_id'),
    )
    if record.get('event_type') == 'DEVIATION':
        d=record.get('deviation')
        if not isinstance(d,dict): errors.append('DEVIATION event requires deviation object')
        else:
            reject_unexpected_fields(d, DEVIATION_FIELDS, f"{path}:deviation", errors)
            for f in ['deviation_id','timestamp_utc','category','planned_condition','observed_condition','impact','mutation_status','evidence_reference','owner_disposition','permanent_control_decision']:
                if not isinstance(d.get(f),str) or not d.get(f,'').strip(): errors.append(f'deviation.{f} required')
            if d.get('timestamp_utc') and not utc(d.get('timestamp_utc')): errors.append('deviation.timestamp_utc invalid')
    if record.get('event_type') == 'QUALIFICATION_RUN':
        tr=record.get('test_run')
        if not isinstance(tr,dict):
            errors.append('QUALIFICATION_RUN requires exactly one test_run object')
        else:
            dist_from_runs([tr],errors)
    if record.get('event_type') == 'EXTERNAL_BLOCKER':
        ex=record.get('external_incident')
        if not isinstance(ex,dict): errors.append('EXTERNAL_BLOCKER requires external_incident')
        else:
            reject_unexpected_fields(ex, EXTERNAL_INCIDENT_FIELDS, f"{path}:external_incident", errors)
            if ex.get('candidate_revision_action') != 'PRESERVE_EXACT_CANDIDATE': errors.append('external incident must preserve exact candidate')
            if ex.get('code_revision_created') is True and ex.get('exposed_internal_defect') is not True: errors.append('external incident may not create code revision without exposed internal defect')
    return errors


def assignments(text: str) -> dict[str,list[str]]:
    result:dict[str,list[str]]={}
    for raw in text.splitlines():
        m=ASSIGNMENT_RE.fullmatch(raw.strip())
        if m: result.setdefault(m.group(1),[]).append(m.group(2))
    return result


def validate_markdown(repo_root: Path, path: str, text: str, policy: dict[str,Any]) -> list[str]:
    errors=[]; lower=PurePosixPath(path).name.lower(); assn=assignments(text)
    if path.startswith('docs/Releases/') and any(k in lower for k in policy['metrics_link_filename_keywords']):
        vals=assn.get(policy['transition_metrics_assignment'],[])
        if len(vals)!=1: errors.append(f"{path}: requires exactly one {policy['transition_metrics_assignment']}")
        else:
            try: rel=safe_rel(repo_root,vals[0])
            except ValueError as exc: errors.append(f"{path}: metrics link {exc}")
            else:
                full=repo_root/rel
                if not full.is_file() or full.is_symlink():
                    errors.append(f"{path}: metrics record missing/non-regular: {rel}")
                else:
                    try:
                        record=load_json_strict(full)
                    except Exception as exc:
                        errors.append(f"{path}: metrics record JSON parse failed: {rel}: {exc}")
                    else:
                        if not isinstance(record,dict) or record.get('record_type') != policy['record_types']['snapshot']:
                            errors.append(f"{path}: metrics record must be {policy['record_types']['snapshot']}: {rel}")
                        else:
                            errors.extend(validate_snapshot(repo_root,rel,record,policy))
    if any(k in lower for k in policy['change_record_filename_keywords']):
        for field in policy['required_change_record_fields']:
            vals=assn.get(field,[])
            if len(vals)!=1 or not vals[0].strip(): errors.append(f"{path}: requires exactly one non-empty {field}")
    return errors


def is_transition_json(data: Any, policy: dict[str,Any]) -> bool:
    return isinstance(data,dict) and data.get('record_type') in policy['record_types'].values()


def transition_record_path_requires_type(path: str) -> bool:
    if path.startswith("docs/Releases/metrics/") or path in TRANSITION_CANONICAL_RECORD_PATHS:
        return True
    name = PurePosixPath(path).name
    return path.startswith("docs/Templates/") and name.startswith("SMT-Transition-") and name.endswith(".json")


def deleted_path_is_governed(path: str, policy: dict[str, Any]) -> bool:
    if path in TRANSITION_CANONICAL_PATHS or path.startswith("docs/Releases/metrics/"):
        return True
    if path.startswith("docs/Releases/"):
        lower = PurePosixPath(path).name.lower()
        keywords = list(policy.get("metrics_link_filename_keywords", [])) + list(policy.get("change_record_filename_keywords", []))
        return any(keyword in lower for keyword in keywords)
    return False


def referenced_repository_paths(value: Any) -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        raw_path = value.get("path")
        if isinstance(raw_path, str) and raw_path:
            paths.add(raw_path)
        csv_path = value.get("csv_projection_path")
        if isinstance(csv_path, str) and csv_path:
            paths.add(csv_path)
        for child in value.values():
            paths.update(referenced_repository_paths(child))
    elif isinstance(value, list):
        for child in value:
            paths.update(referenced_repository_paths(child))
    return paths


def build_reverse_reference_index(
    repo_root: Path,
    policy: dict[str, Any],
    *,
    historical_transition_paths: set[str] | None = None,
    base_policy: dict[str, Any] | None = None,
) -> dict[str, set[str]]:
    index: dict[str, set[str]] = {}
    historical_transition_paths = historical_transition_paths or set()

    def add(target: str, source: str) -> None:
        try:
            target_rel = safe_rel(repo_root, target)
            source_rel = safe_rel(repo_root, source)
        except (TypeError, ValueError):
            return
        if target_rel == source_rel:
            return
        index.setdefault(target_rel, set()).add(source_rel)

    releases = repo_root / "docs" / "Releases"
    assignment_names = {policy["transition_metrics_assignment"]}
    if base_policy is not None:
        assignment_names.add(base_policy["transition_metrics_assignment"])
    if releases.is_dir():
        for full in sorted(releases.rglob("*.md")):
            if full.is_symlink() or not full.is_file():
                continue
            source = full.relative_to(repo_root).as_posix()
            try:
                text = read_limited_text(full, policy["resource_limits"]["markdown_bytes"], source)
            except ValueError:
                continue
            parsed = assignments(text)
            for assignment_name in sorted(assignment_names):
                for target in parsed.get(assignment_name, []):
                    if isinstance(target, str) and target:
                        add(target, source)

    # Current records are classified under current policy. Historical off-directory
    # records retain identity by path when the merge-base policy classified them as
    # transition records, so current policy vocabulary changes cannot hide them from
    # reverse-reference discovery.
    for full in sorted(repo_root.rglob("*.json")):
        if ".git" in full.parts or full.is_symlink() or not full.is_file():
            continue
        source = full.relative_to(repo_root).as_posix()
        try:
            obj = load_json_strict(full, policy["resource_limits"]["json_bytes"])
        except Exception:
            continue
        if (
            not is_transition_json(obj, policy)
            and not transition_record_path_requires_type(source)
            and source not in historical_transition_paths
        ):
            continue
        if not isinstance(obj, dict):
            continue
        for target in referenced_repository_paths(obj):
            add(target, source)
    return index


def reverse_reference_closure(
    repo_root: Path,
    changed_targets: set[str],
    policy: dict[str, Any],
    reverse_index: dict[str, set[str]] | None = None,
) -> list[str]:
    index = reverse_index if reverse_index is not None else build_reverse_reference_index(repo_root, policy)
    queue = sorted(changed_targets)
    seen_targets: set[str] = set()
    dependent_sources: set[str] = set()
    while queue:
        target = queue.pop(0)
        if target in seen_targets:
            continue
        seen_targets.add(target)
        for source in sorted(index.get(target, set())):
            if source not in dependent_sources:
                dependent_sources.add(source)
                queue.append(source)
    return sorted(dependent_sources)


def base_transition_record_inventory(
    repo_root: Path,
    merge_base: str,
    base_policy: dict[str, Any] | None,
) -> set[str]:
    if base_policy is None:
        return set()
    result: set[str] = set()
    paths = run_git(repo_root, ["ls-tree", "-r", "--name-only", merge_base]).splitlines()
    for path in sorted(p for p in paths if p.endswith(".json")):
        try:
            text = git_text_at_commit(repo_root, merge_base, path)
            if text is None:
                continue
            obj = load_json_text_strict(text)
        except (RuntimeError, UnicodeError, ValueError, json.JSONDecodeError):
            continue
        if is_transition_json(obj, base_policy):
            result.add(path)
    return result


def base_transition_record_paths(
    candidate_paths: set[str],
    historical_transition_paths: set[str],
) -> set[str]:
    """Return changed paths whose governance identity existed at merge-base."""
    return {path for path in candidate_paths if path in historical_transition_paths}


def base_governed_markdown_inventory(
    repo_root: Path,
    merge_base: str,
    base_policy: dict[str, Any] | None,
) -> set[str]:
    if base_policy is None:
        return set()
    roots = tuple(base_policy["governed_markdown_roots"])
    paths = run_git(repo_root, ["ls-tree", "-r", "--name-only", merge_base]).splitlines()
    return {path for path in paths if path.endswith(".md") and path.startswith(roots)}


def deleted_transition_record_paths(
    deleted_paths: set[str],
    historical_transition_paths: set[str],
) -> set[str]:
    """Compatibility helper using merge-base transition identity inventory."""
    return base_transition_record_paths(deleted_paths, historical_transition_paths)


def validate_deleted_paths(
    repo_root: Path,
    deleted_paths: set[str],
    policy: dict[str, Any],
    reverse_index: dict[str, set[str]] | None = None,
    deleted_transition_records: set[str] | None = None,
    base_policy: dict[str, Any] | None = None,
) -> list[str]:
    violations: list[str] = []
    index = reverse_index if reverse_index is not None else build_reverse_reference_index(repo_root, policy)
    deleted_transition_records = deleted_transition_records or set()
    for path in sorted(deleted_paths):
        historically_governed = base_policy is not None and deleted_path_is_governed(path, base_policy)
        if deleted_path_is_governed(path, policy) or historically_governed or path in deleted_transition_records:
            violations.append(f"{path}: deletion of governed transition artifact is prohibited")
        for source in sorted(index.get(path, set())):
            violations.append(f"{path}: deletion creates dangling transition reference from {source}")
    return violations


def validate_files(
    repo_root: Path,
    paths: list[str],
    policy: dict[str,Any],
    required_transition_paths: set[str] | None = None,
    required_markdown_paths: set[str] | None = None,
) -> dict[str,Any]:
    violations=[]; files=[]
    required_transition_paths = required_transition_paths or set()
    required_markdown_paths = required_markdown_paths or set()
    for raw in sorted(set(paths)):
        try: path=safe_rel(repo_root,raw)
        except ValueError as exc: violations.append(str(exc)); continue
        full=repo_root/path
        if not full.exists(): violations.append(f"{path}: changed path does not exist"); continue
        if full.is_symlink() or not full.is_file(): violations.append(f"{path}: must be regular non-symlink file"); continue
        try:
            suffix_limit = policy['resource_limits']['json_bytes'] if path.endswith('.json') else policy['resource_limits']['markdown_bytes'] if path.endswith('.md') else policy['resource_limits']['csv_bytes'] if path.endswith('.csv') else max(ABSOLUTE_RESOURCE_LIMITS.values())
            data=read_limited_bytes(full, suffix_limit, path)
        except ValueError as exc:
            violations.append(str(exc)); continue
        if b'\r' in data: violations.append(f"{path}: contains CR characters")
        errors=[]
        if path.endswith('.json'):
            try: obj=load_json_strict(full, policy['resource_limits']['json_bytes'])
            except Exception as exc: errors.append(f"{path}: JSON parse failed: {exc}")
            else:
                requires_transition_type = transition_record_path_requires_type(path) or path in required_transition_paths
                if requires_transition_type and not is_transition_json(obj,policy):
                    errors.append(f"{path}: unrecognized transition record_type")
                elif is_transition_json(obj,policy):
                    if obj['record_type']==policy['record_types']['snapshot']: errors.extend(validate_snapshot(repo_root,path,obj,policy))
                    else: errors.extend(validate_event(repo_root,path,obj,policy))
        elif path.endswith('.md') and (path in required_markdown_paths or any(path.startswith(root) for root in policy['governed_markdown_roots'])):
            try: text=data.decode('utf-8')
            except UnicodeDecodeError: errors.append(f"{path}: not UTF-8")
            else:
                if any(line.rstrip(' \t')!=line for line in text.splitlines()): errors.append(f"{path}: trailing whitespace")
                errors.extend(validate_markdown(repo_root,path,text,policy))
        violations.extend(errors)
        files.append({'path':path,'sha256':hashlib.sha256(data).hexdigest(),'status':'PASS' if not errors else 'FAIL'})
    return {
        'record_type':'SMT_TRANSITION_METRICS_VALIDATION',
        'schema_version':'1.0',
        'status':'PASS' if not violations else 'FAIL',
        'file_count':len(files),
        'files':files,
        'violations':violations,
    }



def committed_repository_path_errors(repo_root: Path, seed_paths: list[str], policy: dict[str, Any]) -> list[str]:
    """Require release-authorizing repository paths and their direct bindings to be exact HEAD regular blobs."""
    errors: list[str] = []
    queue = list(dict.fromkeys(seed_paths))
    seen: set[str] = set()
    while queue:
        raw = queue.pop(0)
        try:
            path = safe_rel(repo_root, raw)
        except (TypeError, ValueError) as exc:
            errors.append(f"committed repository path invalid: {raw!r}: {exc}")
            continue
        if path in seen:
            continue
        seen.add(path)
        try:
            require_worktree_matches_head_regular_blob(repo_root, path)
        except GitContractError as exc:
            errors.append(str(exc))
            continue
        full = repo_root / path
        if path.endswith('.json'):
            try:
                obj = load_json_strict(full)
            except Exception:
                continue
            if isinstance(obj, dict):
                for ref in sorted(referenced_repository_paths(obj)):
                    if ref not in seen:
                        queue.append(ref)
        elif path.endswith('.md'):
            try:
                text = full.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                continue
            vals = assignments(text).get(policy.get('transition_metrics_assignment', ''), [])
            for ref in vals:
                if isinstance(ref, str) and ref and ref not in seen:
                    queue.append(ref)
    return errors

def parse_args(argv:list[str]) -> argparse.Namespace:
    p=argparse.ArgumentParser()
    p.add_argument('--repo-root',default='.')
    p.add_argument('--policy',default=DEFAULT_POLICY)
    src=p.add_mutually_exclusive_group(required=True)
    src.add_argument('--base-ref')
    src.add_argument('--files',nargs='+')
    p.add_argument('--report',default=DEFAULT_REPORT)
    return p.parse_args(argv)


def main(argv:list[str]|None=None) -> int:
    args=parse_args(sys.argv[1:] if argv is None else argv)
    repo=Path(args.repo_root).resolve(strict=True)
    out=Path(args.report)
    if not out.is_absolute(): out=repo/out
    policy_path=Path(args.policy)
    if not policy_path.is_absolute(): policy_path=repo/policy_path
    try:
        policy_rel = repository_relative_file(repo, policy_path)
        policy=load_json_strict(policy_path)
        current_policy_errors = policy_shape_errors(policy, "current policy")
        if current_policy_errors:
            raise ValueError("; ".join(current_policy_errors))
    except Exception as exc:
        report = policy_failure_report(f"current policy invalid: {exc}", current_policy_path=str(args.policy))
        write_report(out, report)
        print(json.dumps(report,indent=2,sort_keys=True))
        return 1

    merge_base: str | None = None
    base_policy: dict[str, Any] | None = None
    base_policy_status = "NOT_APPLICABLE"
    historical_transition_paths: set[str] = set()
    historical_markdown_paths: set[str] = set()
    try:
        if args.base_ref:
            direct_paths, deleted_paths = changed_files(repo, args.base_ref)
            merge_base, base_policy, base_policy_status = load_base_policy_context(
                repo, args.base_ref, policy_path, policy
            )
            historical_transition_paths = base_transition_record_inventory(repo, merge_base, base_policy)
            historical_markdown_paths = base_governed_markdown_inventory(repo, merge_base, base_policy)
        else:
            direct_paths, deleted_paths = list(args.files), set()
    except Exception as exc:
        report = policy_failure_report(f"base-policy/governance classification failed: {exc}", current_policy_path=policy_rel)
        report["base_policy_status"] = "FAIL"
        write_report(out, report)
        print(json.dumps(report,indent=2,sort_keys=True))
        return 1


    try:
        direct_paths = sorted(set(direct_paths))
        changed_targets = set(direct_paths) | set(deleted_paths)
        reverse_index = build_reverse_reference_index(
            repo, policy, historical_transition_paths=historical_transition_paths, base_policy=base_policy
        )
        reverse_paths = reverse_reference_closure(repo, changed_targets, policy, reverse_index)
        validation_paths = sorted(set(direct_paths) | set(reverse_paths))
        base_governed_changed_paths = (
            base_transition_record_paths(set(direct_paths) | set(deleted_paths), historical_transition_paths)
            if args.base_ref else set()
        )
        required_transition_paths = historical_transition_paths.intersection(validation_paths)
        required_markdown_paths = historical_markdown_paths.intersection(validation_paths)
        base_governed_markdown_changed_paths = historical_markdown_paths.intersection(set(direct_paths) | set(deleted_paths))
        report=validate_files(
            repo, validation_paths, policy, required_transition_paths, required_markdown_paths
        )
        committed_errors = committed_repository_path_errors(repo, validation_paths, policy) if args.base_ref else []
        if committed_errors:
            report['violations'].extend(committed_errors)
            report['status'] = 'FAIL'
        deleted_transition_records = base_governed_changed_paths.intersection(deleted_paths)
        deleted_violations = validate_deleted_paths(
            repo, deleted_paths, policy, reverse_index, deleted_transition_records, base_policy
        )
        if deleted_violations:
            report['violations'].extend(deleted_violations)
            report['status'] = 'FAIL'
        report['direct_changed_paths'] = direct_paths
        report['reverse_reference_paths'] = reverse_paths
        report['validation_paths'] = validation_paths
        report['deleted_paths'] = sorted(deleted_paths)
        report['base_governed_changed_paths'] = sorted(base_governed_changed_paths)
        report['base_governed_markdown_paths'] = sorted(base_governed_markdown_changed_paths)
        report['base_governed_validation_paths'] = sorted(required_transition_paths)
        report['base_governed_markdown_validation_paths'] = sorted(required_markdown_paths)
        report['current_policy_path'] = policy_rel
        report['merge_base'] = merge_base
        report['base_policy_status'] = base_policy_status
        if args.base_ref:
            report['base_commit'] = resolve_commit(repo, args.base_ref)
            report['head_commit'], report['candidate_tree'] = head_commit_and_tree(repo)
    except Exception as exc:
        report = policy_failure_report(f"transition validation failed closed: {type(exc).__name__}: {exc}", current_policy_path=policy_rel)
        report['merge_base'] = merge_base
        report['base_policy_status'] = base_policy_status

    write_report(out, report)
    print(json.dumps(report,indent=2,sort_keys=True))
    return 0 if report['status']=='PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
