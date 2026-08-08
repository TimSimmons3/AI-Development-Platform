#!/usr/bin/env python3
"""Validate permanent ADP post-R1 process institutionalization controls."""
from __future__ import annotations
import argparse, json, os, re, sys
from pathlib import Path, PurePosixPath
from typing import Any

EXPECTED_CONTROLS = [f"PI-{i:02d}" for i in range(1,17)]
EXPECTED_METRICS = [f"P{i:02d}" for i in range(1,15)]
EXPECTED_R1_COMMIT = "e599880ad7d1359efaf48c818b561275c069382e"
EXPECTED_R1_TREE = "533199b8332304b34501cddac3e1965005b11b45"
EXPECTED_R1_DENOMINATOR = 374
MAX_JSON = 1024 * 1024
MAX_TEXT = 2 * 1024 * 1024

def load_json_strict(path: Path, limit: int = MAX_JSON) -> Any:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"not regular file: {path}")
    data = path.read_bytes()
    if len(data) > limit:
        raise ValueError(f"JSON exceeds limit: {path}")
    text = data.decode("utf-8", "strict")
    def pairs(items):
        out = {}
        for k,v in items:
            if k in out:
                raise ValueError(f"duplicate JSON key: {k}")
            out[k]=v
        return out
    return json.loads(text, object_pairs_hook=pairs)

def safe_rel(value: str) -> str:
    if not isinstance(value,str) or not value:
        raise ValueError("empty path")
    p=PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts or "." in p.parts:
        raise ValueError(f"unsafe path: {value}")
    return p.as_posix()

def read_text(repo: Path, rel: str, limit: int = MAX_TEXT) -> str:
    rel=safe_rel(rel)
    path=repo/rel
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"required regular file missing: {rel}")
    data=path.read_bytes()
    if len(data)>limit:
        raise ValueError(f"text exceeds limit: {rel}")
    return data.decode("utf-8","strict")

def validate_policy_shape(policy: Any) -> list[str]:
    e=[]
    if not isinstance(policy,dict):
        return ["policy must be object"]
    if policy.get("policy_id")!="ADP_HIGH_ASSURANCE_PROCESS_INSTITUTIONALIZATION_R1": e.append("policy_id mismatch")
    if policy.get("schema_version")!="1.0": e.append("schema_version mismatch")
    src=policy.get("source_baseline")
    if not isinstance(src,dict): e.append("source_baseline missing")
    else:
        if src.get("main_commit")!=EXPECTED_R1_COMMIT: e.append("R1 source commit mismatch")
        if src.get("tree")!=EXPECTED_R1_TREE: e.append("R1 source tree mismatch")
        if src.get("r1_frozen_denominator")!=EXPECTED_R1_DENOMINATOR: e.append("R1 denominator mismatch")
        if src.get("r1_reopen_allowed") is not False: e.append("R1 reopen must be false")
    if policy.get("control_ids")!=EXPECTED_CONTROLS: e.append("control_ids must be exact PI-01..PI-16")
    metrics=policy.get("process_metrics")
    if not isinstance(metrics,dict) or sorted(metrics)!=EXPECTED_METRICS: e.append("process_metrics must be exact P01..P14")
    sections=policy.get("mandatory_handoff_sections")
    if not isinstance(sections,list) or len(sections)!=16 or len(set(sections))!=16 or any(not isinstance(x,str) or not x for x in sections):
        e.append("mandatory_handoff_sections must contain 16 unique nonempty sections")
    for key in ("required_artifacts","required_trust_root_paths","required_codeowners_paths","workflow","r1_frozen_oracle","external_evidence_fail_safe"):
        if key not in policy: e.append(f"policy missing {key}")
    return e

def validate_repo(repo: Path, policy: dict[str,Any]) -> dict[str,Any]:
    violations=validate_policy_shape(policy)
    checked=[]
    artifacts=policy.get("required_artifacts",{})
    if isinstance(artifacts,dict):
        for rel,markers in sorted(artifacts.items()):
            try:
                text=read_text(repo,rel)
            except Exception as exc:
                violations.append(str(exc)); continue
            checked.append(rel)
            if not isinstance(markers,list):
                violations.append(f"{rel}: marker list invalid"); continue
            for marker in markers:
                if not isinstance(marker,str) or marker not in text:
                    violations.append(f"{rel}: missing marker: {marker}")
    else:
        violations.append("required_artifacts must be object")

    try:
        manifest=load_json_strict(repo/"config/assurance-trust-root-manifest.json")
        trusted=manifest.get("trusted_paths") if isinstance(manifest,dict) else None
        if not isinstance(trusted,list): raise ValueError("trusted_paths missing")
        if trusted!=sorted(set(trusted)): violations.append("trusted_paths not sorted unique")
        for rel in policy.get("required_trust_root_paths",[]):
            if rel not in trusted: violations.append(f"trust root missing required path: {rel}")
    except Exception as exc:
        violations.append(f"trust-root manifest invalid: {exc}")

    try:
        codeowners=read_text(repo,".github/CODEOWNERS")
        for rel in policy.get("required_codeowners_paths",[]):
            expected=f"/{rel} @TimSimmons3"
            if expected not in codeowners.splitlines():
                violations.append(f"CODEOWNERS missing exact owner rule: {rel}")
    except Exception as exc:
        violations.append(f"CODEOWNERS invalid: {exc}")

    wf=policy.get("workflow",{})
    if isinstance(wf,dict):
        for key,marker_key in (("candidate_path","candidate_markers"),("trusted_path","trusted_markers")):
            try:
                text=read_text(repo,wf[key],MAX_JSON)
                for marker in wf.get(marker_key,[]):
                    if marker not in text: violations.append(f"{wf[key]}: missing workflow marker: {marker}")
            except Exception as exc:
                violations.append(f"workflow validation failed: {exc}")

    try:
        oracle=load_json_strict(repo/policy["r1_frozen_oracle"]["path"], 8*MAX_JSON)
        cells=oracle.get("cells") if isinstance(oracle,dict) else None
        if not isinstance(cells,list): raise ValueError("oracle cells missing")
        count=sum(1 for c in cells if isinstance(c,dict) and c.get("applicable") is not False)
        if count!=EXPECTED_R1_DENOMINATOR: violations.append(f"R1 oracle applicable count changed: {count}")
    except Exception as exc:
        violations.append(f"R1 frozen oracle validation failed: {exc}")

    try:
        ext=policy["external_evidence_fail_safe"]
        text=read_text(repo,ext["path"],MAX_TEXT)
        for marker in ext["markers"]:
            if marker not in text: violations.append(f"external evidence fail-safe missing marker: {marker}")
    except Exception as exc:
        violations.append(f"external evidence fail-safe validation failed: {exc}")

    return {
        "record_type":"ADP_PROCESS_INSTITUTIONALIZATION_VALIDATION",
        "schema_version":"1.0",
        "status":"PASS" if not violations else "FAIL",
        "control_count":16,
        "process_metric_count":14,
        "mandatory_handoff_section_count":16,
        "checked_artifact_count":len(checked),
        "violations":violations,
    }

def main(argv=None) -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--repo-root",default=".")
    p.add_argument("--policy",default="config/adp-process-institutionalization-policy.json")
    p.add_argument("--report",default="adp-process-institutionalization-validation-report.json")
    a=p.parse_args(sys.argv[1:] if argv is None else argv)
    repo=Path(a.repo_root).resolve(strict=True)
    policy_path=Path(a.policy)
    if not policy_path.is_absolute(): policy_path=repo/policy_path
    report_path=Path(a.report)
    if not report_path.is_absolute(): report_path=repo/report_path
    try:
        policy=load_json_strict(policy_path)
        result=validate_repo(repo,policy)
    except Exception as exc:
        result={"record_type":"ADP_PROCESS_INSTITUTIONALIZATION_VALIDATION","schema_version":"1.0","status":"FAIL","violations":[f"validation failed closed: {type(exc).__name__}: {exc}"]}
    report_path.parent.mkdir(parents=True,exist_ok=True)
    report_path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if result["status"]=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())
