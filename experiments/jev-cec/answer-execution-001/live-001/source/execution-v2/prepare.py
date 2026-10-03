"""Offline four-question schedule; deliberately no live transport."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'development-v2'
spec=importlib.util.spec_from_file_location('standard_preparer',ROOT/'prepare_standard.py')
standard=importlib.util.module_from_spec(spec);spec.loader.exec_module(standard)

def schedule():
    requests=list(standard.requests())
    questions=json.loads((ROOT/'standard-001/questions.json').read_text())
    for card in json.loads((ROOT/'prevention-001/cards.json').read_text()):
        if set(card)!={'id','pair_id','synthetic','scope','evidence'} or card['synthetic'] is not True:
            raise ValueError('Unexpected prevention card')
        if set(card['scope'])!={'objective','targets','trajectory','consequence','interval'} or any(set(e)!={'id','text'} for e in card['evidence']):
            raise ValueError('Unexpected state field')
        requests.append((card['id'],{'model':'jev-1.13.0','state':{k:card[k] for k in ('synthetic','scope','evidence')},'questions':questions}))
    if len(requests)!=30 or len({i for i,r in requests})!=30:
        raise ValueError('Expected thirty unique card identifiers')
    rows=[]
    for pass_id in range(1,4):
        for card_id,request in sorted(requests):
            raw=(json.dumps(request,sort_keys=True,indent=2)+'\n').encode()
            rows.append(dict(attempt_id=f'P{pass_id}-{card_id}',pass_id=pass_id,card_id=card_id,request_sha256=hashlib.sha256(raw).hexdigest(),request=request))
    return rows

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output
    rows=schedule()
    out.mkdir(parents=True,exist_ok=False)
    (out/'schedule.json').write_text(json.dumps({'status':'offline_not_frozen','rows':rows},indent=2)+'\n')
