from __future__ import annotations
import copy,importlib.util,json,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'scripts'/'validate_mandatory_assurance_invariants.py';S=importlib.util.spec_from_file_location('m',P);assert S and S.loader
m=importlib.util.module_from_spec(S);S.loader.exec_module(m);POLICY=json.loads((ROOT/'config/mandatory-assurance-invariant-policy.json').read_text())
def block(policy=POLICY,status='NOT_GRANTED'):
 vals=dict(policy['required_block']);vals['EXCEPTION_STATUS']=status;return '```text\n'+'\n'.join(f'{k}={vals[k]}' for k in policy['required_block_order'])+'\n```\n'
class MandatoryTests(unittest.TestCase):
 def repo(self):
  r=Path(tempfile.mkdtemp());(r/'config').mkdir();(r/'docs/Releases').mkdir(parents=True);(r/'docs/Exceptions').mkdir(parents=True);(r/'config/mandatory-assurance-invariant-policy.json').write_text(json.dumps(POLICY,sort_keys=True));return r
 def init(self,r):
  subprocess.run(['git','init','-q'],cwd=r,check=True);subprocess.run(['git','config','user.name','T'],cwd=r,check=True);subprocess.run(['git','config','user.email','t@example.invalid'],cwd=r,check=True)
 def commit(self,r,msg):subprocess.run(['git','add','-A'],cwd=r,check=True);subprocess.run(['git','commit','-qm',msg],cwd=r,check=True);return subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip()
 def validate(self,r,*paths):return m.validate_files(r,list(paths),POLICY)
 def test_valid_governed_document_passes(self):
  r=self.repo();p=r/'docs/Releases/Test-Plan.md';p.write_text('# P\n'+block());self.assertEqual('PASS',self.validate(r,'docs/Releases/Test-Plan.md')['status'])
 def test_missing_required_line_fails(self):
  r=self.repo();p=r/'docs/Releases/Test-Plan.md';p.write_text(block().replace('PATCH_AND_RETRY_CYCLE=PROHIBITED\n',''));self.assertEqual('FAIL',self.validate(r,'docs/Releases/Test-Plan.md')['status'])
 def test_duplicate_assignment_fails(self):
  r=self.repo();p=r/'docs/Releases/Test-Plan.md';p.write_text(block()+'EXCEPTION_STATUS=NOT_GRANTED\n');self.assertEqual('FAIL',self.validate(r,'docs/Releases/Test-Plan.md')['status'])
 def test_approved_without_record_fails(self):
  r=self.repo();p=r/'docs/Releases/Test-Plan.md';p.write_text(block(status='APPROVED'));self.assertEqual('FAIL',self.validate(r,'docs/Releases/Test-Plan.md')['status'])
 def good_exception(self,r,name='EX-001.md'):
  p=r/'docs/Exceptions'/name;p.write_text('EXCEPTION_STATUS=APPROVED\nAPPROVED_BY=Tim Simmons\nAPPROVED_GITHUB_LOGIN=TimSimmons3\nAPPROVED_UTC=2026-08-05T14:00:00Z\nAPPROVAL_TEXT_SHA256='+'a'*64+'\nCONTROL_IDS=X\nSCOPE=X\nRATIONALE=X\nRESIDUAL_RISK=X\nCOMPENSATING_CONTROLS=X\nEXPIRATION_UTC=2026-08-06T14:00:00Z\nARTIFACT_SHA256_SET='+'b'*64+'\n');return p
 def test_valid_owner_exception_passes(self):
  r=self.repo();self.good_exception(r);p=r/'docs/Releases/Test-Plan.md';p.write_text(block(status='APPROVED')+'EXCEPTION_RECORD=docs/Exceptions/EX-001.md\n');self.assertEqual('PASS',self.validate(r,'docs/Releases/Test-Plan.md','docs/Exceptions/EX-001.md')['status'])
 def test_exception_readme_uses_normal_invariant(self):
  r=self.repo();p=r/'docs/Exceptions/README.md';p.write_text(block());self.assertEqual('PASS',self.validate(r,'docs/Exceptions/README.md')['status'])
 def test_wrong_owner_exception_fails(self):
  r=self.repo();p=self.good_exception(r);p.write_text(p.read_text().replace('APPROVED_BY=Tim Simmons','APPROVED_BY=Other'));self.assertEqual('FAIL',self.validate(r,'docs/Exceptions/EX-001.md')['status'])
 def test_placeholder_exception_fails(self):
  r=self.repo();p=self.good_exception(r);p.write_text(p.read_text().replace('SCOPE=X','SCOPE=TBD'));self.assertEqual('FAIL',self.validate(r,'docs/Exceptions/EX-001.md')['status'])
 def test_non_governed_file_ignored(self):
  r=self.repo();(r/'notes.md').write_text('# N\n');x=self.validate(r,'notes.md');self.assertEqual('PASS',x['status']);self.assertEqual(0,x['governed_file_count'])
 def test_keyword_governs_root_file(self):
  r=self.repo();(r/'Project-Handoff.md').write_text('# H\n');self.assertEqual('FAIL',self.validate(r,'Project-Handoff.md')['status'])
 def test_symlink_rejected(self):
  r=self.repo();(r/'target.md').write_text(block());p=r/'docs/Releases/Test-Plan.md';p.symlink_to(r/'target.md');self.assertEqual('FAIL',self.validate(r,'docs/Releases/Test-Plan.md')['status'])
 def test_trailing_whitespace_fails(self):
  r=self.repo();p=r/'docs/Releases/Test-Plan.md';p.write_text(block()+'bad  \n');self.assertEqual('FAIL',self.validate(r,'docs/Releases/Test-Plan.md')['status'])
 def test_outside_path_rejected(self):
  r=self.repo();p=r.parent/'outside-plan.md';p.write_text(block());self.assertEqual('FAIL',self.validate(r,str(p))['status'])
 def test_load_json_strict_rejects_duplicate_keys(self):
  r=self.repo();p=r/'x';p.write_text('{"a":1,"a":2}');self.assertRaises(ValueError,m.load_json_strict,p)
 def test_load_json_strict_rejects_non_object(self):
  r=self.repo();p=r/'x';p.write_text('[]');self.assertRaises(ValueError,m.load_json_strict,p)
 def test_invalid_utf8_fails(self):
  r=self.repo();p=r/'docs/Releases/Test-Plan.md';p.write_bytes(b'\xff');self.assertEqual('FAIL',self.validate(r,'docs/Releases/Test-Plan.md')['status'])
 def test_cr_character_fails(self):
  r=self.repo();p=r/'docs/Releases/Test-Plan.md';p.write_bytes(('# P\r\n'+block()).encode());self.assertEqual('FAIL',self.validate(r,'docs/Releases/Test-Plan.md')['status'])
 def test_missing_changed_path_fails(self):self.assertEqual('FAIL',self.validate(self.repo(),'docs/Releases/Missing-Plan.md')['status'])
 def test_directory_changed_path_fails(self):self.assertEqual('FAIL',self.validate(self.repo(),'docs/Releases')['status'])
 def test_malformed_exception_formats_fail(self):
  r=self.repo();p=self.good_exception(r);p.write_text(p.read_text().replace('APPROVED_UTC=2026-08-05T14:00:00Z','APPROVED_UTC=bad'));self.assertEqual('FAIL',self.validate(r,'docs/Exceptions/EX-001.md')['status'])
 def test_approved_record_outside_directory_fails(self):
  r=self.repo();q=r/'docs/Releases/Other.md';q.write_text(block());p=r/'docs/Releases/Test-Plan.md';p.write_text(block(status='APPROVED')+'EXCEPTION_RECORD=docs/Releases/Other.md\n');self.assertEqual('FAIL',self.validate(r,'docs/Releases/Test-Plan.md')['status'])
 def test_policy_shape_valid(self):self.assertEqual([],m.policy_shape_errors(POLICY,'p'))
 def test_policy_shape_non_object(self):self.assertTrue(m.policy_shape_errors([], 'p'))
 def test_policy_compat_exact_passes(self):self.assertEqual([],m.policy_compatibility_errors(POLICY,copy.deepcopy(POLICY)))
 def test_current_governance_keyword_positive(self):self.assertTrue(m.is_governed('X-Handoff.md',POLICY))
 # New production-path discovery and history tests.
 def git_case(self,mutator):
  r=self.repo();p=r/'docs/Releases/Test-Plan.md';p.write_text(block());self.init(r);b=self.commit(r,'base');mutator(r,p);self.commit(r,'change');rp=r/'report.json';rc=m.main(['--repo-root',str(r),'--policy','config/mandatory-assurance-invariant-policy.json','--base-ref',b,'--report',str(rp)]);return rc,json.loads(rp.read_text()),r
 def test_base_ref_regular_to_symlink_T_fails(self):
  rc,d,_=self.git_case(lambda r,p:(p.unlink(),p.symlink_to('target')));self.assertEqual(1,rc);self.assertTrue(any('regular non-symlink' in x for x in d['violations']),d)
 def test_base_ref_delete_governed_fails(self):
  rc,d,_=self.git_case(lambda r,p:p.unlink());self.assertEqual(1,rc);self.assertIn('docs/Releases/Test-Plan.md',d['deleted_paths'])
 def test_base_ref_rename_outside_root_fails_via_old_path(self):
  def mut(r,p):p.rename(r/'moved.md')
  rc,d,_=self.git_case(mut);self.assertEqual(1,rc);self.assertIn('docs/Releases/Test-Plan.md',d['deleted_paths'])
 def test_base_ref_mode_only_valid_content_passes(self):
  rc,d,_=self.git_case(lambda r,p:p.chmod(0o755));self.assertEqual(0,rc);self.assertEqual('PASS',d['status'])
 def test_base_ref_current_policy_cannot_remove_root(self):
  def mut(r,p):
   pol=copy.deepcopy(POLICY);pol['governed_markdown_roots'].remove('docs/Releases/');(r/'config/mandatory-assurance-invariant-policy.json').write_text(json.dumps(pol))
  rc,d,_=self.git_case(mut);self.assertEqual(1,rc);self.assertTrue(any('may not remove' in x for x in d['violations']),d)
 def test_base_ref_current_policy_cannot_weaken_block(self):
  def mut(r,p):
   pol=copy.deepcopy(POLICY);pol['required_block']['PATCH_AND_RETRY_CYCLE']='ALLOWED';(r/'config/mandatory-assurance-invariant-policy.json').write_text(json.dumps(pol))
  rc,d,_=self.git_case(mut);self.assertEqual(1,rc);self.assertTrue(any('required_block is immutable' in x for x in d['violations']),d)
 def test_base_ref_current_policy_cannot_change_owner(self):
  def mut(r,p):
   pol=copy.deepcopy(POLICY);pol['owner']['github_login']='Other';(r/'config/mandatory-assurance-invariant-policy.json').write_text(json.dumps(pol))
  rc,d,_=self.git_case(mut);self.assertEqual(1,rc);self.assertTrue(any('owner is immutable' in x for x in d['violations']),d)
 def test_base_ref_historical_governance_sticky_when_additional_keyword_only(self):
  def mut(r,p):
   pol=copy.deepcopy(POLICY);pol['governed_filename_keywords'].append('new');(r/'config/mandatory-assurance-invariant-policy.json').write_text(json.dumps(pol));p.write_text('# missing invariant\n')
  rc,d,_=self.git_case(mut);self.assertEqual(1,rc);self.assertIn('docs/Releases/Test-Plan.md',d['base_governed_paths'])
 def test_base_ref_malformed_policy_structured_fail(self):
  def mut(r,p):(r/'config/mandatory-assurance-invariant-policy.json').write_text('{bad')
  rc,d,_=self.git_case(mut);self.assertEqual(1,rc);self.assertEqual('FAIL',d['status'])
 def test_base_ref_bad_base_structured_fail(self):
  r=self.repo();self.init(r);self.commit(r,'b');rp=r/'report';rc=m.main(['--repo-root',str(r),'--policy','config/mandatory-assurance-invariant-policy.json','--base-ref','bad','--report',str(rp)]);self.assertEqual(1,rc);self.assertEqual('FAIL',json.loads(rp.read_text())['status'])

 def test_final_recovery_policy_unexpected_top_field_fails(self):
  pol=copy.deepcopy(POLICY);pol['candidate_override']=True;self.assertTrue(any('unexpected top-level fields' in x for x in m.policy_shape_errors(pol,'p')))
 def test_final_recovery_policy_unexpected_owner_field_fails(self):
  pol=copy.deepcopy(POLICY);pol['owner']['candidate_override']=True;self.assertTrue(any('owner unexpected fields' in x for x in m.policy_shape_errors(pol,'p')))
 def test_final_recovery_policy_unexpected_exception_field_fails(self):
  pol=copy.deepcopy(POLICY);pol['exception']['candidate_override']=True;self.assertTrue(any('exception unexpected fields' in x for x in m.policy_shape_errors(pol,'p')))
 def test_final_recovery_legacy_base_without_resource_limits_bootstraps_canonical_limits(self):
  base=copy.deepcopy(POLICY);base.pop("resource_limits",None)
  self.assertEqual([],m.policy_shape_errors(base,"base",allow_legacy_missing_resource_limits=True))
  self.assertEqual([],m.policy_compatibility_errors(base,POLICY))

if __name__=='__main__':unittest.main()
