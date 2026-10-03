import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments/jev-cec/answer-execution-001'))
import answer_run as runner
from eligibility import assess
from answer_inputs import encode,schedule


class AnswerRunnerTests(unittest.TestCase):
    def raw(self):return runner.mock_transport(encode(schedule()[0]['payload']))[1]
    def execute(self,transport):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        p=Path(tmp.name)/'run';r=runner.run(p,transport,'mock');runner.verify(p)
        return p,r
    def test_partial_keeps_siblings_and_pair_dependencies(self):
        calls=0
        def transport(raw):
            nonlocal calls
            calls+=1;status,response=runner.mock_transport(raw)
            if calls==1:
                d=json.loads(response);d['answers']['action']['probabilities']['yes']-=.01;response=encode(d)
            return status,response,{'x-typesafe-request-id':'mock-id','Authorization':'must-not-store'}
        p,r=self.execute(transport)
        self.assertEqual(r['request_counts']['partial'],1)
        self.assertEqual(r['eligibility_counts']['eligible'],31)
        self.assertEqual(r['whole_response_eligible_judgments'],28)
        self.assertEqual(r['passes']['1']['eligible'],1)
        self.assertEqual(r['passes']['1']['by_dimension']['original']['propagation']['valid'],2)
        self.assertEqual(r['repetition']['original']['eligible'],1)
        attempts=json.loads((p/'attempts.json').read_text())
        self.assertEqual(attempts[0]['diagnostic_headers'],{'x-typesafe-request-id':'mock-id'})
        self.assertIsNone(r['passes']['1']['by_dimension']['original']['action']['agreement'])
    def test_bad_envelopes(self):
        for raw in [b'{',b'{"x":1,"x":2}',b'{"x":NaN}',b'[]']:
            self.assertFalse(assess(raw)['envelope_eligible'])
        d=json.loads(self.raw());del d['answers']['action']
        self.assertFalse(assess(encode(d))['envelope_eligible'])
        self.assertFalse(assess(self.raw(),503)['envelope_eligible'])
    def test_local_failures_and_ties(self):
        self.assertTrue(all(x['eligible'] for x in assess(self.raw())['answers'].values()))
        for value in [True,float('inf'),-.1,1.1,None]:
            d=json.loads(self.raw());d['answers']['action']['confidence']=value
            result=assess(encode(d))
            if value==float('inf'):self.assertFalse(result['envelope_eligible'])
            else:
                self.assertFalse(result['answers']['action']['eligible'])
                self.assertTrue(result['answers']['propagation']['eligible'])
        d=json.loads(self.raw());d['answers']['action']['probabilities']['yes']=.2
        result=assess(encode(d))['answers']['action']
        self.assertEqual(set(result['reasons']),{'sum_outside_tolerance','choice_not_maximum'})
    def test_zero_pairs_and_stop(self):
        _,r=self.execute(lambda raw:(503,b'{}'))
        self.assertEqual(r['attempted_requests'],1)
        self.assertEqual(r['request_counts']['not_attempted'],7)
        self.assertEqual(r['passes']['1']['eligible'],0)
        self.assertIsNone(r['passes']['1']['by_dimension']['explicit']['action']['agreement'])
    def test_all_invalid_answers(self):
        def transport(raw):
            status,response=runner.mock_transport(raw);d=json.loads(response)
            for k in d['answers']:d['answers'][k]=None
            return status,encode(d)
        _,r=self.execute(transport)
        self.assertEqual(r['request_counts']['invalid'],8)
        self.assertEqual(r['eligibility_counts']['eligible'],0)
    def test_mock_archive_reproduces(self):
        p=ROOT/'experiments/jev-cec/answer-execution-001/mock-001'
        runner.verify(p)
        rows=json.loads((p/'schedule.json').read_text());records=json.loads((p/'attempts.json').read_text())
        for r in records:
            if r['status'] in ('valid','partial'):r['response_raw']=(p/'responses'/(r['attempt_id']+'.bin')).read_bytes()
        key=json.loads((p/'source/packet-linkage-001/reference.json').read_text())
        actual=runner.summarize(rows,records,key,'mock');saved=json.loads((p/'report.json').read_text())
        for k,v in actual.items():self.assertEqual(v,saved[k])
        self.assertEqual(saved['live_requests_sent'],0)
    def test_live_archive_reproduces(self):
        p=ROOT/'experiments/jev-cec/answer-execution-001/live-001'
        runner.verify(p)
        rows=json.loads((p/'schedule.json').read_text());records=json.loads((p/'attempts.json').read_text())
        for r in records:
            if r['status'] in ('valid','partial'):r['response_raw']=(p/'responses'/(r['attempt_id']+'.bin')).read_bytes()
        key=json.loads((p/'source/packet-linkage-001/reference.json').read_text())
        actual=runner.summarize(rows,records,key,'live');saved=json.loads((p/'report.json').read_text())
        for k,v in actual.items():self.assertEqual(v,saved[k])
        self.assertEqual(saved['live_requests_sent'],8)
