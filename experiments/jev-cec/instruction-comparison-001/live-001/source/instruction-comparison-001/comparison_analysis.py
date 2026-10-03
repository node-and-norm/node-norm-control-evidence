"""Paired descriptive arithmetic; no independent accuracy inference."""
from collections import Counter
from comparison_inputs import DIMS,LABELS,schedule
from v2_execution import validate_response
STATUSES={'valid','invalid','http_error','transport_error','interrupted','not_attempted'}
SECONDARY={'direct_evidence':[('V2-04-B','propagation'),('V2-14-A','propagation'),('V2-14-A','trajectory_effect')],
           'disputed_reference':[('V2-12-A','action'),('V2-12-B','action'),('V2-15-B','outcome_mitigation')]}
def ratio(n,d):return n/d if d else None

def metrics(items,n):
    matrix={a:{b:0 for b in sorted(LABELS)} for a in sorted(LABELS)}
    for x in items:matrix[x['reference']][x['choice']]+=1
    matches=sum(x['matches_reference'] for x in items)
    return dict(valid=len(items),scheduled=n,coverage=ratio(len(items),n),matches=matches,agreement=ratio(matches,len(items)),
        mean_brier_loss=ratio(sum(x['brier_loss'] for x in items),len(items)),confusion=matrix,
        recall={k:ratio(matrix[k][k],sum(matrix[k].values())) for k in sorted(LABELS)})

def summarize(rows,records,key,mode):
    expected_rows=schedule()
    if rows!=expected_rows or len(records)!=120:raise ValueError('Exact schedule and complete accounting required')
    reference={r['id']:r['judgments'] for r in key}
    counts=Counter();out=[]
    for row,record in zip(rows,records):
        if record['attempt_id']!=row['attempt_id'] or record['status'] not in STATUSES:raise ValueError('Attempt mismatch')
        counts[record['status']]+=1
        if record['status']!='valid':continue
        doc=validate_response(record['response_raw'])
        for d in sorted(DIMS):
            answer=doc['answers'][d];gold=reference[row['card_id']][d]['value']
            out.append(dict(attempt_id=row['attempt_id'],card_id=row['card_id'],condition=row['condition'],pass_id=row['pass'],dimension=d,
                choice=answer['choice'],reference=gold,matches_reference=answer['choice']==gold,
                probabilities=answer['probabilities'],confidence=answer['confidence'],
                brier_loss=sum((answer['probabilities'][k]-int(k==gold))**2 for k in sorted(LABELS))))
    lookup={(x['pass_id'],x['card_id'],x['dimension'],x['condition']):x for x in out}
    pairs=[];passes={}
    for p in (1,2):
        group=[]
        for card in sorted(reference):
            for d in sorted(DIMS):
                a,b=lookup.get((p,card,d,'A')),lookup.get((p,card,d,'B'))
                category='unavailable' if not a or not b else ('both_match' if a['matches_reference'] and b['matches_reference'] else 'A_only' if a['matches_reference'] else 'B_only' if b['matches_reference'] else 'neither_match')
                group.append(dict(pass_id=p,card_id=card,dimension=d,category=category,choices=[a['choice'],b['choice']] if a and b else None))
        pairs+=group;c=Counter(x['category'] for x in group);eligible=120-c['unavailable']
        passes[str(p)]={'conditions':{condition:metrics([x for x in out if x['pass_id']==p and x['condition']==condition],120) for condition in ('A','B')},
            'paired':dict(counts={k:c[k] for k in ('both_match','A_only','B_only','neither_match','unavailable')},eligible=eligible,scheduled=120,agreement_difference=ratio(c['B_only']-c['A_only'],eligible)),
            'by_dimension':{condition:{d:metrics([x for x in out if x['pass_id']==p and x['condition']==condition and x['dimension']==d],30) for d in sorted(DIMS)} for condition in ('A','B')},
            'secondary':{name:{condition:metrics([x for x in out if x['pass_id']==p and x['condition']==condition and (x['card_id'],x['dimension']) in members],len(members)) for condition in ('A','B')} for name,members in SECONDARY.items()}}
    repetition={}
    for condition in ('A','B'):
        eligible=same=0
        for card in reference:
            for d in DIMS:
                a,b=lookup.get((1,card,d,condition)),lookup.get((2,card,d,condition))
                if a and b:eligible+=1;same+=a['choice']==b['choice']
        repetition[condition]=dict(eligible=eligible,excluded=120-eligible,same=same,agreement=ratio(same,eligible))
    disagreements=[{**x,'review_disposition':'unresolved','evidence_ids':reference[x['card_id']][x['dimension']]['evidence_ids'],'reference_rationale':reference[x['card_id']][x['dimension']]['rationale']} for x in out if not x['matches_reference']]
    return dict(mode=mode,interpretation='Mock plumbing only' if mode=='mock' else 'Exposed instruction-package comparison; no independent accuracy or length-only effect',scheduled_requests=120,attempted_requests=120-counts['not_attempted'],request_counts={s:counts[s] for s in sorted(STATUSES)},determination_counts={s:counts[s]*4 for s in sorted(STATUSES)},primary_pass=1,passes=passes,paired_records=pairs,repetition=repetition,determinations=out,disagreements=disagreements,unique_states=29,duplicate_baseline=['V2-14-B','V2-15-A'])
