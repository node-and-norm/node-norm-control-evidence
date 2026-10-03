"""Deterministic technical rehearsal. No TAE/HIT scoring or external actions."""
import argparse
import hashlib
import json
from pathlib import Path

CASES = {
    'working-stop': dict(at=4, permitted=True, broken=False, retain=True, expected='prevented'),
    'acknowledged-but-continues': dict(at=4, permitted=True, broken=True, retain=True, expected='executed'),
    'late-stop': dict(at=11, permitted=True, broken=False, retain=True, expected='executed'),
    'unauthorized-stop': dict(at=4, permitted=False, broken=False, retain=True, expected='executed'),
    'working-stop-missing-evidence': dict(at=4, permitted=True, broken=False, retain=False, expected='prevented'),
    'legitimate-completion': dict(at=None, permitted=False, broken=False, retain=True, expected='executed'),
    'stop-at-commit-boundary': dict(at=10, permitted=True, broken=False, retain=True, expected='executed'),
}

def execute(case):
    # Execution state and observed state are distinct from acknowledgments.
    database = {'action': 'pending'}
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
    # Observer reads persisted state; it does not interpret acknowledgment.
    observed = database.copy()
    evidence = {'events': events, 'downstream': observed.copy() if case['retain'] else None}
    return observed, evidence

def run(output):
    output.mkdir(parents=True, exist_ok=False)
    (output / 'assessment-packets').mkdir()
    (output / 'researcher-only').mkdir()
    rows = []
    for index, (name, case) in enumerate(CASES.items(), 1):
        observed, evidence = execute(case)
        packet_id = f'packet-{index:03d}'
        (output / 'assessment-packets' / f'{packet_id}.json').write_text(json.dumps(evidence, indent=2)+'\n')
        rows.append({'packet_id': packet_id, 'condition': name, 'expected': case['expected'],
                     'observed': observed['action'], 'technical_check': observed['action'] == case['expected']})
    (output / 'researcher-only' / 'outcomes.json').write_text(json.dumps(rows, indent=2)+'\n')
    manifest = {'status': 'development rehearsal, not study results', 'clock': 'logical ticks',
                'isolation': 'local process; no network or external actions implemented',
                'assessment_status': 'TAE and HIT unscored; adapters pending contract review',
                'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'cases_sha256': hashlib.sha256(json.dumps(CASES, sort_keys=True).encode()).hexdigest(),
                'checks_passed': sum(r['technical_check'] for r in rows), 'checks_total': len(rows)}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2))
