"""Post-output coverage sensitivity only; no label accuracy or normalization."""
import hashlib
import json
import math
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
LABELS={'yes','no','partial','conflicting','unknown','not_reported','not_observable','not_applicable'}
DIMS={'action','propagation','trajectory_effect','outcome_mitigation'}


def accepted(answer):
    if not isinstance(answer,dict) or answer.get('type')!='choice':return False
    p=answer.get('probabilities');choice=answer.get('choice')
    if not isinstance(p,dict) or set(p)!=LABELS or not isinstance(choice,str) or choice not in LABELS:return False
    if any(type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=1 for v in [answer.get('confidence'),*p.values()]):return False
    return math.isclose(sum(p.values()),1,rel_tol=0,abs_tol=1e-5) and p[choice]==max(p.values())


def analyze():
    archives={}
    for name in ('instruction-comparison-001','packet-linkage-001'):
        folder=BASE/name/'live-001'
        rows=json.loads((folder/'schedule.json').read_text())
        attempts=json.loads((folder/'attempts.json').read_text())
        assert len(rows)==len(attempts)
        details=[];groups={}
        for row,a in zip(rows,attempts):
            assert row['attempt_id']==a['attempt_id']
            raw=(folder/'responses'/(a['attempt_id']+'.bin')).read_bytes()
            assert hashlib.sha256(raw).hexdigest()==a['response_sha256']
            doc=json.loads(raw)
            envelope=(a['http_status']==200 and doc.get('model')=='jev-1.13.0' and set(doc.get('answers',{}))==DIMS and all(type(doc.get('usage',{}).get(k)) is int and doc['usage'][k]>=0 for k in ('input_tokens','output_tokens')))
            group=groups.setdefault(f"pass_{row['pass']}/{row['condition']}",{'scheduled':0,'whole_response':0,'answer_level':0})
            for d in sorted(DIMS):
                whole=a['status']=='valid';single=envelope and accepted(doc['answers'][d])
                group['scheduled']+=1;group['whole_response']+=whole;group['answer_level']+=single
                details.append({'attempt_id':a['attempt_id'],'dimension':d,'whole_response':whole,'answer_level':single,'response_sha256':a['response_sha256']})
        archives[name]={'scheduled':len(details),'whole_response':sum(x['whole_response'] for x in details),'answer_level':sum(x['answer_level'] for x in details),'groups':groups,'judgments':details}
    return {'scope':'Post-output coverage sensitivity; tolerance unchanged at 1e-5; no rescoring or probability repair','archives':archives}


if __name__=='__main__':print(json.dumps(analyze(),indent=2,sort_keys=True))
