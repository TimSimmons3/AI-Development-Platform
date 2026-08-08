#!/usr/bin/env python3
"""Validate permanent ADP post-R1 process institutionalization controls."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

EXPECTED_CONTROLS = [f"PI-{i:02d}" for i in range(1, 17)]
EXPECTED_METRICS = [f"P{i:02d}" for i in range(1, 15)]
EXPECTED_R1_COMMIT = "e599880ad7d1359efaf48c818b561275c069382e"
EXPECTED_R1_TREE = "533199b8332304b34501cddac3e1965005b11b45"
EXPECTED_R1_DENOMINATOR = 374
PROCESS_METRICS_RECORD_TYPE = "ADP_PROCESS_ASSURANCE_METRICS"
ALLOWED_METRIC_STATUS = {"PASS", "HOLD", "FAIL", "TRACK"}
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
ASSIGNMENT_RE = re.compile(r"^([A-Z][A-Z0-9_]*)=(.*)$")
MAX_JSON = 1024 * 1024
MAX_TEXT = 2 * 1024 * 1024
POLICY_PATH = "config/adp-process-institutionalization-policy.json"

def load_json_text_strict(text: str) -> Any:
    def pairs(items):
        out = {}
        for k, v in items:
            if k in out:
                raise ValueError(f"duplicate JSON key: {k}")
            out[k] = v
        return out
    return json.loads(text, object_pairs_hook=pairs)

def load_json_strict(path: Path, limit: int = MAX_JSON) -> Any:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"not regular file: {path}")
    data = path.read_bytes()
    if len(data) > limit:
        raise ValueError(f"JSON exceeds limit: {path}")
    return load_json_text_strict(data.decode("utf-8", "strict"))

def safe_rel(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("empty path")
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts or "." in p.parts:
        raise ValueError(f"unsafe path: {value}")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in p.as_posix()):
        raise ValueError(f"path contains prohibited control character: {value!r}")
    return p.as_posix()

def read_text(repo: Path, rel: str, limit: int = MAX_TEXT) -> str:
    rel = safe_rel(rel)
    path = repo / rel
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"required regular file missing: {rel}")
    data = path.read_bytes()
    if len(data) > limit:
        raise ValueError(f"text exceeds limit: {rel}")
    return data.decode("utf-8", "strict")

def run_git(repo: Path, args: list[str]) -> str:
    try:
        p = subprocess.run(
            ["git", *args], cwd=repo, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"git {' '.join(args)} execution failed: {type(exc).__name__}: {exc}") from exc
    if p.returncode:
        raise ValueError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p.stdout

def git_object_text(repo: Path, commit: str, rel: str) -> str | None:
    rel = safe_rel(rel)
    exists = run_git(repo, ["ls-tree", "--name-only", commit, "--", rel])
    if rel not in {line.strip() for line in exists.splitlines() if line.strip()}:
        return None
    size_text = run_git(repo, ["cat-file", "-s", f"{commit}:{rel}"]).strip()
    try:
        size = int(size_text)
    except ValueError as exc:
        raise ValueError(f"historical object size invalid: {rel}") from exc
    if size > MAX_JSON:
        raise ValueError(f"historical JSON exceeds limit: {rel}")
    return run_git(repo, ["show", f"{commit}:{rel}"])

def validate_policy_shape(policy: Any) -> list[str]:
    e: list[str] = []
    if not isinstance(policy, dict):
        return ["policy must be object"]
    required_top = {
        "policy_id", "schema_version", "effective_date", "source_baseline",
        "control_ids", "process_metrics", "mandatory_handoff_sections",
        "required_artifacts", "required_trust_root_paths", "required_codeowners_paths",
        "workflow", "r1_frozen_oracle", "external_evidence_fail_safe",
        "resource_limits", "instance_enforcement",
    }
    extra = sorted(set(policy) - required_top)
    missing = sorted(required_top - set(policy))
    if extra:
        e.append(f"policy unexpected top-level fields: {','.join(extra)}")
    if missing:
        e.append(f"policy missing top-level fields: {','.join(missing)}")
    if policy.get("policy_id") != "ADP_HIGH_ASSURANCE_PROCESS_INSTITUTIONALIZATION_R1":
        e.append("policy_id mismatch")
    if policy.get("schema_version") != "1.0":
        e.append("schema_version mismatch")
    if policy.get("effective_date") != "2026-08-08":
        e.append("effective_date mismatch")
    expected_src = {
        "main_commit": EXPECTED_R1_COMMIT,
        "tree": EXPECTED_R1_TREE,
        "r1_status": "ADMINISTRATIVELY_CLOSED_AND_RECOVERABLE",
        "r1_frozen_denominator": EXPECTED_R1_DENOMINATOR,
        "r1_reopen_allowed": False,
    }
    if policy.get("source_baseline") != expected_src:
        e.append("source_baseline must remain exact closed R1 identity")
    if policy.get("control_ids") != EXPECTED_CONTROLS:
        e.append("control_ids must be exact PI-01..PI-16")
    metrics = policy.get("process_metrics")
    if not isinstance(metrics, dict) or sorted(metrics) != EXPECTED_METRICS:
        e.append("process_metrics must be exact P01..P14")
    elif any(
        not isinstance(metrics[mid], dict)
        or not isinstance(metrics[mid].get("name"), str)
        or not metrics[mid].get("name")
        or not isinstance(metrics[mid].get("target"), str)
        or not metrics[mid].get("target")
        for mid in EXPECTED_METRICS
    ):
        e.append("process_metrics definitions must have nonempty name and target")
    sections = policy.get("mandatory_handoff_sections")
    if not isinstance(sections, list) or len(sections) != 16 or len(set(sections)) != 16 or any(
        not isinstance(x, str) or not x for x in sections
    ):
        e.append("mandatory_handoff_sections must contain 16 unique nonempty sections")
    for key in ("required_artifacts", "workflow", "r1_frozen_oracle", "external_evidence_fail_safe", "instance_enforcement"):
        if not isinstance(policy.get(key), dict):
            e.append(f"{key} must be object")
    for key in ("required_trust_root_paths", "required_codeowners_paths"):
        value = policy.get(key)
        if not isinstance(value, list) or value != sorted(set(value)) or any(not isinstance(x, str) or not x for x in value):
            e.append(f"{key} must be sorted unique nonempty strings")
    if policy.get("resource_limits") != {"json_bytes": MAX_JSON, "markdown_bytes": MAX_TEXT, "yaml_bytes": MAX_JSON}:
        e.append("resource_limits mismatch")
    inst = policy.get("instance_enforcement")
    if isinstance(inst, dict):
        if inst.get("process_metrics_assignment") != "PROCESS_ASSURANCE_METRICS_RECORD":
            e.append("instance_enforcement process_metrics_assignment mismatch")
        if inst.get("process_metrics_record_type") != PROCESS_METRICS_RECORD_TYPE:
            e.append("instance_enforcement process_metrics_record_type mismatch")
        if inst.get("handoff_roots") != ["docs/Integration/", "docs/Releases/"]:
            e.append("instance_enforcement handoff_roots mismatch")
        if inst.get("handoff_filename_keywords") != ["continuation", "handoff"]:
            e.append("instance_enforcement handoff_filename_keywords mismatch")
        if inst.get("process_metrics_instance_roots") != [
            "docs/Integration/process-metrics/",
            "docs/Releases/process-metrics/",
        ]:
            e.append("instance_enforcement process_metrics_instance_roots mismatch")
        if inst.get("process_metrics_template_path") != "docs/Templates/SMT-Process-Assurance-Metrics-Template.json":
            e.append("instance_enforcement process_metrics_template_path mismatch")
    return e

def policy_compatibility_errors(base: dict[str, Any], current: dict[str, Any]) -> list[str]:
    e: list[str] = []
    immutable = [
        "policy_id", "schema_version", "effective_date", "source_baseline",
        "control_ids", "process_metrics", "mandatory_handoff_sections",
        "workflow", "r1_frozen_oracle", "external_evidence_fail_safe",
        "resource_limits", "instance_enforcement",
    ]
    for field in immutable:
        if base.get(field) != current.get(field):
            e.append(f"process institutionalization policy {field} is immutable after bootstrap")
    for field in ("required_trust_root_paths", "required_codeowners_paths"):
        before = base.get(field, [])
        after = current.get(field, [])
        if not isinstance(before, list) or not isinstance(after, list):
            e.append(f"process institutionalization policy {field} must remain lists")
        else:
            removed = sorted(set(before) - set(after))
            if removed:
                e.append(f"process institutionalization policy {field} may not remove paths: {','.join(removed)}")
    before_art = base.get("required_artifacts", {})
    after_art = current.get("required_artifacts", {})
    if not isinstance(before_art, dict) or not isinstance(after_art, dict):
        e.append("process institutionalization required_artifacts must remain objects")
    else:
        for rel, markers in before_art.items():
            if rel not in after_art:
                e.append(f"process institutionalization required_artifacts may not remove artifact: {rel}")
                continue
            before_markers = markers if isinstance(markers, list) else []
            after_markers = after_art[rel] if isinstance(after_art[rel], list) else []
            removed = sorted(set(before_markers) - set(after_markers))
            if removed:
                e.append(f"process institutionalization required_artifacts may not remove markers from {rel}: {','.join(removed)}")
    return e

def assignments(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for raw in text.splitlines():
        m = ASSIGNMENT_RE.fullmatch(raw.strip())
        if m:
            result.setdefault(m.group(1), []).append(m.group(2))
    return result

def valid_utc(value: Any) -> bool:
    if not isinstance(value, str) or not UTC_RE.fullmatch(value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return False
    return True

def validate_process_metrics_record(record: Any, policy: dict[str, Any], context: str) -> list[str]:
    e: list[str] = []
    if not isinstance(record, dict):
        return [f"{context}: process metrics record must be object"]
    expected_fields = {
        "record_type", "schema_version", "workstream_id", "candidate_head",
        "candidate_tree", "created_utc", "metrics",
    }
    extra = sorted(set(record) - expected_fields)
    missing = sorted(expected_fields - set(record))
    if extra:
        e.append(f"{context}: unexpected fields: {','.join(extra)}")
    if missing:
        e.append(f"{context}: missing fields: {','.join(missing)}")
    if record.get("record_type") != PROCESS_METRICS_RECORD_TYPE:
        e.append(f"{context}: record_type mismatch")
    if record.get("schema_version") != "1.0":
        e.append(f"{context}: schema_version mismatch")
    if not isinstance(record.get("workstream_id"), str) or not record.get("workstream_id", "").strip():
        e.append(f"{context}: workstream_id required")
    if not isinstance(record.get("candidate_head"), str) or not SHA1_RE.fullmatch(record.get("candidate_head", "")):
        e.append(f"{context}: candidate_head must be 40-character lowercase SHA")
    if not isinstance(record.get("candidate_tree"), str) or not SHA1_RE.fullmatch(record.get("candidate_tree", "")):
        e.append(f"{context}: candidate_tree must be 40-character lowercase SHA")
    if not valid_utc(record.get("created_utc")):
        e.append(f"{context}: created_utc must be valid strict UTC")
    rows = record.get("metrics")
    if not isinstance(rows, list):
        return e + [f"{context}: metrics must be list"]
    ids = [row.get("metric_id") if isinstance(row, dict) else None for row in rows]
    if ids != EXPECTED_METRICS:
        e.append(f"{context}: metrics must contain P01-P14 exactly once in canonical order")
    policy_metrics = policy.get("process_metrics", {})
    expected_row_fields = {"metric_id", "name", "target", "value", "status", "evidence_refs"}
    for idx, row in enumerate(rows):
        ctx = f"{context}:metrics[{idx}]"
        if not isinstance(row, dict):
            e.append(f"{ctx}: must be object")
            continue
        extra_row = sorted(set(row) - expected_row_fields)
        missing_row = sorted(expected_row_fields - set(row))
        if extra_row:
            e.append(f"{ctx}: unexpected fields: {','.join(extra_row)}")
        if missing_row:
            e.append(f"{ctx}: missing fields: {','.join(missing_row)}")
        mid = row.get("metric_id")
        definition = policy_metrics.get(mid) if isinstance(mid, str) else None
        if not isinstance(definition, dict):
            e.append(f"{ctx}: unsupported metric_id")
            continue
        if row.get("name") != definition.get("name"):
            e.append(f"{ctx}: name mismatch")
        if row.get("target") != definition.get("target"):
            e.append(f"{ctx}: target mismatch")
        if row.get("status") not in ALLOWED_METRIC_STATUS:
            e.append(f"{ctx}: status must be PASS/HOLD/FAIL/TRACK")
        value = row.get("value")
        if value is None or (isinstance(value, str) and (not value.strip() or "<" in value or "REQUIRED" in value.upper())):
            e.append(f"{ctx}: concrete value required")
        refs = row.get("evidence_refs")
        if not isinstance(refs, list) or not refs or any(not isinstance(x, str) or not x.strip() for x in refs):
            e.append(f"{ctx}: evidence_refs must be nonempty string list")
    return e

def is_handoff_path(path: str, policy: dict[str, Any]) -> bool:
    inst = policy.get("instance_enforcement", {})
    lower = PurePosixPath(path).name.lower()
    return (
        path.lower().endswith(".md")
        and any(path.startswith(root) for root in inst.get("handoff_roots", []))
        and any(keyword in lower for keyword in inst.get("handoff_filename_keywords", []))
    )

def is_process_metrics_instance_path(path: str, policy: dict[str, Any]) -> bool:
    roots = policy.get("instance_enforcement", {}).get("process_metrics_instance_roots", [])
    return path.lower().endswith(".json") and any(path.startswith(root) for root in roots)

def validate_handoff_document(repo: Path, rel: str, text: str, policy: dict[str, Any]) -> list[str]:
    e: list[str] = []
    for section in policy["mandatory_handoff_sections"]:
        pattern = re.compile(rf"(?m)^##\s+(?:\d+\.\s+)?{re.escape(section)}\s*$")
        if not pattern.search(text):
            e.append(f"{rel}: missing mandatory handoff section: {section}")
    assn = assignments(text)
    key = policy["instance_enforcement"]["process_metrics_assignment"]
    values = assn.get(key, [])
    if len(values) != 1:
        e.append(f"{rel}: requires exactly one {key}")
        return e
    try:
        metrics_rel = safe_rel(values[0])
    except ValueError as exc:
        e.append(f"{rel}: process metrics path {exc}")
        return e
    if not is_process_metrics_instance_path(metrics_rel, policy):
        e.append(f"{rel}: process metrics record must be under a governed process-metrics instance root: {metrics_rel}")
        return e
    if metrics_rel == policy["instance_enforcement"]["process_metrics_template_path"]:
        e.append(f"{rel}: canonical process metrics template may not be used as a live metrics record")
        return e
    full = repo / metrics_rel
    if full.is_symlink() or not full.is_file():
        e.append(f"{rel}: process metrics record missing/non-regular: {metrics_rel}")
        return e
    try:
        record = load_json_strict(full)
    except Exception as exc:
        e.append(f"{rel}: process metrics record parse failed: {type(exc).__name__}: {exc}")
        return e
    e.extend(validate_process_metrics_record(record, policy, metrics_rel))
    return e

def changed_paths(repo: Path, base_ref: str) -> tuple[str, list[str], list[str]]:
    base = run_git(repo, ["rev-parse", f"{base_ref}^{{commit}}"]).strip()
    head = run_git(repo, ["rev-parse", "HEAD^{commit}"]).strip()
    merge_base = run_git(repo, ["merge-base", base, head]).strip()
    if merge_base != base:
        raise ValueError(f"base freshness failure: merge-base {merge_base} != base {base}")
    raw = run_git(repo, ["diff", "--name-only", "-z", f"{base}...{head}"])
    changed = [safe_rel(x) for x in raw.split("\0") if x]
    deleted_raw = run_git(repo, ["diff", "--diff-filter=D", "--name-only", "-z", f"{base}...{head}"])
    deleted = [safe_rel(x) for x in deleted_raw.split("\0") if x]
    return base, sorted(set(changed)), sorted(set(deleted))

def validate_base_policy(repo: Path, base_commit: str, current_policy: dict[str, Any]) -> list[str]:
    text = git_object_text(repo, base_commit, POLICY_PATH)
    if text is None:
        base_tree = run_git(repo, ["rev-parse", f"{base_commit}^{{tree}}"]).strip()
        if base_commit != EXPECTED_R1_COMMIT or base_tree != EXPECTED_R1_TREE:
            return ["process policy bootstrap allowed only from exact closed R1 baseline"]
        return []
    try:
        base_policy = load_json_text_strict(text)
    except Exception as exc:
        return [f"merge-base process policy parse failed: {type(exc).__name__}: {exc}"]
    errors = validate_policy_shape(base_policy)
    if errors:
        return [f"merge-base process policy invalid: {x}" for x in errors]
    return policy_compatibility_errors(base_policy, current_policy)

def validate_repo(repo: Path, policy: dict[str, Any], base_ref: str | None = None) -> dict[str, Any]:
    violations = validate_policy_shape(policy)
    checked: list[str] = []
    artifacts = policy.get("required_artifacts", {})
    if isinstance(artifacts, dict):
        for rel, markers in sorted(artifacts.items()):
            try:
                text = read_text(repo, rel)
            except Exception as exc:
                violations.append(str(exc))
                continue
            checked.append(rel)
            if not isinstance(markers, list):
                violations.append(f"{rel}: marker list invalid")
                continue
            for marker in markers:
                if not isinstance(marker, str) or marker not in text:
                    violations.append(f"{rel}: missing marker: {marker}")
    else:
        violations.append("required_artifacts must be object")
    try:
        manifest = load_json_strict(repo / "config/assurance-trust-root-manifest.json")
        trusted = manifest.get("trusted_paths") if isinstance(manifest, dict) else None
        if not isinstance(trusted, list):
            raise ValueError("trusted_paths missing")
        if trusted != sorted(set(trusted)):
            violations.append("trusted_paths not sorted unique")
        for rel in policy.get("required_trust_root_paths", []):
            if rel not in trusted:
                violations.append(f"trust root missing required path: {rel}")
    except Exception as exc:
        violations.append(f"trust-root manifest invalid: {exc}")
    try:
        codeowners = read_text(repo, ".github/CODEOWNERS")
        lines = codeowners.splitlines()
        for rel in policy.get("required_codeowners_paths", []):
            expected = f"/{rel} @TimSimmons3"
            if expected not in lines:
                violations.append(f"CODEOWNERS missing exact owner rule: {rel}")
    except Exception as exc:
        violations.append(f"CODEOWNERS invalid: {exc}")
    wf = policy.get("workflow", {})
    if isinstance(wf, dict):
        for key, marker_key in (("candidate_path", "candidate_markers"), ("trusted_path", "trusted_markers")):
            try:
                text = read_text(repo, wf[key], MAX_JSON)
                for marker in wf.get(marker_key, []):
                    if marker not in text:
                        violations.append(f"{wf[key]}: missing workflow marker: {marker}")
            except Exception as exc:
                violations.append(f"workflow validation failed: {exc}")
    try:
        oracle = load_json_strict(repo / policy["r1_frozen_oracle"]["path"], 8 * MAX_JSON)
        cells = oracle.get("cells") if isinstance(oracle, dict) else None
        if not isinstance(cells, list):
            raise ValueError("oracle cells missing")
        count = sum(1 for c in cells if isinstance(c, dict) and c.get("applicable") is not False)
        if count != EXPECTED_R1_DENOMINATOR:
            violations.append(f"R1 oracle applicable count changed: {count}")
    except Exception as exc:
        violations.append(f"R1 frozen oracle validation failed: {exc}")
    try:
        ext = policy["external_evidence_fail_safe"]
        text = read_text(repo, ext["path"], MAX_TEXT)
        for marker in ext["markers"]:
            if marker not in text:
                violations.append(f"external evidence fail-safe missing marker: {marker}")
    except Exception as exc:
        violations.append(f"external evidence fail-safe validation failed: {exc}")

    changed: list[str] = []
    deleted: list[str] = []
    base_commit: str | None = None
    instance_count = 0
    if base_ref is not None:
        try:
            base_commit, changed, deleted = changed_paths(repo, base_ref)
            violations.extend(validate_base_policy(repo, base_commit, policy))
            for rel in deleted:
                if is_handoff_path(rel, policy):
                    violations.append(f"{rel}: governed handoff deletion requires separate owner disposition")
            for rel in changed:
                full = repo / rel
                if rel in deleted or full.is_symlink() or not full.is_file():
                    continue
                if is_handoff_path(rel, policy):
                    instance_count += 1
                    try:
                        text = read_text(repo, rel)
                    except Exception as exc:
                        violations.append(str(exc))
                    else:
                        violations.extend(validate_handoff_document(repo, rel, text, policy))
                elif is_process_metrics_instance_path(rel, policy):
                    instance_count += 1
                    try:
                        obj = load_json_strict(full)
                    except Exception as exc:
                        violations.append(f"{rel}: process metrics instance parse failed: {type(exc).__name__}: {exc}")
                        continue
                    violations.extend(validate_process_metrics_record(obj, policy, rel))
        except Exception as exc:
            violations.append(f"committed-delta instance validation failed: {type(exc).__name__}: {exc}")

    return {
        "record_type": "ADP_PROCESS_INSTITUTIONALIZATION_VALIDATION",
        "schema_version": "1.0",
        "status": "PASS" if not violations else "FAIL",
        "control_count": 16,
        "process_metric_count": 14,
        "mandatory_handoff_section_count": 16,
        "checked_artifact_count": len(checked),
        "base_commit": base_commit,
        "changed_path_count": len(changed),
        "deleted_path_count": len(deleted),
        "validated_instance_count": instance_count,
        "violations": violations,
    }

def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", default=".")
    p.add_argument("--policy", default=POLICY_PATH)
    p.add_argument("--base-ref")
    p.add_argument("--report", default="adp-process-institutionalization-validation-report.json")
    a = p.parse_args(sys.argv[1:] if argv is None else argv)
    repo = Path(a.repo_root).resolve(strict=True)
    policy_path = Path(a.policy)
    if not policy_path.is_absolute():
        policy_path = repo / policy_path
    report_path = Path(a.report)
    if not report_path.is_absolute():
        report_path = repo / report_path
    try:
        policy = load_json_strict(policy_path)
        result = validate_repo(repo, policy, a.base_ref)
    except Exception as exc:
        result = {
            "record_type": "ADP_PROCESS_INSTITUTIONALIZATION_VALIDATION",
            "schema_version": "1.0",
            "status": "FAIL",
            "violations": [f"validation failed closed: {type(exc).__name__}: {exc}"],
        }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
