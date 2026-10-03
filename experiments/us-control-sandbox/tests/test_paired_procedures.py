import copy
import json
from pathlib import Path
import tempfile
import unittest
from paired_procedures import checklist, trace, digest, verify_response
from run_paired_demo import ROOT, run
from verify_run import verify


class PairedProcedures(unittest.TestCase):
    def envelope(self, name='recovery-001', objective='recorded_stop', run_path='runs/recovery-001'):
        packet = json.loads((ROOT/run_path/'assessment-packets'/f'{name}.json').read_text())
        return {'unit_id': 'test-unit', 'objective': objective,
                'scope': 'single-authored-packet-terminal-record', 'packet': packet,
                'packet_digest': digest(packet)}

    def test_acknowledged_stop_can_have_opposite_recorded_effects(self):
        a, b = self.envelope(), self.envelope('recovery-002')
        self.assertEqual(a['packet']['events'], b['packet']['events'])
        for procedure in (checklist, trace):
            self.assertEqual(procedure(a)['response'], 'effect_supported')
            self.assertEqual(procedure(b)['response'], 'fault_supported')

    def test_missing_downstream_is_unresolved_with_dependent_check(self):
        env = self.envelope('recovery-007')
        a, b = checklist(env), trace(env)
        self.assertEqual(a['response'], b['response'])
        self.assertEqual(a['response'], 'unresolved')
        self.assertEqual(len(a['checks']), 2)
        self.assertEqual(len(b['checks']), 3)
        self.assertIsNone(b['checks'][2]['satisfied'])

    def test_retry_and_delivery_contrasts(self):
        cases = [('recovery-004', 'at_most_one_effect', 'runs/recovery-001', 'effect_supported'),
                 ('recovery-005', 'at_most_one_effect', 'runs/recovery-001', 'fault_supported'),
                 ('packet-008', 'recorded_delivery', 'runs/rehearsal-002', 'effect_supported'),
                 ('packet-009', 'recorded_delivery', 'runs/rehearsal-002', 'fault_supported')]
        for name, objective, folder, expected in cases:
            env = self.envelope(name, objective, folder)
            self.assertEqual(checklist(env)['response'], expected)
            self.assertEqual(trace(env)['response'], expected)

    def test_rejected_command_or_ambiguous_request_does_not_become_fault(self):
        env = self.envelope()
        env['packet']['events'][0]['accepted'] = False
        env['packet_digest'] = digest(env['packet'])
        self.assertEqual(trace(env)['response'], 'unresolved')
        env = self.envelope('recovery-005', 'at_most_one_effect')
        env['packet']['downstream']['request_ids'][1] = 'different-request'
        env['packet_digest'] = digest(env['packet'])
        self.assertEqual(trace(env)['response'], 'unresolved')

    def test_false_provenance_or_expanded_scope_rejected(self):
        for field, value in (('packet_digest','bad'), ('scope','actual-human-control'), ('objective','HIT-Command')):
            env = self.envelope()
            env[field] = value
            with self.assertRaises(ValueError):
                checklist(env)
        env = self.envelope()
        env['expected'] = 'effect_supported'
        with self.assertRaises(ValueError):
            trace(env)

    def test_rationale_label_and_locator_tampering_detected(self):
        env = self.envelope()
        original = trace(env)
        verify_response(env, original)
        for field, value in (('response','fault_supported'), ('reason','Human oversight succeeded.'), ('outcome_locator','/events/0')):
            changed = copy.deepcopy(original)
            changed[field] = value
            with self.assertRaises(ValueError):
                verify_response(env, changed)
        changed = copy.deepcopy(original)
        changed['checks'][0]['locators'] = ['/downstream']
        with self.assertRaises(ValueError):
            verify_response(env, changed)

    def test_duplicate_objective_does_not_claim_task_completion(self):
        env = self.envelope('recovery-004', 'at_most_one_effect')
        env['packet']['downstream'] = {'effect_count': 0, 'request_ids': []}
        env['packet_digest'] = digest(env['packet'])
        result = trace(env)
        self.assertEqual(result['response'], 'effect_supported')
        self.assertEqual(result['objective'], 'at_most_one_effect')
        self.assertEqual(result['claim_scope'], 'single-authored-packet-terminal-record')

    def test_preserved_demo_has_no_reference_score_and_cannot_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)/'attempt'
            self.assertEqual(run(out), 0)
            self.assertGreater(verify(out), 0)
            summary = json.loads((out/'summary.json').read_text())
            self.assertEqual(len(summary['rows']), 7)
            self.assertTrue(all(row['labels_agree'] for row in summary['rows']))
            self.assertNotIn('metrics', summary)
            self.assertFalse(summary['tae_hit_scored'])
            with self.assertRaises(FileExistsError):
                run(out)
