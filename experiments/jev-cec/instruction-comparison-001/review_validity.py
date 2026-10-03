"""Reproduce a post-output diagnostic without repairing or rescoring responses."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def review():
    archive = ROOT / 'live-001'
    attempts = json.loads((archive / 'attempts.json').read_text())
    failures = []
    for attempt in attempts:
        raw = (archive / 'responses' / (attempt['attempt_id'] + '.bin')).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == attempt['response_sha256']
        response = json.loads(raw)
        failing = []
        for dimension, answer in response['answers'].items():
            total = sum(answer['probabilities'].values())
            if not math.isclose(total, 1, rel_tol=0, abs_tol=1e-5):
                failing.append({'dimension': dimension, 'sum': total})
        if attempt['status'] == 'invalid':
            failures.append({
                'attempt_id': attempt['attempt_id'],
                'response_sha256': attempt['response_sha256'],
                'rejection': attempt['validation_error'],
                'failing_distributions': failing,
                'all_choices_are_maxima': all(
                    a['probabilities'][a['choice']] == max(a['probabilities'].values())
                    for a in response['answers'].values()),
            })
        else:
            assert not failing
    return {'scope': 'Post-output descriptive review; no normalization or rescoring.',
            'attempts': len(attempts), 'invalid_responses': len(failures),
            'excluded_judgments': len(failures) * 4, 'failures': failures}


if __name__ == '__main__':
    print(json.dumps(review(), indent=2, sort_keys=True))
