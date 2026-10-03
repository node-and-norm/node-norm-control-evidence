"""Development-only agreement and dependent factorial edges."""
from collections import Counter
import json
from boundary_inputs import schedule,encode,DIMS
from eligibility import assess
STATUSES={'valid','partial','invalid','http_error','transport_error','interrupted','not_attempted'}
FACTORS=('propagation','trajectory_effect','outcome_mitigation')
CONDITIONS=('shared','structured')


def fraction(n,d):return n/d if d else None


def summarize(rows,records,key,mode):
    if encode(rows)!=encode(schedule()) or len(records)!=32:raise ValueError('Exact ordered schedule required')
    refs={r['id']:r['judgments'] for r in key['cards']}
    if len(refs)!=8:raise ValueError('Expected eight references')
    counts=Counter();out=[]
    for row,r in zip(rows,records):
        if r['attempt_id']!=row['attempt_id'] or r['status'] not in STATUSES:raise ValueError('Attempt mismatch')
        counts[r['status']]+=1
        if r['status'] not in ('valid','partial'):continue
        assessment=assess(r['response_raw']);doc=json.loads(r['response_raw'])
        if not assessment['envelope_eligible']:raise ValueError('Envelope mismatch')
        n=sum(a['eligible'] for a in assessment['answers'].values())
        if r['status']!=('valid' if n==4 else 'partial' if n else 'invalid'):raise ValueError('Eligibility status mismatch')
        for d in sorted(DIMS):
            if not assessment['answers'][d]['eligible']:continue
            a=doc['answers'][d];ref=refs[row['card_id']][d]['label']
            out.append(dict(attempt_id=r['attempt_id'],card_id=row['card_id'],condition=row['condition'],order=row['order'],dimension=d,choice=a['choice'],reference=ref,matches_reference=None if ref is None else a['choice']==ref,probabilities=a['probabilities'],confidence=a['confidence']))
    lookup={(x['order'],x['condition'],x['card_id'],x['dimension']):x for x in out}
    # Packet design is a full three-factor binary cube, so exactly twelve edges.
    edges=[]
    cards=sorted(refs)
    for i,a in enumerate(cards):
        for b in cards[i+1:]:
            differences=[d for d in FACTORS if refs[a][d]['label']!=refs[b][d]['label']]
            if len(differences)==1:edges.append((a,b,differences[0]))
    if len(edges)!=12:raise ValueError('Expected twelve factorial edges')
    orders={}
    for order in ('canonical','reversed'):
        conditions={}
        for condition in CONDITIONS:
            metrics={}
            for d in sorted(DIMS):
                items=[x for x in out if x['order']==order and x['condition']==condition and x['dimension']==d]
                scored=[x for x in items if x['reference'] is not None]
                matches=sum(x['matches_reference'] for x in scored)
                metrics[d]=dict(scheduled=8,eligible=len(items),scorable=len(scored),matches=matches,agreement=fraction(matches,len(scored)))
            edge_records=[]
            for a,b,d in edges:
                x=lookup.get((order,condition,a,d));y=lookup.get((order,condition,b,d))
                target=bool(x and y);other=[(lookup.get((order,condition,a,k)),lookup.get((order,condition,b,k))) for k in sorted(DIMS-{d})]
                stable_available=all(u and v for u,v in other)
                edge_records.append(dict(cards=[a,b],target_dimension=d,target_eligible=target,
                    target_choices=[x['choice'],y['choice']] if target else None,
                    target_matches_proposals=(x['matches_reference'] and y['matches_reference']) if target and x['reference'] is not None and y['reference'] is not None else None,
                    unrelated_eligible=stable_available,unrelated_changes=sum(u['choice']!=v['choice'] for u,v in other) if stable_available else None))
            conditions[condition]=dict(by_dimension=metrics,edges=edge_records,
                target_edges_eligible=sum(e['target_eligible'] for e in edge_records),
                unrelated_edges_eligible=sum(e['unrelated_eligible'] for e in edge_records),scheduled_edges=12)
        paired=[]
        for card in cards:
            for d in sorted(DIMS):
                a=lookup.get((order,'shared',card,d));b=lookup.get((order,'structured',card,d))
                category='unavailable' if not a or not b else 'unscored' if a['reference'] is None or b['reference'] is None else 'both' if a['matches_reference'] and b['matches_reference'] else 'shared_only' if a['matches_reference'] else 'structured_only' if b['matches_reference'] else 'neither'
                paired.append(dict(card_id=card,dimension=d,category=category))
        orders[order]={'conditions':conditions,'paired':paired,'paired_counts':dict(Counter(x['category'] for x in paired)),'scheduled_pairs':32}
    return dict(mode=mode,interpretation='Mock plumbing only' if mode=='mock' else 'Exposed missingness development comparison; dependent edges, no independent accuracy',scheduled_requests=32,attempted_requests=32-counts['not_attempted'],request_counts={s:counts[s] for s in sorted(STATUSES)},eligibility_counts={'eligible':len(out),'excluded':128-len(out),'scheduled':128},whole_response_eligible_judgments=4*counts['valid'],primary_order='canonical',orders=orders,determinations=out)
