from __future__ import annotations
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
WF=(ROOT/'.github/workflows/mandatory-assurance-trusted-gate.yml').read_text(encoding='utf-8')
class TrustedWorkflowArchitectureTests(unittest.TestCase):
 def test_pull_request_target_is_trust_event(self):self.assertIn('pull_request_target:',WF)
 def test_permissions_are_read_only(self):
  self.assertIn('contents: read',WF);self.assertIn('issues: read',WF);self.assertIn('pull-requests: read',WF)
  for bad in ['contents: write','issues: write','pull-requests: write','actions: write','id-token: write']:self.assertNotIn(bad,WF)
 def test_separate_trusted_and_candidate_checkouts(self):self.assertIn('path: trusted',WF);self.assertIn('path: candidate',WF)
 def test_candidate_checkout_binds_pr_head_repository_and_sha(self):self.assertIn('repository: ${{ github.event.pull_request.head.repo.full_name }}',WF);self.assertIn('ref: ${{ github.event.pull_request.head.sha }}',WF)
 def test_credentials_not_persisted(self):self.assertGreaterEqual(WF.count('persist-credentials: false'),2)
 def test_executable_python_is_trusted_only(self):
  for line in WF.splitlines():
   if 'python3 ' in line and not 'python3 -c' in line:self.assertTrue('trusted/scripts/' in line or 'trusted/tests' in line,line)
 def test_no_candidate_shell_or_python_execution(self):
  for token in ['bash candidate/','sh candidate/','python candidate/','python3 candidate/','source candidate/','. candidate/']:
   self.assertNotIn(token,WF)
 def test_candidate_policy_is_data_input(self):self.assertIn('--policy candidate/config/mandatory-assurance-invariant-policy.json',WF);self.assertIn('--policy candidate/config/transition-metrics-policy.json',WF)
 def test_default_branch_checkout_must_equal_pr_base_sha(self):self.assertIn('git -C trusted rev-parse HEAD',WF);self.assertIn('= "${BASE_SHA}"',WF)
 def test_base_freshness_and_merge_tree_are_explicit(self):self.assertIn('merge-base "${BASE_SHA}" "${HEAD_SHA}"',WF);self.assertIn('merge-tree --write-tree',WF);self.assertIn('test "${merge_tree}" = "${head_tree}"',WF)
 def test_trust_root_runs_before_candidate_governance_validation(self):
  self.assertLess(WF.index('validate_assurance_trust_root.py'),WF.index('validate_mandatory_assurance_invariants.py'));self.assertLess(WF.index('validate_assurance_trust_root.py'),WF.index('validate_transition_metrics.py'))
 def test_comment_fetch_is_read_only_get(self):self.assertIn('gh api --paginate --slurp',WF);self.assertNotIn(' -X POST',WF);self.assertNotIn(' -X PATCH',WF);self.assertNotIn(' -X DELETE',WF)
 def test_reports_are_bound_to_base_head_tree_inputs(self):self.assertIn('trusted-base-sha.txt',WF);self.assertIn('trusted-head-sha.txt',WF);self.assertIn('trusted-head-tree.txt',WF)
 def test_trusted_default_branch_regression_executes_before_candidate_validation(self):
  self.assertIn("python3 -B -m unittest discover -s trusted/tests -p 'test_*.py'",WF)
  self.assertLess(WF.index('Run default-branch trusted assurance regression'),WF.index('Validate assurance trust-root change boundary'))
if __name__=='__main__':unittest.main()
