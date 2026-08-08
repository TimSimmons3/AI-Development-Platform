from __future__ import annotations

import hashlib
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
APPROVED_UTC = "2026-08-05T14:00:00Z"
COMMENT_UTC = "2026-08-05T15:00:00Z"
EVALUATION_UTC = "2026-08-05T16:00:00Z"
EXPIRATION_UTC = "2026-08-05T18:00:00Z"


def report(records=None, status="PASS"):
    values = RECORDS if records is None else records
    return {"status": status, "exception_record_count": len(values), "exception_records": values}


def comment(body, login=OWNER, created_at=COMMENT_UTC):
    return {"user": {"login": login}, "body": body, "created_at": created_at}


class OwnerApprovalTests(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp())
        (self.repo / "docs/Exceptions/Artifacts").mkdir(parents=True)
        (self.repo / "artifacts").mkdir(parents=True)
        self.artifact = self.repo / "artifacts/evidence.txt"
        self.artifact.write_text("evidence\n", encoding="utf-8")
        self.write_manifest()
        for record in RECORDS:
            self.write_exception(record)

    @property
    def manifest_rel(self):
        return "docs/Exceptions/Artifacts/EX-EVIDENCE.json"

    def write_manifest(self, artifacts=None):
        if artifacts is None:
            artifacts = [{
                "type": "REPO_PATH",
                "path": "artifacts/evidence.txt",
                "sha256": hashlib.sha256(self.artifact.read_bytes()).hexdigest(),
            }]
        path = self.repo / self.manifest_rel
        path.write_text(json.dumps({
            "record_type": owner_gate.ARTIFACT_MANIFEST_RECORD_TYPE,
            "schema_version": "1.0",
            "artifacts": artifacts,
        }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def exception_assignments(self, approved=APPROVED_UTC, expiration=EXPIRATION_UTC):
        manifest = json.loads((self.repo / self.manifest_rel).read_text(encoding="utf-8"))
        hash_set = ",".join(item["sha256"] for item in manifest["artifacts"])
        values = {
            "EXCEPTION_STATUS": "APPROVED",
            "APPROVED_BY": "Tim Simmons",
            "APPROVED_GITHUB_LOGIN": OWNER,
            "APPROVED_UTC": approved,
            "CONTROL_IDS": "CTRL-1",
            "SCOPE": "Exact test scope",
            "RATIONALE": "Bound test exception",
            "RESIDUAL_RISK": "LOW",
            "COMPENSATING_CONTROLS": "Independent validation",
            "EXPIRATION_UTC": expiration,
            "ARTIFACT_MANIFEST": self.manifest_rel,
            "ARTIFACT_SHA256_SET": hash_set,
        }
        mapping = {key: [value] for key, value in values.items()}
        values["APPROVAL_TEXT_SHA256"] = owner_gate.approval_basis_sha256(mapping)
        return values

    def write_exception(self, rel, **overrides):
        values = self.exception_assignments(
            approved=overrides.pop("APPROVED_UTC", APPROVED_UTC),
            expiration=overrides.pop("EXPIRATION_UTC", EXPIRATION_UTC),
        )
        values.update(overrides)
        order = [
            "EXCEPTION_STATUS", "APPROVED_BY", "APPROVED_GITHUB_LOGIN", "APPROVED_UTC",
            "APPROVAL_TEXT_SHA256", "CONTROL_IDS", "SCOPE", "RATIONALE", "RESIDUAL_RISK",
            "COMPENSATING_CONTROLS", "EXPIRATION_UTC", "ARTIFACT_MANIFEST", "ARTIFACT_SHA256_SET",
        ]
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(f"{key}={values[key]}" for key in order) + "\n", encoding="utf-8")
        return path

    def expected(self, records=RECORDS):
        return owner_gate.expected_approval(PR, HEAD, records)

    def validate(self, rep=None, comments=None, owner=OWNER, pr=PR, head=HEAD, evaluation=EVALUATION_UTC, repo=None):
        return owner_gate.validate_approval(
            rep or report(),
            [] if comments is None else comments,
            owner,
            pr,
            head,
            repo_root=self.repo if repo is None else repo,
            evaluation_utc=evaluation,
        )

    def test_no_exception_passes_without_comment(self):
        result = self.validate(rep=report([]))
        self.assertEqual("PASS", result["status"])
        self.assertFalse(result["approval_required"])

    def test_exact_owner_comment_and_bound_exception_records_pass(self):
        result = self.validate(comments=[comment(self.expected())])
        self.assertEqual("PASS", result["status"], result["violations"])
        self.assertEqual(1, result["matching_comment_count"])
        self.assertEqual(2, len(result["exception_bindings"]))

    def test_paginated_slurp_shape_passes(self):
        result = self.validate(comments=[[comment(self.expected())], []])
        self.assertEqual("PASS", result["status"], result["violations"])

    def test_wrong_owner_fails(self):
        self.assertEqual("FAIL", self.validate(comments=[comment(self.expected(), login="Other")])["status"])

    def test_wrong_pr_fails(self):
        wrong = owner_gate.expected_approval(PR + 1, HEAD, RECORDS)
        self.assertEqual("FAIL", self.validate(comments=[comment(wrong)])["status"])

    def test_stale_head_fails(self):
        stale = owner_gate.expected_approval(PR, "b" * 40, RECORDS)
        self.assertEqual("FAIL", self.validate(comments=[comment(stale)])["status"])

    def test_wrong_exception_set_fails(self):
        wrong = owner_gate.expected_approval(PR, HEAD, [RECORDS[0]])
        self.assertEqual("FAIL", self.validate(comments=[comment(wrong)])["status"])

    def test_extra_whitespace_fails(self):
        self.assertEqual("FAIL", self.validate(comments=[comment(self.expected() + " ")])["status"])

    def test_duplicate_exact_comments_fail(self):
        exact = comment(self.expected())
        result = self.validate(comments=[exact, exact])
        self.assertEqual("FAIL", result["status"])
        self.assertEqual(2, result["matching_comment_count"])

    def test_failed_invariant_report_fails(self):
        self.assertEqual("FAIL", self.validate(rep=report(status="FAIL"), comments=[comment(self.expected())])["status"])

    def test_unsorted_exception_records_fail(self):
        self.assertEqual("FAIL", self.validate(rep=report(list(reversed(RECORDS))), comments=[])["status"])

    def test_duplicate_exception_records_fail(self):
        self.assertEqual("FAIL", self.validate(rep=report([RECORDS[0], RECORDS[0]]), comments=[])["status"])

    def test_count_mismatch_fails(self):
        rep = report(); rep["exception_record_count"] = 1
        self.assertEqual("FAIL", self.validate(rep=rep, comments=[])["status"])

    def test_invalid_head_fails(self):
        self.assertEqual("FAIL", self.validate(comments=[], head="bad")["status"])

    def test_invalid_comments_root_fails(self):
        self.assertEqual("FAIL", self.validate(comments={"not": "a list"})["status"])

    def test_non_object_comment_fails(self):
        self.assertEqual("FAIL", self.validate(comments=["bad"])["status"])

    def test_canonical_approval_basis_hash_mismatch_fails(self):
        path = self.write_exception(RECORDS[0], APPROVAL_TEXT_SHA256="0" * 64)
        result = self.validate(comments=[comment(self.expected())])
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("APPROVAL_TEXT_SHA256" in x for x in result["violations"]), result)

    def test_artifact_file_digest_mismatch_fails(self):
        self.artifact.write_text("changed\n", encoding="utf-8")
        result = self.validate(comments=[comment(self.expected())])
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("artifact sha256 mismatch" in x for x in result["violations"]), result)

    def test_artifact_hash_set_mismatch_fails(self):
        self.write_exception(RECORDS[0], ARTIFACT_SHA256_SET="f" * 64)
        result = self.validate(comments=[comment(self.expected())])
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("ARTIFACT_SHA256_SET" in x for x in result["violations"]), result)

    def test_unsorted_artifact_manifest_fails(self):
        digest = hashlib.sha256(self.artifact.read_bytes()).hexdigest()
        self.write_manifest([
            {"type":"REPO_PATH","path":"z","sha256":digest},
            {"type":"REPO_PATH","path":"artifacts/evidence.txt","sha256":digest},
        ])
        self.write_exception(RECORDS[0])
        result = self.validate(comments=[comment(self.expected())])
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("sorted by canonical identity" in x for x in result["violations"]), result)

    def test_expired_at_evaluation_fails_including_equality(self):
        for evaluation in (EXPIRATION_UTC, "2026-08-05T19:00:00Z"):
            with self.subTest(evaluation=evaluation):
                result = self.validate(comments=[comment(self.expected())], evaluation=evaluation)
                self.assertEqual("FAIL", result["status"])
                self.assertTrue(any("expired at trusted evaluation" in x for x in result["violations"]), result)

    def test_comment_before_approved_utc_fails(self):
        result = self.validate(comments=[comment(self.expected(), created_at="2026-08-05T13:59:59Z")])
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("predates APPROVED_UTC" in x for x in result["violations"]), result)

    def test_comment_after_evaluation_fails(self):
        result = self.validate(comments=[comment(self.expected(), created_at="2026-08-05T17:00:00Z")])
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("later than trusted evaluation" in x for x in result["violations"]), result)

    def test_invalid_record_timestamp_order_fails(self):
        self.write_exception(RECORDS[0], APPROVED_UTC="2026-08-05T19:00:00Z", EXPIRATION_UTC="2026-08-05T18:00:00Z")
        result = self.validate(comments=[comment(self.expected())])
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("earlier than EXPIRATION_UTC" in x for x in result["violations"]), result)

    def test_missing_trusted_evaluation_time_fails(self):
        result = self.validate(comments=[comment(self.expected())], evaluation=None)
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any("evaluation_utc" in x for x in result["violations"]), result)

    def test_cli_success_writes_report(self):
        temp = Path(tempfile.mkdtemp())
        report_path = temp / "report.json"; comments_path = temp / "comments.json"; output_path = temp / "output.json"
        report_path.write_text(json.dumps(report()), encoding="utf-8")
        comments_path.write_text(json.dumps([comment(self.expected())]), encoding="utf-8")
        rc = owner_gate.main([
            "--report", str(report_path), "--comments", str(comments_path), "--owner-login", OWNER,
            "--pr-number", str(PR), "--head-sha", HEAD, "--repo-root", str(self.repo),
            "--evaluation-utc", EVALUATION_UTC, "--output", str(output_path),
        ])
        self.assertEqual(0, rc)
        self.assertEqual("PASS", json.loads(output_path.read_text())["status"])

    def test_strict_json_rejects_duplicate_keys(self):
        temp = Path(tempfile.mkdtemp()); path = temp / "bad.json"; path.write_text('{"a":1,"a":2}', encoding="utf-8")
        with self.assertRaises(ValueError): owner_gate.load_json_strict(path)

    def test_cli_malformed_json_is_structured_fail(self):
        temp = Path(tempfile.mkdtemp()); report_path=temp/"report.json";comments_path=temp/"comments.json";output_path=temp/"output.json"
        report_path.write_text("{bad", encoding="utf-8"); comments_path.write_text("[]", encoding="utf-8")
        rc=owner_gate.main(["--report",str(report_path),"--comments",str(comments_path),"--owner-login",OWNER,"--pr-number",str(PR),"--head-sha",HEAD,"--repo-root",str(self.repo),"--evaluation-utc",EVALUATION_UTC,"--output",str(output_path)])
        self.assertEqual(1,rc);result=json.loads(output_path.read_text());self.assertEqual("FAIL",result["status"]);self.assertTrue(result["violations"])

    def test_cli_oversized_json_is_structured_fail(self):
        temp=Path(tempfile.mkdtemp());report_path=temp/"report.json";comments_path=temp/"comments.json";output_path=temp/"output.json"
        report_path.write_bytes(b" "*(owner_gate.MAX_JSON_BYTES+1));comments_path.write_text("[]",encoding="utf-8")
        rc=owner_gate.main(["--report",str(report_path),"--comments",str(comments_path),"--owner-login",OWNER,"--pr-number",str(PR),"--head-sha",HEAD,"--repo-root",str(self.repo),"--evaluation-utc",EVALUATION_UTC,"--output",str(output_path)])
        self.assertEqual(1,rc);result=json.loads(output_path.read_text());self.assertEqual("FAIL",result["status"]);self.assertTrue(any("exceeds limit" in x for x in result["violations"]))


if __name__ == "__main__":
    unittest.main()
