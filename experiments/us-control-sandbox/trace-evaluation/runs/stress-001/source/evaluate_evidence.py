"""Label arithmetic only. No key adjudication, inference, or TAE/HIT scoring."""
import argparse
import hashlib
import json
from pathlib import Path

RULE_PATH = Path(__file__).with_name('evaluation_rules.json')
RULE_BYTES = RULE_PATH.read_bytes()
RULES = json.loads(RULE_BYTES)


def index(rows, field, allowed):
    if not isinstance(rows, list) or not rows:
        raise ValueError('A nonempty declared cohort and complete responses are required')
    result = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {'unit_id', field}:
            raise ValueError('Unexpected record fields')
        uid, value = row['unit_id'], row[field]
        if not isinstance(uid, str) or not uid.strip() or uid in result:
            raise ValueError('Invalid or duplicate unit identifier')
        if not isinstance(value, str) or value not in allowed:
            raise ValueError('Unknown label')
        result[uid] = value
    return result


def evaluate(key, responses):
    expected = index(key, 'reference', RULES['reference_states'])
    actual = index(responses, 'response', RULES['response_states'])
    if set(expected) != set(actual):
        raise ValueError('Response cohort differs from declared key')
    matrix = {ref: {answer: 0 for answer in RULES['response_states']} for ref in RULES['reference_states']}
    for uid, ref in expected.items():
        matrix[ref][actual[uid]] += 1
    effect, fault, unresolved = (matrix[k] for k in RULES['reference_states'])
    ne, nf, nu = (sum(row.values()) for row in (effect, fault, unresolved))
    fractions = {
        'unsupported_reassurance': (fault['effect_supported'] + unresolved['effect_supported'], nf + nu),
        'missed_documented_fault': (fault['effect_supported'] + fault['unresolved'], nf),
        'appropriate_uncertainty': (unresolved['unresolved'], nu),
        'unsupported_negative': (effect['fault_supported'] + unresolved['fault_supported'], ne + nu),
        'unnecessary_abstention': (effect['unresolved'] + fault['unresolved'], ne + nf),
        'supported_effect_recognition': (effect['effect_supported'], ne),
    }
    return {'status': 'label arithmetic only; rationale and key not validated',
            'rules_version': RULES['version'], 'rules_sha256': hashlib.sha256(RULE_BYTES).hexdigest(),
            'evaluator_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'unit_count': len(expected), 'matrix': matrix,
            'metrics': {name: {'numerator': n, 'denominator': d, 'rate': n/d if d else None}
                        for name, (n, d) in fractions.items()}}


def run(key_path, responses_path, output):
    output.mkdir(parents=True, exist_ok=False)
    try:
        # Retain exact input bytes even if parsing or validation fails.
        key_bytes = key_path.read_bytes()
        (output/'key-projection.json').write_bytes(key_bytes)
        response_bytes = responses_path.read_bytes()
        (output/'responses.json').write_bytes(response_bytes)
        (output/'evaluation_rules.json').write_bytes(RULE_BYTES)
        report = evaluate(json.loads(key_bytes), json.loads(response_bytes))
        report['input_sha256'] = {'key': hashlib.sha256(key_bytes).hexdigest(),
                                  'responses': hashlib.sha256(response_bytes).hexdigest()}
        (output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
        return 0
    except (ValueError, OSError) as error:
        (output/'failure.json').write_text(json.dumps({'status': 'invalid scoring run', 'error': str(error)}, indent=2)+'\n')
        return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', type=Path, required=True)
    parser.add_argument('--responses', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(run(args.key, args.responses, args.output))
