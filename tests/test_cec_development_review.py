"""Integrity of exposed development material, not validity of authored labels."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]/'experiments/jev-cec/development-v2'

class DevelopmentReviewTests(unittest.TestCase):
    def setUp(self):
        self.cards = []
        self.references = []
        for folder in (ROOT, ROOT/'expansion-001'):
            self.cards += json.loads((folder/'cards.json').read_text())
            self.references += json.loads((folder/'proposed-reference.json').read_text())
        self.review = json.loads((ROOT/'expansion-001/reference-review.json').read_text())

    def test_review_bound_to_exact_sources(self):
        for name, digest in self.review['inputs'].items():
            self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), digest)

    def test_every_proposal_reviewed_once_with_valid_evidence(self):
        cards = {c['id']: c for c in self.cards}
        self.assertEqual(len(cards), len(self.cards))
        expected = {(r['id'], d): v for r in self.references for d, v in r['expected'].items()}
        seen = set()
        for item in self.review['judgments']:
            identity = (item['card_id'], item['dimension'])
            self.assertNotIn(identity, seen)
            seen.add(identity)
            self.assertEqual(item['original_proposal'], expected[identity])
            self.assertIsNone(item['replacement_label'])
            self.assertTrue(item['basis'])
            self.assertTrue(set(item['evidence_ids']) <= {e['id'] for e in cards[item['card_id']]['evidence']})
        self.assertEqual(seen, set(expected))
        self.assertEqual(len(seen), 104)
        self.assertFalse(self.review['independent'])

    def test_pairs_preserve_scope_and_common_evidence(self):
        pairs = {}
        for c in self.cards:
            pairs.setdefault(c['pair_id'], []).append(c)
            self.assertNotIn('expected', c)
            self.assertTrue(c['synthetic'])
        self.assertEqual(len(pairs), 13)
        for pair in pairs.values():
            self.assertEqual(len(pair), 2)
            a,b = pair
            self.assertEqual(a['scope'], b['scope'])
            self.assertEqual(a['evidence'][0], b['evidence'][0])
            self.assertNotEqual(a['evidence'][1], b['evidence'][1])

    def test_coverage_and_open_issues_remain_visible(self):
        labels = {v for r in self.references for v in r['expected'].values()}
        self.assertEqual(labels, {'yes','no','partial','conflicting','unknown','not_reported','not_observable','not_applicable'})
        unresolved = [j for j in self.review['judgments'] if j['disposition']=='open_construct_issue']
        self.assertTrue(unresolved)
        self.assertTrue(all(j['limitation'] for j in unresolved))
