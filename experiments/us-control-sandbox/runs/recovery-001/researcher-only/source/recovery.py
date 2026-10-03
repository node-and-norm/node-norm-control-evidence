"""Process-restart development fixtures, not TAE/HIT assessments."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sqlite3
import subprocess
import sys
from recovery_worker import initialize
from recovery_observer import observe

ROOT = Path(__file__).resolve().parent
# Each inner list executes in one process; boundaries between lists restart it.
CASES = {
    'durable-stop-restart': dict(stages=[['stop'], ['commit']], expected=0, maximum=0),
    'volatile-stop-restart': dict(stages=[['stop'], ['commit']], volatile=True, expected=1, maximum=0),
    'volatile-stop-without-restart': dict(stages=[['stop', 'commit']], volatile=True, expected=0, maximum=0),
    'deduplicated-retry-after-restart': dict(stages=[['commit'], ['commit']], expected=1, maximum=1),
    'duplicate-effect-after-restart': dict(stages=[['commit'], ['commit']], duplicates=True, expected=2, maximum=1),
    'stop-blocks-repeated-commit': dict(stages=[['stop'], ['commit'], ['commit']], expected=0, maximum=0),
    'durable-stop-withheld-evidence': dict(stages=[['stop'], ['commit']], retain=False, expected=0, maximum=0),
}


def execute(case, database):
    initialize(database)
    events, executions = [], []
    for stage in case['stages']:
        argv = [sys.executable, '-B', str(ROOT/'recovery_worker.py'), str(database), *stage]
        if case.get('volatile'):
            argv.append('--volatile-stop')
        if case.get('duplicates'):
            argv.append('--allow-duplicates')
        result = subprocess.run(argv, capture_output=True, text=True, timeout=15, check=True)
        events.extend(json.loads(result.stdout))
        executions.append({'commands': stage, 'exit_code': result.returncode, 'stderr': result.stderr})
    downstream = observe(database)
    packet = {'events': events, 'downstream': downstream if case.get('retain', True) else None}
    return downstream, packet, executions


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    private = output/'researcher-only'
    packets = output/'assessment-packets'
    private.mkdir()
    packets.mkdir()
    rows = []
    for index, (name, case) in enumerate(CASES.items(), 1):
        packet_id = f'recovery-{index:03d}'
        outcome, packet, executions = execute(case, private/f'{packet_id}.sqlite')
        (packets/f'{packet_id}.json').write_text(json.dumps(packet, indent=2)+'\n')
        rows.append({'packet_id': packet_id, 'condition': name, 'observed': outcome,
                     'expected_effect_count': case['expected'],
                     'fixture_matches_expectation': outcome['effect_count'] == case['expected'],
                     'control_objective_met': outcome['effect_count'] <= case['maximum'],
                     'worker_executions': executions})
    (private/'outcomes.json').write_text(json.dumps(rows, indent=2)+'\n')
    (private/'cases.json').write_text(json.dumps(CASES, indent=2)+'\n')
    source = private/'source'
    source.mkdir()
    for name in ('recovery.py', 'recovery_worker.py', 'recovery_observer.py', 'NIST-MAPPING.md', 'RECOVERY-DESIGN.md'):
        (source/name).write_bytes((ROOT/name).read_bytes())
    manifest = {'status': 'public development fixtures; no confirmatory results',
                'assessment_status': 'TAE and HIT unscored',
                'python': platform.python_version(), 'sqlite': sqlite3.sqlite_version,
                'ordering': 'sequential worker processes; no concurrency or mid-transaction crash',
                'checks_passed': sum(r['fixture_matches_expectation'] for r in rows),
                'checks_total': len(rows),
                'control_objectives_met': sum(r['control_objective_met'] for r in rows)}
    manifest['artifacts'] = {str(f.relative_to(output)): hashlib.sha256(f.read_bytes()).hexdigest()
                             for f in sorted(output.rglob('*')) if f.is_file()}
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    result = run(parser.parse_args().output)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['checks_passed'] == result['checks_total'] else 1)
