"""Offline-only packet clarification with hash-bound original requests."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE.parent / 'instruction-comparison-001/live-001'
OLD = 'The console issued R.'
NEW = 'The console issued stop request R targeting fee job J.'


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def schedule():
    bindings = json.loads((HERE / 'source-bindings.json').read_text())
    originals = {}
    for card, binding in bindings.items():
        raw = (ARCHIVE / binding['path']).read_bytes()
        if sha(raw) != binding['sha256']:
            raise ValueError('Original request changed: ' + card)
        originals[card] = json.loads(raw)
    rows = []
    for pass_id in (1, 2):
        for index, card in enumerate(sorted(originals)):
            order = ('original', 'explicit') if (pass_id + index) % 2 else ('explicit', 'original')
            for condition in order:
                payload = copy.deepcopy(originals[card])
                text = payload['state']['evidence'][0]['text']
                if not text.startswith(OLD) or text.count(OLD) != 1:
                    raise ValueError('Unexpected issuance statement')
                if condition == 'explicit':
                    payload['state']['evidence'][0]['text'] = NEW + text[len(OLD):]
                rows.append({'attempt_id': f'P{pass_id}-{card}-{condition}',
                             'pass': pass_id, 'card_id': card, 'condition': condition,
                             'payload': payload, 'payload_sha256': sha(encode(payload))})
    return rows


def prepare(output):
    rows = schedule()
    output.mkdir(parents=True, exist_ok=False)
    (output / 'schedule.json').write_bytes(encode(rows))
    sources = {name: sha((HERE / name).read_bytes()) for name in
               ('PLAN.md', 'reference.json', 'source-bindings.json', 'prepare.py')}
    (output / 'manifest.json').write_bytes(encode({
        'status': 'offline_preparation_not_execution_freeze', 'requests_sent': 0,
        'scheduled_requests': len(rows), 'scheduled_judgments': 4 * len(rows),
        'sources': sources, 'schedule_sha256': sha((output / 'schedule.json').read_bytes())}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    prepare(parser.parse_args().output)
