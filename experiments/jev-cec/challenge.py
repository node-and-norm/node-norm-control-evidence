"""Verify and prepare frozen synthetic CEC challenges, without inference."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE / 'challenge-v1'
FILES = {'cards.json', 'reference-key.json', 'questions.json', 'CODEBOOK.txt', 'README.md'}
DIMS = {'action', 'propagation', 'outcome_mitigation'}
LABELS = {'yes', 'no', 'partial', 'conflicting', 'unknown', 'not_reported', 'not_observable', 'not_applicable'}


def encode(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def fields(row, required):
    if not isinstance(row, dict) or set(row) != set(required):
        raise ValueError('Unexpected or missing fields')


def validate_cards(cards):
    if not isinstance(cards, list) or len(cards) != 12:
        raise ValueError('Expected twelve development cards')
    ids = set()
    for card in cards:
        fields(card, {'id', 'state'})
        if not isinstance(card['id'], str) or not card['id'] or card['id'] in ids:
            raise ValueError('Invalid or duplicate card ID')
        ids.add(card['id'])
        state = card['state']
        fields(state, {'synthetic', 'scope', 'cutoff', 'evidence', 'sources', 'source_relations'})
        if state['synthetic'] is not True:
            raise ValueError('Synthetic only')
        fields(state['scope'], {'objective', 'opportunity', 'relevant_from', 'relevant_to'})
        for value in [state['cutoff'], *state['scope'].values()]:
            if not isinstance(value, str) or not value.strip():
                raise ValueError('Missing scope')
        seen_sources = set()
        for source in state['sources']:
            fields(source, {'id', 'family_id', 'source_date', 'retrieved_at', 'version'})
            if source['id'] in seen_sources:
                raise ValueError('Duplicate source ID')
            seen_sources.add(source['id'])
        seen_evidence = set()
        if not state['evidence']:
            raise ValueError('Empty evidence')
        for evidence in state['evidence']:
            fields(evidence, {'id', 'source_id', 'locator', 'observation', 'valid_from'})
            if evidence['id'] in seen_evidence or evidence['source_id'] not in seen_sources:
                raise ValueError('Broken evidence reference')
            if any(not isinstance(v, str) or not v.strip() for v in evidence.values()):
                raise ValueError('Empty evidence field')
            seen_evidence.add(evidence['id'])
        for relation in state['source_relations']:
            fields(relation, {'from_source_id', 'to_source_id', 'relation', 'basis'})
            if relation['from_source_id'] not in seen_sources or relation['to_source_id'] not in seen_sources:
                raise ValueError('Broken lineage reference')


def check(folder=FOLDER):
    freeze = json.loads((folder / 'freeze.json').read_text())
    if set(freeze['artifacts']) != FILES:
        raise ValueError('Unexpected freeze artifact set')
    for name, expected in freeze['artifacts'].items():
        if sha((folder / name).read_bytes()) != expected:
            raise ValueError('Freeze mismatch: ' + name)
    cards = json.loads((folder / 'cards.json').read_text())
    validate_cards(cards)
    questions = json.loads((folder / 'questions.json').read_text())
    if set(questions) != DIMS or any(set(q['criteria']) != LABELS for q in questions.values()):
        raise ValueError('Question vocabulary mismatch')
    key = json.loads((folder / 'reference-key.json').read_text())
    if len(key) != len(cards) or [k['id'] for k in key] != [c['id'] for c in cards]:
        raise ValueError('Key coverage mismatch')
    for row, card in zip(key, cards):
        if set(row['judgments']) != DIMS:
            raise ValueError('Dimension mismatch')
        evidence_ids = {e['id'] for e in card['state']['evidence']}
        for judgment in row['judgments'].values():
            if judgment['value'] not in LABELS or not judgment['rationale'].strip():
                raise ValueError('Invalid authored judgment')
            if not judgment['evidence_ids'] or not set(judgment['evidence_ids']) <= evidence_ids:
                raise ValueError('Invalid key locator')
    return cards, questions


def prepare(output, folder=FOLDER):
    cards, questions = check(folder)
    requests = [{'card_id': c['id'], 'payload': {'model': 'jev-1.13.0', 'state': c['state'], 'questions': questions}} for c in cards]
    output.mkdir(parents=True, exist_ok=False)
    raw = encode(requests)
    (output / 'requests.json').write_bytes(raw)
    (output / 'manifest.json').write_bytes(encode({
        'status': 'prepared-only', 'requests_sent': 0, 'requests_prepared': len(cards),
        'questions_prepared': len(cards) * len(questions),
        'freeze_sha256': sha((folder / 'freeze.json').read_bytes()),
        'preparer_sha256': sha(Path(__file__).read_bytes()),
        'requests_sha256': sha(raw),
        'payload_sha256': {r['card_id']: sha(encode(r['payload'])) for r in requests}}))
    return requests


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['check', 'prepare'])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.mode == 'check':
        check()
        print('Twelve cards, 36 authored judgments and freeze hashes verified. No inference.')
    else:
        if args.output is None:
            parser.error('--output is required')
        prepare(args.output)
        print('Prepared twelve requests, 36 questions; zero requests sent.')
