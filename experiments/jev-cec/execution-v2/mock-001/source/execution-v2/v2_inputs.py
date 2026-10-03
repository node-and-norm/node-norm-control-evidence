"""Exact-source freeze and answer-free request schedule for v2."""
import hashlib
import importlib.util
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
HERE=BASE/'execution-v2'
DIMS={'action','propagation','trajectory_effect','outcome_mitigation'}
LABELS={'yes','no','partial','conflicting','unknown','not_reported','not_observable','not_applicable'}
FILES=[
    'execution-v2/'+n for n in ('v2_inputs.py','v2_execution.py','v2_analysis.py','v2_run.py','prepare.py','reference-key.json','PROTOCOL.md')
]+['development-v2/'+n for n in (
    'prepare_standard.py','cards.json','proposed-reference.json','README.md',
    'standard-001/questions.json','standard-001/DECISION.md',
    'expansion-001/cards.json','expansion-001/proposed-reference.json','expansion-001/reference-review.json','expansion-001/README.md',
    'prevention-001/cards.json','prevention-001/proposed-reference.json','prevention-001/README.md')]

def encode(value):return (json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()

def schedule():
    spec=importlib.util.spec_from_file_location('v2_schedule_prepare',HERE/'prepare.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return [{'attempt_id':r['attempt_id'],'pass':r['pass_id'],'card_id':r['card_id'],'payload':r['request']} for r in module.schedule()]

def check():
    freeze=json.loads((HERE/'freeze.json').read_text())
    if set(freeze['artifacts'])!=set(FILES):raise ValueError('Freeze file set differs')
    for name in FILES:
        if sha((BASE/name).read_bytes())!=freeze['artifacts'][name]:raise ValueError('Freeze mismatch: '+name)
    rows=schedule();key=json.loads((HERE/'reference-key.json').read_text())
    cards={r['card_id']:r['payload']['state'] for r in rows}
    if len(key)!=30 or {r['id'] for r in key}!=set(cards):raise ValueError('Reference coverage')
    for r in key:
        if set(r['judgments'])!=DIMS:raise ValueError('Reference dimensions')
        for j in r['judgments'].values():
            if j['value'] not in LABELS or not j['rationale'] or not j['evidence_ids'] or not set(j['evidence_ids']) <= {e['id'] for e in cards[r['id']]['evidence']}:raise ValueError('Reference evidence')
    return freeze
