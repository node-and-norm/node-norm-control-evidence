"""Offline schedule; packet factors and instruction/order factors stay separate."""
import argparse
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'packet-linkage-001/live-001/requests/P1-V2-12-A-explicit.json'


def encode(x):return (json.dumps(x,indent=2,sort_keys=False)+'\n').encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()


def schedule():
    base=json.loads(SOURCE.read_text())
    cards=json.loads((HERE/'cards.json').read_text())
    candidate=json.loads((HERE/'candidate-questions.json').read_text())
    rows=[]
    for order in ('canonical','reversed'):
        for i,card in enumerate(cards):
            conditions=('shared','structured') if i%2==0 else ('structured','shared')
            if order=='reversed':conditions=tuple(reversed(conditions))
            for condition in conditions:
                questions=json.loads(json.dumps(base['questions'] if condition=='shared' else candidate))
                for q in questions.values():
                    names=sorted(q['criteria'],reverse=order=='reversed')
                    q['criteria']={name:q['criteria'][name] for name in names}
                payload={'model':base['model'],'questions':questions,'state':card['state']}
                rows.append({'id':f'{order}-{card["id"]}-{condition}','card_id':card['id'],'condition':condition,'order':order,'payload':payload,'payload_sha256':sha(encode(payload))})
    return rows


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=False)
    rows=schedule();(args.output/'schedule.json').write_bytes(encode(rows))
    (args.output/'manifest.json').write_bytes(encode({'status':'offline_not_execution_freeze','requests_sent':0,'scheduled_requests':len(rows),'source_request_sha256':sha(SOURCE.read_bytes()),'source_hashes':{n:sha((HERE/n).read_bytes()) for n in ('PLAN.md','prepare.py','cards.json','reference.json','candidate-questions.json')},'schedule_sha256':sha((args.output/'schedule.json').read_bytes())}))
