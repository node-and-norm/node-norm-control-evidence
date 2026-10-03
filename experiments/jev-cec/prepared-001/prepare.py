"""Prepare synthetic-only Jev requests. No SDK, credentials, inference or scoring."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate import validate

HERE = Path(__file__).resolve().parent
EXAMPLES = ('synthetic.json', 'override-confirmed.json', 'policy-only.json')
MODEL = 'jev-1.13.0'


def encoded(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def prepare(data):
    if data.get('mode') != 'synthetic':
        raise ValueError('Only synthetic development bundles are eligible')
    errors = validate(data)
    if errors:
        raise ValueError('Invalid bundle: ' + '; '.join(errors))
    if len(data['packet']) != 1 or len(data['control']) != 1 or len(data['event']) != 1:
        raise ValueError('Preparation requires exactly one event, control and packet')
    packet, control = data['packet'][0], data['control'][0]
    evidence = [e for e in data['evidence_item'] if e['id'] in packet['evidence_ids']]
    source_ids = {e['source_id'] for e in evidence}
    while True:
        linked = {r['to_source_id'] for r in data['provenance_relation']
                  if r['from_source_id'] in source_ids}
        if linked <= source_ids:
            break
        source_ids |= linked
    # Explicit field projection: no annotations, claims, quality ratings, titles,
    # adjudications, omissions commentary or downstream derived measures.
    state = {
        'synthetic': True,
        'scope': {k: control[k] for k in ('objective', 'opportunity', 'relevant_from', 'relevant_to')},
        'cutoff': packet['cutoff'],
        'evidence': [{k: e[k] for k in ('id', 'source_id', 'locator', 'observation', 'valid_from')}
                     for e in evidence],
        'sources': [{k: s[k] for k in ('id', 'family_id', 'source_date', 'retrieved_at', 'version')}
                    for s in data['source'] if s['id'] in source_ids],
        'source_relations': [{k: r[k] for k in ('from_source_id', 'to_source_id', 'relation', 'basis')}
                             for r in data['provenance_relation'] if r['from_source_id'] in source_ids],
    }
    request = {'model': MODEL, 'state': state,
               'questions': json.loads((HERE / 'questions.json').read_text())}
    return request


def export(destination):
    requests, sources, provenance = [], {}, []
    for name in EXAMPLES:
        raw = (ROOT / 'examples' / name).read_bytes()
        data = json.loads(raw)
        request = prepare(data)
        index = len(requests) + 1
        requests.append(request)
        sources[f'input-{index}.json'] = raw
        provenance.append({'request_index': index, 'source_path': 'examples/' + name,
                           'input_sha256': digest(raw),
                           'packet_sha256': data['packet'][0]['content_sha256'],
                           'request_sha256': digest(encoded(request))})
    artifacts = {'requests.json': encoded(requests), 'provenance.json': encoded(provenance),
                 'questions.json': (HERE / 'questions.json').read_bytes(),
                 'prepare.py': Path(__file__).read_bytes(),
                 'PLAN.txt': (HERE / 'PLAN.md').read_bytes(),
                 'CODEBOOK.txt': (ROOT / 'docs/methods/CODEBOOK.md').read_bytes(), **sources}
    destination.mkdir(parents=True, exist_ok=False)
    for name, raw in artifacts.items():
        (destination / name).write_bytes(raw)
    manifest = {'status': 'prepared-only', 'model_requested': MODEL, 'model_resolved': None,
                'requests_prepared': len(requests), 'requests_sent': 0,
                'research_status': 'author-exposed synthetic preparation; no model results',
                'artifacts': {name: digest(raw) for name, raw in artifacts.items()}}
    (destination / 'manifest.json').write_bytes(encoded(manifest))
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(export(args.output), indent=2))
