import hashlib
import json
import math
from pathlib import Path
import unittest

BASE=Path(__file__).resolve().parents[1]/'experiments/jev-cec'

class ContractReviewTests(unittest.TestCase):
    def test_located_observations_reproduce(self):
        found=[]
        for name in ('instruction-comparison-001','packet-linkage-001'):
            p=BASE/name/'live-001'
            for a in json.loads((p/'attempts.json').read_text()):
                raw=(p/'responses'/(a['attempt_id']+'.bin')).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(),a['response_sha256'])
                for dim,v in json.loads(raw)['answers'].items():
                    total=sum(v['probabilities'].values())
                    if not math.isclose(total,1,rel_tol=0,abs_tol=1e-5):
                        found.append(dict(archive=name+'/live-001',attempt_id=a['attempt_id'],dimension=dim,sum=total,response_sha256=a['response_sha256']))
        saved=json.loads((BASE/'response-contract-001/observations.json').read_text())['failing_distributions']
        self.assertEqual(found,saved)
        self.assertEqual(len(found),19)
        self.assertEqual(len({(x['archive'],x['attempt_id']) for x in found}),17)

    def test_acceptance_sensitivity_reproduces(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location('cec_sensitivity',BASE/'response-contract-001/sensitivity.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        actual=mod.analyze()
        self.assertEqual(actual,json.loads((BASE/'response-contract-001/sensitivity.json').read_text()))
        for name,expected in [('instruction-comparison-001',(424,466)),('packet-linkage-001',(20,27))]:
            r=actual['archives'][name]
            self.assertEqual((r['whole_response'],r['answer_level']),expected)
            self.assertTrue(all(not x['whole_response'] or x['answer_level'] for x in r['judgments']))
        answer={'type':'choice','choice':'yes','confidence':1.0,'probabilities':{k:float(k=='yes') for k in mod.LABELS}}
        self.assertTrue(mod.accepted(answer))
        answer['probabilities']['yes']=.99
        self.assertFalse(mod.accepted(answer))
        answer['probabilities']['yes']=1.0;answer['confidence']=True
        self.assertFalse(mod.accepted(answer))
        answer['confidence']=float('nan')
        self.assertFalse(mod.accepted(answer))
        answer['confidence']=1.;answer['choice']='no'
        self.assertFalse(mod.accepted(answer))
