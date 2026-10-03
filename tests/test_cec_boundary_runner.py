import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments/jev-cec/missingness-boundary-001'))
import boundary_run as runner
from boundary_inputs import schedule,encode
class BoundaryRunnerTests(unittest.TestCase):
    def execute(self,transport):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        p=Path(tmp.name)/'run';r=runner.run(p,transport,'mock');runner.verify(p)
        return p,r
    def test_mock_counts_and_wire_order(self):
        p,r=self.execute(runner.mock_transport)
        self.assertEqual(r['eligibility_counts']['eligible'],128)
        for order,block in r['orders'].items():
            for c in block['conditions'].values():
                self.assertEqual(c['target_edges_eligible'],12)
                self.assertEqual(c['unrelated_edges_eligible'],12)
            for row in schedule():
                if row['order']==order:
                    payload=json.loads((p/'requests'/(row['attempt_id']+'.json')).read_text())
                    for q in payload['questions'].values():self.assertEqual(list(q['criteria']),sorted(q['criteria'],reverse=order=='reversed'))
    def test_target_and_unrelated_dependencies(self):
        calls=0
        def transport(raw):
            nonlocal calls
            calls+=1;status,response=runner.mock_transport(raw)
            if calls==1:
                d=json.loads(response);d['answers']['propagation']['probabilities']['yes']-=.01;response=encode(d)
            return status,response
        _,r=self.execute(transport)
        self.assertEqual(r['eligibility_counts']['eligible'],127)
        c=r['orders']['canonical']['conditions']['shared']
        self.assertEqual(c['target_edges_eligible'],11)
        self.assertEqual(c['unrelated_edges_eligible'],10)
        self.assertEqual(r['orders']['canonical']['paired_counts']['unavailable'],1)
    def test_perfect_fixture_targets(self):
        rows=schedule();key=json.loads((ROOT/'experiments/jev-cec/missingness-boundary-001/reference.json').read_text());refs={r['id']:r['judgments'] for r in key['cards']};records=[]
        for row in rows:
            _,raw=runner.mock_transport(encode(row['payload']));d=json.loads(raw)
            for dim,a in d['answers'].items():
                choice=refs[row['card_id']][dim]['label'];a['choice']=choice;a['probabilities']={k:float(k==choice) for k in a['probabilities']}
            records.append({'attempt_id':row['attempt_id'],'status':'valid','response_raw':encode(d)})
        r=runner.summarize(rows,records,key,'mock')
        for block in r['orders'].values():
            self.assertEqual(block['paired_counts'],{'both':32})
            for c in block['conditions'].values():
                self.assertTrue(all(e['target_matches_proposals'] and e['unrelated_changes']==0 for e in c['edges']))
        rows[0]['payload']['questions']['action']['criteria']=dict(reversed(list(rows[0]['payload']['questions']['action']['criteria'].items())))
        with self.assertRaises(ValueError):runner.summarize(rows,records,key,'mock')
    def test_stop_and_budget(self):
        _,r=self.execute(lambda raw:(503,b'{}'))
        self.assertEqual(r['request_counts']['not_attempted'],31)
        self.assertEqual(r['orders']['canonical']['paired_counts'],{'unavailable':32})
        with patch.object(runner,'CAP',runner.Decimal(0)):
            _,r=self.execute(lambda raw:self.fail())
        self.assertEqual(r['attempted_requests'],0)
        self.assertIsNone(r['orders']['canonical']['conditions']['shared']['by_dimension']['action']['agreement'])
    def test_interruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'run'
            def stop(raw):raise KeyboardInterrupt
            with self.assertRaises(KeyboardInterrupt):runner.run(p,stop,'mock')
            runner.verify(p);r=json.loads((p/'report.json').read_text())
            self.assertEqual(r['request_counts']['interrupted'],1)
            self.assertEqual(r['request_counts']['not_attempted'],31)
    def test_mock_archive_reproduces(self):
        p=ROOT/'experiments/jev-cec/missingness-boundary-001/mock-001';runner.verify(p)
        rows=json.loads((p/'schedule.json').read_text());records=json.loads((p/'attempts.json').read_text())
        for r in records:
            if r['status'] in ('valid','partial'):r['response_raw']=(p/'responses'/(r['attempt_id']+'.bin')).read_bytes()
        key=json.loads((p/'source/missingness-boundary-001/reference.json').read_text())
        actual=runner.summarize(rows,records,key,'mock');saved=json.loads((p/'report.json').read_text())
        for k,v in actual.items():self.assertEqual(v,saved[k])
        self.assertEqual(saved['live_requests_sent'],0)
