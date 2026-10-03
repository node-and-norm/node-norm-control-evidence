import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments/jev-cec/execution-v2'))
import v2_run as runner
from v2_inputs import check, encode, schedule
from v2_execution import validate_response

class V2RunnerTests(unittest.TestCase):
    def execute(self,transport):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        path=Path(tmp.name)/'run'
        report=runner.run(path,transport,'mock')
        runner.verify(path)
        return path,report

    def test_complete_mock_counts_and_arithmetic(self):
        _,r=self.execute(runner.mock_transport)
        self.assertEqual(r['request_counts']['valid'],90)
        self.assertEqual(r['live_requests_sent'],0)
        self.assertEqual(len(r['determinations']),360)
        for p in r['passes'].values():
            self.assertEqual(p['overall']['valid_determinations'],120)
            self.assertEqual(p['overall']['mean_brier_loss'],.875)
            self.assertEqual(p['overall']['coverage'],1)
        self.assertEqual(r['repeatability']['eligible_triplets'],120)
        self.assertEqual(len(r['pair_contrasts']),180)
        self.assertTrue(all(x['status']=='available' for x in r['pair_contrasts']))

    def test_one_bad_answer_invalidates_four_and_pair(self):
        calls=0
        def transport(payload):
            nonlocal calls
            calls+=1
            status,raw=runner.mock_transport(payload)
            if calls==1:
                doc=json.loads(raw);doc['answers']['trajectory_effect']['probabilities']['yes']=.1
                raw=encode(doc)
            return status,raw
        _,r=self.execute(transport)
        self.assertEqual(r['request_counts']['invalid'],1)
        self.assertEqual(r['passes']['1']['overall']['valid_determinations'],116)
        self.assertEqual(sum(x['status']=='unavailable' for x in r['pair_contrasts']),4)
        self.assertEqual(r['repeatability']['excluded_triplets'],4)

    def test_http_failure_no_retry(self):
        calls=[]
        _,r=self.execute(lambda raw:(calls.append(raw) or (429,b'{}')))
        self.assertEqual(len(calls),1)
        self.assertEqual(r['request_counts']['not_attempted'],89)
        self.assertIsNone(r['passes']['1']['overall']['agreement'])
        self.assertTrue(r['unknown_usage'])

    def test_missing_usage_and_model_mismatch_stop(self):
        for change,reason in [('usage','usage_unavailable'),('model','model_mismatch')]:
            def transport(payload):
                status,raw=runner.mock_transport(payload);doc=json.loads(raw)
                if change=='usage':del doc['usage']
                else:doc['model']='different-model'
                return status,encode(doc)
            _,r=self.execute(transport)
            self.assertEqual(r['stop_reason'],reason)
            self.assertEqual(r['request_counts']['not_attempted'],89)

    def test_transport_failure_and_interruption_preserved(self):
        def fail(raw):raise TimeoutError('not retained')
        _,r=self.execute(fail)
        self.assertEqual(r['request_counts']['transport_error'],1)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'run'
            def interrupt(raw):raise KeyboardInterrupt
            with self.assertRaises(KeyboardInterrupt):runner.run(p,interrupt,'mock')
            runner.verify(p)
            r=json.loads((p/'report.json').read_text())
            self.assertEqual(r['request_counts']['interrupted'],1)
            self.assertEqual(r['request_counts']['not_attempted'],89)

    def test_budget_prevents_dispatch(self):
        with patch.object(runner,'CAP',runner.Decimal('0')):
            _,r=self.execute(lambda raw:self.fail('must not send'))
        self.assertEqual(r['attempted_requests'],0)

    def test_three_question_response_is_rejected(self):
        _,raw=runner.mock_transport(encode(schedule()[0]['payload']))
        doc=json.loads(raw);del doc['answers']['trajectory_effect']
        with self.assertRaises(ValueError):validate_response(encode(doc))
        for bad in [b'{"model":1,"model":2}',b'{"model":NaN}']:
            with self.assertRaises(ValueError):validate_response(bad)

    def test_live_requires_preflight_before_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'run'
            with self.assertRaises(ValueError):runner.run(p,lambda raw:self.fail(),'live')
            self.assertFalse(p.exists())

    def test_manifest_detects_tampering(self):
        p,r=self.execute(runner.mock_transport)
        (p/'report.json').write_text('{}')
        with self.assertRaises(ValueError):runner.verify(p)
        self.assertEqual(check()['status'],'prospective_source_freeze')

    def test_preserved_mock_reproduces_report(self):
        p=ROOT/'experiments/jev-cec/execution-v2/mock-001'
        self.assertEqual(runner.verify(p)['mode'],'mock')
        rows=json.loads((p/'schedule.json').read_text())
        records=json.loads((p/'attempts.json').read_text())
        for r in records:
            if r['status']=='valid':r['response_raw']=(p/'responses'/f'{r["attempt_id"]}.bin').read_bytes()
        key=json.loads((p/'source/execution-v2/reference-key.json').read_text())
        actual=runner.summarize(rows,records,key,'mock')
        saved=json.loads((p/'report.json').read_text())
        for k,v in actual.items():self.assertEqual(v,saved[k])
        self.assertEqual(saved['live_requests_sent'],0)
        self.assertFalse(json.loads((p/'metadata.json').read_text())['working_tree_dirty'])

    def test_preserved_live_reproduction(self):
        p=ROOT/'experiments/jev-cec/execution-v2/live-001'
        self.assertEqual(runner.verify(p)['mode'],'live')
        rows=json.loads((p/'schedule.json').read_text())
        records=json.loads((p/'attempts.json').read_text())
        for r in records:
            if r['status']=='valid':r['response_raw']=(p/'responses'/f'{r["attempt_id"]}.bin').read_bytes()
        key=json.loads((p/'source/execution-v2/reference-key.json').read_text())
        actual=runner.summarize(rows,records,key,'live')
        saved=json.loads((p/'report.json').read_text())
        def compare(a,b,key=''):
            if isinstance(a,dict):
                self.assertEqual(set(a),set(b))
                for k in a:compare(a[k],b[k],k)
            elif isinstance(a,list):
                self.assertEqual(len(a),len(b))
                for x,y in zip(a,b):compare(x,y,key)
            elif key in ('brier_loss','mean_brier_loss') and isinstance(a,float):
                self.assertAlmostEqual(a,b,delta=1e-12)
            else:self.assertEqual(a,b)
        for k,v in actual.items():compare(v,saved[k],k)
        self.assertEqual(saved['live_requests_sent'],90)
        self.assertEqual(saved['request_counts']['invalid'],14)
        self.assertEqual(saved['passes']['1']['overall']['matches'],76)
        self.assertFalse(json.loads((p/'metadata.json').read_text())['working_tree_dirty'])

    def test_disagreement_review_preserves_all_outputs(self):
        import hashlib
        base=ROOT/'experiments/jev-cec/execution-v2'
        review=json.loads((base/'DISAGREEMENT-REVIEW.json').read_text())
        raw=(base/'live-001/report.json').read_bytes()
        report=json.loads(raw)
        self.assertEqual(review['source_report_sha256'],hashlib.sha256(raw).hexdigest())
        expected={(d['attempt_id'],d['card_id'],d['dimension'],d['choice'],d['reference']) for d in report['disagreements']}
        actual=[]
        for item in review['items']:
            self.assertEqual(item['adjudication_status'],'unresolved')
            self.assertIsNone(item['replacement_label'])
            for obs in item['observations']:
                request=json.loads((base/'live-001/requests'/f'{obs["attempt_id"]}.json').read_text())
                self.assertEqual(item['evidence'],request['state']['evidence'])
                self.assertEqual(item['question'],request['questions'][item['dimension']]['instructions'])
                actual.append((obs['attempt_id'],item['card_id'],item['dimension'],obs['choice'],item['reference']))
        self.assertEqual(len(actual),62)
        self.assertEqual(set(actual),expected)
        self.assertEqual(len(review['items']),30)
        self.assertEqual((base/'live-001/requests/P1-V2-14-B.json').read_bytes(),(base/'live-001/requests/P1-V2-15-A.json').read_bytes())
