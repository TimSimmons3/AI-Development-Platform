from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_mandatory_assurance_invariants.py"
SPEC = importlib.util.spec_from_file_location("validator", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

POLICY = json.loads((ROOT / "config" / "mandatory-assurance-invariant-policy.json").read_text())


def block(status: str = "NOT_GRANTED") -> str:
    lines = []
    for key in POLICY["required_block_order"]:
        value = POLICY["required_block"][key]
        if key == "EXCEPTION_STATUS":
            value = status
        lines.append(f"{key}={value}")
    return "```text\n" + "\n".join(lines) + "\n```\n"


class ValidatorTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temp = Path(tempfile.mkdtemp())
        (temp / "config").mkdir()
        (temp / "docs" / "Releases").mkdir(parents=True)
        (temp / "docs" / "Exceptions").mkdir(parents=True)
        (temp / "config" / "mandatory-assurance-invariant-policy.json").write_text(
            json.dumps(POLICY), encoding="utf-8"
        )
        return temp

    def validate(self, repo: Path, *paths: str):
        return validator.validate_files(repo, list(paths), POLICY)

    def test_valid_governed_document_passes(self):
        repo = self.make_repo()
        path = repo / "docs" / "Releases" / "Test-Plan.md"
        path.write_text("# Plan\n\n" + block(), encoding="utf-8")
        report = self.validate(repo, "docs/Releases/Test-Plan.md")
        self.assertEqual("PASS", report["status"])

    def test_missing_required_line_fails(self):
        repo = self.make_repo()
        text = block().replace("PATCH_AND_RETRY_CYCLE=PROHIBITED\n", "")
        path = repo / "docs" / "Releases" / "Test-Plan.md"
        path.write_text(text, encoding="utf-8")
        report = self.validate(repo, "docs/Releases/Test-Plan.md")
        self.assertEqual("FAIL", report["status"])
        self.assertTrue(any("PATCH_AND_RETRY_CYCLE" in item for item in report["violations"]))

    def test_duplicate_assignment_fails(self):
        repo = self.make_repo()
        path = repo / "docs" / "Releases" / "Test-Plan.md"
        path.write_text(block() + "EXCEPTION_STATUS=NOT_GRANTED\n", encoding="utf-8")
        report = self.validate(repo, "docs/Releases/Test-Plan.md")
        self.assertEqual("FAIL", report["status"])

    def test_approved_without_record_fails(self):
        repo = self.make_repo()
        path = repo / "docs" / "Releases" / "Test-Plan.md"
        path.write_text(block("APPROVED"), encoding="utf-8")
        report = self.validate(repo, "docs/Releases/Test-Plan.md")
        self.assertEqual("FAIL", report["status"])
        self.assertTrue(any("EXCEPTION_RECORD" in item for item in report["violations"]))

    def test_valid_owner_exception_passes(self):
        repo = self.make_repo()
        exception = repo / "docs" / "Exceptions" / "EX-001.md"
        exception.write_text(
            "# Exception\n\n"
            "```text\n"
            "EXCEPTION_STATUS=APPROVED\n"
            "APPROVED_BY=Tim Simmons\n"
            "APPROVED_GITHUB_LOGIN=TimSimmons3\n"
            "APPROVED_UTC=2026-08-05T14:00:00Z\n"
            f"APPROVAL_TEXT_SHA256={'a'*64}\n"
            "CONTROL_IDS=ONE_PASS_WORKING_DELIVERABLE\n"
            "SCOPE=ONE_NAMED_DOCUMENT_ONLY\n"
            "RATIONALE=Owner-approved constrained exception\n"
            "RESIDUAL_RISK=One user-visible revision may occur\n"
            "COMPENSATING_CONTROLS=Independent owner review before execution\n"
            "EXPIRATION_UTC=2026-08-06T14:00:00Z\n"
            f"ARTIFACT_SHA256_SET={'b'*64}\n"
            "```\n",
            encoding="utf-8",
        )
        plan = repo / "docs" / "Releases" / "Test-Plan.md"
        plan.write_text(
            "# Plan\n\n" + block("APPROVED") + "EXCEPTION_RECORD=docs/Exceptions/EX-001.md\n",
            encoding="utf-8",
        )
        report = self.validate(
            repo, "docs/Releases/Test-Plan.md", "docs/Exceptions/EX-001.md"
        )
        self.assertEqual("PASS", report["status"], report["violations"])
        self.assertEqual(1, report["exception_record_count"])

    def test_exception_readme_uses_normal_invariant(self):
        repo = self.make_repo()
        path = repo / "docs" / "Exceptions" / "README.md"
        path.write_text("# Exceptions\n\n" + block(), encoding="utf-8")
        report = self.validate(repo, "docs/Exceptions/README.md")
        self.assertEqual("PASS", report["status"], report["violations"])
        self.assertEqual(0, report["exception_record_count"])

    def test_wrong_owner_exception_fails(self):
        repo = self.make_repo()
        exception = repo / "docs" / "Exceptions" / "EX-001.md"
        exception.write_text(
            "EXCEPTION_STATUS=APPROVED\nAPPROVED_BY=Other\nAPPROVED_GITHUB_LOGIN=Other\n",
            encoding="utf-8",
        )
        report = self.validate(repo, "docs/Exceptions/EX-001.md")
        self.assertEqual("FAIL", report["status"])

    def test_placeholder_exception_fails(self):
        repo = self.make_repo()
        exception = repo / "docs" / "Exceptions" / "EX-001.md"
        exception.write_text(
            "EXCEPTION_STATUS=APPROVED\n"
            "APPROVED_BY=Tim Simmons\n"
            "APPROVED_GITHUB_LOGIN=TimSimmons3\n"
            "APPROVED_UTC=<UTC>\n"
            f"APPROVAL_TEXT_SHA256={'a'*64}\n"
            "CONTROL_IDS=TBD\nSCOPE=X\nRATIONALE=X\nRESIDUAL_RISK=X\n"
            "COMPENSATING_CONTROLS=X\nEXPIRATION_UTC=2026-08-06T14:00:00Z\n"
            f"ARTIFACT_SHA256_SET={'b'*64}\n",
            encoding="utf-8",
        )
        report = self.validate(repo, "docs/Exceptions/EX-001.md")
        self.assertEqual("FAIL", report["status"])
        self.assertTrue(any("placeholder" in item for item in report["violations"]))

    def test_non_governed_file_is_ignored(self):
        repo = self.make_repo()
        (repo / "notes.md").write_text("# Notes\n", encoding="utf-8")
        report = self.validate(repo, "notes.md")
        self.assertEqual("PASS", report["status"])
        self.assertEqual(0, report["governed_file_count"])

    def test_keyword_governs_root_file(self):
        repo = self.make_repo()
        path = repo / "Project-Handoff.md"
        path.write_text("# Handoff\n", encoding="utf-8")
        report = self.validate(repo, "Project-Handoff.md")
        self.assertEqual("FAIL", report["status"])

    def test_symlink_rejected(self):
        repo = self.make_repo()
        target = repo / "target.md"
        target.write_text(block(), encoding="utf-8")
        link = repo / "docs" / "Releases" / "Test-Plan.md"
        link.symlink_to(target)
        report = self.validate(repo, "docs/Releases/Test-Plan.md")
        self.assertEqual("FAIL", report["status"])

    def test_trailing_whitespace_fails(self):
        repo = self.make_repo()
        path = repo / "docs" / "Releases" / "Test-Plan.md"
        path.write_text(block() + "bad  \n", encoding="utf-8")
        report = self.validate(repo, "docs/Releases/Test-Plan.md")
        self.assertEqual("FAIL", report["status"])

    def test_outside_path_rejected(self):
        repo = self.make_repo()
        outside = repo.parent / "outside-plan.md"
        outside.write_text(block(), encoding="utf-8")
        report = self.validate(repo, str(outside))
        self.assertEqual("FAIL", report["status"])

    def test_load_json_strict_rejects_duplicate_keys(self):
        repo = self.make_repo()
        path = repo / "duplicate.json"
        path.write_text('{"a":1,"a":2}', encoding="utf-8")
        with self.assertRaises(ValueError):
            validator.load_json_strict(path)

    def test_load_json_strict_rejects_non_object(self):
        repo = self.make_repo()
        path = repo / "array.json"
        path.write_text('[]', encoding="utf-8")
        with self.assertRaises(ValueError):
            validator.load_json_strict(path)

    def test_changed_files_uses_git_diff(self):
        repo = self.make_repo()
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
        base = repo / "docs" / "Releases" / "Base-Plan.md"
        base.write_text("# Base\n\n" + block(), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=repo, check=True)
        base_ref = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
        new = repo / "docs" / "Releases" / "New-Plan.md"
        new.write_text("# New\n\n" + block(), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-qm", "new"], cwd=repo, check=True)
        self.assertEqual(["docs/Releases/New-Plan.md"], validator.changed_files(repo, base_ref))

    def test_run_git_failure_raises(self):
        repo = self.make_repo()
        with self.assertRaises(RuntimeError):
            validator.run_git(repo, ["status"])

    def test_absolute_inside_path_normalizes(self):
        repo = self.make_repo()
        path = repo / "docs" / "Releases" / "Test-Plan.md"
        path.write_text(block(), encoding="utf-8")
        self.assertEqual(
            "docs/Releases/Test-Plan.md",
            validator.normalized_relative(repo, str(path)),
        )

    def test_invalid_utf8_fails(self):
        repo = self.make_repo()
        path = repo / "docs" / "Releases" / "Test-Plan.md"
        path.write_bytes(b"\xff\xfe")
        report = self.validate(repo, "docs/Releases/Test-Plan.md")
        self.assertEqual("FAIL", report["status"])

    def test_cr_character_fails(self):
        repo = self.make_repo()
        path = repo / "docs" / "Releases" / "Test-Plan.md"
        path.write_bytes(("# Plan\r\n" + block()).encode("utf-8"))
        report = self.validate(repo, "docs/Releases/Test-Plan.md")
        self.assertEqual("FAIL", report["status"])
        self.assertTrue(any("CR characters" in item for item in report["violations"]))

    def test_missing_changed_path_fails(self):
        repo = self.make_repo()
        report = self.validate(repo, "docs/Releases/Missing-Plan.md")
        self.assertEqual("FAIL", report["status"])

    def test_directory_changed_path_fails(self):
        repo = self.make_repo()
        report = self.validate(repo, "docs/Releases")
        self.assertEqual("FAIL", report["status"])

    def test_malformed_exception_formats_fail(self):
        repo = self.make_repo()
        exception = repo / "docs" / "Exceptions" / "EX-002.md"
        exception.write_text(
            "EXCEPTION_STATUS=APPROVED\n"
            "APPROVED_BY=Tim Simmons\n"
            "APPROVED_GITHUB_LOGIN=TimSimmons3\n"
            "APPROVED_UTC=bad\nAPPROVAL_TEXT_SHA256=bad\n"
            "CONTROL_IDS=X\nSCOPE=X\nRATIONALE=X\nRESIDUAL_RISK=X\n"
            "COMPENSATING_CONTROLS=X\nEXPIRATION_UTC=bad\nARTIFACT_SHA256_SET=bad\n",
            encoding="utf-8",
        )
        report = self.validate(repo, "docs/Exceptions/EX-002.md")
        self.assertEqual("FAIL", report["status"])
        self.assertGreaterEqual(len(report["violations"]), 4)

    def test_approved_record_outside_exception_directory_fails(self):
        repo = self.make_repo()
        path = repo / "docs" / "Releases" / "Test-Plan.md"
        path.write_text(block("APPROVED") + "EXCEPTION_RECORD=docs/Releases/Other.md\n", encoding="utf-8")
        other = repo / "docs" / "Releases" / "Other.md"
        other.write_text(block(), encoding="utf-8")
        report = self.validate(repo, "docs/Releases/Test-Plan.md")
        self.assertEqual("FAIL", report["status"])

    def test_cli_main_writes_success_report(self):
        repo = self.make_repo()
        path = repo / "docs" / "Releases" / "Test-Plan.md"
        path.write_text(block(), encoding="utf-8")
        report_path = repo / "report.json"
        rc = validator.main([
            "--repo-root", str(repo),
            "--policy", "config/mandatory-assurance-invariant-policy.json",
            "--files", "docs/Releases/Test-Plan.md",
            "--report", str(report_path),
        ])
        self.assertEqual(0, rc)
        self.assertEqual("PASS", json.loads(report_path.read_text())["status"])

    def test_cli_main_returns_failure(self):
        repo = self.make_repo()
        path = repo / "docs" / "Releases" / "Test-Plan.md"
        path.write_text("# Missing block\n", encoding="utf-8")
        rc = validator.main([
            "--repo-root", str(repo),
            "--policy", "config/mandatory-assurance-invariant-policy.json",
            "--files", "docs/Releases/Test-Plan.md",
            "--report", str(repo / "report.json"),
        ])
        self.assertEqual(1, rc)


if __name__ == "__main__":
    unittest.main()
