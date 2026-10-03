import importlib.util
import json
from pathlib import Path
import unittest
P=Path(__file__).resolve().parents[1]/'experiments/jev-cec/missingness-boundary-001'
spec=importlib.util.spec_from_file_location('missingness_prepare',P/'prepare.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class MissingnessTests(unittest.TestCase):
    def test_factorial_edges_and_reference(self):
        refs=json.loads((P/'reference.json').read_text())['cards'];cards=json.loads((P/'cards.json').read_text())
        signatures=[tuple(r['judgments'][d]['label'] for d in ('propagation','trajectory_effect','outcome_mitigation')) for r in refs]
        self.assertEqual(len(set(signatures)),8)
        edges=[(i,j) for i in range(8) for j in range(i+1,8) if sum(a!=b for a,b in zip(signatures[i],signatures[j]))==1]
        self.assertEqual(len(edges),12)
        for i,j in edges:self.assertEqual(sum(a!=b for a,b in zip(cards[i]['state']['evidence'],cards[j]['state']['evidence'])),1)
    def test_payload_and_order_manipulation(self):
        rows=m.schedule();self.assertEqual(len(rows),32)
        for row in rows:
            self.assertEqual(set(row['payload']),{'model','questions','state'})
            self.assertEqual(set(row['payload']['state']),{'scope','evidence','synthetic'})
            for q in row['payload']['questions'].values():
                names=list(q['criteria']);self.assertEqual(names,sorted(names,reverse=row['order']=='reversed'))
            other=next(r for r in rows if r['card_id']==row['card_id'] and r['condition']==row['condition'] and r['order']!=row['order'])
            self.assertNotEqual(row['payload_sha256'],other['payload_sha256'])
            self.assertEqual(row['payload'],other['payload'])
    def test_review_binds_all_judgments_and_changes(self):
        import hashlib
        review=json.loads((P/'REVIEW.json').read_text())
        self.assertEqual(len(review['judgments']),32)
        self.assertEqual(len({(r['card_id'],r['dimension']) for r in review['judgments']}),32)
        self.assertEqual(len(review['packet_clarifications']),12)
        for name in ('cards','reference'):
            self.assertEqual(review[name+'_sha256'],hashlib.sha256((P/(name+'.json')).read_bytes()).hexdigest())
        cards={c['id']:c for c in json.loads((P/'cards.json').read_text())}
        for r in review['judgments']:
            self.assertFalse(r['independent_adjudication'])
            for e in r['evidence']:self.assertIn(e,cards[r['card_id']]['state']['evidence'])
        for change in review['packet_clarifications']:
            e=next(e for e in cards[change['card_id']]['state']['evidence'] if e['id']==change['evidence_id'])
            self.assertEqual(e['text'],change['after'])
            self.assertIn('whether',e['text'])
