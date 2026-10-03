import json
from pathlib import Path
import tempfile
import unittest
from evaluate_evidence import evaluate, run


class EvaluationRules(unittest.TestCase):
    def cohort(self, answers):
        key = [{'unit_id': str(i), 'reference': ref} for i, ref in enumerate(('supported_effect', 'supported_fault', 'unresolved'))]
        response = [{'unit_id': str(i), 'response': answer} for i, answer in enumerate(answers)]
        return key, response

    def test_full_nine_cell_matrix_and_denominators(self):
        key, response = [], []
        for ref in ('supported_effect', 'supported_fault', 'unresolved'):
            for answer in ('effect_supported', 'fault_supported', 'unresolved'):
                uid = ref + ':' + answer
                key.append({'unit_id': uid, 'reference': ref})
                response.append({'unit_id': uid, 'response': answer})
        result = evaluate(key, response)
        self.assertEqual(result['unit_count'], 9)
        self.assertTrue(all(count == 1 for row in result['matrix'].values() for count in row.values()))
        wanted = {'unsupported_reassurance': (2, 6), 'missed_documented_fault': (2, 3),
                  'appropriate_uncertainty': (1, 3), 'unsupported_negative': (2, 6),
                  'unnecessary_abstention': (2, 6), 'supported_effect_recognition': (1, 3)}
        for name, (n, d) in wanted.items():
            self.assertEqual(result['metrics'][name], {'numerator': n, 'denominator': d, 'rate': n/d})

    def test_always_unresolved_cannot_hide_missed_faults(self):
        key, response = self.cohort(['unresolved']*3)
        metrics = evaluate(key, response)['metrics']
        self.assertEqual(metrics['appropriate_uncertainty']['rate'], 1)
        self.assertEqual(metrics['missed_documented_fault']['rate'], 1)
        self.assertEqual(metrics['unnecessary_abstention']['rate'], 1)
        self.assertEqual(metrics['supported_effect_recognition']['rate'], 0)

    def test_optimistic_missing_evidence_is_unsupported_reassurance(self):
        key = [{'unit_id': 'a', 'reference': 'unresolved'}]
        response = [{'unit_id': 'a', 'response': 'effect_supported'}]
        result = evaluate(key, response)
        self.assertEqual(result['metrics']['unsupported_reassurance']['rate'], 1)
        self.assertIsNone(result['metrics']['missed_documented_fault']['rate'])
        self.assertIsNone(result['metrics']['supported_effect_recognition']['rate'])

    def test_correct_determinate_and_unresolved_responses(self):
        key, response = self.cohort(['effect_supported', 'fault_supported', 'unresolved'])
        metrics = evaluate(key, response)['metrics']
        for name in ('unsupported_reassurance', 'missed_documented_fault', 'unsupported_negative', 'unnecessary_abstention'):
            self.assertEqual(metrics[name]['numerator'], 0)
        self.assertEqual(metrics['supported_effect_recognition']['rate'], 1)
        self.assertEqual(metrics['appropriate_uncertainty']['rate'], 1)

    def test_missing_extra_and_duplicate_responses_fail_whole_run(self):
        key, response = self.cohort(['unresolved']*3)
        for rows in (response[:-1], response+[response[0]], response+[{'unit_id':'extra','response':'unresolved'}]):
            with self.assertRaises(ValueError):
                evaluate(key, rows)
        with self.assertRaises(ValueError):
            evaluate(key+[key[0]], response)

    def test_unknown_labels_and_outcome_bait_are_rejected(self):
        key, response = self.cohort(['unresolved']*3)
        for value in ('IE', '2', True, None):
            altered = [dict(row) for row in response]
            altered[0]['response'] = value
            with self.assertRaises(ValueError):
                evaluate(key, altered)
        key[0]['actual_outcome'] = 'successful'
        with self.assertRaises(ValueError):
            evaluate(key, response)

    def test_empty_cohort_cannot_be_reported_as_success(self):
        with self.assertRaises(ValueError):
            evaluate([], [])

    def test_failed_attempt_preserves_inputs_without_a_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            key, response = self.cohort(['unresolved']*3)
            (root/'key.json').write_text(json.dumps(key))
            (root/'response.json').write_text(json.dumps(response[:-1]))
            out = root/'attempt'
            self.assertEqual(run(root/'key.json', root/'response.json', out), 1)
            self.assertTrue((out/'failure.json').exists())
            self.assertFalse((out/'report.json').exists())
            self.assertEqual((out/'responses.json').read_bytes(), (root/'response.json').read_bytes())
            with self.assertRaises(FileExistsError):
                run(root/'key.json', root/'response.json', out)

    def test_successful_attempt_records_rule_and_input_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            key, response = self.cohort(['effect_supported', 'fault_supported', 'unresolved'])
            (root/'key.json').write_text(json.dumps(key))
            (root/'response.json').write_text(json.dumps(response))
            out = root/'attempt'
            self.assertEqual(run(root/'key.json', root/'response.json', out), 0)
            result = json.loads((out/'report.json').read_text())
            self.assertEqual(len(result['rules_sha256']), 64)
            self.assertEqual(set(result['input_sha256']), {'key', 'responses'})
            self.assertNotIn('score', result)
            self.assertFalse((out/'failure.json').exists())
