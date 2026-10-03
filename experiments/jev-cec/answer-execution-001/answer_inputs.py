"""Exact source binding for the packet-linkage execution."""
import importlib.util
import json
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE / 'execution-v2'))
import v2_inputs
from v2_inputs import encode, sha, DIMS, LABELS
FILES = v2_inputs.FILES + ['execution-v2/freeze.json'] + [
    'instruction-comparison-001/live-001/requests/P1-' + card + '-A.json'
    for card in ('V2-12-A', 'V2-12-B')
] + ['packet-linkage-001/' + name for name in (
    'PLAN.md', 'reference.json', 'source-bindings.json', 'prepare.py',
    'linkage_inputs.py', 'linkage_run.py', 'linkage_analysis.py')]


FILES += ['response-contract-001/ANSWER-CONTRACT.md'] + ['answer-execution-001/'+n for n in ('PLAN.md','answer_inputs.py','answer_run.py','answer_analysis.py','eligibility.py')]


def schedule():
    spec = importlib.util.spec_from_file_location('linkage_prepare', BASE / 'packet-linkage-001/prepare.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.schedule()


def check():
    v2_inputs.check()
    freeze = json.loads((HERE / 'freeze.json').read_text())
    if set(freeze['artifacts']) != set(FILES):
        raise ValueError('Freeze file set differs')
    for name in FILES:
        if sha((BASE / name).read_bytes()) != freeze['artifacts'][name]:
            raise ValueError('Freeze mismatch: ' + name)
    return freeze
