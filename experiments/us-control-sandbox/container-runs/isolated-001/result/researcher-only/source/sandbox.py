"""Deterministic technical rehearsal. No TAE/HIT scoring or external actions."""
import argparse
import hashlib
import json
import sqlite3
import tempfile
import platform
from observer import observe
from pathlib import Path

CASES = {
    'working-stop': dict(at=4, permitted=True, broken=False, retain=True, expected='prevented'),
    'acknowledged-but-continues': dict(at=4, permitted=True, broken=True, retain=True, expected='executed'),
    'late-stop': dict(at=11, permitted=True, broken=False, retain=True, expected='executed'),
    'unauthorized-stop': dict(at=4, permitted=False, broken=False, retain=True, expected='executed'),
    'working-stop-missing-evidence': dict(at=4, permitted=True, broken=False, retain=False, expected='prevented'),
    'legitimate-completion': dict(at=None, permitted=False, broken=False, retain=True, expected='executed'),
    'stop-at-commit-boundary': dict(at=10, permitted=True, broken=False, retain=True, expected='executed'),
    'correction-delivered': dict(at=None, permitted=False, broken=False, retain=True, correction=True, delivery=True, expected='executed', expected_recipient='corrected'),
    'correction-not-delivered': dict(at=None, permitted=False, broken=False, retain=True, correction=True, delivery=False, expected='executed', expected_recipient='original'),
}

def execute(case, database_path=None):
    if database_path is None:
        with tempfile.TemporaryDirectory() as temp:
            return execute(case, Path(temp) / 'outcome.sqlite')
    # Create new records only; preserve previous attempts.
    database_path = Path(database_path)
    with database_path.open('xb'):
        pass
    database = {'action': 'pending', 'internal_record': 'original', 'recipient_record': 'original'}
    events = []
    halted = False
    for tick in range(12):
        # The frozen tie rule commits before handling same-tick commands.
        if tick == 10:
            database['action'] = 'prevented' if halted else 'executed'
        if case['at'] == tick:
            accepted = case['permitted'] and database['action'] == 'pending'
            events.append({'tick': tick, 'event': 'stop_response', 'accepted': accepted})
            if accepted and not case['broken']:
                halted = True
    if case.get('correction'):
        database['internal_record'] = 'corrected'
        events.append({'tick': 12, 'event': 'correction_response', 'accepted': True})
        if case['delivery']:
            database['recipient_record'] = 'corrected'
    with sqlite3.connect(database_path) as connection:
        connection.execute('CREATE TABLE outcome (action TEXT, internal_record TEXT, recipient_record TEXT)')
        connection.execute('INSERT INTO outcome VALUES (?, ?, ?)', tuple(database.values()))
    observed = observe(database_path)
    evidence = {'events': events, 'downstream': observed.copy() if case['retain'] else None}
    return observed, evidence

def run(output):
    output.mkdir(parents=True, exist_ok=False)
    (output / 'assessment-packets').mkdir()
    (output / 'researcher-only').mkdir()
    rows = []
    for index, (name, case) in enumerate(CASES.items(), 1):
        packet_id = f'packet-{index:03d}'
        observed, evidence = execute(case, output / 'researcher-only' / f'{packet_id}.sqlite')
        (output / 'assessment-packets' / f'{packet_id}.json').write_text(json.dumps(evidence, indent=2)+'\n')
        rows.append({'packet_id': packet_id, 'condition': name, 'expected': case['expected'],
                     'observed': observed, 'technical_check': observed['action'] == case['expected'] and observed['recipient_record'] == case.get('expected_recipient', 'original')})
    (output / 'researcher-only' / 'outcomes.json').write_text(json.dumps(rows, indent=2)+'\n')
    source_dir = output / 'researcher-only' / 'source'
    source_dir.mkdir()
    for name in ('sandbox.py', 'observer.py'):
        (source_dir / name).write_bytes(Path(__file__).with_name(name).read_bytes())
    manifest = {'status': 'development rehearsal, not study results', 'clock': 'logical ticks', 'python': platform.python_version(), 'sqlite': sqlite3.sqlite_version,
                'isolation': 'local process; no network or external actions implemented',
                'assessment_status': 'TAE and HIT unscored; adapters pending contract review',
                'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'cases_sha256': hashlib.sha256(json.dumps(CASES, sort_keys=True).encode()).hexdigest(),
                'checks_passed': sum(r['technical_check'] for r in rows), 'checks_total': len(rows)}
    manifest['artifacts'] = {str(f.relative_to(output)): hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(output.rglob('*')) if f.is_file()}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2))
