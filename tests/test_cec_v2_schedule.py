import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]/'experiments/jev-cec'
spec=importlib.util.spec_from_file_location('v2_schedule',ROOT/'execution-v2/prepare.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ScheduleV2Tests(unittest.TestCase):
    def test_schedule_denominators_and_isolation(self):
        rows=m.schedule()
        self.assertEqual(len(rows),90)
        self.assertEqual(len({r['attempt_id'] for r in rows}),90)
        for p in (1,2,3):
            subset=[r for r in rows if r['pass_id']==p]
            self.assertEqual(len(subset),30)
            self.assertEqual(sum(len(r['request']['questions']) for r in subset),120)
            self.assertEqual(len({r['request_sha256'] for r in subset}),29)
        for r in rows:
            self.assertEqual(set(r['request']['state']),{'synthetic','scope','evidence'})
            self.assertNotIn('expected',r['request']['state'])
    def test_shared_baseline_and_pair_changes(self):
        cards=json.loads((ROOT/'development-v2/prevention-001/cards.json').read_text())
        self.assertEqual(cards[1]['evidence'],cards[2]['evidence'])
        for a,b in zip(cards[::2],cards[1::2]):
            self.assertEqual(a['scope'],b['scope'])
            self.assertEqual(a['evidence'][0],b['evidence'][0])
            self.assertNotEqual(a['evidence'][1],b['evidence'][1])
    def test_every_new_judgment_has_located_rationale(self):
        folder=ROOT/'development-v2/prevention-001'
        cards={c['id']:c for c in json.loads((folder/'cards.json').read_text())}
        refs=json.loads((folder/'proposed-reference.json').read_text())
        self.assertEqual({r['id'] for r in refs},set(cards))
        for r in refs:
            self.assertEqual(set(r['judgments']),m.standard.DIMS)
            for j in r['judgments'].values():
                self.assertTrue(j['rationale'])
                self.assertTrue(set(j['evidence_ids']) <= {e['id'] for e in cards[r['id']]['evidence']})
