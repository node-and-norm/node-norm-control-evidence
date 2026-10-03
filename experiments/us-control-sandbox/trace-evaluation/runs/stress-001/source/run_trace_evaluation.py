"""Save procedure outputs before opening an author-exposed reference key."""
import argparse
import hashlib
import json
from pathlib import Path
from paired_procedures import checklist, trace
from trace_quality import audit, aggregate
from evaluate_evidence import evaluate

ROOT = Path(__file__).resolve().parent

def dump(path, obj):
    path.write_text(json.dumps(obj,indent=2)+'\n')

def run(output, plan_commit, implementation_commit):
    output.mkdir(parents=True, exist_ok=False)
    try:
        inputs_path = ROOT/'trace-evaluation/inputs.json'
        raw = inputs_path.read_bytes()
        (output/'inputs.json').write_bytes(raw)
        inputs = json.loads(raw)
        ids = [item['unit_id'] for item in inputs]
        if len(set(ids)) != len(ids): raise ValueError('Duplicate input unit')
        records = []
        for envelope in inputs:
            row = {'unit_id':envelope['unit_id']}
            for name, procedure in (('checklist', checklist), ('trace', trace)):
                try:
                    row[name] = {'status':'responded','output':procedure(envelope)}
                except ValueError as error:
                    row[name] = {'status':'rejected','reason':str(error)}
            records.append(row)
        dump(output/'responses-before-key.json', records)
        # Only now does the runner open the reference key.
        key_bytes = (ROOT/'trace-evaluation/reference-key.json').read_bytes()
        (output/'reference-key.json').write_bytes(key_bytes)
        keys = json.loads(key_bytes)
        key = {item['unit_id']:item for item in keys}
        if len(key) != len(keys) or set(key) != set(ids): raise ValueError('Key/input cohort mismatch')
        if any(k['admission'] not in ('valid','excluded') for k in keys): raise ValueError('Unknown admission state')
        rows = {name:[] for name in ('checklist','trace')}
        labels = {name:[] for name in rows}
        valid_key = [{'unit_id':k['unit_id'],'reference':k['reference']} for k in keys if k['admission']=='valid']
        intake_failures = []
        for record in records:
            k = key[record['unit_id']]
            for name in rows:
                response = record[name]
                if (k['admission']=='excluded') != (response['status']=='rejected'):
                    intake_failures.append({'unit_id':k['unit_id'],'procedure':name})
                if k['admission']=='valid' and response['status']=='responded':
                    metrics = audit(response['output'], k)
                    rows[name].append({'unit_id':k['unit_id'],'stratum':k['stratum'],**metrics})
                    labels[name].append({'unit_id':k['unit_id'],'response':response['output']['response']})
        if intake_failures:
            dump(output/'intake-failures.json',intake_failures)
            raise ValueError('Unexpected intake result prevents clean comparison')
        totals = {name:aggregate(value) for name,value in rows.items()}
        report = {'status':'author-exposed technical stress evaluation; no independent validation',
                  'plan_commit':plan_commit,'pre_run_commit':implementation_commit,
                  'intake':{'total':len(inputs),'valid':len(valid_key),'excluded':len(keys)-len(valid_key),'unexpected':0},
                  'mechanical_audit':totals, 'per_unit':rows,
                  'label_arithmetic':{name:evaluate(valid_key, labels[name]) for name in labels},
                  'added_trace_bytes':totals['trace']['output_bytes']-totals['checklist']['output_bytes'],
                  'added_trace_checks':totals['trace']['reported_checks']-totals['checklist']['reported_checks'],
                  'limitations':['Constructed packet content, not independently observed execution.',
                      'Key and procedures share author exposure and contract assumptions.',
                      'Coverage difference is expected from the output design.',
                      'Bytes are not a measure of human reading burden or value.']}
        dump(output/'report.json', report)
        source = output/'source'; source.mkdir()
        for name in ('paired_procedures.py','build_evidence_appendices.py','trace_quality.py','run_trace_evaluation.py','evaluate_evidence.py','evaluation_rules.json'):
            (source/name).write_bytes((ROOT/name).read_bytes())
        for name in ('PLAN.md','build_inputs.py'):
            (source/name).write_bytes((ROOT/'trace-evaluation'/name).read_bytes())
        hashes = {str(p.relative_to(output)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.rglob('*')) if p.is_file()}
        dump(output/'manifest.json', {'status':'author-exposed evaluation record','artifacts':hashes})
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        dump(output/'failure.json',{'status':'failed evaluation attempt','error':str(error)})
        return 1

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--plan-commit',required=True)
    parser.add_argument('--implementation-commit',required=True)
    args=parser.parse_args()
    raise SystemExit(run(args.output,args.plan_commit,args.implementation_commit))
