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


def load_json_strict(path: Path) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


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


def changed_files(repo_root: Path, base_ref: str) -> tuple[list[str], set[str]]:
    out = run_git(repo_root, ["diff", "--name-status", "--no-renames", "--diff-filter=ACMRD", f"{base_ref}...HEAD"])
    paths: list[str] = []
    deleted: set[str] = set()
    for raw in out.splitlines():
        if not raw.strip():
            continue
        fields = raw.split("\t")
        if len(fields) != 2:
            raise RuntimeError(f"unexpected git diff --name-status output: {raw}")
        status, path = fields
        path = path.strip()
        if not path:
            raise RuntimeError(f"empty changed path in git diff output: {raw}")
        if status == "D":
            deleted.add(path)
        else:
            paths.append(path)
    return sorted(set(paths)), deleted


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
    elif typ in {"EXTERNAL_ARTIFACT", "EXTERNAL_INCIDENT"}:
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
    if expected_record_types is not None and target.get("record_type") not in expected_record_types:
        errors.append(f"{context}: bound record has incompatible record_type: {rel}")
    if expected_workstream_id is not None and target.get("workstream_id") != expected_workstream_id:
        errors.append(f"{context}: bound record workstream_id mismatch: {rel}")
    if expected_snapshot_type is not None and target.get("snapshot_type") != expected_snapshot_type:
        errors.append(f"{context}: bound record snapshot_type must be {expected_snapshot_type}: {rel}")
    return target


def finite_number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    result = float(value)
    return result if math.isfinite(result) else None


def metric_value_domain(metric: dict[str, Any], definition: dict[str, Any], errors: list[str], context: str) -> None:
    dq = metric.get("data_quality")
    value = metric.get("value")
    if dq in {"UNKNOWN", "NOT_APPLICABLE"}:
        if value is not None:
            errors.append(f"{context}: {dq} metric value must be null")
        if not isinstance(metric.get("reason"), str) or not metric.get("reason", "").strip():
            errors.append(f"{context}: {dq} requires non-empty reason")
        if not isinstance(metric.get("collection_method"), str) or not metric.get("collection_method", "").strip():
            errors.append(f"{context}: {dq} requires collection_method")
        return
    if dq not in {"MEASURED", "DERIVED"}:
        errors.append(f"{context}: invalid data_quality {dq}")
        return
    refs = metric.get("evidence_refs")
    if not isinstance(refs, list) or not refs:
        errors.append(f"{context}: measured/derived metric requires evidence_refs")
    if not isinstance(metric.get("collection_method"), str) or not metric.get("collection_method", "").strip():
        errors.append(f"{context}: measured/derived metric requires collection_method")
    typ = definition["value_type"]
    if typ in {"COUNT", "DURATION_SECONDS"}:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            errors.append(f"{context}: {typ} value must be non-negative integer")
    elif typ == "PERCENT":
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)) or not (0 <= float(value) <= 100):
            errors.append(f"{context}: percent value must be finite in [0,100]")
    elif typ == "PASS_FAIL":
        if value not in {"PASS", "FAIL"}:
            errors.append(f"{context}: PASS_FAIL value must be PASS or FAIL")
    elif typ == "TEST_DISTRIBUTION":
        if not isinstance(value, dict):
            errors.append(f"{context}: TEST_DISTRIBUTION value must be object")


def ratio_check(metric: dict[str, Any], errors: list[str], context: str) -> None:
    if metric.get("data_quality") not in {"MEASURED","DERIVED"}:
        return
    num = metric.get("numerator")
    den = metric.get("denominator")
    if isinstance(num, bool) or isinstance(den, bool) or not isinstance(num, (int,float)) or not isinstance(den, (int,float)):
        errors.append(f"{context}: ratio metric requires numeric numerator and denominator")
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
    expected = float(num) / float(den) * 100.0
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
        iid = item.get("interval_id")
        if not isinstance(iid, str) or not iid or iid in ids:
            errors.append(f"{ctx}: interval_id missing or duplicate")
        else:
            ids.add(iid)
        cat = item.get("category")
        if cat not in policy["timing_categories"]:
            errors.append(f"{ctx}: invalid category {cat}")
        s, e = item.get("start_utc"), item.get("end_utc")
        if not utc(s) or not utc(e):
            errors.append(f"{ctx}: timestamps must be strict UTC")
            continue
        sd, ed = parse_time(s), parse_time(e)
        if ed < sd:
            errors.append(f"{ctx}: end before start")
            continue
        spans.append((sd,ed,cat,iid or str(idx)))
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
        rid=run.get("run_id")
        if not isinstance(rid,str) or not rid or rid in ids:
            errors.append(f"{ctx}: run_id missing or duplicate")
        else: ids.add(rid)
        layer=run.get("test_layer"); result=run.get("result")
        if not isinstance(layer,str) or not layer.strip(): errors.append(f"{ctx}: test_layer required")
        if result not in {"PASS","FAIL","BLOCKED"}: errors.append(f"{ctx}: invalid result")
        if not isinstance(run.get("release_authorizing"), bool): errors.append(f"{ctx}: release_authorizing must be boolean")
        for field in ["test_id","requirement_id","production_function_path","fixture_provenance","expected_result_source","actual_result","mutation_boundary","cleanup_preserve_behavior","evidence_artifact"]:
            if not isinstance(run.get(field),str) or not run.get(field," ").strip(): errors.append(f"{ctx}: {field} required")
        if isinstance(layer,str) and result in {"PASS","FAIL","BLOCKED"}: counts[(layer,result)] += 1
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
    if record.get("schema_version") != policy["schema_version"]: errors.append("schema_version mismatch")
    if record.get("snapshot_type") not in policy["snapshot_types"]: errors.append("invalid snapshot_type")
    if record.get("lifecycle_state") not in policy["lifecycle_states"]: errors.append("invalid lifecycle_state")
    if not utc(record.get("created_utc")): errors.append("created_utc invalid")
    if not isinstance(record.get("baseline_commit"),str) or not SHA1_RE.fullmatch(record.get("baseline_commit","")): errors.append("baseline_commit invalid")
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
        definition=policy["metrics"][mid]
        if m.get("name") != definition["name"]: errors.append(f"{ctx}: name mismatch")
        if m.get("unit") != definition["unit"]: errors.append(f"{ctx}: unit mismatch")
        metric_value_domain(m, definition, errors, ctx)
        for ref in m.get("evidence_refs", []) if isinstance(m.get("evidence_refs",[]),list) else []:
            validate_reference(repo_root, ref, errors, ctx)
        if definition.get("ratio_inputs_required_when_numeric"): ratio_check(m,errors,ctx)

    def numeric(mid:str) -> float | None:
        m=byid.get(mid,{})
        if m.get("data_quality") not in {"MEASURED","DERIVED"}:
            return None
        return finite_number(m.get("value"))
    for mid, expected in [('M21',ext),('M22',active)]:
        val=numeric(mid)
        if val is not None and val != expected: errors.append(f"{path}:{mid}: value does not match timing intervals")
    m23=byid.get('M23',{})
    if active == 0:
        if m23.get('data_quality') not in {'NOT_APPLICABLE','UNKNOWN'}: errors.append(f"{path}:M23: zero active denominator requires NOT_APPLICABLE or UNKNOWN")
    else:
        val23=numeric('M23')
        if val23 is not None:
            expected=rework/active*100.0
            if abs(val23-expected)>1e-9: errors.append(f"{path}:M23: value does not match rework/active ratio")
    m24=byid.get('M24',{})
    if m24.get('data_quality') in {'MEASURED','DERIVED'} and dist is not None and m24.get('value') != dist: errors.append(f"{path}:M24: distribution does not match test_runs")
    m25=byid.get('M25',{})
    if repeat_rate is None:
        if m25.get('data_quality') not in {'NOT_APPLICABLE','UNKNOWN'}: errors.append(f"{path}:M25: no defects requires NOT_APPLICABLE or UNKNOWN")
    elif m25.get('data_quality') in {'MEASURED','DERIVED'}:
        val25=numeric('M25')
        if val25 is not None and abs(val25-repeat_rate)>1e-9: errors.append(f"{path}:M25: value does not match defect ledger")

    m26=byid.get('M26',{})
    comps=record.get('handoff_components',[])
    if record.get('snapshot_type') == 'HANDOFF':
        if not isinstance(comps,list): errors.append(f"{path}: handoff_components must be list")
        else:
            cids=[c.get('component_id') if isinstance(c,dict) else None for c in comps]
            if cids != policy['required_handoff_components']: errors.append(f"{path}: M26 handoff components incomplete/out of order")
            present=0
            for idx,c in enumerate(comps):
                if not isinstance(c,dict):
                    continue
                cid=c.get('component_id')
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
            if m26.get('data_quality') not in {'MEASURED','DERIVED'} or val26 is None or abs(val26-expected)>1e-9:
                errors.append(f"{path}:M26 value mismatch")
            if expected != 100.0: errors.append(f"{path}: handoff completeness must be 100%")
    elif m26.get('data_quality') not in {'NOT_APPLICABLE','UNKNOWN'} and not comps:
        errors.append(f"{path}:M26 non-handoff snapshot without components must be NOT_APPLICABLE or UNKNOWN")

    good=0
    for mid in policy['m27_denominator_metric_ids']:
        m=byid.get(mid,{})
        dq=m.get('data_quality')
        method=isinstance(m.get('collection_method'),str) and bool(m.get('collection_method','').strip())
        if dq in {'MEASURED','DERIVED'}:
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
    if csv_path:
        try: rel=safe_rel(repo_root,csv_path)
        except ValueError as exc: errors.append(f"{path}: csv_projection_path {exc}")
        else:
            full=repo_root/rel
            if not full.is_file() or full.is_symlink(): errors.append(f"{path}: csv projection missing/non-regular: {rel}")
            else: errors.extend(validate_csv_projection(full, rows, path))
    return errors


def csv_cell(value: Any) -> str:
    if value is None: return ""
    if isinstance(value,(dict,list)): return json.dumps(value,sort_keys=True,separators=(",",":"))
    if isinstance(value,float): return format(value,'.12g')
    return str(value)


def validate_csv_projection(path: Path, rows: list[dict[str,Any]], context: str) -> list[str]:
    errors=[]
    expected_header=['metric_id','name','unit','value','data_quality','collection_method','reason']
    with path.open(newline='',encoding='utf-8') as fh:
        reader=csv.DictReader(fh)
        if reader.fieldnames != expected_header: return [f"{context}: CSV header mismatch"]
        actual=list(reader)
    if len(actual)!=len(rows): return [f"{context}: CSV row count mismatch"]
    for i,(a,m) in enumerate(zip(actual,rows)):
        expected={
            'metric_id':m.get('metric_id',''),'name':m.get('name',''),'unit':m.get('unit',''),
            'value':csv_cell(m.get('value')),'data_quality':m.get('data_quality',''),
            'collection_method':m.get('collection_method',''),'reason':m.get('reason','') or ''
        }
        if a != expected: errors.append(f"{context}: CSV row mismatch at index {i} metric {m.get('metric_id')}")
    return errors


def validate_event(repo_root: Path, path: str, record: dict[str,Any], policy: dict[str,Any]) -> list[str]:
    errors=[]
    if record.get('schema_version') != policy['schema_version']: errors.append('schema_version mismatch')
    if record.get('event_type') not in policy['event_types']: errors.append('invalid event_type')
    if not utc(record.get('created_utc')): errors.append('created_utc invalid')
    if not isinstance(record.get('workstream_id'),str) or not record.get('workstream_id','').strip(): errors.append('workstream_id required')
    if not isinstance(record.get('event_id'),str) or not record.get('event_id','').strip(): errors.append('event_id required')
    frm,to=record.get('lifecycle_from'),record.get('lifecycle_to')
    transition_events={'LIFECYCLE','RELEASE_RESET','LIVE_ATTEMPT'}
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
            for f in ['deviation_id','timestamp_utc','category','planned_condition','observed_condition','impact','mutation_status','evidence_reference','owner_disposition','permanent_control_decision']:
                if not isinstance(d.get(f),str) or not d.get(f,'').strip(): errors.append(f'deviation.{f} required')
            if d.get('timestamp_utc') and not utc(d.get('timestamp_utc')): errors.append('deviation.timestamp_utc invalid')
    if record.get('event_type') == 'QUALIFICATION_RUN':
        tr=record.get('test_run')
        if dist_from_runs([tr] if isinstance(tr,dict) else tr,errors) is None: errors.append('QUALIFICATION_RUN requires test_run')
    if record.get('event_type') == 'EXTERNAL_BLOCKER':
        ex=record.get('external_incident')
        if not isinstance(ex,dict): errors.append('EXTERNAL_BLOCKER requires external_incident')
        else:
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


def deleted_path_is_governed(path: str, policy: dict[str, Any]) -> bool:
    if path in TRANSITION_CANONICAL_PATHS or path.startswith("docs/Releases/metrics/"):
        return True
    if path.startswith("docs/Releases/"):
        lower = PurePosixPath(path).name.lower()
        keywords = list(policy.get("metrics_link_filename_keywords", [])) + list(policy.get("change_record_filename_keywords", []))
        return any(keyword in lower for keyword in keywords)
    return False


def record_references_path(value: Any, target: str) -> bool:
    if isinstance(value, dict):
        if value.get("path") == target or value.get("csv_projection_path") == target:
            return True
        return any(record_references_path(child, target) for child in value.values())
    if isinstance(value, list):
        return any(record_references_path(child, target) for child in value)
    return False


def deletion_reference_sources(repo_root: Path, target: str, policy: dict[str, Any]) -> list[str]:
    sources: list[str] = []
    releases = repo_root / "docs" / "Releases"
    if releases.is_dir():
        for full in sorted(releases.rglob("*.md")):
            if full.is_symlink() or not full.is_file():
                continue
            try:
                text = full.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            vals = assignments(text).get(policy["transition_metrics_assignment"], [])
            if target in vals:
                sources.append(full.relative_to(repo_root).as_posix())
    metrics = repo_root / "docs" / "Releases" / "metrics"
    if metrics.is_dir():
        for full in sorted(metrics.rglob("*.json")):
            if full.is_symlink() or not full.is_file():
                continue
            try:
                obj = load_json_strict(full)
            except Exception:
                continue
            if is_transition_json(obj, policy) and record_references_path(obj, target):
                sources.append(full.relative_to(repo_root).as_posix())
    return sorted(set(sources))


def validate_deleted_paths(repo_root: Path, deleted_paths: set[str], policy: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    for path in sorted(deleted_paths):
        if deleted_path_is_governed(path, policy):
            violations.append(f"{path}: deletion of governed transition artifact is prohibited")
        for source in deletion_reference_sources(repo_root, path, policy):
            violations.append(f"{path}: deletion creates dangling transition reference from {source}")
    return violations


def validate_files(repo_root: Path, paths: list[str], policy: dict[str,Any]) -> dict[str,Any]:
    violations=[]; files=[]
    for raw in sorted(set(paths)):
        try: path=safe_rel(repo_root,raw)
        except ValueError as exc: violations.append(str(exc)); continue
        full=repo_root/path
        if not full.exists(): violations.append(f"{path}: changed path does not exist"); continue
        if full.is_symlink() or not full.is_file(): violations.append(f"{path}: must be regular non-symlink file"); continue
        data=full.read_bytes()
        if b'\r' in data: violations.append(f"{path}: contains CR characters")
        errors=[]
        if path.endswith('.json'):
            try: obj=load_json_strict(full)
            except Exception as exc: errors.append(f"{path}: JSON parse failed: {exc}")
            else:
                if path.startswith('docs/Releases/metrics/') and not is_transition_json(obj,policy):
                    errors.append(f"{path}: unrecognized transition metrics record_type")
                elif is_transition_json(obj,policy):
                    if obj['record_type']==policy['record_types']['snapshot']: errors.extend(validate_snapshot(repo_root,path,obj,policy))
                    else: errors.extend(validate_event(repo_root,path,obj,policy))
        elif path.endswith('.md') and any(path.startswith(root) for root in policy['governed_markdown_roots']):
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
    policy_path=Path(args.policy)
    if not policy_path.is_absolute(): policy_path=repo/policy_path
    policy=load_json_strict(policy_path)
    if args.base_ref:
        paths, deleted_paths = changed_files(repo, args.base_ref)
    else:
        paths, deleted_paths = list(args.files), set()
    report=validate_files(repo,paths,policy)
    deleted_violations = validate_deleted_paths(repo, deleted_paths, policy)
    if deleted_violations:
        report['violations'].extend(deleted_violations)
        report['status'] = 'FAIL'
    report['deleted_paths'] = sorted(deleted_paths)
    out=Path(args.report)
    if not out.is_absolute(): out=repo/out
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2,sort_keys=True))
    return 0 if report['status']=='PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
