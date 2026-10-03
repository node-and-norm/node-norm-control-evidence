"""Extract bounded observations from supplied packets, without scoring TAE/HIT."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACKET_REVISION = '8a792f69df95d7c96481871d960fe420385bb885'
RUNS = ('runs/rehearsal-002', 'runs/recovery-001')


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def appendix(packet, source, digest):
    require(isinstance(packet, dict) and set(packet) == {'events', 'downstream'}, 'Unexpected packet fields')
    require(isinstance(packet['events'], list), 'Events must be a list')
    observations = []
    for index, event in enumerate(packet['events']):
        require(isinstance(event, dict), 'Event must be an object')
        kind = event.get('event')
        require(kind in {'stop_response', 'correction_response', 'commit_response'}, 'Unknown event')
        flag = 'received' if kind == 'commit_response' else 'accepted'
        require(set(event) in ({'event', flag}, {'event', flag, 'tick'}), 'Unexpected event fields')
        require(type(event[flag]) is bool, 'Response flag must be boolean')
        if 'tick' in event:
            require(type(event['tick']) is int and event['tick'] >= 0, 'Invalid logical tick')
        observations.append({'locator': f'/events/{index}', 'proposition': 'The supplied response record contains this event.', 'value': event})
    downstream = packet['downstream']
    if downstream is not None:
        require(isinstance(downstream, dict), 'Invalid downstream object')
        if set(downstream) == {'action', 'internal_record', 'recipient_record'}:
            require(downstream['action'] in {'prevented', 'executed'}, 'Unknown action')
            require(all(downstream[k] in {'original', 'corrected'} for k in ('internal_record', 'recipient_record')), 'Unknown record state')
        elif set(downstream) == {'effect_count', 'request_ids'}:
            require(type(downstream['effect_count']) is int and downstream['effect_count'] >= 0, 'Invalid effect count')
            require(isinstance(downstream['request_ids'], list) and all(isinstance(x, str) and x for x in downstream['request_ids']), 'Invalid request IDs')
            require(len(downstream['request_ids']) == downstream['effect_count'], 'Effect count contradicts listed records')
        else:
            raise ValueError('Unexpected downstream fields')
        for key, value in downstream.items():
            observations.append({'locator': '/downstream/'+key,
                                 'proposition': 'The supplied downstream record contains this value.', 'value': value})
    return {'format': 'node-norm-technical-evidence-appendix/0.1',
            'evidence_origin': 'authored synthetic development fixture',
            'source': {'path': source, 'sha256': digest, 'git_revision': PACKET_REVISION},
            'method_assessment': {'tae_scoring_enabled': False, 'hit_scoring_enabled': False,
                                  'eligibility': 'technical appendix only; no human or institutional unit'},
            'observations': observations,
            'unresolved': ([{'locator': '/downstream', 'proposition': 'The downstream result is not supplied in this packet.'}] if downstream is None else []),
            'limitations': ['Records and observer share the authored fixture origin; no independent corroboration.',
                            'Public development packet; no blinding or held-out status.',
                            'Matching a recorded hash does not establish completeness or truth.',
                            'No human authority, comprehension, judgment, correction or repair finding.']}


def documents(root=ROOT):
    result = {}
    for run in RUNS:
        folder = root/run
        manifest = json.loads((folder/'manifest.json').read_text())
        expected = {p: h for p, h in manifest['artifacts'].items() if p.startswith('assessment-packets/')}
        actual = {str(p.relative_to(folder)) for p in (folder/'assessment-packets').glob('*.json')}
        require(actual == set(expected), 'Packet inventory differs from recorded manifest')
        for relative, digest in sorted(expected.items()):
            raw = (folder/relative).read_bytes()
            require(hashlib.sha256(raw).hexdigest() == digest, 'Packet hash differs from recorded manifest')
            source = run+'/'+relative
            name = Path(run).name+'-'+Path(relative).name
            result[name] = appendix(json.loads(raw), source, digest)
    return result


def serialized(value):
    return (json.dumps(value, indent=2, sort_keys=True)+'\n').encode()


def write(output):
    docs = documents()
    output.mkdir(parents=True, exist_ok=False)
    for name, value in docs.items():
        (output/name).write_bytes(serialized(value))
    return len(docs)


def check(output):
    expected = {name: serialized(value) for name, value in documents().items()}
    actual = {str(p.relative_to(output)): p.read_bytes() for p in output.rglob('*') if p.is_file()}
    require(actual == expected, 'Appendix inventory or content differs from reproducible extraction')
    return len(expected)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print(check(args.output) if args.check else write(args.output))
