#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import validate_transition_metrics as transition

RECORD_TYPE = "SMT_TRANSITION_RELEASE_ASSURANCE"
SCHEMA_VERSION = "1.0"

TRIGGER_CONTRACTS: dict[str, tuple[str, str, str]] = {
    "WORKSTREAM_START": ("snapshot", "snapshot_type", "WORKSTREAM_START"),
    "GATE": ("either", "trigger_type", "GATE"),
    "CLOSEOUT": ("snapshot", "snapshot_type", "CLOSEOUT"),
    "HANDOFF": ("snapshot", "snapshot_type", "HANDOFF"),
    "DEVIATION": ("event", "event_type", "DEVIATION"),
    "FAILURE": ("event", "event_type", "FAILURE"),
    "RELEASE_RESET": ("event", "event_type", "RELEASE_RESET"),
    "LIVE_ATTEMPT": ("event", "event_type", "LIVE_ATTEMPT"),
    "EXTERNAL_BLOCKER": ("event", "event_type", "EXTERNAL_BLOCKER"),
}

BLOCKING_METRIC_OUTCOMES = {
    "VALID_RECORD_HOLD",
    "VALID_RECORD_ACTIVE_BLOCKER_HOLD",
    "VALID_RECORD_HOLD_TARGET_NOT_EVALUABLE",
}


def finite_number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    try:
        number = float(value)
    except (OverflowError, ValueError, TypeError):
        return None
    return number if math.isfinite(number) else None


def metric_by_id(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = snapshot.get("metrics")
    if not isinstance(rows, list):
        return {}
    return {
        row["metric_id"]: row
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("metric_id"), str)
    }


def metric_value(metric: dict[str, Any]) -> Any:
    if metric.get("data_quality") not in {"MEASURED", "DERIVED"}:
        return None
    return metric.get("value")


def compare_numeric(value: Any, target: float, relation: str) -> bool | None:
    number = finite_number(value)
    if number is None:
        return None
    if relation == "eq":
        return abs(number - target) <= 1e-9
    if relation == "ge":
        return number >= target
    if relation == "lt":
        return number < target
    raise ValueError(f"unsupported relation: {relation}")


def evaluate_metric(
    metric_id: str,
    metric: dict[str, Any],
    *,
    prior_metric: dict[str, Any] | None = None,
    active_external_blocker: bool = False,
    evidence_status: str = "CONFIRMED",
) -> dict[str, Any]:
    dq = metric.get("data_quality")
    value = metric.get("value")
    result = {
        "metric_id": metric_id,
        "data_quality": dq,
        "value": value,
        "disposition": "TRACK_ONLY",
        "reason": "metric has no release threshold in R1",
    }
    if evidence_status == "CONTRADICTED":
        result.update(disposition="FAIL_CLOSED", reason="authoritative evidence contradicts the declared metric claim")
        return result
    if evidence_status != "CONFIRMED":
        result.update(disposition="VALID_RECORD_HOLD", reason="authoritative metric evidence is not confirmed")
        return result

    if dq == "UNKNOWN":
        result.update(
            disposition="VALID_RECORD_HOLD",
            reason="UNKNOWN is a valid data state but cannot satisfy a release target",
        )
        return result

    if dq == "NOT_APPLICABLE":
        if metric_id == "M23":
            result.update(
                disposition="VALID_RECORD_HOLD_TARGET_NOT_EVALUABLE",
                reason="M23 downward-trend target cannot be evaluated when active-work denominator is zero",
            )
        elif metric_id == "M25":
            result.update(
                disposition="VALID_RECORD_RELEASE_ELIGIBLE",
                reason="M25 is canonically NOT_APPLICABLE when there are no defects; no repeat defect exists",
            )
        else:
            result.update(
                disposition="NOT_APPLICABLE",
                reason="policy-valid NOT_APPLICABLE metric does not independently block release",
            )
        return result

    if metric_id in {"M01", "M05", "M08", "M13", "M14", "M16", "M27"}:
        met = compare_numeric(value, 100.0, "eq")
        result.update(
            disposition="VALID_RECORD_RELEASE_ELIGIBLE" if met else "VALID_RECORD_HOLD",
            reason="100 percent target met" if met else "100 percent target missed",
        )
        return result

    if metric_id in {"M02", "M03", "M04", "M07", "M09", "M18", "M28"}:
        met = compare_numeric(value, 0.0, "eq")
        result.update(
            disposition="VALID_RECORD_RELEASE_ELIGIBLE" if met else "VALID_RECORD_HOLD",
            reason="zero target met" if met else "zero target missed",
        )
        return result

    if metric_id == "M06":
        number = finite_number(value)
        if number is None:
            result.update(disposition="VALID_RECORD_HOLD", reason="M06 target cannot be evaluated")
        elif abs(number - 100.0) <= 1e-9:
            result.update(disposition="VALID_RECORD_RELEASE_ELIGIBLE", reason="100 percent target met")
        elif number >= 95.0:
            result.update(
                disposition="VALID_RECORD_THRESHOLD_MET_TARGET_MISSED",
                reason="minimum 95 percent threshold met but 100 percent target missed",
            )
        else:
            result.update(disposition="VALID_RECORD_HOLD", reason="M06 below 95 percent minimum")
        return result

    if metric_id in {"M10", "M11", "M12", "M15", "M17"}:
        met = value == "PASS"
        result.update(
            disposition="VALID_RECORD_RELEASE_ELIGIBLE" if met else "VALID_RECORD_HOLD",
            reason="PASS target met" if met else "PASS target missed",
        )
        return result

    if metric_id == "M19":
        number = finite_number(value)
        if number is not None and abs(number) <= 1e-9:
            result.update(disposition="VALID_RECORD_RELEASE_ELIGIBLE", reason="no owner exceptions")
        else:
            result.update(
                disposition="VALID_RECORD_GOVERNED_EXCEPTION",
                reason="one or more owner exceptions require exact governed authorization evidence",
            )
        return result

    if metric_id == "M20":
        number = finite_number(value)
        if active_external_blocker:
            result.update(
                disposition="VALID_RECORD_ACTIVE_BLOCKER_HOLD",
                reason="material external blocker remains active at release evaluation",
            )
        elif number is not None and abs(number) <= 1e-9:
            result.update(disposition="VALID_RECORD_RELEASE_ELIGIBLE", reason="no external blocker events")
        else:
            result.update(
                disposition="VALID_RECORD_TRACK",
                reason="external blocker history is resolved and retained as tracking evidence",
            )
        return result

    if metric_id == "M23":
        current = finite_number(value)
        prior = finite_number(metric_value(prior_metric or {}))
        if current is None or prior is None:
            result.update(
                disposition="VALID_RECORD_HOLD_TARGET_NOT_EVALUABLE",
                reason="M23 downward trend requires current and bound prior numeric values",
            )
        elif current < prior:
            result.update(disposition="VALID_RECORD_RELEASE_ELIGIBLE", reason="M23 downward trend target met")
        else:
            result.update(disposition="VALID_RECORD_HOLD", reason="M23 downward trend target missed")
        return result

    if metric_id == "M25":
        number = finite_number(value)
        met = number is not None and abs(number) <= 1e-9
        result.update(
            disposition="VALID_RECORD_RELEASE_ELIGIBLE" if met else "VALID_RECORD_HOLD",
            reason="M25 zero target met" if met else "M25 zero target missed",
        )
        return result

    return result


def validate_trigger_record(
    repo_root: Path,
    policy: dict[str, Any],
    trigger_id: str,
    record_path: str | None,
    workstream_id: str,
) -> dict[str, Any]:
    errors: list[str] = []
    if trigger_id not in TRIGGER_CONTRACTS:
        return {"trigger_id": trigger_id, "status": "FAIL", "violations": ["unknown trigger_id"]}
    if not isinstance(record_path, str) or not record_path.strip():
        return {"trigger_id": trigger_id, "status": "FAIL", "violations": ["required trigger record is missing"]}
    try:
        rel = transition.safe_rel(repo_root, record_path)
    except (TypeError, ValueError) as exc:
        return {"trigger_id": trigger_id, "status": "FAIL", "violations": [f"trigger record path invalid: {exc}"]}
    full = repo_root / rel
    if full.is_symlink() or not full.is_file():
        return {"trigger_id": trigger_id, "status": "FAIL", "violations": [f"trigger record missing/non-regular: {rel}"]}
    try:
        record = transition.load_json_strict(full, policy["resource_limits"]["json_bytes"])
    except Exception as exc:
        return {"trigger_id": trigger_id, "status": "FAIL", "violations": [f"trigger record parse failed: {type(exc).__name__}: {exc}"]}
    if not isinstance(record, dict):
        return {"trigger_id": trigger_id, "status": "FAIL", "violations": ["trigger record root must be object"]}
    if record.get("workstream_id") != workstream_id:
        errors.append("trigger record workstream_id mismatch")

    record_kind, _, expected_type = TRIGGER_CONTRACTS[trigger_id]
    snapshot_type = policy["record_types"]["snapshot"]
    event_type = policy["record_types"]["event"]
    actual_record_type = record.get("record_type")
    if record_kind == "snapshot":
        if actual_record_type != snapshot_type or record.get("snapshot_type") != expected_type:
            errors.append(f"trigger requires snapshot_type={expected_type}")
        else:
            errors.extend(transition.validate_snapshot(repo_root, rel, record, policy))
    elif record_kind == "event":
        if actual_record_type != event_type or record.get("event_type") != expected_type:
            errors.append(f"trigger requires event_type={expected_type}")
        else:
            errors.extend(transition.validate_event(repo_root, rel, record, policy))
    else:
        if actual_record_type == snapshot_type and record.get("snapshot_type") == expected_type:
            errors.extend(transition.validate_snapshot(repo_root, rel, record, policy))
        elif actual_record_type == event_type and record.get("event_type") == expected_type:
            errors.extend(transition.validate_event(repo_root, rel, record, policy))
        else:
            errors.append(f"trigger requires GATE snapshot or GATE event")
    return {
        "trigger_id": trigger_id,
        "record_path": rel,
        "status": "PASS" if not errors else "FAIL",
        "violations": errors,
    }


def load_prior_snapshot(repo_root: Path, snapshot: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any] | None:
    binding = snapshot.get("prior_handoff")
    if not isinstance(binding, dict):
        return None
    path = binding.get("path")
    if not isinstance(path, str):
        return None
    try:
        rel = transition.safe_rel(repo_root, path)
        value = transition.load_json_strict(repo_root / rel, policy["resource_limits"]["json_bytes"])
    except Exception:
        return None
    return value if isinstance(value, dict) else None


def evaluate_release_snapshot(
    repo_root: Path,
    policy: dict[str, Any],
    snapshot_path: str,
    *,
    active_external_blocker: bool = False,
    evidence_status: str = "CONFIRMED",
) -> dict[str, Any]:
    rel = transition.safe_rel(repo_root, snapshot_path)
    full = repo_root / rel
    try:
        snapshot = transition.load_json_strict(full, policy["resource_limits"]["json_bytes"])
    except Exception as exc:
        return {
            "snapshot_path": rel,
            "status": "FAIL",
            "release_state": "FAIL_CLOSED",
            "violations": [f"snapshot parse failed: {type(exc).__name__}: {exc}"],
            "metric_dispositions": [],
        }
    if not isinstance(snapshot, dict) or snapshot.get("record_type") != policy["record_types"]["snapshot"]:
        return {
            "snapshot_path": rel,
            "status": "FAIL",
            "release_state": "FAIL_CLOSED",
            "violations": ["release snapshot must be a transition metrics snapshot"],
            "metric_dispositions": [],
        }
    errors = transition.validate_snapshot(repo_root, rel, snapshot, policy)
    if errors:
        return {
            "snapshot_path": rel,
            "status": "FAIL",
            "release_state": "FAIL_CLOSED",
            "violations": errors,
            "metric_dispositions": [],
        }
    current = metric_by_id(snapshot)
    prior_snapshot = load_prior_snapshot(repo_root, snapshot, policy)
    prior = metric_by_id(prior_snapshot or {})
    rows: list[dict[str, Any]] = []
    for metric_id in policy["metric_order"]:
        if metric_id in {"M21", "M22", "M24", "M26"}:
            continue
        rows.append(
            evaluate_metric(
                metric_id,
                current.get(metric_id, {}),
                prior_metric=prior.get(metric_id),
                active_external_blocker=active_external_blocker if metric_id == "M20" else False,
            )
        )
    dispositions = {row["disposition"] for row in rows}
    if dispositions & BLOCKING_METRIC_OUTCOMES:
        release_state = "HOLD"
    elif "VALID_RECORD_GOVERNED_EXCEPTION" in dispositions:
        release_state = "GOVERNED_EXCEPTION"
    elif "VALID_RECORD_THRESHOLD_MET_TARGET_MISSED" in dispositions:
        release_state = "ELIGIBLE_WITH_TARGET_MISS"
    else:
        release_state = "ELIGIBLE"
    return {
        "snapshot_path": rel,
        "status": "PASS",
        "release_state": release_state,
        "violations": [],
        "metric_dispositions": rows,
    }


def git_is_ancestor(repo_root: Path, older: str, newer: str) -> bool:
    import subprocess
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        cwd=repo_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode == 0:
        return True
    if completed.returncode == 1:
        return False
    raise ValueError(f"git ancestry check failed: {completed.stderr.strip()}")


def evaluate_offline_collection_timeliness(
    repo_root: Path,
    *,
    trigger_commit: str,
    record_commit: str,
    next_transition_commit: str | None,
    declared_status: str,
) -> dict[str, Any]:
    """Evaluate deterministic offline collection ordering using commit ancestry only.

    CONTEMPORANEOUS is valid when the record is committed in the trigger commit or
    after it but no later than the next governed transition/gate. A truthful
    LATE_RECONSTRUCTION after the next transition is retained but places release
    on HOLD. A false contemporaneous claim or impossible ordering fails closed.
    """
    if declared_status not in {"CONTEMPORANEOUS", "LATE_RECONSTRUCTION"}:
        return {"status": "FAIL", "disposition": "FAIL_CLOSED", "reason": "invalid declared collection status"}
    try:
        trigger_before_record = git_is_ancestor(repo_root, trigger_commit, record_commit)
        if not trigger_before_record:
            return {"status": "FAIL", "disposition": "FAIL_CLOSED", "reason": "record commit precedes or is unrelated to trigger commit"}
        record_before_next = True
        if next_transition_commit is not None:
            if not git_is_ancestor(repo_root, trigger_commit, next_transition_commit):
                return {"status": "FAIL", "disposition": "FAIL_CLOSED", "reason": "next transition is not after trigger"}
            record_before_next = git_is_ancestor(repo_root, record_commit, next_transition_commit)
    except ValueError as exc:
        return {"status": "FAIL", "disposition": "FAIL_CLOSED", "reason": str(exc)}

    if record_before_next:
        if declared_status != "CONTEMPORANEOUS":
            return {"status": "FAIL", "disposition": "FAIL_CLOSED", "reason": "late-reconstruction claim contradicts commit ordering"}
        return {"status": "PASS", "disposition": "VALIDATE_ALLOW", "reason": "record committed before next governed transition"}
    if declared_status == "LATE_RECONSTRUCTION":
        return {"status": "PASS", "disposition": "VALID_RECORD_HOLD", "reason": "truthful late reconstruction retained after next governed transition"}
    return {"status": "FAIL", "disposition": "FAIL_CLOSED", "reason": "contemporaneous claim contradicts commit ordering"}


def validate_release_manifest(repo_root: Path, policy: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    if manifest.get("record_type") != "SMT_TRANSITION_RELEASE_MANIFEST":
        violations.append("manifest record_type must be SMT_TRANSITION_RELEASE_MANIFEST")
    if manifest.get("schema_version") != "1.0":
        violations.append("manifest schema_version must be 1.0")
    workstream_id = manifest.get("workstream_id")
    if not isinstance(workstream_id, str) or not workstream_id.strip():
        violations.append("manifest workstream_id is required")
        workstream_id = ""
    triggers = manifest.get("required_triggers")
    trigger_rows: list[dict[str, Any]] = []
    if not isinstance(triggers, list):
        violations.append("manifest required_triggers must be a list")
    else:
        seen: set[str] = set()
        for index, item in enumerate(triggers):
            if not isinstance(item, dict):
                violations.append(f"required_triggers[{index}] must be object")
                continue
            trigger_id = item.get("trigger_id")
            if not isinstance(trigger_id, str) or trigger_id not in TRIGGER_CONTRACTS:
                violations.append(f"required_triggers[{index}] trigger_id invalid")
                continue
            if trigger_id in seen:
                violations.append(f"duplicate required trigger: {trigger_id}")
                continue
            seen.add(trigger_id)
            row = validate_trigger_record(repo_root, policy, trigger_id, item.get("record_path"), workstream_id)
            trigger_rows.append(row)
            violations.extend(f"{trigger_id}: {message}" for message in row["violations"])
    snapshot_path = manifest.get("release_snapshot_path")
    release_result: dict[str, Any] | None = None
    if not isinstance(snapshot_path, str) or not snapshot_path.strip():
        violations.append("manifest release_snapshot_path is required")
    else:
        release_result = evaluate_release_snapshot(
            repo_root,
            policy,
            snapshot_path,
            active_external_blocker=manifest.get("active_external_blocker") is True,
        )
        if release_result["status"] != "PASS":
            violations.extend(release_result["violations"])
    status = "FAIL" if violations else "PASS"
    release_state = "FAIL_CLOSED" if violations else release_result["release_state"] if release_result else "HOLD"
    return {
        "record_type": RECORD_TYPE,
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "release_state": release_state,
        "workstream_id": workstream_id,
        "trigger_results": trigger_rows,
        "release_snapshot": release_result,
        "violations": violations,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--report", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    report_path = Path(args.report)
    try:
        repo_root = Path(args.repo_root).resolve(strict=True)
        policy = transition.load_json_strict(repo_root / args.policy)
        if not isinstance(policy, dict):
            raise ValueError("policy root must be object")
        manifest = transition.load_json_strict(repo_root / args.manifest)
        if not isinstance(manifest, dict):
            raise ValueError("manifest root must be object")
        result = validate_release_manifest(repo_root, policy, manifest)
    except Exception as exc:
        result = {
            "record_type": RECORD_TYPE,
            "schema_version": SCHEMA_VERSION,
            "status": "FAIL",
            "release_state": "FAIL_CLOSED",
            "workstream_id": None,
            "trigger_results": [],
            "release_snapshot": None,
            "violations": [f"release assurance failed closed: {type(exc).__name__}: {exc}"],
        }
    report_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if result["status"] == "PASS" and result["release_state"] not in {"HOLD", "FAIL_CLOSED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
