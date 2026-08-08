from __future__ import annotations

import ast
import copy
import csv
import hashlib
import importlib.util
import json
import subprocess
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

    def make_handoff(self,repo,rec):
        rec['snapshot_type']='HANDOFF'
        components=[]
        for idx,cid in enumerate(POLICY['required_handoff_components']):
            rel=f'docs/Releases/handoff/component-{idx:02d}.txt'
            full=repo/rel;full.parent.mkdir(parents=True,exist_ok=True);full.write_text(f'{cid}\n',encoding='utf-8')
            components.append({'component_id':cid,'status':'PRESENT','path':rel,'sha256':hashlib.sha256(full.read_bytes()).hexdigest()})
        rec['handoff_components']=components
        m26=next(m for m in rec['metrics'] if m['metric_id']=='M26')
        m26.update(value=100.0,data_quality='DERIVED',collection_method='HANDOFF_COMPONENT_FILE_AND_DIGEST_VALIDATION',reason='',evidence_refs=[self.ext()])
        next(m for m in rec['metrics'] if m['metric_id']=='M27')['value']=100.0
        self.write_csv(repo,rec)
        return rec


    def test_security_sensitive_content_negative_corpus_fails(self):
        samples=[
            '-----BEGIN PRIVATE KEY-----',
            'Bearer abcdefghijklmnop',
            'ghp_abcdefghijklmnopqrstuvwxyz123456',
            'sk-abcdefghijklmnopqrstuvwxyz123456',
            'AKIAABCDEFGHIJKLMNOP',
            'password=supersecret',
            '123-45-6789',
            'person@example.com',
            'Traceback (most recent call last):',
            'BEGIN SYSTEM PROMPT',
        ]
        for sample in samples:
            with self.subTest(sample=sample):
                repo=self.make_repo();rec=self.snapshot(repo);m=next(x for x in rec['metrics'] if x['metric_id']=='M02');m['reason']=sample;self.write_csv(repo,rec);report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('prohibited' in x for x in report['violations']),report)

    def test_normal_governance_text_is_not_security_false_positive(self):
        repo=self.make_repo();rec=self.snapshot(repo);m=next(x for x in rec['metrics'] if x['metric_id']=='M02');m['reason']='No user-visible replacement package was issued';self.write_csv(repo,rec);self.assertEqual('PASS',self.validate(repo,rec)['status'])

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
    def test_markdown_metrics_link_unrelated_json_fails(self):
        repo=self.make_repo(); p=repo/'docs/Releases/Test-Gate.md';p.write_text('TRANSITION_METRICS_RECORD=config/transition-metrics-policy.json\n',encoding='utf-8'); self.assertEqual('FAIL',v.validate_files(repo,['docs/Releases/Test-Gate.md'],POLICY)['status'])
    def test_markdown_metrics_link_valid_snapshot_passes(self):
        repo=self.make_repo(); rec=self.snapshot(repo); self.validate(repo,rec); p=repo/'docs/Releases/Test-Gate.md';p.write_text('TRANSITION_METRICS_RECORD=docs/Releases/metrics/s.json\n',encoding='utf-8'); self.assertEqual('PASS',v.validate_files(repo,['docs/Releases/Test-Gate.md'],POLICY)['status'])
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
    def test_m21_incorrect_computed_value_fails(self):
        repo=self.make_repo();rec=self.snapshot(repo);rec['timing_intervals'].append({'interval_id':'I2','category':'HOLD_EXTERNAL','start_utc':'2026-08-07T12:01:00Z','end_utc':'2026-08-07T12:02:00Z'});next(m for m in rec['metrics'] if m['metric_id']=='M21')['value']=0;self.write_csv(repo,rec);report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('M21: value does not match timing intervals' in x for x in report['violations']),report)
    def test_m22_incorrect_computed_value_fails(self):
        repo=self.make_repo();rec=self.snapshot(repo);next(m for m in rec['metrics'] if m['metric_id']=='M22')['value']=30;self.write_csv(repo,rec);report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('M22: value does not match timing intervals' in x for x in report['violations']),report)
    def test_m23_nonzero_denominator_value_mismatch_fails(self):
        repo=self.make_repo();rec=self.snapshot(repo);rec['timing_intervals']=[{'interval_id':'I1','category':'ACTIVE_ENGINEERING','start_utc':'2026-08-07T12:00:00Z','end_utc':'2026-08-07T12:01:00Z'},{'interval_id':'I2','category':'REWORK','start_utc':'2026-08-07T12:01:00Z','end_utc':'2026-08-07T12:02:00Z'}];next(m for m in rec['metrics'] if m['metric_id']=='M22')['value']=120;next(m for m in rec['metrics'] if m['metric_id']=='M23')['value']=40.0;self.write_csv(repo,rec);report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('M23: value does not match rework/active ratio' in x for x in report['violations']),report)

    def test_m24_missing_metadata_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo);del rec['test_runs'][0]['test_layer'];self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_repeat_defect_without_link_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo);rec['defects']=[{'defect_id':'D1','repeated':True}];m=next(m for m in rec['metrics'] if m['metric_id']=='M25');m.update(value=100.0,data_quality='DERIVED',evidence_refs=[self.ext()]);self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_m26_missing_component_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo);rec['snapshot_type']='HANDOFF';rec['handoff_components']=[];m=next(m for m in rec['metrics'] if m['metric_id']=='M26');m.update(value=0.0,data_quality='DERIVED',collection_method='HANDOFF_COMPONENT_COUNT',reason='',evidence_refs=[self.ext()]);self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_valid_handoff_components_and_digests_pass(self):
        repo=self.make_repo(); rec=self.make_handoff(repo,self.snapshot(repo)); self.assertEqual('PASS',self.validate(repo,rec)['status'])
    def test_handoff_component_missing_file_fails(self):
        repo=self.make_repo(); rec=self.make_handoff(repo,self.snapshot(repo)); (repo/rec['handoff_components'][0]['path']).unlink(); self.assertEqual('FAIL',self.validate(repo,rec)['status'])
    def test_handoff_component_digest_mismatch_fails(self):
        repo=self.make_repo(); rec=self.make_handoff(repo,self.snapshot(repo)); rec['handoff_components'][0]['sha256']='b'*64; self.assertEqual('FAIL',self.validate(repo,rec)['status'])
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
    def test_m23_zero_active_requires_canonical_not_applicable(self):
        repo=self.make_repo();rec=self.snapshot(repo);rec['timing_intervals']=[]
        m22=next(m for m in rec['metrics'] if m['metric_id']=='M22');m22.update(value=0,data_quality='MEASURED',collection_method='EVENT_INTERVALS',reason='',evidence_refs=[self.ext()])
        m23=next(m for m in rec['metrics'] if m['metric_id']=='M23');m23.update(value=None,data_quality='UNKNOWN',reason='unknown',collection_method='GAP',evidence_refs=[])
        m27=next(m for m in rec['metrics'] if m['metric_id']=='M27');m27['value']=26/27*100
        self.write_csv(repo,rec);report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('M23: zero active denominator requires NOT_APPLICABLE' in x for x in report['violations']),report)

    def test_m23_zero_active_canonical_not_applicable_passes(self):
        repo=self.make_repo();rec=self.snapshot(repo);rec['timing_intervals']=[]
        m22=next(m for m in rec['metrics'] if m['metric_id']=='M22');m22.update(value=0,data_quality='MEASURED',collection_method='EVENT_INTERVALS',reason='',evidence_refs=[self.ext()])
        m23=next(m for m in rec['metrics'] if m['metric_id']=='M23');m23.update(value=None,data_quality='NOT_APPLICABLE',reason='no active denominator',collection_method='POLICY',evidence_refs=[])
        self.write_csv(repo,rec);self.assertEqual('PASS',self.validate(repo,rec)['status'])


    def test_m25_numerator_only_mismatch_fails(self):
        repo=self.make_repo();rec=self.snapshot(repo);rec['defects']=[{'defect_id':'D1','classification':'IMPLEMENTATION_DEFECT','repeated':True,'prior_lesson_or_control_ref':'CTRL'},{'defect_id':'D2','classification':'IMPLEMENTATION_DEFECT','repeated':False,'prior_lesson_or_control_ref':None}]
        m=next(x for x in rec['metrics'] if x['metric_id']=='M25');m.update(value=50.0,data_quality='DERIVED',collection_method='DEFECT_LEDGER',reason='',evidence_refs=[self.ext()],numerator=0,denominator=2)
        self.write_csv(repo,rec);report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('M25: numerator does not match' in x for x in report['violations']),report)

    def test_m25_denominator_only_mismatch_fails(self):
        repo=self.make_repo();rec=self.snapshot(repo);rec['defects']=[{'defect_id':'D1','classification':'IMPLEMENTATION_DEFECT','repeated':True,'prior_lesson_or_control_ref':'CTRL'},{'defect_id':'D2','classification':'IMPLEMENTATION_DEFECT','repeated':False,'prior_lesson_or_control_ref':None}]
        m=next(x for x in rec['metrics'] if x['metric_id']=='M25');m.update(value=50.0,data_quality='DERIVED',collection_method='DEFECT_LEDGER',reason='',evidence_refs=[self.ext()],numerator=1,denominator=3)
        self.write_csv(repo,rec);report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('M25: denominator does not match' in x for x in report['violations']),report)

    def test_m25_ratio_only_mismatch_fails(self):
        repo=self.make_repo();rec=self.snapshot(repo);rec['defects']=[{'defect_id':'D1','classification':'IMPLEMENTATION_DEFECT','repeated':True,'prior_lesson_or_control_ref':'CTRL'},{'defect_id':'D2','classification':'IMPLEMENTATION_DEFECT','repeated':False,'prior_lesson_or_control_ref':None}]
        m=next(x for x in rec['metrics'] if x['metric_id']=='M25');m.update(value=40.0,data_quality='DERIVED',collection_method='DEFECT_LEDGER',reason='',evidence_refs=[self.ext()],numerator=1,denominator=2)
        self.write_csv(repo,rec);report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('M25: value does not match defect ledger' in x for x in report['violations']),report)

    def test_m25_ratio_operand_requirement_can_strengthen_false_to_true(self):
        base=copy.deepcopy(POLICY);base['metrics']['M25']['ratio_inputs_required_when_numeric']=False
        current=copy.deepcopy(POLICY)
        self.assertEqual([],v.policy_identity_compatibility_errors(base,current))

    def test_m25_ratio_operand_requirement_cannot_weaken_true_to_false(self):
        base=copy.deepcopy(POLICY);current=copy.deepcopy(POLICY);current['metrics']['M25']['ratio_inputs_required_when_numeric']=False
        errors=v.policy_identity_compatibility_errors(base,current);self.assertTrue(any('metrics is immutable' in x and 'M25' in x for x in errors),errors)

    def test_m25_zero_defects_requires_canonical_not_applicable(self):
        repo=self.make_repo();rec=self.snapshot(repo);rec['defects']=[]
        m25=next(m for m in rec['metrics'] if m['metric_id']=='M25');m25.update(value=None,data_quality='UNKNOWN',reason='unknown',collection_method='GAP',evidence_refs=[])
        m27=next(m for m in rec['metrics'] if m['metric_id']=='M27');m27['value']=26/27*100
        self.write_csv(repo,rec);report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('M25: no defects requires NOT_APPLICABLE' in x for x in report['violations']),report)

    def test_m25_zero_defects_canonical_not_applicable_passes(self):
        repo=self.make_repo();rec=self.snapshot(repo);rec['defects']=[]
        m25=next(m for m in rec['metrics'] if m['metric_id']=='M25');m25.update(value=None,data_quality='NOT_APPLICABLE',reason='no defects',collection_method='POLICY',evidence_refs=[])
        self.write_csv(repo,rec);self.assertEqual('PASS',self.validate(repo,rec)['status'])

    def test_m27_unknown_lowers_quality(self):
        repo=self.make_repo();rec=self.snapshot(repo);m=next(m for m in rec['metrics'] if m['metric_id']=='M22');m.update(value=None,data_quality='UNKNOWN',reason='gap',collection_method='GAP',evidence_refs=[]);rec['timing_intervals']=[];m23=next(m for m in rec['metrics'] if m['metric_id']=='M23');m23.update(value=None,data_quality='NOT_APPLICABLE',reason='no active denominator',collection_method='POLICY',evidence_refs=[]);m27=next(m for m in rec['metrics'] if m['metric_id']=='M27');m27['value']=26/27*100;self.write_csv(repo,rec);self.assertEqual('PASS',self.validate(repo,rec)['status'])
    def test_deterministic_report(self):
        repo=self.make_repo();rec=self.snapshot(repo);p=repo/'docs/Releases/metrics/s.json';p.write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n');r1=v.validate_files(repo,['docs/Releases/metrics/s.json'],POLICY);r2=v.validate_files(repo,['docs/Releases/metrics/s.json'],POLICY);self.assertEqual(json.dumps(r1,sort_keys=True),json.dumps(r2,sort_keys=True))
    def test_unknown_record_type_in_metrics_directory_fails(self):
        repo=self.make_repo();p=repo/'docs/Releases/metrics/other.json';p.write_text('{"record_type":"TYPO"}');self.assertEqual('FAIL',v.validate_files(repo,['docs/Releases/metrics/other.json'],POLICY)['status'])
    def test_missing_record_type_in_metrics_directory_fails(self):
        repo=self.make_repo();p=repo/'docs/Releases/metrics/other.json';p.write_text('{"x":1}');self.assertEqual('FAIL',v.validate_files(repo,['docs/Releases/metrics/other.json'],POLICY)['status'])
    def test_non_transition_json_outside_metrics_directory_ignored(self):
        repo=self.make_repo();p=repo/'config/other.json';p.write_text('{"x":1}');self.assertEqual('PASS',v.validate_files(repo,['config/other.json'],POLICY)['status'])
    def test_valid_event_passes(self):
        repo=self.make_repo();evt={'record_type':POLICY['record_types']['event'],'schema_version':'1.0','workstream_id':'W','event_id':'E','created_utc':'2026-08-07T12:00:00Z','event_type':'LIFECYCLE','lifecycle_from':'PLANNING_READ_ONLY','lifecycle_to':'DESIGN_QUALIFICATION','classification':'NONE','mutation_boundary_crossed':False,'previous_record':None,'evidence_refs':[self.ext()]};p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt));self.assertEqual('PASS',v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY)['status'])
    def test_event_missing_workstream_id_fails(self):
        repo=self.make_repo();evt={'record_type':POLICY['record_types']['event'],'schema_version':'1.0','event_id':'E','created_utc':'2026-08-07T12:00:00Z','event_type':'LIFECYCLE','lifecycle_from':'PLANNING_READ_ONLY','lifecycle_to':'DESIGN_QUALIFICATION','classification':'NONE','mutation_boundary_crossed':False,'previous_record':None,'evidence_refs':[self.ext()]};p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt));self.assertEqual('FAIL',v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY)['status'])
    def test_valid_deviation_passes(self):
        repo=self.make_repo();evt={'record_type':POLICY['record_types']['event'],'schema_version':'1.0','workstream_id':'W','event_id':'E','created_utc':'2026-08-07T12:00:00Z','event_type':'DEVIATION','lifecycle_from':'DESIGN_QUALIFICATION','lifecycle_to':'IMPLEMENTATION_OFFLINE','classification':'REVIEW_TEST_DEFECT','mutation_boundary_crossed':False,'previous_record':None,'evidence_refs':[self.ext()],'deviation':{'deviation_id':'D1','timestamp_utc':'2026-08-07T12:00:00Z','category':'REVIEW','planned_condition':'x','observed_condition':'y','impact':'z','mutation_status':'NONE','evidence_reference':'E','owner_disposition':'CORRECT','permanent_control_decision':'ADD_TEST'}};p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt));self.assertEqual('PASS',v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY)['status'])

    def test_standard_handoff_word_does_not_require_metrics_link(self):
        repo=self.make_repo();p=repo/'docs/Standards/Example-Handoff-Standard.md';p.write_text('# Standard\n',encoding='utf-8');self.assertEqual('PASS',v.validate_files(repo,['docs/Standards/Example-Handoff-Standard.md'],POLICY)['status'])
    def test_repository_template_snapshot_passes(self):
        report=v.validate_files(ROOT,['docs/Templates/SMT-Transition-Metrics-Baseline-Template.json'],POLICY);self.assertEqual('PASS',report['status'],report['violations'])

    def test_same_state_deviation_passes(self):
        repo=self.make_repo();evt={'record_type':POLICY['record_types']['event'],'schema_version':'1.0','workstream_id':'W','event_id':'E','created_utc':'2026-08-07T12:00:00Z','event_type':'DEVIATION','lifecycle_from':'IMPLEMENTATION_OFFLINE','lifecycle_to':'IMPLEMENTATION_OFFLINE','classification':'REVIEW_TEST_DEFECT','mutation_boundary_crossed':False,'previous_record':None,'evidence_refs':[self.ext()],'deviation':{'deviation_id':'D1','timestamp_utc':'2026-08-07T12:00:00Z','category':'INTERNAL_QUALIFICATION','planned_condition':'PASS','observed_condition':'FAIL','impact':'NO_RELEASE','mutation_status':'OFFLINE_ONLY','evidence_reference':'E','owner_disposition':'CORRECT_BEFORE_RELEASE','permanent_control_decision':'ADD_REGRESSION_TEST'}};p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt));self.assertEqual('PASS',v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY)['status'])

    def git(self, repo, *args):
        return subprocess.run(["git", *args], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.strip()

    def init_git(self, repo):
        self.git(repo, "init", "-q")
        self.git(repo, "config", "user.name", "Test User")
        self.git(repo, "config", "user.email", "test@example.invalid")

    def commit_all(self, repo, message):
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-q", "-m", message)
        return self.git(repo, "rev-parse", "HEAD")

    def write_bound_record(self, repo, rel, record):
        full=repo/rel; full.parent.mkdir(parents=True,exist_ok=True)
        full.write_text(json.dumps(record,sort_keys=True)+'\n',encoding='utf-8')
        return {'path':rel,'sha256':hashlib.sha256(full.read_bytes()).hexdigest()}

    def test_git_diff_reports_deleted_governed_metrics_record(self):
        repo=self.make_repo(); self.init_git(repo)
        p=repo/'docs/Releases/metrics/deleted.json'; p.write_text('{"record_type":"SMT_TRANSITION_EVENT"}\n',encoding='utf-8')
        base=self.commit_all(repo,'base')
        p.unlink(); self.commit_all(repo,'delete')
        paths,deleted=v.changed_files(repo,base)
        self.assertNotIn('docs/Releases/metrics/deleted.json',paths)
        self.assertIn('docs/Releases/metrics/deleted.json',deleted)
        violations=v.validate_deleted_paths(repo,deleted,POLICY)
        self.assertTrue(any('deletion of governed transition artifact is prohibited' in x for x in violations),violations)

    def test_deleted_unrelated_unreferenced_file_is_not_transition_violation(self):
        repo=self.make_repo(); self.init_git(repo)
        p=repo/'notes.txt'; p.write_text('x\n',encoding='utf-8')
        base=self.commit_all(repo,'base')
        p.unlink(); self.commit_all(repo,'delete')
        _,deleted=v.changed_files(repo,base)
        self.assertEqual([],v.validate_deleted_paths(repo,deleted,POLICY))

    def test_deleted_referenced_evidence_file_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo)
        evidence=repo/'evidence.txt'; evidence.write_text('evidence\n',encoding='utf-8')
        m=next(m for m in rec['metrics'] if m['metric_id']=='M02')
        m['evidence_refs']=[{'type':'REPO_PATH','path':'evidence.txt','sha256':hashlib.sha256(evidence.read_bytes()).hexdigest()}]
        self.write_csv(repo,rec); self.validate(repo,rec)
        self.init_git(repo); base=self.commit_all(repo,'base')
        evidence.unlink(); self.commit_all(repo,'delete evidence')
        _,deleted=v.changed_files(repo,base)
        violations=v.validate_deleted_paths(repo,deleted,POLICY)
        self.assertTrue(any('dangling transition reference' in x for x in violations),violations)

    def test_deleted_metrics_snapshot_reports_unchanged_markdown_link(self):
        repo=self.make_repo(); rec=self.snapshot(repo); self.validate(repo,rec)
        md=repo/'docs/Releases/Test-Gate.md'; md.write_text('TRANSITION_METRICS_RECORD=docs/Releases/metrics/s.json\n',encoding='utf-8')
        self.init_git(repo); base=self.commit_all(repo,'base')
        (repo/'docs/Releases/metrics/s.json').unlink(); self.commit_all(repo,'delete snapshot')
        _,deleted=v.changed_files(repo,base)
        violations=v.validate_deleted_paths(repo,deleted,POLICY)
        self.assertTrue(any('Test-Gate.md' in x and 'dangling transition reference' in x for x in violations),violations)

    def test_previous_record_unrelated_json_fails_semantic_binding(self):
        repo=self.make_repo(); rec=self.snapshot(repo)
        full=repo/'config/transition-metrics-policy.json'
        rec['previous_record']={'path':'config/transition-metrics-policy.json','sha256':hashlib.sha256(full.read_bytes()).hexdigest()}
        self.assertEqual('FAIL',self.validate(repo,rec)['status'])

    def test_previous_record_different_workstream_fails(self):
        repo=self.make_repo(); rec=self.snapshot(repo)
        target={'record_type':POLICY['record_types']['event'],'workstream_id':'OTHER'}
        rec['previous_record']=self.write_bound_record(repo,'docs/Releases/metrics/prev.json',target)
        self.assertEqual('FAIL',self.validate(repo,rec)['status'])

    def test_previous_record_same_workstream_transition_record_passes(self):
        repo=self.make_repo(); rec=self.snapshot(repo)
        target={'record_type':POLICY['record_types']['event'],'workstream_id':rec['workstream_id']}
        rec['previous_record']=self.write_bound_record(repo,'docs/Releases/metrics/prev.json',target)
        self.assertEqual('PASS',self.validate(repo,rec)['status'])

    def test_prior_handoff_requires_handoff_snapshot_same_workstream(self):
        repo=self.make_repo(); rec=self.snapshot(repo)
        target={'record_type':POLICY['record_types']['snapshot'],'snapshot_type':'GATE','workstream_id':rec['workstream_id']}
        rec['prior_handoff_available']=True; rec['prior_handoff_unavailable_reason']=''; rec['prior_handoff']=self.write_bound_record(repo,'docs/Releases/metrics/prior.json',target)
        self.assertEqual('FAIL',self.validate(repo,rec)['status'])

    def test_prior_handoff_valid_semantic_binding_passes(self):
        repo=self.make_repo(); rec=self.snapshot(repo)
        target={'record_type':POLICY['record_types']['snapshot'],'snapshot_type':'HANDOFF','workstream_id':rec['workstream_id']}
        rec['prior_handoff_available']=True; rec['prior_handoff_unavailable_reason']=''; rec['prior_handoff']=self.write_bound_record(repo,'docs/Releases/metrics/prior.json',target)
        self.assertEqual('PASS',self.validate(repo,rec)['status'])

    def test_m26_malformed_string_returns_structured_fail(self):
        repo=self.make_repo(); rec=self.make_handoff(repo,self.snapshot(repo)); m=next(m for m in rec['metrics'] if m['metric_id']=='M26');m['value']='bad';self.write_csv(repo,rec)
        report=self.validate(repo,rec); self.assertEqual('FAIL',report['status']); self.assertTrue(report['violations'])

    def test_m26_null_returns_structured_fail(self):
        repo=self.make_repo(); rec=self.make_handoff(repo,self.snapshot(repo)); m=next(m for m in rec['metrics'] if m['metric_id']=='M26');m['value']=None;self.write_csv(repo,rec)
        report=self.validate(repo,rec); self.assertEqual('FAIL',report['status']); self.assertTrue(report['violations'])

    def test_ratio_metric_malformed_value_returns_structured_fail(self):
        repo=self.make_repo(); rec=self.snapshot(repo); m=next(m for m in rec['metrics'] if m['metric_id']=='M05');m['value']='bad';self.write_csv(repo,rec)
        report=self.validate(repo,rec); self.assertEqual('FAIL',report['status']); self.assertTrue(report['violations'])

    def test_m25_malformed_value_returns_structured_fail(self):
        repo=self.make_repo(); rec=self.snapshot(repo);rec['defects']=[{'defect_id':'D1','repeated':False}];m=next(m for m in rec['metrics'] if m['metric_id']=='M25');m.update(value='bad',data_quality='DERIVED',collection_method='DEFECT_LEDGER',reason='',evidence_refs=[self.ext()]);self.write_csv(repo,rec)
        report=self.validate(repo,rec); self.assertEqual('FAIL',report['status']); self.assertTrue(report['violations'])

    def test_m27_malformed_value_returns_structured_fail(self):
        repo=self.make_repo(); rec=self.snapshot(repo);m=next(m for m in rec['metrics'] if m['metric_id']=='M27');m['value']='bad';self.write_csv(repo,rec)
        report=self.validate(repo,rec); self.assertEqual('FAIL',report['status']); self.assertTrue(report['violations'])

    def test_main_base_ref_deleted_governed_record_fails(self):
        repo=self.make_repo(); self.init_git(repo)
        p=repo/'docs/Releases/metrics/deleted.json'; p.write_text('{"record_type":"SMT_TRANSITION_EVENT"}\n',encoding='utf-8')
        base=self.commit_all(repo,'base')
        p.unlink(); self.commit_all(repo,'delete')
        report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)])
        data=json.loads(report.read_text())
        self.assertEqual(1,rc); self.assertEqual('FAIL',data['status']); self.assertIn('docs/Releases/metrics/deleted.json',data['deleted_paths'])

    def test_main_base_ref_unrelated_deletion_passes(self):
        repo=self.make_repo(); self.init_git(repo)
        p=repo/'notes.txt'; p.write_text('x\n',encoding='utf-8')
        base=self.commit_all(repo,'base')
        p.unlink(); self.commit_all(repo,'delete')
        report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)])
        data=json.loads(report.read_text())
        self.assertEqual(0,rc); self.assertEqual('PASS',data['status']); self.assertEqual(['notes.txt'],data['deleted_paths'])

    def test_load_json_strict_rejects_nonfinite_constants(self):
        repo=self.make_repo()
        for token in ['NaN','Infinity','-Infinity']:
            with self.subTest(token=token):
                p=repo/f'nonfinite-{token.replace("-", "neg-")}.json'
                p.write_text('{"value":'+token+'}',encoding='utf-8')
                with self.assertRaises(ValueError):
                    v.load_json_strict(p)

    def test_ratio_nonfinite_operands_return_structured_fail(self):
        cases=[('numerator',float('nan')),('numerator',float('inf')),('numerator',float('-inf')),('denominator',float('nan')),('denominator',float('inf')),('denominator',float('-inf'))]
        for field,bad in cases:
            with self.subTest(field=field,bad=repr(bad)):
                repo=self.make_repo(); rec=self.snapshot(repo); m=next(m for m in rec['metrics'] if m['metric_id']=='M05');m[field]=bad;self.write_csv(repo,rec)
                report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])

    def test_ratio_huge_integer_operand_returns_structured_fail(self):
        repo=self.make_repo();rec=self.snapshot(repo);m=next(m for m in rec['metrics'] if m['metric_id']=='M05');m['numerator']=10**400;self.write_csv(repo,rec)
        report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])

    def test_pass_fail_malformed_values_return_structured_fail(self):
        malformed=[[],{},None,0,1,True,False,3.14]
        for bad in malformed:
            with self.subTest(bad=repr(bad)):
                repo=self.make_repo();rec=self.snapshot(repo);m=next(m for m in rec['metrics'] if m['metric_id']=='M10');m.update(value=bad,data_quality='MEASURED',collection_method='TEST_RESULT',reason='',evidence_refs=[self.ext()]);self.write_csv(repo,rec)
                report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])

    def test_pass_fail_valid_strings_pass_domain_check(self):
        definition=POLICY['metrics']['M10']
        for value in ['PASS','FAIL']:
            with self.subTest(value=value):
                errors=[]
                metric={'metric_id':'M10','value':value,'data_quality':'MEASURED','collection_method':'TEST_RESULT','reason':'','evidence_refs':[self.ext()]}
                v.metric_value_domain(metric,definition,errors,'M10')
                self.assertEqual([],errors)

    def test_metric_value_domain_malformed_type_matrix_is_fail_closed(self):
        bad_by_type={
            'COUNT':[[],{},'x',1.5,True,None],
            'DURATION_SECONDS':[[],{},'x',1.5,True,None],
            'PERCENT':[[],{},'x',True,None,float('nan'),float('inf'),float('-inf')],
            'PASS_FAIL':[[],{},0,1,True,False,None,3.14],
            'TEST_DISTRIBUTION':[[],'x',0,1,True,None],
        }
        for metric_id,definition in POLICY['metrics'].items():
            for bad in bad_by_type[definition['value_type']]:
                with self.subTest(metric_id=metric_id,value_type=definition['value_type'],bad=repr(bad)):
                    errors=[]
                    metric={'metric_id':metric_id,'value':bad,'data_quality':'MEASURED','collection_method':'MALFORMED_VALUE_REGRESSION','reason':'','evidence_refs':[self.ext()]}
                    v.metric_value_domain(metric,definition,errors,metric_id)
                    self.assertTrue(errors,(metric_id,definition['value_type'],bad))

    def test_finite_number_rejects_nonfinite_and_overflow(self):
        self.assertIsNone(v.finite_number(float('nan')))
        self.assertIsNone(v.finite_number(float('inf')))
        self.assertIsNone(v.finite_number(float('-inf')))
        self.assertIsNone(v.finite_number(10**10000))
        self.assertIsNone(v.finite_number(True))
        self.assertEqual(12.5,v.finite_number(12.5))

    def test_percent_huge_integer_returns_structured_fail(self):
        repo=self.make_repo();rec=self.snapshot(repo);m=next(m for m in rec['metrics'] if m['metric_id']=='M05');m['value']=10**400;self.write_csv(repo,rec)
        report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])

    def test_computed_duration_huge_integer_cannot_silently_pass(self):
        repo=self.make_repo();rec=self.snapshot(repo);m=next(m for m in rec['metrics'] if m['metric_id']=='M22');m['value']=10**400;self.write_csv(repo,rec)
        report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])

    def test_metric_data_quality_container_matrix_is_fail_closed(self):
        malformed=[[],{},0,1,True,False,3.14]
        for metric_id in POLICY['metric_order']:
            for bad in malformed:
                with self.subTest(metric_id=metric_id,bad=repr(bad)):
                    repo=self.make_repo();rec=self.snapshot(repo);m=next(m for m in rec['metrics'] if m['metric_id']==metric_id);m['data_quality']=bad;self.write_csv(repo,rec)
                    report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])

    def test_evidence_reference_type_containers_are_fail_closed(self):
        for bad in [[],{},0,1,True,False,3.14,None]:
            with self.subTest(bad=repr(bad)):
                repo=self.make_repo();rec=self.snapshot(repo);m=next(m for m in rec['metrics'] if m['metric_id']=='M02');m['evidence_refs']=[{'type':bad}];self.write_csv(repo,rec)
                report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])

    def test_test_run_result_containers_are_fail_closed(self):
        for bad in [[],{},0,1,True,False,3.14,None]:
            with self.subTest(bad=repr(bad)):
                repo=self.make_repo();rec=self.snapshot(repo);rec['test_runs'][0]['result']=bad;self.write_csv(repo,rec)
                report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])

    def test_event_type_containers_are_fail_closed(self):
        for bad in [[],{},0,1,True,False,3.14,None]:
            with self.subTest(bad=repr(bad)):
                repo=self.make_repo();evt={'record_type':POLICY['record_types']['event'],'schema_version':'1.0','workstream_id':'W','event_id':'E','created_utc':'2026-08-07T12:00:00Z','event_type':bad,'lifecycle_from':'PLANNING_READ_ONLY','lifecycle_to':'DESIGN_QUALIFICATION','classification':'NONE','mutation_boundary_crossed':False,'previous_record':None,'evidence_refs':[self.ext()]};p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt));
                report=v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY);self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])

    def test_modified_referenced_evidence_revalidates_unchanged_snapshot(self):
        repo=self.make_repo(); evidence=repo/'evidence.txt'; evidence.write_text('before\n',encoding='utf-8'); rec=self.snapshot(repo);m=next(m for m in rec['metrics'] if m['metric_id']=='M02');m['evidence_refs']=[{'type':'REPO_PATH','path':'evidence.txt','sha256':hashlib.sha256(evidence.read_bytes()).hexdigest()}];self.write_csv(repo,rec);self.validate(repo,rec)
        self.init_git(repo);base=self.commit_all(repo,'base');evidence.write_text('after\n',encoding='utf-8');self.commit_all(repo,'modify evidence');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertIn('docs/Releases/metrics/s.json',data['reverse_reference_paths']);self.assertTrue(any('reference sha256 mismatch' in x for x in data['violations']),data['violations'])

    def test_modified_handoff_component_revalidates_unchanged_handoff(self):
        repo=self.make_repo();rec=self.make_handoff(repo,self.snapshot(repo));self.validate(repo,rec);self.init_git(repo);base=self.commit_all(repo,'base');component=repo/rec['handoff_components'][0]['path'];component.write_text('modified\n',encoding='utf-8');self.commit_all(repo,'modify component');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertIn('docs/Releases/metrics/s.json',data['reverse_reference_paths']);self.assertTrue(any('handoff component sha256 mismatch' in x for x in data['violations']),data['violations'])

    def test_modified_csv_projection_revalidates_unchanged_snapshot(self):
        repo=self.make_repo();rec=self.snapshot(repo);self.validate(repo,rec);self.init_git(repo);base=self.commit_all(repo,'base');csv_path=repo/rec['csv_projection_path'];csv_path.write_text('bad\n',encoding='utf-8');self.commit_all(repo,'modify csv');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertIn('docs/Releases/metrics/s.json',data['reverse_reference_paths']);self.assertTrue(any('CSV header mismatch' in x for x in data['violations']),data['violations'])

    def test_modified_bound_record_revalidates_unchanged_dependent(self):
        repo=self.make_repo();rec=self.snapshot(repo);target={'record_type':POLICY['record_types']['event'],'workstream_id':rec['workstream_id']};rec['previous_record']=self.write_bound_record(repo,'docs/Releases/metrics/prev.json',target);self.validate(repo,rec);self.init_git(repo);base=self.commit_all(repo,'base');target['event_id']='changed';(repo/'docs/Releases/metrics/prev.json').write_text(json.dumps(target,sort_keys=True)+'\n',encoding='utf-8');self.commit_all(repo,'modify bound record');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertIn('docs/Releases/metrics/s.json',data['reverse_reference_paths']);self.assertTrue(any('bound file sha256 mismatch' in x for x in data['violations']),data['violations'])

    def test_reverse_reference_closure_is_transitive(self):
        repo=self.make_repo();leaf=repo/'evidence.txt';leaf.write_text('before\n',encoding='utf-8');a=self.snapshot(repo);a['workstream_id']='W';next(m for m in a['metrics'] if m['metric_id']=='M02')['evidence_refs']=[{'type':'REPO_PATH','path':'evidence.txt','sha256':hashlib.sha256(leaf.read_bytes()).hexdigest()}];self.write_csv(repo,a);self.validate(repo,a,'docs/Releases/metrics/a.json')
        a_path=repo/'docs/Releases/metrics/a.json';b=self.snapshot(repo);b['workstream_id']='W';b['previous_record']={'path':'docs/Releases/metrics/a.json','sha256':hashlib.sha256(a_path.read_bytes()).hexdigest()};b['csv_projection_path']='docs/Releases/metrics/b.csv';self.write_csv(repo,b);self.validate(repo,b,'docs/Releases/metrics/b.json')
        self.init_git(repo);base=self.commit_all(repo,'base');leaf.write_text('after\n',encoding='utf-8');self.commit_all(repo,'modify leaf');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertIn('docs/Releases/metrics/a.json',data['reverse_reference_paths']);self.assertIn('docs/Releases/metrics/b.json',data['reverse_reference_paths'])

    def test_modified_unreferenced_file_does_not_expand_reverse_validation(self):
        repo=self.make_repo();rec=self.snapshot(repo);self.validate(repo,rec);other=repo/'notes.txt';other.write_text('before\n');self.init_git(repo);base=self.commit_all(repo,'base');other.write_text('after\n');self.commit_all(repo,'modify notes');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(0,rc);self.assertEqual([],data['reverse_reference_paths']);self.assertEqual(['notes.txt'],data['validation_paths'])

    def test_no_direct_float_conversion_outside_finite_number(self):
        source=MODULE_PATH.read_text(encoding='utf-8');tree=ast.parse(source);parents=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='float':
                parent_fn=None
                for candidate in ast.walk(tree):
                    if isinstance(candidate,(ast.FunctionDef,ast.AsyncFunctionDef)) and any(child is node for child in ast.walk(candidate)):
                        parent_fn=candidate.name;break
                parents.append(parent_fn)
        self.assertEqual(['finite_number'],parents)

    def test_unknown_or_na_evidence_refs_must_still_be_list(self):
        for metric_id in POLICY['metric_order']:
            for bad in [{},'bad',0,True,None]:
                with self.subTest(metric_id=metric_id,bad=repr(bad)):
                    repo=self.make_repo();rec=self.snapshot(repo);m=next(x for x in rec['metrics'] if x['metric_id']==metric_id);m.update(value=None,data_quality='UNKNOWN',reason='unknown',collection_method='GAP',evidence_refs=bad);self.write_csv(repo,rec)
                    report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('evidence_refs must be list' in x for x in report['violations']),report['violations'])

    def test_non_handoff_components_must_be_empty_list(self):
        for bad in [{},'bad',None,True,1,1.5]:
            with self.subTest(bad=repr(bad)):
                repo=self.make_repo();rec=self.snapshot(repo);rec['handoff_components']=bad
                report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('handoff_components must be list' in x for x in report['violations']),report['violations'])
        repo=self.make_repo();rec=self.snapshot(repo);rec['handoff_components']=[{'component_id':'unexpected'}]
        report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('must not contain handoff_components' in x for x in report['violations']),report['violations'])

    def test_csv_projection_path_must_be_nonempty_string(self):
        for bad in [[],{},None,True,1,1.5,'']:
            with self.subTest(bad=repr(bad)):
                repo=self.make_repo();rec=self.snapshot(repo);rec['csv_projection_path']=bad;p=repo/'docs/Releases/metrics/s.json';p.write_text(json.dumps(rec)+'\n')
                report=v.validate_files(repo,['docs/Releases/metrics/s.json'],POLICY);self.assertEqual('FAIL',report['status']);self.assertTrue(any('csv_projection_path must be non-empty string' in x for x in report['violations']),report['violations'])

    def test_prior_handoff_must_be_null_when_unavailable(self):
        for bad in [{},[],'bad',True,1,1.5]:
            with self.subTest(bad=repr(bad)):
                repo=self.make_repo();rec=self.snapshot(repo);rec['prior_handoff_available']=False;rec['prior_handoff']=bad
                report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('prior_handoff must be null when unavailable' in x for x in report['violations']),report['violations'])


    def test_malformed_interval_sort_keys_are_fail_closed(self):
        for field,bad in [('category',[]),('category',{}),('interval_id',[]),('interval_id',{})]:
            with self.subTest(field=field,bad=repr(bad)):
                repo=self.make_repo();rec=self.snapshot(repo);rec['timing_intervals'].append({'interval_id':'I2','category':'ACTIVE_ENGINEERING','start_utc':'2026-08-07T12:00:00Z','end_utc':'2026-08-07T12:01:00Z'});rec['timing_intervals'][0][field]=bad
                p=repo/'docs/Releases/metrics/s.json';p.write_text(json.dumps(rec)+'\n')
                report=v.validate_files(repo,['docs/Releases/metrics/s.json'],POLICY);self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])


    def test_modified_referenced_evidence_with_updated_snapshot_passes(self):
        repo=self.make_repo();evidence=repo/'evidence.txt';evidence.write_text('before\n',encoding='utf-8');rec=self.snapshot(repo);m=next(x for x in rec['metrics'] if x['metric_id']=='M02');m['evidence_refs']=[{'type':'REPO_PATH','path':'evidence.txt','sha256':hashlib.sha256(evidence.read_bytes()).hexdigest()}];self.write_csv(repo,rec);self.validate(repo,rec)
        self.init_git(repo);base=self.commit_all(repo,'base');evidence.write_text('after\n',encoding='utf-8');m['evidence_refs'][0]['sha256']=hashlib.sha256(evidence.read_bytes()).hexdigest();self.validate(repo,rec);self.commit_all(repo,'update evidence and snapshot');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(0,rc);self.assertEqual('PASS',data['status']);self.assertIn('docs/Releases/metrics/s.json',data['validation_paths'])

    def test_added_referenced_evidence_with_source_update_passes(self):
        repo=self.make_repo();rec=self.snapshot(repo);self.validate(repo,rec);self.init_git(repo);base=self.commit_all(repo,'base');evidence=repo/'new-evidence.txt';evidence.write_text('new\n',encoding='utf-8');m=next(x for x in rec['metrics'] if x['metric_id']=='M02');m['evidence_refs']=[{'type':'REPO_PATH','path':'new-evidence.txt','sha256':hashlib.sha256(evidence.read_bytes()).hexdigest()}];self.validate(repo,rec);self.commit_all(repo,'add evidence and update snapshot');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(0,rc);self.assertEqual('PASS',data['status']);self.assertIn('new-evidence.txt',data['direct_changed_paths'])

    def test_renamed_referenced_evidence_without_source_update_fails(self):
        repo=self.make_repo();evidence=repo/'evidence.txt';evidence.write_text('before\n',encoding='utf-8');rec=self.snapshot(repo);m=next(x for x in rec['metrics'] if x['metric_id']=='M02');m['evidence_refs']=[{'type':'REPO_PATH','path':'evidence.txt','sha256':hashlib.sha256(evidence.read_bytes()).hexdigest()}];self.validate(repo,rec);self.init_git(repo);base=self.commit_all(repo,'base');self.git(repo,'mv','evidence.txt','renamed-evidence.txt');self.commit_all(repo,'rename evidence only');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertIn('evidence.txt',data['deleted_paths']);self.assertIn('renamed-evidence.txt',data['direct_changed_paths']);self.assertIn('docs/Releases/metrics/s.json',data['reverse_reference_paths'])

    def test_renamed_referenced_evidence_with_source_update_passes(self):
        repo=self.make_repo();evidence=repo/'evidence.txt';evidence.write_text('before\n',encoding='utf-8');rec=self.snapshot(repo);m=next(x for x in rec['metrics'] if x['metric_id']=='M02');m['evidence_refs']=[{'type':'REPO_PATH','path':'evidence.txt','sha256':hashlib.sha256(evidence.read_bytes()).hexdigest()}];self.validate(repo,rec);self.init_git(repo);base=self.commit_all(repo,'base');self.git(repo,'mv','evidence.txt','renamed-evidence.txt');renamed=repo/'renamed-evidence.txt';m['evidence_refs'][0]={'type':'REPO_PATH','path':'renamed-evidence.txt','sha256':hashlib.sha256(renamed.read_bytes()).hexdigest()};self.validate(repo,rec);self.commit_all(repo,'rename evidence and update snapshot');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(0,rc);self.assertEqual('PASS',data['status']);self.assertIn('evidence.txt',data['deleted_paths']);self.assertIn('renamed-evidence.txt',data['direct_changed_paths'])


    def test_malformed_metric_rows_return_structured_fail(self):
        malformed=[[],0,1,True,False,None,3.14,'x']
        for index in [0,5,27]:
            for bad in malformed:
                with self.subTest(index=index,bad=repr(bad)):
                    repo=self.make_repo(); rec=self.snapshot(repo); rec['metrics'][index]=copy.deepcopy(bad)
                    report=self.validate(repo,rec)
                    self.assertEqual('FAIL',report['status'])
                    self.assertTrue(report['violations'])


    # CR5 comprehensive validator closure: repository discovery, schema cardinality,
    # parser/decoding boundaries, and fail-closed exception-surface coverage.
    def qualification_run_event(self):
        return {
            'record_type':POLICY['record_types']['event'],'schema_version':'1.0','workstream_id':'W',
            'event_id':'Q1','created_utc':'2026-08-07T12:00:00Z','event_type':'QUALIFICATION_RUN',
            'lifecycle_from':'DESIGN_QUALIFICATION','lifecycle_to':'DESIGN_QUALIFICATION',
            'classification':'NONE','mutation_boundary_crossed':False,'previous_record':None,
            'evidence_refs':[self.ext()],
            'test_run':{'run_id':'R1','test_layer':'UNIT','result':'PASS','release_authorizing':False,
                'test_id':'T1','requirement_id':'REQ1','production_function_path':'validator',
                'fixture_provenance':'independent','expected_result_source':'policy','actual_result':'PASS',
                'mutation_boundary':'NONE','cleanup_preserve_behavior':'NONE','evidence_artifact':'E'}
        }

    def test_qualification_run_requires_exactly_one_object(self):
        malformed=[None,[],[self.qualification_run_event()['test_run']],
            [self.qualification_run_event()['test_run'],self.qualification_run_event()['test_run']],
            'bad',0,1,True,False,3.14]
        for bad in malformed:
            with self.subTest(bad=repr(bad)):
                repo=self.make_repo();evt=self.qualification_run_event();evt['test_run']=bad
                p=repo/'docs/Releases/metrics/q.json';p.write_text(json.dumps(evt),encoding='utf-8')
                report=v.validate_files(repo,['docs/Releases/metrics/q.json'],POLICY)
                self.assertEqual('FAIL',report['status']);self.assertTrue(any('exactly one test_run object' in x for x in report['violations']),report['violations'])

    def test_qualification_run_single_object_passes(self):
        repo=self.make_repo();evt=self.qualification_run_event();p=repo/'docs/Releases/metrics/q.json';p.write_text(json.dumps(evt),encoding='utf-8')
        report=v.validate_files(repo,['docs/Releases/metrics/q.json'],POLICY);self.assertEqual('PASS',report['status'],report['violations'])

    def test_canonical_template_csv_change_revalidates_template(self):
        repo=self.make_repo();(repo/'docs/Templates').mkdir(parents=True,exist_ok=True)
        rec=self.snapshot(repo);rec['csv_projection_path']='docs/Templates/template.csv';self.write_csv(repo,rec)
        template=repo/'docs/Templates/template.json';template.write_text(json.dumps(rec,sort_keys=True)+'\n',encoding='utf-8')
        self.init_git(repo);base=self.commit_all(repo,'base')
        (repo/'docs/Templates/template.csv').write_text('bad\n',encoding='utf-8');self.commit_all(repo,'corrupt template csv')
        report_path=repo/'report.json';rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report_path)])
        data=json.loads(report_path.read_text());self.assertEqual(1,rc);self.assertEqual('FAIL',data['status'])
        self.assertIn('docs/Templates/template.json',data['reverse_reference_paths']);self.assertTrue(any('CSV header mismatch' in x for x in data['violations']),data['violations'])

    def test_repository_transition_record_outside_metrics_is_reverse_indexed(self):
        repo=self.make_repo();(repo/'governance').mkdir(parents=True,exist_ok=True)
        evidence=repo/'evidence.txt';evidence.write_text('before\n',encoding='utf-8')
        rec=self.snapshot(repo);rec['csv_projection_path']='governance/custom.csv';self.write_csv(repo,rec)
        next(m for m in rec['metrics'] if m['metric_id']=='M02')['evidence_refs']=[{'type':'REPO_PATH','path':'evidence.txt','sha256':hashlib.sha256(evidence.read_bytes()).hexdigest()}]
        self.write_csv(repo,rec);source=repo/'governance/custom-transition.json';source.write_text(json.dumps(rec,sort_keys=True)+'\n',encoding='utf-8')
        self.init_git(repo);base=self.commit_all(repo,'base');evidence.write_text('after\n',encoding='utf-8');self.commit_all(repo,'modify evidence')
        report_path=repo/'report.json';rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report_path)])
        data=json.loads(report_path.read_text());self.assertEqual(1,rc);self.assertIn('governance/custom-transition.json',data['reverse_reference_paths'])
        self.assertTrue(any('reference sha256 mismatch' in x for x in data['violations']),data['violations'])

    def test_unrelated_json_outside_transition_roots_is_not_reverse_indexed(self):
        repo=self.make_repo();(repo/'misc').mkdir(parents=True,exist_ok=True)
        (repo/'misc/data.json').write_text(json.dumps({'path':'evidence.txt','record_type':'UNRELATED'})+'\n',encoding='utf-8')
        evidence=repo/'evidence.txt';evidence.write_text('before\n',encoding='utf-8')
        self.init_git(repo);base=self.commit_all(repo,'base');evidence.write_text('after\n',encoding='utf-8');self.commit_all(repo,'modify evidence')
        report_path=repo/'report.json';rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report_path)])
        data=json.loads(report_path.read_text());self.assertEqual(0,rc);self.assertNotIn('misc/data.json',data['reverse_reference_paths'])

    def test_non_utf8_csv_returns_structured_fail(self):
        repo=self.make_repo();rec=self.snapshot(repo);(repo/rec['csv_projection_path']).write_bytes(b'\xff\xfe\x00bad')
        report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('CSV decode/parse failed' in x for x in report['violations']),report['violations'])

    def test_csv_parser_error_returns_structured_fail(self):
        repo=self.make_repo();rec=self.snapshot(repo);p=repo/rec['csv_projection_path']
        huge='x'*(csv.field_size_limit()+1);p.write_text('metric_id,name,unit,value,data_quality,collection_method,reason\n'+huge+',x,x,x,x,x,x\n',encoding='utf-8')
        report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('CSV decode/parse failed' in x for x in report['violations']),report['violations'])

    def test_non_utf8_json_returns_structured_fail(self):
        repo=self.make_repo();p=repo/'docs/Releases/metrics/bad.json';p.write_bytes(b'\xff\xfe')
        report=v.validate_files(repo,['docs/Releases/metrics/bad.json'],POLICY);self.assertEqual('FAIL',report['status']);self.assertTrue(any('JSON parse failed' in x for x in report['violations']),report['violations'])

    def test_non_utf8_governed_markdown_returns_structured_fail(self):
        repo=self.make_repo();p=repo/'docs/Releases/Test-Gate.md';p.write_bytes(b'\xff\xfe')
        report=v.validate_files(repo,['docs/Releases/Test-Gate.md'],POLICY);self.assertEqual('FAIL',report['status']);self.assertTrue(any('not UTF-8' in x for x in report['violations']),report['violations'])

    def test_binary_repo_path_evidence_with_digest_is_allowed(self):
        repo=self.make_repo();rec=self.snapshot(repo);p=repo/'evidence.bin';p.write_bytes(bytes(range(256)))
        next(m for m in rec['metrics'] if m['metric_id']=='M02')['evidence_refs']=[{'type':'REPO_PATH','path':'evidence.bin','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}]
        self.write_csv(repo,rec);report=self.validate(repo,rec);self.assertEqual('PASS',report['status'],report['violations'])

    def test_event_specific_single_object_fields_fail_closed_matrix(self):
        bad_values=[None,[],[{}],'bad',0,1,True,False,3.14]
        deviation=self.qualification_run_event();deviation.update(event_type='DEVIATION',classification='REVIEW_TEST_DEFECT');deviation.pop('test_run',None)
        deviation['deviation']={'deviation_id':'D1','timestamp_utc':'2026-08-07T12:00:00Z','category':'REVIEW','planned_condition':'x','observed_condition':'y','impact':'z','mutation_status':'NONE','evidence_reference':'E','owner_disposition':'CORRECT','permanent_control_decision':'ADD_TEST'}
        blocker=self.qualification_run_event();blocker.update(event_type='EXTERNAL_BLOCKER');blocker.pop('test_run',None);blocker['external_incident']={'candidate_revision_action':'PRESERVE_EXACT_CANDIDATE','code_revision_created':False,'exposed_internal_defect':False}
        for field,template in [('deviation',deviation),('external_incident',blocker),('test_run',self.qualification_run_event())]:
            for bad in bad_values:
                with self.subTest(field=field,bad=repr(bad)):
                    repo=self.make_repo();evt=copy.deepcopy(template);evt[field]=bad;p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt),encoding='utf-8')
                    report=v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY);self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])

    def test_snapshot_container_field_matrix_never_raises(self):
        bad_values=[None,{},'bad',0,1,True,False,3.14]
        for field in ['metrics','timing_intervals','test_runs','defects','handoff_components']:
            for bad in bad_values:
                with self.subTest(field=field,bad=repr(bad)):
                    repo=self.make_repo();rec=self.snapshot(repo);rec[field]=bad
                    try: report=self.validate(repo,rec)
                    except Exception as exc: self.fail(f'{field}={bad!r} raised {type(exc).__name__}: {exc}')
                    self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])

    def test_event_container_and_scalar_field_matrix_never_raises(self):
        base=self.qualification_run_event()
        cases={
            'event_type':[[],{},0,True,None], 'classification':[[],{},0,True,None],
            'lifecycle_from':[[],{},0,True,None], 'lifecycle_to':[[],{},0,True,None],
            'evidence_refs':[{},'bad',0,True,None], 'previous_record':[[],'bad',0,True],
            'workstream_id':[[],{},0,True,None], 'event_id':[[],{},0,True,None],
            'created_utc':[[],{},0,True,None], 'mutation_boundary_crossed':[[],{},0,'bad',None],
        }
        for field,values in cases.items():
            for bad in values:
                with self.subTest(field=field,bad=repr(bad)):
                    repo=self.make_repo();evt=copy.deepcopy(base);evt[field]=bad;p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt),encoding='utf-8')
                    try: report=v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY)
                    except Exception as exc: self.fail(f'{field}={bad!r} raised {type(exc).__name__}: {exc}')
                    self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])

    def test_snapshot_scalar_field_matrix_never_raises(self):
        cases={
            'snapshot_type':[[],{},0,True,None], 'lifecycle_state':[[],{},0,True,None],
            'created_utc':[[],{},0,True,None], 'baseline_commit':[[],{},0,True,None],
            'workstream_id':[[],{},0,True,None], 'collection_method':[[],{},0,True,None],
            'previous_record':[[],'bad',0,True], 'prior_handoff_available':[[],{},0,'bad',None],
            'csv_projection_path':[[],{},0,True,None],
        }
        for field,values in cases.items():
            for bad in values:
                with self.subTest(field=field,bad=repr(bad)):
                    repo=self.make_repo();rec=self.snapshot(repo);rec[field]=bad
                    try: report=self.validate(repo,rec)
                    except Exception as exc: self.fail(f'{field}={bad!r} raised {type(exc).__name__}: {exc}')
                    self.assertEqual('FAIL',report['status']);self.assertTrue(report['violations'])

    def test_repository_templates_are_discovered_as_transition_records(self):
        index=v.build_reverse_reference_index(ROOT,POLICY)
        self.assertIn('docs/Templates/SMT-Transition-Metrics-Baseline-Projection.csv',index)
        self.assertIn('docs/Templates/SMT-Transition-Metrics-Baseline-Template.json',index['docs/Templates/SMT-Transition-Metrics-Baseline-Projection.csv'])

    def test_reverse_index_ignores_malformed_unrelated_json_without_exception(self):
        repo=self.make_repo();p=repo/'config/bad-unrelated.json';p.write_bytes(b'\xff\xfe')
        try: index=v.build_reverse_reference_index(repo,POLICY)
        except Exception as exc: self.fail(f'reverse index raised {type(exc).__name__}: {exc}')
        self.assertIsInstance(index,dict)


    def test_modified_non_utf8_csv_reverse_revalidation_is_structured_fail(self):
        repo=self.make_repo();rec=self.snapshot(repo);self.validate(repo,rec);self.init_git(repo);base=self.commit_all(repo,'base')
        (repo/rec['csv_projection_path']).write_bytes(b'\xff\xfe\x00bad');self.commit_all(repo,'corrupt csv encoding');report_path=repo/'report.json'
        try: rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report_path)])
        except Exception as exc: self.fail(f'reverse CSV validation raised {type(exc).__name__}: {exc}')
        data=json.loads(report_path.read_text());self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertIn('docs/Releases/metrics/s.json',data['reverse_reference_paths']);self.assertTrue(any('CSV decode/parse failed' in x for x in data['violations']),data['violations'])

    def test_modified_oversized_csv_reverse_revalidation_is_structured_fail(self):
        repo=self.make_repo();rec=self.snapshot(repo);self.validate(repo,rec);self.init_git(repo);base=self.commit_all(repo,'base');p=repo/rec['csv_projection_path']
        huge='x'*(csv.field_size_limit()+1);p.write_text('metric_id,name,unit,value,data_quality,collection_method,reason\n'+huge+',x,x,x,x,x,x\n',encoding='utf-8');self.commit_all(repo,'oversize csv field');report_path=repo/'report.json'
        try: rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report_path)])
        except Exception as exc: self.fail(f'reverse CSV validation raised {type(exc).__name__}: {exc}')
        data=json.loads(report_path.read_text());self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertIn('docs/Releases/metrics/s.json',data['reverse_reference_paths']);self.assertTrue(any('CSV decode/parse failed' in x for x in data['violations']),data['violations'])


    def test_canonical_transition_templates_reject_unknown_or_missing_record_type(self):
        cases=[
            ('docs/Templates/SMT-Transition-Metrics-Baseline-Template.json',{'record_type':'TYPO'}),
            ('docs/Templates/SMT-Transition-Metrics-Baseline-Template.json',{'x':1}),
            ('docs/Templates/SMT-Transition-Event-Metrics-Template.json',{'record_type':'TYPO'}),
            ('docs/Templates/SMT-Transition-Event-Metrics-Template.json',{'x':1}),
        ]
        for rel,obj in cases:
            with self.subTest(rel=rel,obj=obj):
                repo=self.make_repo();p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj)+'\n',encoding='utf-8')
                report=v.validate_files(repo,[rel],POLICY);self.assertEqual('FAIL',report['status']);self.assertTrue(any('unrecognized transition record_type' in x for x in report['violations']),report['violations'])

    def test_metrics_directory_unknown_record_type_error_remains_fail_closed(self):
        repo=self.make_repo();p=repo/'docs/Releases/metrics/unknown.json';p.write_text('{"record_type":"TYPO"}\n',encoding='utf-8')
        report=v.validate_files(repo,['docs/Releases/metrics/unknown.json'],POLICY);self.assertEqual('FAIL',report['status']);self.assertTrue(any('unrecognized transition record_type' in x for x in report['violations']),report['violations'])


    def test_future_named_canonical_transition_template_requires_transition_record_type(self):
        repo=self.make_repo();rel='docs/Templates/SMT-Transition-Future-Template.json';p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{"record_type":"TYPO"}\n',encoding='utf-8')
        report=v.validate_files(repo,[rel],POLICY);self.assertEqual('FAIL',report['status']);self.assertTrue(any('unrecognized transition record_type' in x for x in report['violations']),report['violations'])

    def test_deleted_transition_record_outside_metrics_is_governed(self):
        repo=self.make_repo();(repo/'governance').mkdir(parents=True,exist_ok=True);evt=self.qualification_run_event();evt['event_type']='LIFECYCLE';evt.pop('test_run',None);evt['lifecycle_from']='PLANNING_READ_ONLY';evt['lifecycle_to']='DESIGN_QUALIFICATION'
        p=repo/'governance/custom-transition.json';p.write_text(json.dumps(evt)+'\n',encoding='utf-8');self.init_git(repo);base=self.commit_all(repo,'base');p.unlink();self.commit_all(repo,'delete transition record');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertIn('governance/custom-transition.json',data['deleted_paths']);self.assertTrue(any('deletion of governed transition artifact is prohibited' in x for x in data['violations']),data['violations'])

    def test_deleted_unrelated_json_outside_metrics_remains_allowed(self):
        repo=self.make_repo();(repo/'governance').mkdir(parents=True,exist_ok=True);p=repo/'governance/unrelated.json';p.write_text('{"record_type":"OTHER","x":1}\n',encoding='utf-8');self.init_git(repo);base=self.commit_all(repo,'base');p.unlink();self.commit_all(repo,'delete unrelated json');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(0,rc);self.assertEqual('PASS',data['status'])

    def off_directory_transition_event(self):
        evt=self.qualification_run_event();evt['event_type']='LIFECYCLE';evt.pop('test_run',None);evt['lifecycle_from']='PLANNING_READ_ONLY';evt['lifecycle_to']='DESIGN_QUALIFICATION'
        return evt

    def run_base_ref_case(self, base_obj, current_bytes, rel='governance/custom-transition.json'):
        repo=self.make_repo();p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(base_obj)+'\n',encoding='utf-8');self.init_git(repo);base=self.commit_all(repo,'base')
        if current_bytes is None:
            p.unlink()
        else:
            p.write_bytes(current_bytes)
        self.commit_all(repo,'change');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)])
        return rc,json.loads(report.read_text()),repo,base

    def test_base_governed_modified_off_directory_record_cannot_drop_record_type(self):
        evt=self.off_directory_transition_event();current=copy.deepcopy(evt);current.pop('record_type')
        rc,data,_,_=self.run_base_ref_case(evt,(json.dumps(current)+'\n').encode())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertIn('governance/custom-transition.json',data['base_governed_changed_paths']);self.assertTrue(any('unrecognized transition record_type' in x for x in data['violations']),data['violations'])

    def test_base_governed_modified_off_directory_record_cannot_mistype_record_type(self):
        evt=self.off_directory_transition_event();current=copy.deepcopy(evt);current['record_type']='TYPO'
        rc,data,_,_=self.run_base_ref_case(evt,(json.dumps(current)+'\n').encode())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertTrue(any('unrecognized transition record_type' in x for x in data['violations']),data['violations'])

    def test_base_governed_modified_off_directory_record_cannot_become_unrelated_object(self):
        evt=self.off_directory_transition_event();rc,data,_,_=self.run_base_ref_case(evt,b'{"x":1}\n')
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertTrue(any('unrecognized transition record_type' in x for x in data['violations']),data['violations'])

    def test_base_governed_modified_off_directory_record_non_object_fails(self):
        evt=self.off_directory_transition_event()
        for raw in [b'[]\n',b'null\n',b'1\n',b'"x"\n']:
            with self.subTest(raw=raw):
                rc,data,_,_=self.run_base_ref_case(evt,raw)
                self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertTrue(any('unrecognized transition record_type' in x for x in data['violations']),data['violations'])

    def test_base_governed_modified_off_directory_record_malformed_or_non_utf8_fails_closed(self):
        evt=self.off_directory_transition_event()
        for raw in [b'{bad\n',b'\xff\xfe\x00bad']:
            with self.subTest(raw=raw):
                try: rc,data,_,_=self.run_base_ref_case(evt,raw)
                except Exception as exc: self.fail(f'base-governed malformed record raised {type(exc).__name__}: {exc}')
                self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertTrue(any('JSON parse failed' in x for x in data['violations']),data['violations'])

    def test_base_governed_modified_off_directory_valid_transition_remains_validated(self):
        evt=self.off_directory_transition_event();current=copy.deepcopy(evt);current['event_id']='E2'
        rc,data,_,_=self.run_base_ref_case(evt,(json.dumps(current)+'\n').encode())
        self.assertEqual(0,rc);self.assertEqual('PASS',data['status']);self.assertEqual(['governance/custom-transition.json'],data['base_governed_changed_paths'])

    def test_new_off_directory_unrelated_json_remains_allowed(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');p=repo/'governance/new.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{"x":1}\n',encoding='utf-8');self.commit_all(repo,'add unrelated');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(0,rc);self.assertEqual('PASS',data['status']);self.assertEqual([],data['base_governed_changed_paths'])

    def test_new_off_directory_transition_json_is_validated(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');p=repo/'governance/new-transition.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(self.off_directory_transition_event())+'\n',encoding='utf-8');self.commit_all(repo,'add transition');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(0,rc);self.assertEqual('PASS',data['status']);self.assertEqual([],data['base_governed_changed_paths'])

    def test_unchanged_off_directory_transition_record_remains_out_of_scope(self):
        repo=self.make_repo();p=repo/'governance/custom-transition.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(self.off_directory_transition_event())+'\n',encoding='utf-8');self.init_git(repo);base=self.commit_all(repo,'base');other=repo/'notes.txt';other.write_text('changed\n',encoding='utf-8');self.commit_all(repo,'other change');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(0,rc);self.assertEqual('PASS',data['status']);self.assertNotIn('governance/custom-transition.json',data['validation_paths']);self.assertEqual([],data['base_governed_changed_paths'])

    def test_base_governed_rename_move_remains_prohibited_via_deleted_identity(self):
        repo=self.make_repo();old=repo/'governance/custom-transition.json';old.parent.mkdir(parents=True,exist_ok=True);old.write_text(json.dumps(self.off_directory_transition_event())+'\n',encoding='utf-8');self.init_git(repo);base=self.commit_all(repo,'base');new=repo/'moved/custom-transition.json';new.parent.mkdir(parents=True,exist_ok=True);old.rename(new);self.commit_all(repo,'move transition');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertIn('governance/custom-transition.json',data['deleted_paths']);self.assertIn('governance/custom-transition.json',data['base_governed_changed_paths']);self.assertTrue(any('deletion of governed transition artifact is prohibited' in x for x in data['violations']),data['violations'])

    def test_canonical_modified_record_type_remains_fail_closed_under_base_identity(self):
        evt=self.off_directory_transition_event();rel='docs/Templates/SMT-Transition-Future-Template.json';current=copy.deepcopy(evt);current.pop('record_type')
        rc,data,_,_=self.run_base_ref_case(evt,(json.dumps(current)+'\n').encode(),rel)
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertIn(rel,data['base_governed_changed_paths']);self.assertTrue(any('unrecognized transition record_type' in x for x in data['violations']),data['violations'])

    def test_unrelated_base_json_can_become_valid_transition_record(self):
        base_obj={'x':1};current=self.off_directory_transition_event();rc,data,_,_=self.run_base_ref_case(base_obj,(json.dumps(current)+'\n').encode())
        self.assertEqual(0,rc);self.assertEqual('PASS',data['status']);self.assertEqual([],data['base_governed_changed_paths'])


    def test_baseline_snapshot_recovery_identity_is_required(self):
        for bad in [None,'',[],{},0,True]:
            with self.subTest(bad=repr(bad)):
                repo=self.make_repo();rec=self.snapshot(repo);rec['baseline_snapshot']=bad
                report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('baseline_snapshot required' in x for x in report['violations']),report['violations'])


    # CR6-R2 Policy-Version Continuity: historical identity must use merge-base
    # policy while current validation continues to use current policy.
    def write_policy(self, repo, policy):
        path=repo/'config/transition-metrics-policy.json';path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(policy,sort_keys=True)+'\n',encoding='utf-8')
        return path

    def renamed_record_type_policy(self):
        policy=copy.deepcopy(POLICY)
        policy['record_types']={'event':'SMT_TRANSITION_EVENT_V2','snapshot':'SMT_TRANSITION_METRICS_SNAPSHOT_V2'}
        return policy

    def run_policy_version_case(self, base_obj, current_obj, current_policy=None, rel='governance/custom-transition.json'):
        repo=self.make_repo();p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(base_obj)+'\n',encoding='utf-8');self.init_git(repo);base=self.commit_all(repo,'base')
        if current_policy is not None:self.write_policy(repo,current_policy)
        if current_obj is None:p.unlink()
        elif isinstance(current_obj,bytes):p.write_bytes(current_obj)
        else:p.write_text(json.dumps(current_obj)+'\n',encoding='utf-8')
        self.commit_all(repo,'change');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)])
        return rc,json.loads(report.read_text()),repo,base

    def test_policy_version_p1_record_type_rename_is_rejected_before_degovernance(self):
        evt=self.off_directory_transition_event();policy=self.renamed_record_type_policy()
        rc,data,_,_=self.run_policy_version_case(evt,{'x':1},policy)
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertEqual('FAIL',data['base_policy_status'])
        self.assertTrue(any('record_types identities are immutable' in x for x in data['violations']),data['violations'])

    def test_policy_version_record_type_migration_requires_new_governed_design_not_in_place_identity_change(self):
        evt=self.off_directory_transition_event();policy=self.renamed_record_type_policy();current=copy.deepcopy(evt);current['record_type']=policy['record_types']['event'];current['event_id']='E2'
        rc,data,_,_=self.run_policy_version_case(evt,current,policy)
        self.assertEqual(1,rc);self.assertTrue(any('record_types identities are immutable' in x for x in data['violations']),data['violations'])

    def test_policy_version_record_type_change_cannot_disable_reverse_reference_governance(self):
        repo=self.make_repo();evidence=repo/'evidence.txt';evidence.write_text('old\n',encoding='utf-8')
        evt=self.off_directory_transition_event();evt['evidence_refs']=[{'type':'REPO_PATH','path':'evidence.txt','sha256':hashlib.sha256(evidence.read_bytes()).hexdigest()}]
        p=repo/'governance/custom-transition.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(evt)+'\n',encoding='utf-8')
        self.init_git(repo);base=self.commit_all(repo,'base');self.write_policy(repo,self.renamed_record_type_policy());evidence.write_text('new\n',encoding='utf-8');self.commit_all(repo,'policy and evidence change');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['base_policy_status']);self.assertTrue(any('record_types identities are immutable' in x for x in data['violations']),data['violations'])

    def test_policy_version_assignment_identity_is_immutable(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');policy=copy.deepcopy(POLICY);policy['transition_metrics_assignment']='TRANSITION_METRICS_RECORD_V2';self.write_policy(repo,policy);self.commit_all(repo,'change assignment identity');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('transition_metrics_assignment identity is immutable' in x for x in data['violations']),data['violations'])

    def test_policy_version_metrics_filename_classifier_cannot_be_removed(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');policy=copy.deepcopy(POLICY);policy['metrics_link_filename_keywords']=['handoff','closeout'];self.write_policy(repo,policy);self.commit_all(repo,'remove gate classifier');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('metrics_link_filename_keywords may not remove' in x for x in data['violations']),data['violations'])

    def test_policy_version_change_filename_classifier_cannot_be_removed(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');policy=copy.deepcopy(POLICY);policy['change_record_filename_keywords']=['plan','authorization'];self.write_policy(repo,policy);self.commit_all(repo,'remove change classifier');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('change_record_filename_keywords may not remove' in x for x in data['violations']),data['violations'])

    def test_policy_version_governed_markdown_root_cannot_be_removed(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');policy=copy.deepcopy(POLICY);policy['governed_markdown_roots']=['skills/','docs/Releases/','docs/Standards/'];self.write_policy(repo,policy);self.commit_all(repo,'remove markdown root');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('governed_markdown_roots may not remove' in x for x in data['violations']),data['violations'])

    def test_policy_version_governance_classifier_additions_are_allowed(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');policy=copy.deepcopy(POLICY);policy['governed_markdown_roots'].append('docs/Future/');policy['metrics_link_filename_keywords'].append('checkpoint');policy['change_record_filename_keywords'].append('waiver');self.write_policy(repo,policy);self.commit_all(repo,'add classifiers');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(0,rc);self.assertEqual('PASS',data['status'],data['violations']);self.assertEqual('PRESENT_VALID',data['base_policy_status'])

    def test_policy_version_baseline_adoption_anchor_is_immutable(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');policy=copy.deepcopy(POLICY);policy['baseline_commit_for_adoption']='a'*40;self.write_policy(repo,policy);self.commit_all(repo,'change baseline anchor');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('baseline_commit_for_adoption is immutable' in x for x in data['violations']),data['violations'])

    def test_policy_version_unrelated_base_json_remains_unrelated_with_compatible_policy(self):
        base={'record_type':'OTHER','x':1};current={'record_type':'OTHER','x':2};policy=copy.deepcopy(POLICY);policy['governed_markdown_roots'].append('docs/Future/')
        rc,data,_,_=self.run_policy_version_case(base,current,policy)
        self.assertEqual(0,rc);self.assertEqual('PASS',data['status'],data['violations']);self.assertEqual([],data['base_governed_changed_paths'])

    def test_policy_bootstrap_absent_base_policy_requires_exact_adoption_baseline(self):
        repo=self.make_repo();(repo/'config/transition-metrics-policy.json').unlink();(repo/'pre-adoption.txt').write_text('baseline\n',encoding='utf-8');self.init_git(repo);base=self.commit_all(repo,'pre-adoption base');policy=copy.deepcopy(POLICY);policy['baseline_commit_for_adoption']=base;self.write_policy(repo,policy);self.commit_all(repo,'adopt policy');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(0,rc);self.assertEqual('BOOTSTRAP_ABSENT_AUTHORIZED',data['base_policy_status']);self.assertEqual('PASS',data['status'],data['violations'])

    def test_policy_bootstrap_absent_base_policy_mismatched_baseline_fails_closed(self):
        repo=self.make_repo();(repo/'config/transition-metrics-policy.json').unlink();(repo/'pre-adoption.txt').write_text('baseline\n',encoding='utf-8');self.init_git(repo);base=self.commit_all(repo,'pre-adoption base');policy=copy.deepcopy(POLICY);policy['baseline_commit_for_adoption']='a'*40;self.write_policy(repo,policy);self.commit_all(repo,'bad adoption policy');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertEqual('FAIL',data['base_policy_status']);self.assertTrue(any('base-policy/governance classification failed' in x for x in data['violations']),data['violations'])

    def test_policy_malformed_base_json_fails_closed_structured(self):
        repo=self.make_repo();path=repo/'config/transition-metrics-policy.json';path.write_text('{bad\n',encoding='utf-8');self.init_git(repo);base=self.commit_all(repo,'malformed base policy');self.write_policy(repo,POLICY);self.commit_all(repo,'repair policy');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertEqual('FAIL',data['base_policy_status']);self.assertTrue(any('merge-base policy parse failed' in x for x in data['violations']),data['violations'])

    def test_policy_malformed_base_shape_fails_closed_structured(self):
        repo=self.make_repo();bad=copy.deepcopy(POLICY);bad['record_types']=['bad'];self.write_policy(repo,bad);self.init_git(repo);base=self.commit_all(repo,'bad base shape');self.write_policy(repo,POLICY);self.commit_all(repo,'repair policy');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertTrue(any('merge-base policy: record_types must be an object' in x for x in data['violations']),data['violations'])

    def test_policy_malformed_current_json_fails_closed_structured(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');path=repo/'config/transition-metrics-policy.json';path.write_text('{bad\n',encoding='utf-8');self.commit_all(repo,'bad current policy');report=repo/'report.json'
        try:rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)])
        except Exception as exc:self.fail(f'malformed current policy raised {type(exc).__name__}: {exc}')
        data=json.loads(report.read_text());self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertTrue(any('current policy invalid' in x for x in data['violations']),data['violations'])

    def test_policy_malformed_current_shape_fails_closed_structured(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');bad=copy.deepcopy(POLICY);bad['record_types']={'event':'SAME','snapshot':'SAME'};self.write_policy(repo,bad);self.commit_all(repo,'bad current policy shape');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertTrue(any('event and snapshot record types must be distinct' in x for x in data['violations']),data['violations'])

    def test_policy_id_change_fails_closed_against_base_policy(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');policy=copy.deepcopy(POLICY);policy['policy_id']='OTHER_POLICY';self.write_policy(repo,policy);self.commit_all(repo,'change policy identity');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertTrue(any('policy_id does not match' in x for x in data['violations']),data['violations'])

    def test_policy_shape_rejects_extra_record_type_identity(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');bad=copy.deepcopy(POLICY);bad['record_types']['legacy']='LEGACY';self.write_policy(repo,bad);self.commit_all(repo,'bad policy');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('record_types must contain exactly event and snapshot' in x for x in data['violations']),data['violations'])

    def test_policy_shape_rejects_non_boolean_overlap_control(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');bad=copy.deepcopy(POLICY);bad['allow_overlapping_timing_intervals']='false';self.write_policy(repo,bad);self.commit_all(repo,'bad policy');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('allow_overlapping_timing_intervals must be boolean' in x for x in data['violations']),data['violations'])

    def test_policy_shape_rejects_duplicate_classifier_values(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');bad=copy.deepcopy(POLICY);bad['metrics_link_filename_keywords'].append(bad['metrics_link_filename_keywords'][0]);self.write_policy(repo,bad);self.commit_all(repo,'bad policy');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('metrics_link_filename_keywords must be a non-empty unique-string list' in x for x in data['violations']),data['violations'])

    def test_policy_shape_rejects_unsafe_markdown_root(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');bad=copy.deepcopy(POLICY);bad['governed_markdown_roots'].append('../escape/');self.write_policy(repo,bad);self.commit_all(repo,'bad policy');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('unsafe/non-directory root' in x for x in data['violations']),data['violations'])

    def test_policy_shape_rejects_invalid_assignment_key(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');bad=copy.deepcopy(POLICY);bad['transition_metrics_assignment']='bad-key';self.write_policy(repo,bad);self.commit_all(repo,'bad policy');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('uppercase assignment key' in x for x in data['violations']),data['violations'])

    def test_policy_shape_rejects_metrics_topology_mismatch(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');bad=copy.deepcopy(POLICY);bad['metrics'].pop('M28');self.write_policy(repo,bad);self.commit_all(repo,'bad policy');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('metrics keys must exactly match metric_order' in x for x in data['violations']),data['violations'])

    def test_policy_shape_rejects_unsupported_metric_value_type(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');bad=copy.deepcopy(POLICY);bad['metrics']['M01']['value_type']='FLOAT';self.write_policy(repo,bad);self.commit_all(repo,'bad policy');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('unsupported value_type' in x for x in data['violations']),data['violations'])

    def test_policy_shape_rejects_allowed_transition_unknown_state(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');bad=copy.deepcopy(POLICY);bad['allowed_transitions']['PLANNING_READ_ONLY']=['NOT_A_STATE'];self.write_policy(repo,bad);self.commit_all(repo,'bad policy');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('contains unknown lifecycle state' in x for x in data['violations']),data['violations'])

    def test_policy_shape_rejects_supported_state_vocabulary_drift(self):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');bad=copy.deepcopy(POLICY);bad['data_quality_states']=['MEASURED'];self.write_policy(repo,bad);self.commit_all(repo,'bad policy');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertTrue(any('data_quality_states must match supported validator states' in x for x in data['violations']),data['violations'])


    # Final Assurance Recovery: complete Git-state and full semantic-policy compatibility.
    def test_final_recovery_type_change_regular_to_symlink_is_discovered_and_fails(self):
        repo=self.make_repo();p=repo/'governance/custom-transition.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(self.off_directory_transition_event())+'\n',encoding='utf-8')
        self.init_git(repo);base=self.commit_all(repo,'base');p.unlink();p.symlink_to('missing-target');self.commit_all(repo,'type change');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertIn('governance/custom-transition.json',data['direct_changed_paths'])

    def test_final_recovery_type_change_symlink_to_regular_is_discovered(self):
        repo=self.make_repo();p=repo/'unrelated';p.symlink_to('target');self.init_git(repo);base=self.commit_all(repo,'base');p.unlink();p.write_text('regular\n',encoding='utf-8');self.commit_all(repo,'type change');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);data=json.loads(report.read_text())
        self.assertEqual(0,rc);self.assertIn('unrelated',data['direct_changed_paths'])

    def run_policy_mutation(self, mutate):
        repo=self.make_repo();self.init_git(repo);base=self.commit_all(repo,'base');policy=copy.deepcopy(POLICY);mutate(policy);self.write_policy(repo,policy);self.commit_all(repo,'policy change');report=repo/'report.json'
        rc=v.main(['--repo-root',str(repo),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(report)]);return rc,json.loads(report.read_text())

    def test_final_recovery_required_handoff_component_removal_fails(self):
        rc,d=self.run_policy_mutation(lambda p:p['required_handoff_components'].pop());self.assertEqual(1,rc);self.assertTrue(any('required_handoff_components' in x for x in d['violations']),d)

    def test_final_recovery_required_change_record_field_removal_fails(self):
        rc,d=self.run_policy_mutation(lambda p:p['required_change_record_fields'].pop());self.assertEqual(1,rc);self.assertTrue(any('required_change_record_fields may not remove' in x for x in d['violations']),d)

    def test_final_recovery_lifecycle_graph_expansion_fails(self):
        def mut(p):p['allowed_transitions']['PLANNING_READ_ONLY'].append('CLOSED_AND_FROZEN')
        rc,d=self.run_policy_mutation(mut);self.assertEqual(1,rc);self.assertTrue(any('allowed_transitions is immutable' in x for x in d['violations']),d)

    def test_final_recovery_overlap_control_weakening_fails(self):
        rc,d=self.run_policy_mutation(lambda p:p.__setitem__('allow_overlapping_timing_intervals',True));self.assertEqual(1,rc);self.assertTrue(any('allow_overlapping_timing_intervals is immutable' in x for x in d['violations']),d)

    def test_final_recovery_metric_semantic_redefinition_fails(self):
        def mut(p):p['metrics']['M01']['definition']='weakened'
        rc,d=self.run_policy_mutation(mut);self.assertEqual(1,rc);self.assertTrue(any('metrics is immutable' in x for x in d['violations']),d)

    def test_final_recovery_m27_denominator_shrink_fails(self):
        rc,d=self.run_policy_mutation(lambda p:p['m27_denominator_metric_ids'].pop());self.assertEqual(1,rc);self.assertTrue(any('m27_denominator_metric_ids is immutable' in x for x in d['violations']),d)

    def test_final_recovery_timing_semantic_change_fails(self):
        rc,d=self.run_policy_mutation(lambda p:p['m22_active_categories'].remove('REWORK'));self.assertEqual(1,rc);self.assertTrue(any('m22_active_categories is immutable' in x for x in d['violations']),d)

    def test_final_recovery_schema_version_in_place_change_fails(self):
        rc,d=self.run_policy_mutation(lambda p:p.__setitem__('schema_version','2.0'));self.assertEqual(1,rc);self.assertTrue(any('schema_version is immutable' in x for x in d['violations']),d)

    def test_final_recovery_effective_date_rollback_fails(self):
        rc,d=self.run_policy_mutation(lambda p:p.__setitem__('effective_date','2026-08-06'));self.assertEqual(1,rc);self.assertTrue(any('effective_date may not move backward' in x for x in d['violations']),d)

    def test_final_recovery_stricter_required_change_record_addition_allowed(self):
        rc,d=self.run_policy_mutation(lambda p:p['required_change_record_fields'].append('FINAL_ASSURANCE_ORACLE'));self.assertEqual(0,rc);self.assertEqual('PASS',d['status'],d['violations'])

    def test_final_recovery_stricter_handoff_component_append_allowed(self):
        rc,d=self.run_policy_mutation(lambda p:p['required_handoff_components'].append('FINAL_ASSURANCE_ORACLE'));self.assertEqual(0,rc);self.assertEqual('PASS',d['status'],d['violations'])

    def test_final_recovery_policy_unexpected_field_fails(self):
        rc,d=self.run_policy_mutation(lambda p:p.__setitem__('candidate_override',True));self.assertEqual(1,rc);self.assertTrue(any('unexpected top-level fields' in x for x in d['violations']),d)

    def test_final_recovery_snapshot_unexpected_field_fails(self):
        repo=self.make_repo();rec=self.snapshot(repo);rec['candidate_override']=True;self.write_csv(repo,rec);report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertTrue(any('unexpected fields' in x for x in report['violations']),report['violations'])

    def test_final_recovery_event_unexpected_field_fails(self):
        repo=self.make_repo();evt=self.qualification_run_event();evt['candidate_override']=True;p=repo/'docs/Releases/metrics/e.json';p.write_text(json.dumps(evt));report=v.validate_files(repo,['docs/Releases/metrics/e.json'],POLICY);self.assertEqual('FAIL',report['status']);self.assertTrue(any('unexpected fields' in x for x in report['violations']),report['violations'])

    def test_final_recovery_nested_unexpected_fields_fail(self):
        repo=self.make_repo();rec=self.snapshot(repo);rec['metrics'][0]['candidate_override']=True;rec['test_runs'][0]['candidate_override']=True;rec['defects']=[{'defect_id':'D','classification':'IMPLEMENTATION_DEFECT','repeated':False,'prior_lesson_or_control_ref':'','candidate_override':True}];self.write_csv(repo,rec);report=self.validate(repo,rec);self.assertEqual('FAIL',report['status']);self.assertGreaterEqual(sum('unexpected fields' in x for x in report['violations']),3,report['violations'])

if __name__=='__main__': unittest.main()
