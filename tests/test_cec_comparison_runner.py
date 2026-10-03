import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments/jev-cec/instruction-comparison-001'))
import comparison_run as runner
from comparison_inputs import schedule,encode
class ComparisonRunnerTests(unittest.TestCase):
    def execute(self,transport):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        p=Path(tmp.name)/'run';r=runner.run(p,transport,'mock');runner.verify(p)
        return p,r
    def test_uniform_mock_has_zero_paired_difference(self):
        _,r=self.execute(runner.mock_transport)
        self.assertEqual(len(r['determinations']),480)
        self.assertEqual(len(r['paired_records']),240)
        for p in r['passes'].values():
            self.assertEqual(p['paired']['eligible'],120)
            self.assertEqual(p['paired']['agreement_difference'],0)
            for m in p['conditions'].values():self.assertEqual(m['mean_brier_loss'],.875)
        self.assertEqual(r['live_requests_sent'],0)
    def test_invalid_member_excludes_whole_pair(self):
        calls=0
        def transport(raw):
            nonlocal calls
            calls+=1;status,response=runner.mock_transport(raw)
            if calls==1:
                d=json.loads(response);del d['answers']['action'];response=encode(d)
            return status,response
        _,r=self.execute(transport)
        self.assertEqual(r['passes']['1']['paired']['eligible'],116)
        self.assertEqual(r['passes']['1']['conditions']['A']['valid'],116)
        self.assertEqual(r['passes']['1']['conditions']['B']['valid'],120)
    def test_failure_stops_without_retry(self):
        _,r=self.execute(lambda raw:(503,b'{}'))
        self.assertEqual(r['attempted_requests'],1)
        self.assertEqual(r['request_counts']['not_attempted'],119)
        self.assertIsNone(r['passes']['1']['paired']['agreement_difference'])
    def test_budget_and_preflight(self):
        with patch.object(runner,'CAP',runner.Decimal('0')):
            _,r=self.execute(lambda raw:self.fail())
        self.assertEqual(r['attempted_requests'],0)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):runner.run(Path(tmp)/'run',lambda raw:self.fail(),'live')
    def test_analysis_rejects_changed_schedule(self):
        rows=schedule();rows.reverse()
        with self.assertRaises(ValueError):runner.summarize(rows,[],[],'mock')
    def test_interruption_preserves_accounting(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'run'
            def interrupt(raw):raise KeyboardInterrupt
            with self.assertRaises(KeyboardInterrupt):runner.run(p,interrupt,'mock')
            runner.verify(p);r=json.loads((p/'report.json').read_text())
            self.assertEqual(r['request_counts']['interrupted'],1)
            self.assertEqual(r['request_counts']['not_attempted'],119)
    def test_paired_difference_direction(self):
        rows=schedule();base=ROOT/'experiments/jev-cec/execution-v2'
        key=json.loads((base/'reference-key.json').read_text());ref={r['id']:r['judgments'] for r in key}
        records=[]
        for row in rows:
            _,raw=runner.mock_transport(encode(row['payload']));doc=json.loads(raw)
            for dim,answer in doc['answers'].items():
                gold=ref[row['card_id']][dim]['value']
                choice=gold if row['condition']=='B' else next(k for k in answer['probabilities'] if k!=gold)
                answer['choice']=choice;answer['probabilities']={k:int(k==choice) for k in answer['probabilities']}
            records.append({'attempt_id':row['attempt_id'],'status':'valid','response_raw':encode(doc)})
        r=runner.summarize(rows,records,key,'mock')
        self.assertEqual(r['passes']['1']['paired']['agreement_difference'],1)
        self.assertEqual(r['passes']['1']['paired']['counts']['B_only'],120)

    def test_preserved_rehearsal_reproduces(self):
        p=ROOT/'experiments/jev-cec/instruction-comparison-001/mock-001'
        runner.verify(p)
        rows=json.loads((p/'schedule.json').read_text());records=json.loads((p/'attempts.json').read_text())
        for r in records:
            if r['status']=='valid':r['response_raw']=(p/'responses'/f'{r["attempt_id"]}.bin').read_bytes()
        key=json.loads((p/'source/execution-v2/reference-key.json').read_text())
        report=runner.summarize(rows,records,key,'mock');saved=json.loads((p/'report.json').read_text())
        for k,v in report.items():self.assertEqual(v,saved[k])
        self.assertEqual(saved['live_requests_sent'],0)
        self.assertFalse(json.loads((p/'metadata.json').read_text())['working_tree_dirty'])
