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
