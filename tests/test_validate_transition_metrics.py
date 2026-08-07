from __future__ import annotations

import copy
import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'scripts'/'validate_transition_metrics.py'
SPEC=importlib.util.spec_from_file_location('transition_validator',MODULE_PATH)
assert SPEC and SPEC.loader
v=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(v)
POLICY=v.load_json_strict(ROOT/'config'/'transition-metrics-policy.json')
START=v.load_json_strict(ROOT/'docs/Releases/metrics/ADP-Transition-Governance-Repository-Integration-R1-Implementation-Start-Metrics.json')

class TransitionValidatorTests(unittest.TestCase):
    def make_repo(self):
        td=Path(tempfile.mkdtemp())
        for sub in ['config','docs/Releases/metrics','docs/Releases','docs/Standards','docs/Integration','skills/x']:
            (td/sub).mkdir(parents=True,exist_ok=True)
        (td/'config/transition-metrics-policy.json').write_text(json.dumps(POLICY,sort_keys=True),encoding='utf-8')
        return td
    def ext(self): return {'type':'EXTERNAL_ARTIFACT','artifact_id':'E','sha256':'a'*64}
    def snapshot(self,repo):
        rec=copy.deepcopy(START)
        rec['baseline_commit']='a'*40; rec['baseline_snapshot']='S'; rec['created_utc']='2026-08-07T12:00:00Z'; rec['prior_handoff_unavailable_reason']='none canonical yet'
        rec['csv_projection_path']='docs/Releases/metrics/s.csv'
        for m in rec['metrics']:
            if m['metric_id']=='M22':
                m.update(value=60,data_quality='MEASURED',collection_method='EVENT_INTERVALS',reason='',evidence_refs=[self.ext()])
            if m['metric_id']=='M23':
                m.update(value=0.0,data_quality='DERIVED',collection_method='EVENT_INTERVALS',reason='',evidence_refs=[self.ext()])
            if m['metric_id']=='M24':
                m.update(value={'total_runs':1,'by_layer_result':[{'test_layer':'UNIT','result':'PASS','count':1}]},data_quality='DERIVED',collection_method='TEST_RUN_LEDGER',reason='',evidence_refs=[self.ext()])
        rec['timing_intervals']=[{'interval_id':'I1','category':'ACTIVE_ENGINEERING','start_utc':'2026-08-07T12:00:00Z','end_utc':'2026-08-07T12:01:00Z'}]
        rec['test_runs']=[{'run_id':'R1','test_layer':'UNIT','result':'PASS','release_authorizing':False,'test_id':'T1','requirement_id':'REQ1','production_function_path':'validator','fixture_provenance':'independent','expected_result_source':'policy','actual_result':'PASS','mutation_boundary':'NONE','cleanup_preserve_behavior':'NONE','evidence_artifact':'E'}]
        # M27 now all 27 denominator metrics are quality-complete.
        next(m for m in rec['metrics'] if m['metric_id']=='M27')['value']=100.0
        self.write_csv(repo,rec)
        return rec
    def write_csv(self,repo,rec):
        p=repo/rec['csv_projection_path']; p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('w',newline='',encoding='utf-8') as fh:
            w=csv.writer(fh,lineterminator='\n'); w.writerow(['metric_id','name','unit','value','data_quality','collection_method','reason'])
            for m in rec['metrics']:
                val=v.csv_cell(m.get('value'))
                w.writerow([m['metric_id'],m['name'],m['unit'],val,m['data_quality'],m['collection_method'],m.get('reason','')])
    def validate(self,repo,rec,path='docs/Releases/metrics/s.json'):
        p=repo/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n',encoding='utf-8')
        return v.validate_files(repo,[path],POLICY)

    def test_valid_snapshot_passes(self):
        repo=self.make_repo(); rec=self.snapshot(repo); self.assertEqual('PASS',self.validate(repo,rec)['status'])
    def test_duplicate_metric_id_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); rec['metrics'][1]['metric_id']='M01'; self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_missing_metric_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); rec['metrics'].pop(); self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_unknown_metric_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); rec['metrics'][-1]['metric_id']='M99'; self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_duplicate_json_key_rejected(self):
        repo=self.make_repo(); p=repo/'x.json'; p.write_text('{"a":1,"a":2}',encoding='utf-8'); self.assertRaises(ValueError,v.load_json_strict,p)
    def test_bad_timestamp_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); rec['created_utc']='bad'; self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_bad_commit_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); rec['baseline_commit']='bad'; self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_negative_count_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); next(m for m in rec['metrics'] if m['metric_id']=='M02')['value']=-1; self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_negative_duration_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); next(m for m in rec['metrics'] if m['metric_id']=='M21')['value']=-1; self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_percent_out_of_bounds_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); m=next(m for m in rec['metrics'] if m['metric_id']=='M05');m['value']=101; self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_unknown_as_zero_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); m=next(m for m in rec['metrics'] if m['metric_id']=='M22');m.update(data_quality='UNKNOWN',value=0,reason='unknown'); self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_missing_evidence_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); next(m for m in rec['metrics'] if m['metric_id']=='M02')['evidence_refs']=[]; self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_invalid_lifecycle_transition_fails(self):
        repo=self.make_repo(); evt={'record_type':POLICY['record_types']['event'],'schema_version':'1.0','workstream_id':'W','event_id':'E1','created_utc':'2026-08-07T12:00:00Z','event_type':'LIFECYCLE','lifecycle_from':'PLANNING_READ_ONLY','lifecycle_to':'IMPLEMENTATION_OFFLINE','classification':'NONE','mutation_boundary_crossed':False,'previous_record':None,'evidence_refs':[self.ext()]}; p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt),encoding='utf-8'); self.assertEqual('FAIL',v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY)['status'])
    def test_unsafe_path_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); rec['csv_projection_path']='../x.csv'; self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_symlink_reference_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); target=repo/'t';target.write_text('x'); link=repo/'docs/Releases/link';link.symlink_to(target); m=next(m for m in rec['metrics'] if m['metric_id']=='M02');m['evidence_refs']=[{'type':'REPO_PATH','path':'docs/Releases/link'}]; self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_markdown_metrics_link_missing_fails(self):
        repo=self.make_repo(); p=repo/'docs/Releases/Test-Handoff.md';p.write_text('# H\n',encoding='utf-8'); self.assertEqual('FAIL',v.validate_files(repo,['docs/Releases/Test-Handoff.md'],POLICY)['status'])
    def test_markdown_metrics_link_missing_target_fails(self):
        repo=self.make_repo(); p=repo/'docs/Releases/Test-Gate.md';p.write_text('TRANSITION_METRICS_RECORD=docs/Releases/metrics/missing.json\n',encoding='utf-8'); self.assertEqual('FAIL',v.validate_files(repo,['docs/Releases/Test-Gate.md'],POLICY)['status'])
    def test_previous_record_hash_mismatch_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); q=repo/'docs/Releases/metrics/prev.json';q.write_text('{}');rec['previous_record']={'path':'docs/Releases/metrics/prev.json','sha256':'a'*64}; self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_csv_projection_mismatch_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo); (repo/rec['csv_projection_path']).write_text('bad\n'); self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_missing_prior_handoff_binding_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo);rec['prior_handoff_available']=True;rec['prior_handoff']=None; self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_external_hold_not_in_m22(self):
        repo=self.make_repo(); rec=self.snapshot(repo);rec['timing_intervals'].append({'interval_id':'I2','category':'HOLD_EXTERNAL','start_utc':'2026-08-07T12:01:00Z','end_utc':'2026-08-07T12:02:00Z'});next(m for m in rec['metrics'] if m['metric_id']=='M21')['value']=60;self.write_csv(repo,rec); self.assertEqual('PASS',self.validate(repo,rec)['status'])
    def test_user_hold_not_in_m22(self):
        repo=self.make_repo(); rec=self.snapshot(repo);rec['timing_intervals'].append({'interval_id':'I2','category':'HOLD_USER','start_utc':'2026-08-07T12:01:00Z','end_utc':'2026-08-07T12:02:00Z'});self.write_csv(repo,rec); self.assertEqual('PASS',self.validate(repo,rec)['status'])
    def test_rework_in_m23_denominator(self):
        repo=self.make_repo(); rec=self.snapshot(repo);rec['timing_intervals']=[{'interval_id':'I1','category':'ACTIVE_ENGINEERING','start_utc':'2026-08-07T12:00:00Z','end_utc':'2026-08-07T12:01:00Z'},{'interval_id':'I2','category':'REWORK','start_utc':'2026-08-07T12:01:00Z','end_utc':'2026-08-07T12:02:00Z'}];next(m for m in rec['metrics'] if m['metric_id']=='M22')['value']=120;next(m for m in rec['metrics'] if m['metric_id']=='M23')['value']=50.0;self.write_csv(repo,rec);self.assertEqual('PASS',self.validate(repo,rec)['status'])
    def test_m24_missing_metadata_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo);del rec['test_runs'][0]['test_layer'];self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_repeat_defect_without_link_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo);rec['defects']=[{'defect_id':'D1','repeated':True}];m=next(m for m in rec['metrics'] if m['metric_id']=='M25');m.update(value=100.0,data_quality='DERIVED',evidence_refs=[self.ext()]);self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_m26_missing_component_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo);rec['snapshot_type']='HANDOFF';rec['handoff_components']=[];m=next(m for m in rec['metrics'] if m['metric_id']=='M26');m.update(value=0.0,data_quality='DERIVED',collection_method='HANDOFF_COMPONENT_COUNT',reason='',evidence_refs=[self.ext()]);self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_change_record_missing_field_fails(self):
        repo=self.make_repo();p=repo/'docs/Releases/X-Plan.md';p.write_text('CHANGE_RECORD_BASELINE=x\n',encoding='utf-8');self.assertEqual('FAIL',v.validate_files(repo,['docs/Releases/X-Plan.md'],POLICY)['status'])
    def test_external_incident_revision_fails(self):
        repo=self.make_repo();evt={'record_type':POLICY['record_types']['event'],'schema_version':'1.0','workstream_id':'W','event_id':'E','created_utc':'2026-08-07T12:00:00Z','event_type':'EXTERNAL_BLOCKER','lifecycle_from':'AUTHORIZED_FOR_SINGLE_LIVE_ATTEMPT','lifecycle_to':'LIVE_EXECUTION_OR_EXTERNAL_CHECKPOINT','classification':'EXTERNAL_CONSTRAINT','mutation_boundary_crossed':False,'previous_record':None,'evidence_refs':[self.ext()],'external_incident':{'candidate_revision_action':'PRESERVE_EXACT_CANDIDATE','code_revision_created':True,'exposed_internal_defect':False}};p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt));self.assertEqual('FAIL',v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY)['status'])
    def test_closed_workstream_reopen_fails(self):
        repo=self.make_repo();evt={'record_type':POLICY['record_types']['event'],'schema_version':'1.0','workstream_id':'W','event_id':'E','created_utc':'2026-08-07T12:00:00Z','event_type':'LIFECYCLE','lifecycle_from':'CLOSED_AND_FROZEN','lifecycle_to':'PLANNING_READ_ONLY','classification':'NONE','mutation_boundary_crossed':False,'previous_record':None,'evidence_refs':[self.ext()]};p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt));self.assertEqual('FAIL',v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY)['status'])
    def test_overlapping_intervals_fail(self):
        repo=self.make_repo();rec=self.snapshot(repo);rec['timing_intervals'].append({'interval_id':'I2','category':'REWORK','start_utc':'2026-08-07T12:00:30Z','end_utc':'2026-08-07T12:01:30Z'});self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_ratio_zero_denominator_fails_when_numeric(self):
        repo=self.make_repo();rec=self.snapshot(repo);m=next(m for m in rec['metrics'] if m['metric_id']=='M05');m['denominator']=0;m['numerator']=0;m['value']=0;self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_m27_unknown_lowers_quality(self):
        repo=self.make_repo();rec=self.snapshot(repo);m=next(m for m in rec['metrics'] if m['metric_id']=='M22');m.update(value=None,data_quality='UNKNOWN',reason='gap',collection_method='GAP',evidence_refs=[]);rec['timing_intervals']=[];m23=next(m for m in rec['metrics'] if m['metric_id']=='M23');m23.update(value=None,data_quality='NOT_APPLICABLE',reason='no active denominator',collection_method='POLICY',evidence_refs=[]);m27=next(m for m in rec['metrics'] if m['metric_id']=='M27');m27['value']=26/27*100;self.write_csv(repo,rec);self.assertEqual('PASS',self.validate(repo,rec)['status'])
    def test_deterministic_report(self):
        repo=self.make_repo();rec=self.snapshot(repo);p=repo/'docs/Releases/metrics/s.json';p.write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n');r1=v.validate_files(repo,['docs/Releases/metrics/s.json'],POLICY);r2=v.validate_files(repo,['docs/Releases/metrics/s.json'],POLICY);self.assertEqual(json.dumps(r1,sort_keys=True),json.dumps(r2,sort_keys=True))
    def test_non_transition_json_ignored(self):
        repo=self.make_repo();p=repo/'docs/Releases/metrics/other.json';p.write_text('{"x":1}');self.assertEqual('PASS',v.validate_files(repo,['docs/Releases/metrics/other.json'],POLICY)['status'])
    def test_valid_event_passes(self):
        repo=self.make_repo();evt={'record_type':POLICY['record_types']['event'],'schema_version':'1.0','workstream_id':'W','event_id':'E','created_utc':'2026-08-07T12:00:00Z','event_type':'LIFECYCLE','lifecycle_from':'PLANNING_READ_ONLY','lifecycle_to':'DESIGN_QUALIFICATION','classification':'NONE','mutation_boundary_crossed':False,'previous_record':None,'evidence_refs':[self.ext()]};p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt));self.assertEqual('PASS',v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY)['status'])
    def test_valid_deviation_passes(self):
        repo=self.make_repo();evt={'record_type':POLICY['record_types']['event'],'schema_version':'1.0','workstream_id':'W','event_id':'E','created_utc':'2026-08-07T12:00:00Z','event_type':'DEVIATION','lifecycle_from':'DESIGN_QUALIFICATION','lifecycle_to':'IMPLEMENTATION_OFFLINE','classification':'REVIEW_TEST_DEFECT','mutation_boundary_crossed':False,'previous_record':None,'evidence_refs':[self.ext()],'deviation':{'deviation_id':'D1','timestamp_utc':'2026-08-07T12:00:00Z','category':'REVIEW','planned_condition':'x','observed_condition':'y','impact':'z','mutation_status':'NONE','evidence_reference':'E','owner_disposition':'CORRECT','permanent_control_decision':'ADD_TEST'}};p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt));self.assertEqual('PASS',v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY)['status'])

    def test_standard_handoff_word_does_not_require_metrics_link(self):
        repo=self.make_repo();p=repo/'docs/Standards/Example-Handoff-Standard.md';p.write_text('# Standard\n',encoding='utf-8');self.assertEqual('PASS',v.validate_files(repo,['docs/Standards/Example-Handoff-Standard.md'],POLICY)['status'])
    def test_repository_template_snapshot_passes(self):
        report=v.validate_files(ROOT,['docs/Templates/SMT-Transition-Metrics-Baseline-Template.json'],POLICY);self.assertEqual('PASS',report['status'],report['violations'])

    def test_same_state_deviation_passes(self):
        repo=self.make_repo();evt={'record_type':POLICY['record_types']['event'],'schema_version':'1.0','workstream_id':'W','event_id':'E','created_utc':'2026-08-07T12:00:00Z','event_type':'DEVIATION','lifecycle_from':'IMPLEMENTATION_OFFLINE','lifecycle_to':'IMPLEMENTATION_OFFLINE','classification':'REVIEW_TEST_DEFECT','mutation_boundary_crossed':False,'previous_record':None,'evidence_refs':[self.ext()],'deviation':{'deviation_id':'D1','timestamp_utc':'2026-08-07T12:00:00Z','category':'INTERNAL_QUALIFICATION','planned_condition':'PASS','observed_condition':'FAIL','impact':'NO_RELEASE','mutation_status':'OFFLINE_ONLY','evidence_reference':'E','owner_disposition':'CORRECT_BEFORE_RELEASE','permanent_control_decision':'ADD_REGRESSION_TEST'}};p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt));self.assertEqual('PASS',v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY)['status'])

if __name__=='__main__': unittest.main()
