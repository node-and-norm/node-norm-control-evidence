"""Answer contract 001; reasons are data, not evidence labels."""
import json
import math
MODEL='jev-1.13.0'
DIMS={'action','propagation','trajectory_effect','outcome_mitigation'}
LABELS={'yes','no','partial','conflicting','unknown','not_reported','not_observable','not_applicable'}


def unique(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise ValueError('duplicate key')
        out[k]=v
    return out


def reject_constant(value):raise ValueError('nonfinite JSON constant')


def assess(raw,status=200):
    invalid={'envelope_eligible':False,'envelope_reasons':['envelope_invalid'],'answers':{}}
    try:doc=json.loads(raw,object_pairs_hook=unique,parse_constant=reject_constant)
    except (ValueError,UnicodeDecodeError):return invalid
    if not isinstance(doc,dict) or status!=200 or doc.get('model')!=MODEL:return invalid
    answers=doc.get('answers');usage=doc.get('usage')
    if not isinstance(answers,dict) or set(answers)!=DIMS or not isinstance(usage,dict):return invalid
    if any(type(usage.get(k)) is not int or usage[k]<0 for k in ('input_tokens','output_tokens')):return invalid
    result={'envelope_eligible':True,'envelope_reasons':[],'answers':{}}
    for dim,a in answers.items():
        reasons=[];total=None
        if not isinstance(a,dict) or a.get('type')!='choice':reasons.append('answer_shape')
        if isinstance(a,dict):
            p=a.get('probabilities');choice=a.get('choice')
            labels=isinstance(p,dict) and set(p)==LABELS
            if not labels or not isinstance(choice,str) or choice not in LABELS:reasons.append('label_coverage')
            numeric=labels and all(type(v) in (int,float) and math.isfinite(v) and 0<=v<=1 for v in [a.get('confidence'),*p.values()])
            if not numeric:reasons.append('numeric_range')
            if numeric:
                total=sum(p.values())
                if not math.isclose(total,1,rel_tol=0,abs_tol=1e-5):reasons.append('sum_outside_tolerance')
                if isinstance(choice,str) and choice in LABELS and p[choice]<max(p.values()):reasons.append('choice_not_maximum')
        result['answers'][dim]={'eligible':not reasons,'reasons':reasons,'raw_sum':total,'sum_discrepancy':None if total is None else total-1}
    return result
