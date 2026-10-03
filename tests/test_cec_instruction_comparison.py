import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('instruction_comparison',ROOT/'experiments/jev-cec/instruction-comparison-001/prepare.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ComparisonTests(unittest.TestCase):
    def test_balanced_full_schedule(self):
        rows=m.schedule()
        self.assertEqual(len(rows),120)
        self.assertEqual(len({r['attempt_id'] for r in rows}),120)
        for p in (1,2):
            group=[r for r in rows if r['pass']==p]
            self.assertEqual(sum(r['condition']=='A' for r in group),30)
            self.assertEqual(sum(r['condition']=='A' for r in group[::2]),15)
        for i in range(0,60,2):
            self.assertEqual(rows[i]['card_id'],rows[i+60]['card_id'])
            self.assertNotEqual(rows[i]['condition'],rows[i+60]['condition'])
    def test_only_instructions_change(self):
        rows=m.schedule()
        for left,right in zip(rows[::2],rows[1::2]):
            self.assertEqual(left['card_id'],right['card_id'])
            a,b=left['payload'],right['payload']
            self.assertEqual(a['state'],b['state'])
            self.assertEqual(a['model'],b['model'])
            for d in a['questions']:
                self.assertEqual(a['questions'][d]['criteria'],b['questions'][d]['criteria'])
                self.assertNotEqual(a['questions'][d]['instructions'],b['questions'][d]['instructions'])
            self.assertEqual(set(a['state']),{'synthetic','scope','evidence'})
    def test_baseline_exactly_matches_v2(self):
        old={r['card_id']:r['payload'] for r in m.v2.schedule() if r['pass']==1}
        for row in m.schedule():
            if row['condition']=='A':self.assertEqual(row['payload'],old[row['card_id']])
