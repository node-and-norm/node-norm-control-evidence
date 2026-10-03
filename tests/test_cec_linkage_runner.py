import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments/jev-cec/packet-linkage-001'))
import linkage_run as runner
from linkage_inputs import schedule, encode


class LinkageRunnerTests(unittest.TestCase):
    def execute(self, transport):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        path=Path(tmp.name)/'run'
        report=runner.run(path,transport,'mock');runner.verify(path)
        return path,report

    def test_unresolved_reference_never_scored(self):
        _,r=self.execute(runner.mock_transport)
        self.assertEqual(len(r['determinations']),32)
        self.assertEqual(r['live_requests_sent'],0)
        for p in r['passes'].values():
            self.assertEqual(p['eligible'],2)
            m=p['by_dimension']['original']['action']
            self.assertIsNone(m['matches']);self.assertIsNone(m['agreement'])
            self.assertEqual(p['by_dimension']['explicit']['action']['matches'],0)
        for d in r['determinations']:
            if d['condition']=='original' and d['dimension']=='action':
                self.assertIsNone(d['reference']);self.assertIsNone(d['matches_reference'])

    def test_sum_failure_excludes_all_four_answers(self):
        calls=0
        def transport(raw):
            nonlocal calls
            calls+=1;status,response=runner.mock_transport(raw)
            if calls==1:
                d=json.loads(response);d['answers']['action']['probabilities']['yes']-=.01
                response=encode(d)
            return status,response
        _,r=self.execute(transport)
        self.assertEqual(r['attempted_requests'],8)
        self.assertEqual(r['determination_counts']['invalid'],4)
        self.assertEqual(r['passes']['1']['eligible'],1)
        for m in r['passes']['1']['by_dimension']['original'].values():self.assertEqual(m['valid'],1)
        self.assertEqual(r['repetition']['original']['excluded'],1)

    def test_stop_and_zero_denominators(self):
        _,r=self.execute(lambda raw:(503,b'{}'))
        self.assertEqual(r['attempted_requests'],1)
        self.assertEqual(r['request_counts']['not_attempted'],7)
        self.assertIsNone(r['passes']['1']['by_dimension']['explicit']['action']['agreement'])
        self.assertEqual(r['passes']['1']['unavailable'],2)

    def test_transport_model_usage_stops(self):
        def error(raw):raise OSError('offline failure')
        _,r=self.execute(error);self.assertEqual(r['stop_reason'],'transport_error')
        for field,value,reason in [('model','wrong','model_mismatch'),('usage',None,'usage_unavailable')]:
            def transport(raw):
                status,response=runner.mock_transport(raw);d=json.loads(response);d[field]=value
                return status,encode(d)
            _,r=self.execute(transport)
            self.assertEqual(r['stop_reason'],reason);self.assertEqual(r['attempted_requests'],1)

    def test_budget_preflight_and_interruption(self):
        with patch.object(runner,'CAP',runner.Decimal('0')):
            _,r=self.execute(lambda raw:self.fail())
        self.assertEqual(r['attempted_requests'],0)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):runner.run(Path(tmp)/'live',lambda raw:self.fail(),'live')
            path=Path(tmp)/'interrupted'
            def interrupt(raw):raise KeyboardInterrupt
            with self.assertRaises(KeyboardInterrupt):runner.run(path,interrupt,'mock')
            runner.verify(path)
            r=json.loads((path/'report.json').read_text())
            self.assertEqual(r['request_counts']['interrupted'],1)
            self.assertEqual(r['request_counts']['not_attempted'],7)

    def test_schedule_and_manifest_tampering(self):
        rows=schedule();rows.reverse()
        with self.assertRaises(ValueError):runner.summarize(rows,[],{},'mock')
        path,_=self.execute(runner.mock_transport)
        (path/'report.json').write_text('{}')
        with self.assertRaises(ValueError):runner.verify(path)

    def test_preserved_mock_reproduces(self):
        path=ROOT/'experiments/jev-cec/packet-linkage-001/mock-001'
        runner.verify(path)
        rows=json.loads((path/'schedule.json').read_text())
        records=json.loads((path/'attempts.json').read_text())
        for record in records:
            if record['status']=='valid':
                record['response_raw']=(path/'responses'/f"{record['attempt_id']}.bin").read_bytes()
        key=json.loads((path/'source/packet-linkage-001/reference.json').read_text())
        result=runner.summarize(rows,records,key,'mock')
        saved=json.loads((path/'report.json').read_text())
        for name,value in result.items():self.assertEqual(value,saved[name])
        self.assertEqual(saved['live_requests_sent'],0)
