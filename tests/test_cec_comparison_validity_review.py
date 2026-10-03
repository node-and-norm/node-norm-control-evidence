"""Keep the diagnostic traceable to the unchanged live bytes."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'experiments/jev-cec/instruction-comparison-001'
spec = importlib.util.spec_from_file_location('review_validity', FOLDER / 'review_validity.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ValidityReviewTests(unittest.TestCase):
    def test_archive_reproduces_register(self):
        result = module.review()
        self.assertEqual(result, json.loads((FOLDER / 'VALIDITY-REVIEW.json').read_text()))
        self.assertEqual((result['attempts'], result['invalid_responses'], result['excluded_judgments']), (120, 14, 56))
        for failure in result['failures']:
            self.assertEqual(len(failure['failing_distributions']), 1)
            self.assertAlmostEqual(failure['failing_distributions'][0]['sum'], .99)
            self.assertTrue(failure['all_choices_are_maxima'])
