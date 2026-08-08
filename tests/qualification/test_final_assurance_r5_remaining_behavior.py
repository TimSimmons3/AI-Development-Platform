from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests import test_validate_transition_metrics as tvt
from tests import test_validate_mandatory_assurance_invariants as mvt

POLICY = tvt.POLICY
v = tvt.v

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "release_assurance", ROOT / "scripts" / "validate_transition_release_assurance.py"
)
assert SPEC and SPEC.loader
r = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r)


class RemainingR5BehaviorTests(unittest.TestCase):
    def setUp(self):
        self.helper = tvt.TransitionValidatorTests(methodName="test_valid_snapshot_passes")
        self.repo = self.helper.make_repo()

    def ext(self):
        return {"type": "EXTERNAL_ARTIFACT", "artifact_id": "E", "sha256": "a" * 64}

    def event(self, frm: str, to: str, event_type: str = "LIFECYCLE") -> dict:
        return {
            "record_type": POLICY["record_types"]["event"],
            "schema_version": POLICY["schema_version"],
            "workstream_id": "W",
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

    def deviation(self) -> dict:
        event = self.event("IMPLEMENTATION_OFFLINE", "IMPLEMENTATION_OFFLINE", "DEVIATION")
        event["classification"] = "REVIEW_TEST_DEFECT"
        event["deviation"] = {
            "deviation_id": "D1",
            "timestamp_utc": "2026-08-07T12:00:00Z",
            "category": "REVIEW",
            "planned_condition": "planned",
            "observed_condition": "observed",
            "impact": "impact",
            "mutation_status": "NONE",
            "evidence_reference": "E1",
            "owner_disposition": "CORRECT",
            "permanent_control_decision": "ADD_TEST",
        }
        return event

    def external_blocker(self, exposed_internal_defect: bool, code_revision_created: bool) -> dict:
        event = self.event("IMPLEMENTATION_OFFLINE", "IMPLEMENTATION_OFFLINE", "EXTERNAL_BLOCKER")
        event["external_incident"] = {
            "candidate_revision_action": "PRESERVE_EXACT_CANDIDATE",
            "code_revision_created": code_revision_created,
            "exposed_internal_defect": exposed_internal_defect,
        }
        return event

    def test_RB_01_all_policy_allowed_lifecycle_transitions_validate(self):
        for frm, targets in POLICY["allowed_transitions"].items():
            for to in targets:
                with self.subTest(frm=frm, to=to):
                    errors = v.validate_event(self.repo, "e.json", self.event(frm, to), POLICY)
                    self.assertEqual([], errors)

    def test_RB_02_all_policy_disallowed_lifecycle_transitions_fail(self):
        states = POLICY["lifecycle_states"]
        for frm in states:
            allowed = set(POLICY["allowed_transitions"].get(frm, []))
            for to in states:
                if to in allowed:
                    continue
                with self.subTest(frm=frm, to=to):
                    errors = v.validate_event(self.repo, "e.json", self.event(frm, to), POLICY)
                    self.assertTrue(any("invalid lifecycle transition" in x or "closed workstream" in x for x in errors), errors)

    def test_RB_04_release_reset_required_has_exact_two_valid_exits(self):
        for to in ("PLANNING_READ_ONLY", "DESIGN_QUALIFICATION"):
            with self.subTest(to=to):
                self.assertEqual([], v.validate_event(self.repo, "e.json", self.event("RELEASE_RESET_REQUIRED", to), POLICY))

    def test_RB_05_lifecycle_required_identity_time_and_state_failures_are_structured(self):
        base = self.event("PLANNING_READ_ONLY", "DESIGN_QUALIFICATION")
        cases = []
        for field in ("workstream_id", "event_id"):
            value = copy.deepcopy(base); value.pop(field); cases.append(value)
        bad_time = copy.deepcopy(base); bad_time["created_utc"] = "not-utc"; cases.append(bad_time)
        bad_from = copy.deepcopy(base); bad_from["lifecycle_from"] = "NO_STATE"; cases.append(bad_from)
        bad_to = copy.deepcopy(base); bad_to["lifecycle_to"] = "NO_STATE"; cases.append(bad_to)
        bad_type = copy.deepcopy(base); bad_type["event_type"] = "NO_EVENT"; cases.append(bad_type)
        for index, event in enumerate(cases):
            with self.subTest(case=index):
                self.assertTrue(v.validate_event(self.repo, "e.json", event, POLICY))

    def test_RB_14_every_deviation_required_field_omission_fails(self):
        base = self.deviation()
        for field in v.DEVIATION_FIELDS:
            with self.subTest(field=field):
                event = copy.deepcopy(base)
                event["deviation"].pop(field)
                errors = v.validate_event(self.repo, "e.json", event, POLICY)
                self.assertTrue(any(f"deviation.{field} required" in x for x in errors), errors)

    def test_RB_15_malformed_deviation_types_and_classification_fail_structured(self):
        base = self.deviation()
        cases = []
        d = copy.deepcopy(base); d["classification"] = "NO_CLASS"; cases.append(d)
        d = copy.deepcopy(base); d["deviation"] = []; cases.append(d)
        d = copy.deepcopy(base); d["deviation"]["timestamp_utc"] = "bad"; cases.append(d)
        d = copy.deepcopy(base); d["deviation"]["deviation_id"] = []; cases.append(d)
        for index, event in enumerate(cases):
            with self.subTest(case=index):
                self.assertTrue(v.validate_event(self.repo, "e.json", event, POLICY))

    def test_RB_16_deviation_owner_disposition_and_permanent_control_are_mandatory(self):
        for field in ("owner_disposition", "permanent_control_decision"):
            with self.subTest(field=field):
                event = self.deviation(); event["deviation"][field] = ""
                errors = v.validate_event(self.repo, "e.json", event, POLICY)
                self.assertTrue(any(f"deviation.{field} required" in x for x in errors), errors)

    def test_RB_19_external_blocker_exposing_internal_defect_can_record_revision_truthfully(self):
        event = self.external_blocker(exposed_internal_defect=True, code_revision_created=True)
        self.assertEqual([], v.validate_event(self.repo, "e.json", event, POLICY))

    def test_RB_20_release_reset_boundary_rejects_direct_return_to_implementation(self):
        errors = v.validate_event(self.repo, "e.json", self.event("RELEASE_RESET_REQUIRED", "IMPLEMENTATION_OFFLINE"), POLICY)
        self.assertTrue(any("invalid lifecycle transition" in x for x in errors), errors)

    def test_RB_22_measured_metric_requires_value_collection_method_and_evidence(self):
        definition = POLICY["metrics"]["M02"]
        good = {"metric_id":"M02","data_quality":"MEASURED","value":0,"collection_method":"LEDGER","reason":"","evidence_refs":[self.ext()]}
        cases = []
        x=copy.deepcopy(good); x["value"] = None; cases.append(x)
        x=copy.deepcopy(good); x["collection_method"] = ""; cases.append(x)
        x=copy.deepcopy(good); x["evidence_refs"] = []; cases.append(x)
        for index, metric in enumerate(cases):
            with self.subTest(case=index):
                errors=[]; v.metric_value_domain(metric, definition, errors, "M02")
                self.assertTrue(errors)

    def test_RB_23_well_formed_unknown_is_structurally_valid_and_release_hold(self):
        metric={"metric_id":"M02","data_quality":"UNKNOWN","value":None,"collection_method":"GAP","reason":"evidence pending","evidence_refs":[]}
        errors=[]; v.metric_value_domain(metric, POLICY["metrics"]["M02"], errors, "M02")
        self.assertEqual([], errors)
        self.assertEqual("VALID_RECORD_HOLD", r.evaluate_metric("M02", metric)["disposition"])

    def test_RB_24_well_formed_policy_na_states_validate(self):
        helper = tvt.TransitionValidatorTests(methodName="test_valid_snapshot_passes")
        helper.test_m23_zero_active_canonical_not_applicable_passes()
        helper.test_m25_zero_defects_canonical_not_applicable_passes()

    def test_RB_25_zero_denominator_never_creates_artificial_success_percentage(self):
        metric={"metric_id":"M23","data_quality":"NOT_APPLICABLE","value":None,"collection_method":"EVENT_INTERVALS","reason":"zero active denominator","evidence_refs":[]}
        errors=[]; v.metric_value_domain(metric, POLICY["metrics"]["M23"], errors, "M23")
        self.assertEqual([], errors)
        self.assertEqual("VALID_RECORD_HOLD_TARGET_NOT_EVALUABLE", r.evaluate_metric("M23", metric)["disposition"])

    def test_RB_57_linked_repeat_defect_computation_passes(self):
        repo=self.helper.make_repo(); rec=self.helper.snapshot(repo)
        rec["defects"]=[
            {"defect_id":"D1","classification":"IMPLEMENTATION_DEFECT","repeated":True,"prior_lesson_or_control_ref":"CTRL-1"},
            {"defect_id":"D2","classification":"IMPLEMENTATION_DEFECT","repeated":False,"prior_lesson_or_control_ref":""},
        ]
        m=next(x for x in rec["metrics"] if x["metric_id"]=="M25")
        m.update(data_quality="DERIVED",value=50.0,numerator=1,denominator=2,collection_method="DEFECT_LEDGER",reason="",evidence_refs=[self.ext()])
        self.helper.write_csv(repo,rec)
        self.assertEqual("PASS", self.helper.validate(repo,rec)["status"])

    def test_RB_70_complete_change_record_fields_validate(self):
        text="\n".join(f"{field}=VALUE_{index}" for index,field in enumerate(POLICY["required_change_record_fields"]))+"\n"
        errors=v.validate_markdown(self.repo,"docs/Releases/Test-Change.md",text,POLICY)
        self.assertEqual([],errors)

    def test_RB_72_owner_authorization_fields_are_in_same_authorized_change_record(self):
        text="\n".join(f"{field}=VALUE_{index}" for index,field in enumerate(POLICY["required_change_record_fields"]))+"\n"
        parsed=v.assignments(text)
        self.assertEqual(1,len(parsed["CHANGE_RECORD_SCOPE"]))
        self.assertEqual(1,len(parsed["OWNER_AUTHORIZATION"]))
        self.assertEqual(1,len(parsed["OWNER_AUTHORIZATION_EXPIRATION"]))
        self.assertEqual([],v.validate_markdown(self.repo,"docs/Releases/Test-Authorization.md",text,POLICY))

    def test_RB_80_valid_external_artifact_and_incident_references_pass(self):
        refs=[
            {"type":"EXTERNAL_ARTIFACT","artifact_id":"A1","sha256":"a"*64},
            {"type":"EXTERNAL_INCIDENT","incident_id":"I1","sha256":"b"*64},
        ]
        errors=[]
        for ref in refs: v.validate_reference(self.repo,ref,errors,"ref")
        self.assertEqual([],errors)

    def _git_repo_with_commits(self):
        repo=Path(tempfile.mkdtemp()); subprocess.run(["git","init","-q"],cwd=repo,check=True)
        subprocess.run(["git","config","user.name","T"],cwd=repo,check=True); subprocess.run(["git","config","user.email","t@example.invalid"],cwd=repo,check=True)
        commits=[]
        for i in range(4):
            (repo/"state.txt").write_text(str(i),encoding="utf-8")
            subprocess.run(["git","add","state.txt"],cwd=repo,check=True); subprocess.run(["git","commit","-qm",f"c{i}"],cwd=repo,check=True)
            commits.append(subprocess.check_output(["git","rev-parse","HEAD"],cwd=repo,text=True).strip())
        return repo,commits

    def test_EX_03_missing_wrong_location_and_nonregular_exception_record_fail(self):
        helper=mvt.MandatoryTests(methodName="test_valid_governed_document_passes")
        # Missing binding target.
        repo=helper.repo(); doc=repo/"docs/Releases/Test-Plan.md";doc.write_text(mvt.block(status="APPROVED")+"EXCEPTION_RECORD=docs/Exceptions/Missing.md\n")
        self.assertEqual("FAIL",helper.validate(repo,"docs/Releases/Test-Plan.md")["status"])
        # Wrong location/non-Exception Markdown.
        repo=helper.repo(); other=repo/"docs/Releases/Other.md";other.write_text(mvt.block());doc=repo/"docs/Releases/Test-Plan.md";doc.write_text(mvt.block(status="APPROVED")+"EXCEPTION_RECORD=docs/Releases/Other.md\n")
        self.assertEqual("FAIL",helper.validate(repo,"docs/Releases/Test-Plan.md")["status"])
        # Symlink/non-regular exception record.
        repo=helper.repo(); target=repo/"target.md";target.write_text("x\n"); link=repo/"docs/Exceptions/EX-001.md";link.symlink_to(target);doc=repo/"docs/Releases/Test-Plan.md";doc.write_text(mvt.block(status="APPROVED")+"EXCEPTION_RECORD=docs/Exceptions/EX-001.md\n")
        self.assertEqual("FAIL",helper.validate(repo,"docs/Releases/Test-Plan.md")["status"])

    def test_TL_01_record_before_next_transition_is_contemporaneous(self):
        repo,c=self._git_repo_with_commits()
        result=r.evaluate_offline_collection_timeliness(repo,trigger_commit=c[0],record_commit=c[1],next_transition_commit=c[2],declared_status="CONTEMPORANEOUS")
        self.assertEqual("VALIDATE_ALLOW",result["disposition"])

    def test_TL_03_truthful_late_reconstruction_is_preserved_but_hold(self):
        repo,c=self._git_repo_with_commits()
        result=r.evaluate_offline_collection_timeliness(repo,trigger_commit=c[0],record_commit=c[3],next_transition_commit=c[2],declared_status="LATE_RECONSTRUCTION")
        self.assertEqual("VALID_RECORD_HOLD",result["disposition"])

    def test_TL_04_false_contemporaneous_or_impossible_order_fails_closed(self):
        repo,c=self._git_repo_with_commits()
        result=r.evaluate_offline_collection_timeliness(repo,trigger_commit=c[0],record_commit=c[3],next_transition_commit=c[2],declared_status="CONTEMPORANEOUS")
        self.assertEqual("FAIL_CLOSED",result["disposition"])
        result=r.evaluate_offline_collection_timeliness(repo,trigger_commit=c[2],record_commit=c[1],next_transition_commit=c[3],declared_status="CONTEMPORANEOUS")
        self.assertEqual("FAIL_CLOSED",result["disposition"])


if __name__ == "__main__":
    unittest.main()
