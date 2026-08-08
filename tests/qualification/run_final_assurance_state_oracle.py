from __future__ import annotations

import argparse
import concurrent.futures
import os
import hashlib
import subprocess
import contextlib
import io
import json
import sys
import unittest
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ORACLE_PATH = ROOT / "config/adp-transition-governance-final-assurance-state-oracle-r1.json"
CATALOG_PATH = ROOT / "tests/qualification/final_assurance_oracle_probe_catalog.json"

CONFIRMED = "CONFIRMED"
CONTRADICTED = "CONTRADICTED"
EVIDENCE_REQUIRED = "EVIDENCE_REQUIRED"
EXTERNAL_EVIDENCE_AUTHORIZATION_MODE = "HOLD_ONLY_UNTIL_TRUSTED_COLLECTOR"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def run_probe(probe_id: str) -> dict[str, Any]:
    suite = unittest.defaultTestLoader.loadTestsFromName(probe_id)
    unittest_stream = io.StringIO()
    probe_stdout = io.StringIO()
    probe_stderr = io.StringIO()
    with contextlib.redirect_stdout(probe_stdout), contextlib.redirect_stderr(probe_stderr):
        result = unittest.TextTestRunner(stream=unittest_stream, verbosity=0).run(suite)
    ok = result.wasSuccessful() and result.testsRun > 0
    return {
        "probe_id": probe_id,
        "status": CONFIRMED if ok else CONTRADICTED,
        "tests_run": result.testsRun,
        "unittest_output": unittest_stream.getvalue().strip(),
        "captured_stdout": probe_stdout.getvalue(),
        "captured_stderr": probe_stderr.getvalue(),
    }




class CapturingProbeResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.probe_records: dict[str, dict[str, Any]] = {}
        self._stdout_cm = None
        self._stderr_cm = None
        self._probe_stdout = None
        self._probe_stderr = None
        self._detail = ""
        self._status = CONTRADICTED

    def startTest(self, test):
        self._probe_stdout = io.StringIO()
        self._probe_stderr = io.StringIO()
        self._stdout_cm = contextlib.redirect_stdout(self._probe_stdout)
        self._stderr_cm = contextlib.redirect_stderr(self._probe_stderr)
        self._stdout_cm.__enter__(); self._stderr_cm.__enter__()
        self._detail = ""
        self._status = CONTRADICTED
        super().startTest(test)

    def addSuccess(self, test):
        self._status = CONFIRMED
        super().addSuccess(test)

    def addFailure(self, test, err):
        self._status = CONTRADICTED
        self._detail = self._exc_info_to_string(err, test)
        super().addFailure(test, err)

    def addError(self, test, err):
        self._status = CONTRADICTED
        self._detail = self._exc_info_to_string(err, test)
        super().addError(test, err)

    def addSkip(self, test, reason):
        self._status = CONTRADICTED
        self._detail = f"SKIPPED: {reason}"
        super().addSkip(test, reason)

    def stopTest(self, test):
        try:
            test_id = test.id()
            self.probe_records[test_id] = {
                "probe_id": test_id,
                "status": self._status,
                "tests_run": 1,
                "unittest_output": self._detail.strip(),
                "captured_stdout": self._probe_stdout.getvalue() if self._probe_stdout else "",
                "captured_stderr": self._probe_stderr.getvalue() if self._probe_stderr else "",
            }
        finally:
            if self._stderr_cm is not None: self._stderr_cm.__exit__(None, None, None)
            if self._stdout_cm is not None: self._stdout_cm.__exit__(None, None, None)
            super().stopTest(test)


def _flatten_suite(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from _flatten_suite(item)
        else:
            yield item


def run_probe_batch(probe_ids: list[str]) -> dict[str, dict[str, Any]]:
    suite = unittest.TestSuite()
    requested_to_actual: dict[str, str] = {}
    for probe_id in probe_ids:
        loaded = unittest.defaultTestLoader.loadTestsFromName(probe_id)
        tests = list(_flatten_suite(loaded))
        if len(tests) != 1:
            return {
                probe_id: {
                    "probe_id": probe_id,
                    "status": CONTRADICTED,
                    "tests_run": len(tests),
                    "unittest_output": f"probe must resolve to exactly one test, got {len(tests)}",
                    "captured_stdout": "",
                    "captured_stderr": "",
                }
                for probe_id in probe_ids
            }
        actual_id = tests[0].id()
        requested_to_actual[probe_id] = actual_id
        suite.addTest(tests[0])
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=0, resultclass=CapturingProbeResult).run(suite)
    records: dict[str, dict[str, Any]] = {}
    for requested, actual in requested_to_actual.items():
        rec = dict(result.probe_records.get(actual, {
            "probe_id": requested, "status": CONTRADICTED, "tests_run": 0,
            "unittest_output": "probe result missing", "captured_stdout": "", "captured_stderr": "",
        }))
        rec["probe_id"] = requested
        records[requested] = rec
    return records


def run_probe_batches_parallel(probe_ids: list[str], workers: int) -> dict[str, dict[str, Any]]:
    if not probe_ids:
        return {}
    if workers <= 1 or len(probe_ids) == 1:
        return run_probe_batch(probe_ids)
    worker_count = min(max(1, workers), len(probe_ids))
    shards: list[list[str]] = [[] for _ in range(worker_count)]
    for index, probe_id in enumerate(probe_ids):
        shards[index % worker_count].append(probe_id)
    merged: dict[str, dict[str, Any]] = {}
    with concurrent.futures.ProcessPoolExecutor(max_workers=worker_count) as pool:
        futures = [pool.submit(run_probe_batch, shard) for shard in shards if shard]
        for future in futures:
            records = future.result()
            overlap = set(merged).intersection(records)
            if overlap:
                raise ValueError(f"duplicate parallel probe results: {sorted(overlap)}")
            merged.update(records)
    if set(merged) != set(probe_ids):
        missing = sorted(set(probe_ids) - set(merged))
        extra = sorted(set(merged) - set(probe_ids))
        raise ValueError(f"parallel probe result mismatch missing={missing} extra={extra}")
    return merged



def unique_unittest_probe_ids(catalog_cells: list[dict[str, Any]]) -> list[str]:
    result: list[str] = []
    for catalog_row in catalog_cells:
        if catalog_row.get("probe_type") != "UNITTEST":
            continue
        for probe_id in catalog_row.get("probe_ids", []):
            if isinstance(probe_id, str) and probe_id and probe_id not in result:
                result.append(probe_id)
    return result


def exact_candidate_identity() -> tuple[str, str]:
    status = subprocess.run(["git", "status", "--porcelain=v1"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
    if status:
        raise ValueError("release-authorizing probe cache requires a clean committed candidate")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.strip()
    tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.strip()
    return head, tree


def write_probe_cache(path: Path, probe_ids: list[str], records: dict[str, dict[str, Any]], shard_index: int, shard_count: int) -> dict[str, Any]:
    missing = sorted(set(probe_ids) - set(records))
    extra = sorted(set(records) - set(probe_ids))
    status = "PASS" if not missing and not extra and all(records[p]["status"] == CONFIRMED for p in probe_ids) else "FAIL"
    head, tree = exact_candidate_identity()
    payload = {
        "record_type": "ADP_FINAL_ASSURANCE_UNITTEST_PROBE_CACHE_R1",
        "schema_version": "1.1",
        "candidate_head": head,
        "candidate_tree": tree,
        "oracle_sha256": hashlib.sha256(ORACLE_PATH.read_bytes()).hexdigest(),
        "catalog_sha256": hashlib.sha256(CATALOG_PATH.read_bytes()).hexdigest(),
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "shard_index": shard_index,
        "shard_count": shard_count,
        "status": status,
        "probe_count": len(probe_ids),
        "missing_probe_ids": missing,
        "extra_probe_ids": extra,
        "records": [records[p] for p in probe_ids if p in records],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def load_probe_caches(paths: list[Path], required_probe_ids: list[str]) -> dict[str, dict[str, Any]]:
    oracle_sha = hashlib.sha256(ORACLE_PATH.read_bytes()).hexdigest()
    catalog_sha = hashlib.sha256(CATALOG_PATH.read_bytes()).hexdigest()
    runner_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    candidate_head, candidate_tree = exact_candidate_identity()
    merged: dict[str, dict[str, Any]] = {}
    for path in paths:
        payload = load_object(path)
        if payload.get("record_type") != "ADP_FINAL_ASSURANCE_UNITTEST_PROBE_CACHE_R1":
            raise ValueError(f"{path}: invalid probe cache record_type")
        if (
            payload.get("candidate_head") != candidate_head
            or payload.get("candidate_tree") != candidate_tree
            or payload.get("oracle_sha256") != oracle_sha
            or payload.get("catalog_sha256") != catalog_sha
            or payload.get("runner_sha256") != runner_sha
        ):
            raise ValueError(f"{path}: stale probe cache binding")
        if payload.get("status") != "PASS":
            raise ValueError(f"{path}: probe shard did not PASS")
        records = payload.get("records")
        if not isinstance(records, list):
            raise ValueError(f"{path}: records must be a list")
        for record in records:
            if not isinstance(record, dict) or not isinstance(record.get("probe_id"), str):
                raise ValueError(f"{path}: invalid probe record")
            probe_id = record["probe_id"]
            if probe_id in merged:
                raise ValueError(f"duplicate cached probe {probe_id}")
            merged[probe_id] = record
    missing = sorted(set(required_probe_ids) - set(merged))
    extra = sorted(set(merged) - set(required_probe_ids))
    if missing or extra:
        raise ValueError(f"probe cache coverage mismatch missing={missing} extra={extra}")
    return merged


def load_external_evidence(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    value = load_object(path)
    if value.get("record_type") != "ADP_FINAL_ASSURANCE_EXTERNAL_EVIDENCE_R1":
        raise ValueError("external evidence record_type invalid")
    rows = value.get("cells")
    if not isinstance(rows, list):
        raise ValueError("external evidence cells must be a list")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("cell_id"), str):
            raise ValueError("external evidence row invalid")
        cid = row["cell_id"]
        if cid in result:
            raise ValueError(f"duplicate external evidence cell {cid}")
        result[cid] = row
    return result


def qualify(external_evidence_path: Path | None = None, workers: int = 1, probe_cache_paths: list[Path] | None = None) -> dict[str, Any]:
    oracle = load_object(ORACLE_PATH)
    catalog = load_object(CATALOG_PATH)
    external = load_external_evidence(external_evidence_path)
    oracle_cells = oracle.get("cells")
    catalog_cells = catalog.get("cells")
    if not isinstance(oracle_cells, list) or not isinstance(catalog_cells, list):
        raise ValueError("oracle and catalog cells must be lists")

    cat_by_id: dict[str, dict[str, Any]] = {}
    for row in catalog_cells:
        if not isinstance(row, dict) or not isinstance(row.get("cell_id"), str):
            raise ValueError("invalid probe catalog row")
        if "implementation_enforcement" in row:
            raise ValueError(f"{row['cell_id']}: self-declared implementation_enforcement is prohibited")
        cid = row["cell_id"]
        if cid in cat_by_id:
            raise ValueError(f"duplicate probe catalog cell {cid}")
        cat_by_id[cid] = row

    oracle_ids = [row.get("cell_id") for row in oracle_cells if isinstance(row, dict)]
    if len(oracle_ids) != len(set(oracle_ids)):
        raise ValueError("duplicate oracle cell_id")
    if set(cat_by_id) != set(oracle_ids):
        raise ValueError("probe catalog must exactly cover oracle cell IDs")

    rows: list[dict[str, Any]] = []
    confirmed = contradicted = evidence_required = 0
    unique_probe_ids = unique_unittest_probe_ids(catalog_cells)
    if probe_cache_paths:
        probe_cache = load_probe_caches(probe_cache_paths, unique_probe_ids)
    else:
        probe_cache = run_probe_batch(unique_probe_ids) if unique_probe_ids else {}
    for cell in oracle_cells:
        if not isinstance(cell, dict):
            raise ValueError("invalid oracle cell")
        cid = cell["cell_id"]
        expected = cell.get("expected_enforcement")
        evidence_class = cell.get("evidence_class")
        catalog_row = cat_by_id[cid]
        probe_type = catalog_row.get("probe_type")
        probe_results: list[dict[str, Any]] = []
        evidence_ids: list[str] = []
        observed_enforcement: str | None = None

        if probe_type == "UNITTEST":
            probe_ids = catalog_row.get("probe_ids")
            if not isinstance(probe_ids, list) or not probe_ids or any(not isinstance(x, str) or not x for x in probe_ids):
                cell_status = CONTRADICTED
                detail = "UNITTEST row requires non-empty probe_ids"
            else:
                probe_results = [probe_cache.get(probe_id, {
                    "probe_id": probe_id, "status": CONTRADICTED, "tests_run": 0,
                    "unittest_output": "probe result missing", "captured_stdout": "", "captured_stderr": "",
                }) for probe_id in probe_ids]
                cell_status = CONFIRMED if all(r["status"] == CONFIRMED for r in probe_results) else CONTRADICTED
                detail = "scenario assertion probes confirmed expected behavior" if cell_status == CONFIRMED else "one or more scenario assertion probes failed"
        elif probe_type == "EXTERNAL_EVIDENCE":
            ext = external.get(cid)
            if ext is not None:
                raw_observed = ext.get("observed_enforcement")
                if isinstance(raw_observed, str):
                    observed_enforcement = raw_observed
                raw_ids = ext.get("evidence_ids")
                if isinstance(raw_ids, list) and all(isinstance(x, str) and x for x in raw_ids):
                    evidence_ids = raw_ids
            cell_status = EVIDENCE_REQUIRED
            detail = (
                "external/live/process evidence is non-authorizing under Final Closure Override R1; "
                "this cell remains HOLD until a separately governed trusted external-evidence "
                "collector/verifier is implemented"
            )
        elif probe_type == "EVIDENCE_REQUIRED":
            cell_status = EVIDENCE_REQUIRED
            detail = "scenario-faithful behavioral/static probe has not yet been implemented"
        else:
            cell_status = CONTRADICTED
            detail = f"invalid probe_type {probe_type!r}"

        if cell_status == CONFIRMED:
            confirmed += 1
        elif cell_status == CONTRADICTED:
            contradicted += 1
        else:
            evidence_required += 1

        rows.append({
            "cell_id": cid,
            "domain": cell.get("domain"),
            "scenario": cell.get("scenario"),
            "applicable": cell.get("applicable") is True,
            "evidence_class": evidence_class,
            "oracle_expected_enforcement": expected,
            "cell_status": cell_status,
            "expectation_confirmed": cell_status == CONFIRMED,
            "observed_enforcement": observed_enforcement,
            "probe_type": probe_type,
            "probe_results": probe_results,
            "evidence_ids": evidence_ids,
            "detail": detail,
            "architecture_controls": cell.get("architecture_controls", []),
        })

    hard_missing = [
        row["cell_id"]
        for row in rows
        if row["cell_status"] == EVIDENCE_REQUIRED
        and row["evidence_class"] in {"BEHAVIORAL_EXECUTION", "STATIC_TRUST_CONTRACT"}
    ]
    deferred_external = [
        row["cell_id"]
        for row in rows
        if row["cell_status"] == EVIDENCE_REQUIRED
        and row["evidence_class"] in {"LIVE_GITHUB_STATE", "PROCESS_ARTIFACT_EVIDENCE"}
    ]

    if contradicted or hard_missing:
        status = "FAIL"
    elif deferred_external:
        status = "HOLD"
    elif confirmed == len(rows):
        status = "PASS"
    else:
        status = "FAIL"

    return {
        "record_type": "ADP_FINAL_ASSURANCE_STATE_ORACLE_QUALIFICATION_R2",
        "schema_version": "2.0",
        "source_head": oracle.get("source_head"),
        "source_main": oracle.get("source_main"),
        "oracle_policy_id": oracle.get("policy_id"),
        "status": status,
        "total_cells": len(rows),
        "confirmed_cells": confirmed,
        "contradicted_cells": contradicted,
        "evidence_required_cells": evidence_required,
        "hard_missing_probe_cells": hard_missing,
        "deferred_external_evidence_cells": deferred_external,
        "self_declared_observed_enforcement_fields": 0,
        "external_evidence_authorization_mode": EXTERNAL_EVIDENCE_AUTHORIZATION_MODE,
        "unique_unittest_probes_executed": len(probe_cache),
        "probe_workers": workers,
        "probe_cache_files": [str(p) for p in (probe_cache_paths or [])],
        "domain_counts": dict(sorted(Counter(row["domain"] for row in rows).items())),
        "evidence_class_counts": dict(sorted(Counter(row["evidence_class"] for row in rows).items())),
        "cell_status_counts": dict(sorted(Counter(row["cell_status"] for row in rows).items())),
        "cells": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("--external-evidence")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--probe-cache", action="append", default=[])
    parser.add_argument("--probe-shard-index", type=int)
    parser.add_argument("--probe-shard-count", type=int)
    parser.add_argument("--probe-cache-out")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    try:
        if args.probe_shard_index is not None or args.probe_shard_count is not None or args.probe_cache_out:
            if args.probe_shard_index is None or args.probe_shard_count is None or not args.probe_cache_out:
                raise ValueError("probe shard mode requires --probe-shard-index, --probe-shard-count, and --probe-cache-out")
            if args.probe_shard_count <= 0 or not 0 <= args.probe_shard_index < args.probe_shard_count:
                raise ValueError("invalid probe shard index/count")
            catalog = load_object(CATALOG_PATH)
            catalog_cells = catalog.get("cells")
            if not isinstance(catalog_cells, list):
                raise ValueError("catalog cells must be a list")
            all_probe_ids = unique_unittest_probe_ids(catalog_cells)
            shard_probe_ids = all_probe_ids[args.probe_shard_index::args.probe_shard_count]
            records = run_probe_batch(shard_probe_ids)
            result = write_probe_cache(Path(args.probe_cache_out), shard_probe_ids, records, args.probe_shard_index, args.probe_shard_count)
        else:
            result = qualify(
                Path(args.external_evidence) if args.external_evidence else None,
                workers=max(1, args.workers),
                probe_cache_paths=[Path(x) for x in args.probe_cache],
            )
    except Exception as exc:
        result = {
            "record_type": "ADP_FINAL_ASSURANCE_STATE_ORACLE_QUALIFICATION_R2",
            "schema_version": "2.0",
            "status": "FAIL",
            "fatal_error": f"{type(exc).__name__}: {exc}",
        }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result.get("status") == "PASS" else 2 if result.get("status") == "HOLD" else 1


if __name__ == "__main__":
    raise SystemExit(main())
