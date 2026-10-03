"""Offline, answer-free request preparation. No transport or inference."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
DIMS = {'action', 'propagation', 'trajectory_effect', 'outcome_mitigation'}

def requests(root=ROOT):
    questions = json.loads((root/'standard-001/questions.json').read_text())
    if set(questions) != DIMS:
        raise ValueError('Four dimensions required')
    seen = set()
    for folder in (root, root/'expansion-001'):
        for card in json.loads((folder/'cards.json').read_text()):
            if set(card) != {'id','pair_id','synthetic','scope','evidence'}:
                raise ValueError('Unexpected card field')
            if card['synthetic'] is not True or card['id'] in seen:
                raise ValueError('Synthetic unique cards required')
            if not card['evidence'] or any(set(e) != {'id','text'} for e in card['evidence']):
                raise ValueError('Unexpected evidence fields')
            if set(card['scope']) != {'objective','targets','trajectory','consequence','interval'}:
                raise ValueError('Unexpected scope fields')
            seen.add(card['id'])
            yield card['id'], {'model':'jev-1.13.0','state':{k:card[k] for k in ('synthetic','scope','evidence')},'questions':questions}

def prepare(output, root=ROOT):
    prepared = list(requests(root))
    output.mkdir(parents=True, exist_ok=False)
    index=[]
    for n,(card_id,request) in enumerate(prepared,1):
        raw=(json.dumps(request,sort_keys=True,indent=2)+'\n').encode()
        name=f'request-{n:02}.json'
        (output/name).write_bytes(raw)
        index.append({'card_id':card_id,'file':name,'sha256':hashlib.sha256(raw).hexdigest()})
    (output/'index.json').write_text(json.dumps({'status':'offline_unfrozen','requests':index},indent=2)+'\n')

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    prepare(parser.parse_args().output)
