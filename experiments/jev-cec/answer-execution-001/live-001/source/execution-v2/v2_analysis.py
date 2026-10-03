"""Descriptive arithmetic against the authored CEC reference; no adjudication."""
from collections import Counter
from v2_inputs import DIMS, LABELS
from v2_execution import validate_response

STATUSES = {'valid', 'invalid', 'http_error', 'transport_error', 'interrupted', 'not_attempted'}


def ratio(n, d):
    return n / d if d else None


def summarize(rows, records, key, mode):
    if len(rows) != 90 or len(records) != 90 or len({r['attempt_id'] for r in rows}) != 90:
        raise ValueError('Complete schedule and accounting required')
    expected = {r['id']: r['judgments'] for r in key}
    outcomes = []
    counts = Counter()
    for row, record in zip(rows, records):
        if row['attempt_id'] != record['attempt_id'] or record['status'] not in STATUSES:
            raise ValueError('Attempt identity or status mismatch')
        counts[record['status']] += 1
        if record['status'] != 'valid':
            continue
        doc = validate_response(record['response_raw'])
        for dim in sorted(DIMS):
            answer = doc['answers'][dim]
            reference = expected[row['card_id']][dim]
            gold = reference['value']
            loss = sum((answer['probabilities'][label] - int(label == gold)) ** 2 for label in sorted(LABELS))
            outcomes.append({'attempt_id': row['attempt_id'], 'card_id': row['card_id'], 'pass': row['pass'],
                             'dimension': dim, 'reference': gold, 'choice': answer['choice'],
                             'brier_loss': loss, 'confidence': answer['confidence'],
                             'probabilities': answer['probabilities'], 'matches_reference': answer['choice'] == gold})

    def metrics(subset, scheduled):
        matrix = {a: {b: 0 for b in sorted(LABELS)} for a in sorted(LABELS)}
        for item in subset:
            matrix[item['reference']][item['choice']] += 1
        matches = sum(x['matches_reference'] for x in subset)
        return {'valid_determinations': len(subset), 'scheduled_determinations': scheduled,
                'coverage': ratio(len(subset), scheduled), 'matches': matches,
                'agreement': ratio(matches, len(subset)),
                'mean_brier_loss': ratio(sum(x['brier_loss'] for x in subset), len(subset)),
                'confusion_reference_by_prediction': matrix,
                'recall': {label: ratio(matrix[label][label], sum(matrix[label].values())) for label in sorted(LABELS)}}

    passes = {}
    for number in range(1, 4):
        group = [x for x in outcomes if x['pass'] == number]
        passes[str(number)] = {'overall': metrics(group, 120), 'by_dimension': {
            dim: metrics([x for x in group if x['dimension'] == dim], 30) for dim in sorted(DIMS)}}
    eligible = same = 0
    for card in sorted({r['card_id'] for r in rows}):
        for dim in sorted(DIMS):
            group = [x for x in outcomes if x['card_id'] == card and x['dimension'] == dim]
            if len(group) == 3:
                eligible += 1
                same += len({x['choice'] for x in group}) == 1
    disagreements = [{**x, 'review_disposition': 'unresolved',
                       'reference_rationale': expected[x['card_id']][x['dimension']]['rationale'],
                       'evidence_ids': expected[x['card_id']][x['dimension']]['evidence_ids']}
                     for x in outcomes if not x['matches_reference']]
    return {'mode': mode, 'interpretation': 'Mock arithmetic only; no Jev findings.' if mode == 'mock' else
            'Agreement with AI-authored public reference; no independent accuracy or human-benefit finding.',
            'scheduled_requests': 90, 'attempted_requests': 90-counts['not_attempted'],
            'request_counts': {s: counts[s] for s in sorted(STATUSES)},
            'determination_counts': {s: counts[s]*4 for s in sorted(STATUSES)},
            'primary_pass': 1, 'passes': passes,
            'repeatability': {'eligible_triplets': eligible, 'scheduled_triplets': 120,
                              'excluded_triplets': 120-eligible, 'all_three_same': same,
                              'agreement': ratio(same, eligible)},
            'determinations': outcomes, 'disagreements': disagreements,
            'duplicate_baseline': ['V2-14-B','V2-15-A'], 'unique_states': 29,
            'pair_contrasts': contrasts(outcomes, expected)}


def contrasts(outcomes, expected):
    lookup={(r['pass'],r['card_id'],r['dimension']):r for r in outcomes}
    result=[]
    for pass_id in (1,2,3):
        for n in range(1,16):
            a,b=f'V2-{n:02}-A',f'V2-{n:02}-B'
            for dim in sorted(DIMS):
                left,right=lookup.get((pass_id,a,dim)),lookup.get((pass_id,b,dim))
                result.append({'pass':pass_id,'cards':[a,b],'dimension':dim,
                    'status':'available' if left and right else 'unavailable',
                    'choices':[left['choice'],right['choice']] if left and right else None,
                    'references':[expected[a][dim]['value'],expected[b][dim]['value']]})
    return result
