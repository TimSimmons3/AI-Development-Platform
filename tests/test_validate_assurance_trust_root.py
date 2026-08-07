from __future__ import annotations
import copy,hashlib,importlib.util,json,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'scripts/validate_assurance_trust_root.py';S=importlib.util.spec_from_file_location('t',P);assert S and S.loader
t=importlib.util.module_from_spec(S);S.loader.exec_module(t);MAN=json.loads((ROOT/'config/assurance-trust-root-manifest.json').read_text())
class TrustRootTests(unittest.TestCase):
 def repo(self):
  r=Path(tempfile.mkdtemp());subprocess.run(['git','init','-q'],cwd=r,check=True);subprocess.run(['git','config','user.name','T'],cwd=r,check=True);subprocess.run(['git','config','user.email','t@example.invalid'],cwd=r,check=True)
  for rel in MAN['trusted_paths']:
   p=r/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('trusted\n')
  return r
 def commit(self,r,m):subprocess.run(['git','add','-A'],cwd=r,check=True);subprocess.run(['git','commit','-qm',m],cwd=r,check=True);return subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip()
 def test_manifest_valid(self):self.assertEqual([],t.manifest_errors(MAN))
 def test_unrelated_change_passes_ordinary(self):
  r=self.repo();b=self.commit(r,'base');(r/'note').write_text('x');self.commit(r,'c');self.assertEqual('PASS',t.validate(r,b,MAN,'ordinary',None,[])['status'])
 def test_trust_root_change_fails_ordinary(self):
  r=self.repo();b=self.commit(r,'base');(r/'scripts/validate_transition_metrics.py').write_text('changed');self.commit(r,'c');x=t.validate(r,b,MAN,'ordinary',None,[]);self.assertEqual('FAIL',x['status']);self.assertIn('scripts/validate_transition_metrics.py',x['changed_trust_root_paths'])
 def make_migration(self,r,b,change='scripts/validate_transition_metrics.py',pr=5):
  (r/change).write_text('changed\n');record='docs/Releases/Assurance-Trust-Root-Migration-R1.json';rp=r/record;rp.parent.mkdir(parents=True,exist_ok=True);changed=[change];rationale='qualified assurance trust-root migration';rec={'record_type':'SMT_ASSURANCE_TRUST_ROOT_MIGRATION','schema_version':'1.0','base_commit':b,'changed_trust_root_paths':changed,'owner_login':MAN['owner_login'],'rationale':rationale,'rationale_sha256':hashlib.sha256(rationale.encode()).hexdigest()};rp.write_text(json.dumps(rec,sort_keys=True)+'\n');head=self.commit(r,'migration');expected=t.expected_approval(pr,head,record,changed);comments=[{'user':{'login':MAN['owner_login']},'body':expected}];return t.validate(r,b,MAN,'migration',pr,comments),head
 def test_exact_migration_record_and_owner_approval_pass(self):
  r=self.repo();b=self.commit(r,'base');x,h=self.make_migration(r,b);self.assertEqual('PASS',x['status'],x['violations']);self.assertEqual(h,x['head_commit']);self.assertEqual(1,x['matching_owner_approval_count'])
 def test_migration_without_exact_owner_approval_fails(self):
  r=self.repo();b=self.commit(r,'base');(r/'scripts/validate_transition_metrics.py').write_text('changed\n');record='docs/Releases/Assurance-Trust-Root-Migration-R1.json';rp=r/record;rp.parent.mkdir(parents=True,exist_ok=True);reason='x';rp.write_text(json.dumps({'record_type':'SMT_ASSURANCE_TRUST_ROOT_MIGRATION','schema_version':'1.0','base_commit':b,'changed_trust_root_paths':['scripts/validate_transition_metrics.py'],'owner_login':MAN['owner_login'],'rationale':reason,'rationale_sha256':hashlib.sha256(reason.encode()).hexdigest()}));self.commit(r,'m');x=t.validate(r,b,MAN,'migration',5,[]);self.assertEqual('FAIL',x['status'])
 def test_paths_digest_ordered(self):self.assertEqual(t.paths_digest(['a','b']),hashlib.sha256(b'a\nb\n').hexdigest())
 def test_expected_approval_binds_head(self):self.assertIn('HEAD='+'a'*40,t.expected_approval(5,'a'*40,'docs/Releases/Assurance-Trust-Root-Migration-R1.json',['x']))
 def test_manifest_rejects_unsorted_paths(self):
  m=copy.deepcopy(MAN);m['trusted_paths']=list(reversed(m['trusted_paths']));self.assertTrue(t.manifest_errors(m))
 def test_comment_normalization_rejects_scalar(self):self.assertRaises(ValueError,t.normalized_comments,{})
 def test_migration_cannot_delete_existing_trusted_path(self):
  r=self.repo();b=self.commit(r,'base');(r/'scripts/validate_transition_metrics.py').unlink();self.commit(r,'d');x=t.validate(r,b,MAN,'migration',5,[]);self.assertEqual('FAIL',x['status']);self.assertTrue(any('deletion is prohibited' in y for y in x['violations']),x)
 def test_migration_cannot_type_change_trusted_path_to_symlink(self):
  r=self.repo();b=self.commit(r,'base');p=r/'scripts/validate_transition_metrics.py';p.unlink();p.symlink_to('target');self.commit(r,'t');x=t.validate(r,b,MAN,'migration',5,[]);self.assertEqual('FAIL',x['status']);self.assertTrue(any('regular blob' in y for y in x['violations']),x)
 def test_candidate_manifest_cannot_remove_trusted_path(self):
  r=self.repo();b=self.commit(r,'base');cm=copy.deepcopy(MAN);cm['trusted_paths'].remove('scripts/validate_transition_metrics.py');(r/'config/assurance-trust-root-manifest.json').write_text(json.dumps(cm,sort_keys=True));self.commit(r,'m');x=t.validate(r,b,MAN,'migration',5,[]);self.assertEqual('FAIL',x['status']);self.assertTrue(any('may not remove' in y for y in x['violations']),x)
 def test_candidate_manifest_addition_must_exist_in_same_migration(self):
  r=self.repo();b=self.commit(r,'base');cm=copy.deepcopy(MAN);cm['trusted_paths'].append('scripts/new_trusted.py');cm['trusted_paths']=sorted(cm['trusted_paths']);(r/'config/assurance-trust-root-manifest.json').write_text(json.dumps(cm,sort_keys=True));self.commit(r,'m');x=t.validate(r,b,MAN,'migration',5,[]);self.assertEqual('FAIL',x['status']);self.assertTrue(any('new trusted paths must be introduced' in y for y in x['violations']),x)

 def test_stale_base_fails_closed(self):
  r=self.repo();b=self.commit(r,'base');subprocess.run(['git','branch','candidate',b],cwd=r,check=True);(r/'base-advance').write_text('x');newbase=self.commit(r,'base advance');subprocess.run(['git','switch','-q','candidate'],cwd=r,check=True);(r/'note').write_text('candidate');self.commit(r,'candidate');x=t.validate(r,newbase,MAN,'ordinary',None,[]);self.assertEqual('FAIL',x['status']);self.assertTrue(any('base freshness failure' in y for y in x['violations']),x)

 def test_manifest_rejects_unexpected_field(self):
  m=copy.deepcopy(MAN);m['unexpected']=1;self.assertTrue(any('unexpected' in x for x in t.manifest_errors(m)))
 def test_migration_rejects_unexpected_field(self):
  r=self.repo();b=self.commit(r,'base');(r/'scripts/validate_transition_metrics.py').write_text('changed\n');changed=['scripts/validate_transition_metrics.py'];reason='x';rec={'record_type':'SMT_ASSURANCE_TRUST_ROOT_MIGRATION','schema_version':'1.0','base_commit':b,'changed_trust_root_paths':changed,'owner_login':MAN['owner_login'],'rationale':reason,'rationale_sha256':hashlib.sha256(reason.encode()).hexdigest(),'unexpected':1};self.assertTrue(any('unexpected' in x for x in t.migration_record_errors(rec,b,changed,MAN['owner_login'])))
 def test_load_json_oversize_fails_bounded(self):
  p=Path(tempfile.mkdtemp())/'x.json';p.write_bytes(b' '*(t.MAX_JSON_BYTES+1));self.assertRaises(ValueError,t.load_json_strict,p)

 def test_manifest_protects_future_trusted_regression_and_codeowners(self):
  required={'.github/CODEOWNERS','tests/test_validate_mandatory_assurance_invariants.py','tests/test_validate_owner_exception_approval.py','tests/test_validate_transition_metrics.py'}
  self.assertTrue(required<=set(MAN['trusted_paths']))
 def test_codeowners_covers_every_trust_root_path(self):
  lines=[]
  for raw in (ROOT/'.github/CODEOWNERS').read_text().splitlines():
   raw=raw.strip()
   if not raw or raw.startswith('#'):continue
   pattern,*owners=raw.split();lines.append((pattern,owners))
  for path in MAN['trusted_paths']:
   matches=[]
   for pattern,owners in lines:
    q=pattern.lstrip('/')
    if (q.endswith('/') and path.startswith(q)) or path==q:matches.append(owners)
   self.assertTrue(matches,path)
   self.assertIn('@TimSimmons3',matches[-1],path)
if __name__=='__main__':unittest.main()
