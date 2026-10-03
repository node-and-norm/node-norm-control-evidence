"""Two presentations of one technical evidence contract; no method scores."""
import hashlib
import json
from build_evidence_appendices import appendix

VERSION = 'paired-record-procedures/0.1'
OBJECTIVES = {'recorded_stop', 'at_most_one_effect', 'recorded_delivery'}


def digest(packet):
    return hashlib.sha256(json.dumps(packet, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def facts(envelope):
    if not isinstance(envelope, dict) or set(envelope) != {'unit_id', 'objective', 'scope', 'packet', 'packet_digest'}:
        raise ValueError('Unexpected envelope fields')
    if not isinstance(envelope['unit_id'], str) or not envelope['unit_id'].strip():
        raise ValueError('Missing unit ID')
    if not isinstance(envelope['objective'], str) or envelope['objective'] not in OBJECTIVES:
        raise ValueError('Undefined objective')
    if envelope['scope'] != 'single-authored-packet-terminal-record':
        raise ValueError('Unsupported scope; execution inference is not permitted')
    packet = envelope['packet']
    if digest(packet) != envelope['packet_digest']:
        raise ValueError('Packet digest mismatch')
    # Reuse structural checks only; no result or oracle is read.
    appendix(packet, 'supplied-packet', envelope['packet_digest'])
    objective = envelope['objective']
    events = packet['events']
    kind = {'recorded_stop': 'stop_response', 'at_most_one_effect': 'commit_response', 'recorded_delivery': 'correction_response'}[objective]
    flag = 'received' if kind == 'commit_response' else 'accepted'
    relevant = [(i, event) for i, event in enumerate(events) if event['event'] == kind]
    required = 2 if objective == 'at_most_one_effect' else 1
    applicable = len(relevant) >= required and all(event[flag] for _, event in relevant)
    event_locs = ['/events/'+str(i) for i, _ in relevant] or ['/events']
    downstream = packet['downstream']
    observed = downstream is not None
    aligned = None if downstream is None else False
    effect = None
    if downstream is not None:
        if objective == 'recorded_stop':
            if 'action' in downstream:
                aligned = True
                effect = downstream['action'] == 'prevented'
            elif 'effect_count' in downstream:
                aligned = len(set(downstream['request_ids'])) <= 1
                effect = downstream['effect_count'] == 0
        elif objective == 'at_most_one_effect' and 'effect_count' in downstream:
            aligned = len(set(downstream['request_ids'])) <= 1
            effect = downstream['effect_count'] <= 1
        elif objective == 'recorded_delivery' and 'internal_record' in downstream:
            aligned = downstream['internal_record'] == 'corrected'
            effect = downstream['recipient_record'] == 'corrected'
    checks = [
        {'check': 'applicable_response_recorded', 'satisfied': applicable, 'locators': event_locs},
        {'check': 'downstream_record_supplied', 'satisfied': observed, 'locators': ['/downstream']},
        {'check': 'record_fits_objective', 'satisfied': aligned, 'locators': ['/downstream']},
    ]
    return checks, effect


def result(envelope, procedure, response, checks):
    return {'version': VERSION, 'procedure': procedure, 'unit_id': envelope['unit_id'],
            'objective': envelope['objective'], 'claim_scope': envelope['scope'],
            'packet_digest': envelope['packet_digest'], 'response': response,
            'reason': ('A required record condition is unresolved.' if response == 'unresolved'
                       else 'The supplied terminal record supports the stated record-level objective.' if response == 'effect_supported'
                       else 'The supplied terminal record contradicts the stated record-level objective.'),
            'checks': checks, 'outcome_locator': None if response == 'unresolved' else '/downstream',
            'limits': ['No human-control or institutional finding.', 'Source completeness and truth are not independently established.']}


def checklist(envelope):
    checks, effect = facts(envelope)
    inspected = []
    for check in checks:
        inspected.append(check)
        if not check['satisfied']:
            return result(envelope, 'checklist', 'unresolved', inspected)
    return result(envelope, 'checklist', 'effect_supported' if effect else 'fault_supported', inspected)


def trace(envelope):
    checks, effect = facts(envelope)
    blockers = [check['check'] for check in checks if not check['satisfied']]
    response = 'unresolved' if blockers else ('effect_supported' if effect else 'fault_supported')
    output = result(envelope, 'trace', response, checks)
    output['blockers'] = blockers
    return output


def verify_response(envelope, response):
    # Mechanical agreement with this implementation, not independent rationale review.
    procedure = response.get('procedure') if isinstance(response, dict) else None
    if procedure not in {'checklist', 'trace'}:
        raise ValueError('Unknown procedure')
    expected = checklist(envelope) if procedure == 'checklist' else trace(envelope)
    if expected != response:
        raise ValueError('Response, rationale or locators differ from the declared procedure')
    return True
