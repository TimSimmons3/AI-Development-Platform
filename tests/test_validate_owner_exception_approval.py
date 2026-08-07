from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_owner_exception_approval.py"
SPEC = importlib.util.spec_from_file_location("owner_gate", MODULE_PATH)
assert SPEC and SPEC.loader
owner_gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(owner_gate)

OWNER = "TimSimmons3"
PR = 17
HEAD = "a" * 40
RECORDS = ["docs/Exceptions/EX-001.md", "docs/Exceptions/EX-002.md"]


def report(records=None, status="PASS"):
    values = RECORDS if records is None else records
    return {
        "status": status,
        "exception_record_count": len(values),
        "exception_records": values,
    }


def comment(body, login=OWNER):
    return {"user": {"login": login}, "body": body}


class OwnerApprovalTests(unittest.TestCase):
    def expected(self):
        return owner_gate.expected_approval(PR, HEAD, RECORDS)

    def validate(self, rep=None, comments=None, owner=OWNER, pr=PR, head=HEAD):
        return owner_gate.validate_approval(
            rep or report(), [] if comments is None else comments, owner, pr, head
        )

    def test_no_exception_passes_without_comment(self):
        result = self.validate(rep=report([]))
        self.assertEqual("PASS", result["status"])
        self.assertFalse(result["approval_required"])

    def test_exact_owner_comment_passes(self):
        result = self.validate(comments=[comment(self.expected())])
        self.assertEqual("PASS", result["status"], result["violations"])
        self.assertEqual(1, result["matching_comment_count"])

    def test_paginated_slurp_shape_passes(self):
        result = self.validate(comments=[[comment(self.expected())], []])
        self.assertEqual("PASS", result["status"], result["violations"])

    def test_wrong_owner_fails(self):
        result = self.validate(comments=[comment(self.expected(), login="Other")])
        self.assertEqual("FAIL", result["status"])

    def test_wrong_pr_fails(self):
        wrong = owner_gate.expected_approval(PR + 1, HEAD, RECORDS)
        result = self.validate(comments=[comment(wrong)])
        self.assertEqual("FAIL", result["status"])

    def test_stale_head_fails(self):
        stale = owner_gate.expected_approval(PR, "b" * 40, RECORDS)
        result = self.validate(comments=[comment(stale)])
        self.assertEqual("FAIL", result["status"])

    def test_wrong_exception_set_fails(self):
        wrong = owner_gate.expected_approval(PR, HEAD, [RECORDS[0]])
        result = self.validate(comments=[comment(wrong)])
        self.assertEqual("FAIL", result["status"])

    def test_extra_whitespace_fails(self):
        result = self.validate(comments=[comment(self.expected() + " ")])
        self.assertEqual("FAIL", result["status"])

    def test_duplicate_exact_comments_fail(self):
        exact = comment(self.expected())
        result = self.validate(comments=[exact, exact])
        self.assertEqual("FAIL", result["status"])
        self.assertEqual(2, result["matching_comment_count"])

    def test_failed_invariant_report_fails(self):
        result = self.validate(rep=report(status="FAIL"), comments=[comment(self.expected())])
        self.assertEqual("FAIL", result["status"])

    def test_unsorted_exception_records_fail(self):
        result = self.validate(rep=report(list(reversed(RECORDS))), comments=[])
        self.assertEqual("FAIL", result["status"])

    def test_duplicate_exception_records_fail(self):
        result = self.validate(rep=report([RECORDS[0], RECORDS[0]]), comments=[])
        self.assertEqual("FAIL", result["status"])

    def test_count_mismatch_fails(self):
        rep = report()
        rep["exception_record_count"] = 1
        result = self.validate(rep=rep, comments=[])
        self.assertEqual("FAIL", result["status"])

    def test_invalid_head_fails(self):
        result = self.validate(comments=[], head="bad")
        self.assertEqual("FAIL", result["status"])

    def test_invalid_comments_root_fails(self):
        result = self.validate(comments={"not": "a list"})
        self.assertEqual("FAIL", result["status"])

    def test_non_object_comment_fails(self):
        result = self.validate(comments=["bad"])
        self.assertEqual("FAIL", result["status"])

    def test_cli_success_writes_report(self):
        temp = Path(tempfile.mkdtemp())
        report_path = temp / "report.json"
        comments_path = temp / "comments.json"
        output_path = temp / "output.json"
        report_path.write_text(json.dumps(report()), encoding="utf-8")
        comments_path.write_text(json.dumps([comment(self.expected())]), encoding="utf-8")
        rc = owner_gate.main([
            "--report", str(report_path),
            "--comments", str(comments_path),
            "--owner-login", OWNER,
            "--pr-number", str(PR),
            "--head-sha", HEAD,
            "--output", str(output_path),
        ])
        self.assertEqual(0, rc)
        self.assertEqual("PASS", json.loads(output_path.read_text())["status"])

    def test_strict_json_rejects_duplicate_keys(self):
        temp = Path(tempfile.mkdtemp())
        path = temp / "bad.json"
        path.write_text('{"a":1,"a":2}', encoding="utf-8")
        with self.assertRaises(ValueError):
            owner_gate.load_json_strict(path)

    def test_cli_malformed_json_is_structured_fail(self):
        temp = Path(tempfile.mkdtemp())
        report_path = temp / "report.json"
        comments_path = temp / "comments.json"
        output_path = temp / "output.json"
        report_path.write_text("{bad", encoding="utf-8")
        comments_path.write_text("[]", encoding="utf-8")
        rc = owner_gate.main([
            "--report", str(report_path), "--comments", str(comments_path),
            "--owner-login", OWNER, "--pr-number", str(PR),
            "--head-sha", HEAD, "--output", str(output_path),
        ])
        self.assertEqual(1, rc)
        result = json.loads(output_path.read_text())
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(result["violations"])

    def test_cli_oversized_json_is_structured_fail(self):
        temp = Path(tempfile.mkdtemp())
        report_path = temp / "report.json"
        comments_path = temp / "comments.json"
        output_path = temp / "output.json"
        report_path.write_bytes(b" " * (owner_gate.MAX_JSON_BYTES + 1))
        comments_path.write_text("[]", encoding="utf-8")
        rc = owner_gate.main([
            "--report", str(report_path), "--comments", str(comments_path),
            "--owner-login", OWNER, "--pr-number", str(PR),
            "--head-sha", HEAD, "--output", str(output_path),
        ])
        self.assertEqual(1, rc)
        result = json.loads(output_path.read_text())
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("exceeds limit" in x for x in result["violations"]))


if __name__ == "__main__":
    unittest.main()
