from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from tests import test_validate_transition_metrics as tvt

POLICY = tvt.POLICY

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "release_assurance", ROOT / "scripts" / "validate_transition_release_assurance.py"
)
assert SPEC and SPEC.loader
r = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r)


class MetricReleaseDispositionTests(unittest.TestCase):
    def metric(self, value, data_quality="MEASURED"):
        return {"data_quality": data_quality, "value": value}

    def run_mr_case(self, cell_id: str) -> None:
        ordered = [f"M{i:02d}" for i in range(1, 21)] + ["M28"]
        index = int(cell_id.split("-")[1])
        if 1 <= index <= 63:
            group = (index - 1) // 3
            branch = (index - 1) % 3
            metric_id = ordered[group]
            if branch == 2:
                result = r.evaluate_metric(metric_id, self.metric(0), evidence_status="CONTRADICTED")
                self.assertEqual("FAIL_CLOSED", result["disposition"])
                return
            nominal = branch == 0
            if metric_id in {"M01", "M05", "M08", "M13", "M14", "M16"}:
                value = 100.0 if nominal else 80.0
                expected = "VALID_RECORD_RELEASE_ELIGIBLE" if nominal else "VALID_RECORD_HOLD"
            elif metric_id == "M06":
                value = 100.0 if nominal else 90.0
                expected = "VALID_RECORD_RELEASE_ELIGIBLE" if nominal else "VALID_RECORD_HOLD"
            elif metric_id in {"M02", "M03", "M04", "M07", "M09", "M18", "M28"}:
                value = 0 if nominal else 1
                expected = "VALID_RECORD_RELEASE_ELIGIBLE" if nominal else "VALID_RECORD_HOLD"
            elif metric_id in {"M10", "M11", "M12", "M15", "M17"}:
                value = "PASS" if nominal else "FAIL"
                expected = "VALID_RECORD_RELEASE_ELIGIBLE" if nominal else "VALID_RECORD_HOLD"
            elif metric_id == "M19":
                value = 0 if nominal else 1
                expected = "VALID_RECORD_RELEASE_ELIGIBLE" if nominal else "VALID_RECORD_GOVERNED_EXCEPTION"
            elif metric_id == "M20":
                value = 0 if nominal else 1
                expected = "VALID_RECORD_RELEASE_ELIGIBLE" if nominal else "VALID_RECORD_TRACK"
            else:
                self.fail(f"unhandled metric {metric_id}")
            result = r.evaluate_metric(metric_id, self.metric(value))
            self.assertEqual(expected, result["disposition"], result)
            return

        specs = {
            "MR-64": ("M06", self.metric(97.0), None, False, "CONFIRMED", "VALID_RECORD_THRESHOLD_MET_TARGET_MISSED"),
            "MR-65": ("M23", self.metric(5.0), self.metric(10.0), False, "CONFIRMED", "VALID_RECORD_RELEASE_ELIGIBLE"),
            "MR-66": ("M23", self.metric(10.0), self.metric(10.0), False, "CONFIRMED", "VALID_RECORD_HOLD"),
            "MR-67": ("M23", self.metric(5.0), self.metric(10.0), False, "CONTRADICTED", "FAIL_CLOSED"),
            "MR-68": ("M25", self.metric(0.0), None, False, "CONFIRMED", "VALID_RECORD_RELEASE_ELIGIBLE"),
            "MR-69": ("M25", self.metric(10.0), None, False, "CONFIRMED", "VALID_RECORD_HOLD"),
            "MR-70": ("M25", self.metric(0.0), None, False, "CONTRADICTED", "FAIL_CLOSED"),
            "MR-71": ("M27", self.metric(100.0), None, False, "CONFIRMED", "VALID_RECORD_RELEASE_ELIGIBLE"),
            "MR-72": ("M27", self.metric(90.0), None, False, "CONFIRMED", "VALID_RECORD_HOLD"),
            "MR-73": ("M27", self.metric(100.0), None, False, "CONTRADICTED", "FAIL_CLOSED"),
            "MR-74": ("M20", self.metric(1), None, True, "CONFIRMED", "VALID_RECORD_ACTIVE_BLOCKER_HOLD"),
            "MR-75": ("M23", self.metric(None, "NOT_APPLICABLE"), None, False, "CONFIRMED", "VALID_RECORD_HOLD_TARGET_NOT_EVALUABLE"),
        }
        metric_id, metric, prior, active, evidence, expected = specs[cell_id]
        result = r.evaluate_metric(
            metric_id,
            metric,
            prior_metric=prior,
            active_external_blocker=active,
            evidence_status=evidence,
        )
        self.assertEqual(expected, result["disposition"], result)


for _index in range(1, 76):
    _cell_id = f"MR-{_index:02d}"

    def _make_mr_test(cell_id: str):
        def _test(self):
            self.run_mr_case(cell_id)
        _test.__name__ = f"test_{cell_id.replace('-', '_')}"
        return _test

    setattr(MetricReleaseDispositionTests, f"test_MR_{_index:02d}", _make_mr_test(_cell_id))


class CollectionTriggerTests(unittest.TestCase):
    trigger_order = [
        "WORKSTREAM_START",
        "GATE",
        "CLOSEOUT",
        "HANDOFF",
        "DEVIATION",
        "FAILURE",
        "RELEASE_RESET",
        "LIVE_ATTEMPT",
        "EXTERNAL_BLOCKER",
    ]

    def setUp(self):
        self.helper = tvt.TransitionValidatorTests(methodName="test_valid_snapshot_passes")
        self.repo = self.helper.make_repo()
        self.workstream = "W"

    def ext(self):
        return {"type": "EXTERNAL_ARTIFACT", "artifact_id": "E", "sha256": "a" * 64}

    def base_event(self, event_type: str) -> dict:
        frm = "IMPLEMENTATION_OFFLINE"
        to = "IMPLEMENTATION_OFFLINE"
        if event_type == "RELEASE_RESET":
            to = "RELEASE_RESET_REQUIRED"
        elif event_type == "LIVE_ATTEMPT":
            frm = "AUTHORIZED_FOR_SINGLE_LIVE_ATTEMPT"
            to = "LIVE_EXECUTION_OR_EXTERNAL_CHECKPOINT"
        event = {
            "record_type": POLICY["record_types"]["event"],
            "schema_version": POLICY["schema_version"],
            "workstream_id": self.workstream,
            "event_id": "E1",
            "created_utc": "2026-08-07T12:00:00Z",
            "event_type": event_type,
            "lifecycle_from": frm,
            "lifecycle_to": to,
            "classification": "NONE",
            "mutation_boundary_crossed": False,
            "previous_record": None,
            "evidence_refs": [self.ext()],
        }
        if event_type == "DEVIATION":
            event["classification"] = "REVIEW_TEST_DEFECT"
            event["deviation"] = {
                "deviation_id": "D1",
                "timestamp_utc": "2026-08-07T12:00:00Z",
                "category": "REVIEW",
                "planned_condition": "x",
                "observed_condition": "y",
                "impact": "z",
                "mutation_status": "NONE",
                "evidence_reference": "E",
                "owner_disposition": "CORRECT",
                "permanent_control_decision": "ADD_TEST",
            }
        if event_type == "EXTERNAL_BLOCKER":
            event["external_incident"] = {
                "candidate_revision_action": "PRESERVE_EXACT_CANDIDATE",
                "code_revision_created": False,
                "exposed_internal_defect": False,
            }
        return event

    def make_valid_record(self, trigger_id: str) -> tuple[str, dict]:
        if trigger_id in {"WORKSTREAM_START", "GATE", "CLOSEOUT", "HANDOFF"}:
            rec = self.helper.snapshot(self.repo)
            rec["workstream_id"] = self.workstream
            rec["snapshot_type"] = trigger_id
            if trigger_id == "HANDOFF":
                self.helper.make_handoff(self.repo, rec)
            else:
                self.helper.write_csv(self.repo, rec)
            return f"docs/Releases/metrics/{trigger_id.lower()}.json", rec
        return f"docs/Releases/metrics/{trigger_id.lower()}.json", self.base_event(trigger_id)

    def write_record(self, path: str, record) -> None:
        full = self.repo / path
        full.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(record, str):
            full.write_text(record, encoding="utf-8")
        else:
            full.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")

    def run_ct_case(self, cell_id: str) -> None:
        index = int(cell_id.split("-")[1])
        if 1 <= index <= 9:
            trigger = self.trigger_order[index - 1]
            path, rec = self.make_valid_record(trigger)
            self.write_record(path, rec)
            result = r.validate_trigger_record(self.repo, POLICY, trigger, path, self.workstream)
            self.assertEqual("PASS", result["status"], result)
            return
        if 10 <= index <= 18:
            trigger = self.trigger_order[index - 10]
            result = r.validate_trigger_record(self.repo, POLICY, trigger, None, self.workstream)
            self.assertEqual("FAIL", result["status"], result)
            return
        if 19 <= index <= 27:
            trigger = self.trigger_order[index - 19]
            path, valid = self.make_valid_record(trigger)
            cases = []
            cases.append("{not-json")
            missing = copy.deepcopy(valid)
            missing.pop("created_utc", None)
            cases.append(missing)
            wrong_container = copy.deepcopy(valid)
            if trigger in {"WORKSTREAM_START", "GATE", "CLOSEOUT", "HANDOFF"}:
                wrong_container["metrics"] = {}
            else:
                wrong_container["evidence_refs"] = {}
            cases.append(wrong_container)
            for n, case in enumerate(cases):
                with self.subTest(trigger=trigger, malformed_branch=n):
                    self.write_record(path, case)
                    result = r.validate_trigger_record(self.repo, POLICY, trigger, path, self.workstream)
                    self.assertEqual("FAIL", result["status"], result)
            return
        if 28 <= index <= 36:
            trigger = self.trigger_order[index - 28]
            path, rec = self.make_valid_record(trigger)
            if trigger in {"WORKSTREAM_START", "GATE", "CLOSEOUT", "HANDOFF"}:
                rec["snapshot_type"] = "WORKSTREAM_START" if trigger != "WORKSTREAM_START" else "CLOSEOUT"
            else:
                rec["event_type"] = "FAILURE" if trigger != "FAILURE" else "GATE"
            self.write_record(path, rec)
            result = r.validate_trigger_record(self.repo, POLICY, trigger, path, self.workstream)
            self.assertEqual("FAIL", result["status"], result)
            return
        if 37 <= index <= 45:
            trigger = self.trigger_order[index - 37]
            path, rec = self.make_valid_record(trigger)
            rec["workstream_id"] = "OTHER"
            if trigger in {"WORKSTREAM_START", "GATE", "CLOSEOUT", "HANDOFF"}:
                self.helper.write_csv(self.repo, rec)
            self.write_record(path, rec)
            result = r.validate_trigger_record(self.repo, POLICY, trigger, path, self.workstream)
            self.assertEqual("FAIL", result["status"], result)
            return
        self.fail(f"unhandled {cell_id}")


for _index in range(1, 46):
    _cell_id = f"CT-{_index:02d}"

    def _make_ct_test(cell_id: str):
        def _test(self):
            self.run_ct_case(cell_id)
        _test.__name__ = f"test_{cell_id.replace('-', '_')}"
        return _test

    setattr(CollectionTriggerTests, f"test_CT_{_index:02d}", _make_ct_test(_cell_id))


class ReleaseAssuranceBehaviorTests(unittest.TestCase):
    def test_missing_metric_evidence_confirmation_holds(self):
        result = r.evaluate_metric("M02", {"data_quality": "MEASURED", "value": 0}, evidence_status="MISSING")
        self.assertEqual("VALID_RECORD_HOLD", result["disposition"])

    def test_contradicted_metric_evidence_fails_closed(self):
        result = r.evaluate_metric("M02", {"data_quality": "MEASURED", "value": 0}, evidence_status="CONTRADICTED")
        self.assertEqual("FAIL_CLOSED", result["disposition"])

    def test_unknown_metric_is_valid_but_hold(self):
        result = r.evaluate_metric("M02", {"data_quality": "UNKNOWN", "value": None}, evidence_status="CONFIRMED")
        self.assertEqual("VALID_RECORD_HOLD", result["disposition"])

    def test_m25_zero_defect_not_applicable_is_release_eligible(self):
        result = r.evaluate_metric("M25", {"data_quality": "NOT_APPLICABLE", "value": None})
        self.assertEqual("VALID_RECORD_RELEASE_ELIGIBLE", result["disposition"])


if __name__ == "__main__":
    unittest.main()
