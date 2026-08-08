from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from tests.qualification import run_final_assurance_state_oracle as runner

ROOT = Path(__file__).resolve().parents[2]
ORACLE_PATH = ROOT / "config/adp-transition-governance-final-assurance-state-oracle-r1.json"
CATALOG_PATH = ROOT / "tests/qualification/final_assurance_oracle_probe_catalog.json"
ORACLE = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
CATALOG = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

EXPECTED_DOMAINS = {
    "COLLECTION_TIMELINESS",
    "COLLECTION_TRIGGER",
    "EXCEPTION_BINDING",
    "GIT_CHANGE_DISCOVERY",
    "GOVERNANCE_IDENTITY",
    "LIVE_RULESET",
    "MANDATORY_INVARIANT",
    "METRIC_RELEASE_DISPOSITION",
    "ORACLE_OUTPUT_INTEGRITY",
    "OWNER_EXCEPTION",
    "PARSER_SCHEMA",
    "RECORD_BEHAVIOR",
    "REFERENCE_GRAPH",
    "RELEASE_GATE_NEGATIVE",
    "REPORTING_PROCESS",
    "TRANSITION_POLICY",
    "TRUST_ROOT_MIGRATION",
    "WORKFLOW_TRUST_ROOT",
}
EXPECTED_EVIDENCE_CLASSES = {
    "BEHAVIORAL_EXECUTION",
    "STATIC_TRUST_CONTRACT",
    "LIVE_GITHUB_STATE",
    "PROCESS_ARTIFACT_EVIDENCE",
}


class OracleTests(unittest.TestCase):
    def test_identity_and_closed_denominator(self):
        self.assertEqual("ADP_TRANSITION_GOVERNANCE_FINAL_ASSURANCE_STATE_ORACLE_R1", ORACLE["policy_id"])
        self.assertEqual("2.0", ORACLE["schema_version"])
        self.assertEqual(374, ORACLE["applicable_cell_count"])
        self.assertEqual("PROHIBITED_WITHOUT_MATERIALITY_TEST", ORACLE["automatic_denominator_revision"])

    def test_exact_374_unique_applicable_cells(self):
        cells = ORACLE["cells"]
        ids = [row["cell_id"] for row in cells]
        self.assertEqual(374, len(cells))
        self.assertEqual(374, len(set(ids)))
        self.assertTrue(all(row.get("applicable") is True for row in cells))

    def test_all_cells_have_concrete_expected_outcomes(self):
        prohibited = {None, "", "CONTRACT_SPECIFIC", "TRIGGER_SPECIFIC_PASS_OR_FAIL", "AS_REFROZEN"}
        for row in ORACLE["cells"]:
            with self.subTest(cell=row["cell_id"]):
                self.assertNotIn(row.get("expected_enforcement"), prohibited)
                self.assertTrue(str(row.get("scenario", "")).strip())
                self.assertTrue(str(row.get("domain", "")).strip())
                self.assertIn(row.get("evidence_class"), EXPECTED_EVIDENCE_CLASSES)

    def test_required_domains_complete(self):
        self.assertEqual(EXPECTED_DOMAINS, {row["domain"] for row in ORACLE["cells"]})

    def test_catalog_exactly_covers_oracle_without_self_declared_enforcement(self):
        oracle_ids = [row["cell_id"] for row in ORACLE["cells"]]
        catalog_ids = [row["cell_id"] for row in CATALOG["cells"]]
        self.assertEqual(374, len(catalog_ids))
        self.assertEqual(set(oracle_ids), set(catalog_ids))
        self.assertEqual(len(catalog_ids), len(set(catalog_ids)))
        self.assertEqual("ADP_FINAL_ASSURANCE_IMPLEMENTATION_PROBE_CATALOG_R2", CATALOG["record_type"])
        self.assertTrue(all("implementation_enforcement" not in row for row in CATALOG["cells"]))

    def test_mi08_maps_exact_exception_deletion_and_type_change(self):
        row = next(row for row in CATALOG["cells"] if row["cell_id"] == "MI-08")
        self.assertEqual("UNITTEST", row["probe_type"])
        self.assertEqual(
            [
                "tests.test_validate_mandatory_assurance_invariants.MandatoryTests.test_base_ref_exception_record_deletion_fails",
                "tests.test_validate_mandatory_assurance_invariants.MandatoryTests.test_base_ref_exception_record_regular_to_symlink_T_fails",
            ],
            row["probe_ids"],
        )

    def test_runner_captures_probe_stdout_and_stderr(self):
        class NoiseCase(unittest.TestCase):
            def runTest(self):
                import sys
                print("PROBE_STDOUT_SENTINEL")
                print("PROBE_STDERR_SENTINEL", file=sys.stderr)
                self.assertTrue(True)
        suite = unittest.TestSuite([NoiseCase()])
        with mock.patch.object(unittest.defaultTestLoader, "loadTestsFromName", return_value=suite):
            result = runner.run_probe("synthetic.noise.probe")
        self.assertEqual("CONFIRMED", result["status"])
        self.assertEqual(1, result["tests_run"])
        self.assertIn("PROBE_STDOUT_SENTINEL", result["captured_stdout"])
        self.assertIn("PROBE_STDERR_SENTINEL", result["captured_stderr"])

    def test_external_evidence_must_bind_expected_enforcement(self):
        evidence = {
            "record_type": "ADP_FINAL_ASSURANCE_EXTERNAL_EVIDENCE_R1",
            "cells": [
                {
                    "cell_id": "LR-01",
                    "status": "CONFIRMED",
                    "observed_enforcement": "WRONG",
                    "evidence_ids": ["E1"],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "evidence.json"
            path.write_text(json.dumps(evidence), encoding="utf-8")
            loaded = runner.load_external_evidence(path)
            self.assertEqual("WRONG", loaded["LR-01"]["observed_enforcement"])


    def test_OI_03_probe_stderr_is_isolated(self):
        class StderrCase(unittest.TestCase):
            def runTest(self):
                import sys
                print("ONLY_PROBE_STDERR", file=sys.stderr)
        suite = unittest.TestSuite([StderrCase()])
        with mock.patch.object(unittest.defaultTestLoader, "loadTestsFromName", return_value=suite):
            result = runner.run_probe("synthetic.stderr.probe")
        self.assertEqual("CONFIRMED", result["status"])
        self.assertIn("ONLY_PROBE_STDERR", result["captured_stderr"])
        self.assertNotIn("ONLY_PROBE_STDERR", result["captured_stdout"])

    def test_OI_04_probe_json_stdout_is_captured_not_emitted_as_oracle_document(self):
        class JsonNoiseCase(unittest.TestCase):
            def runTest(self):
                print(json.dumps({"probe_document": True}))
        suite = unittest.TestSuite([JsonNoiseCase()])
        with mock.patch.object(unittest.defaultTestLoader, "loadTestsFromName", return_value=suite):
            result = runner.run_probe("synthetic.json.noise")
        self.assertEqual("CONFIRMED", result["status"])
        self.assertEqual({"probe_document": True}, json.loads(result["captured_stdout"]))

    def test_OI_05_thrown_probe_exception_is_bounded_contradiction(self):
        class ThrowCase(unittest.TestCase):
            def runTest(self):
                raise RuntimeError("bounded-probe-exception")
        suite = unittest.TestSuite([ThrowCase()])
        with mock.patch.object(unittest.defaultTestLoader, "loadTestsFromName", return_value=suite):
            result = runner.run_probe("synthetic.throw.probe")
        self.assertEqual("CONTRADICTED", result["status"])
        self.assertEqual(1, result["tests_run"])
        self.assertIn("bounded-probe-exception", result["unittest_output"])

    def test_OI_06_invalid_probe_protocol_or_external_binding_cannot_confirm_cell(self):
        oracle = {
            "policy_id": "TEST",
            "source_head": "a" * 40,
            "source_main": "b" * 40,
            "cells": [{
                "cell_id": "X-01", "domain": "TEST", "scenario": "x", "applicable": True,
                "evidence_class": "BEHAVIORAL_EXECUTION", "expected_enforcement": "FAIL_CLOSED",
            }],
        }
        catalog = {"cells": [{"cell_id": "X-01", "probe_type": "UNITTEST", "probe_ids": []}]}
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            op = td / "oracle.json"; cp = td / "catalog.json"
            op.write_text(json.dumps(oracle), encoding="utf-8")
            cp.write_text(json.dumps(catalog), encoding="utf-8")
            with mock.patch.object(runner, "ORACLE_PATH", op), mock.patch.object(runner, "CATALOG_PATH", cp):
                result = runner.qualify()
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("CONTRADICTED", result["cells"][0]["cell_status"])
        self.assertFalse(result["cells"][0]["expectation_confirmed"])

    def test_probe_cache_binds_exact_candidate_tree_and_runner(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "cache.json"
            records = {"probe.one": {"probe_id": "probe.one", "status": "CONFIRMED", "tests_run": 1, "unittest_output": "", "captured_stdout": "", "captured_stderr": ""}}
            with mock.patch.object(runner, "exact_candidate_identity", return_value=("h" * 40, "t" * 40)):
                payload = runner.write_probe_cache(cache, ["probe.one"], records, 0, 1)
                loaded = runner.load_probe_caches([cache], ["probe.one"])
            self.assertEqual("PASS", payload["status"])
            self.assertEqual("h" * 40, payload["candidate_head"])
            self.assertEqual("t" * 40, payload["candidate_tree"])
            self.assertEqual("CONFIRMED", loaded["probe.one"]["status"])

    def test_probe_cache_rejects_stale_candidate_binding(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "cache.json"
            records = {"probe.one": {"probe_id": "probe.one", "status": "CONFIRMED", "tests_run": 1, "unittest_output": "", "captured_stdout": "", "captured_stderr": ""}}
            with mock.patch.object(runner, "exact_candidate_identity", return_value=("h" * 40, "t" * 40)):
                runner.write_probe_cache(cache, ["probe.one"], records, 0, 1)
            with mock.patch.object(runner, "exact_candidate_identity", return_value=("x" * 40, "t" * 40)):
                with self.assertRaisesRegex(ValueError, "stale probe cache binding"):
                    runner.load_probe_caches([cache], ["probe.one"])

    def test_closure_rule_and_model_record_are_trust_root_artifacts(self):
        self.assertTrue((ROOT / "docs/Standards/ADP-Final-Assurance-Convergence-and-Closure-Rule-R1.md").is_file())
        self.assertTrue((ROOT / "docs/Releases/ADP-Transition-Governance-Repository-Integration-R1-Final-Assurance-Model-Convergence-Closure-R1.md").is_file())


if __name__ == "__main__":
    unittest.main()
