"""Answer-free two-condition offline preparation; no transport."""
import argparse
import importlib.util
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
spec=importlib.util.spec_from_file_location('comparison_v2_inputs',BASE/'execution-v2/v2_inputs.py')
v2=importlib.util.module_from_spec(spec);spec.loader.exec_module(v2)

def schedule():
    v2.check()
    original=[r for r in v2.schedule() if r['pass']==1]
    candidate=json.loads((HERE/'candidate-questions.json').read_text())
    baseline=original[0]['payload']['questions']
    if set(candidate)!=set(baseline):raise ValueError('Question IDs changed')
    for d in baseline:
        if set(candidate[d])!=set(baseline[d]) or any(candidate[d][k]!=baseline[d][k] for k in baseline[d] if k!='instructions'):
            raise ValueError('Only instructions may change')
    rows=[]
    for pass_id in (1,2):
        for index,row in enumerate(original):
            order=('A','B') if (index+pass_id)%2 else ('B','A')
            for condition in order:
                payload={**row['payload'],'questions':baseline if condition=='A' else candidate}
                rows.append({'attempt_id':f'P{pass_id}-{row["card_id"]}-{condition}',
                    'pass':pass_id,'card_id':row['card_id'],'condition':condition,
                    'payload':payload,'payload_sha256':v2.sha(v2.encode(payload))})
    return rows

def prepare(output):
    rows=schedule()
    output.mkdir(parents=True,exist_ok=False)
    (output/'schedule.json').write_bytes(v2.encode(rows))
    artifacts={str(p.relative_to(BASE)):v2.sha(p.read_bytes()) for p in [HERE/'PLAN.md',HERE/'candidate-questions.json',HERE/'prepare.py',BASE/'execution-v2/freeze.json']}
    (output/'manifest.json').write_bytes(v2.encode({'status':'offline_not_execution_freeze','requests_sent':0,'scheduled_requests':len(rows),'scheduled_determinations':len(rows)*4,'artifacts':artifacts,'schedule_sha256':v2.sha((output/'schedule.json').read_bytes())}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    prepare(parser.parse_args().output)
