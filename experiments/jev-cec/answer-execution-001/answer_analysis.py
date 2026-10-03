"""Prespecified label transitions with unresolved references left unscored."""
from collections import Counter
from answer_inputs import schedule, DIMS
from eligibility import assess
import json
STATUSES = {'valid','partial','invalid','http_error','transport_error','interrupted','not_attempted'}
CARDS = ('V2-12-A', 'V2-12-B')
CONDITIONS = ('original', 'explicit')


def ratio(n, d):
    return n / d if d else None


def summarize(rows, records, key, mode):
    if rows != schedule() or len(records) != 8:
        raise ValueError('Exact schedule and complete accounting required')
    counts = Counter()
    out = []
    for row, record in zip(rows, records):
        if record['attempt_id'] != row['attempt_id'] or record['status'] not in STATUSES:
            raise ValueError('Attempt mismatch')
        counts[record['status']] += 1
        if record['status'] not in ('valid','partial'):
            continue
        eligibility = assess(record['response_raw'])
        if not eligibility['envelope_eligible']:raise ValueError('Envelope mismatch')
        response = json.loads(record['response_raw'])
        for dimension in sorted(DIMS):
            if not eligibility['answers'][dimension]['eligible']:continue
            answer = response['answers'][dimension]
            reference = key['conditions'][row['condition']][row['card_id']][dimension]['label']
            out.append(dict(attempt_id=row['attempt_id'], pass_id=row['pass'],
                card_id=row['card_id'], condition=row['condition'], dimension=dimension,
                choice=answer['choice'], reference=reference,
                matches_reference=None if reference is None else answer['choice']==reference,
                probabilities=answer['probabilities'], confidence=answer['confidence']))
    lookup = {(x['pass_id'], x['card_id'], x['condition'], x['dimension']): x for x in out}
    passes = {}
    for pass_id in (1, 2):
        transitions = []
        for card in CARDS:
            a = lookup.get((pass_id, card, 'original', 'action'))
            b = lookup.get((pass_id, card, 'explicit', 'action'))
            transitions.append(dict(card_id=card, available=bool(a and b),
                original=a['choice'] if a else None, explicit=b['choice'] if b else None))
        metrics = {}
        for condition in CONDITIONS:
            metrics[condition] = {}
            for dimension in sorted(DIMS):
                items = [x for x in out if x['pass_id']==pass_id and x['condition']==condition and x['dimension']==dimension]
                unscored = condition == 'original' and dimension == 'action'
                matches = None if unscored else sum(x['matches_reference'] for x in items)
                metrics[condition][dimension] = dict(valid=len(items), scheduled=2,
                    coverage=len(items)/2, matches=matches,
                    agreement=None if unscored else ratio(matches, len(items)))
        eligible = sum(x['available'] for x in transitions)
        passes[str(pass_id)] = dict(action_transitions=transitions, eligible=eligible,
            unavailable=2-eligible, scheduled_pairs=2, by_dimension=metrics)
    repetition = {}
    for condition in CONDITIONS:
        eligible = same = 0
        for card in CARDS:
            a = lookup.get((1, card, condition, 'action'))
            b = lookup.get((2, card, condition, 'action'))
            if a and b:
                eligible += 1
                same += a['choice'] == b['choice']
        repetition[condition] = dict(eligible=eligible, excluded=2-eligible,
            scheduled=2, same=same, agreement=ratio(same, eligible))
    return dict(mode=mode, interpretation='Mock plumbing only' if mode=='mock' else 'Exposed packet-clarification diagnostic; no independent accuracy claim',
        scheduled_requests=8, attempted_requests=8-counts['not_attempted'],
        request_counts={s:counts[s] for s in sorted(STATUSES)},
        eligibility_counts={'eligible':len(out),'excluded':32-len(out),'scheduled':32},
        whole_response_eligible_judgments=4*counts['valid'],
        primary_pass=1, passes=passes, repetition=repetition, determinations=out)
