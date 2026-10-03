"""Source binding for the prospective instruction comparison."""
import importlib.util
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
sys.path.insert(0,str(BASE/'execution-v2'))
import v2_inputs
from v2_inputs import encode,sha,DIMS,LABELS
FILES=v2_inputs.FILES+['execution-v2/freeze.json']+['instruction-comparison-001/'+n for n in ('PLAN.md','candidate-questions.json','prepare.py','comparison_inputs.py','comparison_analysis.py','comparison_run.py')]

def schedule():
    spec=importlib.util.spec_from_file_location('comparison_schedule',HERE/'prepare.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod.schedule()

def check():
    v2_inputs.check()
    freeze=json.loads((HERE/'freeze.json').read_text())
    if set(freeze['artifacts'])!=set(FILES):raise ValueError('Freeze file set differs')
    for name in FILES:
        if sha((BASE/name).read_bytes())!=freeze['artifacts'][name]:raise ValueError('Freeze mismatch: '+name)
    return freeze
