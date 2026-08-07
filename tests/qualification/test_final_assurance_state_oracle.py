from __future__ import annotations
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'config/adp-transition-governance-final-assurance-state-oracle-r1.json'
C=ROOT/'tests/qualification/final_assurance_oracle_probe_catalog.json'
O=json.loads(P.read_text())
CAT=json.loads(C.read_text())
class OracleTests(unittest.TestCase):
 def test_identity(self):self.assertEqual('ADP_TRANSITION_GOVERNANCE_FINAL_ASSURANCE_STATE_ORACLE_R1',O['policy_id']);self.assertEqual('1.0',O['schema_version'])
 def test_exact_108_unique_cells(self):ids=[x['cell_id'] for x in O['cells']];self.assertEqual(108,len(ids));self.assertEqual(108,len(set(ids)))
 def test_all_cells_applicable_and_disposition_defined(self):
  for c in O['cells']:
   with self.subTest(c=c['cell_id']):self.assertIs(c.get('applicable'),True);self.assertIn(c.get('expected_enforcement'),{'FAIL_CLOSED','VALIDATE_ALLOW','CONTRACT_SPECIFIC','HOLD_REQUALIFY'})
 def test_all_cells_have_independent_expected_result(self):
  for c in O['cells']:
   with self.subTest(c=c['cell_id']):self.assertTrue(c['expected_result'].strip());self.assertTrue(c['scenario'].strip());self.assertTrue(c['domain'].strip())
 def test_all_cells_map_architecture_control(self):
  allowed={f'ARC-{i:02d}' for i in range(1,14)}
  for c in O['cells']:
   with self.subTest(c=c['cell_id']):self.assertTrue(c['architecture_controls']);self.assertTrue(set(c['architecture_controls'])<=allowed)
 def test_required_domains_complete(self):
  self.assertEqual({'GIT_CHANGE_DISCOVERY','MANDATORY_INVARIANT','TRANSITION_POLICY','GOVERNANCE_IDENTITY','REFERENCE_GRAPH','PARSER_SCHEMA','WORKFLOW_TRUST_ROOT','REPORTING_PROCESS'},{x['domain'] for x in O['cells']})
 def test_known_escape_cells_present(self):
  by={x['cell_id']:x for x in O['cells']};self.assertIn('type change',by['GIT-11']['scenario'].lower());self.assertIn('same candidate',(by['WF-01']['scenario']+' '+by['WF-01']['expected_result']+' '+by['WF-01']['required_action']).lower());self.assertTrue({'ARC-06','ARC-07'}<=set(by['WF-01']['architecture_controls']))
 def test_no_cell_uses_implementation_test_as_expected_source(self):self.assertIn('independent',O['source'].lower())
 def test_probe_catalog_exactly_covers_oracle(self):
  oi=[x['cell_id'] for x in O['cells']];ci=[x['cell_id'] for x in CAT['cells']];self.assertEqual(108,len(ci));self.assertEqual(set(oi),set(ci));self.assertEqual(len(ci),len(set(ci)))
 def test_probe_catalog_is_separate_from_oracle_expectation_source(self):
  self.assertEqual('ADP_FINAL_ASSURANCE_IMPLEMENTATION_PROBE_CATALOG_R1',CAT['record_type']);self.assertNotIn('probe_id',O['cells'][0]);self.assertTrue(all(x.get('probe_type')=='UNITTEST' and x.get('probe_id') for x in CAT['cells']))
if __name__=='__main__':unittest.main()
