"""Re-present seven existing public packets; no fresh cases or reference labels."""
import argparse
import hashlib
import json
from pathlib import Path
from paired_procedures import checklist, trace, digest, verify_response

ROOT = Path(__file__).resolve().parent
SELECTION = [
    ('runs/recovery-001', 'recovery-001', 'recorded_stop'),
    ('runs/recovery-001', 'recovery-002', 'recorded_stop'),
    ('runs/recovery-001', 'recovery-004', 'at_most_one_effect'),
    ('runs/recovery-001', 'recovery-005', 'at_most_one_effect'),
    ('runs/recovery-001', 'recovery-007', 'recorded_stop'),
    ('runs/rehearsal-002', 'packet-008', 'recorded_delivery'),
    ('runs/rehearsal-002', 'packet-009', 'recorded_delivery'),
]


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    rows = []
    try:
        for i, (run_path, name, objective) in enumerate(SELECTION, 1):
            packet_path = f'{run_path}/assessment-packets/{name}.json'
            raw = (ROOT/packet_path).read_bytes()
            manifest = json.loads((ROOT/run_path/'manifest.json').read_text())
            expected = manifest['artifacts'][f'assessment-packets/{name}.json']
            if hashlib.sha256(raw).hexdigest() != expected:
                raise ValueError('Source bytes differ from recorded packet hash')
            packet = json.loads(raw)
            envelope = {'unit_id': f'demo-{i:03d}', 'objective': objective,
                        'scope': 'single-authored-packet-terminal-record', 'packet': packet,
                        'packet_digest': digest(packet)}
            a, b = checklist(envelope), trace(envelope)
            verify_response(envelope, a)
            verify_response(envelope, b)
            artifact = {'source': {'path': packet_path, 'sha256': expected,
                                   'revision': '8a792f69df95d7c96481871d960fe420385bb885'},
                        'envelope': envelope, 'checklist': a, 'trace': b}
            (output/f'demo-{i:03d}.json').write_text(json.dumps(artifact, indent=2)+'\n')
            rows.append({'unit_id': envelope['unit_id'], 'checklist_response': a['response'],
                         'trace_response': b['response'], 'labels_agree': a['response'] == b['response']})
        summary = {'status': 'public development demonstration; no independent reference key or comparative performance estimate',
                   'selection': 'seven existing packets chosen for visible development contrasts',
                   'tae_hit_scored': False, 'rows': rows}
        (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
        source = output/'source'
        source.mkdir()
        for name in ('paired_procedures.py', 'run_paired_demo.py', 'build_evidence_appendices.py', 'PROCEDURES.md', 'RUN-PLAN.md'):
            (source/name).write_bytes((ROOT/name).read_bytes())
        hashes = {str(p.relative_to(output)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(output.rglob('*')) if p.is_file()}
        (output/'manifest.json').write_text(json.dumps({'status': 'development demonstration', 'artifacts': hashes}, indent=2)+'\n')
        return 0
    except (OSError, ValueError, KeyError) as error:
        (output/'failure.json').write_text(json.dumps({'status': 'failed attempt', 'error': str(error)}, indent=2)+'\n')
        return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    raise SystemExit(run(parser.parse_args().output))
