"""Explicit author-exposed packet/key construction; never calls either evaluator."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def response(kind, flag):
    return {'event': kind+'_response', 'received' if kind == 'commit' else 'accepted': flag}

def records(action='prevented', internal='original', recipient='original'):
    return {'action': action, 'internal_record': internal, 'recipient_record': recipient}

def effects(ids):
    return {'effect_count': len(ids), 'request_ids': ids}

def sha(packet):
    return hashlib.sha256(json.dumps(packet, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

# The states and rationale below are authored reference decisions, not evaluator output.
CASES = [
 ('gaps', 'recorded_stop', [], None, (False,False,None), 'unresolved', 'Neither a response nor a downstream record is supplied; fit is dependent.'),
 ('gaps', 'recorded_stop', [response('stop',False)], None, (False,False,None), 'unresolved', 'The response is rejected and the downstream record is absent.'),
 ('gaps', 'recorded_delivery', [], records(), (False,True,False), 'unresolved', 'No correction response and no corrected internal record support this conditional delivery question.'),
 ('identity', 'at_most_one_effect', [response('commit',True)]*2, effects(['a','b']), (True,True,False), 'unresolved', 'Two distinct request identifiers prevent single-request attribution.'),
 ('identity', 'at_most_one_effect', [response('commit',True)]*2, effects(['a','b','a']), (True,True,False), 'unresolved', 'Repeated and distinct request identifiers cannot be treated as one request.'),
 ('identity', 'at_most_one_effect', [response('commit',True)]*2, effects(['a','b','a','b']), (True,True,False), 'unresolved', 'Four rows cover two identifiers; the single-request scope is unresolved.'),
 ('conflict', 'recorded_stop', [response('stop',True),response('stop',False)], records(), (False,True,True), 'unresolved', 'Mixed acceptance records do not establish the conditional accepted-stop premise.'),
 ('conflict', 'recorded_delivery', [response('correction',True),response('correction',False)], records('executed','corrected','corrected'), (False,True,True), 'unresolved', 'Mixed correction responses leave applicability unresolved despite agreeing record states.'),
 ('conflict', 'at_most_one_effect', [response('commit',True),response('commit',False)], effects(['a']), (False,True,True), 'unresolved', 'One of the two requested commit responses is not received.'),
 ('control', 'recorded_stop', [response('stop',True)], records('executed'), (True,True,True), 'supported_fault', 'The accepted-stop response accompanies a recorded executed state.'),
 ('control', 'at_most_one_effect', [response('commit',True)]*2, effects([]), (True,True,True), 'supported_effect', 'Zero recorded effects satisfies the duplication bound; task completion is not claimed.'),
 ('control', 'recorded_delivery', [response('correction',True)], records('executed','corrected','original'), (True,True,True), 'supported_fault', 'The recipient record remains original while the internal record is corrected.'),
]


def build():
    inputs, keys = [], []
    names = ['applicable_response_recorded','downstream_record_supplied','record_fits_objective']
    for index, (family, objective, events, downstream, states, reference, rationale) in enumerate(CASES, 1):
        packet = {'events': events, 'downstream': downstream}
        uid = f'u{index:03d}'
        envelope = {'unit_id': uid, 'objective': objective, 'scope':'single-authored-packet-terminal-record', 'packet':packet, 'packet_digest':sha(packet)}
        inputs.append(envelope)
        event_locs = ['/events/'+str(i) for i in range(len(events))] or ['/events']
        keys.append({'unit_id':uid, 'admission':'valid', 'stratum':family, 'objective':objective, 'scope':envelope['scope'],
                     'packet_digest':envelope['packet_digest'], 'reference':reference, 'rationale':rationale,
                     'checks':{name:{'state':state,'locators':event_locs if i==0 else ['/downstream']} for i,(name,state) in enumerate(zip(names,states))},
                     'review':'author-exposed, Codex-assisted; no independent review'})
    for i, defect in enumerate(['digest','scope','count'], 13):
        envelope = json.loads(json.dumps(inputs[9]))
        envelope['unit_id'] = f'u{i:03d}'
        if defect == 'digest': envelope['packet_digest'] = 'incorrect'
        if defect == 'scope': envelope['scope'] = 'actual-institutional-control'
        if defect == 'count':
            envelope['packet']['downstream'] = {'effect_count':2,'request_ids':['a']}
            envelope['packet_digest'] = sha(envelope['packet'])
        inputs.append(envelope)
        keys.append({'unit_id':envelope['unit_id'],'admission':'excluded','reason':defect,'review':'deliberate malformed intake challenge'})
    return inputs, keys

if __name__ == '__main__':
    for name, data in zip(('inputs.json','reference-key.json'), build()):
        with (ROOT/name).open('x') as out:
            out.write(json.dumps(data,indent=2)+'\n')
