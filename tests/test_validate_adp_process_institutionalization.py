#!/usr/bin/env python3
from __future__ import annotations
import copy, importlib.util, json, shutil, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/validate_adp_process_institutionalization.py"
SPEC=importlib.util.spec_from_file_location("inst",SCRIPT)
inst=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(inst)

class ProcessInstitutionalizationTests(unittest.TestCase):
    def setUp(self):
        self.policy=inst.load_json_strict(ROOT/"config/adp-process-institutionalization-policy.json")

    def test_repository_positive(self):
        self.assertEqual("PASS",inst.validate_repo(ROOT,self.policy)["status"])

    def test_policy_exact_control_count(self):
        p=copy.deepcopy(self.policy);p["control_ids"]=p["control_ids"][:-1]
        self.assertIn("control_ids must be exact PI-01..PI-16",inst.validate_policy_shape(p))

    def test_policy_exact_metric_set(self):
        p=copy.deepcopy(self.policy);p["process_metrics"].pop("P14")
        self.assertIn("process_metrics must be exact P01..P14",inst.validate_policy_shape(p))

    def test_policy_exact_handoff_section_count(self):
        p=copy.deepcopy(self.policy);p["mandatory_handoff_sections"]=p["mandatory_handoff_sections"][:-1]
        self.assertTrue(any("16 unique" in x for x in inst.validate_policy_shape(p)))

    def test_r1_reopen_prohibited(self):
        p=copy.deepcopy(self.policy);p["source_baseline"]["r1_reopen_allowed"]=True
        self.assertTrue(any("closed R1 identity" in x for x in inst.validate_policy_shape(p)))

    def test_r1_denominator_frozen(self):
        p=copy.deepcopy(self.policy);p["source_baseline"]["r1_frozen_denominator"]=375
        self.assertTrue(any("closed R1 identity" in x for x in inst.validate_policy_shape(p)))

    def test_safe_rel_rejects_parent(self):
        with self.assertRaises(ValueError):inst.safe_rel("../x")

    def _fixture(self):
        td=tempfile.TemporaryDirectory();root=Path(td.name)
        paths=set(self.policy["required_artifacts"]);paths.update(self.policy["required_trust_root_paths"]);paths.update([
            ".github/CODEOWNERS",".github/workflows/mandatory-assurance-invariant-gate.yml",
            ".github/workflows/mandatory-assurance-trusted-gate.yml","config/assurance-trust-root-manifest.json",
            self.policy["r1_frozen_oracle"]["path"],self.policy["external_evidence_fail_safe"]["path"],
        ])
        for rel in paths:
            src=ROOT/rel
            if src.is_file():
                dst=root/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
        return td,root

    def test_missing_required_artifact_fails(self):
        td,root=self._fixture()
        try:(root/"docs/Templates/SMT-Workstream-Continuation-Control-Template.md").unlink();self.assertEqual("FAIL",inst.validate_repo(root,self.policy)["status"])
        finally:td.cleanup()

    def test_symlink_required_artifact_fails(self):
        td,root=self._fixture()
        try:
            p=root/"docs/Templates/SMT-Workstream-Continuation-Control-Template.md";p.unlink();p.symlink_to("/tmp/nonexistent")
            self.assertEqual("FAIL",inst.validate_repo(root,self.policy)["status"])
        finally:td.cleanup()

    def test_missing_marker_fails(self):
        td,root=self._fixture()
        try:
            p=root/"skills/smt-high-assurance-engineering-delivery/SKILL.md";p.write_text(p.read_text(encoding="utf-8").replace("PRODUCTION_CHANGE_REQUIRES_FAILED_EXACT_PROBE=TRUE","REMOVED"),encoding="utf-8")
            self.assertEqual("FAIL",inst.validate_repo(root,self.policy)["status"])
        finally:td.cleanup()

    def test_intermediate_control_marker_fails(self):
        td,root=self._fixture()
        try:
            p=root/"docs/Standards/ADP-High-Assurance-Process-Institutionalization-Standard-R1.md";p.write_text(p.read_text(encoding="utf-8").replace("### PI-08","### REMOVED"),encoding="utf-8")
            self.assertEqual("FAIL",inst.validate_repo(root,self.policy)["status"])
        finally:td.cleanup()

    def test_intermediate_metric_template_marker_fails(self):
        td,root=self._fixture()
        try:
            p=root/"docs/Templates/SMT-Process-Assurance-Metrics-Template.json";p.write_text(p.read_text(encoding="utf-8").replace('"metric_id": "P07"','"metric_id": "REMOVED"'),encoding="utf-8")
            self.assertEqual("FAIL",inst.validate_repo(root,self.policy)["status"])
        finally:td.cleanup()

    def test_missing_trust_root_path_fails(self):
        td,root=self._fixture()
        try:
            p=root/"config/assurance-trust-root-manifest.json";obj=json.loads(p.read_text(encoding="utf-8"));obj["trusted_paths"].remove("scripts/validate_adp_process_institutionalization.py");p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")
            self.assertEqual("FAIL",inst.validate_repo(root,self.policy)["status"])
        finally:td.cleanup()

    def test_missing_codeowners_rule_fails(self):
        td,root=self._fixture()
        try:
            p=root/".github/CODEOWNERS";p.write_text(p.read_text(encoding="utf-8").replace("/scripts/validate_adp_process_institutionalization.py @TimSimmons3\n",""),encoding="utf-8")
            self.assertEqual("FAIL",inst.validate_repo(root,self.policy)["status"])
        finally:td.cleanup()

    def test_missing_candidate_workflow_step_fails(self):
        td,root=self._fixture()
        try:
            p=root/".github/workflows/mandatory-assurance-invariant-gate.yml";p.write_text(p.read_text(encoding="utf-8").replace("Validate institutionalized high-assurance process controls","REMOVED"),encoding="utf-8")
            self.assertEqual("FAIL",inst.validate_repo(root,self.policy)["status"])
        finally:td.cleanup()

    def test_missing_trusted_workflow_step_fails(self):
        td,root=self._fixture()
        try:
            p=root/".github/workflows/mandatory-assurance-trusted-gate.yml";p.write_text(p.read_text(encoding="utf-8").replace("Validate institutionalized process controls with trusted code","REMOVED"),encoding="utf-8")
            self.assertEqual("FAIL",inst.validate_repo(root,self.policy)["status"])
        finally:td.cleanup()

    def test_external_hold_marker_required(self):
        td,root=self._fixture()
        try:
            p=root/"tests/qualification/run_final_assurance_state_oracle.py";p.write_text(p.read_text(encoding="utf-8").replace('EXTERNAL_EVIDENCE_AUTHORIZATION_MODE = "HOLD_ONLY_UNTIL_TRUSTED_COLLECTOR"',"REMOVED"),encoding="utf-8")
            self.assertEqual("FAIL",inst.validate_repo(root,self.policy)["status"])
        finally:td.cleanup()

    def test_handoff_section_marker_required(self):
        td,root=self._fixture()
        try:
            p=root/"docs/Templates/SMT-Workstream-Continuation-Control-Template.md";marker=self.policy["mandatory_handoff_sections"][0];p.write_text(p.read_text(encoding="utf-8").replace(marker,"REMOVED"),encoding="utf-8")
            self.assertEqual("FAIL",inst.validate_repo(root,self.policy)["status"])
        finally:td.cleanup()

    def test_commit_delta_validator_requires_committed_fixture_marker(self):
        td,root=self._fixture()
        try:
            p=root/"docs/Standards/ADP-High-Assurance-Process-Institutionalization-Standard-R1.md";p.write_text(p.read_text(encoding="utf-8").replace("COMMIT_DELTA_VALIDATOR_REQUIRES_COMMITTED_FIXTURE=TRUE","REMOVED"),encoding="utf-8")
            self.assertEqual("FAIL",inst.validate_repo(root,self.policy)["status"])
        finally:td.cleanup()

    def _valid_metrics_record(self):
        rows=[]
        for mid in inst.EXPECTED_METRICS:
            d=self.policy["process_metrics"][mid];rows.append({"metric_id":mid,"name":d["name"],"target":d["target"],"value":0,"status":"TRACK","evidence_refs":["evidence://example"]})
        return {"record_type":inst.PROCESS_METRICS_RECORD_TYPE,"schema_version":"1.0","workstream_id":"EXAMPLE","candidate_head":"a"*40,"candidate_tree":"b"*40,"created_utc":"2026-08-08T15:00:00Z","metrics":rows}

    def test_process_metrics_record_positive(self):
        self.assertEqual([],inst.validate_process_metrics_record(self._valid_metrics_record(),self.policy,"metrics.json"))

    def test_process_metrics_missing_middle_metric_fails(self):
        r=self._valid_metrics_record();r["metrics"].pop(6);self.assertTrue(any("P01-P14 exactly once" in x for x in inst.validate_process_metrics_record(r,self.policy,"metrics.json")))

    def test_process_metrics_target_mismatch_fails(self):
        r=self._valid_metrics_record();r["metrics"][6]["target"]="WRONG";self.assertTrue(any("target mismatch" in x for x in inst.validate_process_metrics_record(r,self.policy,"metrics.json")))

    def test_process_metrics_bad_candidate_head_fails(self):
        r=self._valid_metrics_record();r["candidate_head"]="bad";self.assertTrue(any("candidate_head" in x for x in inst.validate_process_metrics_record(r,self.policy,"metrics.json")))

    def test_process_metrics_placeholder_value_fails(self):
        r=self._valid_metrics_record();r["metrics"][0]["value"]="<REQUIRED>";self.assertTrue(any("concrete value" in x for x in inst.validate_process_metrics_record(r,self.policy,"metrics.json")))

    def test_handoff_document_positive(self):
        td=tempfile.TemporaryDirectory()
        try:
            root=Path(td.name);rel="docs/Releases/process-metrics/example.json";p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(self._valid_metrics_record(),indent=2)+"\n",encoding="utf-8")
            lines=["# Example",f"PROCESS_ASSURANCE_METRICS_RECORD={rel}"]
            for i,s in enumerate(self.policy["mandatory_handoff_sections"],1):lines += [f"## {i}. {s}","Evidence."]
            self.assertEqual([],inst.validate_handoff_document(root,"docs/Releases/Example-Handoff.md","\n".join(lines),self.policy))
        finally:td.cleanup()

    def test_handoff_document_missing_section_fails(self):
        td=tempfile.TemporaryDirectory()
        try:
            root=Path(td.name);rel="docs/Releases/process-metrics/example.json";p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(self._valid_metrics_record(),indent=2)+"\n",encoding="utf-8")
            lines=["# Example",f"PROCESS_ASSURANCE_METRICS_RECORD={rel}"]
            for i,s in enumerate(self.policy["mandatory_handoff_sections"][1:],2):lines.append(f"## {i}. {s}")
            self.assertTrue(any("missing mandatory handoff section" in x for x in inst.validate_handoff_document(root,"docs/Releases/Example-Handoff.md","\n".join(lines),self.policy)))
        finally:td.cleanup()

    def test_handoff_document_missing_metrics_assignment_fails(self):
        text="\n".join(f"## {i}. {s}" for i,s in enumerate(self.policy["mandatory_handoff_sections"],1));self.assertTrue(any("requires exactly one PROCESS_ASSURANCE_METRICS_RECORD" in x for x in inst.validate_handoff_document(Path("."),"docs/Releases/Example-Handoff.md",text,self.policy)))

    def test_policy_compatibility_rejects_control_change(self):
        b=copy.deepcopy(self.policy);c=copy.deepcopy(self.policy);c["control_ids"]=c["control_ids"][:-1];self.assertTrue(any("control_ids is immutable" in x for x in inst.policy_compatibility_errors(b,c)))

    def test_policy_compatibility_rejects_marker_removal(self):
        b=copy.deepcopy(self.policy);c=copy.deepcopy(self.policy);rel="docs/Standards/ADP-High-Assurance-Process-Institutionalization-Standard-R1.md";c["required_artifacts"][rel]=c["required_artifacts"][rel][:-1];self.assertTrue(any("may not remove markers" in x for x in inst.policy_compatibility_errors(b,c)))

    def test_policy_compatibility_allows_additive_owner_path(self):
        b=copy.deepcopy(self.policy);c=copy.deepcopy(self.policy);c["required_codeowners_paths"].append("z/new/path");c["required_codeowners_paths"]=sorted(c["required_codeowners_paths"]);self.assertEqual([],inst.policy_compatibility_errors(b,c))

    def test_instance_enforcement_shape_required(self):
        p=copy.deepcopy(self.policy);p["instance_enforcement"]["handoff_roots"]=["docs/Releases/"];self.assertTrue(any("handoff_roots mismatch" in x for x in inst.validate_policy_shape(p)))

if __name__=="__main__":
    unittest.main()
