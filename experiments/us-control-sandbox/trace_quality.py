"""Audit mechanical assertions against a separately authored key, not a procedure."""
import json

CHECKS = {'applicable_response_recorded', 'downstream_record_supplied', 'record_fits_objective'}
LABELS = {'supported_effect': 'effect_supported', 'supported_fault': 'fault_supported', 'unresolved': 'unresolved'}


def audit(response, key):
    if not isinstance(response, dict) or response.get('procedure') not in {'checklist', 'trace'}:
        raise ValueError('Invalid procedure response')
    for field in ('unit_id', 'objective', 'packet_digest'):
        if response.get(field) != key[field]:
            raise ValueError('Response identity differs from key')
    if response.get('claim_scope') != key['scope'] or response.get('response') not in LABELS.values():
        raise ValueError('Invalid scope or response label')
    if not isinstance(response.get('reason'), str) or not response['reason'].strip() or not isinstance(response.get('limits'), list) or not response['limits']:
        raise ValueError('Missing rationale or limitations')
    if set(key['checks']) != CHECKS or key['reference'] not in LABELS:
        raise ValueError('Invalid reference key')
    if any(not any(item['state'] is value for value in (True, False, None)) for item in key['checks'].values()):
        raise ValueError('Invalid reference check state')
    entries = response.get('checks')
    if not isinstance(entries, list) or not entries:
        raise ValueError('Missing check assertions')
    seen, correctly_reported = set(), set()
    wrong, bad_locators = 0, 0
    for item in entries:
        if not isinstance(item, dict) or set(item) != {'check', 'satisfied', 'locators'}:
            raise ValueError('Malformed check assertion')
        name = item['check']
        if name not in CHECKS or name in seen:
            raise ValueError('Unknown or duplicate check')
        seen.add(name)
        expected = key['checks'][name]
        same_state = item['satisfied'] is expected['state']
        locators = item['locators']
        valid_locators = (isinstance(locators, list) and bool(locators)
                          and all(isinstance(p, str) for p in locators)
                          and set(locators) == set(expected['locators']))
        wrong += not same_state
        bad_locators += not valid_locators
        if same_state and valid_locators:
            correctly_reported.add(name)
    blockers = {name for name, value in key['checks'].items() if value['state'] is False}
    determinate = response['response'] != 'unresolved'
    expected_outcome = '/downstream' if determinate else None
    if 'outcome_locator' not in response:
        raise ValueError('Missing outcome locator field')
    if not determinate and response['outcome_locator'] is not None:
        raise ValueError('Unresolved response asserts an outcome locator')
    bad_locators += int(determinate and response['outcome_locator'] != expected_outcome)
    if response['procedure'] == 'trace' and 'blockers' not in response:
        raise ValueError('Missing trace blocker list')
    named = response.get('blockers', [])
    if not isinstance(named, list) or any(name not in CHECKS for name in named) or len(set(named)) != len(named):
        raise ValueError('Invalid blocker labels')
    dependent = sum(key['checks'][name]['state'] is None for name in named)
    return {'material_blockers': len(blockers), 'omitted_blockers': len(blockers-correctly_reported),
            'incorrect_assertions': wrong, 'reported_checks': len(entries),
            'locator_errors': bad_locators, 'locator_opportunities': len(entries)+int(determinate),
            'dependent_blocker_labels': dependent,
            'label_matches_key': response['response'] == LABELS[key['reference']],
            'output_bytes': len(json.dumps(response, sort_keys=True, separators=(',', ':')).encode('utf-8'))}


def aggregate(rows):
    names = ('material_blockers', 'omitted_blockers', 'incorrect_assertions', 'reported_checks',
             'locator_errors', 'locator_opportunities', 'dependent_blocker_labels', 'output_bytes')
    total = {name: sum(row[name] for row in rows) for name in names}
    total['units'] = len(rows)
    for name, numerator, denominator in (
        ('omission_rate', 'omitted_blockers', 'material_blockers'),
        ('assertion_error_rate', 'incorrect_assertions', 'reported_checks'),
        ('locator_error_rate', 'locator_errors', 'locator_opportunities')):
        total[name] = total[numerator]/total[denominator] if total[denominator] else None
    return total
