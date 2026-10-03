import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments/jev-cec'))
import run as runner
from analysis import summarize
from execution import schedule


class RunnerTests(unittest.TestCase):
    def execute(self, transport):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        path=Path(tmp.name)/'run'
        report=runner.run(path,transport,'mock')
        runner.verify(path)
        return path,report

    def test_complete_mock_arithmetic_and_no_live_claim(self):
        path,report=self.execute(runner.mock_transport)
        self.assertEqual(report['request_counts']['valid'],36)
        self.assertEqual(report['live_requests_sent'],0)
        primary=report['passes']['1']['overall']
        self.assertEqual(primary['valid_determinations'],36)
        self.assertEqual(primary['mean_brier_loss'],0.875)
        self.assertIsNone(primary['recall']['not_applicable'])
        self.assertEqual(report['repeatability']['eligible_triplets'],36)
        self.assertEqual(report['repeatability']['all_three_same'],36)
        self.assertTrue(all(d['review_disposition']=='unresolved' for d in report['disagreements']))
        with self.assertRaises(FileExistsError):runner.run(path,runner.mock_transport,'mock')

    def test_invalid_probability_retained_no_retry(self):
        calls=[]
        def transport(raw):
            calls.append(raw);status,response=runner.mock_transport(raw)
            if len(calls)==1:
                doc=json.loads(response);doc['answers']['action']['probabilities']['yes']=0.3
                response=runner.encode(doc)
            return status,response
        path,report=self.execute(transport)
        self.assertEqual(len(calls),36)
        self.assertEqual(report['request_counts']['invalid'],1)
        self.assertEqual(report['passes']['1']['overall']['valid_determinations'],33)
        self.assertEqual(report['repeatability']['excluded_triplets'],3)
        self.assertIn(b'0.3',(path/'responses/P1-C01.bin').read_bytes())

    def test_missing_usage_stops(self):
        def transport(raw):
            _,response=runner.mock_transport(raw);doc=json.loads(response);del doc['usage']
            return 200,runner.encode(doc)
        _,report=self.execute(transport)
        self.assertEqual(report['request_counts']['invalid'],1)
        self.assertEqual(report['request_counts']['not_attempted'],35)
        self.assertTrue(report['unknown_usage'])
        self.assertIsNone(report['passes']['1']['overall']['agreement'])

    def test_wrong_model_stops(self):
        def transport(raw):
            _,response=runner.mock_transport(raw);doc=json.loads(response);doc['model']='jev-other'
            return 200,runner.encode(doc)
        _,report=self.execute(transport)
        self.assertEqual(report['stop_reason'],'model_mismatch')
        self.assertEqual(report['attempted_requests'],1)

    def test_http_failure_and_timeout_stop_without_retries(self):
        for kind in ('http','timeout'):
            calls=[]
            def transport(raw):
                calls.append(raw)
                if kind=='timeout':raise TimeoutError('private error text must not be recorded')
                return 429,b'{"error":"rate limited"}'
            path,report=self.execute(transport)
            self.assertEqual(len(calls),1)
            self.assertEqual(report['request_counts']['not_attempted'],35)
            self.assertTrue(report['unknown_usage'])
            self.assertNotIn('private error text',(path/'attempts.json').read_text())

    def test_interruption_has_preserved_attempt_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'run'
            def transport(raw):raise KeyboardInterrupt()
            with self.assertRaises(KeyboardInterrupt):runner.run(path,transport,'mock')
            runner.verify(path)
            report=json.loads((path/'report.json').read_text())
            self.assertEqual(report['request_counts']['interrupted'],1)
            self.assertEqual(report['request_counts']['not_attempted'],35)

    def test_request_is_saved_before_transport_without_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'run';calls=[]
            def transport(raw):
                calls.append(raw)
                self.assertEqual(raw,(path/f'requests/P1-C01.json').read_bytes())
                self.assertEqual(set(json.loads(raw)),{'model','state','questions'})
                return 401,b'{}'
            runner.run(path,transport,'mock')
            self.assertEqual(len(calls),1)

    def test_budget_reservation_prevents_dispatch(self):
        with patch.object(runner,'CAP',runner.Decimal('0')):
            def transport(raw):self.fail('Must not dispatch')
            _,report=self.execute(transport)
        self.assertEqual(report['attempted_requests'],0)
        self.assertEqual(report['stop_reason'],'budget_reservation')

    def test_live_preflight_required_before_directory_or_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'run'
            with self.assertRaises(ValueError):runner.run(path,lambda _:self.fail(),'live')
            self.assertFalse(path.exists())

    def test_artifact_tampering_and_extra_manifest_detected(self):
        path,_=self.execute(runner.mock_transport)
        (path/'responses/manifest.json').write_text('{}')
        with self.assertRaises(ValueError):runner.verify(path)

    def test_analysis_requires_complete_accounting(self):
        key=json.loads((runner.FOLDER/'reference-key.json').read_text())
        with self.assertRaises(ValueError):summarize(schedule(),[],key,'mock')

    def test_http_transport_official_endpoint_timeout_no_redirect(self):
        captured={}
        class Response:
            status=200
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self):return b'{}'
        class Opener:
            def open(self,request,timeout):
                captured.update(url=request.full_url,method=request.method,body=request.data,timeout=timeout)
                return Response()
        transport=runner.LiveTransport('test-not-secret');transport.opener=Opener()
        self.assertEqual(transport(b'{}'),(200,b'{}'))
        self.assertEqual(captured,{'url':runner.ENDPOINT,'method':'POST','body':b'{}','timeout':30})
        self.assertIsNone(runner.NoRedirect().redirect_request(None,None,302,'',{},'https://example.invalid'))

    def test_preserved_mock_manifest_and_report_reproduction(self):
        path=ROOT/'experiments/jev-cec/execution-v1/mock-001'
        self.assertEqual(runner.verify(path)['mode'],'mock')
        rows=json.loads((path/'schedule.json').read_text())
        records=json.loads((path/'attempts.json').read_text())
        for record in records:
            if record['status']=='valid':
                record['response_raw']=(path/'responses'/f'{record["attempt_id"]}.bin').read_bytes()
        key=json.loads((path/'source/reference-key.json').read_text())
        expected=summarize(rows,records,key,'mock')
        saved=json.loads((path/'report.json').read_text())
        for field,value in expected.items():
            self.assertEqual(saved[field],value)
        self.assertEqual(saved['live_requests_sent'],0)
