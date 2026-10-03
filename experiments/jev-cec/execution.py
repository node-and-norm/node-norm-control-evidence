"""Offline schedule and strict response acceptance for CEC Jev protocol v1."""
import argparse
import json
import math
from pathlib import Path
from challenge import check, encode, sha, FOLDER, DIMS, LABELS

MODEL = 'jev-1.13.0'
REPETITIONS = 3


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError('nonfinite JSON number')


def validate_response(raw):
    doc = json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant)
    if not isinstance(doc, dict) or doc.get('model') != MODEL:
        raise ValueError('resolved model mismatch')
    answers = doc.get('answers')
    if not isinstance(answers, dict) or set(answers) != DIMS:
        raise ValueError('answer identifiers mismatch')
    usage = doc.get('usage')
    if not isinstance(usage, dict) or any(type(usage.get(k)) is not int or usage[k] < 0 for k in ('input_tokens', 'output_tokens')):
        raise ValueError('invalid or missing usage')
    for answer in answers.values():
        if not isinstance(answer, dict) or answer.get('type') != 'choice' or not isinstance(answer.get('choice'), str) or answer['choice'] not in LABELS:
            raise ValueError('invalid answer choice')
        probabilities = answer.get('probabilities')
        if not isinstance(probabilities, dict) or set(probabilities) != LABELS:
            raise ValueError('probability labels mismatch')
        for value in [answer.get('confidence'), *probabilities.values()]:
            if type(value) not in (int, float) or not 0 <= value <= 1 or not math.isfinite(value):
                raise ValueError('invalid probability or confidence')
        if not math.isclose(sum(probabilities.values()), 1.0, rel_tol=0, abs_tol=1e-5):
            raise ValueError('probability sum mismatch')
        if probabilities[answer['choice']] < max(probabilities.values()):
            raise ValueError('choice is not a maximum')
    return doc


def schedule():
    cards, questions = check()
    return [{'attempt_id': f'P{repeat}-{card["id"]}', 'pass': repeat, 'card_id': card['id'],
             'payload': {'model': MODEL, 'state': card['state'], 'questions': questions}}
            for repeat in range(1, REPETITIONS + 1) for card in cards]


def prepare(output):
    rows = schedule()
    output.mkdir(parents=True, exist_ok=False)
    raw = encode(rows)
    (output / 'schedule.json').write_bytes(raw)
    protocol = Path(__file__).parent / 'execution-v1/PROTOCOL.md'
    (output / 'manifest.json').write_bytes(encode({
        'mode': 'offline_schedule', 'scheduled_requests': len(rows), 'scheduled_determinations': len(rows)*3,
        'requests_sent': 0, 'schedule_sha256': sha(raw),
        'protocol_sha256': sha(protocol.read_bytes()), 'challenge_freeze_sha256': sha((FOLDER/'freeze.json').read_bytes()),
        'payload_sha256': {row['attempt_id']: sha(encode(row['payload'])) for row in rows}}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    prepare(args.output)
    print('36 requests scheduled; 108 determinations; zero requests sent.')
