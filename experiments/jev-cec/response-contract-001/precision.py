"""Offline representation audit; hypothetical rounding never changes eligibility."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent


def audit():
    result={}
    for name in ('instruction-comparison-001','packet-linkage-001'):
        folder=BASE/name/'live-001'
        rows=[]
        for attempt in json.loads((folder/'attempts.json').read_text()):
            raw=(folder/'responses'/(attempt['attempt_id']+'.bin')).read_bytes()
            if hashlib.sha256(raw).hexdigest()!=attempt['response_sha256']:
                raise ValueError('Response hash mismatch')
            doc=json.loads(raw,parse_float=Decimal)
            for dimension,answer in doc['answers'].items():
                values=[Decimal(v) for v in answer['probabilities'].values()]
                total=sum(values)
                rows.append({'attempt_id':attempt['attempt_id'],'dimension':dimension,
                    'sum_decimal':str(total),'strict_sum_pass':abs(total-1)<=Decimal('.00001'),
                    'near_cent_grid':all(abs(v-v.quantize(Decimal('.01')))<=Decimal('1e-12') for v in values),
                    'response_sha256':attempt['response_sha256']})
        result[name]={'distributions':len(rows),'strict_sum_failures':sum(not r['strict_sum_pass'] for r in rows),
            'near_cent_grid':sum(r['near_cent_grid'] for r in rows),'records':rows}
    return {'scope':'Exact decimal parsing of saved JSON number tokens; no normalization, eligibility change or accuracy scoring', 'archives':result}


if __name__=='__main__':print(json.dumps(audit(),indent=2,sort_keys=True))
