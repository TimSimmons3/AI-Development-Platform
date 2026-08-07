from __future__ import annotations
import copy, importlib.util, json, subprocess, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);assert spec and spec.loader
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

T=load('transition',Path('scripts/validate_transition_metrics.py'))
M=load('mandatory',Path('scripts/validate_mandatory_assurance_invariants.py'))
TP=json.loads((ROOT/'config/transition-metrics-policy.json').read_text())
MP=json.loads((ROOT/'config/mandatory-assurance-invariant-policy.json').read_text())
START=json.loads((ROOT/'docs/Releases/metrics/ADP-Transition-Governance-Repository-Integration-R1-Implementation-Start-Metrics.json').read_text())

class FinalAssuranceExceptionSurfaceTests(unittest.TestCase):
    def init(self, repo:Path):
        subprocess.run(['git','init','-q'],cwd=repo,check=True);subprocess.run(['git','config','user.name','Test'],cwd=repo,check=True);subprocess.run(['git','config','user.email','test@example.invalid'],cwd=repo,check=True)
    def commit(self,repo,msg):
        subprocess.run(['git','add','-A'],cwd=repo,check=True);subprocess.run(['git','commit','-qm',msg],cwd=repo,check=True);return subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
    def transition_repo(self):
        r=Path(tempfile.mkdtemp());(r/'config').mkdir();(r/'docs/Releases/metrics').mkdir(parents=True)
        (r/'config/transition-metrics-policy.json').write_text(json.dumps(TP)+'\n')
        return r
    def mandatory_repo(self):
        r=Path(tempfile.mkdtemp());(r/'config').mkdir();(r/'docs/Releases').mkdir(parents=True)
        (r/'config/mandatory-assurance-invariant-policy.json').write_text(json.dumps(MP)+'\n')
        return r
    def test_transition_resource_limit_policy_shape(self):
        for bad in [None,{}, {'json_bytes':1,'csv_bytes':4194304,'markdown_bytes':2097152}, {'json_bytes':1048577,'csv_bytes':4194304,'markdown_bytes':2097152}]:
            p=copy.deepcopy(TP);p['resource_limits']=bad
            with self.subTest(bad=bad):self.assertTrue(any('resource_limits' in e for e in T.policy_shape_errors(p,'p')))
    def test_mandatory_resource_limit_policy_shape(self):
        for bad in [None,{}, {'json_bytes':1024,'markdown_bytes':2097153}]:
            p=copy.deepcopy(MP);p['resource_limits']=bad
            with self.subTest(bad=bad):self.assertTrue(any('resource_limits' in e for e in M.policy_shape_errors(p,'p')))
    def test_transition_resource_limits_immutable(self):
        cur=copy.deepcopy(TP);cur['resource_limits']['json_bytes']//=2
        self.assertTrue(any('resource_limits' in e for e in T.policy_identity_compatibility_errors(TP,cur)))
    def test_mandatory_resource_limits_immutable_after_bootstrap(self):
        cur=copy.deepcopy(MP);cur['resource_limits']['markdown_bytes']//=2
        self.assertTrue(any('resource_limits' in e for e in M.policy_compatibility_errors(MP,cur)))
    def test_mandatory_resource_limit_bootstrap_exact_default_only(self):
        base=copy.deepcopy(MP);base.pop('resource_limits')
        self.assertEqual([],M.policy_compatibility_errors(base,MP))
        cur=copy.deepcopy(MP);cur['resource_limits']['json_bytes']//=2
        self.assertTrue(any('bootstrap' in e for e in M.policy_compatibility_errors(base,cur)))
    def test_changed_transition_json_over_limit_is_structured_fail(self):
        r=self.transition_repo();self.init(r);base=self.commit(r,'base');p=r/'docs/Releases/metrics/huge.json';p.write_bytes(b'{' + b' '*(TP['resource_limits']['json_bytes']+1));self.commit(r,'huge')
        out=r/'report.json';rc=T.main(['--repo-root',str(r),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(out)]);data=json.loads(out.read_text())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertTrue(any('exceeds limit' in e for e in data['violations']),data['violations'])
    def test_changed_mandatory_markdown_over_limit_is_structured_fail(self):
        r=self.mandatory_repo();p=r/'docs/Releases/X-Plan.md';p.write_text('x\n');self.init(r);base=self.commit(r,'base');p.write_bytes(b'x'*(MP['resource_limits']['markdown_bytes']+1));self.commit(r,'huge')
        out=r/'report.json';rc=M.main(['--repo-root',str(r),'--policy','config/mandatory-assurance-invariant-policy.json','--base-ref',base,'--report',str(out)]);data=json.loads(out.read_text())
        self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertTrue(any('exceeds limit' in e for e in data['violations']),data['violations'])
    def test_deep_changed_json_never_raises(self):
        r=self.transition_repo();self.init(r);base=self.commit(r,'base');p=r/'docs/Releases/metrics/deep.json';p.write_text('['*2000+'0'+']'*2000);self.commit(r,'deep');out=r/'report.json'
        try:rc=T.main(['--repo-root',str(r),'--policy','config/transition-metrics-policy.json','--base-ref',base,'--report',str(out)])
        except Exception as exc:self.fail(f'unhandled {type(exc).__name__}: {exc}')
        data=json.loads(out.read_text());self.assertEqual(1,rc);self.assertEqual('FAIL',data['status']);self.assertTrue(data['violations'])
    def test_policy_json_over_absolute_limit_never_parsed(self):
        r=self.transition_repo();p=r/'config/transition-metrics-policy.json';p.write_bytes(b'{' + b' '*(T.ABSOLUTE_RESOURCE_LIMITS['json_bytes']+1));out=r/'report.json'
        try:rc=T.main(['--repo-root',str(r),'--policy','config/transition-metrics-policy.json','--files','x','--report',str(out)])
        except Exception as exc:self.fail(f'unhandled {type(exc).__name__}: {exc}')
        self.assertEqual(1,rc);self.assertIn('exceeds limit',out.read_text())
    def test_csv_projection_over_limit_fails_without_parse(self):
        r=self.transition_repo();rec=copy.deepcopy(START);rec['baseline_commit']='a'*40;rec['baseline_snapshot']='s';rec['created_utc']='2026-08-07T12:00:00Z';rec['prior_handoff_unavailable_reason']='x';rec['csv_projection_path']='docs/Releases/metrics/huge.csv'
        p=r/rec['csv_projection_path'];p.write_bytes(b'x'*(TP['resource_limits']['csv_bytes']+1));errs=T.validate_csv_projection(p,rec['metrics'],'x',TP['resource_limits']['csv_bytes']);self.assertTrue(any('exceeds limit' in x for x in errs),errs)

if __name__=='__main__':unittest.main()
