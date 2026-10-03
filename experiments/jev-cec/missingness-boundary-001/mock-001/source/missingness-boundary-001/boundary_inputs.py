"""Frozen sources and order-preserving request serialization."""
import importlib.util
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
sys.path.insert(0,str(BASE/'answer-execution-001'))
from eligibility import DIMS,LABELS
spec=importlib.util.spec_from_file_location('boundary_prepare',HERE/'prepare.py')
prep=importlib.util.module_from_spec(spec);spec.loader.exec_module(prep)
encode,sha=prep.encode,prep.sha
FILES=['answer-execution-001/eligibility.py','response-contract-001/ANSWER-CONTRACT.md',
'packet-linkage-001/live-001/requests/P1-V2-12-A-explicit.json']+['missingness-boundary-001/'+n for n in ('PLAN.md','REVIEW.md','REVIEW.json','cards.json','reference.json','candidate-questions.json','prepare.py','boundary_inputs.py','boundary_analysis.py','boundary_run.py')]


def schedule():
    return [{**r,'attempt_id':r['id']} for r in prep.schedule()]


def check():
    f=json.loads((HERE/'freeze.json').read_text())
    if set(f['artifacts'])!=set(FILES):raise ValueError('Freeze set differs')
    for n in FILES:
        if sha((BASE/n).read_bytes())!=f['artifacts'][n]:raise ValueError('Freeze mismatch: '+n)
    return f
