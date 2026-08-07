from __future__ import annotations

import argparse
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
ALLOWED_ENFORCEMENT = {"FAIL_CLOSED", "VALIDATE_ALLOW", "CONTRACT_SPECIFIC", "HOLD_REQUALIFY"}


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def run_probe(probe_id: str) -> tuple[bool, int, str]:
    suite = unittest.defaultTestLoader.loadTestsFromName(probe_id)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
    ok = result.wasSuccessful() and result.testsRun > 0
    return ok, result.testsRun, stream.getvalue().strip()


def qualify() -> dict[str, Any]:
    oracle = load_object(ORACLE_PATH)
    catalog = load_object(CATALOG_PATH)
    oracle_cells = oracle.get("cells")
    catalog_cells = catalog.get("cells")
    if not isinstance(oracle_cells, list) or not isinstance(catalog_cells, list):
        raise ValueError("oracle and catalog cells must be lists")

    cat_by_id: dict[str, dict[str, Any]] = {}
    for row in catalog_cells:
        if not isinstance(row, dict) or not isinstance(row.get("cell_id"), str):
            raise ValueError("invalid probe catalog row")
        cid = row["cell_id"]
        if cid in cat_by_id:
            raise ValueError(f"duplicate probe catalog cell {cid}")
        cat_by_id[cid] = row

    rows: list[dict[str, Any]] = []
    deltas = 0
    probe_failures = 0
    applicable_count = 0
    for cell in oracle_cells:
        if not isinstance(cell, dict):
            raise ValueError("invalid oracle cell")
        cid = cell.get("cell_id")
        if not isinstance(cid, str) or not cid:
            raise ValueError("oracle cell_id invalid")
        applicable = cell.get("applicable") is True
        if applicable:
            applicable_count += 1
        expected = cell.get("expected_enforcement")
        if expected not in ALLOWED_ENFORCEMENT:
            raise ValueError(f"{cid}: invalid expected_enforcement {expected!r}")
        probe = cat_by_id.get(cid)
        if probe is None:
            ok, tests_run, detail = False, 0, "missing implementation probe"
            observed = "MISSING_PROBE"
        else:
            observed = probe.get("implementation_enforcement")
            probe_id = probe.get("probe_id")
            if probe.get("probe_type") != "UNITTEST" or not isinstance(probe_id, str) or not probe_id:
                ok, tests_run, detail = False, 0, "invalid implementation probe"
            else:
                ok, tests_run, detail = run_probe(probe_id)
        delta = expected != observed
        if delta:
            deltas += 1
        if applicable and not ok:
            probe_failures += 1
        rows.append({
            "cell_id": cid,
            "domain": cell.get("domain"),
            "applicable": applicable,
            "scenario": cell.get("scenario"),
            "oracle_expected_enforcement": expected,
            "implementation_observed_enforcement": observed,
            "expectation_delta": delta,
            "probe_id": probe.get("probe_id") if probe else None,
            "probe_pass": ok,
            "probe_tests_run": tests_run,
            "probe_detail": detail if not ok else "",
            "architecture_controls": cell.get("architecture_controls", []),
        })

    oracle_ids = [r.get("cell_id") for r in oracle_cells if isinstance(r, dict)]
    orphan_catalog = sorted(set(cat_by_id) - set(oracle_ids))
    missing_catalog = sorted(set(oracle_ids) - set(cat_by_id))
    disposition_count = sum(1 for r in rows if r["applicable"] and r["probe_pass"] and not r["expectation_delta"])
    applicable_disposition_pct = (100.0 * disposition_count / applicable_count) if applicable_count else 0.0
    status = "PASS" if (
        applicable_count == 108
        and disposition_count == applicable_count
        and deltas == 0
        and probe_failures == 0
        and not orphan_catalog
        and not missing_catalog
    ) else "FAIL"
    return {
        "record_type": "ADP_FINAL_ASSURANCE_STATE_ORACLE_QUALIFICATION_R1",
        "schema_version": "1.0",
        "source_head": oracle.get("source_head"),
        "oracle_policy_id": oracle.get("policy_id"),
        "status": status,
        "total_cells": len(rows),
        "applicable_cells": applicable_count,
        "disposed_applicable_cells": disposition_count,
        "applicable_cell_disposition_percent": applicable_disposition_pct,
        "expectation_delta_count": deltas,
        "probe_failure_count": probe_failures,
        "missing_probe_cells": missing_catalog,
        "orphan_probe_cells": orphan_catalog,
        "enforcement_counts": dict(sorted(Counter(r["oracle_expected_enforcement"] for r in rows).items())),
        "domain_counts": dict(sorted(Counter(r["domain"] for r in rows).items())),
        "cells": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    try:
        result = qualify()
    except Exception as exc:
        result = {
            "record_type": "ADP_FINAL_ASSURANCE_STATE_ORACLE_QUALIFICATION_R1",
            "schema_version": "1.0",
            "status": "FAIL",
            "fatal_error": f"{type(exc).__name__}: {exc}",
        }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
