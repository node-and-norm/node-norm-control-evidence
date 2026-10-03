"""Create, inspect and probe one container; remove only the container created here."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from run_container import ROOT, command


def execute(image, context, name):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', name):
        raise ValueError('Invalid verification name')
    destination = ROOT/'isolation-runs'/name
    destination.mkdir(parents=True, exist_ok=False)
    base = ['docker', '--context', context]
    argv = command(image, destination, context=context)
    argv[argv.index('run')] = 'create'
    argv.remove('--rm')
    argv[argv.index('sandbox.py'):] = ['isolation_probe.py', '--output', '/output/probe.json']
    (destination/'command.json').write_text(json.dumps(argv, indent=2)+'\n')
    cid = None
    try:
        created = subprocess.run(argv, capture_output=True, text=True, check=True)
        cid = created.stdout.strip()
        if not re.fullmatch(r'[0-9a-f]{64}', cid):
            raise RuntimeError('Unexpected container identifier')
        inspection = json.loads(subprocess.check_output(base+['inspect', cid], text=True))[0]
        (destination/'inspection.json').write_text(json.dumps(inspection, indent=2)+'\n')
        cfg = inspection['HostConfig']
        checks = {
            'network_none': cfg['NetworkMode'] == 'none',
            'read_only': cfg['ReadonlyRootfs'],
            'no_privileged': not cfg['Privileged'],
            'drop_all': cfg['CapDrop'] == ['ALL'],
            'memory': cfg['Memory'] == 268435456,
            'pids': cfg['PidsLimit'] == 64,
            'cpu': cfg['NanoCpus'] == 1000000000,
            'mounts': {(m['Destination'], m['RW']) for m in inspection['Mounts']} == {('/app',False),('/output',True)},
        }
        (destination/'configuration-checks.json').write_text(json.dumps(checks, indent=2)+'\n')
        if not all(checks.values()):
            raise RuntimeError('Effective container configuration differs from intended restrictions')
        result = subprocess.run(base+['start','--attach',cid], capture_output=True, text=True)
        (destination/'stdout.txt').write_text(result.stdout)
        (destination/'stderr.txt').write_text(result.stderr)
        state = json.loads(subprocess.check_output(base+['inspect',cid],text=True))[0]['State']
        (destination/'state.json').write_text(json.dumps(state,indent=2)+'\n')
        if result.returncode or state['ExitCode'] or not (destination/'probe.json').exists():
            raise RuntimeError('Isolation probe failed; inspect preserved logs')
        probe=json.loads((destination/'probe.json').read_text())
        if not probe['passed']:
            raise RuntimeError('One or more probe checks failed')
        report = {'status':'passed within declared checks', 'image':image, 'context':context,
                  'configuration_checks':len(checks), 'probe_checks':len(probe['checks']),
                  'probe_source_sha256':hashlib.sha256((ROOT/'isolation_probe.py').read_bytes()).hexdigest(),
                  'limitation':'Not a general escape-resistance or hostile-code security assessment'}
        (destination/'result.json').write_text(json.dumps(report,indent=2)+'\n')
        return report
    finally:
        if cid and re.fullmatch(r'[0-9a-f]{64}',cid):
            cleanup=subprocess.run(base+['rm','--force',cid],capture_output=True,text=True)
            (destination/'cleanup.json').write_text(json.dumps({'exit_code':cleanup.returncode,'stderr':cleanup.stderr})+'\n')

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--image',required=True)
    parser.add_argument('--context',required=True)
    parser.add_argument('--name',required=True)
    args=parser.parse_args()
    print(json.dumps(execute(args.image,args.context,args.name),indent=2))
