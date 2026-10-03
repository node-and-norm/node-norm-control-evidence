import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'experiments/jev-cec'))
import execution as e


def response():
    return {'model': e.MODEL, 'usage': {'input_tokens': 100, 'output_tokens': 30}, 'answers': {
        dim: {'type':'choice', 'choice':'unknown', 'confidence':0,
              'probabilities': {label: 0.125 for label in e.LABELS}} for dim in e.DIMS}}


class ExecutionTests(unittest.TestCase):
    def test_fixed_schedule_and_identical_repetitions(self):
        rows=e.schedule()
        self.assertEqual(len(rows),36)
        self.assertEqual(len({r['attempt_id'] for r in rows}),36)
        for i in range(12):
            self.assertEqual(rows[i]['payload'],rows[i+12]['payload'])
            self.assertEqual(rows[i]['payload'],rows[i+24]['payload'])
        self.assertEqual([r['card_id'] for r in rows[:12]],[f'C{i:02}' for i in range(1,13)])

    def test_valid_ties_and_raw_probabilities_preserved(self):
        doc=response()
        self.assertEqual(e.validate_response(json.dumps(doc)),doc)

    def test_invalid_numbers_and_sums(self):
        for value in (True, float('nan'), float('inf'), -0.1, 1.1, 0.124):
            doc=response(); doc['answers']['action']['probabilities']['yes']=value
            with self.subTest(value=value),self.assertRaises(ValueError):
                e.validate_response(json.dumps(doc))

    def test_duplicate_keys_rejected(self):
        raw=json.dumps(response()).replace('"input_tokens": 100','"input_tokens": 100, "input_tokens": 100')
        with self.assertRaisesRegex(ValueError,'duplicate'):
            e.validate_response(raw)

    def test_model_question_and_usage_mismatch(self):
        for defect in ('model','question','usage','boolean'):
            doc=response()
            if defect=='model':doc['model']='jev-latest'
            elif defect=='question':del doc['answers']['action']
            elif defect=='usage':del doc['usage']
            else:doc['usage']['input_tokens']=True
            with self.subTest(defect=defect),self.assertRaises(ValueError):e.validate_response(json.dumps(doc))

    def test_nonmaximum_choice_rejected_whole_request(self):
        doc=response();probs=doc['answers']['action']['probabilities']
        probs['yes']=0.25;probs['unknown']=0
        with self.assertRaisesRegex(ValueError,'maximum'):e.validate_response(json.dumps(doc))

    def test_schedule_preserved_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'run';e.prepare(path)
            manifest=json.loads((path/'manifest.json').read_text())
            self.assertEqual(manifest['requests_sent'],0)
            self.assertEqual(manifest['schedule_sha256'],e.sha((path/'schedule.json').read_bytes()))
            with self.assertRaises(FileExistsError):e.prepare(path)

    def test_wrong_choice_type_and_missing_probability_label(self):
        doc=response();doc['answers']['action']['choice']=[]
        with self.assertRaises(ValueError):e.validate_response(json.dumps(doc))
        doc=response();del doc['answers']['action']['probabilities']['yes']
        with self.assertRaises(ValueError):e.validate_response(json.dumps(doc))
